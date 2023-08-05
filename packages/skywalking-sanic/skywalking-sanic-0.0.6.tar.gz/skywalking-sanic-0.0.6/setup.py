import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    "sanic",
    "apache-skywalking==0.3.0",
    "requests"
]

setuptools.setup(
    name="skywalking-sanic",
    version="0.0.6",
    author="Parker Zhu",
    author_email="806000178@qq.com",
    description="Skywalking Sanic Support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/parkerzhu/skywalking-sanic",
    install_requires=install_requires,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)