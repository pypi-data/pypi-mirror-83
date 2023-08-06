import setuptools

setuptools.setup(
    name='django-http-last-modified-view',
    version='2020.10.29',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
