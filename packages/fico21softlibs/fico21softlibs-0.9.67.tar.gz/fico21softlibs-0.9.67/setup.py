from setuptools import setup, find_packages
from sys import platform as _platform

if _platform == 'win32' or _platform == 'win64':
    # ========================================================================================================#
    # Windows only
    # ========================================================================================================#
    setup(
        name             = 'fico21softlibs',
        version          = '0.9.67',
        description      = 'This is a fico21soft\'s common libraries',
        long_description = open('README.md').read(),
        author           = 'Senna Kang',
        author_email     = 'fico21soft@gmail.com',
        url              = '',
        download_url     = '',
        install_requires = ['pyodbc', 'selenium', 'pynput', 'fcntl', 'win32api', 'win32con', 'pywinauto'],
        packages         = find_packages(exclude = ['docs', 'example']),
        keywords         = ['common', 'library', 'fico21soft'],
        python_requires  = '>=3',
        zip_safe=False,
        classifiers      = [
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8'
        ]
    )
else:
    setup(
        name             = 'fico21softlibs',
        version          = '0.9.67',
        description      = 'This is a fico21soft\'s common libraries',
        long_description = open('README.md').read(),
        author           = 'Senna Kang',
        author_email     = 'fico21soft@gmail.com',
        url              = '',
        download_url     = '',
        install_requires = ['pyodbc', 'selenium', 'pynput'],
        packages         = find_packages(exclude = ['docs', 'example']),
        keywords         = ['common', 'library', 'fico21soft'],
        python_requires  = '>=3',
        zip_safe=False,
        classifiers      = [
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8'
        ]
    )