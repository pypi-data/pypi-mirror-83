# Check for NTGS standard of files.
#
# *Only checks the first sheet of a file

import argparse
import datetime
import textwrap
import logging
import numpy as np
import pandas as pd
import pathlib
import re
import sys
import time
import zipfile as zip

class FileDataChecker():
    # Index offset: CSV, Excel files contain column headers in first row, plus zero-indexed Python
    I_OFFSET = 2

    # Time regex for HH:MM:SS but with proper values (no 99 seconds, 25 hours, etc.)
    TIME_RGX = re.compile('^(?:2[0-3]|[01]?[0-9]):[0-5][0-9]:[0-5][0-9]')

    # Metre match - should expect all other columns to be #.#_m
    METRE_RGX = re.compile('^(?:(?!.*)|[+-]?((\d+\.?\d*)|(\.\d+)))(_m)$')

    # Error Dictionary
    ERRORS = {
        'time': 'An invalid time appears to be present: ',
        'date': 'An invalid date appears to be present: ',
        'unexpectedColumn': 'No further checking will be done because an unexpected column name was found: ',
        'unexpectedMetre': 'An unexpected metre column name was found: ',
        'unsupportedExt': 'The following file type is not supported: ',
        'coordinate': 'A problematic coordinate was found: ',
        'latitude': 'An erroneous latitude was found: ',
        'longitude': 'An erroneous longitude was found: ',
        'temperature': 'A problematic temperature was found: ',
        'noMeasures': 'No measurement columns were found.',
        'nonUniqueTime': 'A non unique time was found: '
    }

    # Expected column names in the exact order
    EXPECTED_COLS = [
        'project_name',
        'site_id',
        'latitude',
        'longitude',
        'date_YYYY-MM-DD',
        'time_HH:MM:SS'
    ]
    
    def __init__(self):
        self.log = logging.getLogger('main')

    def collectErrorIndex(self, errString, errValue, index):
        self.log.info(errString + str(errValue) + ' @ ROW ' + str((index + self.I_OFFSET)))
        
    def collectError(self, errString, errValue):
        self.log.info(errString + str(errValue))

    def checkTimeFmt(self, time, index):
        if self.TIME_RGX.match(str(time)) is None:
            self.collectErrorIndex(self.ERRORS['time'], time, index)

    def checkDateFmt(self, date, index):
        try:
            datetime.datetime.strptime(str(date).split(" ")[0], "%Y-%m-%d")
        except ValueError:
            self.collectErrorIndex(self.ERRORS['date'], date, index)

    def checkColNames(self, cols):
        initColsFlag = False
        foundMetreCols = False
        for i, name in enumerate(cols):
            if (i < len(self.EXPECTED_COLS)):
                if (name != self.EXPECTED_COLS[i]):
                    # If the current column name is not in the exact position with the exact expected name
                    self.collectError(self.ERRORS['unexpectedColumn'], name)
                    initColsFlag = True
            elif (i >= len(self.EXPECTED_COLS)):
                foundMetreCols = True
                if self.METRE_RGX.match(name) is None:
                    # Did not match the regex properly, so it is not a good column name
                    self.collectError(self.ERRORS['unexpectedMetre'], name)
                    
        return (initColsFlag, foundMetreCols)

    def checkTemperatures(self, temp, index):
        try:
            if temp == "":
                # Blank temperature values are OK
                return
            else:
                val = float(temp)
                if np.isnan(val):
                    # If it was a NaN (which is a valid float after conversion) - it's not good
                    self.collectErrorIndex(self.ERRORS['temperature'], temp, index)
        except ValueError:
            # Failed to convert to float
            self.collectErrorIndex(self.ERRORS['temperature'], temp, index)
      
    def checkLatitude(self, lat, index):
        # Only checks if the values here are valid latitude values, not if they have drifted off or are inconsistent.
        # They are expected to be the same throughout (per station/site).
        conversionFailure = False
        
        try:
            lat = float(lat)
        except ValueError:
            conversionFailure = True
            self.collectErrorIndex(self.ERRORS['coordinate'], lat, index)
        
        if conversionFailure: return
            
        if lat < -90 or lat > 90:
            self.collectErrorIndex(self.ERRORS['latitude'], lat, index)
            
    def checkLongitude(self, longitude, index):
        # Only checks if the values here are valid longitude values, not if they have drifted off or are inconsistent.
        # They are expected to be the same throughout (per station/site).
        conversionFailure = False
        
        try:
            longitude = float(longitude)
        except ValueError:
            conversionFailure = True
            self.collectErrorIndex(self.ERRORS['coordinate'], longitude, index)
        
        if conversionFailure: return
            
        if longitude < -180 or longitude > 180:
            self.collectErrorIndex(self.ERRORS['longitude'], longitude, index)
    
    def checkUniqueTimes(self, dateCol, timeCol):
        timeSeries = (dateCol + " " + timeCol)
        if not timeSeries.is_unique:
            dupeTimes = timeSeries.value_counts()[timeSeries.value_counts() > 1].index.tolist()
            for time in dupeTimes:
                self.collectError(self.ERRORS['nonUniqueTime'], time)
    
    def checkFile(self, filename):
        fileExt = pathlib.Path(filename).suffix
        self.log.info(f"\nChecking: {pathlib.Path(filename).name}")
        if fileExt == ".csv":
            df = pd.read_csv(filename, keep_default_na=False, float_precision="round_trip");
        elif fileExt in [".xls", ".xlsx"]:
            df = pd.read_excel(filename, keep_default_na=False);
        else:
            self.collectError(self.ERRORS['unsupportedExt'], fileExt)
            return 
       
        # Checks
        # Check all of the column names
        res = self.checkColNames(df.columns)
        # If the first six columns are not the expected ones - exit.
        if res[0]:
            return
        if not res[1]:
            # No metre columns found
            self.collectError(self.ERRORS['noMeasures'], '')
            
        # Latitude and longitude check
        df.apply(lambda row: self.checkLatitude(row['latitude'], row.name), axis=1)
        df.apply(lambda row: self.checkLongitude(row['longitude'], row.name), axis=1)
        
        # Time is in xx:xx:xx format
        df.apply(lambda row: self.checkTimeFmt(row['time_HH:MM:SS'], row.name), axis=1)
        
        # Date is in yyyy-mm-dd format
        df.apply(lambda row: self.checkDateFmt(row['date_YYYY-MM-DD'], row.name), axis=1)
        
        for i in range(len(self.EXPECTED_COLS), len(df.columns)): # All other metre columns
            # Temperature can be converted to float or not
            df.apply(lambda row: self.checkTemperatures(row[df.columns[i]], row.name), axis=1)
        
        # Check if all time values are unique
        self.checkUniqueTimes(df["date_YYYY-MM-DD"], df["time_HH:MM:SS"])

    @staticmethod
    def pathExists(path):
        if pathlib.Path(path).exists():
            return path
        else:
            raise argparse.ArgumentTypeError(f"The path specified does not exist: {path}")

    @staticmethod
    def createPathIfExists(path):
        if not pathlib.Path(path).exists():
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        return path

    def checkPath(self, pathLoc, isVerbose, logPath):
        pathLoc = pathlib.Path(pathLoc)
        finalFilePath = ''
        f_handle = None
        
        self.log.setLevel(logging.INFO)
        
        # Verbose printing or not
        if isVerbose:
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            self.log.addHandler(console)
        
        # Concerning log file output
        if logPath is not None:
            if not pathlib.Path(logPath).suffix:
                # If there is no suffix in the path, it means a directory was given
                FileDataChecker.createPathIfExists(logPath)
            else:
                # There is a parent folder that needs to be made, a file w/ extension was given
                FileDataChecker.createPathIfExists(pathlib.Path(logPath).parent)
        
        currTime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')
        if logPath:
            logPathObj = pathlib.Path(logPath)
            # Set logging file path
            if logPathObj.is_dir():
                # Is a directory - add file name and current time to log name
                finalFilePath = str(logPathObj.joinpath(pathLoc.stem)) + '_' + currTime + '.txt'
                f_handle = logging.FileHandler(filename=finalFilePath, mode='w')
            else:
                # User specified filename
                finalFilePath = logPathObj
                f_handle = logging.FileHandler(filename=finalFilePath, mode='w')
        else:
            # No log path specified, create in same directory as this script
            finalFilePath = pathLoc.stem + '_' + currTime + '.txt'
            f_handle = logging.FileHandler(filename=finalFilePath, mode='w')
            
        # File handler always writes to a file
        f_handle.setFormatter(logging.Formatter())
        f_handle.setLevel(logging.INFO)
        self.log.addHandler(f_handle)
        self.log.info(currTime)
        
        # If it's a zip file, unzip it to a directory and set the path to that directory.
        zipDir = ''
        if pathLoc.suffix == ".zip":
            # Current time appended to prevent read of similarly named zips
            zipDir = str(pathLoc.parent) + "\\" + str(pathLoc.stem) + currTime
            # Unzip the archive - expected zip files only
            with zip.ZipFile(pathLoc) as zf:
                zf.extractall(zipDir)
            pathLoc = pathlib.Path(zipDir)
            
        if pathLoc.is_dir():
            for filename in pathLoc.iterdir():
                if filename.is_file():
                    self.checkFile(filename)
            # Delete the unzipped directory and contents afterwards
            if zipDir != '':
                for filename in pathLoc.iterdir():
                    pathlib.Path(filename).unlink()
                pathlib.Path(zipDir).rmdir()
        elif pathLoc.is_file():
            filename = pathLoc
            self.checkFile(filename)
        else:
            self.log.error("Error: unrecognized path")
            return -1
        return 1

