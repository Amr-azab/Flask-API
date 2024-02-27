from flask import jsonify, request
from flask_restful import reqparse
import sqlite3
from app import app

# Set up SQLite database and create tables
conn = sqlite3.connect('test_cases.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        execution_result TEXT
    )
''')
conn.commit()

# Request parser for parsing JSON data in requests
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name is required')
parser.add_argument('description', type=str, required=True, help='Description is required')
parser.add_argument('execution_result', type=str)
parser.add_argument('test_case_id', type=int)



# Helper methods
def test_case_exists(test_case_id):
    conn = sqlite3.connect('test_cases.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_cases WHERE id=?", (test_case_id,))
    test_case = cursor.fetchone()
    conn.close()
    return test_case is not None

def get_all_test_cases():
    conn = sqlite3.connect('test_cases.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_cases")
    test_cases = cursor.fetchall()
    conn.close()
    return [{'id': row[0], 'name': row[1], 'description': row[2]} for row in test_cases]

def create_test_case():
    args = request.get_json()
    if not args['name'] or not args['description']:
        return jsonify({'message': 'Name and description are required'}), 400
    conn = sqlite3.connect('test_cases.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test_cases (name, description) VALUES (?, ?)",
                   (args['name'], args['description']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Test case created successfully'}), 200

def get_test_case(test_case_id):
    if not test_case_exists(test_case_id):
        return jsonify({'message': 'Test case not found'}), 404
    conn = sqlite3.connect('test_cases.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_cases WHERE id=?", (test_case_id,))
    test_case = cursor.fetchone()
    conn.close()
    return jsonify({'id': test_case[0], 'name': test_case[1], 'description': test_case[2]}), 200

def update_test_case(test_case_id):
    args = request.get_json()
    if not test_case_exists(test_case_id):
        return jsonify({'message': 'Test case not found'}), 404
    conn = sqlite3.connect('test_cases.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("UPDATE test_cases SET name=?, description=? WHERE id=?",
                   (args['name'], args['description'], test_case_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Test case updated successfully'}), 200

def delete_test_case(test_case_id):
    if not test_case_exists(test_case_id):
        return jsonify({'message': 'Test case not found'}), 404
    conn = sqlite3.connect('test_cases.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM test_cases WHERE id=?", (test_case_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Test case deleted successfully'}), 200

def get_execution_result(test_asset_id):
    if not test_case_exists(test_asset_id):
        return jsonify({'message': 'Test case not found'}), 404
    conn = sqlite3.connect('test_cases.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_cases WHERE id=?", (test_asset_id,))
    test_case = cursor.fetchone()
    conn.close()
    return jsonify({'id': test_case[0], 'name': test_case[1], 'description': test_case[2], 'execution_result': test_case[3]}), 200

def record_execution_result(test_asset_id):
    args = request.get_json()
    if not test_case_exists(test_asset_id):
        return jsonify({'message': 'Test case not found'}), 404
    conn = sqlite3.connect('test_cases.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("UPDATE test_cases SET execution_result=? WHERE id=?", (args['execution_result'], test_asset_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Execution result recorded successfully'}), 200

def get_execution_results():
    conn = sqlite3.connect('test_cases.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_cases")
    test_cases = cursor.fetchall()
    conn.close()
    response_data_list = [{'id': row[0], 'name': row[1], 'description': row[2], 'execution_result': row[3]} for row in test_cases]
    return jsonify(response_data_list), 200

# Decorator-style routes
@app.route('/test_cases', methods=['GET', 'POST'])
def test_cases_route():
    if request.method == 'GET':
        return jsonify(get_all_test_cases())
    elif request.method == 'POST':
        return create_test_case()

@app.route('/test_cases/<int:test_case_id>', methods=['GET', 'PUT', 'DELETE'])
def test_case_route(test_case_id):
    if request.method == 'GET':
        return get_test_case(test_case_id)
    elif request.method == 'PUT':
        return update_test_case(test_case_id)
    elif request.method == 'DELETE':
        return delete_test_case(test_case_id)

@app.route('/execution_results/<int:test_asset_id>', methods=['GET', 'POST'])
def execution_result_route(test_asset_id):
    if request.method == 'GET':
        return get_execution_result(test_asset_id)
    elif request.method == 'POST':
        return record_execution_result(test_asset_id)

@app.route('/execution_results', methods=['GET'])
def execution_results_list_route():
    return get_execution_results()
