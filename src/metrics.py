import psycopg2
from dataclasses import dataclass

def get_metrics(dbname: str, user: str, password: str):
    # Connect to your postgres DB
    conn = psycopg2.connect(f"dbname={dbname} user={user} password={password}")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    cur.execute("SELECT datid, datname, pid, leader_pid, usesysid, usename, application_name, client_addr,client_hostname, client_port, backend_start, xact_start, query_start, state_change, wait_event_type, wait_event, state, backend_xid, backend_xmin, query_id, query, backend_type  FROM pg_stat_activity")

    # Retrieve query results
    res = cur.fetchall()
    r = []
    for records in res:
        r.append({
        "datid": records[0],
        "datname": records[1],
        "pid": records[2],
        "leader_pid": records[3],
        "usesysid": records[4],
        "usename": records[5],
        "application_name": records[6],
        "client_addr": records[7],
        "client_hostname": records[8],
        "client_port": records[9], 
        "backend_start": records[10],
        "xact_start": records[11],
        "query_start": records[12],
        "state_change": records[13],
        "wait_event_type": records[14],
        "wait_event": records[15],
        "state": records[16],
        "backend_xid": records[17],
        "backend_xmin": records[18],
        "query_id": records[19],
        "query": records[20],
        "backend_type": records[21]
        })
    conn.close()
    return r

def get_queries(dbname: str, user: str, password: str):
    # Connect to your postgres DB
    conn = psycopg2.connect(f"dbname={dbname} user={user} password={password}")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    cur.execute("SELECT query FROM pg_stat_activity")

    # Retrieve query results
    records = cur.fetchall()
    conn.close()
    return records

def get_long_queries(dbname: str, user: str, password: str):
    conn = psycopg2.connect(f"dbname={dbname} user={user} password={password}")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    cur.execute("SELECT current_timestamp - query_start as runtime, datname, usename, query FROM pg_stat_activity WHERE state != 'idle' ORDER BY 1 desc;")

    # Retrieve query results
    records = cur.fetchall()
    
    conn.close()
    return records