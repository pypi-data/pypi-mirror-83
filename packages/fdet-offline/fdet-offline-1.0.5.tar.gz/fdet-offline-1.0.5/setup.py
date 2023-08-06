"""The setup script"""

from setuptools import setup, find_packages

AUTHOR = 'Viktoria R.'
EMAIL = 'viktoria.rosjo@gmail.com'
VERSION = '1.0.5'
 
setup(
    name='fdet-offline',
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    url='https://github.com/vikrosj/fdet-offline',
    download_url='https://github.com/vikrosj/fdet-offline/archive/1.0.5.tar.gz',
    description='An easy to use face detection module based on MTCNN and RetinaFace algorithms.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important!
    keywords='face recognition detection biometry',
    packages=find_packages(),
    zip_safe=False,
    python_requires='>=3.8',
    install_requires=[
                    'appdirs==1.4.3',
                    'attrs==20.2.0',
                    'CacheControl==0.12.6',
                    'certifi==2019.11.28',
                    'chardet==3.0.4',
                    'click==7.1.2',
                    'colorama==0.4.4',
                    'colour==0.1.5',
                    'contextlib2==0.6.0',
                    'distlib==0.3.0',
                    'distro==1.4.0',
                    'fdet-offline-mtcnn-weights==1.0.0',
                    'future==0.18.2',
                    'html5lib==1.0.1',
                    'idna==2.8',
                    'iniconfig==1.1.1',
                    'ipaddr==2.2.0',
                    'lockfile==0.12.2',
                    'msgpack==0.6.2',
                    'numpy==1.19.2',
                    'opencv-python==4.4.0.44',
                    'packaging==20.3',
                    'pep517==0.8.2',
                    'Pillow==8.0.0',
                    'pluggy==0.13.1',
                    'progress==1.5',
                    'py==1.9.0',
                    'pyparsing==2.4.6',
                    'pytest==6.1.1',
                    'pytoml==0.1.21',
                    'requests==2.22.0',
                    'retrying==1.3.3',
                    'six==1.14.0',
                    'toml==0.10.1',
                    'torch==1.6.0+cpu',
                    'torchvision==0.7.0+cpu',
                    'ttictoc==0.5.6',
                    'urllib3==1.25.8',
                    'webencodings==0.5.1'

                    ],
    entry_points={
        'console_scripts': ['fdet=fdet.cli.main:main']
    }
)
