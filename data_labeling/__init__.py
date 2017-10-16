"""Module defining whole application"""

# WATCH OUT: Script that migrates HBase schema may not work properly if you want to change name of a column!
#            In such case please run your migration manually!
HBASE_SCHEMA = {
    'scans': ['metadata'],
    'original_slices': ['position', 'image'],
    'converted_slices': ['position', 'image'],
}
