""" ELDAM settings """
import pathlib

ELDAM_BASE_FOLDER = pathlib.Path(__file__).parents[2]

# Miscellaneous
PROGRAM_NAME = "ELDAM"
CONTACT_MAIL = "gustave.coste@inra.fr"
REPOSITORY_URL = "https://framagit.org/GustaveCoste/eldam"
CHANGELOG_URL = "https://framagit.org/GustaveCoste/eldam/blob/master/CHANGELOG.rst"
DOCUMENTATION_URL = "https://framagit.org/GustaveCoste/eldam/wikis/home"
LICENSE_URL = "https://framagit.org/GustaveCoste/eldam/blob/master/LICENSE"
ISSUE_TRACKER_URL = "https://framagit.org/GustaveCoste/eldam/issues"
DOWNLOAD_URL = "https://framagit.org/GustaveCoste/eldam/wikis/FAQ/download"
ELDAM_VERSION = "1.0"

# Elda template
ELDA_TEMPLATE_VERSION = "0.19"  # WARNING: Update this version number according to the elda template

# SimaPro export CSV delimiter
CSV_DELIMITER = ";"

# WARNING: Set this constant to False on production
DEBUG = False
