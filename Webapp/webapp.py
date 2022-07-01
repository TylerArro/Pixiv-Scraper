from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import os
from functions import getImglist, createZip
from classes import pixImg

#on click start scraper then display the scraped images in the returned HTML

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home_page.html')

@app.route('/rankings')
def rankings():
    img_list = []
    imgIDs,noImgs = getImglist('rankings')
    for img in imgIDs:
        img_list.append(pixImg('static/rankings/' + img + ".jpg", img))
    createZip('rankings',noImgs)
    
    return render_template('rankings.html',img_list = img_list)

@app.route('/users', methods = ['POST'])
def users():
    pixivID = request.form['pixiv-id']
    img_list = []
    #loop through images and get URL add them to img class list
    imgIDs,noImgs = getImglist(pixivID)
    for img in imgIDs:
        img_list.append(pixImg('static/' + pixivID + '/' + img + ".jpg", img))
    return render_template('users.html', pixivID = pixivID,img_list = img_list)


# 0.0.0.0 to make website avalible on public ip
#default port 5000
if __name__ == '__main__':
    app.run(port=6969,debug=True)