""" Module to handle the IQMs comparison for a BIDS subject/session """

from pathlib import Path

from .utils import (REPOSITORY_PATH,
                    DEVICE_SERIAL_NO,
                    read_mriqc_json,
                    )
from .plots import report_comparison_w_similar
from .local_mriqc_stats import (get_iqms_all_years,
                                )


def bids_mriqc_comparison(mriqc_reports,
                          subject,
                          session=None,
                          local_iqms_repository_folder=None,
                          device_serial_no=None,
                          year_init=2018):
    """
    Wrapper function to do the report_comparison_w_similar for a
    BIDS subject/session

    Returns
    -------

    """
    if not local_iqms_repository_folder:
        local_iqms_repository_folder = REPOSITORY_PATH

    # first, get the json files for this subject/session:
    target_folder = Path(mriqc_reports) / ('sub-' + subject)
    if session:
        target_folder = target_folder / ('ses-' + session)
    jsons = {
        'T1w': list((target_folder / 'anat').rglob('sub-*T1w.json')),
        'T2w': list((target_folder / 'anat').rglob('sub-*T2w.json')),
        'bold': list((target_folder / 'func').rglob('sub-*_bold.json'))
    }
    # bold_folder = target_folder / 'func'

    if not device_serial_no:
        # Get it from the MRIQC reports.
        # Loop through all json files found:
        for file in [f for jj in jsons.values() for f in jj]:
            if file.exists():
                iqms = read_mriqc_json(file)
                device_serial_no = iqms['bids_meta.DeviceSerialNumber'][0]
                break
        if not device_serial_no:
            device_serial_no = DEVICE_SERIAL_NO

    # now, get the iqms to which compare:
    for modality in jsons.keys():
        if jsons[modality]:
            iqms_set = get_iqms_all_years(modality, year_init, local_iqms_repository_folder, device_serial_no)
            report_html = Path(mriqc_reports) / ('comparison_sub-' + subject + '_' + modality + '.html')
            report_comparison_w_similar(jsons[modality], iqms_set, report_html)
