from setuptools import find_packages, setup

setup(
    name='tqirpa',
    packages=find_packages(),
    version='1.0.1',
    description='Pacote de Framework RPA da TQI',
    long_description='Pacote de Framework RPA da TQI',
    author='Leander Ribeiro',
    author_email='leander.ribeiro@tqi.com.br',
    url='https://github.com/usuario/meu-pacote-python',
    install_requires=['selenium'],
    license='MIT',
    keywords=['rpa'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ],
)
