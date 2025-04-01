from .video import images_to_video
from .utils import compare_sizes
from .extraction import extract_frames
from .metrics import compare_psnr_ssim

def run_pipeline(input_folder, output_video, extracted_frames):
    images_to_video(input_folder, output_video, framerate = "1")
    compare_sizes(input_folder, output_video)
    extract_frames(output_video, extracted_frames)
    compare_psnr_ssim(input_folder, extracted_frames)