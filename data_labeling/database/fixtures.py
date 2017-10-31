"""Insert all database fixtures"""
from sqlalchemy import exists

from data_labeling.database import db_session
from data_labeling.database.models import ScanCategory


CATEGORIES = [{
    'key': 'KIDNEYS',
    'name': 'Nerki',
    'image_path': '../../../assets/icon/kidneys_category_icon.svg',
}, {
    'key': 'LIVER',
    'name': 'Wątroba',
    'image_path': '../../../assets/icon/liver_category_icon.svg',
}, {
    'key': 'HEART',
    'name': 'Serce',
    'image_path': '../../../assets/icon/heart_category_icon.svg',
}, {
    'key': 'LUNGS',
    'name': 'Płuca',
    'image_path': '../../../assets/icon/lungs_category_icon.svg',
}]


def insert_scan_categories() -> None:
    """Insert all default Scan Categories if don't exist"""
    with db_session() as session:
        for row in CATEGORIES:
            category_key = row.get('key', '')
            category_exists = session.query(exists().where(ScanCategory.key == category_key)).scalar()
            if category_exists:
                print('Scan Category exists with key "{}"'.format(category_key))
                continue

            category = ScanCategory(**row)
            session.add(category)
            print('Scan Category added for key "{}"'.format(category_key))


if __name__ == '__main__':
    print('Applying fixtures for Scan Categories...')
    insert_scan_categories()
