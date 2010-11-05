#!/usr/bin/python
# -*- coding: utf-8 -*-

# © 2010, David Paleino <d.paleino@gmail.com>

import cjson
import sys

def main():
    json = eval(''.join(open(sys.argv[1])))
    original = json

    cmd = sys.argv[2]
    path = sys.argv[3]

    if cmd == 'get':
        print get(json, path)

def get(json, path):
    strippath = path[1:]
    newpath = None
    if '/' in strippath:
        key, newpath = strippath.split('/', 1)
        newpath = '/'+newpath
    else:
        key = strippath

    if key == '':
        return json

    if type(json) == list:
        if newpath:
            return get(json[int(key)], newpath)
        else:
            return json[int(key)]
    if type(json) == dict:
        if newpath:
            return get(json[key], newpath)
        else:
            return json[key]
    elif type(json) in [str, int, float]:
        return json

if __name__ == '__main__':
    main()
