#!/usr/bin/python3
import os
import pickle
import hashlib
import time
from http import cookies


def print_headers(headers):
    print("Location: http://localhost/edit_profile.py")
    for k, v in headers.items():
        print('%s: %s;\n' % (k, v))

if not os.path.exists('.sessions'):
    os.mkdir('.sessions')


def create_cookie(session_obj):
    headers = {}
    hash_value = hashlib.new('ripemd160', str(time.time()).encode()).hexdigest()
    headers['Set-Cookie'] = 'session_id=%s;expires=%s' % (hash_value, str(time.time() + (60 * 60 * 5)))
    print_headers(headers)
    session_file = open(os.path.join('.sessions', hash_value), 'wb')
    pickle.dump(session_obj, session_file, 1)
    session_file.close()


def delete_cookie():
    c = cookies.SimpleCookie(os.environ['HTTP_COOKIE'])
    if 'session_id' in c.keys():
        c['session_id']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
        return c
    else:
        return False


def current_user():
    if 'HTTP_COOKIE' in os.environ.keys():
        c = cookies.SimpleCookie(os.environ['HTTP_COOKIE'])
        if 'session_id' in c.keys():
            session_id = c['session_id'].value
            if os.path.exists(os.path.join('.sessions', session_id)):
                session_file = open(os.path.join('.sessions', session_id), 'rb')
                session_obj = pickle.load(session_file)
                session_file.close()
                return session_obj['userid']
    return False


def session(user):
    user_id = user['id']
    current = current_user()
    if current:
        return current
    else:
        session_obj = dict()
        session_obj['userid'] = user_id
        create_cookie(session_obj)
