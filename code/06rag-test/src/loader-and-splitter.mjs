import dotenv from "dotenv";
import "cheerio";
import { CheerioWebBaseLoader } from "@langchain/community/document_loaders/web/cheerio";

dotenv.config({
    path: ".env.local",
});

const cheerioLoader = new CheerioWebBaseLoader(
"https://juejin.cn/post/7350571075548397618",
  {
    selector: '.main-area p'
  }
);

const documents = await cheerioLoader.load();

console.log(documents);