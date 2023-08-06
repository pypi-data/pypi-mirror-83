from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name="hmkshub-kmeans",
    version="0.1.2",
    description="A python package to K-means clustring",
    long_description_content_type="text/markdown",
    long_description=README,
    license="MIT",
    packages=find_packages(),
    author="Heramb Mishra",
    author_email="heramb1008@gmail.com",
    url="https://github.com/Herambdata/dl-package",
    include_package_data=True
)

install_requires=[
        "numpy>=1.18.5",
        "pandas>=1.0.5",
        "scikit-learn>=0.23.1",      
]

if __name__=='__main__':
    setup(**setup_args,install_requires=install_requires)