import json
import os
from pathlib import Path

from config import *

from PIL import ImageFile, Image


def crop_img(img: ImageFile.ImageFile, config: dict) -> Image.Image:
    crop_data: dict[str, list[int]] = config["crop"]
    resize_data: list[int] = config["resize"]
    x1, y1 = crop_data["top_left"]
    x2, y2 = crop_data["bottom_right"]
    target_w, target_h = resize_data[0], resize_data[1]
    cropped = img.crop((x1, y1, x2, y2))
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    return resized


def add_border(
    img: Image.Image,
    border_color: str = "#000000",
    top: int = 2,
    bottom: int = 2,
    left: int = 2,
    right: int = 2,
) -> Image.Image:
    # 获取原始图像的大小和模式
    width, height = img.size
    mode = img.mode

    # 计算新图像的大小
    new_width = width + left + right
    new_height = height + top + bottom

    # 将十六进制颜色转换为 RGB 元组
    if border_color.startswith("#"):
        border_color = border_color[1:]
    rgb = tuple(int(border_color[i : i + 2], 16) for i in (0, 2, 4))

    # 创建新图像并填充边框颜色
    new_img = Image.new(mode, (new_width, new_height), rgb)

    # 将原始图像粘贴到新图像的指定位置
    new_img.paste(img, (left, top))

    return new_img


def get_description(status_code: str, description_file_path: Path):
    with open(description_file_path, mode="r", encoding="utf-8") as f:
        data = json.load(f)
        description = data.get(status_code)
        return description.get("description_en"), description.get("description_zh")


if __name__ == "__main__":
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    with open(config_path, "r", encoding="utf-8") as f:
        config: dict[str, dict] = json.load(f)
    for image, params in config.items():
        image_path = raw_dir / image
        output_path = output_dir / image
        with Image.open(image_path) as img:
            croped_img = crop_img(img, params)
            b_img = add_border(croped_img, "#000000", 3, 3, 3, 3)
            w_img = add_border(b_img, "#FFFFFF", 2, 2, 2, 2)
            b_img = add_border(w_img, "#000000", 45, 145, 70, 70)
            b_img.save(str(output_path))
