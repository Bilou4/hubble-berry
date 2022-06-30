from setuptools import setup

setup(
    name="hubble-berry-tools",
    version="0.1",
    py_modules=["main"],
    install_requires=["Click", "opencv-python", "paramiko", "scp", "tqdm", "py-flags"],
    entry_points={"console_scripts": ["hubble-berry=main:cli"]},
)
