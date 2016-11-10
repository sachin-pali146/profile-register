#!/usr/bin/python3
"""
Logout the current user and redirect them to login page
"""
try:
    import cgi
    import cgitb
    import os

    from session import Session
    from utils import create_log, show_404

    cgitb.enable()
    form = cgi.FieldStorage()
    session = Session()
    user = session.current_user()

    if user:
        if os.environ['REQUEST_METHOD'] == 'GET':
            logout = session.delete_cookie()
            if logout:
                print(logout)
            print("Location: http://localhost/login.py\n")
    else:
        print("Location: http://localhost/login.py\n")
except Exception as e:
    create_log("Logout.py : "+str(e))
    show_404()
