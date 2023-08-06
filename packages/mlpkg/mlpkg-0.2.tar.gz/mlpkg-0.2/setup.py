
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name="mlpkg",
    version="0.2",
    description="ML package",
    long_description_content_type="text/markdown",
    long_description=README,
    license="MIT",    packages=find_packages(),
    author="Sakshi Agarwal",
    author_email="sakshi.agg23@gmail.com",
    url="https://https://github.com/Sakshi-agarwal8/DeepLeaning",
    include_package_data=True
)

install_requires=[
        "numpy>=1.18.5",
        "pandas>=1.0.5",
        "scikit-learn>=0.23.1",      
]

if __name__=='__main__':
    setup(**setup_args,install_requires=install_requires)