from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/edit"):
                restaurantIdPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIdPath).one()

                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action ='/restaurants/%s/edit' >" %restaurantIdPath
                    output += "<input name= 'restaurant' type='text' placeholder = '%s'>" %myRestaurantQuery.name
                    output += "<input type='submit' value='Rename'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                return

            if self.path.endswith("/delete"):
                restaurantIdPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIdPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = "<html><body>"
                    output += "<h1>Are you sure want to delete %s ?" %myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action ='/restaurants/%s/delete'>" %restaurantIdPath
                    output += "<input type='submit' value='Delete'>"
                    output += "</form></body></html>"
                    self.wfile.write(output)
                    print output
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                listRestaurants = session.query(Restaurant).all()
                output = ""
                output +="<html><body>"
                output +="<h2><a href ='restaurants/new'>Make a new restaurants</a></h2>"

                for restaurant in listRestaurants:
                    output +="<h2> %s </h2>" % restaurant.name
                    output +="<p><a href='/restaurants/%s/edit'>edit</a>  <a href='/restaurants/%s/delete'>delete</a></p>" %(restaurant.id, restaurant.id)
                
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output = "<html><body>"
                output = "<h1>Create new restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name="restaurant" type="text" placeholder="New Restaurant Name"><input type="submit" value="Create"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>&#161Hola</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s " % self.path)
    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                restaurantIdPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIdPath).one()

                if myRestaurantQuery != []:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                return
            
            if self.path.endswith("/edit"):
                cype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messageContent = fields.get('restaurant')
                    restaurantIdPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIdPath).one()

                    if myRestaurantQuery != [] :
                        myRestaurantQuery.name = messageContent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                    return

            
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                newRestaurant = fields.get('restaurant')

                #Create new restaurant name
                NewRestaurant = Restaurant(name = newRestaurant[0])
                session.add(NewRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

            # output = ""
            # output += "<html><body>"

            # ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            # if ctype == 'multipart/form-data':
            #     fields = cgi.parse_multipart(self.rfile, pdict)
            #     messagecontent = fields.get('message')
                
                
            # output += "</body></html>"
            # self.wfile.write(output)
            # print output
        except:
            pass

            

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    #mapper
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
class MenuItem(Base):
    __tablename__ = 'menu_item'
    #mapper
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

    restaurant = relationship(Restaurant)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)

if __name__ == '__main__':
    main()

            