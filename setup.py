from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='framezip',
        version='0.1.0',
        description='Compress and decompress image sequences into videos with PSNR/SSIM evaluation – no ffmpeg required',
        author='Yellow Radiators',
        packages=find_packages(),
        install_requires=[
            'numpy', 'pillow', 'matplotlib', 'scikit-image', 'imageio', 'imageio-ffmpeg'
        ],
        python_requires='>=3.7'
    )
