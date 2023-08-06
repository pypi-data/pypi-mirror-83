import datetime
import os
import shutil
import subprocess

from . import settings
from .constants import MONTH_CODES


def floatable(value):
    try:
        _ = float(value)
        return True
    except (ValueError, TypeError):
        return False


def run_cmd(cmd):
    """Run subprocess command."""
    return subprocess.run(cmd)


def run_cmd_dry(cmd):
    """
    Run subprocess command in dry run. This is not actually execute the command.
    """
    pass


def edit_sd_ini(
        path,
        folder_name,
        spectrometer_id='USB2+H11553',
        station_name=settings.STATION_NAME):
    """
    Edit task.ini file.

    Folder name format is DYYmdd. For example: D20115.
    """
    with open(path, 'w') as f:
        f.write(folder_name + '\n')
        f.write(station_name + '\n')
        f.write(spectrometer_id + '\n')
        f.write("+250")


def edit_task_ini(
        path,
        date_string,
        station_name=settings.STATION_NAME):
    """
    Edit task.ini file.

    Date string format is YYYYmmdd. For example: 20200115.
    """
    with open(path, 'w') as f:
        f.write(date_string + "\n")
        f.write('0\n')
        f.write(station_name)


def is_processed(date_string, filename=None):
    """
    Check if current date string folder, for example 20200115, already contains
    processed data.

    It is done by checking result filename. If exists, return True. Otherwise,
    return False.
    """
    result_filename = filename or settings.RESULT_FILENAME
    result_fullpath = os.path.join(
        settings.OOI_PATH, date_string, result_filename)
    return os.path.isfile(result_fullpath)


def date_obj_from_format(date_string, format=[]):
    """
    Convert date string to date object with specifed date input format list. If
    input format list is empty, it uses format list from settings module.

    When none of input format succeeded, return None.
    """
    def to_date_obj(date_string, format):
        try:
            datetime_obj = datetime.datetime.strptime(date_string, format)
            return datetime_obj.date()
        except (ValueError, AttributeError):
            return None

    date_input_formats = format if len(
        format) > 0 else settings.DATE_INPUT_FORMATS
    for input_format in date_input_formats:
        date_obj = to_date_obj(date_string, input_format)
        if date_obj:
            return date_obj

    return None


def format_sd_ini_date(date_obj):
    """Convert date object to SD.ini date, i.e. DYYmdd."""
    format = '%y%m%d'
    dts = date_obj.strftime(format)
    return f"D{dts[0:2]}{MONTH_CODES[dts[2:4]]}{dts[4:6]}"


def format_task_ini_date(date_obj):
    """Convert date object to task.ini date, i.e. YYYYmmdd."""
    format = '%Y%m%d'
    return date_obj.strftime(format)


def get_date_obj(date):
    if isinstance(date, str):
        date_obj = date_obj_from_format(date)
        if date_obj is None:
            raise ValueError('Invalid date input string.')
    elif isinstance(date, datetime.date):
        date_obj = date
    else:
        raise ValueError('Unsupported date type.')

    return date_obj


def build_result_path(date):
    """
    Build absolute path to the result file from certain date. Result file name
    is specified from settings module.

    `date` input argument can be a date object or string. 
    """
    date_obj = get_date_obj(date)
    date_string = format_task_ini_date(date_obj)
    return os.path.join(
        settings.OOI_PATH, date_string, settings.RESULT_FILENAME)


def build_input_data_path(date):
    """
    Build absolute path to the input data folder. Input date folder format is
    like in SD.ini file, i.e. DYYmdd. For example: D20115.

    `date` input argument can be a date object or string. 
    """
    date_obj = get_date_obj(date)
    date_string = format_sd_ini_date(date_obj)
    return os.path.join(settings.OOI_PATH, date_string)


def build_work_data_path(date):
    """
    Build absolute path to the work data folder. Work data folder example:
    20190101.

    `date` input argument can be a date object or string. 
    """
    date_obj = get_date_obj(date)
    date_string = format_task_ini_date(date_obj)
    return os.path.join(settings.OOI_PATH, date_string)


def clean_folder(path):
    """
    Remove directory recursively.
    """
    shutil.rmtree(path)


class Answer:
    YES = 'yes'
    NO = 'no'
    NONE = 'none'

    @classmethod
    def check_answer(cls, value):
        value_string = str(value).lower()
        if value_string == 'y' or value_string == 'yes':
            return cls.YES
        elif value_string == 'n' or value_string == 'no':
            return cls.NO
        else:
            return cls.NONE


def is_data_input_folder(value, check_exist=False):
    """
    Check if value is data input folder, e.g D20A09. If folder exists in ooi
    work directory, return True. Otherwise, return False.
    """
    path = os.path.join(settings.OOI_PATH, value)
    try:
        decoded_date = decode_data_input_folder(value)
    except (ValueError, AttributeError):
        decoded_date = None

    if check_exist:
        return (
            value.startswith('D') and
            len(value) == 6 and
            os.path.isdir(path) and
            decoded_date is not None
        )
    return (
        value.startswith('D') and
        len(value) == 6 and
        decoded_date is not None
    )


def is_data_result_folder(value, check_exist=False):
    """
    Check if value is data result folder, e.g. 20201009.
    """
    path = os.path.join(settings.OOI_PATH, value)
    try:
        decoded_date = decode_data_result_folder(value)
    except (ValueError, AttributeError):
        decoded_date = None

    if check_exist:
        return len(value) == 8 and os.path.isdir(path)
    return len(value) == 8 and decoded_date is not None


def decode_data_input_folder(value):
    """
    Decode and convert data input folder, e.g. D20A09 to Python date object.

    See also `Create_folders_DATE_and_DATASET` function at
    work/scripts/SD_conversion/SD_Conversion_Functions.js.
    """
    if len(value) != 6:
        raise ValueError('Value length must be 6')

    year = value[1:3]
    month_code = value[3:4]
    date = value[4:6]
    month = MONTH_CODES.get(month_code.upper())
    if month is None:
        raise ValueError('Unable to get month code')

    return datetime.datetime.strptime(f'{year}{month}{date}', '%y%m%d').date()


def decode_data_result_folder(value):
    """
    Decode and convert data result folder, e.g. 20201009 to Python date object.
    """
    return datetime.datetime.strptime(value, '%Y%m%d')
