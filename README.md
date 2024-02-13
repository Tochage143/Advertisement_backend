# College Backend API

Welcome to the my Api API. This API provides information about colleges, news, exams, and more.

## Routes

### 1. Welcome Route

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Returns a welcome message.

### Example:
```bash
"http://localhost:81/" 
```

### 2. Home

- **Endpoint:** `/Home`
- **Method:** `GET`
- **Description:** This return home page data like top cities, top exam , etch 

### Example:
```bash
"http://localhost:81/Home" 
```


### 3. Search

- **Endpoint:** `/search`
- **Method:** `GET`
- **Parameters:**
  - `q` (string): College name for searching.
- **Description:** Returns information about colleges based on the search query.

### Example:
```bash
"http://localhost:81/search?q=deogiri college" 
```
### 4. College 

- **Endpoint:** `/college`
- **Method:** `GET`
- **Parameters:**
  - `id` (string): This take the id (string) of the college
- **Description:** Returns a the college information

### Example
```bash
"http://localhost:81/college?id=college/160338-deogiri-college-aurangabad"
```


### 5. College Name
#### **Note:** `Do not use this route because it only returns results when college is correct and accurate.` 

- **Endpoint:** `/college_name`
- **Method:** `GET`
- **Parameters:**
  - `name` (string): Returns information about a specific college based on the provided name.

### Example
```bash
"http://localhost:81/college_name?name=diems deogiri institute of engineering and management studies maharashtra aurangabad home"
```

### 6. College List

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

### 7. News

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

### 8. Exams

- **Endpoint:**  `/exams/id`
- **Method:** GET
- **Parameters:**
    - `exam_tabs`(string) : take the exam tabs url and return the exam data 
- **Description:** Returns information about the latest exams and also return exam list 
### Example
```bash
"http://localhost:81/exams/exams/iiad-entrance-exam?exam_tabs=syllabus"
```
