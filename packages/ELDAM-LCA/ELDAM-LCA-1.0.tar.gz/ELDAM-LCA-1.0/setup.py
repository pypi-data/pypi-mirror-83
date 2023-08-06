import setuptools

from eldam.settings import ELDAM_VERSION

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ELDAM-LCA",
    version=ELDAM_VERSION,
    author="Gustave Coste",
    author_email="gustave.coste@inrae.fr",
    description="Life Cycle Assessment data management",
    keywords="Life Cycle Assessment, Life Cycle Inventory, Data Quality",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://framagit.org/GustaveCoste/eldam",
    packages=['eldam'],
    package_data={'eldam': ['../files/*',
                            '../files/icons/*',
                            '../files/templates/*',
                            '../files/user_interfaces/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['jinja2',
                      'openpyxl']
)
