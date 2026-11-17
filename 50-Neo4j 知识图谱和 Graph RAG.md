# Neo4j（01） - Neo4j 知识图谱和 Graph RAG

> 读完后，你应能完成以下任务：
> - 绘制“Neo4j（01） - Neo4j 知识图谱和 Graph RAG / 本篇定位”的关键对象与数据流，解释“这是 GraphRAG 专项篇，和 RAG（33）《进阶：GraphRAG 与知识图谱增强》 形成互补。”，并用源码位置、日志或 Trace 标注证据。
> - 为“Neo4j（01） - Neo4j 知识图谱和 Graph RAG / 核心拆解”设计正常与异常输入，验证“Neo4j 存的是节点和关系。”，输出首个偏差位置与回归测试结果。
> - 实现“Neo4j（01） - Neo4j 知识图谱和 Graph RAG / 落地建议”的最小代码或配置，检验“先从小范围核心实体建图，不要全量抽取。”，输出命令、结果与 Diff，并说明不适用边界。

<!-- article-progressive-block:start -->
# 一、先建立全局：Neo4j 知识图谱和 Graph RAG 是什么？

理解“Neo4j 知识图谱和 Graph RAG”，先要把标题中的对象放进同一条处理链：它接收什么输入，经过哪些状态变化，最终用什么证据判断结果。下表不另造概念，只把作者正文已经解释的章节按依赖顺序连起来。

“Neo4j 知识图谱和 Graph RAG”的第一个核心判断是：这是 GraphRAG 专项篇，和 RAG（33）《进阶：GraphRAG 与知识图谱增强》 形成互补。。先弄清这个判断中的对象和输入输出，后面的实现、故障和验收才有共同语境。

| 顺序 | 章节 | 读完本节应抓住的结论 |
| --- | --- | --- |
| 1 | 本篇定位 | 这是 GraphRAG 专项篇，和 RAG（33）《进阶：GraphRAG 与知识图谱增强》 形成互补。 |
| 2 | 核心拆解 | Neo4j 存的是节点和关系。 |
| 3 | 落地建议 | 先从小范围核心实体建图，不要全量抽取。 |
| 4 | 常见坑 | 图谱没有来源，关系无法核验。 |
| 5 | 和已有主线的关系 | ../09-附录/进阶-GraphRAG与知识图谱增强.md 讲思路； |
| 6 | 设计判断 | Graph RAG 最适合“关系先于文本”的问题。 |

## 1.1 核心对象之间怎样衔接

```mermaid
flowchart LR
  S1["本篇定位"] --> S2
  S2["核心拆解"] --> S3
  S3["落地建议"] --> S4
  S4["常见坑"] --> S5
  S5["和已有主线的关系"]
```

这张图只表达本文的讲解顺序，不替代正文机制。判断“Neo4j 知识图谱和 Graph RAG”是否真正掌握，需要能从最后一个结果沿图回到前面每个章节的输入、状态变化和证据。

## 1.2 再看失败：问题最早会出现在哪一步？

在“Neo4j 知识图谱和 Graph RAG”的对象和顺序已经明确后，再看可观察的失败：漏召回、排序丢失、引用断链或越权命中。定位时不从最后一条错误猜原因，而是沿上图找第一个偏离正文结论的节点。
<!-- article-progressive-block:end -->

# 二、Neo4j 知识图谱和 Graph RAG的学习定位与边界

这是 GraphRAG 专项篇，和 RAG（33）《进阶：GraphRAG 与知识图谱增强》 形成互补。

# 三、Neo4j 知识图谱和 Graph RAG的真实应用场景

用户问“设备 A 的 E17 故障和哪个传感器有关，处理步骤是什么”。普通 RAG 可能召回几段相似文本，但关系链不清楚。知识图谱可以把设备、部件、故障码、原因、处理步骤连成图，先走关系，再回原文找证据。

# 四、Neo4j 知识图谱和 Graph RAG的核心对象与机制

- Neo4j 存的是节点和关系。节点可以是设备、人员、公司、故障、条款；关系可以是属于、导致、引用、依赖。
- Graph RAG 不是替代向量 RAG，而是增加一条关系召回路径。图谱找路径，文本 RAG 找证据，模型负责组织回答。
- 图谱建设成本高，适合实体关系明确、多跳问题多、需要证据路径的领域。

# 五、Neo4j 知识图谱和 Graph RAG的工程链路

- 从文档抽取实体和关系。
- 写入 Neo4j。
- 用户问题做实体识别。
- 查询图谱路径。
- 根据路径回查原文证据。
- 结合文本证据生成回答。

# 六、Neo4j 知识图谱和 Graph RAG的落地建议

- 先从小范围核心实体建图，不要全量抽取。
- 图谱关系要能回到原文来源。
- 图查询结果要和 RAG chunk 一起给模型。

# 七、Neo4j 知识图谱和 Graph RAG的常见故障与误区

- 为了显得高级硬上图谱。
- 图谱没有来源，关系无法核验。
- 实体抽取错误后不做人工校正，图越建越脏。

# 八、Neo4j 知识图谱和 Graph RAG在学习路线中的位置

`../09-附录/进阶-GraphRAG与知识图谱增强.md` 讲思路；本篇聚焦 Neo4j 落地链路。

# 九、设计判断

Graph RAG 最适合“关系先于文本”的问题。如果用户只是问制度条款、产品说明，普通 RAG 往往足够；如果用户问 A 和 B 的关系、某故障由哪些部件导致、某公司和哪些项目关联，图谱才开始有明显价值。建图前先列 20 个真实问题，看其中是否大量需要多跳关系和实体消歧。没有这些问题，图谱会变成昂贵的装饰。

# 十、Neo4j 知识图谱和 Graph RAG的核心结论

> Graph RAG 适合多跳关系和实体消歧。Neo4j 存实体关系，向量库保存原文证据，回答时先查关系路径，再回到文本证据。它不是普通 RAG 的替代品，只有关系问题足够多时才值得引入。

<!-- article-progressive-block:start -->
# 十一、动手验证：先跑通 Neo4j 知识图谱和 Graph RAG，再改变一个变量

前面的章节已经建立问题、概念和机制。现在把“Neo4j 知识图谱和 Graph RAG”放进同一套基线中运行；本节不再引入新术语，只验证前文结论能否被复现。

## 11.1 基线与候选只允许一个变量不同

验证“Neo4j 知识图谱和 Graph RAG”时，先固定查询集、语料快照、权限身份、相关性标注。候选方案只能改变本次要验证的变量；如果同时更换数据、依赖和配置，即使结果改善，也不能知道是哪一项产生作用。

执行“Neo4j 知识图谱和 Graph RAG”时，动作是：离线回放检索，保存候选、过滤、排序和引用。原始结果不能只保留截图或汇总分数，必须同步保存：Recall@K、NDCG、引用命中率、无答案误答率、Trace，使下一次复查可以在同一输入上重放。

| 实验要素 | 本文要求 |
| --- | --- |
| 固定条件 | 查询集、语料快照、权限身份、相关性标注 |
| 唯一变量 | 本次候选方案与基线之间的一项明确差异 |
| 原始证据 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 通过阈值 | 证据可回链，指标达基线，权限过滤无泄漏 |
| 立即停止 | 漏召回、排序丢失、引用断链或越权命中 |

## 11.2 执行前先排除不可比较条件

“Neo4j 知识图谱和 Graph RAG”开始前先确认下面四项；任一项不成立，都应先修复实验条件，而不是解释结果。

- 基线能够在“Neo4j 知识图谱和 Graph RAG”的当前环境重复运行。
- 候选只改变一个与“Neo4j 知识图谱和 Graph RAG”结论直接相关的条件。
- “Neo4j 知识图谱和 Graph RAG”的基线和候选使用同一批输入、同一版本依赖与同一通过阈值。
- “Neo4j 知识图谱和 Graph RAG”的原始输出和失败现场不会被重试、格式化或汇总覆盖。

