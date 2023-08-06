import setuptools

__VERSION__ = "1.0.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yaml-include",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    version=__VERSION__,
    author="Mahe Thomas",
    author_email="thomas.mahe@nxp.com",
    description="Tool to generate yaml file with include",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    entry_points={
        'console_scripts': ['yaml-include=yamlinclude.main:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
