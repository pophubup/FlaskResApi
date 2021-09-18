from flask import Flask, jsonify,make_response
from flask_cors import CORS, cross_origin
from flask_restx import Resource, Api, fields
from utils import DATOInforLoader
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app, version='1.0', title='WebCrawling',
    description='Crawling everyWhere For Fun',)



ns = api.namespace('DATO', description='DATO 遊戲者戰績')
MY_MODEL = ns.model("Result",
    {
        "page": fields.String(example="some string"),
        "result": fields.List(fields.String)
    },
)
@cross_origin()
@ns.route('/Dato/<string:name>')
class DATO(Resource):
    @ns.param('name', '玩家名稱')
    @ns.response(404, '找不到此玩家')
    @ns.response(200, "OK", MY_MODEL) 
    def get(self, name):
        status_code, result= DATOInforLoader(name, r'C:\Users\Yohoo\Desktop\myAllTest\zWebCrawlingRepository\pys\data.json', 5).DataAsJsonData()
        return make_response(jsonify(result),status_code)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

