"""
Local MRIQC Stats
-----------------

This module allows the user to compare his/her images with all
similar images collected at the same scanner and same parameters,
for purpose of Quality Control (QC).

IQM: Image Quality Metrics
"""

import json
import urllib.request
import urllib.error
from datetime import datetime
from numbers import Number
from pathlib import Path

import pandas as pd
import numpy as np

from .utils import (DEVICE_SERIAL_NO,
                    REPOSITORY_PATH,
                    MRIQC_SERVER,
                    RELEVANT_KEYS,
                    read_mriqc_json,
                    )


def get_month_number(month):
    """
    Get the month in numeric format or 'all'

    Parameters
    ----------
    month : int or str

    Returns
    -------
    n_month : int or 'all'
        Month in numeric format, or string 'all'
    """

    if isinstance(month, str):
        if month == 'current':
            n_month = datetime.today().month
        elif month == '':
            n_month = 'all'
        else:
            if len(month) == 3:
                n_month = datetime.strptime(month, '%b').month
            else:
                try:
                    n_month = datetime.strptime(month, '%B').month
                except ValueError:
                    print('Wrong month: {0}'.format(month))
                    raise
    elif isinstance(month, int):
        if not (0 < month < 13):
            raise ValueError('Wrong month: {0}'.format(month))
        else:
            n_month = month
    else:
        raise ValueError('Wrong month: {0}'.format(month))

    return n_month


def get_device_iqms_from_server(modality, month='current', year='current', device_serial_no=None, versions=None):
    """
    Grab all iqms for the given modality and device, for a given month/year

    Parameters
    ----------
    modality : str
        Imaging modality
        Options: "T1w", "T2w", "bold"
    month : int or str
    year : int or str
        Desired year, or "current"
    device_serial_no : str
        Serial number of the device for which we want to query the
        database
    versions : list of str
        Versions of MRIQC for which we want to retrieve data

    Returns
    -------
    Pandas DataFrame with all the entries

    """
    # TODO: - Define a global list or irrelevant fields:
    #         I can remove irrelevant fields (e.g., "WindowWidth", "WindowCenter", ...
    #         "SliceLocation"). Basically, all "Slices." fields.
    #       - see if saving the results as JSONs saves space (by adding them to the
    #         results only if the md5sum is not there already, or maybe replacing it)

    software = 'mriqc'
    url_root = 'https://{m_server}/api/v1/{{modality}}?{{query}}'.format(m_server=MRIQC_SERVER)

    if device_serial_no is None:
        device_serial_no = DEVICE_SERIAL_NO
    if isinstance(year, str):
        if year == 'current':
            year = datetime.today().year
        else:
            year = int(year)
    n_month = get_month_number(month)
    if versions is None:
        versions = ['*']

    # prepare the query and get the data.  E.g.:
    # "bids_meta.DeviceSerialNumber":"166018","_updated":{"$gte":"Fri,%2012%20Jul%202019%2017:20:32%20GMT"}}&page=1
    base_query = ['"bids_meta.DeviceSerialNumber":"{dev_no}"'.format(dev_no=device_serial_no),
                  '"provenance.software":"{software}"'.format(software=software)]
    # it looks like the API requires the full date and time (e.g.: "Fri, 12 Jul 2019 17:20:32 GMT" )
    if n_month == 'all':
        begin_date = datetime(year, 1, 1).strftime('%a, %d %b %Y %H:%M:%S GMT')
        end_date = datetime(year, 12, 31).strftime('%a, %d %b %Y %H:%M:%S GMT')
    else:
        begin_date = datetime(year, n_month, 1).strftime('%a, %d %b %Y %H:%M:%S GMT')
        if n_month < 12:
            end_date = datetime(year, n_month + 1, 1).strftime('%a, %d %b %Y %H:%M:%S GMT')
        else:  # December:
            end_date = datetime(year + 1, 1, 1).strftime('%a, %d %b %Y %H:%M:%S GMT')
    base_query.append(
        '"_updated":{{"$gte":"{begin_d}", "$lte":"{end_d}"}}'.format(
            begin_d=begin_date,
            end_d=end_date
        )
    )

    dfs = []
    for version in versions:
        query = base_query

        if version != '*':
            query.append('"provenance.version":"%s"' % version)

        page = 1
        while True:
            page_url = url_root.format(
                modality=modality,
                query='where={{{where}}}&page={page}'.format(
                    where=','.join(query),
                    page=page
                )
            )
            print(page_url)

            try:
                #   VERY IMPORTANT   #
                # Convert spaces in the page_url into "%20".  Otherwise, it doesn't work:
                with urllib.request.urlopen(page_url.replace(" ", "%20")) as url:
                    data = json.loads(url.read().decode())
                    dfs.append(pd.json_normalize(data['_items']))
                    if 'next' not in data['_links'].keys():
                        break
                    else:
                        page += 1
            except urllib.error.HTTPError as err:
                if err.code == 400:
                    print('No results for these dates')
                    break
                else:
                    raise
            except:
                print('error')
                raise

    if len(dfs) > 0:
        # Compose a pandas dataframe
        return pd.concat(dfs, ignore_index=True, sort=True)
    else:
        return None


