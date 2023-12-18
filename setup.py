from setuptools import setup, find_packages

setup(
    name='file-sorter',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'PyQt5',           # Replace with your GUI library
        'watchdog',        # File system monitoring
        'peewee',          # Database ORM
        'customtkinter',   # Custom Tkinter library (replace with the actual name)
        'packaging',       # Package management
        'pywin32',         # Windows-specific library
        'ttkthemes'        # Themes for the GUI
    ],
    entry_points={
        'console_scripts': [
            'file-sorter-app = app.main:main',       # Command for running the GUI app
            'file-sorter-service = service.main:main' # Command for running the service
        ],
    },
    package_data={
        'app': ['assets/*', 'ui/*.ui'],
    },
    author='Callum White',
    author_email='callumwhi@live.co.uk',
    description='File Sorter Application',
    license='MIT',
)
