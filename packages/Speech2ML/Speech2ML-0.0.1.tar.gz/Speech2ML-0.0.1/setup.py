import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Speech2ML", 
    version="0.0.1",
    author="Tony Dong",
    author_email="tonyleidong@gmail.com",
    description="Library name occupy. Auto-generate Machine Learning script by Speech.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tonyleidong/Speech2ML",
    keywords = ['AutoML'],
    packages=setuptools.find_packages(),
    include_package_data = True,
    install_requires=[
        'speech_recognition',
        'jellyfish'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',

)

