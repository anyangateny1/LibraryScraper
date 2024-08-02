from flask import Flask, render_template, request
from scraper import scrapeLibrary

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        book_name = request.form['query']
        result = scrapeLibrary(book_name)
        return render_template('result.html', result=result)
    
if __name__ == '__main__':
    app.run(debug=True)
