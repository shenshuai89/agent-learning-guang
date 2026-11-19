import { PDFParse } from "pdf-parse";
import { Document } from "@langchain/core/documents";

const url = "https://arxiv.org/pdf/2408.09869";

// 1. 先把 PDF 下载成二进制数据
const res = await fetch(url);
if (!res.ok) {
  throw new Error(`下载失败: ${res.status} ${res.statusText}`);
}
const data = new Uint8Array(await res.arrayBuffer());

// 2. 交给 PDFParse 解析，拿到全部文本
const parser = new PDFParse({ data });
const result = await parser.getText();

// 3. 使用结果
console.log("总页数:", result.pages.length);
console.log("全文总字符数:", result.text.length);
console.log("--- 第 1 页前 300 字符 ---");
console.log(result.pages[0].text.slice(0, 300));

// 4. （RAG 场景）把每一页包装成 LangChain Document，方便后续切分和入库
const docs = result.pages.map(
  (p, i) =>
    new Document({
      pageContent: p.text,
      metadata: { page: i + 1, source: url },
    })
);
console.log("\n包装成 Document 的数量:", docs.length);

// 5. 解析完释放 worker 资源
await parser.destroy();
