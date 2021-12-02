#Importing libraries
from settings import *
import json

#Initializing out database
db = SQLAlchemy(app)




#The class Users will inherit the db.Model of SQLAlchemy
class Users(db.Model):
    __table__name = 'users'
    id = db.Column(db.Integer, primary_key = True) #Primary key for id
    public_id = db.Column(db.String(50), unique = True)
    Name = db.Column(db.String(80), nullable = False) #the column can't be empty since nullable is false
    age = db.Column(db.Integer, nullable = False) 
    city = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(50), nullable = False)
    

    #Convert the output to json
    def json(self):
        return {'Name': self.Name, 'age': self.age, 'city': self.city, 'password': self.password}
    
    #Fuction to add user info to database
    def POST(_Name, _age, _city, _password):
        hashed_password = generate_password_hash(_password, method='sha256')
        new_user = Users(public_id = str(uuid.uuid4()), Name = _Name, age = _age, city = _city, password = hashed_password)
        db.session.add(new_user) #add new user to database session
        db.session.commit() #commit changes to session

    #Retrieve user data based on a unique ID
    def GET(_id):
        user = Users.query.filter_by(id = _id).first()
        x = {
            "Name": user.Name,
            "age" : user.age,
            "city" : user.city
        }
        y = json.dumps(x)
        return y
    
    #Update user information based on ID
    def PUT(_id, _Name, _age, _city):
        User_to_update = Users.query.filter_by(id = _id).first()
        User_to_update.Name = _Name
        User_to_update.age = _age
        User_to_update.city = _city
        db.session.commit()
    
    #Delete the user based on ID
    def DELETE(_id):
        Users.query.filter_by(id = _id).delete()
        db.session.commit()


# decorator for verifying the JWT
def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'Missing token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped

#Login Users
@app.route('/login', methods=['POST'])  
def login_user(): 
    auth = request.authorization   

    if not auth or not auth.username or not auth.password:  
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

    user = Users.query.filter_by(Name=auth.username).first()   
        
    if check_password_hash(user.password, auth.password):  
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
        return make_response(jsonify({'token' : token}), 201) 

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

