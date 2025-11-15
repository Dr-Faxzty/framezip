import os
import numpy as np
from PIL import Image
import imageio.v3 as iio
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim_lib
from rich.progress import Progress
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

def plot_psnr_ssim(psnr_vals, ssim_vals):
    """
    Plots the PSNR and SSIM values.
    
    Args:
        psnr_vals (list): List of PSNR values.
        ssim_vals (list): List of SSIM values.
    """
    plt.figure(figsize=(12, 6))

    # Plot PSNR
    plt.subplot(1, 2, 1)
    plt.plot(psnr_vals, marker='o', linestyle='-', color='blue', label='PSNR')
    plt.axhline(y=40, color='green', linestyle='--', label='Soglia qualità ottima')
    plt.axhline(y=30, color='orange', linestyle='--', label='Soglia qualità buona')
    plt.axhline(y=20, color='red', linestyle='--', label='Soglia qualità bassa')
    plt.title('PSNR per frame')
    plt.xlabel('Frame')
    plt.ylabel('PSNR (dB)')
    plt.legend()
    plt.grid(True)

    # Plot SSIM
    plt.subplot(1, 2, 2)
    plt.plot(ssim_vals, marker='s', color='purple', label='SSIM')
    plt.axhline(y=0.95, color='green', linestyle='--', label='Ottimo')
    plt.axhline(y=0.90, color='orange', linestyle='--', label='Accettabile')
    plt.title('SSIM per frame')
    plt.xlabel('Frame')
    plt.ylabel('SSIM')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

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
    originals = sorted([f for f in os.listdir(original_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    recon = sorted([f for f in os.listdir(reconstructed_folder) if f.lower().endswith('.jpg')])

    psnr_vals = []
    ssim_vals = []
    with Progress() as progress:
        task = progress.add_task("[cyan]Calculating PSNR and SSIM...", total=len(originals))
        for orig, rec in zip(originals, recon):
            img1 = Image.open(os.path.join(original_folder, orig)).convert("RGB")
            img2 = Image.open(os.path.join(reconstructed_folder, rec)).convert("RGB")
            
            img2 = img2.crop((0, 0, img1.width, img1.height))
            iio.imwrite(os.path.join(reconstructed_folder, rec), img2)

            arr1, arr2 = np.array(img1), np.array(img2)
            
            psnr_vals.append(psnr(arr1, arr2))
            ssim_vals.append(ssim_lib(arr1, arr2, channel_axis=2))
            progress.update(task, advance=1)
        
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
        
    with open(csv_output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Frame', 'PSNR', 'SSIM'])
        for i, (p, s) in enumerate(zip(psnr_vals, ssim_vals), start=1):
            writer.writerow([i, round(p, 4), round(s, 4)])

    print("\n📝 CSV exported: psnr_ssim_results.csv")  
    
    plot_psnr_ssim(psnr_vals, ssim_vals)

    return psnr_vals, ssim_vals