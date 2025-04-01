from pathlib import Path
from PIL import Image
from framezip.pipeline import run_pipeline

def test_full_pipeline(tmp_path):
    input_folder = tmp_path / "input_images"
    input_folder.mkdir()

    for i in range(4):
        img = Image.new("RGB", (320, 240), (i * 30, i * 30, i * 30))
        img.save(input_folder / f"img{i+1}.jpg")

    output_video = tmp_path / "output.mp4"
    extracted_folder = tmp_path / "extracted_frames"

    run_pipeline(str(input_folder), str(output_video), str(extracted_folder))

    assert output_video.exists(), "Video file not created"
    assert output_video.stat().st_size > 0, "Video file is empty"

    extracted = list(extracted_folder.glob("*.jpg"))
    assert len(extracted) == 4, "extracted frames count mismatch"

    csv_file = Path("psnr_ssim_results.csv")
    assert csv_file.exists(), "CSV file with PSNR/SSIM results not created"

    csv_file.unlink()