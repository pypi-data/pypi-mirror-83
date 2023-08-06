from setuptools import setup
setup(
    name = 'noterr',
    version = '1.0.0',
    packages = ['noterr'],
    license='MIT',        
    description = 'A package to keep track of your note inside the terminal',  
    author = 'Japroz Singh Saini',                   
    author_email = 'sainijaproz@gmail.com',     
    url = 'https://github.com/Japroz-Saini/',  
    download_url = 'https://github.com/Japroz-Saini/noterr/archive/v_01.tar.gz',
    keywords = ['note','noterr', 'terminal', 'tnote', 'note-taking', 'japroz', 'japroz-saini'],
    entry_points = {
        'console_scripts': [
            'noterr = noterr.__main__:main'
        ]
    },
    install_requires=[
          'cs50',
          'colored',
    ])