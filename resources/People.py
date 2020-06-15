from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query

class Ppl(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('pId',type=int,required=True,help="pId cannot be left blank")
        data=parser.parse_args()
        try:
            return query(f"""select * from restapi.People where pId={data['pId']};""")
        except:
            return {"message":"THERE WAS AN ERROR CONNECTING TO PEOPLE TABLE"},500
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('pId',type=str,required=True,help="pId cannot be left empty")
        parser.add_argument('pname',type=str,required=True,help="pname cannot be left empty")
        parser.add_argument('ptype',type=str,required=True,help="ptype cannot be left empty")
        parser.add_argument('pass',type=str,required=True,help="pass cannot be left empty")
        data=parser.parse_args()
        try:
            x=query(f"""select * from restapi.People where pId={data['pId']}""",return_json=False)
            if len(x)>0: return{"message":"user with that id already exists."},400
        except:
            return{"message":"there was an error inserting into table."},500
        try:
            query(f"""insert into restapi.People values({data['pId']},
                                                        '{data['pname']}',
                                                        '{data['ptype']}',
                                                        '{data['pass']}')""")
            return{"message":"Successfully inserted"},201
        except:
            return {"message":"THERE WAS AN ERROR INSERTING INTO PEOPLE"},500

class User():
    def __init__(self,pId,pname,password):
        self.pId=pId
        self.pname=pname
        self.password=password

    @classmethod
    def getUserBypId(cls,pId):
        result=query(f"""select pId,pname,pass from restapi.People where pId='{pId}'""",return_json=False)
        if len(result)>0: return User(result[0]['pId'],result[0]['pname'],result[0]['pass'])
        return none

    @classmethod
    def getUserBypname(cls,pname):
        result=query(f"""select pId,pname,pass from restapi.People where pname='{pname}'""",return_json=False)
        if len(result)>0: return User(result[0]['pId'],result[0]['pname'],result[0]['pass'])
        return none

class PplLogin(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('pname',type=str,required=True,help="pId cannot be left blank")
        parser.add_argument('pass',type=str,required=True,help="pass cannot be left blank")
        data=parser.parse_args()
        user=User.getUserBypname(data['pname'])
        if user and safe_str_cmp(user.password,data['pass']):
            access_token=create_access_token(identity=user.pId,expires_delta=False)
            return{'access_token':access_token},200
        return{"message":"Invalid Credentials"},401
