from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:5500", "https://my-portfilio.onrender.com"]}})

# Configuration from environment variables
app.config['POSTGRES_HOST'] = os.getenv('DB_HOST')
app.config['POSTGRES_USER'] = os.getenv('DB_USER')
app.config['POSTGRES_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['POSTGRES_DB'] = os.getenv('DB_NAME')

def connect_to_database():
    try:
        conn = psycopg2.connect(
            host=app.config['POSTGRES_HOST'],
            user=app.config['POSTGRES_USER'],
            password=app.config['POSTGRES_PASSWORD'],
            dbname=app.config['POSTGRES_DB']
        )
        return conn
    except Exception as e:
        app.logger.error(f"Database connection error: {str(e)}")
        return None

@app.route('/api', methods=["POST"])
def api():
    if request.method == "POST":
        conn = connect_to_database()
        if not conn:
            return jsonify({'error': 'Database connection error'}), 500
        
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM projects')  
            data = cur.fetchall()
            cur.close()
            conn.close()

            # Structure data into JSON format
            json_data = []
            for item in data:
                json_data.append({
                    'Id': item[0],
                    'Title': item[1],
                    'Description': item[2],
                    'GithubLink': item[3],
                    'WebsiteLink': item[4]
                })

            return jsonify(json_data)

        except Exception as e:
            app.logger.error(f"Query execution error: {str(e)}")
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Method not allowed'}), 405

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
