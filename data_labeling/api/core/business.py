"""Module responsible for business logic in all Core endpoint"""
from typing import Dict


def success() -> Dict[str, bool]:
    """Return dictionary successfully

    :return: dictionary with key 'success' and value 'True'
    """
    return {
        'success': True,
    }
