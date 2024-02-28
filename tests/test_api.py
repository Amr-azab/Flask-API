import pytest
import requests

base_url = 'http://localhost:5000'

def test_create_test_case():
    # create test (name , description)
    response = requests.post(f'{base_url}/test_cases', json={'name': 'Advertisements', 'description': 'Advertisements about project'})
    assert response.status_code == 200
    assert response.json()['message'] == 'Test case created successfully'

def test_get_all_test_cases():
    # get all test 
    response = requests.get(f'{base_url}/test_cases')
    assert response.status_code == 200
    

def test_get_single_test_case():
    # get single test by id 
    response = requests.get(f'{base_url}/test_cases/1')
    if response.status_code == 404:
        assert 'Test case not found' in response.json()['message']
    


def test_update_test_case():
    # update the test (name , description) by id
    response = requests.put(f'{base_url}/test_cases/1', json={'name': 'Updated Test Case', 'description': 'Updated Description'})
    if response.status_code == 404:
        assert 'Test case not found' in response.json()['message']

def test_delete_test_case():
    # delete the test by id
    response = requests.delete(f'{base_url}/test_cases/1')
    if response.status_code == 404:
        assert 'Test case not found' in response.json()['message']

def test_record_execution_result():
    # record execution result the test by id
    response = requests.post(f'{base_url}/execution_results/9', json={'execution_result': 'passed'})
    if response.status_code == 404:
        assert 'Test case not found' in response.json()['message']

def test_get_one_execution_result():
    # get one execution result the test by id
    response = requests.get(f'{base_url}/execution_results/1')
    if response.status_code == 404:
        assert 'Test case not found' in response.json()['message']


def test_get_execution_results():
    response = requests.get(f'{base_url}/execution_results')
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Assuming the response should be a list
    # Additional assertions based on the structure of each item in the list

# you can fill the data in sqlite , can retrive the data , update and delete the data 
# run the code (run.py)    
# select the unit test you want (get , delete , post , put) and write  pytest tests/test_api.py  in git bash 
# write sqlite3 test_cases.db  in git bash 
# and write SELECT * FROM test_cases;  
# you will see the all the data (id , name , description , execution result)    