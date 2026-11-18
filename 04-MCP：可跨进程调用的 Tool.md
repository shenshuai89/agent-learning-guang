# MCP：可跨进程调用的 Tool

> 作者：神说要有光 ｜ 公众号：神光的幸福生活 ｜ 发布：2025-12-24

> 原文链接：https://mp.weixin.qq.com/s/04AEZK_gDjZz0iFV-WIUjg

---

我们已经写了一些 tool 了：读写文件和目录、执行命令

![截图0](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfFkCbpPMVCycL6Q9D3lzQ5694jWVC8jZrKATRgkXic3RFjlA23OLTxibXA/640?wx_fmt=png&from=appmsg)

只要声明 tool 的名字、描述、参数格式，模型会在发现需要用 tool 的时候自动解析出参数传入来调用，然后把执行结果封装成 ToolMessage 传入 chat。

![截图1](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfFmE1h7ezMxhoFrOxKAFhF1OQia5sSnn3PrMgAASj2HjxibrrQcTyibq8ag/640?wx_fmt=png&from=appmsg)

▶ **[视频0](http://mpvideo.qpic.cn/0bc3mmafiaaar4ajqickbruvay6dkrrqavaa.f10002.mp4?dis_k=5fd959dc32db04dc3fe110bd4f430269&dis_t=1783678222&play_scene=10110&auth_info=IN3C0Ip+d+qOvNkhW5fg2MR/VB4Ge2s0TUw6MRs8eDUdJDYSNVdTdnAoKUw5LWsEY11DJAw=&auth_key=8aaf0d1c77db41feb15d8d2e60a3f7c9)**

这些 tool 怎么调用、参数是什么都是大模型自己决定的。
tool 给大模型扩展了做事情的能力，本来它只能思考，不能做事情，但是现在可以自己调用 tool 来帮你做事情了。
但你有没有发现 tool 有个问题：
node 写的 ai agent 的代码，你的 tool 也得是 node 写。
如果你之前有一些工具是 java、python、rust 写的呢？
你想封装成 tool 怎么办呢？
有的同学说：现在不是可以执行命令么，通过单独进程把这些其他语言写的代码跑一下就行啊。
确实，也就是这样：

![截图2](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfFpWvrUuSBfQsfzKibObx5ubaaA4JVIKQJaRVe8PohhyyZAxtcqC5u75A/640?wx_fmt=png&from=appmsg)

这里的 stdio 就是标准输入输出流，也就是键盘输入、控制台输出。当你进程跑一个子进程，就可以用这种方式通信。
还有的同学说：简单，用 http 啊！本地跑个服务就好了。

![截图3](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfFKKWNPHsRO0Lice3XUjh8Q73AFu67SMKcXtciawoyVsIDbFL0bGG2ldVQ/640?wx_fmt=png&from=appmsg)

现在是解决了跨语言调用工具的问题。
那如果每个人都这样搞，它们提供的服务都不一样，我想接入别的 tool，是不是要了解每个服务都是怎么定义的呢？
能不能定义一个统一的通信协议，我们都按照这个格式来沟通，这样所有的跨进程工具调用就都可以接入了。

![截图4](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfF93AfEOrGYQNJDHux6zEXV9vVle1VgxKJaBkqH1chXjE7zMicaW9pIBQ/640?wx_fmt=png&from=appmsg)

想跨进程调用某个工具，通过这个协议通信就行。
不管是本地工具，直接跑那个进程，然后 stdio 通信。
还是远程工具，通过 http 连接远程服务进程。
这个协议叫什么呢？
是给 Model 扩展 Context 上下文，让它能做的更多，知道的更多的 Protocal 协议。
就叫 MCP 吧。
恭喜你，你发明了 MCP！

![截图5](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfFnQdAoI4xtZdia6kNTTHDcaIicfQHWJgDlUNjS4ibCz5ia4DFfRQersPRnA/640?wx_fmt=png&from=appmsg)

MCP 最大的特点就是可以跨进程调用工具。
跨本地的进程调用，就是用 stdio。
跨远程的进程调用，就是用 http。
提到 MCP 都会提到这张图：

![截图6](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfFIQibAKia44olfKESv7dLOMYZ5V7DLrl253jFibbFxby236iaickghfu2V3g/640?wx_fmt=png&from=appmsg)

你的 ai agent 就是 MCP 客户端，可以通过 MCP 协议调用各种 MCP Server，实现跨进程的工具调用。
当然，在 langchain 里，它也是 tool ，只不过是 tool 的一种而已：

![截图7](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVjicppMtsQDdZBjGd9SevLHxP80B3ZicURj03QfKv3wD4Oebiaef5QJow9X6tZY6bvAcN9VjmzzN1Ww/640?wx_fmt=png&from=appmsg)

你在 tool 的函数里，调用下 MCP Client，访问下远程 Mcp Server，它本质上还是 tool，但是却集成了 MCP 工具。
MCP 是由 AI 巨头 Anthropic 公司发起并开发，但是 2025 年 12 月交给了 Linux 基金会维护。
也就是说它现在是完全中立于任何一个模型的行业通用协议。
大概知道 MCP 是啥就行，我们自己来写个 MCP 服务就明白了。
继续在 tool-test 这个项目里写：
安装 mcp 的包：

```javascript
pnpm install @modelcontextprotocol/sdk
```

从包名就可以看出来是中立于任何一家公司的。
创建 src/my-mcp-server.mjs

```javascript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

// 数据库
const database = {
users: {
    '001': { id: '001', name: '张三', email: 'zhangsan@example.com', role: 'admin' },
    '002': { id: '002', name: '李四', email: 'lisi@example.com', role: 'user' },
    '003': { id: '003', name: '王五', email: 'wangwu@example.com', role: 'user' },
  }
};

const server = new McpServer({
name: 'my-mcp-server',
version: '1.0.0',
});


// 注册工具：查询用户信息
server.registerTool('query_user', {
description: '查询数据库中的用户信息。输入用户 ID，返回该用户的详细信息（姓名、邮箱、角色）。',
inputSchema: {
    userId: z.string().describe('用户 ID，例如: 001, 002, 003'),
  },
}, async ({ userId }) => {
const user = database.users[userId];

if (!user) {
    return {
      content: [
        {
          type: 'text',
          text: `用户 ID ${userId} 不存在。可用的 ID: 001, 002, 003`,
        },
      ],
    };
  }

return {
    content: [
      {
        type: 'text',
        text: `用户信息：\n- ID: ${user.id}\n- 姓名: ${user.name}\n- 邮箱: ${user.email}\n- 角色: ${user.role}`,
      },
    ],
  };
});


server.registerResource('使用指南', 'docs://guide', {
description: 'MCP Server 使用文档',
mimeType: 'text/plain',
}, async () => {
return {
    contents: [
      {
        uri: 'docs://guide',
        mimeType: 'text/plain',
        text: `MCP Server 使用指南

功能：提供用户查询等工具。

使用：在 Cursor 等 MCP Client 中通过自然语言对话，Cursor 会自动调用相应工具。`,
      },
    ],
  };
});


const transport = new StdioServerTransport();
await server.connect(transport);
```

代码很容易看懂：
new McpServer 创建了 mcp server 实例
server.registerTool 注册了一个工具，声明 name、description、schema
server.registerResource 注册了一个资源，就是静态数据
和我们写 tool 的时候差不多，只不过这里分了 resource 和 tool，resouce 一般返回静态数据，tool 来做一些事情。
最后，可以提供 stdio 的本地进程的调用方式，也可以提供 http 的远程调用方式。
这里是 stdio 的传输方式（Transport）

![截图8](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfFzLKyB9kybJkGheXLfnJ02AnyTfJSTWO4r5qHrTLDYHuCiaOGQBquf8Q/640?wx_fmt=png&from=appmsg)

这样，我们的 MCP 服务就创建好了！
是不是很简单。
其实就是 tool，加上了协议而已。
我们在 cursor 里配置下这个 mcp server：

▶ **[视频1](http://mpvideo.qpic.cn/0bc3iyaagaaaiyam5vkkeruvarwdandaaaya.f10002.mp4?dis_k=91541c09d43b3c52301e635ad085ded9&dis_t=1783678222&play_scene=10110&auth_info=cbTCsPYvcOnZuYl3V5G0j5Z/WElXdm9uGRZtN0w8e2JMdTZEYQNUdScteRo1Kz9TMV1Pc10=&auth_key=663a6a36ea80a2e09f6f4721675124b1)**

配置好之后测试下：

▶ **[视频2](http://mpvideo.qpic.cn/0bc3naafiaaaziajrqcka5uva2gdkruaavaa.f10002.mp4?dis_k=624490742cd925f37617bd41983d8d3d&dis_t=1783678222&play_scene=10110&auth_info=IqSUk/96JL7Y6dR/XMDojsEiV0pWdmc9Hhs7YBtnejQfdDJCYVEAIiZ9JBI+emNSZgBAcFw=&auth_key=712429bbaa288092a9ef05ea68ba2a41)**

我特意换了个项目来测。
可以看到，确实检测到了这个 mcp 然后调用了！
这里 cursor 有个坑注意下：

▶ **[视频3](http://mpvideo.qpic.cn/0bc3fuacsaaagyaoj6ckdfuvalodfewqakia.f10002.mp4?dis_k=213db9a18013e06fc1ded3c5ce0ef754&dis_t=1783678222&play_scene=10110&auth_info=cvG+wpwrIumP7Y4iX8G23cdyU0lRJjw0SB4xM05tLTFPIWZFNAMGdXF5fk89ez0BYFBEc1s=&auth_key=5eae61adc9c7afea5a16ee4d8774e38a)**

点一下 tool 是禁用，再点一下是启用。
但是 cursor 这个状态颜色区分不明显，没有调用 mcp 工具，可能你关掉了。
这就是 mcp 的好处，写好之后可以插拔到任何地方当 tool 用。
那 resource 呢？
它其实不是用来作为 tool 触发的，主要是你可以引用用来写 prompt 之类的。
比如这样：

▶ **[视频4](http://mpvideo.qpic.cn/0bc3vyaaiaaaciamqykkebuvblwdasxaabaa.f10002.mp4?dis_k=d913c0763e5079b6f1131c3753581bde&dis_t=1783678222&play_scene=10110&auth_info=Jp6l8cF8d7nf79h0WpzhiJYjBUFTcT09Hhk6ZkpufzgbcWNFYVVTJSF7KBk4JmpUMQESe1k=&auth_key=ada784ea3e1ce2ec5a9d7c3973ffc9fc)**

resource 主要是查询信息用的（read）， 而 tool 是执行功能用的（call）
当然，因为有了 mcp，除了 cursor，别的软件同样可以调用这个服务：

![截图9](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfF4WRZ57UGvtNsnPRUv77ibRhJ1T9iaN0oll37ZxzSCj7iaibmuOerXOv1vQ/640?wx_fmt=png&from=appmsg)


在vscode中添加my-mcp-server
首先在扩展工具中安装 MCP Server Explorer 工具
![MCP Server Explorer 工具](./images/MCP-Server-Explorer-工具.png)

点击Server Explorer右侧的+号，可以配置mcp server：
配置完成的json
``` json
{
  "servers": {
    "my-mcp-server": {
      "type": "stdio",
      "command": "node",
      "args": [
        "/Users/xxxx/code/04mcp/src/my-mcp-server.mjs"
      ]
    }
	},
  "inputs": []
}
```

配置完成后，可以点击mcp右侧的运行按钮
运行成功后，就可以在vscode的copilot中进行测试
![copilot查看设置的mcp](./images/copilot-setting-mcp.png)

给 copilot 开启mcp服务
![copilot开启mcp服务](./images/copilot-mcp-start.png)

接下来就可以在对话框中输入：“使用 my-mcp-server 的 工具，帮我查下001用户信息”
![copilot查询结果](./images/copilot-mcp-result.png)

我们在 langchain 代码里调用下 mcp server：
用这个包：

```javascript
pnpm install @langchain/mcp-adapters
```

创建 src/langchain-mcp-test.mjs

```javascript
import 'dotenv/config';
import { MultiServerMCPClient } from '@langchain/mcp-adapters';
import { ChatOpenAI } from '@langchain/openai';
import chalk from 'chalk';
import { HumanMessage, ToolMessage } from '@langchain/core/messages';

const model = new ChatOpenAI({
    modelName: "qwen-plus",
    apiKey: process.env.OPENAI_API_KEY,
    configuration: {
        baseURL: process.env.OPENAI_BASE_URL,
    },
});

const mcpClient = new MultiServerMCPClient({
    mcpServers: {
        'my-mcp-server': {
            command: "node",
            args: [
                "/Users/guang/code/tool-test/src/my-mcp-server.mjs"
            ]
        }
    }
});

const tools = await mcpClient.getTools();
const modelWithTools = model.bindTools(tools);

asyncfunction runAgentWithTools(query, maxIterations = 30) {
    const messages = [
        new HumanMessage(query)
    ];

    for (let i = 0; i < maxIterations; i++) {
        console.log(chalk.bgGreen(`⏳ 正在等待 AI 思考...`));
        const response = await modelWithTools.invoke(messages);
        messages.push(response);

        // 检查是否有工具调用
        if (!response.tool_calls || response.tool_calls.length === 0) {
            console.log(`\n✨ AI 最终回复:\n${response.content}\n`);
            return response.content;
        }

        console.log(chalk.bgBlue(`🔍 检测到 ${response.tool_calls.length} 个工具调用`));
        console.log(chalk.bgBlue(`🔍 工具调用: ${response.tool_calls.map(t => t.name).join(', ')}`));
        // 执行工具调用
        for (const toolCall of response.tool_calls) {
            const foundTool = tools.find(t => t.name === toolCall.name);
            if (foundTool) {
                const toolResult = await foundTool.invoke(toolCall.args);
                messages.push(new ToolMessage({
                    content: toolResult,
                    tool_call_id: toolCall.id,
                }));
            }
        }
    }

    return messages[messages.length - 1].content;
}

await runAgentWithTools("查一下用户 002 的信息");
```

我们用 @langchain/mcp-adapters 创建了 mcp client
写法和 cursor 里配置一样：

![截图10](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfFNnF4Ou3Ubxd8qrNzoJIr8ot5J9wz9zXhkiaBIJD2BkeZVo3zib8ooOrg/640?wx_fmt=png&from=appmsg)

就是用命令行启动这个进程，之后用 stdio 的方式做通信。
拿到 tools 之后绑定到模型。
模型调用返回 tool_calls 消息需要自己调用 tool，调用完通过 ToolMessage 封装返回的消息，继续调用。
这个循环我们写过很多次了。
调用下试试：

▶ **[视频5](http://mpvideo.qpic.cn/0b2eoaakcaaafiagzwck6juva4gdufyabiia.f10002.mp4?dis_k=091a202694c0d0ed529102df0a3e0234&dis_t=1783678222&play_scene=10110&auth_info=IfeXn5t4duiIvt0mXMHg2MFyUUFTI2w9GxkwNxxuLDEcIzBGaVdSdHYqLUs+e2sEZlBGe1k=&auth_key=121266f4d55e3fd27cfdeb1e977afbb1)**

可以看到，你让大模型查询用户，它识别到了工具调用，然后调用了 mcp 的工具。
这里进程没退出，因为你跑了一个子进程作为 mcp server，需要把那个关掉才可以：

![截图11](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfFHdW2XZLhS2QZB8FibGrXYH1qybh9oNKPJLCQ2dL7jv8UtoHbQ5Slgdg/640?wx_fmt=png&from=appmsg)

```javascript
await mcpClient.close();
```

▶ **[视频6](http://mpvideo.qpic.cn/0bc33yafeaaawaaj7i2kgbuvbxwdklpaauqa.f10002.mp4?dis_k=aabb486915e3cc9e18d31bc73fbb7108&dis_t=1783678222&play_scene=10110&auth_info=WOTL8zZ164672nQJxrLdw3ZZGQMgPDkRGTAySjt7Yhp+YEVoAlF3cC8qGWt8OQFkVE4jCQ==&auth_key=43085e2ebedefbd456933453a1029379)**

那 resource 怎么用呢？
那种静态信息可以放到 system message 里。
我们先查一下 resource：

![截图12](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfFibpWicQGGkicLLHKLnXLuHSBL7wH8emZ7IvVibcVKe1E3vG6BZsBr4Zy1g/640?wx_fmt=png&from=appmsg)

```javascript
const res = await mcpClient.listResources();
console.log(res);
```

▶ **[视频7](http://mpvideo.qpic.cn/0bc3saadgaaa2yap4bskhnuvbegdgoiaamya.f10002.mp4?dis_k=b3afd833d2ed8625cfa670474ed7b0a3&dis_t=1783678222&play_scene=10110&auth_info=doWv0Px/cerY79kiC5Oy2pN1A0sDJDo1GhxtMRo6cDdLcmYSMVBVdiZ7KU9pKTkGNFcUcQk=&auth_key=b9e5ca846d872282df58e58c817cdf22)**

遍历依次读取 uri 内容

![截图13](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfFzzxSxTG7UsB1bj3tkNaw53Aibcp1DrCeUtyzS5FFPic2c5FEnqSVicJiaQ/640?wx_fmt=png&from=appmsg)

```javascript
const res = await mcpClient.listResources();

for (const [serverName, resources] of Object.entries(res)) {
    for (const resource of resources) {
        const content = await mcpClient.readResource(serverName, resource.uri);
        console.log(content);
    }
}
```

▶ **[视频8](http://mpvideo.qpic.cn/0b2eyiafwaaaxqajmeskx5uvbqwdlpbaawya.f10002.mp4?dis_k=e33658bb1e3b96bc247bb9917c90c53e&dis_t=1783678222&play_scene=10110&auth_info=JqeU6scuJOPV6dokVpSz38EjBEtRdGs1S004Zkw8cTcbJDdAZwQAfyt9Kkk0LjgDZgETcVs=&auth_key=a3ffc1df513ecb842023d5b81d8a5727)**

然后只要把它放到 system message 里作为上下文就好了：

![截图14](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfFwALSLSoJEmPw6xK0knUaycsuLqaLS930zCE1mD5cMCwibKNjqPQeRlQ/640?wx_fmt=png&from=appmsg)

```javascript
const res = await mcpClient.listResources();

let resourceContent = '';
for (const [serverName, resources] of Object.entries(res)) {
    for (const resource of resources) {
        const content = await mcpClient.readResource(serverName, resource.uri);
        resourceContent += content[0].text;
    }
}
```

```javascript
const messages = [
    new SystemMessage(resourceContent),
    new HumanMessage(query)
];
```

调用下：

![截图15](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfF7SB0qR1uMoZ5FLlJLbA6EFwfGoe2DjsHW1HUA7Yt0FQSAqVhlPZLUw/640?wx_fmt=png&from=appmsg)

```javascript
await runAgentWithTools("MCP Server 的使用指南是什么");
```

跑一下：

▶ **[视频9](http://mpvideo.qpic.cn/0bc3ryafgaaaxeaj4sckbvuvbdwdkohaauya.f10002.mp4?dis_k=49f84272db43253edc681019fa55ace8&dis_t=1783678222&play_scene=10110&auth_info=d9y+jKx0d+rd4YsmWpGxiZd+VUEEemo/Hh1tYUttejRKImEXZl5TdiN1e0s4KzpVMFxCew4=&auth_key=eedc506d70206e8cdd2ca4ac1006dd35)**

现在，大模型就知道这个 resource 的信息，可以用来回答问题了。
resource 可以用在 system message 里，也可以用在 human message 里，总之，是作为信息引用的。
我们主要还是用 mcp 的 tools。

![截图16](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVyG2W4yUxn0yaZkWNVjcfFt8cX99OvYRyXX4K1BbnwyjiaRexz0rgm5oOOrdl3Flqg8hpC6vLPg1g/640?wx_fmt=png&from=appmsg)

这样，我们就写了一个 mcp server，并分别在 cursor、langchain 里用了这个 mcp server。
mcp 本质上还是 tool，和之前的 tool 的区别只不过是可以跨进程调用：

![截图17](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVjicppMtsQDdZBjGd9SevLHxP80B3ZicURj03QfKv3wD4Oebiaef5QJow9X6tZY6bvAcN9VjmzzN1Ww/640?wx_fmt=png&from=appmsg)

当你不需要跨进程用的时候，还是之前那样写更好，还少了进程通信的成本。
代码上传了课程仓库： https://github.com/QuarkGluonPlasma/ai-agent-course-code/tool-test
## 总结
这节我们学了 MCP，它是可跨进程调用的 Tool。
可以是本地进程，用 stdio 进程通信。
可以是远程进程，用 http 通信。
在 langchain 里用 @langchain/mcp-adapters 封装成 tools 来用，其实和其他 tool 没区别。
跨进程就意味着不限语言，开发好之后，可以被任意 mcp client 调用，比如 cursor、langchain 等。
除了自己写 mcp server，现在也有很多现成的 mcp server 可以直接用，下节我们来用一下。
