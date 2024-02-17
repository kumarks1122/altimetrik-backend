from flask import Flask, request, jsonify
import json
import os
import uuid

app = Flask(__name__)

# Load customer data from JSON file
DB_FILE = "db.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            return json.load(file)
    else:
        return []

def update_db(customers):
    with open(DB_FILE, "w") as file:
        json.dump(customers, file, indent=4)

@app.route('/customer/new', methods=['POST'])
def register_new_customer():
    data = request.json
    db = load_db()
    data['id'] = str(uuid.uuid4())
    db["customers"].append(data)
    update_db(db)
    return jsonify({"message": "Customer registered successfully"}), 200

@app.route('/customer/upgrade-plan', methods=['POST'])
def upgrade_plan():
    data = request.json
    customer_id = data.get('customer_id')
    plan_name = data.get('plan_name')
    plan_cost = data.get('plan_cost')
    validity = data.get('validity')
    plan_status = data.get('plan_status')

    db = load_db()
    for customer in db['customers']:
        if customer.get('id') == customer_id:
            customer['plan_name'] = plan_name
            customer['plan_cost'] = plan_cost
            customer['validity'] = validity
            customer['plan_status'] = plan_status
            break
      
    update_db(db)
    return jsonify({"message": f"Plan upgraded for customer {customer_id}"}), 200

@app.route('/customers', methods=['GET'])
def list_customers():
    customers = load_db()
    return jsonify(customers), 200

if __name__ == '__main__':
    app.run(debug=True)
