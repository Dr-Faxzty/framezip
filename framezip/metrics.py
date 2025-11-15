import os
import numpy as np
from PIL import Image
import imageio.v3 as iio
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim_lib
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress
from .utils import get_images, write_psnr_ssim_csv
import csv

def psnr(img1, img2):
    """
    Calculates the Peak Signal-to-Noise Ratio (PSNR) between two images.
    
    Args: 
        img1 (numpy.ndarray): First image.
        img2 (numpy.ndarray): Second image.
    """
    mse = np.mean((np.array(img1, dtype=np.float32) - np.array(img2, dtype=np.float32)) ** 2)
    if mse == 0:
        return float('inf')
    PIXEL_MAX = 255.0
    return 20 * np.log10(PIXEL_MAX / np.sqrt(mse))

def process_frame(orig, rec):
    """Helper function to process a single frame pair."""
    img1 = Image.open(orig).convert("RGB")
    img2 = Image.open(rec).convert("RGB")
    
    img2 = img2.crop((0, 0, img1.width, img1.height))
    iio.imwrite(rec, img2)
    
    arr1, arr2 = np.array(img1), np.array(img2)
    
    psnr_val = psnr(arr1, arr2)
    ssim_val = ssim_lib(arr1, arr2, channel_axis=2)
    
    return psnr_val, ssim_val

def compare_psnr_ssim(original_folder, reconstructed_folder, csv_output = "psnr_ssim_results.csv"):
    """
    Compares the PSNR and SSIM metrics between original and reconstructed images.
    
    Args:
        original_folder (str): Path to the folder containing original images.
        reconstructed_folder (str): Path to the folder containing reconstructed images.
        csv_output (str): Path to save the CSV output file.
        
    Returns:
        psnr_vals (list): List of PSNR values.
        ssim_vals (list): List of SSIM values.
    """
    originals = [os.path.join(original_folder, f) for f in get_images(original_folder)]
    recon = [os.path.join(reconstructed_folder, f) for f in get_images(reconstructed_folder)]

    psnr_vals = []
    ssim_vals = []
    results = [None] * len(originals)
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Calculating PSNR and SSIM...", total=len(originals))
        
        with ThreadPoolExecutor() as executor:
            future_to_index = {
                executor.submit(process_frame, orig, rec): i 
                for i, (orig, rec) in enumerate(zip(originals, recon))
            }
            
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                results[index] = future.result()
                progress.update(task, advance=1)
    
    psnr_vals = [r[0] for r in results]
    ssim_vals = [r[1] for r in results]
        
    avg_psnr = sum(psnr_vals) / len(psnr_vals) if psnr_vals else 0
    avg_ssim = sum(ssim_vals) / len(ssim_vals) if ssim_vals else 0
    
    print(f"\n📊 avg PSNR: {avg_psnr:.2f} dB")
    print(f"📊 avg SSIM: {avg_ssim:.4f}")
    
    if avg_psnr >= 40:
        print("\n🟢 High quality")
    elif avg_psnr >= 30:
        print("\n🟡 Good quality")
    else:
        print("\n🔴 Low quality")
        
    write_psnr_ssim_csv(csv_output, psnr_vals, ssim_vals)
    
    return psnr_vals, ssim_vals