if __name__ == "__main__":
    # Parser init
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''
        Conducts checks on column names and values for CSV, XLS, and XLSX NTGS-standard data files. XLS/XLSX files have been known to contain problematic values themselves, consider converting to CSV.
        
        * Only checks the first sheet of a file
        * Expects data files to contain the first 6 columns with the exact following names:
        ***  project_name
        ***  site_id
        ***  latitude
        ***  longitude
        ***  date_YYYY-MM-DD
        ***  time_HH:MM:SS
        
        Error Explanations:
        Invalid Time - Time does not follow a valid time in the format HH:MM:SS.
        Invalid Date - Date values should be formatted as YYYY-MM-DD.
        Non Unique Time - The combination of date and time column values should uniquely occur/never repeat.
        Unexpected Column - One of the first 6 column names is not from the expected list of column names (or is not in the correct order). If this warning occurs, the columns must be resolved in the correct name and order first, otherwise no other checking is done.
        Unexpected Metre - All following metre columns after the first 6 column names should be formatted as "<decimal>_m" only.
        No Measurements - No measurement columns are detected in the file.
        File Type - The file read in is not supported.
        Coordinate - A latitude or longitude value contains something that is not valid.
        Latitude - A latitude value is found that is not valid (Less than -90 or greater than 90).
        Longitude - A longitude value is found that is not valid (Less than -180 or greater than 180).
        Temperature - A temperature value is found that is not a valid temperature.
        '''))
    parser.add_argument('location', metavar='path', type=FileDataChecker.pathExists, help='Path to specified directory or single file. Non-recursive if directory.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Displays detected issues with the checked file during operation of the program.')
    parser.add_argument('--log-path', metavar='log-path', help='Specified path where output log file should be saved to.')
    arguments = vars(parser.parse_args())
    
    checkingFilePath = arguments['location']
    isVerbose = arguments['verbose']
    outputLogPath = arguments['log_path']
    
    fdc = FileDataChecker()
    fdc.checkPath(checkingFilePath, isVerbose, outputLogPath)
