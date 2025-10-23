#!/usr/bin/env python3
import os
from pathlib import Path
from PIL import Image
import math

# --- CONFIG ---
TARGET_SIZE = 1_000_000      # target max bytes (1 MB)
MIN_PROCESS_SIZE = 1_000_000 # only process files larger than 2 MB
JPEG_QUALITY_STEP = 5        # for iterative JPEG compression

def get_file_size(path):
    return path.stat().st_size

def compress_jpeg(path):
    """Reduce JPEG quality until below target size."""
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    quality = 90

    with Image.open(path) as im:
        im = im.convert("RGB")  # ensure compatibility

        while quality > 10:
            im.save(tmp_path, "JPEG", optimize=True, quality=quality)
            if get_file_size(tmp_path) <= TARGET_SIZE:
                break
            quality -= JPEG_QUALITY_STEP

    os.replace(tmp_path, path)

def compress_png(path):
    """Scale PNG based on size ratio until below target size."""
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    size_bytes = get_file_size(path)

    if size_bytes <= TARGET_SIZE:
        return

    # Compute scaling factor using sqrt(target / current)
    ratio = math.sqrt(TARGET_SIZE / size_bytes)
    ratio = max(0.1, min(1.0, ratio))  # clamp between 10% and 100%
    percent = int(ratio * 100)

    with Image.open(path) as im:
        w, h = im.size
        new_size = (max(1, int(w * ratio)), max(1, int(h * ratio)))
        im = im.convert("RGBA") if im.mode in ("P", "LA") else im.convert("RGB")
        im = im.resize(new_size, Image.LANCZOS)
        im.save(tmp_path, "PNG", optimize=True, compress_level=9)

    # If still too big, shrink iteratively by 10%
    while get_file_size(tmp_path) > TARGET_SIZE:
        with Image.open(tmp_path) as im:
            w, h = im.size
            im = im.resize((int(w * 0.9), int(h * 0.9)), Image.LANCZOS)
            im.save(tmp_path, "PNG", optimize=True, compress_level=9)

    os.replace(tmp_path, path)

def process_image(path):
    ext = path.suffix.lower()
    size = get_file_size(path)

    if size < MIN_PROCESS_SIZE:
        return

    print(f"Processing {path} ({size/1_048_576:.2f} MB)")

    if ext in [".jpg", ".jpeg"]:
        compress_jpeg(path)
    elif ext == ".png":
        compress_png(path)

    new_size = get_file_size(path)
    print(f"  → {new_size/1_048_576:.2f} MB\n")

def main():
    for root, _, files in os.walk("."):
        for name in files:
            if name.lower().endswith((".jpg", ".jpeg", ".png")):
                process_image(Path(root) / name)

if __name__ == "__main__":
    main()
