from setuptools import setup

version = '0.0.1.0';
setup(
    name='tidy3dclient',
    version=version,
    description='A Python API for TIDY3d FDTD Solver',
    author='FlexCompute, Inc.',
    author_email='lei@flexcompute.com',
    packages=['tidy3d'],
    install_requires=['requests>=2.13.0', 'aws-requests-auth', 'bcrypt', 'boto3', 'matplotlib>=3.0.3'
        , 'numpy>=1.16.2', 'scipy>=1.2.1'],
    dependency_links=['http://github.com/flexcompute/warrant/tarball/master#egg=warrant-0.6.4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)
