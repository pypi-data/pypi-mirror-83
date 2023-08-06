from setuptools import setup, find_packages

setup(
    name='swcpm',
    version='0.1.1',
    packages=find_packages(),
    license='MIT',
    description='Manage Software City Packages',
    download_url='https://github.com/Software-City/SWC_packagemanager/archive/v0.1.1.tar.gz',
    url='https://github.com/Software-City/SWC_packagemanager',
    long_description="README.md",
    long_description_content_type="text/markdown",
    author="Davis_Software",
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'tqdm'
    ],
    entry_points={
        "console_scripts": [
            "swcpm=swcpm.main:swc_pm"
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
