from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name="num_thai_cnv",  # Replace with your own username
    version="1.0.0",
    author="Natthakhon Laosurasuntorn",
    author_email="nattlao@gmail.com",
    description="Thai localization package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    keywords=['num', 'thai'],
    License='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
