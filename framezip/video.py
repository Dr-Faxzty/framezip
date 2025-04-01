import os
import imageio.v3 as iio
from PIL import Image
import numpy as np
from .preprocessing import preprocess_images

def images_to_video(input_folder, output_file, framerate="1"):
    """
    Convert a sequence of images into a video using FFmpeg.
    
    Args:
        input_folder (str): Folder containing images (e.g., frame001.jpg, frame002.jpg...)
        output_file (str): Name of the output video (e.g., output.mp4)
        framerate (str or int): FPS of the video (1 = 1 image per second)
    """
    preprocess_images(input_folder)

    files = sorted(os.listdir(input_folder))
    if not files:
        raise RuntimeError("\nNo images found in the temporary folder")
    
    frame_paths = [os.path.join(input_folder, f) for f in files]

    base_image = Image.open(frame_paths[0])
    width, height = base_image.size
    width = (width // 16) * 16
    height = (height // 16) * 16

    frames = []
    for path in frame_paths:
        with Image.open(path) as img:
            img = img.convert("RGB").resize((width, height))
            frames.append(np.array(img))


    print("\n[▶] Video creation in progress...")
    try:
        iio.imwrite(output_file, frames, fps=int(framerate))
    except Exception as e:
        print(f"\n[❌] Error while creating video: {e}")
        return
    print(f"\n[✓] Video created: {output_file}")