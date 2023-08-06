import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="aop-on-robot",
  version="0.0.2",
  author="Software System Laboratory",
  author_email="ntutsoftsyslab@gmail.com",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://ssl-gitlab.csie.ntut.edu.tw/e8315402/aop-on-robot",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3.6",
    "Framework :: Robot Framework",
    "Topic :: Software Development :: Testing :: Acceptance",
  ],
  python_requires='>=3.6',
)