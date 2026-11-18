import dotenv from 'dotenv';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { ChatOpenAI } from '@langchain/openai';
import { tool } from '@langchain/core/tools';
import { HumanMessage, SystemMessage, ToolMessage } from '@langchain/core/messages';
import fs from 'node:fs/promises';
import { z } from 'zod';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.resolve(__dirname, '../.env.local') });

const model = new ChatOpenAI({
    modelName: process.env.MODEL_NAME,
    apiKey: process.env.DASHSCOPE_API_KEY,
    temperature: 0,
    configuration: {
        baseURL: process.env.OPENAI_BASE_URL,
    },
});

const readFileTool = tool(
    async ({ filePath }) => {
        const content = await fs.readFile(filePath, 'utf-8');
        console.log(`  [工具调用] read_file("${filePath}") - 成功读取 ${content.length} 字节`);
        return `文件内容:\n${content}`;
    },
    {
        name: 'read_file',
        description: '用此工具来读取文件内容。当用户要求读取文件、查看代码、分析文件内容时，调用此工具。输入文件路径（可以是相对路径或绝对路径）。',
        schema: z.object({
            filePath: z.string().describe('要读取的文件路径'),
        }),
    }
);

const tools = [
    readFileTool
];

// 将工具绑定到模型上
const modelWithTools = model.bindTools(tools);

const messages = [
    new SystemMessage(`你是一个代码助手，可以使用工具读取文件并解释代码。

工作流程：
1. 用户要求读取文件时，立即调用 read_file 工具
2. 等待工具返回文件内容
3. 基于文件内容进行分析和解释

可用工具：
- read_file: 读取文件内容（使用此工具来获取文件内容）
`),

    new HumanMessage('请读取 src/tool-file-read.mjs 文件内容并解释代码')
];

let response = await modelWithTools.invoke(messages);
// console.log(response);
// 把AI返回的内容加入到消息列表中，以便后续的对话可以参考之前的内容
messages.push(response);

// 循环处理工具调用，直到没有工具调用为止
while (response.tool_calls && response.tool_calls.length > 0) {
    console.log(`\n[检测到 ${response.tool_calls.length} 个工具调用]`);

    // 1. 执行所有工具调用
    const toolResults = await Promise.all(
        response.tool_calls.map(async (toolCall) => {
            const tool = tools.find(t => t.name === toolCall.name);
            if (!tool) {
                return `错误: 找不到工具 ${toolCall.name}`;
            }

            console.log(`  [执行工具] ${toolCall.name}(${JSON.stringify(toolCall.args)})`);
            try {
                const result = await tool.invoke(toolCall.args);
                return result;
            } catch (error) {
                return `错误: ${error.message}`;
            }
        })
    );

    // 2. 将结果包装成 ToolMessage，通过 tool_call_id 与调用配对
    response.tool_calls.forEach((toolCall, index) => {
        messages.push(
            new ToolMessage({
                content: toolResults[index],
                tool_call_id: toolCall.id,
            })
        );
    });

    // 3. 将所有拼接好的messages 再次调用模型，传入工具结果
    response = await modelWithTools.invoke(messages);

}

console.log('AI最终回答:');
console.log(response.content);