from os import path
import setuptools

with open(path.join(path.dirname(__file__), "README.md"), "r") as fh:
    long_description = fh.read()

with open(path.join(path.dirname(__file__), "requirements.txt"), "r") as fh:
    install_requires = [line.strip() for line in fh.readlines()]

setuptools.setup(
    name="grui",
    version="0.0.6",
    author="SECRET Olivier",
    author_email="pypi-package-grui@devo.live",
    description="An ready to use exposer from services oriented code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/olive007/grui",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