def read_iqms(path):
    """
    Read the iqms from a file or folder
    Parameters
    ----------
    path : list or Path or str
        Path of the json file or directory with the iqms
    Returns
    -------
    iqms : pd.DataFrame
        DataFrame with the iqms
    """

    if isinstance(path, list):
        # read iqms from all items into a single DataFrame:
        iqms = pd.DataFrame()
        for p in path:
            this_iqms = read_iqms(p)
            iqms = pd.concat([iqms, this_iqms], ignore_index=True)
        iqms.drop_duplicates(subset=['provenance.md5sum'],
                             inplace=True,
                             keep='last')
    elif Path(path).is_dir():
        # read all the json files in the folder:
        iqms = read_iqms(list(Path(path).rglob('*.json')))
    elif Path(path).is_file():
        if str(path).endswith(".json"):
            # try to read as "normal" json:
            try:
                iqms = pd.read_json(path_or_buf=path, orient='split')
            except ValueError:
                # read it as mriqc does (mriqc/reports/individual.py):
                iqms = read_mriqc_json(path)
        else:
            # read it as table:
            iqms = pd.read_table(path)
    elif str(path).endswith(".json"):
        # it's a json file name, but the file does not exist:
        raise FileNotFoundError('File {} does not exist'.format(str(path)))
    else:
        raise RuntimeError('Wrong argument')

    return iqms


def download_and_save(modality, year, local_iqms_repository_folder, device_serial_no):
    """
    Download iqms from server and save to a file.

    Parameters
    ----------
    modality : str
        Imaging modality.
        Options: "T1w", "T2w", "bold"
    year : int or str
        Desired year, or "current"
    local_iqms_repository_folder : str or Path
        Path to the folder with the repository of iqms
    device_serial_no : str
        Serial number of the device for which we want to query the
        database

    Returns
    -------
    iqms : pd.DataFrame
        IQMs downloaded from server
    """

    if not local_iqms_repository_folder:
        local_iqms_repository_folder = REPOSITORY_PATH
    if not device_serial_no:
        device_serial_no = DEVICE_SERIAL_NO

    iqms = get_device_iqms_from_server(modality,
                                       year=year,
                                       month='',
                                       device_serial_no=device_serial_no)
    iqms.drop_duplicates(subset=['provenance.md5sum'], inplace=True)
    save_iqms_to_json_file(iqms, local_iqms_repository_folder / (
            str(year) + '_' + modality + ".json"))
    return iqms


def get_iqms_all_years(modality, year_init, local_iqms_repository_folder, device_serial_no):
    """
    Gets iqms for all the years, for a given modality.
    If they are not present in the local repository, it queries the MRIQC API
    server, downloads them and saves them to the local repository.

    Parameters
    ----------
    modality : str
        Imaging modality.
        Options: "T1w", "T2w", "bold"
    year_init : str or int
        Initial year since which to get data (Default: current - 2)
    local_iqms_repository_folder : str or Path
        Path to the folder with the repository of iqms
    device_serial_no : str
        Serial number of the device for which we want to query the
        database

    Returns
    -------
    iqms : pd.DataFrame
        IQMs for a given modality, for all years
    """

    if not year_init:
        year_init = datetime.today().year - 2
    elif int(year_init) > datetime.today().year:
        raise RuntimeError('"year_init" cannot be greater than current year.')

    iqms = pd.DataFrame()
    for year in range(int(year_init), datetime.today().year + 1):
        try:
            # Try to read from file:
            this_iqms = read_iqms(
                local_iqms_repository_folder / (str(year) + '_' + modality + ".json")
            )
        except FileNotFoundError:
            this_iqms = download_and_save(modality, year, local_iqms_repository_folder, device_serial_no)
        iqms = pd.concat([iqms, this_iqms], ignore_index=True)
    # drop duplicates:
    iqms.drop_duplicates(subset=['provenance.md5sum'], inplace=True)
    return iqms


