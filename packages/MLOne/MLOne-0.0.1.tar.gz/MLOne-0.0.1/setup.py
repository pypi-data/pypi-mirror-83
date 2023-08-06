import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MLOne", # Replace with your own username
    version="0.0.1",
    author="Suhas and Dhamodaran",
    author_email="srisuhas2000@gmail.com",
    description="A user freindly module with which users can just drop their dataset and download the best ML model for their dataset",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Dhamodaran-Babu/ML-Thunai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    install_requires=[
       "python"
       "pandas",
       "numpy",
       "matplotlib",
       "imblearn",
       "sklearn",
       "mlxtend",
       "seaborn",
       "joblib"
    ]
   
)