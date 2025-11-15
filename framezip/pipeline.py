from .video import images_to_video
from .utils import compare_sizes
from .extraction import video_to_images
from .metrics import compare_psnr_ssim
from .plotter import plot_from_csv

def run_pipeline(input_folder, output_video, extracted_frames):
    heuristic_sort = False
    images_to_video(input_folder, output_video, framerate = "1", heuristic_sort=heuristic_sort)
    compare_sizes(input_folder, output_video)
    video_to_images(output_video, extracted_frames)
    
    if heuristic_sort:
        input_folder += "rd"
    compare_psnr_ssim(input_folder, extracted_frames)
    plot_from_csv("psnr_ssim_results.csv")