import { ChatOpenAI } from '@langchain/openai';
import dotenv from 'dotenv';
dotenv.config({
    path: '.env.local',
});

const model = new ChatOpenAI({
    modelName: "glm-5.3",
    apiKey: process.env.DASHSCOPE_API_KEY,
    configuration: {
        baseURL: process.env.OPENAI_BASE_URL,
    },
});

const response = await model.invoke("介绍下自己");
console.log(response.content);