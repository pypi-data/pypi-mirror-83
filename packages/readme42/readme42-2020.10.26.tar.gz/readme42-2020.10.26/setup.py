import setuptools

setuptools.setup(
    name='readme42',
    version='2020.10.26',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['scripts/readme42']
)
