#!/usr/bin/env python3
import os
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()  # Add HEIC/HEIF support to PIL

# --- CONFIG ---
TARGET_SIZE = 1_000_000      # target max bytes (1 MB)
MAX_DIMENSION = 600          # max pixels on longest side (covers 3in @ 2x retina)
JPEG_QUALITY = 85            # JPEG quality for thumbnail output

def get_file_size(path):
    return path.stat().st_size

def resize_to_max_dimension(im, max_dim=MAX_DIMENSION):
    """Return image scaled so its longest side is at most max_dim pixels."""
    w, h = im.size
    if max(w, h) <= max_dim:
        return im
    if w >= h:
        new_w, new_h = max_dim, max(1, int(h * max_dim / w))
    else:
        new_w, new_h = max(1, int(w * max_dim / h)), max_dim
    return im.resize((new_w, new_h), Image.LANCZOS)

def compress_jpeg(path):
    """Resize to MAX_DIMENSION and save as JPEG at JPEG_QUALITY."""
    tmp_path = path.with_suffix(path.suffix + ".tmp")

    with Image.open(path) as im:
        try:
            im.seek(0)
        except EOFError:
            pass
        im = im.convert("RGB")
        im = resize_to_max_dimension(im)
        im.save(tmp_path, "JPEG", optimize=True, quality=JPEG_QUALITY)

    os.replace(tmp_path, path)

def compress_png(path):
    """Resize to MAX_DIMENSION and save as PNG."""
    tmp_path = path.with_suffix(path.suffix + ".tmp")

    with Image.open(path) as im:
        im = im.convert("RGBA") if im.mode in ("P", "LA", "RGBA") else im.convert("RGB")
        im = resize_to_max_dimension(im)
        im.save(tmp_path, "PNG", optimize=True, compress_level=9)

    os.replace(tmp_path, path)


def convert_heic_to_png(path):
    """Convert HEIC/HEIF to PNG."""
    png_path = path.with_suffix(".png")
    tmp_path = png_path.with_suffix(".png.tmp")

    with Image.open(path) as im:
        im = im.convert("RGBA")
        im.save(tmp_path, "PNG", optimize=True)

    os.remove(path)  # remove original HEIC
    os.replace(tmp_path, png_path)

def convert_mpo_to_jpeg(path):
    """Convert MPO to single-frame JPEG and compress."""
    # Convert to .jpg extension
    jpg_path = path.with_suffix(".jpg")
    tmp_path = jpg_path.with_suffix(".jpg.tmp")

    with Image.open(path) as im:
        print(path)
        try:
            im.seek(0)  # use first frame
        except EOFError:
            pass
        im = im.convert("RGB")
        im.save(tmp_path, "JPEG", optimize=True, quality=90)

    os.remove(path)  # remove original MPO
    os.replace(tmp_path, jpg_path)

    # Then compress as a normal JPEG if needed
    # if get_file_size(jpg_path) > TARGET_SIZE:
    #     compress_jpeg(jpg_path)

def process_image(path):
    path = Path(path)
    ext = path.suffix.lower()

    print(f"Processing {path} ({get_file_size(path)/1_048_576:.2f} MB)")

    if ext in [".jpg", ".jpeg", ".mpo"]:
        compress_jpeg(path)
    elif ext == ".png":
        compress_png(path)

    print(f"  → {get_file_size(path)/1_048_576:.2f} MB\n")

def main():
    for root, _, files in os.walk("."):
        for name in files:
            if name.lower().endswith((".jpg", ".jpeg", ".png", ".mpo")):
                process_image(Path(root) / name)

if __name__ == "__main__":
    main()
