from setuptools import find_packages
from setuptools import setup

with open("requirements_prod.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='fit_tes_courses',
      version="0.0.12",
      description="Fit tes courses (api_pred)",
      license="MIT",
      author="Le Wagon",
      install_requires=requirements,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
