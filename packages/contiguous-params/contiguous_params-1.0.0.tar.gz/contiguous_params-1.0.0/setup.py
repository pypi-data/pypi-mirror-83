from setuptools import setup, find_packages

package_name = "contiguous_params"
version = '1.0.0'

requirements = [
    'torch>=1.5.1',
]

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name=package_name,
    version=version,
    author='Philipp Jund',
    author_email="ijund.phil@gmail.com",
    description='Make pytorch parameters contiguous to speed up training by 100x.',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='http://www.github.com/philjd/contiguous_pytorch_params',
    download_url='http://www.github.com/philjd/contiguous_pytorch_params/tags',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords=['pytorch', 'contiguous', 'parameters', 'speed up', 'accelerate'],
    packages=find_packages(exclude=('test',)),
    zip_safe=True,
    python_requires='>=3.6.0',
    include_package_data=True,
    install_requires=requirements,
    package_data={'': ['LICENSE']},
)
