#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web, logging as log, pprint, json, db
from api import *
import traceback

f=pprint.pformat

files = {}

class Router(object):
    def POST(self, uri):
        if uri == 'api':
            try:
                print web.data()
                json_data = json.loads(web.data())
            except Exception, e:
                traceback.print_exc()
                raise web.badrequest()
            
            try:
                return json.dumps(API().serve(json_data))
            except Exception, e:
                traceback.print_exc()
                raise web.internalerror(e.message)
        else:
            raise web.notfound()
    
    def GET(self, uri):
        dirs = uri.split('/')
        if dirs[0] in ['', 'js', 'css', 'img', 'donate', 'index2.html', 'favicon.ico']:
            filename = uri
            if dirs[0] == '':
                filename = 'index.html'
            try:
                with open(filename) as staticfile:
                    filecontent = staticfile.read()
                    files[filename] = filecontent
                    return filecontent
            except IOError, e:
                if e.errno == 2:
                    raise web.notfound()
            if files.has_key(filename):
                return files[filename]
            else:
                try:
                    with open(filename) as staticfile:
                        filecontent = staticfile.read()
                        files[filename] = filecontent
                        return filecontent
                except IOError, e:
                    if e.errno == 2:
                        raise web.notfound()
        else:
            raise web.notfound()

urls = (
    "/(.*)", Router
)

app = web.application(urls, globals())

#log.basicConfig(level=log.DEBUG, filename='webm.log')
#log.basicConfig(level=log.DEBUG)
if __name__ == "__main__":
    try:
      db.select_tasks(id=1)
    except:
      db.reset_database()
    API().download_last()
    try:
      app.run()
    except:
      print "timeout"
      pass
    
