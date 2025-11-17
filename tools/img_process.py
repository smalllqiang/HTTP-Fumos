import sys
import shutil
import exiftool
from typing import List
from pathlib import Path

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

if __name__ == "__main__":
    dest_path = Path("..", "temp", "raw_imgs")
    EXIFTOOL_EXECUTABLE = r"D:\exiftool-12.98_64\exiftool.exe"
    output_dir = Path("..", "temp", "no_meta_data_imgs")
    imgs = list_files(dest_path)
    # print(imgs)
    strip_imgs(imgs, output_dir)

