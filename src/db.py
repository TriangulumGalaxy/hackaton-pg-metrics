import json

DATA_FILE = "data.json"


def get_data():
    with open(DATA_FILE) as f:
        data = f.read()
    return json.loads(data)

def add_admin(admin: int | str):
    data = get_data()
    data['admins'].append(int(admin))
    with open(DATA_FILE, 'w') as f:
        f.write(json.dumps(data))

def add_banned_query(query: str):
    data = get_data()
    data['banned_queries'].append(query)
    with open(DATA_FILE, 'w') as f:
        f.write(json.dumps(data))

def delete_admin(admin: int | str):
    data = get_data()
    if admin in data['admins']:
        data['admins'].remove(admin)
        return True
    return False
