from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home_page.html')

@app.route('/rankings')
def rankings():
    return render_template('rankings.html')

@app.route('/users')
def users():
    return render_template('users.html')
# 0.0.0.0 to make website avalible on public ip
#default port 5000
if __name__ == '__main__':
    app.run(port=6969,debug=True)
