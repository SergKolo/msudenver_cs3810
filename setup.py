from setuptools import setup

setup(
    name='metadb',
    version='0.1',
    license='MIT',
    description='Metadata database for files on GNOME-based desktops',
    author='Sergiy Kolodyazhnyy',
    author_email='1047481448@qq.com',
    url='https://github.com/SergKolo/msudenver_cs3810',
    packages=['metadb'],
    install_requires=['audioread','PIL']
    classifiers=[
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.0',
        'Topic :: Utilities'
    ]
)

