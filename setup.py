import setuptools


def readme():
    with open("README.md", "r") as f:
        return f.read()


setuptools.setup(
    name="temipy",
    version="1.0.0",
    description="MQTT bridge for temi",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="R. Oung",
    author_email="r.oung@hapi-robo.com",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    install_requires=["paho-mqtt",],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Ubuntu, macOS",
    ],
    python_requires=">=3.6",
)
