import setuptools

with open('README.rst') as file:

    readme = file.read()

name = 'survey'

version = '0.0.0'

author = 'Exahilosys'

url = f'https://github.com/{author}/{name}'

setuptools.setup(
    name = name,
    version = version,
    url = url,
    packages = setuptools.find_packages(),
    license = 'MIT',
    description = 'Building interactive prompts.',
    long_description = readme,
    install_requires = [
        'wrapio'
    ],
)
