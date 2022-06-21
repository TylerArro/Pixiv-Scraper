from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import os

#on click start scraper then display the scraped images in the returned HTML

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home_page.html')

@app.route('/rankings')
def rankings():
    imgIDs = '98962415.png'
    imgURL = 'static/rankings/' + imgIDs
    artworkID = '98962415'
    return render_template('rankings.html',imgURL = imgURL, artworkID = artworkID)

@app.route('/users', methods = ['POST'])
def users():
    pixivID = request.form['pixiv-id']
    imgIDs = '90318579.jpg'
    imgURL =  'static/' + pixivID + '/' + imgIDs
    artworkID = '90318579'
    return render_template('users.html', pixivID = pixivID, imgURL = imgURL, artworkID = artworkID)
# 0.0.0.0 to make website avalible on public ip
#default port 5000
if __name__ == '__main__':
    app.run(port=5000,debug=True)