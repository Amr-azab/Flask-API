from flask import jsonify
from flask_restful import Resource, reqparse
import sqlite3
from app import app, api

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


execution_result_parser = reqparse.RequestParser()
execution_result_parser.add_argument('execution_result', type=str)

class TestCaseResource(Resource):
    def get(self, test_case_id):
        if not self.test_case_exists(test_case_id):
            return jsonify({'message': 'Test case not found'})
        conn = sqlite3.connect('test_cases.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_cases WHERE id=?", (test_case_id,))
        test_case = cursor.fetchone()
        conn.close()

        if test_case:
            return jsonify({'id': test_case[0], 'name': test_case[1], 'description': test_case[2]})
        else:
            return jsonify({'message': 'Test case not found'}), 404

    def put(self, test_case_id):
        args = parser.parse_args()
        if not self.test_case_exists(test_case_id):
            return jsonify({'message': 'Test case not found'})
        conn = sqlite3.connect('test_cases.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("UPDATE test_cases SET name=?, description=? WHERE id=?",
                       (args['name'], args['description'], test_case_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Test case updated successfully'})

    def delete(self, test_case_id):
        if not self.test_case_exists(test_case_id):
            return jsonify({'message': 'Test case not found'})
        conn = sqlite3.connect('test_cases.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM test_cases WHERE id=?", (test_case_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Test case deleted successfully'})
    
    # Helper method to check if the test case exists
    def test_case_exists(self, test_case_id):
        conn = sqlite3.connect('test_cases.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_cases WHERE id=?", (test_case_id,))
        test_case = cursor.fetchone()
        conn.close()
        return test_case is not None


class TestCaseListResource(Resource):
    def get(self):
        conn = sqlite3.connect('test_cases.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_cases")
        test_cases = cursor.fetchall()
        conn.close()
        test_cases_list = [{'id': row[0], 'name': row[1], 'description': row[2]} for row in test_cases]
        return jsonify(test_cases_list)

    def post(self):
        args = parser.parse_args()
        # Data validation for required fields
        if not args['name'] or not args['description']:
            return jsonify({'message': 'Name and description are required'})
        conn = sqlite3.connect('test_cases.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO test_cases (name, description) VALUES (?, ?)",
                       (args['name'], args['description']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Test case created successfully'})


class ExecutionResultResource(Resource):
    def get(self, test_asset_id):
        # Check if the test case exists
        if not self.test_case_exists(test_asset_id):
            return jsonify({'message': 'Test case not found'})

        conn = sqlite3.connect('test_cases.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_cases WHERE id=?", (test_asset_id,))
        test_case = cursor.fetchone()
        conn.close()

        if test_case:
            response_data = {'id': test_case[0], 'name': test_case[1], 'description': test_case[2], 'execution_result': test_case[3]}
            return jsonify(response_data)
        else:
            return jsonify({'message': 'Test case not found'})

    def post(self, test_asset_id):
        args = execution_result_parser.parse_args(strict=True)
        conn = sqlite3.connect('test_cases.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_cases WHERE id=?", (test_asset_id,))
        test_case = cursor.fetchone()

        if test_case:
            cursor.execute("UPDATE test_cases SET execution_result=? WHERE id=?", (args['execution_result'], test_asset_id))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Execution result recorded successfully'})
        else:
            conn.close()
            return jsonify({'message': 'Test case not found'})

    # Helper method to check if the test case exists
    def test_case_exists(self, test_case_id):
        conn = sqlite3.connect('test_cases.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_cases WHERE id=?", (test_case_id,))
        test_case = cursor.fetchone()
        conn.close()
        return test_case is not None


class ExecutionResultList(Resource):
    def get(self):
        # Fetch all test cases
        conn = sqlite3.connect('test_cases.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_cases")
        test_cases = cursor.fetchall()
        conn.close()

        # Create a list of response data for each test case
        response_data_list = []
        for test_case in test_cases:
            response_data = {'id': test_case[0], 'name': test_case[1], 'description': test_case[2], 'execution_result': test_case[3]}
            response_data_list.append(response_data)

        return jsonify(response_data_list)


# Add resources to the API
api.add_resource(TestCaseListResource, '/test_cases')
api.add_resource(TestCaseResource, '/test_cases/<int:test_case_id>')
api.add_resource(ExecutionResultResource, '/execution_results/<int:test_asset_id>')
api.add_resource(ExecutionResultList, '/execution_results')
