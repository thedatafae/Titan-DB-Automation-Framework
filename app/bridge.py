from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'titan_retail'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/execute', methods=['POST'])
def execute_single_query():
    """Endpoint for basic CRUD and Schema Validation tests."""
    data = request.json
    query = data.get('query')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        
        if query.strip().upper().startswith("SELECT"):
            result = cursor.fetchall()
        else:
            conn.commit()
            result = {"status": "success", "affected_rows": cursor.rowcount}
            
        cursor.close()
        conn.close()
        return jsonify(result), 200

    except mysql.connector.Error as err:
        # Professional SQA Error Mapping
        return jsonify({
            "status": "fail",
            "error_code": err.errno,
            "sql_state": err.sqlstate,
            "message": err.msg
        }), 400

@app.route('/transaction', methods=['POST'])
def execute_transaction():
    """Endpoint to test ACID properties (Atomicity)."""
    data = request.json
    queries = data.get('queries') # Expects a list of queries
    
    conn = get_db_connection()
    conn.autocommit = False # Start Transaction
    cursor = conn.cursor()
    
    try:
        for q in queries:
            cursor.execute(q)
        
        conn.commit() # Commit all if all succeed
        return jsonify({"status": "Transaction Committed"}), 200
        
    except mysql.connector.Error as err:
        conn.rollback() # ACID: Rollback if ANY query fails
        return jsonify({
            "status": "Transaction Rolled Back",
            "reason": err.msg,
            "error_code": err.errno
        }), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)