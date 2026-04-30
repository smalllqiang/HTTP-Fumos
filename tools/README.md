## 如何使用

### 图像预处理

- 将文件格式转为jpg
- 去除所有元数据(务必不要上传带有元数据的图像)

### 图像处理

创建虚拟环境.  
在`tools/config`文件中写入你希望的路径.  
在`raw_dir`中放入图像文件, 命名为`{status_code}.jpg`, 如果对应status code已有图像, 在`{status_code}`后按顺序加上`_n`.  
在`tools/scale.json`文件中加入图像, 格式参考该文件.  
如无, 在`tools/descriptions.json`文件中加入相应status code的描述文字.  
执行`img_process.py`, 获得所有成品图像.

### 上传

将获得的图像上传至图床 (也可以直接使用github的静态资源服务)

### 更新KV存储

以`{status_code}`为键, 图床返回的url为值, 上传至cf的KV存储中

如果数据量大的话, 可以使用`uploadKV.js`工具  
你需要创建一个`KV_data.json`文件, 其中以类似

```json
[
    {
        "404": "url"
    }
]
```

的格式填入你的数据  
(node.js环境下)你需要创建一个`config.mjs`文件, 在其中填入

```javascript
export const accountId = "你的cf账户id";
export const namespaceId = "你的KV存储命名空间id";
export const apiToken = "有 Workers KV 写入权限的api密钥";
```

之后执行`uploadKV.js`
