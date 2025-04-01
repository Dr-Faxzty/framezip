from framezip.video import images_to_video
from framezip.extraction import video_to_images
from framezip.metrics import compare_psnr_ssim
from framezip.utils import compare_sizes
from framezip.pipeline import run_pipeline

def full_pipeline():
    print("▶️ COMPLETE PIPELINE EXECUTION")
    print("---------------------------------------")
    run_pipeline(
        input_folder="frames",
        output_video="output.mp4",
        extracted_frames="decoded"
    )

def only_compress():
    print("📦 ONLY COMPRESSION (images → video)")
    print("---------------------------------------")
    images_to_video(
        input_folder="frames",
        output_file="output.mp4",
        framerate="1"
    )

def only_decompress():
    print("🔄 ONLY DECOMPRESSION (video → images)")
    print("---------------------------------------")
    video_to_images(
        video_path="output.mp4",
        output_folder="decoded",
    )
    
def only_compare_sizes():
    print("📦 COMPARE SIZES (video vs images)")
    print("---------------------------------------")
    compare_sizes(
        original_folder="frames",
        reconstructed_file="output.mp4",
    )

def only_metrics():
    print("📦 ONLY METRICS (images vs video)")
    print("---------------------------------------")
    compare_psnr_ssim(
        original_folder="frames",
        reconstructed_folder="decoded",
    )

if __name__ == "__main__":
    full_pipeline()
    #only_compress()
    #only_decompress()
    #only_compare_sizes()
    #only_metrics()
