from setuptools import setup

setup(name='fdb_data',
      version='1.0.0',
      description='FDB database module',
      long_description='Work to the FDB database. This is easy database. It save file in xml format.\nFDB-data use bs4 and lxml. It work in win32, linux and other.',
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
          'lxml',
          'robin_pl',
          'evalnumstr',
          'easy_shortcut'
      ],
      include_package_data=True,
      zip_safe=False)
