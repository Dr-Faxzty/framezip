from PIL import Image
from framezip.metrics import compare_psnr_ssim

def test_compare_psnr_ssim(tmp_path):
    orig_dir = tmp_path / "originals"
    recon_dir = tmp_path / "reconstructed"
    orig_dir.mkdir()
    recon_dir.mkdir()

    for i in range(5):
        orig = Image.new("RGB", (320, 240), (i * 40, i * 40, i * 40))
        recon = Image.new("RGB", (320, 240), (i * 40 + 5, i * 40 + 5, i * 40 + 5))
        orig.save(orig_dir / f"img{i+1}.jpg")
        recon.save(recon_dir / f"frame{i+1:03d}.jpg")
        
    csv_file = tmp_path / "quality.csv"
    psnr_vals, ssim_vals = compare_psnr_ssim(str(orig_dir), str(recon_dir), csv_output=str(csv_file))

    assert len(psnr_vals) == 5, f"Expected 5 PSNR values, got {len(psnr_vals)}"
    assert len(ssim_vals) == 5, f"Expected 5 SSIM values, got {len(ssim_vals)}"
    assert all(p > 20 for p in psnr_vals), f"PSNR values should be greater than 20, got {psnr_vals}"
    assert all(0 <= s <= 1 for s in ssim_vals), f"SSIM values should be between 0 and 1, got {ssim_vals}"