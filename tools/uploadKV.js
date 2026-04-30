import fs from "fs";
import fetch from "node-fetch";
import { accountId, namespaceId, apiToken } from "./config.mjs";

const data = JSON.parse(fs.readFileSync("KV_data.json", "utf8"));

async function uploadKV() {
    for (const obj of data) {
        const [key, value] = Object.entries(obj)[0]; // 每个对象只有一个键值对

        console.log(`正在上传: ${key} => ${value}`);

        const res = await fetch(
            `https://api.cloudflare.com/client/v4/accounts/${accountId}/storage/kv/namespaces/${namespaceId}/values/${encodeURIComponent(key)}`,
            {
                method: "PUT",
                headers: {
                    Authorization: `Bearer ${apiToken}`,
                    "Content-Type": "text/plain",
                },
                body: value,
            },
        );

        const result = await res.json();
        if (!result.success) {
            console.error(`❌ 上传失败: ${key}`, result.errors);
        } else {
            console.log(`✅ 成功: ${key}`);
        }
    }
}

uploadKV().catch((err) => console.error("程序错误:", err));
