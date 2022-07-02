import glob
from zipfile import ZipFile
import os
from os.path import basename


# figure out how to use glob.glob instead of iglob sorted(glob.glob("Webapp/static/28793893/*.jpg"), key=os.path.getmtime)
def getImglist(pixivID):
    print(pixivID)
    img_list = []
    noImgs = 0
    for filename in glob.iglob("Webapp/static/"+ pixivID +"/*.jpg"):
        print(filename)
        img_list.append(filename.split("\\")[-1].split(".")[0])
        noImgs += 1
    return  img_list,noImgs

def createZip(pixivID,noImgs):
    #Check if zip file exists if it does do nothing else
    if os.path.exists("Webapp/static/zips/"+ str(pixivID) + '_' + str(noImgs) + '.zip'):
        print("Updated zip file already exists")
        return("static/zips/"+ str(pixivID) + '_' + str(noImgs) + '.zip')
    #delete old zip file 
    for files in glob.glob("Webapp/static/zips/"+ str(pixivID) + "*.zip"):
        os.remove(files)
    #create new zip with all images
    with ZipFile( "Webapp/static/zips/"+ str(pixivID) + '_' + str(noImgs) + '.zip','w') as zipObj:
        for folderName,subfolders,filenames in os.walk("Webapp/static/"+ pixivID):
            for filename in filenames:
                filePath = os.path.join(folderName,filename)
                zipObj.write(filePath,basename(filePath))
    
    print("ZIP created with " + str(noImgs) + " images")
    return("static/zips/"+ str(pixivID) + '_' + str(noImgs) + '.zip')
#print(getImglist(28793893))