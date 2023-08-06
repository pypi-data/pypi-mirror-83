from setuptools import setup, find_packages

setup(name='lipidhandler',
      version='0.0.2',
      description='Handle lipid names in Python.',
      long_description_content_type='text/markdown',
      url='https://github.com/kaiserpreusse/lipidhandler',
      author='Martin Preusse',
      author_email='martin.preusse@gmail.com',
      license='MIT',
      packages=find_packages(),
      keywords=['LIPIDS', 'LIPIDOMICS'],
      zip_safe=False,
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License'
      ],
      )
