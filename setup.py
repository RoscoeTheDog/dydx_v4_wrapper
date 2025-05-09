from setuptools import setup, find_packages

setup(
    name='dydx_v4_wrapper',
    version='0.1.0',
    description='A simple Python wrapper for a DeFi exchange',
    author='RoscoeTheDog',
    author_email='null',
    packages=find_packages(),  # Automatically finds your_wrapper/
    install_requires=['dydx-v4-client'],       # Add dependencies here, if any
    python_requires='>=3.9',   # Or whatever you support
)
