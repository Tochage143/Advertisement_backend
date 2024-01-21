# College Backend API

Welcome to the my Api API. This API provides information about colleges, news, exams, and more.

## Routes

### 1. Home

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Returns a welcome message.

### Example:
```bash
"http://localhost:81/" 
```
### 2. Search

- **Endpoint:** `/search`
- **Method:** `GET`
- **Parameters:**
  - `q` (string): College name for searching.
- **Description:** Returns information about colleges based on the search query.

### Example:
```bash
"http://localhost:81/search?q=deogiri college" 
```
### 3. College 

- **Endpoint:** `/`
- **Method:** `GET`
- **Parameters:**
  - `id` (string): This take the id (string) of the college
- **Description:** Returns a the college information

### Example
```bash
"http://localhost:81/college?id=college/160338-deogiri-college-aurangabad"
```


### 4. College Name
#### **Note:** `Do not use this route because it only returns results when college is correct and accurate.` 

- **Endpoint:** `/college_name`
- **Method:** `GET`
- **Parameters:**
  - `name` (string): Returns information about a specific college based on the provided name.

### Example
```bash
"http://localhost:81/college_name?name=diems deogiri institute of engineering and management studies maharashtra aurangabad home"
```

### 5. College List

- **Endpoint:** `/college_list/<string:list_url>`
- **Method:** `GET`
- **Parameters:**
    - `page` (int) : Page number (optional, default: 0).
    - `id` (string) : College ID for the list.
- **Description:**  Returns a list of colleges based on the provided URL and ID.

### Example
```bash
"http://localhost:81/college_list/management-colleges?id=13&page=1"
```

### 6. News

- **Endpoint:**  `/news`
- **Method:** GET
- **Parameters:**
  - `news_type`(string) : Type of news (options:college, admission, exam; default: news).
  - `page` (int): Page number (default: 1).
- **Description:** Returns the latest news.

### Example
```bash
"http://localhost:81/news?new_type=college&page=2"
```

### 7. Exams

- **Endpoint:**  `/news`
- **Method:** GET
- **Description:** Returns information about the latest exams.

### Example
```bash
"http://localhost:81/exams"
```

