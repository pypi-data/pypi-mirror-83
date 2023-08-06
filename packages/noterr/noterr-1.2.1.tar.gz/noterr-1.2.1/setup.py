from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'noterr',
    version = '1.2.1',
    packages = ['noterr'],
    license='MIT',        
    description = 'A package to keep track of your note inside the terminal',  
    author = 'Japroz Singh Saini',     
    long_description = long_description,  
    long_description_content_type="text/markdown",            
    author_email = 'sainijaproz@gmail.com',     
    url = 'https://github.com/Japroz-Saini/',  
    download_url = 'https://github.com/Japroz-Saini/noterr/archive/v1.1.0.tar.gz',
    keywords = ['noterr', 'japroz singh saini', 'python', 'pip'],
    entry_points = {
        'console_scripts': [
            'noterr = noterr.__main__:main'
        ]
    },
    install_requires=[
          'cs50',
          'colored',
    ])