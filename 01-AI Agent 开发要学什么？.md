# AI Agent 开发要学什么？

> 作者：神说要有光 ｜ 公众号：神光的幸福生活 ｜ 发布：2025-12-21

> 原文链接：https://mp.weixin.qq.com/s?__biz=MzYzNzI2MTI2Nw==&mid=2247483703&idx=1&sn=7c887f24c74a6e993dcdde20a94b2f32&chksm=f0f2858bc7850c9d508139eb9b6e6f25005513d565ab17786aafff36840435c42218159beffa#rd

---

我们每天都在用各种 AI Agent，比如用 Curosr 写代码，用 Manus 做各种自动化的事情。
那你有没有想过自己开发一个 AI Agent 产品呢？

![截图0](https://mmbiz.qpic.cn/sz_mmbiz_jpg/JnZIbTicL4jWMUiabDiamSHCjWPuYZq5V66xxctCFmWNDMLWFlibLiaBicXdhWBNwjgicX25xoZD0UKsUkLRdyia668ZvA/640?wx_fmt=jpeg&from=appmsg)

有同学说，直接调大模型不就行了？
你可以想一下，大模型是不是有这些问题：
你上周和它聊过的消息，它是不是记不住？
你让它帮你访问一个网页，做一些事情，它是不是只能告诉你思路让你自己做？
你想让它基于你公司内部的私密文档来做一些解答，它是不是不知道那是什么？
你问他刚发生的一个新闻，它是不是不知道？因为它训练的时候没这些数据
这些问题的解决就需要分别给大模型加上 Memory 记忆能力、Tool 工具调用能力、RAG 文档查询能力等。
不管大模型怎么发展，它都没法解决这些：
它的记忆总是有限的，需要开发者做 Memory 管理
它可以调的特定领域的工具，需要开发者开发好 Tool 交给它
它没办法对不知道的私密文档做解答，需要扩展 RAG 知识库查询能力
这些就是我们要学的 AI 技术，也就是 AI Agent 的开发能力。
Agent 是什么？
其实就是给大模型扩展了 Tool 和 Memory。它本来就可以思考、规划，你给他用 Tool 扩展了能力，它就可以自动做事情了，用 Memory 管理了记忆，它就可以记住你想让它记住的东西，还可以用 RAG 查询内部知识库来获取知识。
这样一个知道内部知识、能思考规划、有记忆，能够帮你做事情的扩展后的大模型，就是一个 Agent。

![截图1](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jWMUiabDiamSHCjWPuYZq5V66LRo2GZXr9nQGSJdvqT6v6yqB6H2RpJrbiazkRHSyTuicyQt2fWAFtRCA/640?wx_fmt=png&from=appmsg)

你每天用的 Curosr 等 AI IDE，它是怎么读写文件、执行命令的？
比如改代码需要读写文件：

▶ **[视频0](http://mpvideo.qpic.cn/0bc3syaaoaaaaeak3s2hevuvbfwda6laabya.f10002.mp4?dis_k=253082c0ce0f2d6e1f62d15c337a1df9&dis_t=1783680884&play_scene=10110&auth_info=X5nsk/8Aa6DRt7pzfJTsx656NlNuBWJLF25ULDw0V0xiLU48ZCtPPC8jSh4eLmcbCVghaWQ=&auth_key=c701418ff228a3ec6246c67ae9728f0e)**

帮你运行代码需要执行命令：

▶ **[视频1](http://mpvideo.qpic.cn/0bc3wiadiaaaiyacczcimnuvbmwdgszaanaa.f10002.mp4?dis_k=136c46575c8cc1a68e4cc57fd196e119&dis_t=1783680884&play_scene=10110&auth_info=WPeLzKEFZfeF4u1zf5LplKJ+YFQ4A2pORjsDfzU3VR1lKUw5MylBa3t2HR4dKGJIBVx3bjI=&auth_key=d9829cc3cfd0c8d4545e51c90253e7b8)**

如何实现的这些功能呢？很明显是扩展了 Tool。
帮你做各种事情的 Manus，是怎么唤起浏览器来自动访问一些网页，怎么执行命令，怎么帮你操作各种软件的？
看这个视频：

▶ **[视频2](http://mpvideo.qpic.cn/0b2ebmaisaaaniacaosh4ruvac6drefqbcia.f10002.mp4?dis_k=0610cdfefb7124458bcf66f5956fa446&dis_t=1783680884&play_scene=10110&auth_info=De2Y0cYCaqeB5+h8fpfux/UsMwZrAmUcFz5WfDUwAhgwKh1qbi1OO39zGBEcLWUbUg4kPGE=&auth_key=84b3079cfba9520a3a32dd8cb5204c27)**

Manus 是怎么打开浏览器、访问网页，点击元素，帮你总结成文档，写入 md 文件的？
也是扩展了 Tool。
支付宝里的理财助手，可以帮你分析基金，推荐基金，它是怎么知道这些基金的数据的？

▶ **[视频3](http://mpvideo.qpic.cn/0b2es4aiqaaa7uacf5ch5juvbf6drclqbcaa.f10002.mp4?dis_k=88f3c2c6eefa302d3b88f49e5369642e&dis_t=1783680884&play_scene=10110&auth_info=XYDn7KUHavjW5+4vdpm5xPV6NlVoBTRMFjpQLT4wWUZgKEI6YitOZChzHkIUIzIYUlghb2I=&auth_key=57af541eca70bc8cdb249c6028b4f058)**

支付宝蚂小财是怎么知道这些基金的数据的？是大模型本身就知道么？
肯定不是啊，是基于 RAG 来访问了内部的知识库。
类似的各种需要给大模型扩展能力的场景太多了。
光会和大模型聊天不行，你得能给它扩展各种能力，这样才能满足各种 AI 需求。
这就是我们学习 AI 技术的目标。
那 RAG、Memory、Tool、Agent 等用什么框架呢？
最常用的就是 LangChain，它对这些能力封装好了各种 api，可以直接用。
我在公司做 AI Agent 产品，就是基于 langchain 来开发。
它有 python 和 node 版，我们学的是 node 版。
其实语言是次要的，等你学会了 AI 技术，换语言来写也是很简单的事情，逻辑、概念都是一样的。
作为前端，肯定是 js、node 来上手学 AI 更顺滑啊！
所以这门课程是用 node + langchain + langgraph 来开发各种 Agent。
LangChain 是用来开发单个 Agent 的，每个 Agent 做一件事情。
但涉及到多个 Agent 协作，用 LangChain 自己维护多 Agent 的交互就比较麻烦了，这时候我们就要学习 LangGraph。
它是基于 LangChain 封装的，用于多 Agent 交互的框架。
学 AI 不要只学用 AI 做一些工具，最好是结合后端技术一起学，也就是 AI 全栈。
因为 AI 代码是在后端跑的，这时候你需要用 redis 存记忆、用 mysql 存知识等，这种就需要后端的知识了。
所以我们是后端 + AI 一起学，做 AI 全栈产品，node 后端框架用 Nest。
给大模型扩展 Tool、Memory、RAG 等能力，让它可以去做一些具体的事情，这就是一个 Agent 了。
平时我们用的 cursor、manus 等工具都是 AI Agent。
我们会学习开发 Agent 用的 langchain 框架，开发 Multi Agent 用的 langgraph 框架，基于 node 版来学，学会了后面换语言也很简单，api、逻辑都一样。
我们会结合后端技术一起学，开发 AI 全栈产品。这样才能让 AI 技术落地到产品里，变成我们的竞争力，吃到这波 AI 时代的红利。
