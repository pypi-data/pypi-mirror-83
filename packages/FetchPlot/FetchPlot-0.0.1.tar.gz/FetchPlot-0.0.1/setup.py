import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FetchPlot",
    version="0.0.1",
    author="Jyothi Kiran Reddy",
    author_email="r.jyothikiranreddy@gmail.com",
    description="A simple wrapper around gspread to Fetch Data From Google sheets and plot a chart",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    url="https://github.com/kiranreddy007/Greendeck-FetchPlot",
    packages=setuptools.find_packages(),
    zip_safe=False,
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",

        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)