def find_iqms_w_parameters(iqms_df, desired_params):
    """
    Find iqms in a DataFrame that match a dictionary of parameters

    Parameters
    ----------
    iqms_df : pd.DataFrame
        DataFrame with the iqms we want to search through
    desired_params : dict
        Dictionary with the parameters we want to match.
        If one key has more than one value, we can match any of them

    Returns
    -------
    matching_iqms_df : pd.DataFrame
        DataFrame with the iqms that match the parameters
    """
    idx = np.ones(len(iqms_df), dtype='bool')
    for key in desired_params.keys():
        idx_key = np.empty([len(iqms_df), len(desired_params[key])], dtype='bool')
        if isinstance(desired_params[key][0], Number):
            # The following is basically equivalent to:
            # for i, value in enumerate([desired_params[key]]):
            #     idx_key[:, i] = np.isclose(iqms_df[key] == value)
            idx_key = np.array(
                [np.isclose(iqms_df[key], val, rtol=0.01, equal_nan=True) for val in desired_params[key]]
            )
        elif isinstance(desired_params[key][0], str):
            idx_key = np.array(
                [iqms_df[key] == val for val in desired_params[key]]
            )
        elif isinstance(desired_params[key][0], np.bool_):
            idx_key = np.array([iqms_df[key] == val for val in desired_params[key]])

        # element-wise "OR":
        idx_key = (idx_key.sum(axis=0) > 0)
        idx = idx & idx_key

    matching_iqms_df = iqms_df[idx]

    return matching_iqms_df


def find_similar_iqms(iqms_df, sample_iqms):
    """
    Find iqms in a DataFrame that have the same RELEVANT_PARAMETERS
    as some sample_iqms

    Parameters
    ----------
    iqms_df : pd.DataFrame
        DataFrame with the iqms we want to search through
    sample_iqms : pd.DataFrame
        DataFrame with iqms for which we want to find similar iqms
        (Note: it can have more than one row)

    Returns
    -------
    matching_iqms_df : pd.DataFrame
        DataFrame with the iqms that match the parameters
    """

    # create the dictionary of values we need to match:
    similar_iqms = pd.DataFrame(columns=sample_iqms.columns)
    for index, iqm in sample_iqms.iterrows():
        desired_params = {}
        for key in RELEVANT_KEYS:
            if key in sample_iqms.columns:
                desired_params[key] = list(np.unique(iqm[key]))
        similar_to_iqm = find_iqms_w_parameters(iqms_df, desired_params)
        similar_iqms = similar_iqms.append(
            similar_to_iqm,
            ignore_index=True,
        )
    if 'provenance.md5sum' in similar_iqms.keys():
        similar_iqms.drop_duplicates(subset=['provenance.md5sum'], keep='last')
    return similar_iqms


def save_iqms_to_json_file(iqms, path, append=False):
    """
    Saves iqms to a json file

    Parameters
    ----------
    iqms : pd.DataFrame
        DataFrame containing Image Quality Metrics
    path : str
    append : bool
        Whether to append the iqms to an existing file
    """

    if not append:
        iqms.to_json(
            path_or_buf=path,
            orient='split',
            index=False,
            indent=4
        )
    # TODO: Handle the case append == True


def save_iqms_to_tsv(iqms, path):
    """
    Saves iqms to a tsv file to do the group plotting

    Parameters
    ----------
    iqms : pd.DataFrame
        DataFrame containing Image Quality Metrics
    path : Path or str
    """

    # replace "_etag" with "bids_name" (used by "group_html"):
    iqms = iqms.rename(index=str, columns={"_etag": "bids_name"})
    # save the iqms:
    iqms.to_csv(path, index=False, sep="\t")
