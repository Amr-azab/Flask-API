import pytest
import requests

base_url = 'http://localhost:5000'

def test_create_test_case():
    response = requests.post(f'{base_url}/test_cases', json={'name': 'Test Case 1', 'description': 'Description 1'})
    assert response.status_code == 200
    assert response.json()['message'] == 'Test case created successfully'

def test_get_all_test_cases():
    response = requests.get(f'{base_url}/test_cases')
    assert response.status_code == 200
    

def test_get_single_test_case():
    # Assuming there is no test case with ID 1 in the database
    response = requests.get(f'{base_url}/test_cases/1')
    if response.status_code == 404:
        assert 'Test case not found' in response.json()['message']
    


def test_update_test_case():
    # Assuming there is no test case with ID 1 in the database
    response = requests.put(f'{base_url}/test_cases/1', json={'name': 'Updated Test Case', 'description': 'Updated Description'})
    if response.status_code == 404:
        assert 'Test case not found' in response.json()['message']

def test_delete_test_case():
    # Assuming there is no test case with ID 1 in the database
    response = requests.delete(f'{base_url}/test_cases/1')
    if response.status_code == 404:
        assert 'Test case not found' in response.json()['message']

def test_record_execution_result():
    # Assuming there is no test case with ID 1 in the database
    response = requests.post(f'{base_url}/execution_results/1', json={'execution_result': 'Fail'})
    if response.status_code == 404:
        assert 'Test case not found' in response.json()['message']

def test_get_one_execution_result():
    # Assuming there is no test case with ID 1 in the database
    response = requests.get(f'{base_url}/execution_results/1')
    if response.status_code == 404:
        assert 'Test case not found' in response.json()['message']


def test_get_execution_results():
    response = requests.get(f'{base_url}/execution_results')
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Assuming the response should be a list
    # Additional assertions based on the structure of each item in the list
