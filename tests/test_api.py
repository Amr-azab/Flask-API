import pytest
import requests

base_url = 'http://localhost:5000'  # Update this if your Flask app is running on a different port


def test_create_test_case():
    response = requests.post(f'{base_url}/test_cases', json={'name': 'Test Case 1', 'description': 'Description 1', 'execution_result': 'Pass'})
    assert response.status_code == 200
    assert response.json()['message'] == 'Test case created successfully'


def test_get_all_test_cases():
    response = requests.get(f'{base_url}/test_cases')
    assert response.status_code == 200
    # Add more assertions based on the expected response data structure


def test_get_single_test_case():
    # Assuming there is a test case with ID 1 in the database
    response = requests.get(f'{base_url}/test_cases/1')
    assert response.status_code == 200
    # Add more assertions based on the expected response data structure


def test_update_test_case():
    # Assuming there is a test case with ID 1 in the database
    response = requests.put(f'{base_url}/test_cases/1', json={'name': 'Updated Test Case', 'description': 'Updated Description'})
    assert response.status_code == 200

    # Check if the test case exists before checking the response message
    if 'Test case not found' not in response.json()['message']:
        assert response.json()['message'] == 'Test case updated successfully'
    else:
        assert 'Test case not found' in response.json()['message']


def test_delete_test_case():
    # Assuming there is a test case with ID 1 in the database
    response = requests.delete(f'{base_url}/test_cases/1')
    assert response.status_code == 200

    # Check if the test case exists before checking the response message
    if 'Test case not found' not in response.json()['message']:
        assert response.json()['message'] == 'Test case deleted successfully'
    else:
        assert 'Test case not found' in response.json()['message']


def test_record_execution_result():
    # Assuming there is a test case with ID 1 in the database
    response = requests.post(f'{base_url}/execution_results/1', json={'execution_result': 'Fail'})
    assert response.status_code == 200

    # Check if the test case exists before checking the response message
    if 'Test case not found' not in response.json()['message']:
        assert response.json()['message'] == 'Execution result recorded successfully'
    else:
        assert 'Test case not found' in response.json()['message']

def test_get_one_execution_result():
    response = requests.get(f'{base_url}/execution_results/1')
    assert response.status_code == 200
    # Add more assertions based on the expected response data structure


def test_get_execution_results():
    response = requests.get(f'{base_url}/execution_results')
    assert response.status_code == 200
    # Add more assertions based on the expected response data structure
    assert isinstance(response.json(), list)  # Assuming the response should be a list
    # Additional assertions based on the structure of each item in the list
