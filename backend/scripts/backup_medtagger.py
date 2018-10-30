"""Script for backuping whole MedTagger."""
# flake8: noqa: T001  # Prints instead of logging
import os
import json
from typing import Dict, List  # pylint: disable=unused-import

from medtagger.definitions import LabelTool
from medtagger.repositories import (
    roles as RolesRepository,
    users as UsersRepository,
    scans as ScansRepository,
    slices as SlicesRepository,
    labels as LabelsRepository,
    label_tags as LabelTagsRepository,
    datasets as DatasetsRepository,
)

BACKUP_DIRECTORY = 'medtagger_backup/'
SCANS_DIRECTORY = BACKUP_DIRECTORY + 'dicoms/'
ROLES_AND_USERS_FILE = BACKUP_DIRECTORY + 'roles_and_users.json'
LABELS_FILE = BACKUP_DIRECTORY + 'labels.json'
SCANS_METADATA_FILE = BACKUP_DIRECTORY + 'scans.json'


def create_directory(directory: str) -> None:
    """Create new directory if not exists."""
    if not os.path.exists(directory):
        print('Creating directory: {}.'.format(directory))
        os.makedirs(directory)


# Create needed directory
create_directory(BACKUP_DIRECTORY)

# Backup all Roles & Users to one JSON file
_users_and_roles = {
    'roles': [],
    'users': [],
}  # type: Dict[str, List[Dict]]
print('\nFetching all Roles...')
for role in RolesRepository.get_all_roles():
    print('Saving Role: {}'.format(role.name))
    _users_and_roles['roles'].append({
        'id': role.id,
        'name': role.name,
    })
print('\nFetching all Users...')
for user in UsersRepository.get_all_users():
    print('Saving User: {}'.format(user.email))
    _users_and_roles['users'].append({
        'id': user.id,
        'email': user.email,
        'password': user.password,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'active': user.active,
        'role': user.role.name,
    })
print('\nSaving Roles and Users to file: {}.'.format(ROLES_AND_USERS_FILE))
with open(ROLES_AND_USERS_FILE, 'w') as json_file:
    json.dump(_users_and_roles, json_file)

# Backup all Scans and its Labels with DICOM files
_scans = {
    'datasets': [],
    'label_tags': [],
    'scans': [],
}  # type: Dict[str, List[Dict]]

print('\nFetching Datasets...')
for dataset in DatasetsRepository.get_all_datasets():
    print('Saving Dataset: {}'.format(dataset.key))
    _scans['datasets'].append({
        'id': dataset.id,
        'key': dataset.key,
        'name': dataset.name,
    })
print('\nFetching Label Tags...')
for label_tag in LabelTagsRepository.get_all_tags():
    print('Saving Label Tag: {}'.format(label_tag.key))
    _scans['label_tags'].append({
        'id': label_tag.id,
        'key': label_tag.key,
        'name': label_tag.name,
    })
print('\nSaving all DICOMs to directory...')
for scan in ScansRepository.get_all_scans():
    print('Saving Scan: {}'.format(scan.id))
    scan_directory = SCANS_DIRECTORY + str(scan.id) + '/'
    create_directory(scan_directory)

    # Save metadata to JSON file
    _scans['scans'].append({
        'id': scan.id,
        'converted': scan.converted,
        'declared_number_of_slices': scan.declared_number_of_slices,
        'dataset': scan.dataset.key,
        'owner_id': scan.owner_id,
        'slices': [{
            'id': scan_slice.id,
            'location': scan_slice.location,
            'position_x': scan_slice.position_x,
            'position_y': scan_slice.position_y,
            'position_z': scan_slice.position_z,
            'stored': scan_slice.stored,
            'converted': scan_slice.converted,
        } for scan_slice in scan.stored_slices],
    })

    # Save DICOMs to the Scan directory
    for scan_slice in scan.stored_slices:
        slice_file_name = scan_directory + str(scan_slice.id) + '.dcm'
        slice_bytes = SlicesRepository.get_slice_original_image(scan_slice.id)
        print('Saving DICOM to file: {}'.format(slice_file_name))
        with open(slice_file_name, 'wb') as slice_file:
            slice_file.write(slice_bytes)
print('\nSaving all Scans to file: {}'.format(SCANS_METADATA_FILE))
with open(SCANS_METADATA_FILE, 'w') as json_file:
    json.dump(_scans, json_file)

# Save Labels to JSON file
_labels = {
    'labels': [],
}  # type: Dict[str, List[Dict]]
print('\nFetching all Labels...')
for label in LabelsRepository.get_all_labels():
    print('Saving Label: {}'.format(label.id))
    _labels['labels'].append({
        'id': label.id,
        'scan_id': label.scan_id,
        'labeling_time': label.labeling_time,
        'status': label.status.value,
        'owner_id': label.owner_id,
    })
    for element in label.elements:
        if element.tool.value == LabelTool.RECTANGLE:
            print('Saving Rectangle Label Elements')
            _labels['labels'].append({
                'elements': {
                    'id': element.id,
                    'x': element.x,
                    'y': element.y,
                    'slice_index': element.slice_index,
                    'width': element.width,
                    'height': element.height,
                    'status': element.status.value,
                    'tag_id': element.tag_id,
                    'tool': element.tool,
                }
            })
print('\nSaving all Labels to file: {}'.format(LABELS_FILE))
with open(LABELS_FILE, 'w') as json_file:
    json.dump(_labels, json_file)

# Completed!
print('')
print('--------------------------------')
print('       BACKUP COMPLETED!        ')
print('--------------------------------')
print('                                ')
print(' Saved to: {}'.format(BACKUP_DIRECTORY))
print('                                ')
print('--------------------------------')
