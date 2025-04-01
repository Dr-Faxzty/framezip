from framezip.extraction import extract_frames
from framezip.video import images_to_video

def test_extract_then_compare(tmp_path):
    img_folder = tmp_path / "imgs"
    img_folder.mkdir()
    from PIL import Image
    for i in range(5):
        Image.new("RGB", (320, 240), (255, 255, 255)).save(img_folder / f"img{i}.jpg")

    video_path = tmp_path / "test.mp4"
    images_to_video(str(img_folder), str(video_path))

    output_folder = tmp_path / "frames"
    extract_frames(str(video_path), str(output_folder))

    extracted = list(output_folder.glob("*.jpg"))
    assert len(extracted) == 5, "Frame extraction count mismatch"
