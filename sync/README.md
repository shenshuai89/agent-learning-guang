# 增量同步 Workflow

本目录的工具用于**持续抓取**微信合集「神光的��福生活」中新增的文章。系列未完结，作者发布新文章后，运行一次即可自动补齐。

## 一、前置：刷新微信 Cookie

微信 Cookie 会过期（一般几小时～一天）。每次同步前，需先在 Mac 上重新抓取 Cookie。

### Mac 抓取 Cookie（mitmproxy）

```bash
# 1. 安装并启动代理
brew install mitmproxy
mitmweb                                          # 启动后访问 http://127.0.0.1:8081

# 2. 设置系统代理（新开终端）
sudo networksetup -setwebproxy "Wi-Fi" 127.0.0.1 8080
sudo networksetup -setsecurewebproxy "Wi-Fi" 127.0.0.1 8080

# 3. 首次需信任 mitmproxy 证书
sudo security add-trusted-cert -d -r trustRoot \
  -k /Library/Keychains/System.keychain ~/.mitmproxy/mitmproxy-ca-cert.pem

# 4. 在微信中打开合集里任意一篇付费文章，完整加载
#    在 mitmweb 的 Flow 列表中找到对 mp.weixin.qq.com 的请求，
#    复制其完整 Cookie 头，写入文件：
echo 'wxuin=...; pass_ticket=...; wap_sid2=...; appmsg_token=...' > ~/.wx_cookie.txt

# 5. 恢复代理
sudo networksetup -setwebproxystate "Wi-Fi" off
sudo networksetup -setsecurewebproxystate "Wi-Fi" off
```

> 关键 Cookie 字段：`wxuin`、`pass_ticket`、`wap_sid2`、`appmsg_token`（缺一不可）。

## 二、运行同步

在仓库根目录执行：

```bash
# 标准用法：抓取新文章 + 更新索引 + 推送 GitHub
python3 sync/sync_album.py

# 只抓取不推送
python3 sync/sync_album.py --no-push

# 指定 Cookie 文件位置
python3 sync/sync_album.py --cookie-file /path/to/cookie.txt
```

## 三、脚本会做什么

1. **抓取合集全量列表**：用 `begin_msgid`+`begin_itemidx` 游标分页拿到合集所有文章（修复了 `begin` 偏移不生效的问题）。
2. **比对已存在文件**：以 `pos_num`（合集内稳定序号）作键，文件名格式 `{pos_num:02d}-{标题}.md`。已存在则跳过。
3. **提取新文章**：强制 `http→https`（修复合集付费校验），用微信 UA + Cookie 抓取 `is_paid=1` 的付费全文，解析为 Markdown（正文 / 代码块 / 图片 mmbiz 直链 / 视频 mp4 直链）。
4. **重新生成 README**：按学习顺序（pos_num 升序）生成索引表与统计。
5. **推送 GitHub**：自动 commit + push（可用 `--no-push` 跳过）。

## 四、编号规则

| 规则 | 说明 |
|------|------|
| 编号 = `pos_num` | 合集内每篇文章有固定的 `pos_num`，新文章的 `pos_num` 递增（41、42…），所以新文章自动追加在末尾 |
| 零填充 | `01`-`40`，超过 99 自动变 3 位（`100`） |
| 学习顺序 | pos_num 升序 = 发布时间正序 = 从入门到进阶 |

**幂等**：可反复运行，已存在的文章不会重复提取，编号不会变动。

## 五、常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `is_paid!=1` | Cookie 过期 | 重新抓取 Cookie 写入 `~/.wx_cookie.txt` |
| `参数错误` 页面 | URL 用了 `http://` | 脚本已自动转 `https://`，无需处理 |
| 合集列表只返回 20 篇 | 用了 `begin` 偏移分页（已废弃） | 本脚本用 `begin_msgid` 游标，已修复 |
| 推送失败 `could not read Username` | git 未带认证 | 配置 `GH_TOKEN` 或在仓库设带 token 的 remote URL |
| 新文章没被抓到 | 作者刚发布，合集缓存未更新 | 稍等片刻再跑一次 |

## 六、在 WorkBuddy 中触发（推荐方式）

每次 WorkBuddy 会话是全新沙箱，仓库需重新 clone；Cookie 也会过期，需重新提供。所以触发流程是：

### 触发模板（复制给 WorkBuddy）

> 帮我同步 GitHub 仓库 `Fan-zexu/agent-learning` 的微信合集新文章。
> 步骤：
> 1. `gh repo clone Fan-zexu/agent-learning /workspace/agent-learning`（或 git clone）
> 2. 把下面的微信 Cookie 写入 `~/.wx_cookie.txt`：
>    `wxuin=...; pass_ticket=...; wap_sid2=...; appmsg_token=...`
> 3. 运行 `python3 /workspace/agent-learning/sync/sync_album.py --gh-token <你的GitHub token>`
>
> 微信 Cookie：`<粘贴最新 Cookie>`
> GitHub token：`<粘贴 token，或省略则只同步不推送>`

WorkBuddy 会自动完成 clone → 写 Cookie → 运行同步 → 推送 GitHub，新文章会按 `pos_num` 自动编号追加（如 `41-xxx.md`）。

### 最省事的说法

如果你不想记步骤，直接对 WorkBuddy 说：

> 同步我的 agent-learning 合集，Cookie 是 `<粘贴>`

WorkBuddy 知道这个仓库和脚本，会自己处理 clone 和运行。你只需提供**新鲜的微信 Cookie**（必须）；GitHub token 用于推送（可选，不提供则只在本地生成文件）。

> ⚠️ Cookie 是唯一必须手动刷新的东西——它会过期（一般几小时～一天）。token 不变可一直用。
