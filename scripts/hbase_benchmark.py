import dicom
from datetime import datetime

from data_labeling.clients.hbase_client import HBaseClient


DATA_SOURCE = 'example_data/kaggle'

print('Connecting to HBase.')
connection = HBaseClient()

print('Creating table with slices.')
try:
    connection.create_table('slices', {
        'dicom': dict(),
    })
except Exception:
    # This table may exists, so let's remove it and create again (empty)
    connection.delete_table('slices', disable=True)
    connection.create_table('slices', {
        'dicom': dict(),
    })

print('Reading example Dicom.')
ex_slice = dicom.read_file('example_data/example_dicom.dcm')
data = ex_slice.pixel_array.tostring()

print('Filling empty table with original Dicoms.')
slices_table = connection.table('slices')
# for scan_path in glob.iglob(DATA_SOURCE + '/**/*.dcm'):
#     add...

print('Adding ({})...'.format(datetime.now()))
for i in range(100):
    if i % 10 == 0:
        print('{} already added...'.format(i*10))
    slices_table.put('example_key_{}'.format(i), {'dicom:value': data})
print('Added 100 records ({}).'.format(datetime.now()))

print('Reading ({})...'.format(datetime.now()))
for i in range(100):
    if i % 10 == 0:
        print('{} already read...'.format(i*10))
    _ = slices_table.row('example_key_{}'.format(i))[b'dicom:value']
print('Read 100 records ({}).'.format(datetime.now()))
