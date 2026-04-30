## 如何使用

### 图像预处理

- 将文件格式转为jpg
- 去除所有元数据(务必不要上传带有元数据的图像)

### 图像处理

创建虚拟环境.  
在[tools/config.py](./config.py)文件中写入你希望的路径.

> 本项目在生成的图像中使用`Maple Mono`字体, 项目地址[subframe7536/Maple-font](https://github.com/subframe7536/Maple-font), 该字体依据 SIL Open Font License 1.1 授权.  
> 协议全文请参见[tools/OFL.txt](./OFL.txt)

在`raw_dir`中放入图像文件, 命名为`{status_code}.jpg`, 如果对应status code已有图像, 在`{status_code}`后按顺序加上`_n`.  
在[tools/scale.json](./scale.json)文件中加入图像, 格式参考该文件.  
如无, 在[tools/descriptions.json](./descriptions.json)文件中加入相应status code的描述文字.  
执行[tools/img_process.py](./img_process.py), 获得所有成品图像.

### 上传

将获得的图像上传至图床 (也可以直接使用github的静态资源服务)

### 更新KV存储

以`{status_code}`为键, 图床返回的url为值, 上传至cf的KV存储中

可以使用[tools/uploadKV.js](./uploadKV.js)工具  
你需要创建一个[KV_data.json](./KV_data.json)文件, 格式为

```json
[
    {
        "404": "url"
    }
]
```

(node.js环境下)你需要创建一个[config.mjs](./config.mjs)文件, 在其中填入

```javascript
export const accountId = "你的cf账户id";
export const namespaceId = "你的KV存储命名空间id";
export const apiToken = "有 Workers KV 写入权限的api密钥";
```

之后执行`uploadKV.js`
