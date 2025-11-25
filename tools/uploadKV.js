/**
 * 批量上傳 JSON 鍵值對到 Cloudflare Workers KV
 *
 * 使用方法：
 * 1. 在項目根目錄創建 data.json，格式為：
 *    [
 *      {"foo":"bar"},
 *      {"hello":"world"}
 *    ]
 * 2. 修改下面的配置（accountId, namespaceId, apiToken）
 * 3. 執行：node uploadKV.js
 */

import fs from "fs";
import fetch from "node-fetch";
import { accountId, namespaceId, apiToken } from "./config.mjs";

// === 讀取 JSON 文件 ===
const data = JSON.parse(fs.readFileSync("KV_data.json", "utf8"));

// === 上傳函數 ===
async function uploadKV() {
  for (const obj of data) {
    const [key, value] = Object.entries(obj)[0]; // 每個對象只有一個鍵值對

    console.log(`正在上傳: ${key} => ${value}`);

    const res = await fetch(
      `https://api.cloudflare.com/client/v4/accounts/${accountId}/storage/kv/namespaces/${namespaceId}/values/${encodeURIComponent(key)}`,
      {
        method: "PUT",
        headers: {
          "Authorization": `Bearer ${apiToken}`,
          "Content-Type": "text/plain"
        },
        body: value
      }
    );

    const result = await res.json();
    if (!result.success) {
      console.error(`❌ 上傳失敗: ${key}`, result.errors);
    } else {
      console.log(`✅ 成功: ${key}`);
    }
  }
}

uploadKV().catch(err => console.error("程序錯誤:", err));
