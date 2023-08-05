import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="customtimsort",
    version="0.0.40",
    author="lehatr",
    author_email="lehatrutenb@gmail.com",
    description="Timsort sorting algorithm with custom minrun",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lehatrutenb/FastTimSort",
    #packages=setuptools.find_packages(),
    packages=['sortt'],
    package_dir={'sortt': 'customtimsort/sortt'},
    package_data={'sortt': ['fold/*', 'fold/clinic/*', 'fold/cpython/*']},
    #ext_modules = [setuptools.Extension('tsort', ['/home/leha/Desktop/projects/library/FastTimSort/customtimsort/fold/listobject.c'], include_dirs=['fold'], library_dirs = ['fold'])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
