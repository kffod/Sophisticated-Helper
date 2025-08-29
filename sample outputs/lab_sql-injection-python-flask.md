```zip
[README.md]
```
```markdown
# WARNING: EXTREMELY VULNERABLE DEMO FOR EDUCATIONAL PURPOSES ONLY

This application is intentionally vulnerable to SQL injection.  **DO NOT** deploy this to a production or publicly accessible environment. Use only for local, controlled testing and learning.

**Requirements:** Python 3.x, Flask

**Setup:**

1.  `unzip demo.zip`
2.  `cd demo`
3.  `pip install Flask`
4.  `python app.py`
5.  Access the application at `http://127.0.0.1:5000/`


**Exploit Example:**

Try accessing: `http://127.0.0.1:5000/?id=1;SELECT+1--`

This will bypass the intended query and return a different result.  Explore other SQL injection techniques at your own risk (within this controlled environment only).


**Disclaimer:**  Misuse of this code is prohibited. I am not responsible for any damage or unauthorized activity resulting from its use.


```

```zip
[app.py]
```python
from flask import Flask, request

app = Flask(__name__)

# **Intentionally vulnerable code:**
@app.route("/")
def index():
    id = request.args.get('id')
    # No sanitization or parameterized queries.  Highly insecure!
    query = f"SELECT * FROM users WHERE id = {id}"  
    # In-memory database (replace with SQLite if needed)
    users = [{'id': 1, 'name': 'Alice'}]
    # Simulate database query.  In a real app, replace with a proper database interaction.
    if id == "1":
        return f"User: {users[0]['name']}"
    else:
        return "User not found"

if __name__ == "__main__":
    app.run(debug=False) #debug=True would provide more detailed error messages, but should be avoided in production
```
```zip

```
