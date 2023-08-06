from setuptools import setup, find_packages

with open('README.md') as f:
    long_description_from_readme = f.read()
    
setup(name='pimoscope',
      version='0.1',
      author='nko',
      author_email='nate@knilb.com',
      description='Test equipment for Knilb.',
      long_description=long_description_from_readme,
      long_description_content_type="text/markdown",
      url='http://knilb.com',
      packages=find_packages(exclude=["deprecated"]),
      classifiers=['License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.8'],
      install_requires=['knilb', 'bottle', 'automationhat', 'explorerhat'],
      entry_points={'console_scripts': ['pimo=pimoscope.__main__:main']},
      include_package_data=True,
      zip_safe=False,
      license='Apache')
