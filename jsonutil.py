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

def _loop(fn, json, path):
    stripped = path[1:]
    newpath = None
    if '/' in stripped:
        key, newpath = stripped.split('/', 1)
        newpath = '/'+newpath
    else:
        key = stripped

    if key:
        if type(json) == list:
            if newpath:
                return _loop(fn, json[int(key)], newpath)
            else:
                return fn(json[int(key)])
        if type(json) == dict:
            if newpath:
                return _loop(fn, json[key], newpath)
            else:
                return fn(json[key])
    return fn(json)

def get(json, path):
    def ret(arg):
        return arg
    return _loop(ret, json, path)

def typeof(json, path):
    def ret(arg):
        return str(type(arg))
    return _loop(ret, json, path)

def get_len(json, path):
    def ret(arg):
        try:
            return len(arg)
        except TypeError, e:
            return 'Unsupported, ' + e.args[0]

    return _loop(ret, json, path)

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

if __name__ == '__main__':
    main()
