from flask import Flask,abort,jsonify,request,render_template
from bs4 import BeautifulSoup
import json
import requests

app = Flask(__name__)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
}
searchurl="https://zollege.in/global-search?page_type=in&countryId=2&term="
collegeurl="https://zollege.in/web-api/"
@app.route('/')
def index():
    return 'Welcome to Advertisement backend boys'

@app.route('/search')
def Search():
    search = request.args.get('q')
    try :
        res=requests.get(searchurl+search,headers=headers)
        if res.status_code == 200:
            resdata=json.loads(res.text)
            result=resdata["output"]
            if result is not None:
                newdata=[]
                for x in result:
                    if  x["item_type"]=="college":
                        newdata.append(x)
                return jsonify(newdata)
            return jsonify(result)
        else:
            return abort(404)
    except Exception as e:
        return abort(503)

@app.route('/college')
def College():
    id=request.args.get("id")
    try :
        res=requests.get(collegeurl+id,headers=headers)
        if res.status_code == 200:
            returndata=json.loads(res.text)
            return jsonify(returndata)
        else:
            return abort(404)
    except Exception as e:
        return abort(503)

@app.route('/college_name')
def College_name():
    name=request.args.get("name",default="")
    if name == '':
        return jsonify({"error":"Please enter the college name"})
    try :
        if name != '':
            res=requests.get(searchurl+name,headers=headers)
            if res.status_code == 200:
                resdata=json.loads(res.text)
                result=resdata["output"]
                if result is not None:
                    if len(result) > 1:
                        return jsonify([])
                    url=result[0]["url"]
                    res=requests.get(collegeurl+url,headers=headers)
                    if res.status_code == 200:
                        returndata=json.loads(res.text)
                        return jsonify(returndata)
                    else :
                        return jsonify([])
                else :
                    return jsonify([])
    except Exception as e:
        return abort(503)
        
app.run(host='0.0.0.0', port=81,debug=True)
