from flask import Flask, request, jsonify, make_response
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from marshmallow import fields
import os
# fofofof

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Zcrs1225@127.0.0.1:3306/ninja_dojo'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app)


###User Model & Routes####
class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(100))
    username = db.Column(db.String(20))
    password = db.Column(db.String)
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    def __init__(self,name,email,username,password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
    def __repr__(self):
        return '' % self.id
db.create_all()

class userSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = User
        sqla_session = db.session
    user_id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)


@app.route('/users', methods = ['GET'])
def index():
    get_users = User.query.all()
    user_schema = userSchema(many=True)
    users = user_schema.dump(get_users)
    return make_response(jsonify({"user": users}))


@app.route('/user/<id>', methods = ['GET'])
def get_user_by_id(id):
    get_user = User.query.get(id)
    user_schema = userSchema()
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user": user}))


@app.route('/add/user', methods = ['POST'])
def create_user():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be in JSON format')

    post_data = request.get_json()
    name = post_data.get("name")    
    email = post_data.get("email")    
    username = post_data.get("username")    
    password = post_data.get("password")    


    possible_duplicate = db.session.query(User).filter(User.username == username).first()

    if possible_duplicate is not None:
        return jsonify("Error: the username you've entered has already been taken")


    encrypted_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(name, email, username, encrypted_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify("user has been added.") 



@app.route("/user/verify", methods=["POST"])
def verify_user():
    print(request.content_type)
    if request.content_type != "application/json":
        return jsonify("Error: Data must be in JSON format")
    
    user_data = request.get_json()
    username = user_data.get("username")    
    password = user_data.get("password") 

    user = db.session.query(User).filter(User.username == username).first()

    if user is None:
        return jsonify("User NOT verified")

    if bcrypt.check_password_hash(user.password, password) == False:
        return jsonify("User NOT verified")
        
    return jsonify("User has been verified")


@app.route('/user/<id>', methods = ['PUT'])
def update_user_by_id(id):
    data = request.get_json()
    get_user = User.query.get(id)
    if data.get('name'):
        get_user.name = data['name']
    if data.get('email'):
        get_user.email = data['email']
    if data.get('username'):
        get_user.username = data['username']
    if data.get('password'):
        get_user.password= data['password']    
    db.session.add(get_user)
    db.session.commit()
    user_schema = userSchema(only=['user_id', 'name', 'email','username','passwrod'])
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user": user}))


@app.route('/users/<id>', methods = ['DELETE'])
def delete_user_by_id(id):
    get_user = user.query.get(user_id)
    db.session.delete(get_user)
    db.session.commit()
    return make_response("",204)


###NinjaCard Model & Routes####
class NinjaCard(db.Model):
    __tablename__ = "ninja_card"
    ninjacard_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    dojo = db.Column(db.String(20))
    rank = db.Column(db.String(20))
    health = db.Column(db.Integer)
    ability1 = db.Column(db.String(40))
    ability1_value = db.Column(db.Integer)
    ability2 = db.Column(db.String(40))
    ability2_value = db.Column(db.Integer)
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    def __init__(self, name, dojo, rank, health, ability1, ability1_value, ability2, ability2_value):
        self.name = name
        self.dojo = dojo
        self.rank = rank
        self.health = health
        self.ability1 = ability1
        self.ability1_value = ability1_value
        self.ability2 = ability2
        self.ability2_value = ability2_value
    def __repr__(self):
        return '' % self.ninjacard_id
db.create_all()

class ninjacardSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = NinjaCard
        sqla_session = db.session
    card_id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    dojo = fields.String(required=False)
    rank = fields.String(required=False)
    health = fields.String(required=False)
    ability1 = fields.String(required=True)
    ability1_value = fields.Number(required=False)
    ability2 = fields.String(required=True)
    ability2_value = fields.Number(required=False)

@app.route('/ninjacards', methods = ['GET'])
def get_all_ninjacards():
    get_ninjacards = NinjaCard.query.all()
    ninjacard_schema = ninjacardSchema(many=True)
    ninjacards = ninjacard_schema.dump(get_ninjacards)
    return make_response(jsonify({"ninjacard": ninjacards}))


@app.route('/ninjacard/<id>', methods = ['GET'])
def get_ninjacard_by_id(id):
    get_ninjacard = NinjaCard.query.get(id)
    ninjacard_schema = ninjacardSchema()
    ninjacard = ninjacard_schema.dump(get_ninjacard)
    return make_response(jsonify({"ninjacard": ninjacard}))


@app.route('/add/ninjacard', methods = ['POST'])
def create_ninjacard():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be in JSON format')

    post_data = request.get_json()
    name = post_data.get("name")    
    dojo = post_data.get("dojo")    
    rank = post_data.get("rank")    
    health = post_data.get("health")    
    ability1 = post_data.get("ability1")    
    ability1_value = post_data.get("ability1_value")    
    ability2 = post_data.get("ability2")    
    ability2_value = post_data.get("ability2_value")    


    possible_duplicate = db.session.query(NinjaCard).filter(NinjaCard.name == name).first()

    if possible_duplicate is not None:
        return jsonify("Error: the Name you've entered has already been taken")


    new_ninjacard = NinjaCard(name, dojo, rank, health, ability1, ability1_value, ability2, ability2_value)
    db.session.add(new_ninjacard)
    db.session.commit()

    return jsonify("Your Ninja Card has been added!") 


if __name__ == "__main__":
    app.run(debug=True)
