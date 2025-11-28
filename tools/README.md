## 如何使用

### 配置
首先在`/tools`下创建一个config.py文件, 需要以下内容:
```python
from pathlib import Path

dest_path = Path("path", "to", "your", "path")
EXIFTOOL_EXECUTABLE = r"/path/to/your/exiftool"
no_meta_data_imgs_output_dir = Path("path", "to", "your", "path")
jpeg_imgs = Path("path", "to", "your", "path")
text_imgs = Path("path", "to", "your", "path")

status_code_font = Path("path", "to", "your", "font")
description_en_font = Path("path", "to", "your", "font")
description_zh_font = Path("path", "to", "your", "font")

description_file_path = Path("path", "to", "description", "file")
```

创建虚拟环境, 执行`pip install -r requirements.txt`, 安装需要的库.

### 图像处理
将待处理的图像命名为`{status_code}.jpg`, 放在`dest_path`中  
执行`img_process.py`, 获得去除元数据的jpeg格式图像  

然后执行`create_img_with_text.py`, 生成带有文字描述的图像.
> 在此之前, 最好看看`descriptions.json`中是否有对应的 status code.  

### 上传
将获得的图像上传至图床

### 更新KV存储
以`{status_code}`为键, 图床返回的url为值, 上传至cf的KV存储中.  

如果数据量大的话, 可以使用`uploadKV.js`工具.  
(node.js环境下)你需要创建一个`config.mjs`文件, 在其中填入
```javascript
export const accountId   = "你的cf账户id";
export const namespaceId = "你的KV存储命名空间id";
export const apiToken    = "有 Workers KV 写入权限的api密钥";
```
你还需要一个`KV_data.json`文件, 其中以类似
```json
[
    {
        "404": "url"
    }
}
```
的格式填入你的数据.  
之后执行`uploadKV.js`.