# 实现 mini cursor：大模型自动调用 tool 执行命令

> 作者：神说要有光 ｜ 公众号：神光的幸福生活 ｜ 发布：2025-12-22

> 原文链接：https://mp.weixin.qq.com/s?__biz=MzYzNzI2MTI2Nw==&mid=2247483845&idx=1&sn=4df6696c4b029c65eb007ede6b627c47&chksm=f0f28579c7850c6f03ba50a83ebdb84d437c34ee1d9d802ca12062760005045f92dd31386ce7#rd

---

上节我们给大模型扩展了读文件的 tool，你说一个文件路径让它解释，它就可以自动调工具读文件内容给出解释了。

▶ **[视频0](http://mpvideo.qpic.cn/0b2emeajaaaanyah4oki4fuvayodsbqqbeaa.f10002.mp4?dis_k=849d8c5332ff7a88dfc23a2498a4bce0&dis_t=1783680878&play_scene=10110&auth_info=fKD9nIF+dbve7NR/DpCyiZd2WUxbJmZuHBw6MRk4f2BBf2ESM1RRJyB4JBJsKjlVMFROdlE=&auth_key=36844ee44b2d4f6aaeab40ad7c5ba1b5)**

那继续思考：
如果我们给它扩展了执行命令、写文件、创建目录、读取目录、读文件等 tool，是不是就能实现 cursor 的功能呢？
比如创建项目对文件做增删改：

▶ **[视频1](http://mpvideo.qpic.cn/0b2edqaaaaaajeao4y2ivbuvahgdaaoaaaaa.f10002.mp4?dis_k=e4ca8933909a25aa879c87df260b9da8&dis_t=1783680878&play_scene=10110&auth_info=JbCKzIQofu2Ivt9xX8bpjpN+BEwBI2Y0GhwwM0Y/ejQYJj1DaQVacXYqLxw9fGJSNFwTdgs=&auth_key=68381a3a762511e0d4967510255299a8)**

项目创建后自动执行命令安装依赖和跑服务：

▶ **[视频2](http://mpvideo.qpic.cn/0bc3iaabeaaaamapzzcifvuvaqgdcjaaaeqa.f10002.mp4?dis_k=51ee0ff45195d8d29fb62e9bff5a2b46&dis_t=1783680878&play_scene=10110&auth_info=IL2irJF7dL/VuoshWsXiiMZwVEkHJ25rTxs8MkZrLDkddTwSMlBQIysue0w4f2lUYVJDcw0=&auth_key=99c4a5b455e7c0206b980f3568b49c16)**

是不是现在就可以实现了！

![截图0](https://mmbiz.qpic.cn/sz_mmbiz_jpg/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo3oOqMV0QqqzdBVrqsRasyss7rGHibuLSxe8y9VRNgYUFnTqmNgOT7C4w/640?wx_fmt=jpeg&from=appmsg)

虽然我们不会做那么完善，但是简易版确实可以写了。
这节我们就来实现下大模型根据 prompt 生成项目代码，自动读写文件、通过命令安装依赖、自动把项目跑起来，全程自己调用 tool 的功能：
不创建新项目了，直接在上节的 tool-test 项目继续写。
首先， node 里如何执行命令呢？
用 child_process 这个内置模块。
创建 src/node-exec.mjs

```javascript
import { spawn } from 'node:child_process';

const command = 'ls -la';
const cwd = process.cwd();

// 解析命令和参数
const [cmd, ...args] = command.split(' ');

const child = spawn(cmd, args, {
  cwd,
stdio: 'inherit', // 实时输出到控制台
shell: true,
});

let errorMsg = '';

child.on('error', (error) => {
  errorMsg = error.message;
});

child.on('close', (code) => {
if (code === 0) {
    process.exit(0);
  } else {
    if (errorMsg) {
      console.error(`错误: ${errorMsg}`);
    }
    process.exit(code || 1);
  }
});
```

spawn 可以指定在 cwd 这个目录下执行命令，会创建一个子进程来跑，这也是为啥这个模块叫 child_process。
用空格分割出命令和参数部分，分别作为 cmd、args
inherit 就是这个子进程的 stdout 也输出到父进程的 stdout，也就是控制台。
跑一下：

```javascript
node ./src/node-exec.mjs
```

▶ **[视频3](http://mpvideo.qpic.cn/0bc3xaacaaaa2qam5asi3buvbogdec4aaiaa.f10002.mp4?dis_k=df1666e5cf91ee2dedab85e9e01d107b&dis_t=1783680878&play_scene=10110&auth_info=dqKM2bksfu+J4Yh3XsDh2sUkBR5TdGg7TBpqZUZvLWRLI2AQMQRac3d1eBo8emoGYgYSJFk=&auth_key=69d890c49a0b0989b15884dfacd94d87)**

最终我们是要跑 npx create-vite 这个命令的，试一下：

```javascript
const command = 'echo -e "n\nn" | pnpm create vite react-todo-app --template react-ts';
```

echo 两个 n 是有时候 vite 会让你选择两个选项：用不用 rolldown、安不安装依赖
echo n 然后通过管道操作符输出给那个进程就和我们键盘输入 n 一样的效果。

▶ **[视频4](http://mpvideo.qpic.cn/0bc3e4aeaaaawyak5tkiebuvaj6diatqaqaa.f10002.mp4?dis_k=9f67887eb26f518831d129f1c475dc66&dis_t=1783680878&play_scene=10110&auth_info=fIShz/l4dOOK6Y5zWJG0icRwWB5UdWY1HkprMUk4fTBBfzZFNFdQf3R9fh46Kz9VY1JPJF4=&auth_key=170c6cce140971fb211b4a2918b3ee95)**

测试完之后，接下来就是封装 tools 了。
我们单独一个文件来放所有的 tools：
src/all-tools.mjs

```javascript
import { tool } from '@langchain/core/tools';
import fs from 'node:fs/promises';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { z } from 'zod';

// 1. 读取文件工具
const readFileTool = tool(
async ({ filePath }) => {
    try {
      const content = await fs.readFile(filePath, 'utf-8');
      console.log(`  [工具调用] read_file("${filePath}") - 成功读取 ${content.length} 字节`);
      return `文件内容:\n${content}`;
    } catch (error) {
      console.log(`  [工具调用] read_file("${filePath}") - 错误: ${error.message}`);
      return `读取文件失败: ${error.message}`;
    }
  },
  {
    name: 'read_file',
    description: '读取指定路径的文件内容',
    schema: z.object({
      filePath: z.string().describe('文件路径'),
    }),
  }
);

// 2. 写入文件工具
const writeFileTool = tool(
async ({ filePath, content }) => {
    try {
      const dir = path.dirname(filePath);
      await fs.mkdir(dir, { recursive: true });
      await fs.writeFile(filePath, content, 'utf-8');
      console.log(`  [工具调用] write_file("${filePath}") - 成功写入 ${content.length} 字节`);
      return `文件写入成功: ${filePath}`;
    } catch (error) {
      console.log(`  [工具调用] write_file("${filePath}") - 错误: ${error.message}`);
      return `写入文件失败: ${error.message}`;
    }
  },
  {
    name: 'write_file',
    description: '向指定路径写入文件内容，自动创建目录',
    schema: z.object({
      filePath: z.string().describe('文件路径'),
      content: z.string().describe('要写入的文件内容'),
    }),
  }
);

// 3. 执行命令工具（带实时输出）
const executeCommandTool = tool(
async ({ command, workingDirectory }) => {
    const cwd = workingDirectory || process.cwd();
    console.log(`  [工具调用] execute_command("${command}")${workingDirectory ? ` - 工作目录: ${workingDirectory}` : ''}`);

    returnnewPromise((resolve, reject) => {
      // 解析命令和参数
      const [cmd, ...args] = command.split(' ');

      const child = spawn(cmd, args, {
        cwd,
        stdio: 'inherit', // 实时输出到控制台
        shell: true,
      });

      let errorMsg = '';

      child.on('error', (error) => {
        errorMsg = error.message;
      });

      child.on('close', (code) => {
        if (code === 0) {
          console.log(`  [工具调用] execute_command("${command}") - 执行成功`);
          const cwdInfo = workingDirectory
            ? `\n\n重要提示：命令在目录 "${workingDirectory}" 中执行成功。如果需要在这个项目目录中继续执行命令，请使用 workingDirectory: "${workingDirectory}" 参数，不要使用 cd 命令。`
            : '';
          resolve(`命令执行成功: ${command}${cwdInfo}`);
        } else {
          console.log(`  [工具调用] execute_command("${command}") - 执行失败，退出码: ${code}`);
          resolve(`命令执行失败，退出码: ${code}${errorMsg ? '\n错误: ' + errorMsg : ''}`);
        }
      });
    });
  },
  {
    name: 'execute_command',
    description: '执行系统命令，支持指定工作目录，实时显示输出',
    schema: z.object({
      command: z.string().describe('要执行的命令'),
      workingDirectory: z.string().optional().describe('工作目录（推荐指定）'),
    }),
  }
);

// 4. 列出目录内容工具
const listDirectoryTool = tool(
async ({ directoryPath }) => {
    try {
      const files = await fs.readdir(directoryPath);
      console.log(`  [工具调用] list_directory("${directoryPath}") - 找到 ${files.length} 个项目`);
      return `目录内容:\n${files.map(f => `- ${f}`).join('\n')}`;
    } catch (error) {
      console.log(`  [工具调用] list_directory("${directoryPath}") - 错误: ${error.message}`);
      return `列出目录失败: ${error.message}`;
    }
  },
  {
    name: 'list_directory',
    description: '列出指定目录下的所有文件和文件夹',
    schema: z.object({
      directoryPath: z.string().describe('目录路径'),
    }),
  }
);

export { readFileTool, writeFileTool, executeCommandTool, listDirectoryTool };
```

创建了这几个 tool：
写文件（包含创建目录了）
读目录

![截图1](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo3ZfYqicSicJ7MFDLgsPT9yNZSOG1cPMzniaJPlg2u6mMTdTpWZJ1jR6Bwg/640?wx_fmt=png&from=appmsg)

![截图2](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo3pzWnpTeLVBNcA5kJiaRjmWYbWCJuuqQkKP7Fsr13ueujMqcTEsabNvw/640?wx_fmt=png&from=appmsg)

![截图3](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo3ic6PgpYHibfk5PQNJfiaoia1IPPOtsJd01p8yJAZ2vRA61JrBM52tIh48Q/640?wx_fmt=png&from=appmsg)

![截图4](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo3xkvyWL41MDU3qfic3Cyj0cHIAnicLjqrnwEzI5yYwV4InNQvyvg7EzaQ/640?wx_fmt=png&from=appmsg)

```javascript
重要提示：命令在目录 "${workingDirectory}" 中执行成功。
如果需要在这个项目目录中继续执行命令，
请使用 workingDirectory: "${workingDirectory}" 参数，
不要使用 cd 命令。
```

![截图5](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo3aV1m17X0Edd5JicGqEicb4fsdJicVPrmDrnibadq94skjX0boz1Gg4fvibQ/640?wx_fmt=png&from=appmsg)

每个 tool 都是 name、description 以及基于 zod 声明的参数格式。
接下来就可以调用了：
创建 src/mini-cursor.mjs

```javascript
import 'dotenv/config';
import { ChatOpenAI } from '@langchain/openai';
import { HumanMessage, SystemMessage, ToolMessage } from '@langchain/core/messages';
import { executeCommandTool, listDirectoryTool, readFileTool, writeFileTool } from './all-tools.mjs';

const model = new ChatOpenAI({
    modelName: "qwen-plus",
    apiKey: process.env.OPENAI_API_KEY,
    temperature: 0,
    configuration: {
        baseURL: process.env.OPENAI_BASE_URL,
    },
});


const tools = [
    readFileTool,
    writeFileTool,
    executeCommandTool,
    listDirectoryTool,
];

// 绑定工具到模型
const modelWithTools = model.bindTools(tools);

// Agent 执行函数
asyncfunction runAgentWithTools(query, maxIterations = 30) {
    const messages = [
        new SystemMessage(`你是一个项目管理助手，使用工具完成任务。

当前工作目录: ${process.cwd()}

工具：
1. read_file: 读取文件
2. write_file: 写入文件
3. execute_command: 执行命令（支持 workingDirectory 参数）
4. list_directory: 列出目录

重要规则 - execute_command：
- workingDirectory 参数会自动切换到指定目录
- 当使用 workingDirectory 时，绝对不要在 command 中使用 cd
- 错误示例: { command: "cd react-todo-app && pnpm install", workingDirectory: "react-todo-app" }
这是错误的！因为 workingDirectory 已经在 react-todo-app 目录了，再 cd react-todo-app 会找不到目录
- 正确示例: { command: "pnpm install", workingDirectory: "react-todo-app" }
这样就对了！workingDirectory 已经切换到 react-todo-app，直接执行命令即可

回复要简洁，只说做了什么`),
        new HumanMessage(query)
    ];

    for (let i = 0; i < maxIterations; i++) {
        console.log(`⏳ 正在等待 AI 思考...`);
        const response = await modelWithTools.invoke(messages);
        messages.push(response);

        // 检查是否有工具调用
        if (!response.tool_calls || response.tool_calls.length === 0) {
            console.log(`\n✨ AI 最终回复:\n${response.content}\n`);
            return response.content;
        }

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
```

代码大部分我们都写过。
首先创建大模型对象：

![截图6](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo3kF3P5gJdtyoIXyGyZBtUdedrgsD9FkX3C6lXKgZ6wTAdzgJpLMVIog/640?wx_fmt=png&from=appmsg)

temperature 温度指定为 0，不让 AI 随意发挥。
模型用 qwen-plus，这个更好一点。
然后把 tools 绑定到模型：

![截图7](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo3yWMz6HJGpCicDFh7MCr7PVKBibugGUGXJJMx9U9R1xvZfDCuwiclS6tyw/640?wx_fmt=png&from=appmsg)

后面就是返回的对话了，因为可能会反复对话、返回调用 tools 很多次，这里加了个最大限制。
具体的调用过程和之前一样：
用 System message 指定 AI 可以做什么，回答的规范：

![截图8](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo35eutsuTUU3nlKEopY70tramJEK7kSGtxrHVqIWRhe7lyh7btAibwqicw/640?wx_fmt=png&from=appmsg)

![截图9](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo3z3eRxmub8HOfFUgVic5B4j3ib2m4BeEoECa9ngof56fE5JCCP799heUw/640?wx_fmt=png&from=appmsg)

我还特意说明了下 cd 的问题，有了 cwd 之后，就不用 cd 了。
之后把调用 tool 返回的内容封装成 ToolMessage：

![截图10](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo3ia3b8W7b1G5tXShqWSB9AnibMcmNHbs2KasjsicVTicoJoXh7POXSScPcQ/640?wx_fmt=png&from=appmsg)

这样，模型、工具、调用流程就搭建完了。
接下来我们开始调用：
首先我们用 chalk 加点颜色，不然都是白色不好看：

```javascript
pnpm install chalk
```

这行背景变绿：

![截图11](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo3gpSYrSlwAlp0Bxia1ia1zm48X3Q8dzVciaJD1QJGjwDAQLL00dT5PYncQ/640?wx_fmt=png&from=appmsg)

```javascript
import chalk from 'chalk';

console.log(chalk.bgGreen(`⏳ 正在等待 AI 思考...`));
```

接下来写个 case：

![截图12](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo3APqLyIFkx3QVwKZRoIOibqcXgXqIwW30UykZt1NM7VRZTeTFqPD1zog/640?wx_fmt=png&from=appmsg)

```javascript
const case1 = `创建一个功能丰富的 React TodoList 应用：

1. 创建项目：echo -e "n\nn" | pnpm create vite react-todo-app --template react-ts
2. 修改 src/App.tsx，实现完整功能的 TodoList：
 - 添加、删除、编辑、标记完成
 - 分类筛选（全部/进行中/已完成）
 - 统计信息显示
 - localStorage 数据持久化
3. 添加复杂样式：
 - 渐变背景（蓝到紫）
 - 卡片阴影、圆角
 - 悬停效果
4. 添加动画：
 - 添加/删除时的过渡动画
 - 使用 CSS transitions
5. 列出目录确认

注意：使用 pnpm，功能要完整，样式要美观，要有动画效果

之后在 react-todo-app 项目中：
1. 使用 pnpm install 安装依赖
2. 使用 pnpm run dev 启动服务器
`;

try {
  await runAgentWithTools(case1);
} catch (error) {
  console.error(`\n❌ 错误: ${error.message}\n`);
}
```

告诉它创建一个 todo app，然后安装依赖，跑起来。
你是不是在 cursor 里经常做这种事情？
今天用自己写的工具来做：

```javascript
node ./src/mini-cursor.mjs
```

▶ **[视频5](http://mpvideo.qpic.cn/0bc3buackaaa4eamqsciy5uvadodeugqajia.f10002.mp4?dis_k=afe63ceff21f8b4622cca63b5f435c8a&dis_t=1783680878&play_scene=10110&auth_info=cPrmqtspJ+zfutghW5fliconAB4HdG1uTElvMU44cGNNcTdGMwUDcCEuKEw5LW5VbQUXJA0=&auth_key=61de71ddea2473531d9ad3e8af3006c8)**

可以看到，过程中调用了各种工具：

![截图13](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo3Pvw7BeMGjx72FBuia4uiaDn7SHKiaYGjvQbgDibaKlRhK4XUn6dXIAWjXA/640?wx_fmt=png&from=appmsg)

![截图14](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo3Gn4RMzeeQKKgZjLuY2yza7cOFSS2bzESL2GiaHmuZtt9SricR21NQKPw/640?wx_fmt=png&from=appmsg)

![截图15](https://mmbiz.qpic.cn/sz_mmbiz_png/JnZIbTicL4jVCQicQq5pbFfMlMhLnbUbo34BEiaylqTSD6jXMb8xSIIOzN1dJjRSibyTjkNZn9szHUOn3rsz9QVHTA/640?wx_fmt=png&from=appmsg)

我们写的 tool 都用上了。
读取目录、写入文件、读取文件、执行命令
当然，这个过程慢很正常，生成过程本来就慢，我们没用流式展示过程，其实你等待的时间一直在输出内容。流式相关的后面再做。
但是，这个项目的代码是用我们写的 mini cursor 自动创建、自动跑起来的：

▶ **[视频6](http://mpvideo.qpic.cn/0bc3ayaayaaagyaofakinzuvabwdbqdaadaa.f10002.mp4?dis_k=dab64fbecbd1f7443e7672e7c3a09b1a&dis_t=1783680878&play_scene=10110&auth_info=VfiT5Rdw7d692iRcxeDTkHcAHAMgaDlPTWxgHTp5Z05zMUc1UVRxICkqST5/aw83VRcmCQ==&auth_key=93366ac670c66bacabf8e4ce2ba9b29f)**

![todoList](./images/03-todolist.png)

它和 cursor 肯定有差距，但是已经实现部分功能了。
我们不是想真的实现 cursor，只是要知道它的实现原理。
代码上传了课程仓库： https://github.com/QuarkGluonPlasma/ai-agent-course-code/tool-test
## 总结
这节我们创建了更多的 tool，比如目录、文件的读写，还有用 spawn 执行命令。
我们基于这些 tool 实现了部分 cursor 功能，最终效果是，它可以帮你创建项目，写入文件，执行安装依赖、跑项目的命令。
相信学到这，你就知道 cursor 的大概实现原理了。
你也可以基于 tool + llm 来做一些自己想做的功能，边学边练，AI 学起来还是很有趣的！
