"""
Script used to regenerate elda test files. Files are created in a separate "update" folder to allow for verifications
before erasing.
"""
import openpyxl

from eldam.core.elda import Elda
from eldam.core.elda_index import EldaIndexer
from eldam.core.simapro import SimaProCsvWriter
from eldam.utils.exceptions import ParameterConflictError
from tests.testing_parameters import *
from tests.test_data import *

UPDATE_FOLDER = os.path.join(os.path.dirname(__file__), 'data/update')
ELDA_INDEX_FOLDER = os.path.join(os.path.dirname(__file__), 'data/update/elda_index')
EXCEL_LINK = "'" + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data',
                                "[value_to_be_linked.xlsx]Feuil1'!$C$4")

UPDATE_ELDA_A = UPDATE_ELDA_A_WITH_PROCESS_B_METADATA = UPDATE_ELDA_A_WITH_EXCEL_LINK = UPDATE_XLSX_A_WITH_EXCEL_LINK = \
    UPDATE_ELDA_B = UPDATE_ELDA_R = UPDATE_ELDA_C_MINOR = UPDATE_ELDA_C_MAJOR = UPDATE_ELDA_D = UPDATE_ELDA_E = \
    UPDATE_CSV_A = UPDATE_CSV_B = UPDATE_CSV_B_WITHOUT_ELDA_DATA = UPDATE_CSV_C = UPDATE_CSV_A_B = UPDATE_CSV_D = \
    UPDATE_CSV_E = UPDATE_ELDA_INDEX = UPDATE_INDEXED_ELDAS = False

# Uncomment these lines to run corresponding mode
UPDATE_ELDA_A = True
UPDATE_ELDA_A_WITH_PROCESS_B_METADATA = True
UPDATE_ELDA_A_WITH_EXCEL_LINK = True
UPDATE_XLSX_A_WITH_EXCEL_LINK = True
UPDATE_ELDA_B = True
UPDATE_ELDA_R = True
UPDATE_ELDA_C_MINOR = True
UPDATE_ELDA_C_MAJOR = True
UPDATE_ELDA_D = True
UPDATE_ELDA_E = True
UPDATE_CSV_A = True
UPDATE_CSV_B = True
UPDATE_CSV_B_WITHOUT_ELDA_DATA = True
UPDATE_CSV_C = True
UPDATE_CSV_A_B = True
UPDATE_CSV_D = True
UPDATE_CSV_E = True
UPDATE_ELDA_INDEX = True
UPDATE_INDEXED_ELDAS = True
# Creating a directory named Update if it doesn't already exists
if not os.path.isdir(UPDATE_FOLDER):
    os.mkdir(UPDATE_FOLDER)

if UPDATE_ELDA_A:
    elda = Elda()
    process = process_a()
    process.remove_unused_parameters()
    elda.add_version(process)

    elda.save(os.path.join(UPDATE_FOLDER, "elda_a.xlsm"))

if UPDATE_ELDA_A_WITH_PROCESS_B_METADATA:
    elda = Elda()
    process = process_a_with_process_b_metadata()
    process.remove_unused_parameters()
    elda.add_version(process)

    elda.save(os.path.join(UPDATE_FOLDER, "elda_a_with_process_b_metadata.xlsm"))

if UPDATE_ELDA_A_WITH_EXCEL_LINK:
    elda = Elda()
    process = process_a()

    flow_to_update = [x for x in process.flows if
                      x.name == 'Heat, central or small-scale, natural gas {Europe without Switzerland}|' \
                                ' market for heat, central or small-scale, natural gas | Cut-off, U'][0]
    flow_to_update.amount = EXCEL_LINK
    flow_to_update.amount_type = 'Formula'

    parameter_to_update = [x for x in process.calculated_parameters if x.name == "A_plus_NO2"][0]
    parameter_to_update.formula = parameter_to_update.value_or_formula = EXCEL_LINK
    # parameter_to_update.formula = parameter_to_update.value_or_formula = r"'C:\Users\costegus\Documents\ELSA data\ELDAM\tests\data\[value_to_be_linked.xlsx]Feuil1'!$C$4"
    process.remove_unused_parameters()
    elda.add_version(process)

    elda.save(os.path.join(UPDATE_FOLDER, "elda_a_with_excel_link.xlsm"))

if UPDATE_XLSX_A_WITH_EXCEL_LINK:
    xlsx = openpyxl.load_workbook(XLSX_A)
    xlsx.active['B51'].value = xlsx.active['B84'].value = EXCEL_LINK
    xlsx.save(os.path.join(UPDATE_FOLDER, "xlsx_a_with_excel_link.xlsx"))

if UPDATE_ELDA_B:
    elda = Elda()
    process = process_b()
    process.remove_unused_parameters()
    elda.add_version(process)

    elda.save(os.path.join(UPDATE_FOLDER, "elda_b.xlsm"))

