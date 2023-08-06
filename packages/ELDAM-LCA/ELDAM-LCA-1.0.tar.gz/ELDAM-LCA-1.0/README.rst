ELDAM
=====

.. image:: files/icons/ELDAM.png

**ELDAM (ELsa DAta Manager)** is a program developed by Gustave Coste (`gustave.coste@inra.fr <mailto:gustave.coste@inra.fr>`_) for Life Cycle Analysis data management and conversion based on `ELSA <http://www.elsa-lca.org/>`_'s Quality Management System.

It allows conversion from SimaPro .xlsx export files to Elda spreadsheet and from Elda spreadsheet to SimaPro import csv file.

It features an integrated GUI for graphical use and can also be used easily within a python environment with its API.

.. code-block:: python

    from eldam.core.simapro import SimaProXlsxReader, SimaProCsvWriter
    from eldam.core.elda import Elda

    # SimaPro export file -> Elda spreadsheet
    process = SimaProXlsxReader('path/to/xlsx/file').to_processes()[0]
    elda = Elda()
    elda.add_version(process)
    elda.save('path/to/elda')

    # Elda spreadsheet -> SimaPro import file
    elda = Elda('path/to/elda')
    process = elda.read_last_version().to_process()
    SimaProCsvWriter(process).to_csv('path/to/csv')
  

Features
--------

- Conversion from SimaPro .xlsx export file to Elda spreadsheet
- Conversion from Elda spreadsheet to SimaPro import csv file
- Comparison between SimaPro export file and Elda spreadsheet
- Elda files indexing
- Graphical user interface
- Process detailed view
- Process quality check

Installation and documentation
------------------------------

- User documentation: `framagit.org/GustaveCoste/eldam/wikis/home <https://framagit.org/GustaveCoste/eldam/wikis/home>`_
- API documentation: `eldam-lca.readthedocs.io <https://eldam-lca.readthedocs.io>`_
- Download: `framagit.org/GustaveCoste/eldam/wikis/FAQ/download <https://framagit.org/GustaveCoste/eldam/wikis/FAQ/download>`_

Contribute
----------

- Issue Tracker: `framagit.org/GustaveCoste/eldam/issues <https://framagit.org/GustaveCoste/eldam/issues>`_
- Source Code: `framagit.org/GustaveCoste/eldam <https://framagit.org/GustaveCoste/eldam>`_

Support
-------

If you are having issues, please contact `gustave.coste@inra.fr <mailto:gustave.coste@inra.fr>`_.

Funded by
---------

.. image:: ../../files/icons/eu.png
.. image:: ../../files/icons/eu_occitanie.png
.. image:: ../../files/icons/occitanie.png

