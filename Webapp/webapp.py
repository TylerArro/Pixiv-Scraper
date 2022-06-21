from flask import Flask
app = Flask(__name__)

@app.route('/')
def home_page():
    home_html = '<h1>Home Page</h1>'

# 0.0.0.0 to make website avalible on public ip
#default port 5000
if __name__ == '__main__':
    app.run(port=6969,debug=True)