## 11.3 执行后先核对证据完整性

结果出来后先检查证据，再讨论“Neo4j 知识图谱和 Graph RAG”是否通过。缺少中间状态时，最终输出只能说明现象，不能证明机制。

| 检查项 | 当前文章的判定 |
| --- | --- |
| 输入可追溯 | 查询集、语料快照、权限身份、相关性标注 |
| 过程可回放 | 离线回放检索，保存候选、过滤、排序和引用 |
| 结果可审计 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |

“Neo4j 知识图谱和 Graph RAG”的一次合格基线对照按以下顺序执行：

1. 保存“Neo4j 知识图谱和 Graph RAG”基线版本及输入摘要，确认基线本身可以重复运行。
2. 写下“Neo4j 知识图谱和 Graph RAG”候选方案唯一变化的变量，以及它预期影响的指标。
3. 在同一环境执行“Neo4j 知识图谱和 Graph RAG”：离线回放检索，保存候选、过滤、排序和引用。
4. 为“Neo4j 知识图谱和 Graph RAG”保存：Recall@K、NDCG、引用命中率、无答案误答率、Trace。
5. 使用“Neo4j 知识图谱和 Graph RAG”预登记条件判断：证据可回链，指标达基线，权限过滤无泄漏。
6. 如果“Neo4j 知识图谱和 Graph RAG”未通过，不修改第二个变量，先恢复基线并保留失败现场。

# 十二、用一张矩阵验证 Neo4j 知识图谱和 Graph RAG 的关键结论

矩阵按正文顺序列出“Neo4j 知识图谱和 Graph RAG”的结论。一次实验只选择一行，只改变这一行对应的条件；不要把多行合并成一个无法归因的大实验。

| 正文章节 | 已解释的结论 | 本轮唯一变量 | 必须保存的证据 |
| --- | --- | --- | --- |
| 本篇定位 | 这是 GraphRAG 专项篇，和 RAG（33）《进阶：GraphRAG 与知识图谱增强》 形成互补。 | 只改变与“本篇定位”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 核心拆解 | Neo4j 存的是节点和关系。 | 只改变与“核心拆解”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 落地建议 | 先从小范围核心实体建图，不要全量抽取。 | 只改变与“落地建议”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 常见坑 | 图谱没有来源，关系无法核验。 | 只改变与“常见坑”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 和已有主线的关系 | ../09-附录/进阶-GraphRAG与知识图谱增强.md 讲思路； | 只改变与“和已有主线的关系”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 设计判断 | Graph RAG 最适合“关系先于文本”的问题。 | 只改变与“设计判断”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |

## 12.1 记录本次实际实验

下面的记录用于“Neo4j 知识图谱和 Graph RAG”当前这一次实验，不是第二套知识目录。先从矩阵选择一个章节，再填写实际值；没有填写的字段表示尚未验证。

```yaml
topic: "Neo4j 知识图谱和 Graph RAG"
selected_chapter: required
claim_from_article: required
baseline_version: required
changed_condition: exactly_one
execution: "离线回放检索，保存候选、过滤、排序和引用"
evidence: "Recall@K、NDCG、引用命中率、无答案误答率、Trace"
pass_when: "证据可回链，指标达基线，权限过滤无泄漏"
stop_when: "漏召回、排序丢失、引用断链或越权命中"
observed_result: required
first_deviation: null_or_evidence
recovery_replay: required_after_failure
```

## 12.2 边界实验必须证明能够停止和恢复

成功路径只能证明“Neo4j 知识图谱和 Graph RAG”在当前样本上工作，不能证明它可以进入生产。边界实验需要主动制造：漏召回、排序丢失、引用断链或越权命中，并观察系统是否在产生不可逆副作用前停止。

| 场景 | 只改变什么 | 应保存什么 | 通过标准 |
| --- | --- | --- | --- |
| 正常路径 | 使用已知有效输入 | Recall@K、NDCG、引用命中率、无答案误答率、Trace | 证据可回链，指标达基线，权限过滤无泄漏 |
| 边界路径 | 把一个输入推进到约束临界值 | 临界值前后的输出与指标 | 不静默降级，不把部分结果冒充成功 |
| 明确失败 | 注入：漏召回、排序丢失、引用断链或越权命中 | 原始错误、首个异常阶段和最终状态 | 失败被正确分类且没有扩大副作用 |
| 恢复重放 | 执行：定位解析、召回、过滤、排序或生成阶段，回滚对应版本 | 原失败样本的复测证据 | 原样本恢复，正常样本没有回归 |

恢复动作不是简单重启。对于“Neo4j 知识图谱和 Graph RAG”，第一步是：定位解析、召回、过滤、排序或生成阶段，回滚对应版本。完成后使用原始失败样本复测；只验证一个新样本成功，不能证明触发条件已经消失。

“Neo4j 知识图谱和 Graph RAG”边界实验结束后，应把正常、临界、失败和恢复四类记录放在同一个运行批次中。这样才能区分“候选方案真的修复问题”和“环境变化让问题暂时没有出现”。

# 十三、Neo4j 知识图谱和 Graph RAG 的结果解释

解释“Neo4j 知识图谱和 Graph RAG”实验时先看首个偏差，而不是最后一条错误。最后的异常通常只是上游状态错误的结果；从末端反推容易误把症状当根因。

| 观察结果 | 可以支持的判断 | 下一步 |
| --- | --- | --- |
| 主链路没有达到预期 | 漏召回、排序丢失、引用断链或越权命中 | 先执行：定位解析、召回、过滤、排序或生成阶段，回滚对应版本 |
| 异常链路无法恢复 | 漏召回、排序丢失、引用断链或越权命中 | 先执行：定位解析、召回、过滤、排序或生成阶段，回滚对应版本 |
| 新样本成功但原样本仍失败 | 修复没有覆盖原始触发条件 | 固定原失败输入，恢复基线后重新比较 |
| 指标改善但证据无法回链 | 数据、版本或中间状态没有固定 | 暂停发布，补齐可追溯记录后重跑 |

“Neo4j 知识图谱和 Graph RAG”只有同时满足“证据可回链，指标达基线，权限过滤无泄漏”，并且没有出现“漏召回、排序丢失、引用断链或越权命中”，才可以认为主链路通过。这里的“通过”只对当前固定版本、样本和环境有效，不能外推到尚未测试的容量、权限或数据分布。

如果“Neo4j 知识图谱和 Graph RAG”候选方案与基线差异很小，先检查证据分辨率是否足够；如果差异很大，先排除数据泄漏、环境漂移和版本不一致。两种情况都不能只看一个汇总均值，需要回到逐样本输出和中间状态。

“Neo4j 知识图谱和 Graph RAG”故障定位完成后，记录“现象、首个偏差、根因、改动、原样本复测”五项。缺少原样本复测时，只能标记为待观察，不能标记为已解决。

# 十四、Neo4j 知识图谱和 Graph RAG 的发布判断

发布判断需要把“Neo4j 知识图谱和 Graph RAG”的质量、失败边界和恢复能力放在同一份记录中。以下任一条件缺失，都应停止扩量，而不是用“基本正常”替代证据。

- [ ] “Neo4j 知识图谱和 Graph RAG”的基线与候选只存在一个计划内变量。
- [ ] “Neo4j 知识图谱和 Graph RAG”的输入、代码、依赖、配置和数据版本可以追溯。
- [ ] “Neo4j 知识图谱和 Graph RAG”的正常、临界、失败和恢复样本使用同一套断言。
- [ ] “Neo4j 知识图谱和 Graph RAG”的原始输出、中间状态和失败现场已经保留。
- [ ] “Neo4j 知识图谱和 Graph RAG”的日志、Trace、截图和测试数据已经脱敏。
- [ ] “Neo4j 知识图谱和 Graph RAG”的停止条件、负责人和回滚入口已经演练。
- [ ] “Neo4j 知识图谱和 Graph RAG”尚未覆盖的输入、权限、容量和外部依赖已经登记。

