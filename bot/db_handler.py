import json
import os

DB_FILE = "bot/data/db.json"
DB_DIR = "bot/data"

# Initialize JSON database
def init_db():
    # Ensure the data directory exists
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    # Create db.json if it doesn't exist
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as db_file:
            json.dump({"users": []}, db_file)  # Create an empty users list

# Load the entire database
def load_db():
    with open(DB_FILE, 'r') as db_file:
        return json.load(db_file)

# Save changes to the database
def save_db(data):
    with open(DB_FILE, 'w') as db_file:
        json.dump(data, db_file, indent=4)

# Add or update user in JSON database
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
            "referrals": 0
        })

    save_db(data)

# Update referral count for a user
def update_referrals(user_id):
    data = load_db()
    for user in data['users']:
        if user['user_id'] == user_id:
            user['referrals'] += 1
            break

    save_db(data)

# Get user data from the database
def get_user_data(user_id):
    data = load_db()
    for user in data['users']:
        if user['user_id'] == user_id:
            return user['referrals']
    return 0  # Default to 0 referrals if user not found

# Get user ID by username
def get_user_id_by_username(username):
    data = load_db()
    for user in data['users']:
        if user['username'] == username:
            return user['user_id']
    return None
