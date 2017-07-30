#!/usr/bin/env python
"""
Very simple HTTP server in python.

Usage::
    ./kylie.py [<port>]

Send a GET request::
    curl http://localhost

Send a HEAD request::
    curl -I http://localhost

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

"""


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import json
import MySQLdb
import random

class Serve(BaseHTTPRequestHandler):
    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self.host = ""
        self.name = ""
        self.user = ""
        self.password = ""
        
        get_data = urlparse.parse_qs(self.path)
        
        try:
            data = {"tag": get_data['tag'][0], "city": get_data['city'][0]}
        except (KeyError):
            data = {"tag": "Yoga", "city": "Brisbane"}
        
        try:
            cnxn = MySQLdb.connect(host=self.host, db=self.name, user=self.user, passwd=self.password)
        except MySQLdb.OperationalError as e:
            print(MySQLdb.OperationalError("Error: Failure connecting to DataBase. MySQLdb raised this error {0}".format(e)))

        cursor = cnxn.cursor()
                
        # Example command        
        #sqlCmd = ('SELECT Title,Description,StartDate,EndDate,CouncilWebsite '
        #          'FROM govhack2017.Events '
        #          'WHERE City = "Brisbane" and EventTag = "Fitness"')
        
        cursor.execute("""SELECT Title,Description,StartDate,EndDate,CouncilWebsite 
                  FROM govhack2017.Events 
                  WHERE City = %s and EventTag = %s""", (data["city"], data["tag"]))
        rows = cursor.fetchall()
        
        cursor.close()
        cnxn.close() 
                
        if rows:
            row = rows[random.randrange(len(rows))]
        else:
            row = None
                
        if row is None:
            message = {"title": "none", "description": "none", "start": "none", "finish": "none", "web": "none"}
            message_json = json.dumps(message)
        else:
            start_time = row[2].strftime("%A, %d. %B %I:%M%p")
            finish_time = row[3].strftime("%A, %d. %B %I:%M%p")
            
            title_msg = unicode(row[0], errors='ignore')
            description_msg = unicode(row[1], errors='ignore')
            website_msg = unicode(row[4], errors='ignore')
            
            message = {"title": title_msg, "description": description_msg, "start": start_time, "finish": finish_time, "web": website_msg}
            
            message_json = json.dumps(message)
                    
        self._set_headers()
        self.wfile.write(message_json)
        

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=Serve, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()


