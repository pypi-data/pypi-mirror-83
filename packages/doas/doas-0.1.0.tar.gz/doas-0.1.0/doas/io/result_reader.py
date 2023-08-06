import datetime
import statistics

from ..utils import date_obj_from_format, floatable


class ResultFileReader(object):
    """
    DOAS result data file reader.

    This class is primarily used to read and parse the content of BDSO2CA.txt
    file. When creating an instance, you have to provide the path to the result
    file and date of measurement. If `exclude_zero` is True, it will leave row
    with flux value less than or equal to zero.
    """

    def __init__(self, path, date, exclude_zero=True):
        self.date = date
        self.path = path
        self.exclude_zero = exclude_zero

    def get_measurement_date(self):
        """
        Get measurement date as Python date object. If initial date is string
        type, it will convert to date object using format specified in the
        settings module.
        """
        if isinstance(self.date, str):
            date_obj = date_obj_from_format(self.date)
        elif isinstance(self.date, datetime.date):
            date_obj = self.date
        elif isinstance(self.date, datetime.datetime):
            date_obj = self.date.date()
        else:
            raise ValueError('Unsupported date input format.')

        return date_obj

    def get_raw_content(self):
        """
        Get raw content of result file.
        """
        with open(self.path, 'r') as f:
            content = f.read()
        return content

    def _read(self, as_dict=False):
        """
        Private method to read the content of result file. If `as_dict` is True,
        read content is returned as dictionary. Dictionary keys used are:
        - `scanindex`: Scan index iteration and total number of scan. For
          example: 0/19, 1/19.
        - `filepath`: Path to data retrieval file. For example:
          C:\work\ooi\20201009\BDretr\BD006.ret.
        - `starttime`: Start time of scan completed with date data. For example:
          2020-10-09 09:00:21.>
        - `endtime`: End time of scan completed with date data. For example:
          2020-10-09 09:13:51.
        - `angle`: Maximum angle of scan in degrees. For example: -18.90
          degrees.
        - `flux`: Maximum flux value of SO2 in ton/day. For example: 420.50
          ton/day.
        """
        measurement_date = self.get_measurement_date().strftime('%Y-%m-%d')

        def row_handler(row, exclude_zero=True, as_dict=False):
            scanindex = row[0]
            filepath = row[1]
            starttime = row[2]
            endtime = row[3]
            angle = float(row[4]) if floatable(row[4]) else None
            flux = float(row[5]) if floatable(row[5]) else None

            if exclude_zero:
                if flux is None or flux <= 0:
                    return {} if as_dict else []

            if as_dict:
                return {
                    'scanindex': scanindex,
                    'filepath': filepath,
                    'starttime': f"{measurement_date} {starttime}",
                    'endtime': f"{measurement_date} {endtime}",
                    'angle': angle,
                    'flux': flux,
                }
            return [
                scanindex,
                filepath,
                f"{measurement_date} {starttime}",
                f"{measurement_date} {endtime}",
                angle,
                flux,
            ]

        content = []
        with open(self.path, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                row = line.strip().split()
                parsed_row = row_handler(
                    row,
                    exclude_zero=self.exclude_zero,
                    as_dict=as_dict,
                )
                if parsed_row:
                    content.append(parsed_row)
        return content

    def read_values(self):
        """
        Read the several parts of file content including, `starttime`,
        `endtime`, `angle`, and `flux` values as list. The other fields will be
        excluded.
        """
        values = []
        content = self._read()
        if content:
            for item in content:
                values.append([
                    item[2],
                    item[3],
                    item[4],
                    item[5],
                ])
        return values

    def read_values_as_dict(self):
        """
        Similar with `read_values()` method but return the content as list of
        dictionary.
        """
        values = []
        content = self._read(as_dict=True)
        if content:
            for item in content:
                values.append({
                    'starttime': item['starttime'],
                    'endtime': item['endtime'],
                    'angle': item['angle'],
                    'flux': item['flux'],
                })
        return values

    def read_all_values(self):
        """
        Read the result file and return all content as list.
        """
        return self._read()

    def read_all_values_as_dict(self):
        """
        Similar with `read_all_values()` method but return the content as list
        of dictionary.
        """
        return self._read(as_dict=True)

    def read_compact_values(self):
        """
        Read only flux data and average the values. It will always return the
        content as list of list.
        """
        content = self._read()
        values = [item[5] for item in content]
        return [[
            self.get_measurement_date().strftime('%Y-%m-%d'),
            statistics.mean(values)
        ]]

    def read_compact_values_as_dict(self):
        """
        Similar with `read_compact_values()` method but return the content as
        list of dictionary. Dictionary keys used are `date` and `flux`.
        """
        content = self._read()
        values = [item[5] for item in content]
        return [{
            'date': self.get_measurement_date().strftime('%Y-%m-%d'),
            'flux': statistics.mean(values)
        }]
