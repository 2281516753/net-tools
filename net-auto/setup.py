from setuptools import setup, find_packages

setup(
    name="net-auto",
    version="1.0.0",
    description="Network Automation Toolkit — config backup, ping monitor, subnet calculator, port scanner",
    author="Wang Jiong",
    author_email="2281516753@qq.com",
    url="https://github.com/2281516753/net-auto",
    py_modules=["cli", "backup", "pingmon", "subnet", "scanner"],
    install_requires=[
        "paramiko>=3.0",
        "colorama>=0.4",
    ],
    entry_points={
        "console_scripts": [
            "net-auto=cli:main",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: System :: Networking",
    ],
)
