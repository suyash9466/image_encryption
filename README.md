# Pixel Manipulation Image Encryption

## What it does
Encrypts and decrypts images by:
1. Swapping adjacent pixels horizontally
2. XOR-ing every RGB channel with a key (0–255)

Both operations are self-inverse — running encrypt + decrypt with the same key
restores the original image perfectly.

## Requirements
```
pip install Pillow
```

## How to run
```
python image_encrypt.py
```

## Supported formats
PNG, JPG, BMP, TIFF — anything Pillow supports.

> **Tip:** Use PNG for output to avoid JPEG re-compression artifacts.

## Example
```
Input : photo.png  key=42
Output: photo_enc.png  (looks like noise)
Decrypt photo_enc.png with key=42 → original photo restored
```
