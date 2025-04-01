from framezip.video import images_to_video

def test_video_creation(tmp_path):
    input_folder = tmp_path / "images"
    input_folder.mkdir()
    
    from PIL import Image
    for i in range(3):
        img = Image.new("RGB", (320, 240), (i*50, i*50, i*50))
        img.save(input_folder / f"img{i+1}.jpg")

    output_video = tmp_path / "output.mp4"

    images_to_video(str(input_folder), str(output_video), framerate="1")

    assert output_video.exists(), "Output video file was not created."
    assert output_video.stat().st_size > 0, "Output video file is empty."
