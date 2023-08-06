import setuptools


setuptools.setup(
    name="torch-transformers",
    version="1.0.4",
    author="Tony Nguyen",
    author_email="tonyn0603@gmail.com",
    description="An implementation of Transformers using PyTorch",
    url="https://github.com/UltraSpecialException/torch-transformers",
    packages=["torch_transformers", "torch_transformers.utils"],
    package_dir={
        "torch_transformers": "modules",
        "torch_transformers.utils": "modules/utils"
    },
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.6"
)
