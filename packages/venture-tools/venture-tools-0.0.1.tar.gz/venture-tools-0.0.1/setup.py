import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="venture-tools",
    version="0.0.1",
    author="murmuur",
    author_email="murmuur@protonmail.com",
    description="a CLI tool to initialize a new project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/murmuur-git/venture.git",
    download_url="https://github.com/murmuur-git/venture/archive/v0.0.1-alpha.3.tar.gz",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.24.0'
    ],
    package_data={
       'venture' : ['config.ini','templates/python/*', 'templates/python/libs/*'], # Includes python template
    },
    entry_points = {
        'console_scripts': [
            'venture = venture.__main__:main'
        ],
    })
