# filepath: setup.py
from setuptools import setup, find_packages

setup(
    name='hf-mirror-hub',
    version='0.0.1',
    description='A CLI tool to download Hugging Face models and datasets from mirror sites.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='neverbiasu',
    author_email='1751162157@qq.com',
    url='https://github.com/neverbiasu/hf-mirror-downloader',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'huggingface_hub',
        'hf-transfer',  # 如果要支持 hf-transfer
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'hf-mirror-hub = hf_mirror_hub.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)