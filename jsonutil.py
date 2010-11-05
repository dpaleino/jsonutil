#!/usr/bin/python
# -*- coding: utf-8 -*-

# © 2010, David Paleino <d.paleino@gmail.com>

import cjson
import sys

global original

def main():
    global original
    json = eval(''.join(open(sys.argv[1])))
    original = json

    cmd = sys.argv[2]
    path = sys.argv[3]
    value = sys.argv[4]
    force = False

    if cmd == 'get':
        print get(json, path)
    elif cmd == 'typeof':
        print typeof(json, path)
    elif cmd == 'set':
        print set_value(json, path, value, force)
    elif cmd == 'len':
        print get_len(json, path)

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

def typeof(json, path):
    strippath = path[1:]
    newpath = None
    if '/' in strippath:
        key, newpath = strippath.split('/', 1)
        newpath = '/'+newpath
    else:
        key = strippath

    if key == '':
        return str(type(json))

    if type(json) == list:
        if newpath:
            return typeof(json[int(key)], newpath)
        else:
            return str(type(json[int(key)]))
    if type(json) == dict:
        if newpath:
            return typeof(json[key], newpath)
        else:
            return str(type(json[key]))
    elif type(json) in [str, int, float]:
        return str(type(json))

def set_value(json, path, value, force=False):
    strippath = path[1:]
    newpath = None
    if '/' in strippath:
        key, newpath = strippath.split('/', 1)
        newpath = '/'+newpath
    else:
        key = strippath

    if key == '':
        return 'Unsupported.'

    if type(json) == list:
        if newpath:
            return set_value(json[int(key)], newpath, value)
        else:
            if type(json[int(key)]) in [list, dict]:
                return 'Not setting the value, please use --force.'
            else:
                json[int(key)] = value
                return original
    if type(json) == dict:
        if newpath:
            return set_value(json[key], newpath, value)
        else:
            if type(json[key]) in [list, dict]:
                return 'Not setting the value, please use --force.'
            else:
                json[key] = value
                return original
    elif type(json) in [str, int, float]:
        json = value
        return original

def get_len(json, path):
    strippath = path[1:]
    newpath = None
    if '/' in strippath:
        key, newpath = strippath.split('/', 1)
        newpath = '/'+newpath
    else:
        key = strippath

    if key == '':
        try:
            return len(json)
        except TypeError, e:
            return 'Unsupported, ' + e.args[0]

    if type(json) == list:
        if newpath:
            return get_len(json[int(key)], newpath)
        else:
            try:
                return len(json[int(key)])
            except TypeError, e:
                return 'Unsupported, ' + e.args[0]
    if type(json) == dict:
        if newpath:
            return get_len(json[key], newpath, value)
        else:
            try:
                return len(json[key])
            except TypeError, e:
                return 'Unsupported, ' + e.args[0]

    try:
        return len(json)
    except TypeError, e:
        return 'Unsupported, ' + e.args[0]

if __name__ == '__main__':
    main()
