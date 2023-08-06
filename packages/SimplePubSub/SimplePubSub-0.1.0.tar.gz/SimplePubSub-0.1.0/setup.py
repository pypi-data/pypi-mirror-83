from setuptools import find_packages
from setuptools import setup

__version__ = "0.1.0"

setup(
    name="SimplePubSub",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=['redis', 'pytest'],
    author_email="jack@mizar.ai, cuici@mizar.ai, alex@mizar.ai, cino@mizar.ai",
)
