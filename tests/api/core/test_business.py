"""Unit tests for data_labeling/api/core/business.py"""
from data_labeling.api.core.business import success


def test_success() -> None:
    """Check if method used by status endpoint returns dictionary {success: True}"""
    response = success()
    assert isinstance(response, dict)
    assert response['success']
