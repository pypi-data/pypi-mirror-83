from setuptools import setup, find_packages
import pathlib
Here = pathlib.Path(__file__).parent
readme = (Here / "README.md").read_text()
setup(
    name='lsHotword',
    version='1.0.2',
    description="An Deep Learning Based Hotword Detectors For Python Programmers",
    long_description=readme,
    long_description_content_type="text/markdown",
    #package_dir={"": "lsHotword"},
    packages=find_packages(include=['lsHotword', 'HTrainer.*','hotword.*']),
    install_requires=[
        'keras',
        'numpy',
        'matplotlib',
        'pydub',
        'scikit-learn',
        'scipy'
    ],
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.wav','backgrounds/*.wav','LICENSE','*.md']
    },
    keywords = "hotword detectors for windows 10,linux and mac using deep learning",
    python_requires='>=3.6'

)