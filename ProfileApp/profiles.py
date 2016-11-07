#!/usr/bin/python3

import os

if os.environ['REQUEST_METHOD'] == 'GET':
    print("Content-type: text/html")
    print('')
    f = open('./template/profiles.html')
    print(f.read())
    f.close()
