import os
from .utils import get_images

def preprocess_images(input_folder):
    """
    Rename images in-place to the format frame###.ext (e.g., frame001.jpg).
    ⚠️ This will overwrite original filenames.

    Args:
        input_folder (str): Folder containing images to rename.
    """
    images = get_images(input_folder)
    
    for idx, img_name in enumerate(images, start=1):
        ext = os.path.splitext(img_name)[1].lower()
        new_name = f"frame{idx:03d}{ext}"
        old_path = os.path.join(input_folder, img_name)
        new_path = os.path.join(input_folder, new_name)
        os.rename(old_path, new_path)

    print(f"\n[⚠️] Renamed {len(images)} files in '{input_folder}' using pattern 'frame###.ext'.")
    print("[🔁] Original filenames are lost.\n")
