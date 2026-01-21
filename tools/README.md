## 如何使用

### 配置
首先在`/tools`下创建一个config.py文件, 需要以下内容:  
```python
from pathlib import Path

EXIFTOOL_EXECUTABLE = r"/path/to/your/exiftool" # Exiftool的路径, Exiftool用于清除图像的所有exif数据

raw_imgs_path = Path("path", "to", "your", "path") # 原始图像路径
no_meta_data_imgs_path = Path("path", "to", "your", "path") # 清除了所有元数据的图像输出路径
jpeg_imgs_path = Path("path", "to", "your", "path") # jpg格式的图像输出路径
resize_imgs_path = Path("path", "to", "your", "path") # 重新调整大小的图像输出路径
text_imgs_path = Path("path", "to", "your", "path") # 加入了边框和文字的图像的输出路径

status_code_font = Path("path", "to", "your", "font") # 状态码所用字体路径, 本项目目前使用的字体全部为 等线 Bold , 因版权问题不可能上传, 请自行寻找.  
description_en_font = Path("path", "to", "your", "font") # 英文描述文字所用字体路径
description_zh_font = Path("path", "to", "your", "font") # 中文描述文字所用字体路径

description_file_path = Path("path", "to", "description", "file") # 描述文字路径
```

创建虚拟环境, 执行`pip install -r requirements.txt`, 安装需要的库.  

### 图像处理
将待处理的图像命名为`{status_code}.{ext}`(注意ext需要与MIME类型相符, 因为ExifTool无法处理不相符的情况), 放在`raw_imgs_path`中  
如无, 在`descriptions.json`相应status code的描述文字
执行`img_process.py`, 获得所有图像  

### 上传
将获得的图像上传至图床 (也可以直接使用github的图床)  

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
export const accountId   = "你的cf账户id";
export const namespaceId = "你的KV存储命名空间id";
export const apiToken    = "有 Workers KV 写入权限的api密钥";
```

之后执行`uploadKV.js`  