最终记录至少包含基线版本、唯一变量、原始证据、首个偏差、恢复复测和发布责任人。没有参与本次修改的人如果不能据此重放“Neo4j 知识图谱和 Graph RAG”的判断，就不能发布。
<!-- article-progressive-block:end -->

# 十五、总结

- **本篇定位**：这是 GraphRAG 专项篇，和 RAG（33）《进阶：GraphRAG 与知识图谱增强》 形成互补。
- **核心拆解**：Neo4j 存的是节点和关系。
- **设计判断**：Graph RAG 最适合“关系先于文本”的问题。
- **复述答法**：Graph RAG 适合多跳关系和实体消歧。

## 参考资料

- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [Neo4j GraphRAG for Python](https://neo4j.com/docs/neo4j-graphrag-python/current/)

<!-- knowledge-scenario-inlined:AA-15 -->

## 15.1 可运行实验：GraphRAG 实体关系与路径召回


```html runnable file=index.html title="GraphRAG 实体关系与路径召回" description="调整参数并对比正常路径与典型失败路径"
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>AA-15 在线实验</title>
  <style>
    :root{color-scheme:dark;font-family:Inter,system-ui,sans-serif}*{box-sizing:border-box}body{margin:0;background:#0f1211;color:#e7ece9;font-size:13px}.shell{padding:16px}.top{display:flex;justify-content:space-between;gap:16px;margin-bottom:14px}h1{margin:3px 0;font-size:18px}.id,.value{color:#68e0b5;font-family:ui-monospace,monospace}.summary{margin:4px 0;color:#a5afa9}.run{border:0;border-radius:6px;background:#68e0b5;color:#07110d;padding:8px 14px;font-weight:700}.grid{display:grid;grid-template-columns:minmax(220px,.8fr) minmax(0,1.8fr);gap:12px}.panel{border:1px solid #29322e;background:#141817;padding:12px}.control{display:grid;gap:5px;margin-bottom:11px}.head{display:flex;justify-content:space-between;gap:8px}select,input{width:100%;accent-color:#68e0b5;background:#0d100f;color:#e7ece9}.toggle{display:flex;justify-content:space-between;border-top:1px solid #29322e;padding-top:9px}.toggle input{width:18px}.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px}.metric{border:1px solid #29322e;padding:8px}.metric b{display:block;color:#68e0b5;font-size:16px}.stages{display:flex;gap:6px;overflow:auto;margin:10px 0}.stage{border:1px solid #8a6230;padding:7px;min-width:90px}.stage.ok{border-color:#367a61}.stage.fail{border-color:#8b4545}table{width:100%;border-collapse:collapse}td{border-top:1px solid #29322e;padding:7px}.diagnosis{margin-top:9px;border-left:3px solid #68e0b5;background:#101412;padding:9px;line-height:1.5}.danger{border-color:#ef7f7f}@media(max-width:680px){.top,.grid{display:grid;grid-template-columns:1fr}.metrics{grid-template-columns:repeat(2,1fr)}}
  </style>
</head>
<body>
  <main class="shell">
    <header class="top"><div><div class="id">AA-15 · DETERMINISTIC LAB</div><h1 id="title"></h1><p class="summary" id="summary"></p></div><button class="run" id="run">运行实验</button></header>
    <section class="grid"><div class="panel"><div id="controls"></div><label class="toggle"><span>注入典型故障</span><input id="failure" type="checkbox"></label></div><div class="panel"><div class="metrics" id="metrics"></div><div class="stages" id="stages"></div><table><tbody id="rows"></tbody></table><div class="diagnosis" id="diagnosis"></div></div></section>
  </main>
  <script>
    const scenario = { title: 'GraphRAG 实体关系与路径召回', summary: '比较向量候选、图路径和社区摘要对多跳问题的证据贡献。', controls: [
    { key: 'hops', label: '图遍历深度', type: 'range', min: 1, max: 5, value: 2, suffix: ' hops' },
    { key: 'graphWeight', label: '图路径权重', type: 'range', min: 0, max: 100, step: 10, value: 60, suffix: '%' },
    { key: 'community', label: '社区摘要', type: 'select', value: 'on', options: [['off', '关闭'], ['on', '开启']] }
  ] };
    const controls = document.querySelector('#controls');
    const failure = document.querySelector('#failure');
    document.querySelector('#title').textContent = scenario.title;
    document.querySelector('#summary').textContent = scenario.summary;
    function renderControl(control) {
      const label = document.createElement('label'); label.className = 'control';
      const head = document.createElement('span'); head.className = 'head'; head.innerHTML = '<span>' + control.label + '</span><span class="value" data-value="' + control.key + '"></span>'; label.appendChild(head);
      const input = document.createElement(control.type === 'select' ? 'select' : 'input'); input.dataset.key = control.key;
      if (control.type === 'select') control.options.forEach(option => { const item = document.createElement('option'); item.value = option[0]; item.textContent = option[1]; item.selected = option[0] === control.value; input.appendChild(item); });
      else { input.type = 'range'; input.min = control.min; input.max = control.max; input.step = control.step || 1; input.value = control.value; }
      input.addEventListener('input', updateValues); label.appendChild(input); return label;
    }
    function updateValues() { scenario.controls.forEach(control => { const input = controls.querySelector('[data-key="' + control.key + '"]'); document.querySelector('[data-value="' + control.key + '"]').textContent = control.type === 'select' ? input.options[input.selectedIndex].text : input.value + (control.suffix || ''); }); }
    function readValues() { const values = {}; scenario.controls.forEach(control => { const input = controls.querySelector('[data-key="' + control.key + '"]'); values[control.key] = control.type === 'range' ? Number(input.value) : input.value; }); values.failure = failure.checked; return values; }
    function stage(name, state, detail) { return { name, state, detail }; }
    const aiStage = stage;
    function clamp(value, minimum, maximum) { return Math.min(maximum, Math.max(minimum, value)); }
    function simulate(values) { const fail = values.failure;
      /** 图遍历深度带来的候选路径数量。 */
      const paths = Math.pow(3, values.hops);
      /** 向量和图路径加权后的多跳命中率。 */
      const hitRate = clamp(62 + values.hops * 7 + values.graphWeight * 0.12 + (values.community === 'on' ? 6 : 0) - (values.hops > 3 ? (values.hops - 3) * 8 : 0) - (fail ? 18 : 0), 0, 98);
      /** 遍历和社区摘要带来的估算延迟。 */
      const latency = 90 + paths * 4 + (values.community === 'on' ? 80 : 0);
      return { metrics: [[paths, '候选路径'], [hitRate.toFixed(1) + '%', '多跳命中'], [latency + 'ms', '图检索延迟'], [values.graphWeight + '%', '图证据权重']], stages: [aiStage('实体抽取', fail ? 'fail' : 'ok', fail ? 'alias missing' : 'entities'), aiStage('向量召回', 'ok', 'top 10'), aiStage('图遍历', values.hops > 3 ? 'warn' : 'ok', values.hops + ' hops'), aiStage('社区摘要', values.community === 'on' ? 'ok' : 'warn', values.community), aiStage('证据融合', hitRate >= 75 ? 'ok' : 'warn', hitRate.toFixed(1))], rows: [['适用问题', '组织关系、依赖链、人物事件等需要跨文档多跳的问题'], ['路径爆炸', values.hops > 3 ? '候选指数增长，应限制关系类型、时间和最大路径数' : '遍历深度可控'], ['实体对齐', fail ? '同一实体别名未归一，路径断裂' : '实体 ID、别名和来源均可追溯']], diagnosis: fail ? '实体对齐失败，增加遍历深度只会放大噪声。' : hitRate >= 75 ? '向量、图路径和社区摘要提供互补证据。' : '应调整图权重、遍历范围或实体抽取。', danger: fail };
     }
    function render() { const result = simulate(readValues()); document.querySelector('#metrics').innerHTML = result.metrics.map(item => '<div class="metric"><b>' + item[0] + '</b><span>' + item[1] + '</span></div>').join(''); document.querySelector('#stages').innerHTML = result.stages.map(item => '<div class="stage ' + item.state + '"><b>' + item.name + '</b><div>' + item.detail + '</div></div>').join(''); document.querySelector('#rows').innerHTML = result.rows.map(item => '<tr><td>' + item[0] + '</td><td>' + item[1] + '</td></tr>').join(''); const diagnosis = document.querySelector('#diagnosis'); diagnosis.textContent = result.diagnosis; diagnosis.className = 'diagnosis' + (result.danger ? ' danger' : ''); }
    scenario.controls.forEach(control => controls.appendChild(renderControl(control))); updateValues(); document.querySelector('#run').addEventListener('click', render); render();
  </script>
</body>
</html>
```


# Neo4j（02） - Neo4j GraphRAG：受控多跳检索与证据回链

> 读完后，你应能：
> - 能验证“向量检索擅长找语义相近 Chunk，知识图谱擅长回答显式关系问题，例如“服务 A 依赖哪些组件，这些组件由谁维护””，并保存输入、输出与失败样本。
> - 能验证“GraphRAG 的价值不是把所有文本变成节点，而是用稳定实体和关系补足多跳结构，再回链到原始证据”，并保存输入、输出与失败样本。
> - 能验证“节点使用 (tenant_id, entity_id) 唯一约束，名称只是可变属性”，并保存输入、输出与失败样本。


向量检索擅长找语义相近 Chunk，知识图谱擅长回答显式关系问题，例如“服务 A 依赖哪些组件，这些组件由谁维护”。GraphRAG 的价值不是把所有文本变成节点，而是用稳定实体和关系补足多跳结构，再回链到原始证据。

```mermaid
graph LR
    D[Document] -->|HAS_CHUNK| C[Chunk]
    C -->|MENTIONS| S[Service]
    S -->|DEPENDS_ON| K[Component]
    T[Team] -->|OWNS| K
    C -->|SOURCE| P[Page/URI]
    U[User ACL] -->|FILTER| D
```

<!-- article-progressive-block:start -->
# 一、先建立全局：Neo4j GraphRAG：受控多跳检索与证据回链 是什么？

理解“Neo4j GraphRAG：受控多跳检索与证据回链”，先要把标题中的对象放进同一条处理链：它接收什么输入，经过哪些状态变化，最终用什么证据判断结果。下表不另造概念，只把作者正文已经解释的章节按依赖顺序连起来。

“Neo4j GraphRAG：受控多跳检索与证据回链”的第一个核心判断是：节点使用 (tenant_id, entity_id) 唯一约束，名称只是可变属性。。先弄清这个判断中的对象和输入输出，后面的实现、故障和验收才有共同语境。

| 顺序 | 章节 | 读完本节应抓住的结论 |
| --- | --- | --- |
| 1 | 建模原则 | 节点使用 (tenant_id, entity_id) 唯一约束，名称只是可变属性。 |
| 2 | 参数化写入与查询 | 自然语言应先解析为受控意图和实体 ID，不要让 LLM 直接生成并执行任意 Cypher。 |
| 3 | 与混合检索协作 | 推荐顺序是：BM25/向量召回种子 Chunk → 实体链接 → 有界图扩展 → 取回支持关系的 Chunk → 与原候选融合和 Rerank。 |
| 4 | 安全、稳定与成本 | 所有入口强制租户与 ACL 条件，缓存键包含权限摘要和图谱版本。 |
| 5 | 验收 | 至少准备一跳、两跳、同名实体、跨租户和关系已过期五类问题； |
| 6 | 向量检索擅长找语义相近 Chunk | 向量检索擅长找语义相近 Chunk，知识图谱擅长回答显式关系问题，例如“服务 A 依赖哪些组件，这些组件由谁维护”。 |

## 1.1 核心对象之间怎样衔接

```mermaid
flowchart LR
  S1["建模原则"] --> S2
  S2["参数化写入与查询"] --> S3
  S3["与混合检索协作"] --> S4
  S4["安全、稳定与成本"] --> S5
  S5["验收"]
```

这张图只表达本文的讲解顺序，不替代正文机制。判断“Neo4j GraphRAG：受控多跳检索与证据回链”是否真正掌握，需要能从最后一个结果沿图回到前面每个章节的输入、状态变化和证据。

## 1.2 再看失败：问题最早会出现在哪一步？

在“Neo4j GraphRAG：受控多跳检索与证据回链”的对象和顺序已经明确后，再看可观察的失败：漏召回、排序丢失、引用断链或越权命中。定位时不从最后一条错误猜原因，而是沿上图找第一个偏离正文结论的节点。
<!-- article-progressive-block:end -->

# 二、建模原则

- 节点使用 `(tenant_id, entity_id)` 唯一约束，名称只是可变属性。
- 关系类型使用受控枚举，禁止模型随意创造标签和关系名。
- `Chunk` 保存证据 ID 与摘要，不复制完整附件；原文由对象存储提供。
- 每条实体/关系记录来源 Chunk、抽取模型版本和置信度，低置信关系需要复核。

```cypher
CREATE CONSTRAINT service_identity IF NOT EXISTS
FOR (service:Service)
REQUIRE (service.tenant_id, service.entity_id) IS UNIQUE;

CREATE CONSTRAINT chunk_identity IF NOT EXISTS
FOR (chunk:Chunk)
REQUIRE (chunk.tenant_id, chunk.chunk_id) IS UNIQUE;
```

# 三、参数化写入与查询

```text
# requirements.txt
neo4j>=5,<7
```

```python
from __future__ import annotations

from dataclasses import dataclass

from neo4j import Driver


# 多跳查询允许的最大依赖深度，避免无界遍历。
MAX_GRAPH_DEPTH = 3
# 单次最多返回的证据数量，限制上下文成本。
MAX_EVIDENCE_COUNT = 20


@dataclass(frozen=True)
class GraphSearchContext:
    """保存 GraphRAG 查询所需的可信身份条件。"""

    # 当前租户稳定标识。
    tenant_id: str
    # 用户可访问的权限组。
    acl_groups: tuple[str, ...]


def find_dependency_evidence(
    driver: Driver,
    service_id: str,
    context: GraphSearchContext,
) -> list[dict[str, object]]:
    """查询服务依赖及证据；service_id 是实体 ID，context 是权限上下文。"""

    # Cypher 模板固定关系和深度，模型只能提供经过校验的实体 ID。
    query = f"""
    MATCH (service:Service {{tenant_id: $tenant_id, entity_id: $service_id}})
          -[:DEPENDS_ON*1..{MAX_GRAPH_DEPTH}]->(component:Component)
    MATCH (chunk:Chunk)-[:MENTIONS]->(component)
    MATCH (document:Document)-[:HAS_CHUNK]->(chunk)
    WHERE document.tenant_id = $tenant_id
      AND any(group IN document.acl_groups WHERE group IN $acl_groups)
    OPTIONAL MATCH (team:Team)-[:OWNS]->(component)
    RETURN DISTINCT component.entity_id AS component_id,
           component.name AS component_name,
           team.name AS owner,
           chunk.chunk_id AS chunk_id,
           chunk.source_uri AS source_uri
    LIMIT $limit
    """
    # 参数来自服务端实体解析和鉴权结果，不拼接用户自然语言。
    parameters = {
        "tenant_id": context.tenant_id,
        "service_id": service_id,
        "acl_groups": list(context.acl_groups),
        "limit": MAX_EVIDENCE_COUNT,
    }
    # 结果转换为普通字典，便于与 BM25/向量候选统一融合。
    records, _, _ = driver.execute_query(
        query,
        parameters_=parameters,
        database_="neo4j",
    )
    return [record.data() for record in records]
```

示例为了固定深度把常量插入查询模板；它不是用户输入。自然语言应先解析为受控意图和实体 ID，不要让 LLM 直接生成并执行任意 Cypher。

# 四、与混合检索协作

推荐顺序是：BM25/向量召回种子 Chunk → 实体链接 → 有界图扩展 → 取回支持关系的 Chunk → 与原候选融合和 Rerank。图谱返回“关系”，最终给模型的仍应是有页码、版本和 ACL 的原始证据。

图召回单独评估：实体链接准确率、多跳路径命中率、证据回链率和权限泄漏率。不要只看最终答案，否则无法区分错误来自实体抽取、图关系、证据回链还是生成。

# 五、安全、稳定与成本

- 查询模板白名单化，限制关系类型、深度、返回量和超时；执行只读账号。
- 所有入口强制租户与 ACL 条件，缓存键包含权限摘要和图谱版本。
- 关系抽取只处理对业务有价值的实体类型，控制 LLM 成本和图规模。
- 图数据库不可用时可降级为 BM25 + 向量，但 Trace 明确记录图召回缺失。
- 定期对账孤儿 Chunk、无来源关系、低置信边和已删除文档引用。

# 六、验收

至少准备一跳、两跳、同名实体、跨租户和关系已过期五类问题；每条图路径都能回到可见 Chunk；无界 Cypher 无法执行；索引删除后图节点与关系按版本清理；图召回对最终 Recall 的增益大于其延迟与维护成本。

<!-- article-progressive-block:start -->
# 七、动手验证：先跑通 Neo4j GraphRAG：受控多跳检索与证据回链，再改变一个变量

前面的章节已经建立问题、概念和机制。现在把“Neo4j GraphRAG：受控多跳检索与证据回链”放进同一套基线中运行；本节不再引入新术语，只验证前文结论能否被复现。

## 7.1 基线与候选只允许一个变量不同

验证“Neo4j GraphRAG：受控多跳检索与证据回链”时，先固定查询集、语料快照、权限身份、相关性标注。候选方案只能改变本次要验证的变量；如果同时更换数据、依赖和配置，即使结果改善，也不能知道是哪一项产生作用。

执行“Neo4j GraphRAG：受控多跳检索与证据回链”时，动作是：离线回放检索，保存候选、过滤、排序和引用。原始结果不能只保留截图或汇总分数，必须同步保存：Recall@K、NDCG、引用命中率、无答案误答率、Trace，使下一次复查可以在同一输入上重放。

| 实验要素 | 本文要求 |
| --- | --- |
| 固定条件 | 查询集、语料快照、权限身份、相关性标注 |
| 唯一变量 | 本次候选方案与基线之间的一项明确差异 |
| 原始证据 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 通过阈值 | 证据可回链，指标达基线，权限过滤无泄漏 |
| 立即停止 | 漏召回、排序丢失、引用断链或越权命中 |

## 7.2 执行前先排除不可比较条件

“Neo4j GraphRAG：受控多跳检索与证据回链”开始前先确认下面四项；任一项不成立，都应先修复实验条件，而不是解释结果。

- 基线能够在“Neo4j GraphRAG：受控多跳检索与证据回链”的当前环境重复运行。
- 候选只改变一个与“Neo4j GraphRAG：受控多跳检索与证据回链”结论直接相关的条件。
- “Neo4j GraphRAG：受控多跳检索与证据回链”的基线和候选使用同一批输入、同一版本依赖与同一通过阈值。
- “Neo4j GraphRAG：受控多跳检索与证据回链”的原始输出和失败现场不会被重试、格式化或汇总覆盖。

## 7.3 执行后先核对证据完整性

结果出来后先检查证据，再讨论“Neo4j GraphRAG：受控多跳检索与证据回链”是否通过。缺少中间状态时，最终输出只能说明现象，不能证明机制。

| 检查项 | 当前文章的判定 |
| --- | --- |
| 输入可追溯 | 查询集、语料快照、权限身份、相关性标注 |
| 过程可回放 | 离线回放检索，保存候选、过滤、排序和引用 |
| 结果可审计 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |

“Neo4j GraphRAG：受控多跳检索与证据回链”的一次合格基线对照按以下顺序执行：

1. 保存“Neo4j GraphRAG：受控多跳检索与证据回链”基线版本及输入摘要，确认基线本身可以重复运行。
2. 写下“Neo4j GraphRAG：受控多跳检索与证据回链”候选方案唯一变化的变量，以及它预期影响的指标。
3. 在同一环境执行“Neo4j GraphRAG：受控多跳检索与证据回链”：离线回放检索，保存候选、过滤、排序和引用。
4. 为“Neo4j GraphRAG：受控多跳检索与证据回链”保存：Recall@K、NDCG、引用命中率、无答案误答率、Trace。
5. 使用“Neo4j GraphRAG：受控多跳检索与证据回链”预登记条件判断：证据可回链，指标达基线，权限过滤无泄漏。
6. 如果“Neo4j GraphRAG：受控多跳检索与证据回链”未通过，不修改第二个变量，先恢复基线并保留失败现场。

# 八、用一张矩阵验证 Neo4j GraphRAG：受控多跳检索与证据回链 的关键结论

矩阵按正文顺序列出“Neo4j GraphRAG：受控多跳检索与证据回链”的结论。一次实验只选择一行，只改变这一行对应的条件；不要把多行合并成一个无法归因的大实验。

| 正文章节 | 已解释的结论 | 本轮唯一变量 | 必须保存的证据 |
| --- | --- | --- | --- |
| 建模原则 | 节点使用 (tenant_id, entity_id) 唯一约束，名称只是可变属性。 | 只改变与“建模原则”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 参数化写入与查询 | 自然语言应先解析为受控意图和实体 ID，不要让 LLM 直接生成并执行任意 Cypher。 | 只改变与“参数化写入与查询”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 与混合检索协作 | 推荐顺序是：BM25/向量召回种子 Chunk → 实体链接 → 有界图扩展 → 取回支持关系的 Chunk → 与原候选融合和 Rerank。 | 只改变与“与混合检索协作”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 安全、稳定与成本 | 所有入口强制租户与 ACL 条件，缓存键包含权限摘要和图谱版本。 | 只改变与“安全、稳定与成本”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 验收 | 至少准备一跳、两跳、同名实体、跨租户和关系已过期五类问题； | 只改变与“验收”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 向量检索擅长找语义相近 Chunk | 向量检索擅长找语义相近 Chunk，知识图谱擅长回答显式关系问题，例如“服务 A 依赖哪些组件，这些组件由谁维护”。 | 只改变与“向量检索擅长找语义相近 Chunk”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |

## 8.1 记录本次实际实验

下面的记录用于“Neo4j GraphRAG：受控多跳检索与证据回链”当前这一次实验，不是第二套知识目录。先从矩阵选择一个章节，再填写实际值；没有填写的字段表示尚未验证。

```yaml
topic: "Neo4j GraphRAG：受控多跳检索与证据回链"
selected_chapter: required
claim_from_article: required
baseline_version: required
changed_condition: exactly_one
execution: "离线回放检索，保存候选、过滤、排序和引用"
evidence: "Recall@K、NDCG、引用命中率、无答案误答率、Trace"
pass_when: "证据可回链，指标达基线，权限过滤无泄漏"
stop_when: "漏召回、排序丢失、引用断链或越权命中"
observed_result: required
first_deviation: null_or_evidence
recovery_replay: required_after_failure
```

## 8.2 边界实验必须证明能够停止和恢复

成功路径只能证明“Neo4j GraphRAG：受控多跳检索与证据回链”在当前样本上工作，不能证明它可以进入生产。边界实验需要主动制造：漏召回、排序丢失、引用断链或越权命中，并观察系统是否在产生不可逆副作用前停止。

| 场景 | 只改变什么 | 应保存什么 | 通过标准 |
| --- | --- | --- | --- |
| 正常路径 | 使用已知有效输入 | Recall@K、NDCG、引用命中率、无答案误答率、Trace | 证据可回链，指标达基线，权限过滤无泄漏 |
| 边界路径 | 把一个输入推进到约束临界值 | 临界值前后的输出与指标 | 不静默降级，不把部分结果冒充成功 |
| 明确失败 | 注入：漏召回、排序丢失、引用断链或越权命中 | 原始错误、首个异常阶段和最终状态 | 失败被正确分类且没有扩大副作用 |
| 恢复重放 | 执行：定位解析、召回、过滤、排序或生成阶段，回滚对应版本 | 原失败样本的复测证据 | 原样本恢复，正常样本没有回归 |

恢复动作不是简单重启。对于“Neo4j GraphRAG：受控多跳检索与证据回链”，第一步是：定位解析、召回、过滤、排序或生成阶段，回滚对应版本。完成后使用原始失败样本复测；只验证一个新样本成功，不能证明触发条件已经消失。

“Neo4j GraphRAG：受控多跳检索与证据回链”边界实验结束后，应把正常、临界、失败和恢复四类记录放在同一个运行批次中。这样才能区分“候选方案真的修复问题”和“环境变化让问题暂时没有出现”。

# 九、Neo4j GraphRAG：受控多跳检索与证据回链 的结果解释

解释“Neo4j GraphRAG：受控多跳检索与证据回链”实验时先看首个偏差，而不是最后一条错误。最后的异常通常只是上游状态错误的结果；从末端反推容易误把症状当根因。

| 观察结果 | 可以支持的判断 | 下一步 |
| --- | --- | --- |
| 主链路没有达到预期 | 漏召回、排序丢失、引用断链或越权命中 | 先执行：定位解析、召回、过滤、排序或生成阶段，回滚对应版本 |
| 异常链路无法恢复 | 漏召回、排序丢失、引用断链或越权命中 | 先执行：定位解析、召回、过滤、排序或生成阶段，回滚对应版本 |
| 新样本成功但原样本仍失败 | 修复没有覆盖原始触发条件 | 固定原失败输入，恢复基线后重新比较 |
| 指标改善但证据无法回链 | 数据、版本或中间状态没有固定 | 暂停发布，补齐可追溯记录后重跑 |

“Neo4j GraphRAG：受控多跳检索与证据回链”只有同时满足“证据可回链，指标达基线，权限过滤无泄漏”，并且没有出现“漏召回、排序丢失、引用断链或越权命中”，才可以认为主链路通过。这里的“通过”只对当前固定版本、样本和环境有效，不能外推到尚未测试的容量、权限或数据分布。

如果“Neo4j GraphRAG：受控多跳检索与证据回链”候选方案与基线差异很小，先检查证据分辨率是否足够；如果差异很大，先排除数据泄漏、环境漂移和版本不一致。两种情况都不能只看一个汇总均值，需要回到逐样本输出和中间状态。

“Neo4j GraphRAG：受控多跳检索与证据回链”故障定位完成后，记录“现象、首个偏差、根因、改动、原样本复测”五项。缺少原样本复测时，只能标记为待观察，不能标记为已解决。

# 十、Neo4j GraphRAG：受控多跳检索与证据回链 的发布判断

发布判断需要把“Neo4j GraphRAG：受控多跳检索与证据回链”的质量、失败边界和恢复能力放在同一份记录中。以下任一条件缺失，都应停止扩量，而不是用“基本正常”替代证据。

- [ ] “Neo4j GraphRAG：受控多跳检索与证据回链”的基线与候选只存在一个计划内变量。
- [ ] “Neo4j GraphRAG：受控多跳检索与证据回链”的输入、代码、依赖、配置和数据版本可以追溯。
- [ ] “Neo4j GraphRAG：受控多跳检索与证据回链”的正常、临界、失败和恢复样本使用同一套断言。
- [ ] “Neo4j GraphRAG：受控多跳检索与证据回链”的原始输出、中间状态和失败现场已经保留。
- [ ] “Neo4j GraphRAG：受控多跳检索与证据回链”的日志、Trace、截图和测试数据已经脱敏。
- [ ] “Neo4j GraphRAG：受控多跳检索与证据回链”的停止条件、负责人和回滚入口已经演练。
- [ ] “Neo4j GraphRAG：受控多跳检索与证据回链”尚未覆盖的输入、权限、容量和外部依赖已经登记。

最终记录至少包含基线版本、唯一变量、原始证据、首个偏差、恢复复测和发布责任人。没有参与本次修改的人如果不能据此重放“Neo4j GraphRAG：受控多跳检索与证据回链”的判断，就不能发布。
<!-- article-progressive-block:end -->

# 十一、总结

- **建模原则**：节点使用 (tenant_id, entity_id) 唯一约束，名称只是可变属性。
- **参数化写入与查询**：自然语言应先解析为受控意图和实体 ID，不要让 LLM 直接生成并执行任意 Cypher。
- **与混合检索协作**：推荐顺序是：BM25/向量召回种子 Chunk → 实体链接 → 有界图扩展 → 取回支持关系的 Chunk → 与原候选融合和 Rerank。
- **安全、稳定与成本**：所有入口强制租户与 ACL 条件，缓存键包含权限摘要和图谱版本。
- **验收**：至少准备一跳、两跳、同名实体、跨租户和关系已过期五类问题；

## 参考资料

- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [Neo4j GraphRAG Python Package](https://neo4j.com/docs/neo4j-graphrag-python/current/)



# Neo4j（03） - Neo4j 增量更新与安全删除：保持 GraphRAG 一致

> 读完后，你应能：
> - 能验证“GraphRAG 同时依赖原文、Chunk、向量索引和图关系”，并保存输入、输出与失败样本。
> - 能验证“直接执行 DETACH DELETE 虽然能删节点，却可能留下向量库孤儿记录、缓存旧答案和无法审计的数据空洞”，并保存输入、输出与失败样本。
> - 能验证“生产更新要围绕稳定 ID、版本和可重试事件设计”，并保存输入、输出与失败样本。


GraphRAG 同时依赖原文、Chunk、向量索引和图关系。直接执行 `DETACH DELETE` 虽然能删节点，却可能留下向量库孤儿记录、缓存旧答案和无法审计的数据空洞。生产更新要围绕稳定 ID、版本和可重试事件设计。

```mermaid
flowchart LR
    S[源文档变更] --> E[Outbox 事件]
    E --> N[Neo4j MERGE/软删除]
    E --> V[VectorDB 更新/删除]
    E --> X[ES 更新/删除]
    N --> R[一致性对账]
    V --> R
    X --> R
    R -->|通过| C[切换可见版本]
    R -->|失败| Q[重试队列]
```

<!-- article-progressive-block:start -->
# 一、先建立全局：Neo4j 增量更新与安全删除：保持 GraphRAG 一致 是什么？

理解“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”，先要把标题中的对象放进同一条处理链：它接收什么输入，经过哪些状态变化，最终用什么证据判断结果。下表不另造概念，只把作者正文已经解释的章节按依赖顺序连起来。

“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”的第一个核心判断是：version 用于拒绝乱序事件；。先弄清这个判断中的对象和输入输出，后面的实现、故障和验收才有共同语境。

| 顺序 | 章节 | 读完本节应抓住的结论 |
| --- | --- | --- |
| 1 | 数据模型与删除语义 | version 用于拒绝乱序事件； |
| 2 | 增量一致性与跨存储对账 | 任何一步失败都可依据墓碑重试。 |
| 3 | 权限与成本 | 图中保留实体与关系，Chunk 通过稳定 ID 回链，可显著降低存储和遍历成本。 |
| 4 | 验收 | 对账失败可定位到具体 document_id 和索引版本。 |
| 5 | GraphRAG 同时依赖原文、Chunk、向量索引和图关系 | GraphRAG 同时依赖原文、Chunk、向量索引和图关系。 |
| 6 | 直接执行 DETACH DELETE 虽然能删节点 | 直接执行 DETACH DELETE 虽然能删节点，却可能留下向量库孤儿记录、缓存旧答案和无法审计的数据空洞。 |

## 1.1 核心对象之间怎样衔接

```mermaid
flowchart LR
  S1["数据模型与删除语义"] --> S2
  S2["增量一致性与跨存储对账"] --> S3
  S3["权限与成本"] --> S4
  S4["验收"] --> S5
  S5["GraphRAG 同时依赖原文、Chunk、向量索引和图关系"]
```

这张图只表达本文的讲解顺序，不替代正文机制。判断“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”是否真正掌握，需要能从最后一个结果沿图回到前面每个章节的输入、状态变化和证据。

## 1.2 再看失败：问题最早会出现在哪一步？

在“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”的对象和顺序已经明确后，再看可观察的失败：漏召回、排序丢失、引用断链或越权命中。定位时不从最后一条错误猜原因，而是沿上图找第一个偏离正文结论的节点。
<!-- article-progressive-block:end -->

# 二、数据模型与删除语义

- `document_id`、`entity_id` 使用业务稳定 ID，不依赖 Neo4j 内部节点 ID。
- `version` 用于拒绝乱序事件；`updated_at` 用于审计，不代替版本比较。
- 用户删除默认写入 `deleted_at` 形成墓碑；完成下游清理并超过恢复窗口后再物理删除。
- 权限关系变化也要发布事件，因为图谱、ES 和向量库都保存可见性字段。

# 三、可运行的幂等写入

```text
# requirements.txt
neo4j>=5,<7
```

```python
from __future__ import annotations

import os
from dataclasses import dataclass

from neo4j import Driver, GraphDatabase


# Neo4j 连接配置从环境变量加载，生产环境应使用 Secret 管理。
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
# 数据库用户名只用于当前示例连接。
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
# 密码没有安全默认值，缺失时立即失败。
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]


@dataclass(frozen=True)
class EntityEvent:
    """保存实体变更事件；version 保证重复和乱序消费安全。"""

    # 业务域内稳定实体 ID。
    entity_id: str
    # 当前租户 ID，用于查询过滤和隔离。
    tenant_id: str
    # 实体显示名称。
    name: str
    # 单调递增的源数据版本。
    version: int
    # 是否为删除事件。
    deleted: bool


def apply_entity_event(driver: Driver, event: EntityEvent) -> None:
    """幂等应用实体事件；driver 是连接池，event 是源系统变更。"""

    # 参数化 Cypher 避免拼接注入，并只接受更新版本大于现有版本的事件。
    query = """
    MERGE (entity:Entity {tenant_id: $tenant_id, entity_id: $entity_id})
    ON CREATE SET entity.version = -1
    WITH entity
    WHERE $version > entity.version
    SET entity.name = $name,
        entity.version = $version,
        entity.deleted_at = CASE WHEN $deleted THEN datetime() ELSE null END
    RETURN entity.entity_id AS entity_id
    """
    # 当前事件参数与 Cypher 字段一一对应。
    parameters = {
        "tenant_id": event.tenant_id,
        "entity_id": event.entity_id,
        "name": event.name,
        "version": event.version,
        "deleted": event.deleted,
    }
    driver.execute_query(query, parameters_=parameters, database_="neo4j")


def main() -> None:
    """创建驱动并写入一条示例事件。"""

    # 驱动内部维护连接池，应用生命周期内应复用。
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        # 示例事件可重复执行，第二次不会造成重复节点。
        event = EntityEvent("product-42", "tenant-a", "知识库产品", 3, False)
        apply_entity_event(driver, event)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
```

首次部署先创建唯一约束：

```cypher
CREATE CONSTRAINT entity_tenant_id_unique IF NOT EXISTS
FOR (entity:Entity)
REQUIRE (entity.tenant_id, entity.entity_id) IS UNIQUE;
```

# 四、增量一致性与跨存储对账

Neo4j、ES、VectorDB 无法共享普通 ACID 事务。推荐源库事务内同时写 Outbox，消费者分别更新三套索引，每个消费者以 `event_id` 去重，以 `version` 抵御乱序。后台对账任务比较每个版本的文档数、Chunk 数、实体数和内容哈希；未通过前不切换读别名。

物理清理顺序可采用：停止新引用 → 写墓碑并从查询中过滤 → 删除 ES/向量 Chunk → 删除图关系和节点 → 清缓存 → 写审计完成事件。任何一步失败都可依据墓碑重试。

# 五、权限与成本

- 所有节点和关系都携带 `tenant_id`，查询入口强制注入租户条件；不能依赖调用者记得写。
- 高敏实体可只保存脱敏摘要，原文保留在受控对象存储。
- 不要把所有 Chunk 都复制成图节点。图中保留实体与关系，Chunk 通过稳定 ID 回链，可显著降低存储和遍历成本。
- 对深度、返回节点数和查询超时设上限，避免模型生成无界 Cypher。

# 六、验收

重复事件不产生重复节点；乱序旧版本不覆盖新版本；删除后图、ES、向量库和缓存均不可命中；跨租户查询返回零条；对账失败可定位到具体 `document_id` 和索引版本。

<!-- article-progressive-block:start -->
# 七、动手验证：先跑通 Neo4j 增量更新与安全删除：保持 GraphRAG 一致，再改变一个变量

前面的章节已经建立问题、概念和机制。现在把“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”放进同一套基线中运行；本节不再引入新术语，只验证前文结论能否被复现。

## 7.1 基线与候选只允许一个变量不同

验证“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”时，先固定查询集、语料快照、权限身份、相关性标注。候选方案只能改变本次要验证的变量；如果同时更换数据、依赖和配置，即使结果改善，也不能知道是哪一项产生作用。

执行“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”时，动作是：离线回放检索，保存候选、过滤、排序和引用。原始结果不能只保留截图或汇总分数，必须同步保存：Recall@K、NDCG、引用命中率、无答案误答率、Trace，使下一次复查可以在同一输入上重放。

| 实验要素 | 本文要求 |
| --- | --- |
| 固定条件 | 查询集、语料快照、权限身份、相关性标注 |
| 唯一变量 | 本次候选方案与基线之间的一项明确差异 |
| 原始证据 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 通过阈值 | 证据可回链，指标达基线，权限过滤无泄漏 |
| 立即停止 | 漏召回、排序丢失、引用断链或越权命中 |

## 7.2 执行前先排除不可比较条件

“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”开始前先确认下面四项；任一项不成立，都应先修复实验条件，而不是解释结果。

- 基线能够在“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”的当前环境重复运行。
- 候选只改变一个与“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”结论直接相关的条件。
- “Neo4j 增量更新与安全删除：保持 GraphRAG 一致”的基线和候选使用同一批输入、同一版本依赖与同一通过阈值。
- “Neo4j 增量更新与安全删除：保持 GraphRAG 一致”的原始输出和失败现场不会被重试、格式化或汇总覆盖。

## 7.3 执行后先核对证据完整性

结果出来后先检查证据，再讨论“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”是否通过。缺少中间状态时，最终输出只能说明现象，不能证明机制。

| 检查项 | 当前文章的判定 |
| --- | --- |
| 输入可追溯 | 查询集、语料快照、权限身份、相关性标注 |
| 过程可回放 | 离线回放检索，保存候选、过滤、排序和引用 |
| 结果可审计 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |

“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”的一次合格基线对照按以下顺序执行：

1. 保存“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”基线版本及输入摘要，确认基线本身可以重复运行。
2. 写下“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”候选方案唯一变化的变量，以及它预期影响的指标。
3. 在同一环境执行“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”：离线回放检索，保存候选、过滤、排序和引用。
4. 为“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”保存：Recall@K、NDCG、引用命中率、无答案误答率、Trace。
5. 使用“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”预登记条件判断：证据可回链，指标达基线，权限过滤无泄漏。
6. 如果“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”未通过，不修改第二个变量，先恢复基线并保留失败现场。

# 八、用一张矩阵验证 Neo4j 增量更新与安全删除：保持 GraphRAG 一致 的关键结论

矩阵按正文顺序列出“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”的结论。一次实验只选择一行，只改变这一行对应的条件；不要把多行合并成一个无法归因的大实验。

| 正文章节 | 已解释的结论 | 本轮唯一变量 | 必须保存的证据 |
| --- | --- | --- | --- |
| 数据模型与删除语义 | version 用于拒绝乱序事件； | 只改变与“数据模型与删除语义”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 增量一致性与跨存储对账 | 任何一步失败都可依据墓碑重试。 | 只改变与“增量一致性与跨存储对账”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 权限与成本 | 图中保留实体与关系，Chunk 通过稳定 ID 回链，可显著降低存储和遍历成本。 | 只改变与“权限与成本”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 验收 | 对账失败可定位到具体 document_id 和索引版本。 | 只改变与“验收”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| GraphRAG 同时依赖原文、Chunk、向量索引和图关系 | GraphRAG 同时依赖原文、Chunk、向量索引和图关系。 | 只改变与“GraphRAG 同时依赖原文、Chunk、向量索引和图关系”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |
| 直接执行 DETACH DELETE 虽然能删节点 | 直接执行 DETACH DELETE 虽然能删节点，却可能留下向量库孤儿记录、缓存旧答案和无法审计的数据空洞。 | 只改变与“直接执行 DETACH DELETE 虽然能删节点”相关的条件 | Recall@K、NDCG、引用命中率、无答案误答率、Trace |

## 8.1 记录本次实际实验

下面的记录用于“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”当前这一次实验，不是第二套知识目录。先从矩阵选择一个章节，再填写实际值；没有填写的字段表示尚未验证。

```yaml
topic: "Neo4j 增量更新与安全删除：保持 GraphRAG 一致"
selected_chapter: required
claim_from_article: required
baseline_version: required
changed_condition: exactly_one
execution: "离线回放检索，保存候选、过滤、排序和引用"
evidence: "Recall@K、NDCG、引用命中率、无答案误答率、Trace"
pass_when: "证据可回链，指标达基线，权限过滤无泄漏"
stop_when: "漏召回、排序丢失、引用断链或越权命中"
observed_result: required
first_deviation: null_or_evidence
recovery_replay: required_after_failure
```

## 8.2 边界实验必须证明能够停止和恢复

成功路径只能证明“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”在当前样本上工作，不能证明它可以进入生产。边界实验需要主动制造：漏召回、排序丢失、引用断链或越权命中，并观察系统是否在产生不可逆副作用前停止。

| 场景 | 只改变什么 | 应保存什么 | 通过标准 |
| --- | --- | --- | --- |
| 正常路径 | 使用已知有效输入 | Recall@K、NDCG、引用命中率、无答案误答率、Trace | 证据可回链，指标达基线，权限过滤无泄漏 |
| 边界路径 | 把一个输入推进到约束临界值 | 临界值前后的输出与指标 | 不静默降级，不把部分结果冒充成功 |
| 明确失败 | 注入：漏召回、排序丢失、引用断链或越权命中 | 原始错误、首个异常阶段和最终状态 | 失败被正确分类且没有扩大副作用 |
| 恢复重放 | 执行：定位解析、召回、过滤、排序或生成阶段，回滚对应版本 | 原失败样本的复测证据 | 原样本恢复，正常样本没有回归 |

恢复动作不是简单重启。对于“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”，第一步是：定位解析、召回、过滤、排序或生成阶段，回滚对应版本。完成后使用原始失败样本复测；只验证一个新样本成功，不能证明触发条件已经消失。

“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”边界实验结束后，应把正常、临界、失败和恢复四类记录放在同一个运行批次中。这样才能区分“候选方案真的修复问题”和“环境变化让问题暂时没有出现”。

# 九、Neo4j 增量更新与安全删除：保持 GraphRAG 一致 的结果解释

解释“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”实验时先看首个偏差，而不是最后一条错误。最后的异常通常只是上游状态错误的结果；从末端反推容易误把症状当根因。

| 观察结果 | 可以支持的判断 | 下一步 |
| --- | --- | --- |
| 主链路没有达到预期 | 漏召回、排序丢失、引用断链或越权命中 | 先执行：定位解析、召回、过滤、排序或生成阶段，回滚对应版本 |
| 异常链路无法恢复 | 漏召回、排序丢失、引用断链或越权命中 | 先执行：定位解析、召回、过滤、排序或生成阶段，回滚对应版本 |
| 新样本成功但原样本仍失败 | 修复没有覆盖原始触发条件 | 固定原失败输入，恢复基线后重新比较 |
| 指标改善但证据无法回链 | 数据、版本或中间状态没有固定 | 暂停发布，补齐可追溯记录后重跑 |

“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”只有同时满足“证据可回链，指标达基线，权限过滤无泄漏”，并且没有出现“漏召回、排序丢失、引用断链或越权命中”，才可以认为主链路通过。这里的“通过”只对当前固定版本、样本和环境有效，不能外推到尚未测试的容量、权限或数据分布。

如果“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”候选方案与基线差异很小，先检查证据分辨率是否足够；如果差异很大，先排除数据泄漏、环境漂移和版本不一致。两种情况都不能只看一个汇总均值，需要回到逐样本输出和中间状态。

“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”故障定位完成后，记录“现象、首个偏差、根因、改动、原样本复测”五项。缺少原样本复测时，只能标记为待观察，不能标记为已解决。

# 十、Neo4j 增量更新与安全删除：保持 GraphRAG 一致 的发布判断

发布判断需要把“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”的质量、失败边界和恢复能力放在同一份记录中。以下任一条件缺失，都应停止扩量，而不是用“基本正常”替代证据。

- [ ] “Neo4j 增量更新与安全删除：保持 GraphRAG 一致”的基线与候选只存在一个计划内变量。
- [ ] “Neo4j 增量更新与安全删除：保持 GraphRAG 一致”的输入、代码、依赖、配置和数据版本可以追溯。
- [ ] “Neo4j 增量更新与安全删除：保持 GraphRAG 一致”的正常、临界、失败和恢复样本使用同一套断言。
- [ ] “Neo4j 增量更新与安全删除：保持 GraphRAG 一致”的原始输出、中间状态和失败现场已经保留。
- [ ] “Neo4j 增量更新与安全删除：保持 GraphRAG 一致”的日志、Trace、截图和测试数据已经脱敏。
- [ ] “Neo4j 增量更新与安全删除：保持 GraphRAG 一致”的停止条件、负责人和回滚入口已经演练。
- [ ] “Neo4j 增量更新与安全删除：保持 GraphRAG 一致”尚未覆盖的输入、权限、容量和外部依赖已经登记。

最终记录至少包含基线版本、唯一变量、原始证据、首个偏差、恢复复测和发布责任人。没有参与本次修改的人如果不能据此重放“Neo4j 增量更新与安全删除：保持 GraphRAG 一致”的判断，就不能发布。
<!-- article-progressive-block:end -->

# 十一、总结

- **数据模型与删除语义**：version 用于拒绝乱序事件；
- **可运行的幂等写入**：首次部署先创建唯一约束：
- **跨存储一致性**：任何一步失败都可依据墓碑重试。
- **权限与成本**：图中保留实体与关系，Chunk 通过稳定 ID 回链，可显著降低存储和遍历成本。
- **验收**：对账失败可定位到具体 document_id 和索引版本。

## 参考资料

- [Neo4j Cypher Manual：MERGE](https://neo4j.com/docs/cypher-manual/current/clauses/merge/)
- [Neo4j Operations Manual：Backup and Restore](https://neo4j.com/docs/operations-manual/current/backup-restore/)