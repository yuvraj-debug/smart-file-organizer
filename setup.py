from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smart-file-organizer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A command-line tool that automatically organizes files in a directory based on their type, date, or custom rules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuvraj-debug/smart-file-organizer",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "sfo=smart_file_organizer.cli:main",
        ],
    },
)