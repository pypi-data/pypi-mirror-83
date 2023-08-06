import setuptools

setuptools.setup(
    name='django-context-extra-view',
    version='2020.10.26',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
