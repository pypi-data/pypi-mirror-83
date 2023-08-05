from setuptools import setup, find_packages

classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python :: 3',
          'Topic :: Communications :: Email',
          'Topic :: Office/Business',
          'Topic :: Software Development :: Bug Tracking',
          ]


setup(name='BeniBasicCalc',
      version='1.0',
      description='A very basic Calculator',
      Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
      author='MSBeni',
      author_email='andrei.sokurov.bitco@gmail.com',
      License='MIT',
      classifiers=classifiers,
      keywords='calculator',
      url='https://www.python.org/sigs/distutils-sig/',
      # packages=['distutils', 'distutils.command'],
      packages=find_packages(),
      install_requiers=['']
     )
