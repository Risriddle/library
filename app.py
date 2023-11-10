from flask_restful import Resource, Api
from flask import render_template
from flask import *
from pymongo import MongoClient
import random
import re
import os

# Retrieve MongoDB connection string from environment variable
connection_string = os.environ.get("MONGODB_CONNECTION_STRING")

# Check if the connection string is available
if connection_string is None:
    raise ValueError("MongoDB connection string not found in environment variables")

# Create MongoClient
client = MongoClient(connection_string)


db = client["Library"]  #name of DB
collection = db["members_info"] # name of collection

app = Flask(__name__)
api = Api(app)

 

class index(Resource):
    def get(self):
        return make_response(render_template("home.html"))
        #return make_response(render_template('index.html'))



class Home(Resource):
    def get(self):
        return make_response(render_template('home.html'))
    def post(self):
        return make_response(render_template('home.html'))



class Membership(Resource):
    def get(self):
        return make_response(render_template('membership.html'))
    def post(self):
        return make_response(render_template('membership.html'))
        

class Member(Resource):
    def get(self):
        return make_response(render_template('member.html'))
    def post(self):
        name =request.form.get('name')
        pwd=request.form.get('pwd')
        def validate_password():
          # define our regex pattern for validation
          pattern = "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
          # We use the re.match function to test the password against the pattern
          match = re.match(pattern, pwd)
          # return True if the password matches the pattern, False otherwise
          return bool(match)
        validate_password()
        mid=random.randint(2000,6000)  
        dict = {"name":name,"pwd":pwd,"mid":mid}
        
        
        collection.insert_one(dict)
        print("-------------------------------")
        print("Data store to db")
        #collection.dict.find_one_and_update({'email':email},{"$set":{'mid':mid}}) # updating but not providing the new document.it gives back the old document
        print(dict)
       # if name in dict.values() and email in dict.values() and number in dict.values() and address in dict.values() and pwd in dict.values():
        d=collection.find_one_and_delete({"name":{"$exists": True, "$eq" : ""}})
        h=collection.find_one_and_delete({"pwd":{"$exists": True, "$eq" : ""}})
        if validate_password():
         if collection.find_one({"mid":mid}):
          return make_response(render_template('membership.html',mid=mid))
         else:
            enter="ENTER VALUES IN ALL FIELDS"
            return make_response(render_template('membership.html',enter=enter))
        else:
            collection.find_one_and_delete({"mid":mid})
            display="ENTER PASSWORD IN CORRECT FORMAT"
            return make_response(render_template('membership.html',display=display))


class Download(Resource):
    def get(self):
        return make_response(render_template('download.html'))
    def post(self):
      mid= int(request.form.get('mid'))
      pwd=request.form.get('pwd')
      data=collection.find_one({"pwd":pwd,"mid":mid},{"_id":0})
      print("-------------------------------")
      if data !=None and mid == data['mid'] and pwd ==data['pwd']:
        print(" Member confirmed--------------------------------")
        member="YOUR MEMBERSHIP HAS BEEN VERIFIED ACCESS SERVICES THROUGH MID"
        return make_response(render_template('download.html',member=member))
      else:
       print("wrong pass")
       dis="INCORRECT ID OR PASSWORD"     
       return make_response(render_template('membership.html',dis=dis)) 

        

class Thriller(Resource):
    def get(self):
        return make_response(render_template('thriller.html'))
    def post(self):
            return make_response(render_template('thriller.html'))


class Romance(Resource):
    def get(self):
        return make_response(render_template('romance.html'))
    def post(self):
        return make_response(render_template('romance.html'))



class Sci_fi(Resource):
    def get(self):
        return make_response(render_template('sci-fi.html'))
    def post(self):
        return make_response(render_template('sci-fi.html'))


class Search(Resource):
    def get(self):
        return make_response(render_template('search.html'))
    def post(self):
        collection=db["books"]
        book=str(request.form.get('search'))
        find=collection.find_one({'book':book},{"_id":0})
        print(find)
        #print(find['book'])
        if find!=None and book==find['book']:
         msg=" IS AVAILABLE"
         m=" "
         return make_response(render_template('search.html',book=book,msg=msg,m=m))     
        else:
            m="BOOK UNAVAILABLE"
            return make_response(render_template('search.html',m=m))


class search_access(Resource):
    def get(self):
        return make_response(render_template('searchbook.html'))
    def post(self):
        collection=db['books']
        book=str(request.form.get('book'))
        #print(book)
        mid=int(request.form.get('mid'))
        find=collection.find_one({'book':book},{"_id":0})
        #print(find)
        pdf=find['pdf']
        #print(pdf)
        c=db['members']
        d=c.find_one({'mid':mid})
        #print(d)
        a="ACCESS GRANTED"
        if d!=None and mid==d['mid']:
            return make_response(render_template('searchbook.html',a=a,book=book,pdf=pdf))
        else:
            msg="INVALID MEMBERSHIP ID"
            return make_response(render_template('membership.html',msg=msg))


          
class Access(Resource):
    def get(self):
        return make_response(render_template('access.html'))
    def post(self):
        mid=int(request.form.get('mid'))
        d=collection.find_one({'mid':mid})
        a="ACCESS GRANTED"
        if d!=None and mid==d['mid']:
            book=request.form.getlist('book')
            b=', '.join(book)
            print(book)
            return make_response(render_template('load.html',a=a,book=b))
        else:
            return make_response(render_template('membership.html'))
    
    
class All(Resource):
    def get(self):
        return make_response(render_template('access.html'))

     



api.add_resource(index, '/',methods=['GET','POST'])  
api.add_resource(Home, '/home/',methods=['GET','POST']) 
api.add_resource(Download, '/download',methods=['GET','POST']) 
api.add_resource(All, '/access',methods=['GET'])
api.add_resource(Thriller, '/thriller',methods=['GET','POST'])
api.add_resource(Romance, '/romance',methods=['GET','POST'])
api.add_resource(Sci_fi, '/sci-fi',methods=['GET','POST'])
api.add_resource(Access, '/access',methods=['GET','POST'])
api.add_resource(search_access, '/searchbook',methods=['GET','POST'])
api.add_resource(Membership, '/membership',methods=['GET','POST'])
api.add_resource(Search, '/search',methods=['GET','POST'])
api.add_resource(Member ,'/member',methods=['GET','POST'])

if __name__ == '__main__':
    obj=Member()
    app.run(debug=True)  
