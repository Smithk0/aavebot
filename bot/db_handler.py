import json
import os

DB_FILE = "data/db.json"
DB_DIR = "data"

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as db_file:
            json.dump({"users": []}, db_file)

def load_db():
    with open(DB_FILE, 'r') as db_file:
        return json.load(db_file)

def save_db(data):
    with open(DB_FILE, 'w') as db_file:
        json.dump(data, db_file, indent=4)

def add_or_update_user(user_id, username):
    data = load_db()
    user_found = False

    for user in data['users']:
        if user['user_id'] == user_id:
            user['username'] = username
            user_found = True
            break
    
    if not user_found:
        data['users'].append({
            "user_id": user_id,
            "username": username,
            "referrals": 0,
            "referred_users": []
        })

    save_db(data)

def update_referrals(user_id, referred_user):
    data = load_db()
    for user in data['users']:
        if user['user_id'] == user_id:
            user['referrals'] += 1
            user['referred_users'].append(referred_user)
            break

    save_db(data)

def get_user_data(user_id):
    data = load_db()
    for user in data['users']:
        if user['user_id'] == user_id:
            return user
    return {"referrals": 0, "referred_users": []}

def get_referred_users(user_id):
    user = get_user_data(user_id)
    return user['referred_users']
