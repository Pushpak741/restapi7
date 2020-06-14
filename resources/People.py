from flask_restful import Resource,reqparse
from db import query

class Ppl(Resource):
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('pId',type=int,required=True,help="pId cannot be left blank")
        data=parser.parse_args()
        try:
            return query(f"""select * from restapi.People where pId={data['pId']};""")
        except:
            return {"message":"THERE WAS AN ERROR CONNECTING TO PEOPLE TABLE"},500
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
