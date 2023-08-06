import setuptools

long = '''A simple command-line clock.
Usage:
python -m cmd_clock
Output:
Thu Oct 22 20:36:35 2020
Install:
pip install cmd_clock
Note: In some systems (and in IDLE) you'll see Thu Oct 22 20:33:11 2020 over and over. Try another shell instead.
'''
setuptools.setup(
    name="cmd_clock", # Replace with your own username
    version="0.3",
    author="Allen Sun",
    author_email="allen.haha@hotmail.com",
    description="a command-line clock",
    long_description=long,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
