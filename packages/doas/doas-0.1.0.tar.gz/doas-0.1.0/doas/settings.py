import os

# DOASIS scripts are hard coded to C:\work directory. So, we follow their rules.
BASE_PATH = os.path.join('C:' + os.sep, 'work')

STATION_NAME = 'BD'

DATA_PATH = os.path.join(BASE_PATH, 'data')
OOI_PATH = os.path.join(BASE_PATH, 'ooi')
SCRIPTS_PATH = os.path.join(BASE_PATH, 'scripts')
SPECTRA_PATH = os.path.join(BASE_PATH, 'spectra')
SPECTROMETERS_PATH = os.path.join(BASE_PATH, 'spectrometers')

DATA_CHECK_PATH = os.path.join(SCRIPTS_PATH, 'Data_Check')
DATA_CORRECTION_PATH = os.path.join(SCRIPTS_PATH, 'Data_Correction')
DATA_RETRIEVAL_PATH = os.path.join(SCRIPTS_PATH, 'Data_Retrieval')
DATA_START_PATH = os.path.join(SCRIPTS_PATH, 'Data_Start')
HT_EXPLORE_PATH = os.path.join(SCRIPTS_PATH, 'HT_explore')
SD_CONVERSION_PATH = os.path.join(SCRIPTS_PATH, 'SD_conversion')

DATA_CHECK_BAT = os.path.join(DATA_CHECK_PATH, 'start_Data_Check.bat')
DATA_CORRECTION_BAT = os.path.join(
    DATA_CORRECTION_PATH, 'start_Data_Correction.bat')
DATA_RETRIEVAL_BAT = os.path.join(
    DATA_RETRIEVAL_PATH, 'start_Data_Retrieval.bat')
DATA_START_BAT = os.path.join(DATA_START_PATH, 'Start.bat')
HT_EXPLORE_BAT = os.path.join(HT_EXPLORE_PATH, 'HT_explore.bat')
SD_CONVERSION_BAT = os.path.join(SD_CONVERSION_PATH, 'start_SD_Conversion.bat')

SD_INI_FILENAME = 'SD.ini'
TASK_INI_FILENAME = 'task.ini'
SD_INI_PATH = os.path.join(OOI_PATH, SD_INI_FILENAME)
TASK_INI_PATH = os.path.join(OOI_PATH, TASK_INI_FILENAME)

RESULT_FILENAME = f'{STATION_NAME}SO2CA.txt'

DATE_INPUT_FORMATS = [
    '%Y-%m-%d',   # '2020-10-25'
    '%Y%m%d',     # '20201025
    '%y%m%d',     # '191025'
    '%m/%d/%Y',   # '10/25/2020'
    '%m/%d/%y',   # '10/25/06'
    '%b %d %Y',   # 'Oct 25 2020'
    '%b %d, %Y',  # 'Oct 25, 2020'
    '%d %b %Y',   # '25 Oct 2020'
    '%d %b, %Y',  # '25 Oct, 2020'
    '%B %d %Y',   # 'October 25 2020'
    '%B %d, %Y',  # 'October 25, 2020'
    '%d %B %Y',   # '25 October 2020'
    '%d %B, %Y',  # '25 October, 2020'
]

DRY_RUN = False
