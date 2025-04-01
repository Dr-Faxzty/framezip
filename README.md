# 📦 framezip

**framezip** is a lightweight and pure-Python toolkit to compress image sequences into a video and decompress them later, with quality evaluation using PSNR and SSIM metrics. All this without external dependencies like FFmpeg.

---

## 💡 Idea
One day, we asked ourselves a simple yet intriguing question:
> _"Is a video made of N frames heavier than N individual images? Or the opposite?"_

That curiosity kicked off a spontaneous experiment — and **framezip** was born.

We built this toolkit to answer that question and explore:
- How much compression we get from turning images into videos
- How much quality we lose in the process (if any)
- How to automate the whole test: compress → decompress → evaluate

Whether you're a curious dev, researcher, or compression nerd, **framezip** is here to help you explore this kind of visual comparison easily.

---

## ⚙️ How it works

1. Renames images using the pattern `frame001.jpg`, `frame002.jpg`, etc.
2. Compresses them into a `.mp4` video using `imageio`
3. Extracts frames back from the video
4. Compares original and reconstructed frames using:
   - **PSNR** (Peak Signal-to-Noise Ratio)
   - **SSIM** (Structural Similarity Index)
5. Outputs graphs and a CSV report with quality metrics

---

## 📦 Installation

### ✅ Requirements
- Python 3.7+

### 🧪 Local development install
```bash
pip install -e .
```

### 🌐 (coming soon) from PyPI
```bash
pip install framezip
```

---

## 🚀 Basic usage (Python)

```python
from framezip.pipeline import run_pipeline

run_pipeline(
    input_folder="frames/",
    output_video="video.mp4",
    extracted_frames="extracted/"
)
```

---

## 🧩 Use individual modules

```python
from framezip.video import images_to_video
from framezip.extraction import extract_frames
from framezip.metrics import compare_psnr_ssim

images_to_video("frames/", "video.mp4")

extract_frames("video.mp4", "extracted/")

compare_psnr_ssim("frames/", "extracted/", csv_output="metrics.csv")
```

---

## 🔭 Next steps
- [ ] Support for `.webm`, `.gif`, `.avi`
- [ ] Lossless mode with pixel-wise difference export
- [ ] Support input video files for analysis

---

## 🤝 Contribute

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push: `git push origin feature/your-feature`
5. Open a pull request ✨

To run tests:
```bash
pytest tests/
```

---

## ❤️ Support the project
If you like this project, give it a ⭐ on GitHub or share it with other devs/video nerds 👾
