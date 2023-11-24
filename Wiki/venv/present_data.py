from flask import Flask, jsonify

from scrap import scrape_data
app = Flask(__name__)

@app.route('/api/nobel', methods=['GET'])
def get_nobel_data():
    url = 'https://en.wikipedia.org/wiki/List_of_Nobel_laureates'
    data = scrape_data(url)
    return jsonify(data)

@app.route('/api/nobel/country', methods=['GET'])
def get_nobel_country_data():
    url = 'https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country'
    data = scrape_data(url)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)