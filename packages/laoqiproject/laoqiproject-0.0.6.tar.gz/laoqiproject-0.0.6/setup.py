import setuptools
import os
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__),os.pardir)))

with open("README.md","r") as f:
    long_description = f.read()

setuptools.setup(
    name = 'laoqiproject',
    version = '0.0.6',
    author = 'qiwsir',
    author_email = 'qiwsir@qq.com',
    description = 'this is my first project.',
    long_description = long_description,
    long_description_content_type = 'text/markdown'  ,
    url = "",
    py_modules = ['langspeak'],
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.6',
)