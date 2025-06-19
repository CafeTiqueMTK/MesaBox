from setuptools import setup, find_packages

setup(
    name="MesaBox",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "scapy"
    ],
    entry_points={
        "console_scripts": [
            "mesabox=mesabox_cli:main"
        ]
    },
    author="Team DSU",
    description="A modular network pentest toolkit.",
    license="MIT"
)
