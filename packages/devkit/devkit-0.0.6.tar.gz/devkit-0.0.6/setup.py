import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="devkit", # Replace with your own username
    version="0.0.6",
    author="Sylvan LE DEUNFF",
    author_email="sledeunf@gmail.com",
    description="A tool to efficiently manage development environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/hoshiyosan/devtools/devkit/devkit-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['devkit=devkit.cli:main'],
    },
    python_requires='>=3.6',
    package_data = {
        'webui': ['*']
    },

    # Optional
    project_urls={
        'Documentation': 'https://hoshiyosan.gitlab.io/devtools/devkit/devkit-python',
        'Source': 'https://gitlab.com/hoshiyosan/devtools/devkit/devkit-python',
    },
)