"""The setup script"""

from setuptools import setup, find_packages

AUTHOR = 'Viktoria R.'
EMAIL = 'viktoria.rosjo@gmail.com'
VERSION = '1.0.1'

setup_args = dict(
    name='fdet_offline_mobilenet_weights',
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    url='https://github.com/vikrosj/fdet_offline_mobilenet_weights',
    download_url='https://github.com/vikrosj/fdet_offline_mobilenet_weights/archive/1.0.1.tar.gz',
    include_package_data=True,
    description='Weights for the models in fdet-offline.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important!
    keywords='face recognition detection biometry',
    packages=find_packages(),
    zip_safe=False,
    python_requires='>=3.5'
)

install_requires=[
                        'future==0.18.2',
                        'numpy==1.19.2',
                        'torch==1.6.0'
                    ]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)