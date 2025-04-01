import os
import shutil
import imageio.v3 as iio

def video_to_images(video_path, output_folder):
    """
    Extract frames from a video and save them as images.
    
    Args:
        video_path (str): Path to the input video file.
        output_folder (str): Directory where the extracted images will be saved.
    """
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    print("\n[🔄] Extracting images from video...")

    for i, frame in enumerate(iio.imiter(video_path)):
        output_path = os.path.join(output_folder, f'frame{i+1:03d}.jpg')
        iio.imwrite(output_path, frame)

    print("\n[✓] Extraction complete.")
    