if UPDATE_ELDA_R:
    process = process_b()
    process.remove_unused_parameters()

    elda_r = Elda(os.path.join(UPDATE_FOLDER, "elda_a.xlsm"))
    elda_r.add_version(process, major_version=False)

    elda_r.save(os.path.join(UPDATE_FOLDER, "elda_r.xlsm"))

if UPDATE_ELDA_C_MINOR:
    process = process_c()
    process.remove_unused_parameters()

    elda_c_minor = Elda(os.path.join(UPDATE_FOLDER, "elda_r.xlsm"))
    elda_c_minor.add_version(process, major_version=False)
    elda_c_minor.save(os.path.join(UPDATE_FOLDER, "elda_c_minor.xlsm"))

if UPDATE_ELDA_C_MAJOR:
    process = process_c()
    process.remove_unused_parameters()

    elda_c_major = Elda(os.path.join(UPDATE_FOLDER, "elda_r.xlsm"))
    elda_c_major.add_version(process, major_version=True)
    elda_c_major.save(os.path.join(UPDATE_FOLDER, "elda_c_major.xlsm"))

if UPDATE_ELDA_D:
    elda = Elda()
    process = process_d()
    process.remove_unused_parameters()
    elda.add_version(process)

    elda.save(os.path.join(UPDATE_FOLDER, "elda_d.xlsm"))

if UPDATE_ELDA_E:
    elda = Elda()
    process = process_e()
    process.remove_unused_parameters()
    elda.add_version(process)

    elda.save(os.path.join(UPDATE_FOLDER, "elda_e.xlsm"))

if UPDATE_CSV_A:
    process = process_a()
    process.remove_unused_parameters()

    SimaProCsvWriter(process).to_csv(os.path.join(UPDATE_FOLDER, "csv_a.csv"))

if UPDATE_CSV_B:
    process = process_b()
    process.remove_unused_parameters()

    SimaProCsvWriter(process).to_csv(os.path.join(UPDATE_FOLDER, "csv_b.csv"))

if UPDATE_CSV_B_WITHOUT_ELDA_DATA:
    process = process_b()
    process.remove_unused_parameters()

    SimaProCsvWriter(process, elda_only_data=False).to_csv(
        os.path.join(UPDATE_FOLDER, "csv_b_without_elda_only_data.csv"))

if UPDATE_CSV_C:
    process = process_c()
    process.remove_unused_parameters()

    SimaProCsvWriter(process).to_csv(os.path.join(UPDATE_FOLDER, "csv_c.csv"))

if UPDATE_CSV_A_B:
    process_1 = process_a()
    process_2 = process_b()

    process_1.remove_unused_parameters()
    process_2.remove_unused_parameters()

    try:
        SimaProCsvWriter(process_1, process_2).to_csv(os.path.join(UPDATE_FOLDER, "csv_a_b.csv"))
    except ParameterConflictError as error:

        chosen_parameters = [params[0] for params in error.args[0]]  # Simulating user choice
        SimaProCsvWriter(process_1, process_2,
                         chosen_parameters=chosen_parameters).to_csv(os.path.join(UPDATE_FOLDER, "csv_a_b.csv"))

if UPDATE_CSV_D:
    process = process_d()
    process.remove_unused_parameters()

    SimaProCsvWriter(process).to_csv(os.path.join(UPDATE_FOLDER, "csv_d.csv"))

if UPDATE_CSV_E:
    process = process_e()
    process.remove_unused_parameters()

    SimaProCsvWriter(process).to_csv(os.path.join(UPDATE_FOLDER, "csv_e.csv"))

if UPDATE_INDEXED_ELDAS:
    elda = Elda()
    process = process_a()
    process.remove_unused_parameters()
    elda.add_version(process)
    elda.save(os.path.join(ELDA_INDEX_FOLDER, "elda_a.xlsm"))

    elda = Elda(os.path.join(ELDA_INDEX_FOLDER, "elda_a.xlsm"))
    process = process_b()
    process.flows = process.product_flows  # Removing flows and parameters to have "Needs change" review state
    process.remove_unused_parameters()
    elda.add_version(process)
    elda.save(os.path.join(ELDA_INDEX_FOLDER, "elda_b.xlsm"))

    #  Setting all metadata review to valid
    metadata_review = process.metadata_review
    for data in metadata_review.values():
        data['review_state'] = 2
    process.metadata_review = metadata_review

    products = process.product_flows
    for flow in products:
        flow.review_state = 2
    process.flows = products
    elda = Elda(os.path.join(ELDA_INDEX_FOLDER, "elda_b.xlsm"))
    elda.add_version(process)
    elda.save(os.path.join(ELDA_INDEX_FOLDER, 'subfolder', "elda_b.xlsm"))

if UPDATE_ELDA_INDEX:
    if os.path.isfile(os.path.join(ELDA_INDEX_FOLDER, 'EldaIndex.xlsx')):
        os.remove(os.path.join(ELDA_INDEX_FOLDER, 'EldaIndex.xlsx'))

    indexer = EldaIndexer(ELDA_INDEX_FOLDER)
    indexer.build_index()
    indexer.save_index()
