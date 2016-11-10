#!/usr/bin/python3
"""
Create session files and cookies for current sessions.
"""
import os
import pickle
import time
from http import cookies

from utils import generate_hash


class Session(object):
    def __init__(self):
        self.headers = dict()
        if 'HTTP_COOKIE' in os.environ.keys():
            self.cookie = cookies.SimpleCookie(os.environ['HTTP_COOKIE'])
        else:
            self.cookie = None

    def print_headers(self):
        """
        print html headers
        """

        print("Location: http://localhost/edit_profile.py")
        for k, v in self.headers.items():
            print('%s: %s;\n' % (k, v))

    def create_cookie(self, session_obj):
        """
        Create cookie for current session.
        :param session_obj: dictionary having the current user id.
        """
        if not os.path.exists('.sessions'):
            os.mkdir('.sessions')
        hash_value = generate_hash(time.time())
        self.headers['Set-Cookie'] = 'session_id=%s;expires=%s' % (hash_value, str(time.time() + (60 * 60 * 5)))
        self.print_headers()
        session_file = open(os.path.join('.sessions', hash_value), 'wb')
        pickle.dump(session_obj, session_file, 1)
        session_file.close()

    def delete_cookie(self):
        """
        Deletes the current cookie.
        """
        if 'session_id' in self.cookie.keys():
            self.cookie['session_id']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
            return self.cookie
        else:
            return False

    def current_user(self):
        """
        Fetch the current user id.
        :return: user id.
        """

        if 'HTTP_COOKIE' in os.environ.keys():
            if 'session_id' in self.cookie.keys():
                session_id = self.cookie['session_id'].value
                if os.path.exists(os.path.join('.sessions', session_id)):
                    session_file = open(os.path.join('.sessions', session_id), 'rb')
                    session_obj = pickle.load(session_file)
                    session_file.close()
                    return session_obj['userid']
        return False

    def session(self, user):
        """
        Create session.
        :param user: user id
        """

        user_id = user['id']
        current = self.current_user()
        if current:
            return current
        else:
            session_obj = dict()
            session_obj['userid'] = user_id
            self.create_cookie(session_obj)
