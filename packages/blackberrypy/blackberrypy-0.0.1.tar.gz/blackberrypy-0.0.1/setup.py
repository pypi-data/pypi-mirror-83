import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blackberrypy",
    version="0.0.1",
    author="Spatial Innovations",
    author_email="spatialinnovations@gmail.com",
    description="Rubik's cube solver Python module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Spatial-Innovations/BlackberryPy",
    py_modules=["blackberrpy"],
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
) 
