# mriqc_comparison
Compare your MRIQC results with other similar runs

#### Example ####
To compare the [MRIQC](https://github.com/poldracklab/mriqc) Image Quality Metrics (IQMs) of subject `01` for a study with the IQMS of all other runs with comparable acquisition parameters collected in the same scanner since `2018`: 
```python
from mriqc_comparison.bids import bids_mriqc_comparison
bids_mriqc_comparison(mriqc_reports="My/Mriqc/Output/Folder",
                      subject="01",
                      year_init=2018)
```
A series of new html files with the comparisons for the different image modality will be created in the `mriqc_reports` input folder.

## About ##

`mriqc_comparison` is a tool that allows you to compare [MRIQC](https://github.com/poldracklab/mriqc) Image Quality Metrics (IQMs) corresponding to certain runs with IQMs from other runs collected with similar parameters (so that the comparison is meaningful). For example, it allows you to compare the IQMs for your runs with all the other runs collected in the same scanner; or to compare your IQMs with those from a different scanner.

[MRIQC](https://github.com/poldracklab/mriqc) does give you the option to generate a report comparing the IQMs for all runs in a given BIDS project. However, it does not allow you to compare IQMs across your projects, or with a colleague's data. This tool comes in to fill that gap.

To generate these comparison reports, you can get the IQMs from the `group_*.tsv` files generaged by the [MRIQC](https://github.com/poldracklab/mriqc) group reports, or you can get them online: [MRIQC](https://github.com/poldracklab/mriqc) sends an annonymized list of the IQMs to a public server (hosted by NIH). The BIDS project name, subject's ID and run name are scrubbed from the data, but if you know the `DeviceSerialNumber` for a certain scanner, you can download all the IQMs corresponding to that scanner stored in the public server. Alternatively, you could also download all the data corresponding to a given scanner model (e.g., "Siemens Prisma")

Once you have the IQMs you want to use in your comparison, you can generate a group report, showing all of the runs, or showing only those runs that were acquired with certain scanning parameters, etc. Also, you can have the group report highlighting certain runs; for example, you can generate a report showing the IQMs of all functional runs collected in your center, highlighting those corresponding to your study, to see if you get similar data to other labs in your center.

The tool is written in Python3, and requires [MRIQC](https://github.com/poldracklab/mriqc).

## Installation ##

You can install `mriqc_comparison` from PyPI using `pip`:

```
pip install mriqc_comparison
```

## Dependencies ##

- [mriqc](https://github.com/poldracklab/mriqc) (>= 0.13.0)
- [pandas](https://pandas.pydata.org) (>= 0.25.0)
- [numpy](https://numpy.org) (>= 1.17.1)


## Usage ##

To download the IQMs corresponding to a given center, year and modality:

```python
from mriqc_comparison import local_mriqc_stats
iqms = local_mriqc_stats.get_device_iqms_from_server(modality, year=year, month='', device_serial_no=dev_sn)
```
where `modality = ['T1w', 'T2w', 'bold']`, `year` is the desired year or `'current'` and `dev_sn` is the scanner serial number (you can find your scanner SN in one of the json files in the mriqc output folder, under the key `"DeviceSerialNumber"`)

Then, you can drop duplicate entries:

```python
iqms.drop_duplicates(subset=['provenance.md5sum'], inplace=True)
```
You can save all the `iqms` in a json file (so that you don't need to query the server again):

```python
local_mriqc_stats.save_iqms_to_json_file(iqms, iqms_json_file)
```
Where `iqms_json_file` is the path to the file where you want to save the data.

If you have a dataframe with your own iqms which you want to compare to all other iqms that you have downloaded from the server:

```python
from mriqc_comparison import plots
plots.report_comparison_w_similar(my_iqms, center_iqms, comparison_report_html)
```
Where `my_iqms` is the dataframe or json file with your iqms, `center_iqms` is the dataframe or json file with the iqms for your center (or any other iqms you want to compare to) and `comparison_report_html` in the output html file with the report.
