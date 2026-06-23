from setuptools import setup, find_packages

setup(
    name="renewable_energy_sim",
    version="1.0.0",
    description="Enterprise Power Systems and Renewable Energy Simulator",
    author="Engineering Team",
    packages=find_packages(),
    install_requires=[
        line.strip() for line in open("requirements.txt").readlines()
    ],
    python_requires=">=3.9",
)
