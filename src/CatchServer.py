#!/usr/bin/python

import os
localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

import cherrypy
import json

from pymongo import Connection
connection = Connection()

db = connection.cleanstreets
picdb = db.pic

class FileDemo(object):

    def index(self):
        return """
        <html><body>
            <h2>Upload a file</h2>
            <form action="upload" method="post" enctype="multipart/form-data">
            filename: <input type="file" name="myFile" /><br />
            <input type="submit" />
            </form>
        </body></html>
        """
    index.exposed = True

    def upload(self, myFile):
        out = """<html>
        <body>
            myFile length: %s<br />
            myFile filename: %s<br />
            myFile mime-type: %s
        </body>
        </html>"""

        print myFile

         ##we still need to parse location
        loc=[50,50]
        ##define a placekeeper name
        placekeeper='placekeeper'
        ##place in the DB object and the the DB ID back
        someIDobect=picdb.insert({"filename" : placekeeper, "loc" : loc})
        ##Define the filename as the object ID
        filename=str(someIDobect)
        filenameDB=filename+".jpg"
        ##Update the filename as the DB object
        picdb.update( { "_id":someIDobect}, { "$set" : { "filename" :  filenameDB}} );
        cherrypy.response.headers['Content-Type'] = 'text/javascript'




        try:
            os.mkdir ("Images")
        except Exception: 
            pass
        f = open("Images/%s" % filename, "w")

        # Although this just counts the file length, it demonstrates
        # how to read large files in chunks instead of all at once.
        # CherryPy reads the uploaded file into a temporary file;
        # myFile.file.read reads from that.
        size = 0
        while True:
            data = myFile.file.read(8192)
            if not data:
                break
            size += len(data)
            f.write(data)

        print "Read file %d bytes" % size
        return out % (size, myFile.filename, myFile.content_type)
    upload.exposed = True



tutconf = os.path.join(os.path.dirname(__file__), 'CatchServer.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(FileDemo(), config=tutconf)
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(FileDemo(), config=tutconf)
