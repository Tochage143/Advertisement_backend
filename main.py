from flask import Flask, abort, jsonify, request, make_response
from bs4 import BeautifulSoup
import json
import requests
import base64

app = Flask(__name__)
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
}
searchurl = "https://zollege.in/global-search?page_type=in&countryId=2&term="
collegeurl = "https://zollege.in/web-api/"


@app.route('/')
def index():
  return 'Welcome to Advertisement backend boys'


# This the search route and  take search input like college name and return college information like id
@app.route('/search')
def Search():
  search = request.args.get('q')
  try:
    res = requests.get(searchurl + search, headers=headers)
    if res.status_code == 200:
      resdata = json.loads(res.text)
      result = resdata["output"]
      if result is not None:
        newdata = []
        for x in result:
          if x["item_type"] == "college":
            newdata.append(x)
        return jsonify(newdata)
      return jsonify(result)
    else:
      return abort(404)
  except Exception as e:
    return make_response(jsonify({'error': str(e)}), 500)


# This the college route and take college id and return college information
@app.route('/college')
def College():
  id = request.args.get("id", default=None)
  if id is None:
    return make_response(jsonify({'error': 'please enter the id'}), 500)
  try:
    res = requests.get(collegeurl + id, headers=headers)
    if res.status_code == 200:
      return jsonify(res.json())
    else:
      return abort(404)
  except Exception as e:
    return make_response(jsonify({'error': str(e)}), 500)


# The collge route and take college id and return college information
@app.route('/college_name')
def College_name():
  name = request.args.get("name", default=None)
  if name is None:
    return make_response(
        jsonify({'error': 'please enter the the college name '}), 500)
  try:
    if name != '':
      res = requests.get(searchurl + name, headers=headers)
      if res.status_code == 200:
        resdata = json.loads(res.text)
        result = resdata["output"]
        if result is not None:
          if len(result) > 1:
            return jsonify([])
          url = result[0]["url"]
          res = requests.get(collegeurl + url, headers=headers)
          if res.status_code == 200:
            returndata = json.loads(res.text)
            return jsonify(returndata)
          else:
            return jsonify([])
        else:
          return jsonify([])
  except Exception as e:
    return make_response(jsonify({'error': str(e)}), 500)


@app.route('/college_list/<string:list_url>')
def college_list(list_url):
  page = request.args.get('page', default=0)
  list_id = request.args.get('id', default='None')
  if list_id is None:
    return make_response(jsonify({"error": "please give the id "}))
  try:
    encoded_string = encoded(list_url, list_id, page)
    res = requests.get(f'{collegeurl}listing?data={encoded_string}',
                       headers=headers)
    if res.status_code == 200:
      return jsonify(res.json())
    else:
      return make_response(jsonify({'error': "There is the problem "}), 500)
  except Exception as e:
    return make_response(jsonify({'error': str(e)}, 500), )


# This function use for encoding json data into a string
def encoded(url, list_id, page=0):
  data = {"url": url, "stream": list_id, "page": page}
  json_string = json.dumps(data)
  encoded_bytes = base64.b64encode(json_string.encode('utf-8'))
  encoded_string = encoded_bytes.decode('utf-8')
  return encoded_string


# This is the news for show latest news it take two queries first news_type and page number
@app.route('/news')
def News():
  news_type = request.args.get('news_type', default='news')
  # There are news types of [news,college,admission,exam]
  page = request.args.get('page', default=1)
  try:
    if news_type == 'news':
      res = requests.get(f"{collegeurl}news/page-{page}", headers=headers)
      if res.status_code == 200:
        return jsonify(res.json())
      else:
        return make_response(jsonify({'error': "There is the problem "}), 500)
    else:
      news_route = "exams"
      if news_route is news_type:
        news_route = "exams"
        news_type = "news"
      res = requests.get(f"{collegeurl}{news_route}/{news_type}/page-{page}",
                         headers=headers)
      if res.status_code == 200:
        return jsonify(res.json())
      else:
        return make_response(jsonify({'error': "There is the problem "}), 500)
  except Exception as e:
    return make_response(jsonify({'error': str(e)}, 500), )


# Route is exams give the lastest exam information
@app.route('/exams')
def Exams():
  try:
    res = requests.get("https://zollege.in/napi/c/nge/exams/", headers=headers)
    if res.status_code == 200:
      return jsonify(res.json())
    else:
      return make_response(jsonify({'error': "There is the problem "}), 500)
  except Exception as e:
    return make_response(jsonify({'error': str(e)}, 500), )


@app.route('/streams')
def Streams():
  try:
    res = requests.get("https://zollege.in/", headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    tag = soup.find('div',
                    class_='slick-slider custom-primary slick-initialized')
    print(tag)
    if res.status_code == 200:
      return 'ok'
    else:
      return make_response(jsonify({'error': "There is the problem "}), 500)
  except Exception as e:
    return make_response(jsonify({'error': str(e)}, 500), )


app.run(host='0.0.0.0', port=81, debug=True)
