#!/usr/bin/python
# -*- coding: utf-8 -*-

# © 2010, David Paleino <d.paleino@gmail.com>

import cjson
import sys

original = None

def main(filename, path, cmd, force, value=None):
    global original
    original = cjson.decode(open(filename).read())

    if cmd == 'get':
        return get(original, path)
    elif cmd == 'typeof':
        return typeof(original, path)
    elif cmd == 'set':
        return set_value(original, path, value, force)
    elif cmd == 'len':
        return get_len(original, path)
    elif cmd == 'keys':
        return get_keys(original, path)

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

def get_keys(json, path):
    def ret(arg):
        try:
            return arg.keys()
        except AttributeError, e:
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
            return set_value(json[int(key)], newpath, value, force)
        else:
            if type(json[int(key)]) in [list, dict] and not force:
                return 'Not setting the value, please use --force.'

            json[int(key)] = value
            return original
    if type(json) == dict:
        if newpath:
            return set_value(json[key], newpath, value, force)
        else:
            if type(json[key]) in [list, dict] and not force:
                return 'Not setting the value, please use --force.'

            json[key] = value
            return original
    elif type(json) in [str, int, float]:
        json = value
        return original

if __name__ == '__main__':
    from optparse import OptionParser
    import pprint

    parser = OptionParser(usage='Usage: %prog [command [arguments]] file.json /path/', version='%prog 0.1', prog='jsonutil')
    parser.set_defaults(verbose=True)

    parser.add_option('-g', '--get', action='store_const', const='get', dest='cmd', default='get',
                      help='get the value of the element at the given path. This is the default action if no command is given.')
    parser.add_option('-s', '--set', action='store', dest='set', metavar='VALUE',
                      help='set the value of the element at the given path to VALUE. The json will not be written in-place,'+
                      'you should use something like sponge(1).')
    parser.add_option('-l', '--length', action='store_const', const='len', dest='cmd',
                      help='get the length of the element at the given path.')
    parser.add_option('-t', '--type', action='store_const', const='typeof', dest='cmd',
                      help='get the type of the element pointed by the given path.')
    parser.add_option('-f', '--force', action='store_true', dest='force', default=False,
                      help='force the setting of a value, even if it overwrites a different type of element.')
    parser.add_option('-k', '--keys', action='store_const', const='keys', dest='cmd',
                      help='lists the keys of the element pointed by the given path.')

    opts, args = parser.parse_args()

    # handle -s/--set
    value = None
    if opts.set:
        opts.cmd = 'set'
        value = opts.set

    if not args:
        parser.error('need a JSON file and a path.')
    else:
        filename = args[0]
        path = args[1]

    ret = main(filename, path, opts.cmd, opts.force, value)
    pprint.pprint(ret, width=20)
