from flask import Flask, request, redirect, url_for, render_template_string
import re
from html import escape

app = Flask(__name__)

# HTML templates
home_template = '''
<!doctype html>
<html>
    <head>
        <title>Search App</title>
    </head>
    <body>
        <h1>Search Page</h1>
        <form method="POST" action="/">
            <label for="search">Enter search term:</label>
            <input type="text" id="search" name="search" value="">
            <input type="submit" value="Submit">
        </form>
    </body>
</html>
'''

result_template = '''
<!doctype html>
<html>
    <head>
        <title>Search Result</title>
    </head>
    <body>
        <h1>Search Term</h1>
        <p>{{ search_term }}</p>
        <a href="/">Go back to home page</a>
    </body>
</html>
'''

def is_valid_search_term(search_term):
    # Ensure the input is alphanumeric and between 3 and 16 characters long
    if not re.match(r'^[a-zA-Z0-9_]{3,16}$', search_term):
        return False

    # HTML escape to prevent XSS attacks
    escaped_search_term = escape(search_term)
    if search_term != escaped_search_term:
        return False

    # Check for common SQL injection patterns
    sql_keywords = [
        'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION', 'ALTER', '--', ';', '/*', '*/', 'OR', 'AND'
    ]
    for keyword in sql_keywords:
        if keyword.lower() in search_term.lower():
            return False

    return True

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search']
        
        if not is_valid_search_term(search_term):
            return render_template_string(home_template)
        
        return redirect(url_for('result', search_term=search_term))
    
    return render_template_string(home_template)

@app.route('/result')
def result():
    search_term = request.args.get('search_term')
    return render_template_string(result_template, search_term=search_term)

if __name__ == '__main__':
    app.run(debug=True)
