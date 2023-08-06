import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-wechatwork-tool",  # Replace with your own username
    version="0.0.3",
    author="iceiceice",
    author_email="597952291@qq.com",
    description="Wechatworktool is a Django app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zxj17815/wechatwork-tool",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
