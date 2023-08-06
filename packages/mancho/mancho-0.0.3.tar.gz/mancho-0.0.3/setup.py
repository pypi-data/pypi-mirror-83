import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mancho",
    version="0.0.3",
    author="Ali Rasim Kocal",
    author_email="arkocal@posteo.net",
    description="A musical transcription tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.arkocal.rocks/arkocal/transcriber",
    packages=["mancho"],
    package_data={"mancho": ["main.glade"]},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    keywords="music musical transcription tool",
    python_requires='>=3.6',
    install_requires=["audiofile", "soundfile", "numpy", "pyrubberband",
                      "pyaudio", "matplotlib"]
)
