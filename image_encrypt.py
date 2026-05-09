import os
import sys
from PIL import Image

def xor_pixels(img, key):
    """Apply XOR with key to every channel of every pixel."""
    pixels = list(img.getdata())
    mode = img.mode

    processed = []
    for px in pixels:
        if mode == 'RGB':
            processed.append(tuple((c ^ key) & 0xFF for c in px))
        elif mode == 'RGBA':
            r, g, b, a = px
            processed.append(((r ^ key) & 0xFF, (g ^ key) & 0xFF, (b ^ key) & 0xFF, a))
        else:
            # grayscale
            processed.append((px ^ key) & 0xFF)

    new_img = Image.new(mode, img.size)
    new_img.putdata(processed)
    return new_img

def swap_pixels(img):
    """Swap adjacent pixels horizontally as an extra scramble layer."""
    pixels = list(img.getdata())
    width, height = img.size

    for y in range(height):
        for x in range(0, width - 1, 2):
            i = y * width + x
            j = i + 1
            pixels[i], pixels[j] = pixels[j], pixels[i]

    new_img = Image.new(img.mode, img.size)
    new_img.putdata(pixels)
    return new_img

def encrypt_image(input_path, output_path, key):
    img = Image.open(input_path)
    # Step 1 — swap adjacent pixels
    img = swap_pixels(img)
    # Step 2 — XOR all channels
    img = xor_pixels(img, key)
    img.save(output_path)
    print(f"  Encrypted image saved to: {output_path}")

def decrypt_image(input_path, output_path, key):
    img = Image.open(input_path)
    # Reverse: XOR first (self-inverse), then swap again (also self-inverse)
    img = xor_pixels(img, key)
    img = swap_pixels(img)
    img.save(output_path)
    print(f"  Decrypted image saved to: {output_path}")

def get_key():
    while True:
        try:
            val = int(input("Enter encryption key (0-255): "))
            if 0 <= val <= 255:
                return val
            print("  Key must be between 0 and 255.")
        except ValueError:
            print("  Please enter a valid integer.")

def get_file(prompt, must_exist=True):
    while True:
        path = input(prompt).strip().strip('"')
        if must_exist and not os.path.isfile(path):
            print(f"  File not found: {path}")
        else:
            return path

def main():
    print("=" * 52)
    print("   Pixel Manipulation Image Encryption")
    print("=" * 52)

    if 'PIL' not in sys.modules and 'Pillow' not in sys.modules:
        pass  # already imported at top

    while True:
        print("\nOptions:")
        print("  1. Encrypt an image")
        print("  2. Decrypt an image")
        print("  3. Exit")

        choice = input("\nChoose (1-3): ").strip()

        if choice == '1':
            src = get_file("Input image path: ")
            name = input("Output filename (e.g. encrypted.png): ").strip()
            # save in the same folder as the input image
            dst = os.path.join(os.path.dirname(os.path.abspath(src)), name)
            key = get_key()
            try:
                encrypt_image(src, dst, key)
                print(f"  Full path: {dst}")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == '2':
            src = get_file("Encrypted image path: ")
            name = input("Output filename (e.g. decrypted.png): ").strip()
            dst = os.path.join(os.path.dirname(os.path.abspath(src)), name)
            key = get_key()
            try:
                decrypt_image(src, dst, key)
                print(f"  Full path: {dst}")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == '3':
            print("\nBye!\n")
            break

        else:
            print("  Invalid option.")

if __name__ == "__main__":
    main()
