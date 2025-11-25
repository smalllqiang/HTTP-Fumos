import sys
import exiftool
from typing import List
from pathlib import Path
from PIL import Image

from config import *

def list_files(dest_path: Path) -> List[Path]:
    folder = dest_path
    return [item for item in folder.iterdir() if item.is_file()]

def strip_to_new_file(src_file: Path, output_dir: Path) -> Path:
    src_file = Path(src_file).expanduser().resolve()
    if not src_file.exists():
        raise FileNotFoundError(src_file)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    dst_file = output_dir / src_file.name
    if dst_file.exists():
        # 目标文件已存在，跳过
        return dst_file
    with exiftool.ExifTool(EXIFTOOL_EXECUTABLE) as et:
        et.execute(
            b"-all=",
            b"-o", str(dst_file).encode("utf-8"),
            str(src_file).encode("utf-8")
        )
    return dst_file

def strip_imgs(src_files: List[Path], output_dir: Path):
    for img in src_files:
        strip_to_new_file(img, output_dir)

def resize_and_convert_to_jpeg(files: List[Path], out_dir: Path, *, quality: int = 100, overwrite: bool = False) -> None:
    out_dir = out_dir.expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    for src in files:
        if not src.exists():
            print(f"跳过不存在文件: {src}", file=sys.stderr)
            continue
        dst = out_dir / f"{src.stem}.jpg"
        if dst.exists():
            # 目标文件已存在，跳过
            continue
        try:
            with Image.open(src) as im:
                # 如果宽度大于600，等比缩放到600宽
                if im.width > 600:
                    ratio = 600 / im.width
                    new_size = (600, int(im.height * ratio))
                    # 兼容 Pillow 新旧版本的 LANCZOS
                    try:
                        resample = Image.Resampling.LANCZOS
                    except AttributeError:
                        resample = 2  # BILINEAR
                    im = im.resize(new_size, resample)
                if im.mode in ("RGBA", "LA", "P"):
                    rgb_im = Image.new("RGB", im.size, (255, 255, 255))
                    rgb_im.paste(im, mask=im.split()[-1] if im.mode in ("RGBA", "LA") else None)
                else:
                    rgb_im = im.convert("RGB")
                rgb_im.save(dst, format="JPEG", quality=quality, optimize=True)
        except Exception as e:
            print(f"处理失败 {src}: {e}", file=sys.stderr)

if __name__ == "__main__":
    raw_imgs = list_files(dest_path)
    strip_imgs(raw_imgs, no_meta_data_imgs_output_dir)
    no_meta_data_imgs = list_files(no_meta_data_imgs_output_dir)
    resize_and_convert_to_jpeg(no_meta_data_imgs, jpeg_imgs)