import setuptools


def readme():
    with open("README.md", "r") as f:
        return f.read()

def requirements():
    with open("requirements.txt", "r") as f:
        return f.read().splitlines()

setuptools.setup(
    name="pytemi",
    version="1.0.0",
    description="A Python client that can be used with Connect MQTT bridge for temi.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="R. Oung",
    author_email="r.oung@hapi-robo.com",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    install_requires=requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Ubuntu, macOS",
    ],
    python_requires=">=3.6",
)
