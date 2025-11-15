import csv
import sys
from matplotlib import pyplot as plt

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
    
def plot_from_csv(csv_path: str = "psnr_ssim_results.csv"):
    """
    Reads a CSV produced by `compare_psnr_ssim` (columns: 'Frame','PSNR','SSIM')
    and plots the PSNR and SSIM series using `plot_psnr_ssim`.

    Args:
        csv_path (str): Path to the CSV file.
    
    Returns:
        tuple: (psnr_vals, ssim_vals) as lists of floats.
    """
    psnr_vals = []
    ssim_vals = []

    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = None
            s = None
            for k, v in row.items():
                if k is None:
                    continue
                key = k.strip().lower()
                if key == 'psnr':
                    p = v
                elif key == 'ssim':
                    s = v

            if p is None or s is None:
                vals = list(row.values())
                if len(vals) >= 3:
                    # order Frame, PSNR, SSIM
                    try:
                        p = p or vals[1]
                        s = s or vals[2]
                    except Exception:
                        pass

            try:
                psnr_vals.append(float(p))
            except (TypeError, ValueError):
                # skip rows that don't parse
                continue

            try:
                ssim_vals.append(float(s))
            except (TypeError, ValueError):
                ssim_vals.append(0.0)

    n = min(len(psnr_vals), len(ssim_vals))
    psnr_vals = psnr_vals[:n]
    ssim_vals = ssim_vals[:n]

    if not psnr_vals and not ssim_vals:
        raise ValueError(f"No PSNR/SSIM data found in {csv_path}")

    plot_psnr_ssim(psnr_vals, ssim_vals)
    return psnr_vals, ssim_vals

if __name__ == "__main__":
    csvfile = sys.argv[1] if len(sys.argv) > 1 else "psnr_ssim_results.csv"
    plot_from_csv(csvfile)