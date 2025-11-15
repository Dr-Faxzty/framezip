import os
import shutil
import imageio.v3 as iio
from PIL import Image
import numpy as np
from rich.progress import Progress
from .preprocessing import preprocess_images
from .utils import get_images
from .sorter import sort_frames

def images_to_video(input_folder, output_file, framerate="1", heuristic_sort=True):
    """
    Convert a sequence of images into a video using FFmpeg.
    
    Args:
        input_folder (str): Folder containing images (e.g., frame001.jpg, frame002.jpg...)
        output_file (str): Name of the output video (e.g., output.mp4)
        framerate (str or int): FPS of the video (1 = 1 image per second)
    """
    preprocess_images(input_folder)

    frame_paths = [os.path.join(input_folder, p) for p in get_images(input_folder)]

    if not frame_paths:
        raise RuntimeError("\nNo images found in the temporary folder")
    
    sizes = [Image.open(p).size for p in frame_paths]
    width = max(s[0] for s in sizes)
    height = max(s[1] for s in sizes)

    frames = []
    with Progress() as p:
        task = p.add_task("[yellow]Converting images...", total=len(frame_paths))
        for path in frame_paths:
            empty = Image.new("RGB", (width, height), (0, 0, 0))
            with Image.open(path) as img:
                empty.paste(img, (0, 0))
                frames.append(np.array(empty))
            p.update(task, advance=1)
            
    if heuristic_sort:
        sorted_frames, frames_idxs = sort_frames(frames, os.path.join(input_folder, "mses.csv"))
        output_image_folder = input_folder + "rd"
        os.makedirs(output_image_folder, exist_ok=True)

        for i, idx in enumerate(frames_idxs):
            output_path = os.path.join(output_image_folder, f'frame{i+1:03d}.jpg')
            file = frame_paths[idx]
            shutil.copy2(file, output_path)
        
        frames = sorted_frames

    print("\n[▶] Video creation in progress...")
    try:
        iio.imwrite(output_file, frames, fps=int(framerate))
    except Exception as e:
        print(f"\n[❌] Error while creating video: {e}")
        return
    print(f"\n[✓] Video created: {output_file}")