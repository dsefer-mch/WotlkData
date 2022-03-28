import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wotlk_db_BY_MCH",
    version="0.0.1",
    author="MCH",
    author_email="mch.dv.uk@gmail.com",
    description="wotlk_db_proj",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dsefer-mch/WotlkData.git",
    project_urls={
        "Bug Tracker": "https://github.com/dsefer-mch/WotlkData.git",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(),
    install_requires=['selenium', 'pandas', 're', 'base64', 'uuid', 'os', 'requests',
                      'io', 'pillow', 'boto3', 'datetime', 'urllib', 'webdriver_manager', 'psycopg2'],
)
