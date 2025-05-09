from setuptools import setup, find_packages

setup(
    name='your-wrapper',
    version='0.1.0',
    description='A simple Python wrapper for a DeFi exchange',
    author='Your Name',
    author_email='you@example.com',
    packages=find_packages(),  # Automatically finds your_wrapper/
    install_requires=[],       # Add dependencies here, if any
    python_requires='>=3.9',   # Or whatever you support
)
