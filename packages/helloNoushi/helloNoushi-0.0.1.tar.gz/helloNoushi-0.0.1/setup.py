from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

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


setup(name='helloNoushi',
      version='0.0.1',
      description='say hello',
      py_modules=["helloNoushi"],
      # package_dir={'': 'src'},
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='MSBeni',
      author_email='andrei.sokurov.bitco@gmail.com',
      # License='MIT',
      classifiers=classifiers,
      keywords='calculator',
      url='https://github.com/MSBeni/LearnPythonPackage',
      packages=find_packages(),
      # install_requiers=[''],
      extras_require={
          "dev": [
              "pytest>=3.7",
          ],
      }
     )

