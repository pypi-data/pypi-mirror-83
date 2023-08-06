from setuptools import setup
setup(
      name='submission',
      version='0.0.1',
      description='Takes algorithm, train, test, X variables, Y variables, column names required for submission and name of submission file as input and produces an output csv for submitting in the competition.',
      py_modules=["submission"],
      package_dir={'':'package'},
      )