from setuptools import setup

setup(name='fdb_data',
      version='0.2.0',
      description='FDB database module',
      long_description='Work to the FDB database.',
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
      ],
      keywords='database foton fotonpc fdb data big',
      url='http://ppbe.ru',
      author='FotonPC',
      author_email='foton-pc@inbox.ru',
      license='MIT',
      packages=['fdb_data'],
      install_requires=[
          'bs4',
          'lxml'
      ],
      include_package_data=True,
      zip_safe=False)
