from setuptools import setup

with open('pandas_extension_christine/README.md') as f:
    long_description = f.read()

setup(name='pandas-extension-christinedonszelmann',
      version='0.2.3',
      description='makes combinations of all columns of one dataframe, and more',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Christine Donszelmann',
      author_email='christine.donszelmann@nl.ey.com',
      license='MIT',
      packages=['pandas_extension_christine'],
      zip_safe=False)
