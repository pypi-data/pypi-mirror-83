import setuptools

setuptools.setup(
    name="py_rap",
    version="0.0.0",
    author="Brian C. Ferrari",
    author_email="brian.ferrari@ucf.edu",
    description="This is a Python package for residue analysis.",
    url="https://github.com/Cavenfish/py_rap",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "scipy", "pandas", "openpyxl", "matplotlib",
                      "xlrd", "xlsxwriter", "sklearn", "collections", "seaborn"
                      "glob"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
)
