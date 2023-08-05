import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    "flask",
    "apache-skywalking==0.3.0",
    "requests",
]

setuptools.setup(
    name="skywalking-flask",
    version="0.0.7",
    author="Parker Zhu",
    author_email="806000178@qq.com",
    description="Skywalking Flask Support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/parkerzhu/skywalking-flask",
    install_requires=install_requires,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)