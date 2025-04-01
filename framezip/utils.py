import os

def get_folder_size_mb(folder, exts):
    """
    Calculate the size of all files in a folder with specific extensions.
    
    Args:
        folder (str): Path to the folder.
        exts (tuple): Tuple of file extensions to include in the size calculation.
    """
    total = sum(
        os.path.getsize(os.path.join(folder, f))
        for f in os.listdir(folder) if f.lower().endswith(exts)
    )
    return total / (1024 * 1024)


def compare_sizes(original_folder, video_path):
    """
    compare the size of images in a folder with the size of a video file.
    
    Args:
        original_folder (str): Path to the folder containing images.
        video_path (str): Path to the video file.
    """
    img_mb = get_folder_size_mb(original_folder, ('.jpg', '.jpeg', '.png'))
    vid_mb = os.path.getsize(video_path) / (1024 * 1024) if os.path.exists(video_path) else 0
    
    print(f"\n📦 Images size: {img_mb:.2f} MB")
    print(f"🎞️  Video size:   {vid_mb:.2f} MB")

    if vid_mb < img_mb:
        print("\n✅ Video is lighter than images")
    elif vid_mb > img_mb:
        print("\n⚠️ Video is heavier than images")
    else:
        print("\n🤝 Sizes are the same")