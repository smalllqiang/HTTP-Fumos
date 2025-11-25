import json
from typing import List
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from config import *

def list_files(dest_path: Path) -> List[Path]:
    folder = dest_path
    return [item for item in folder.iterdir() if item.is_file()]

def wrap_text(text: str, font, max_width: int, draw=None) -> list:
    """将长文本按像素宽度折行，返回行列表。

    - text: 原始文本，支持换行符 `\n`。
    - font: 用于测量文本的字体对象。
    - max_width: 每行最大像素宽度。
    - draw: 可选的 ImageDraw 对象，用于测量；若为 None 会创建临时对象。
    """
    if draw is None:
        tmp_img = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(tmp_img)

    lines: list = []
    # 保留显式换行符
    paragraphs = text.splitlines() or [""]
    for para in paragraphs:
        if not para:
            lines.append("")
            continue

        # 如果包含空格，优先按单词拆分（适用于英文）。否则按字符拆分（适用于中文）。
        if " " in para:
            words = para.split(" ")
            cur = ""
            for w in words:
                test = (cur + " " + w).strip() if cur else w
                bbox = draw.textbbox((0, 0), test, font=font)
                if bbox[2] - bbox[0] <= max_width:
                    cur = test
                else:
                    if cur:
                        lines.append(cur)
                    # 如果单个 word 本身就超长，则逐字拆
                    wbbox = draw.textbbox((0, 0), w, font=font)
                    if wbbox[2] - wbbox[0] <= max_width:
                        cur = w
                    else:
                        # 按字符累加
                        part = ""
                        for ch in w:
                            tb = (part + ch)
                            bb = draw.textbbox((0, 0), tb, font=font)
                            if bb[2] - bb[0] <= max_width:
                                part = tb
                            else:
                                if part:
                                    lines.append(part)
                                part = ch
                        if part:
                            cur = part
            if cur:
                lines.append(cur)
        else:
            # 无空格：按字符拆分（适合中文）
            cur = ""
            for ch in para:
                test = cur + ch
                bb = draw.textbbox((0, 0), test, font=font)
                if bb[2] - bb[0] <= max_width:
                    cur = test
                else:
                    if cur:
                        lines.append(cur)
                    cur = ch
            if cur:
                lines.append(cur)

    return lines

def process_image(input_path: Path, output_path: Path, status_code_font_path: Path, description_en_font_path: Path, description_zh_font_path: Path, title_text: str, content_text_en: str, content_text_zh: str):
    img = Image.open(input_path).convert("RGB")
    w, h = img.size

    white_border = 2
    img_with_white = Image.new("RGB", (w + 2*white_border, h + 2*white_border), "white")
    img_with_white.paste(img, (white_border, white_border))

    top, left, right = 30, 45, 45
    title_font = ImageFont.truetype(status_code_font_path, 50)
    content_en_font = ImageFont.truetype(description_en_font_path, 35)
    content_zh_font = ImageFont.truetype(description_zh_font_path, 35)

    # 使用临时绘图对象计算文字尺寸与自动换行（在添加黑边之前）
    dummy_img = Image.new("RGB", (1, 1))
    dummy_draw = ImageDraw.Draw(dummy_img)

    title_bbox = dummy_draw.textbbox((0, 0), title_text, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    title_h = title_bbox[3] - title_bbox[1]

    # 最大文字宽度（在白边内，留 20px 水平内边距）
    max_text_width = max(10, img_with_white.size[0] - 20)

    en_lines = wrap_text(content_text_en, content_en_font, max_text_width, dummy_draw)
    zh_lines = wrap_text(content_text_zh, content_zh_font, max_text_width, dummy_draw)

    # 计算每段的宽高（含行间距）
    line_spacing = 6

    content_en_w = 0
    content_en_h = 0
    en_line_heights = []
    for ln in en_lines:
        bb = dummy_draw.textbbox((0, 0), ln, font=content_en_font)
        w_line = bb[2] - bb[0]
        h_line = bb[3] - bb[1]
        content_en_w = max(content_en_w, w_line)
        en_line_heights.append(h_line)
        content_en_h += h_line
    if len(en_lines) > 1:
        content_en_h += line_spacing * (len(en_lines) - 1)

    content_zh_w = 0
    content_zh_h = 0
    zh_line_heights = []
    for ln in zh_lines:
        bb = dummy_draw.textbbox((0, 0), ln, font=content_zh_font)
        w_line = bb[2] - bb[0]
        h_line = bb[3] - bb[1]
        content_zh_w = max(content_zh_w, w_line)
        zh_line_heights.append(h_line)
        content_zh_h += h_line
    if len(zh_lines) > 1:
        content_zh_h += line_spacing * (len(zh_lines) - 1)

    # 总文字高度：标题 + 间距 + 英文段高度 + 间距 + 中文段高度 + 底部缓冲
    text_total_height = title_h + 10 + content_en_h + 6 + content_zh_h + 20
    bottom = text_total_height

    # 向下扩展图片以容纳文字（在添加黑边之前）
    extended_w = img_with_white.size[0]
    extended_h = img_with_white.size[1] + bottom
    # 扩展区域使用黑色背景，这样白色文字能在黑色区域上可见
    img_extended = Image.new("RGB", (int(extended_w), int(extended_h)), "black")
    img_extended.paste(img_with_white, (0, 0))

    # 在扩展后的画布上绘制文字（坐标不包含黑边的 top 偏移）
    draw = ImageDraw.Draw(img_extended)

    title_x = (extended_w - title_w) // 2
    title_y = img_with_white.size[1] + 10
    draw.text((title_x, title_y), title_text, font=title_font, fill="white")

    # 绘制英文描述（逐行）
    y = title_y + title_h + 10
    for idx, ln in enumerate(en_lines):
        bb = draw.textbbox((0, 0), ln, font=content_en_font)
        w_line = bb[2] - bb[0]
        h_line = bb[3] - bb[1]
        x = (extended_w - w_line) // 2
        draw.text((x, y), ln, font=content_en_font, fill="white")
        y += h_line + line_spacing

    # 绘制中文描述（逐行）
    y += 0  # 保持与上面计算的一致间距（en 段后已有 line_spacing）
    for idx, ln in enumerate(zh_lines):
        bb = draw.textbbox((0, 0), ln, font=content_zh_font)
        w_line = bb[2] - bb[0]
        h_line = bb[3] - bb[1]
        x = (extended_w - w_line) // 2
        draw.text((x, y), ln, font=content_zh_font, fill="white")
        y += h_line + line_spacing

    # 最后添加黑色外框并把扩展后的图贴上去
    bottom_black = 30  # 用户指定下方黑边为 30px
    final_w = img_extended.size[0] + left + right
    final_h = img_extended.size[1] + top + bottom_black
    img_with_black = Image.new("RGB", (int(final_w), int(final_h)), "black")
    img_with_black.paste(img_extended, (left, top))

    img_with_black.save(output_path, "JPEG")

def get_description(status_code: str, file_path: Path):
    with open(file_path, mode="r", encoding="utf-8") as f:
        data = json.load(f)
        description = data.get(status_code)
        return description.get("description_en"), description.get("description_zh")

if __name__ == "__main__":
    jpeg_imgs = list_files(jpeg_imgs)
    for img in jpeg_imgs:
        en_text, zh_text = get_description(img.stem, description_file_path)
        output_path = text_imgs / img.name
        if output_path.exists():
            # 目标文件已存在，跳过
            continue
        process_image(img, output_path, status_code_font, description_en_font, description_zh_font, img.stem, en_text, zh_text)