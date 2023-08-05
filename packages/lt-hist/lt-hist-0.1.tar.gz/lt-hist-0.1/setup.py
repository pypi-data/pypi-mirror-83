import setuptools

with open('requirements.txt', 'r') as requirements_file:
  requirements_text = requirements_file.read()

requirements = requirements_text.split()

setuptools.setup(
      name='lt-hist',
      include_package_data=True,
      version='0.1',
      description='Compares the last results of Load Test',
      url='https://github.com/ifood/lt-hist',
      author='Felipe Volpone    ',
      author_email='felipe.volpone@ifood.com.br',
      license='none',
      packages=setuptools.find_packages(),
      zip_safe=False,
      install_requires=requirements,
      entry_points='''
      [console_scripts]
      lt_hist=lt_hist.entrypoint:compare
      ''',
)