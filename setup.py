from setuptools import setup

setup(name='blis',
      version='0.1',
      description='BLIS - Balancing Load of Intermittent Solar: A characteristic-based transient power plant model',
      url='https://github.com/EnergyModels/blis',
      author='Jeff Bennett',
      author_email='jab6ft@virginia.edu',
      license = 'MIT',
      packages=['blis'],
      zip_safe=False,
      install_requires=['pandas', 'numpy', 'matplotlib', 'seaborn','joblib'])