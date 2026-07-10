#!/usr/bin/env python3
"""
神光 Agent 学习合集 —— 增量同步工具
====================================
用途：抓取微信合集(album)中新增的文章，自动编号、生成索引并推送 GitHub。
      已存在的文章会跳过，只提取新内容（幂等，可反复运行）。

运行：
    python3 sync_album.py                 # 同步并推送
    python3 sync_album.py --no-push       # 只同步，不推送
    python3 sync_album.py --cookie-file ~/.wx_cookie.txt

前置条件：
    1. 微信 Cookie 已写入 ~/.wx_cookie.txt（Mac 抓取方法见 README.md）
    2. 本脚本所在仓库目录有 git 远程（首次已配置好）
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

from lxml import etree

# ============================ 配置 ============================
ALBUM_ID = "4306749160512208899"
BIZ = "MzYzNzI2MTI2Nw=="
ALBUM_URL = ("https://mp.weixin.qq.com/mp/appmsgalbum?__biz="
             + BIZ + "&action=getalbum&album_id=" + ALBUM_ID)

# 仓库根目录 = 本脚本上级目录（sync/ 的父目录）
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_COOKIE = os.path.expanduser("~/.wx_cookie.txt")
PAGE_COUNT = 20  # 合集每页文章数（微信上限 20）

WX_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
         "Safari/537.36 MicroMessenger/8.0.20(0x18001432) MacWeChat")


# ====================== 文章解析逻辑（自 skill 移植） ======================
def load_cookie(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return f.read().strip()


def fetch_article(url, cookie):
    """抓取文章 HTML（强制 http→https，修复合集付费校验）"""
    if url.startswith("http://mp.weixin.qq.com"):
        url = "https://" + url[len("http://"):]
    cmd = ["curl", "-sL", "-A", WX_UA,
           "-H", f"Cookie: {cookie}",
           "-H", "Referer: https://mp.weixin.qq.com/", url]
    return subprocess.run(cmd, capture_output=True).stdout


def check_paid(raw_html):
    html = raw_html.decode("utf-8", errors="ignore")
    m = re.search(r"is_paid\s*[:=]\s*['\"]?(\d)", html)
    return bool(m and m.group(1) == "1")


def _br_to_newline(el):
    parts = []
    if el.text:
        parts.append(el.text)
    for child in el:
        tag = child.tag if isinstance(child.tag, str) else None
        parts.append("\n" if tag == "br" else _br_to_newline(child))
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def _extract_code(pre_el):
    code_el = pre_el.find(".//code")
    return _br_to_newline(code_el if code_el is not None else pre_el)


def _fix_code_spacing(code):
    code = re.sub(r"\bfrom([\"'])", r"from \1", code)
    code = re.sub(r"\bimport([\"'])", r"import \1", code)
    code = re.sub(r"\bawait([A-Za-z])", r"await \1", code)
    code = re.sub(r"\breturn([`\"'])", r"return \1", code)
    code = re.sub(r"\)(catch)", r") \1", code)
    code = re.sub(r"\}(catch)", r"} \1", code)
    return code


def _build_vid_mp4_map(html_text):
    html = html_text.replace("\\x26", "&").replace("\\x3c", "<").replace("\\x3e", ">")
    vids = re.findall(r"vid=(wxv_\d+)", html)
    seen, order = set(), []
    for v in vids:
        if v not in seen:
            seen.add(v); order.append(v)
    all_mp4 = re.findall(r"url\s*:\s*'(http://mpvideo\.qpic\.cn/[^']+)'", html)
    seen_base, mp4_list = set(), []
    for u in all_mp4:
        u = u.replace("&amp;", "&")
        m = re.search(r"/([a-z0-9]+)\.f(\d+)\.mp4", u)
        base = m.group(1) if m else u
        q = m.group(2) if m else ""
        if q == "10002" and base not in seen_base:
            seen_base.add(base); mp4_list.append(u)
    vid_map = {}
    for i, v in enumerate(order):
        if i < len(mp4_list):
            vid_map[v] = mp4_list[i]
    return vid_map


def parse_article(raw_html):
    tree = etree.HTML(raw_html)
    jc = tree.xpath('//*[@id="js_content"]')
    if not jc:
        return None, None
    jc = jc[0]
    title = "".join(tree.xpath('//*[@id="activity-name"]//text()')).strip().replace("已付费", "")
    author = "".join(tree.xpath('//*[@id="js_author_name"]//text()')).strip()
    account = "".join(tree.xpath('//*[@id="js_name"]//text()')).strip()
    ct_m = re.search(rb'var\s+ct\s*=\s*"?(\d+)"?', raw_html)
    pubtime = datetime.datetime.fromtimestamp(int(ct_m.group(1))).strftime("%Y-%m-%d") if ct_m else ""
    meta = {"title": title, "author": author, "account": account, "pubtime": pubtime}

    pre_set = set()
    for el in jc.iter():
        if (el.tag if isinstance(el.tag, str) else None) == "pre":
            pre_set.add(id(el))
            for sub in el.iter():
                pre_set.add(id(sub))

    items = []
    for el in jc.iter():
        tag = el.tag if isinstance(el.tag, str) else None
        if tag == "pre":
            code = _extract_code(el).replace("\xa0", " ")
            lines = [l.rstrip() for l in code.split("\n")]
            while lines and not lines[0].strip():
                lines.pop(0)
            while lines and not lines[-1].strip():
                lines.pop()
            items.append(("code", el, "\n".join(lines)))
        elif tag == "img":
            src = el.get("data-src") or el.get("src") or ""
            if "mmbiz" in src:
                items.append(("img", el, src))
        elif tag == "iframe":
            src = el.get("data-src") or el.get("src") or ""
            if "video_player" in src or "mpvideo" in src:
                items.append(("video", el, src))

    BLOCK = {"p", "section", "div", "span", "figure", "figcaption",
             "h1", "h2", "h3", "li", "blockquote", "strong", "em", "b", "i"}
    text_blocks = []
    for el in jc.iter():
        if id(el) in pre_set:
            continue
        tag = el.tag if isinstance(el.tag, str) else None
        if tag in ("img", "br", "script", "style", "code", "iframe") or tag not in BLOCK:
            continue
        if not any((s.tag if isinstance(s.tag, str) else None) in ("pre", "img", "iframe")
                   for s in el.iter()):
            txt = "".join(el.itertext()).replace("\xa0", " ").strip()
            if txt:
                text_blocks.append((el, txt))

    position = {id(el): i for i, el in enumerate(jc.iter())}
    combined = [(position.get(id(el), 0), "text", txt, el) for el, txt in text_blocks]
    for t, el, c in items:
        combined.append((position.get(id(el), 0), t, c, el))
    combined.sort(key=lambda x: x[0])

    merged, seen_texts = [], []
    for pos, t, c, el in combined:
        if t == "text":
            sub = False
            for _, _, _, prev in merged:
                if prev is not el:
                    anc = el.getparent()
                    while anc is not None:
                        if anc is prev:
                            sub = True; break
                        anc = anc.getparent()
                    if sub:
                        break
            if sub or c in seen_texts:
                continue
            if any(c in s for s in seen_texts):
                continue
            seen_texts.append(c)
            if merged and merged[-1][1] == "text":
                merged[-1] = (merged[-1][0], "text", merged[-1][2] + "\n" + c, merged[-1][3])
            else:
                merged.append((pos, "text", c, el))
        else:
            merged.append((pos, t, c, el))

    img_i = vid_i = 0
    final = []
    for pos, t, c, el in merged:
        if t == "img":
            final.append(("img", img_i, c)); img_i += 1
        elif t == "video":
            final.append(("video", vid_i, c)); vid_i += 1
        elif t == "code":
            final.append(("code", c))
        else:
            final.append(("text", c))
    return meta, final


def generate_markdown(meta, blocks, url, vid_map):
    md = [f"# {meta['title']}\n",
          f"> 作者：{meta['author']} ｜ 公众号：{meta['account']} ｜ 发布：{meta['pubtime']}\n",
          f"> 原文链接：{url}\n", "---\n"]
    for item in blocks:
        t = item[0]
        if t == "text":
            md.append(item[1] + "\n")
        elif t == "code":
            md.append(f"```javascript\n{_fix_code_spacing(item[1])}\n```\n")
        elif t == "img":
            md.append(f"![截图{item[1]}]({item[2]})\n")
        elif t == "video":
            vm = re.search(r"vid=(wxv_\d+)", item[2])
            if vm and vm.group(1) in vid_map:
                md.append(f"▶ **[视频{item[1]}]({vid_map[vm.group(1)]})**\n")
            else:
                md.append(f"▶ **[视频{item[1]}]({item[2]})**\n")
    return ("".join(md)).replace("\n总结\n", "\n## 总结\n")


# ====================== 合集列表抓取（游标分页） ======================
def fetch_album_list(cookie):
    """用 begin_msgid+begin_itemidx 游标分页，返回全部文章（已转 https）"""
    articles, seen = [], set()
    cur_msgid = cur_idx = None
    page = 0
    while True:
        params = {"__biz": BIZ, "action": "getalbum", "album_id": ALBUM_ID,
                  "count": PAGE_COUNT, "f": "json"}
        if cur_msgid:
            params["begin_msgid"] = cur_msgid
            params["begin_itemidx"] = cur_idx
        url = ("https://mp.weixin.qq.com/mp/appmsgalbum?"
               + urllib.parse.urlencode(params))
        req = urllib.request.Request(url, headers={
            "User-Agent": WX_UA, "Cookie": cookie,
            "Referer": "https://mp.weixin.qq.com/"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
        resp = data.get("getalbum_resp", {})
        al = resp.get("article_list", [])
        if not al:
            break
        for it in al:
            u = it.get("url", "")
            if u and u not in seen:
                seen.add(u)
                articles.append({
                    "title": it.get("title", ""),
                    "url": u.replace("http://", "https://"),
                    "create_time": int(it.get("create_time", "0") or 0),
                    "msgid": it.get("msgid", ""),
                    "itemidx": it.get("itemidx", ""),
                    "pos_num": int(it.get("pos_num", "0") or 0),
                })
        last = al[-1]
        cur_msgid = last.get("msgid")
        cur_idx = last.get("itemidx")
        page += 1
        print(f"  第{page}页: 累计 {len(articles)} 篇 continue={resp.get('continue_flag')}", flush=True)
        if str(resp.get("continue_flag")) != "1":
            break
        time.sleep(1)
    articles.sort(key=lambda a: a["pos_num"])  # pos_num 升序 = 学习顺序
    return articles


# ====================== 工具 ======================
def safe_title(t):
    return re.sub(r'[\\/:*?"<>|]', "_", t)


def numbered_filename(pos_num, title):
    return f"{pos_num:02d}-{safe_title(title)}.md"


def extract_one(url, cookie):
    raw = fetch_article(url, cookie)
    if not raw:
        raise RuntimeError("抓取为空")
    if not check_paid(raw):
        raise RuntimeError("is_paid!=1（Cookie 过期或无权限）")
    meta, blocks = parse_article(raw)
    if not meta:
        raise RuntimeError("解析失败：无 js_content")
    vid_map = _build_vid_mp4_map(raw.decode("utf-8", errors="ignore"))
    return meta, blocks, generate_markdown(meta, blocks, url, vid_map)


def generate_readme(arts, dir_):
    lines = ["# 神光 Agent 学习\n",
             "> 微信公众号「神光的幸福生活」付费合集全文提取。\n",
             "> 原文合集：" + ALBUM_URL + "\n",
             ">\n> 编号按**学习顺序**排列（01 = 最早/入门，最新在后），建议按序阅读。\n",
             "---\n\n## 目录（学习顺序）\n\n",
             "| 编号 | 标题 | 发布日期 | 代码 | 图片 | 视频 | 文件 |\n",
             "|------|------|---------|------|------|------|------|\n"]
    tc = ti = tv = 0
    for a in arts:
        nn = f"{a['pos_num']:02d}"
        date = datetime.datetime.fromtimestamp(a['create_time']).strftime('%Y-%m-%d')
        fn = numbered_filename(a['pos_num'], a['title'])
        fp = os.path.join(dir_, fn)
        cc = ic = vc = 0
        if os.path.exists(fp):
            txt = open(fp, encoding='utf-8', errors='ignore').read()
            cc = txt.count('```javascript')
            ic = len(re.findall(r'!\[截图\d+\]', txt))
            vc = len(re.findall(r'▶ \*\*\[视频\d+\]', txt))
        tc += cc; ti += ic; tv += vc
        lines.append(f"| {nn} | {a['title']} | {date} | {cc} | {ic} | {vc} | [{fn}](./{fn}) |\n")
    lines += [f"\n---\n\n## 统计\n\n",
              f"- 文章总数：**{len(arts)}** 篇\n",
              f"- 代码块合计：**{tc}** ｜ 图片：**{ti}** ｜ 视频：**{tv}**\n",
              f"- 时间跨度：{datetime.datetime.fromtimestamp(arts[0]['create_time']).strftime('%Y-%m-%d')}"
              f" ~ {datetime.datetime.fromtimestamp(arts[-1]['create_time']).strftime('%Y-%m-%d')}\n",
              f"- 最近同步：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
              f"\n---\n\n## 后续更新\n\n",
              f"本系列仍在更新。作者发布新文章后，运行增量同步即可自动补齐：\n\n",
              f"```bash\npython3 sync/sync_album.py\n```\n\n",
              f"详见 [sync/README.md](./sync/README.md)（含 Cookie 刷新、编号规则、常见问题）。\n"]
    with open(os.path.join(dir_, "README.md"), 'w', encoding='utf-8') as f:
        f.writelines(lines)


# ====================== 主流程 ======================
def main():
    ap = argparse.ArgumentParser(description="神光 Agent 学习合集增量同步")
    ap.add_argument("--cookie-file", default=DEFAULT_COOKIE, help=f"Cookie 文件（默认 {DEFAULT_COOKIE}）")
    ap.add_argument("--no-push", action="store_true", help="只同步，不推送 GitHub")
    ap.add_argument("--delay", type=float, default=1.2, help="每篇间隔秒数")
    args = ap.parse_args()

    cookie = load_cookie(args.cookie_file)
    if not cookie:
        print(f"❌ 未找到 Cookie 文件: {args.cookie_file}")
        print("   请先抓取微信 Cookie 写入该文件（方法见 sync/README.md）")
        sys.exit(1)

    print(f"📁 仓库目录: {REPO_DIR}")
    print("📥 抓取合集文章列表...")
    arts = fetch_album_list(cookie)
    print(f"✅ 合集共 {len(arts)} 篇（pos_num {arts[0]['pos_num']}~{arts[-1]['pos_num']}）\n")

    print("🔍 检查需提取的新文章...")
    new_arts = []
    for a in arts:
        fn = numbered_filename(a['pos_num'], a['title'])
        fp = os.path.join(REPO_DIR, fn)
        if os.path.exists(fp) and os.path.getsize(fp) > 500:
            continue
        new_arts.append(a)
    print(f"   已存在 {len(arts) - len(new_arts)} 篇，需新提取 {len(new_arts)} 篇\n")

    if not new_arts:
        print("✨ 无新文章，仅刷新 README 索引")
        generate_readme(arts, REPO_DIR)
        _git_commit_push(args, new_count=0)
        return

    ok = fail = 0
    for i, a in enumerate(new_arts):
        fn = numbered_filename(a['pos_num'], a['title'])
        try:
            meta, blocks, md = extract_one(a['url'], cookie)
            with open(os.path.join(REPO_DIR, fn), 'w', encoding='utf-8') as f:
                f.write(md)
            ok += 1
            cc = sum(1 for b in blocks if b[0] == 'code')
            print(f"  [{i+1}/{len(new_arts)}] ✅ {fn} | 代码{cc}", flush=True)
        except Exception as e:
            fail += 1
            print(f"  [{i+1}/{len(new_arts)}] ❌ {fn} | {e}", flush=True)
        time.sleep(args.delay)

    print(f"\n提取完成: 成功 {ok} 失败 {fail}")
    generate_readme(arts, REPO_DIR)
    _git_commit_push(args, new_count=ok)


def _git_commit_push(args, new_count):
    print("\n📝 更新 README 索引 ✓")
    if args.no_push:
        print("⏭️  --no-push 已跳过推送")
        return
    try:
        subprocess.run(["git", "-C", REPO_DIR, "add", "-A"], check=True)
        msg = (f"sync: 新增 {new_count} 篇文章" if new_count
               else "sync: 刷新索引")
        msg += f"（{datetime.datetime.now().strftime('%Y-%m-%d')}）"
        subprocess.run(["git", "-C", REPO_DIR, "commit", "-q", "-m", msg],
                       check=True, capture_output=True)
        r = subprocess.run(["git", "-C", REPO_DIR, "push"], capture_output=True, text=True)
        if r.returncode == 0:
            print(f"🚀 已推送 GitHub: {msg}")
        else:
            print(f"⚠️ 推送失败（可能需要配置认证）: {r.stderr.strip()[:100]}")
            print("   可手动执行: cd 神光agent学习 && git push")
    except subprocess.CalledProcessError:
        print("⚠️ git 操作异常，可手动提交")


if __name__ == "__main__":
    main()
