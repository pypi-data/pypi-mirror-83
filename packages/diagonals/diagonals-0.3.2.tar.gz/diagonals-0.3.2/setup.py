from setuptools import setup, find_packages


PACKAGES = [
    'diagonals',
]

REQUIREMENTS = {
    # Installation script (this file) dependencies
    # Installation dependencies
    # Use with pip install . to install from source
    "setup": [
        'pytest-runner',
        'setuptools_scm',
    ],
    'install': [
        'netCDF4',
        'numba',
        'numpy',
        'six',
    ],
    'gpu': [
        'pycuda'
    ],
    'test': [
        'mock',
        'pycodestyle',
        'pytest',
        'pytest-cov',
        'pytest-html',
        'pytest-flake8',
        'pytest-metadata>=1.5.1',
    ]

}


setup(name='diagonals',
      version='0.3.2',
      description='Compute diagnostics targeting the CPU or the GPU',
      url='https://earth.bsc.es/gitlab/es/diagonals',
      author='BSC-CNS Earth Sciences Department',
      author_email='saskia.loosveldt@bsc.es',
      classifiers=[
          'Environment :: Console',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
      ],
      packages=find_packages(),
      setup_requires=REQUIREMENTS["setup"],
      install_requires=REQUIREMENTS["install"],
      tests_require=REQUIREMENTS["test"],
      extras_require={
          'gpu': REQUIREMENTS['gpu'],
      },
      zip_safe=False,)
