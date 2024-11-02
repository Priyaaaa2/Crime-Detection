from flask import Flask, render_template, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from datetime import datetime

app = Flask(__name__)

# Initialize a list to store data
data_list = []

def fetch_and_store_data():
    global data_list
    try:
        response = requests.get('Replace with your API URL')  
        response.raise_for_status()
        new_data = response.json()
        current_time = datetime.now().isoformat()
        
        # Create a new list with updated data
        updated_data_list = []
        for item in new_data:
            if not any(existing_item['cid'] == item['cid'] for existing_item in data_list):
                # Add new item with default assignment=False
                updated_data_list.append({
                    'cid': item['cid'],
                    'datetime': item['datetime'],
                    'assignment': False
                })
        
        # Merge with existing data
        data_list.extend(updated_data_list)
        data_list = sorted(data_list, key=lambda x: x['datetime'])
        
        print(f"Data fetched at {current_time}")
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_and_store_data, trigger="interval", seconds=10)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(data_list)

@app.route('/assign/<cid>', methods=['POST'])
def assign(cid):
    global data_list
    for item in data_list:
        if item['cid'] == cid:
            item['assignment'] = True
            break
    return jsonify({'status': 'success', 'cid': cid})

if __name__ == '__main__':
    try:
        app.run(debug=True, use_reloader=False)
    except KeyboardInterrupt:
        scheduler.shutdown()
