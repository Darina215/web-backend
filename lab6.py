from flask import Blueprint, render_template, request, session, current_app
from os import path
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

lab6 = Blueprint('lab6', __name__)

def db_connect():
    if current_app.config.get('DB_TYPE') == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='darina_redkacheva_knowledge_base',
            user='darina_redkacheva_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def get_all_offices():
    conn, cur = db_connect()
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT number, tenant, price FROM offices ORDER BY number")
        else:
            cur.execute("SELECT number, tenant, price FROM offices ORDER BY number")
        
        offices = cur.fetchall()
        
        # Преобразуем в список словарей для совместимости
        result = []
        for office in offices:
            if hasattr(office, '__getitem__'):
                result.append({
                    'number': office['number'],
                    'tenant': office['tenant'] or '',  
                    'price': office['price']
                })
            else:
                result.append({
                    'number': office[0],
                    'tenant': office[1] or '', 
                    'price': office[2]
                })
        return result
    except Exception as e:
        print(f"Error getting offices: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def update_office_tenant(office_number, tenant):
    conn, cur = db_connect()
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute(
                "UPDATE offices SET tenant = %s WHERE number = %s",
                (tenant, office_number)
            )
        else:
            cur.execute(
                "UPDATE offices SET tenant = ? WHERE number = ?",
                (tenant, office_number)
            )
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"Error updating office tenant: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def get_office_by_number(office_number):
    conn, cur = db_connect()
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute(
                "SELECT number, tenant, price FROM offices WHERE number = %s",
                (office_number,)
            )
        else:
            cur.execute(
                "SELECT number, tenant, price FROM offices WHERE number = ?",
                (office_number,)
            )
        
        office = cur.fetchone()
        if office:
            if hasattr(office, '__getitem__'):
                return {
                    'number': office['number'],
                    'tenant': office['tenant'] or '', 
                    'price': office['price']
                }
            else:
                return {
                    'number': office[0],
                    'tenant': office[1] or '', 
                    'price': office[2]
                }
        return None
    
    except Exception as e:
        print(f"Error getting office: {e}")
        return None
    finally:
        cur.close()
        conn.close()

@lab6.route('/lab6/')
def main():
    login = session.get('login')
    return render_template('lab6/lab6.html', login=login)

@lab6.route('/lab6/json-rpc-api/', methods = ['POST'])
def api():
    data = request.json
    print(f"DEBUG: Received request: {data}") 
    id = data['id']

    if data['method'] == 'info':
        offices = get_all_offices()
        print(f"DEBUG: Returning offices: {offices}")
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }
    
    if data['method'] == 'booking':
        office_number = data['params']
        office = get_office_by_number(office_number)
        
        if not office:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Office not found'
                },
                'id': id
            }
        
        if office['tenant'] != '':
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Already booked'
                },
                'id': id
            }
        
        if update_office_tenant(office_number, login):
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            }
        else:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32000,
                    'message': 'Database error'
                },
                'id': id
            }
    
    if data['method'] == 'cancellation':
        office_number = data['params']
        office = get_office_by_number(office_number)
        
        if not office:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Office not found'
                },
                'id': id
            }
        
        if office['tenant'] == '':
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Office is not booked'
                },
                'id': id
            }
        
        if office['tenant'] != login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'You are not the tenant of this office'
                },
                'id': id
            }
        
        if update_office_tenant(office_number, ''):
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            }
        else:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32000,
                    'message': 'Database error'
                },
                'id': id
            }

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }