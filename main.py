from flask import Flask, abort, jsonify, request, make_response
from bs4 import BeautifulSoup
import json
import requests
import base64
from flask_cors import CORS
import urllib.parse

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
}
searchurl = "https://zollege.in/global-search?page_type=in&countryId=2&term="
collegeurl = "https://zollege.in/web-api/"
collegemainurl = 'https://zollege.in/'


@app.route('/')
def index():
  return 'Welcome to Advertisement backend boys'


@app.route('/Home')
def Home():
  try:
    res = requests.get(collegemainurl, headers=headers)
    if res.status_code == 200:
      soup = BeautifulSoup(res.text, 'html.parser')
      Top_college_tag = soup.find(
          'div', class_='slick-slider custom-primary slick-initialized')
      Top_college_parent_tag = Top_college_tag.find('div',
                                                    class_='slick-track')
      Top_college_child_tag = Top_college_parent_tag.find_all(
          'div', class_='slick-slide')
      Top_college = []
      for item in Top_college_child_tag:
        a_tag = item.find('a')
        svg = item.find('svg')
        link = a_tag.get('href')
        name = a_tag.get_text()
        data = {
            "img": str(svg),
            'link': link,
            'name': name,
        }
        Top_college.append(data)
      return make_response(jsonify(Top_college), 200)
      Strict_data = soup.find('script', id="__NEXT_DATA__")
      return 'Ok'
    else:
      return make_response(jsonify([]), 200)
  except Exception as e:
    return make_response(jsonify({'error': str(e)}), 500)


# This the search route and  take search input like college name and return college information like id
@app.route('/search')
def Search():
  search = request.args.get('q', default=None)
  if search is None:
    return make_response(jsonify({'messages': 'please give ther query'}), 500)
  try:
    res = requests.get(searchurl + search, headers=headers)
    if res.status_code == 200:
      return make_response(jsonify(res.json()), 200)
    else:
      return make_response(jsonify({'error': 'not found'}), 404)
  except Exception as e:
    return make_response(jsonify({'error': str(e)}), 500)


# This the college route and take college id and return college information
@app.route('/college')
def College():
  id = request.args.get("id")
  if id is None:
    return make_response(jsonify({'error': 'please enter the id'}), 400)

  try:
    res = requests.get(collegeurl + id, headers=headers)
    if res.status_code == 200:
      data = res.json()
      status = data.get("status")
      if status == 301:
        new_id = data["target"].replace('https://zollege.in/', '')
        res = requests.get(collegeurl + new_id, headers=headers)
        if res.status_code == 200:
          returndata = res.json()
          return jsonify(returndata)
        else:
          return make_response(jsonify({'error': 'not found'}), 404)
      else:
        return jsonify(data)
    else:
      return make_response(jsonify({'error': 'not found'}), 404)
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


@app.route('/college_list/<path:list_url>')
def college_list(list_url):
  page = request.args.get('page', default=0)
  list_id = request.args.get('id', default='None')
  decoded_url = urllib.parse.unquote(list_url)
  if list_id is None:
    return make_response(jsonify({"error": "please give the id "}))
  try:
    encoded_string = encoded(decoded_url, list_id, page)
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
  data = {"url": url, "page": page}
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


@app.route('/exams/<path:exam_url>')
def Exams(exam_url):
  try:
    decoded_url = urllib.parse.unquote(exam_url)
    exam_tabs = request.args.get('exam_tabs', default=None)
    if exam_tabs is None:
      res = requests.get(f"https://zollege.in/napi/c/nge/{decoded_url}",
                         headers=headers)
      if res.status_code == 200:
        return jsonify(res.json())
      else:
        return make_response(jsonify({'error': "There is the problem "}), 500)
    else:
      res = requests.get(
          f"https://zollege.in/napi/c/nge/{decoded_url}/{exam_tabs}",
          headers=headers)
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


@app.route('/course/<path:course_id>')
def Courses(course_id):
  try:
    decoded_url = urllib.parse.unquote(course_id).replace('courses/', '')

    res = requests.get(f"https://zollege.in/web-api/courses/{decoded_url}",
                       headers=headers)
    if res.status_code == 200:
      return jsonify(res.json())
    else:
      return make_response(jsonify({'error': "There is the problem "}), 500)
  except Exception as e:
    return make_response(jsonify({'error': str(e)}, 500), )


def encode_data(json_Data):
  json_string = json.dumps(json_Data)
  encoded_bytes = base64.b64encode(json_string.encode('utf-8'))
  encoded_string = encoded_bytes.decode('utf-8')
  return encoded_string


@app.route('/filterurl', methods=['POST'])
def Filterurl():
  try:
    # request_data = { "stream": "3", "course_tag_id": "12", "state": "10" }
    request_data = request.json
    encode_string = encode_data(request_data)
    res = requests.get(
        f"https://zollege.in/web-api/listing-url?data={encode_string}",
        headers=headers)
    if res.status_code == 200:
      return res.json()
    else:
      return make_response(
          jsonify({'error': 'Invalid request data. URL missing.'}), 400)
  except Exception as e:
    return make_response(jsonify({'error': str(e)}), 500)


@app.route('/filter/<path:Filter_id>')
def Filter(Filter_id):
  try:
    decoded_url = urllib.parse.unquote(Filter_id)
    filter_encoded_string = encode_data({'url': decoded_url})
    res = requests.get(
        f"https://zollege.in/web-api/listing-filters?data={filter_encoded_string}",
        headers=headers)
    if res.status_code == 200:
      return res.json()
    else:
      return make_response(
          jsonify({'error': 'there is problem with the api '}), 500)
  except Exception as e:
    return make_response(jsonify({'error': str(e)}), 500)


app.run(host='0.0.0.0', port=81, debug=False)
