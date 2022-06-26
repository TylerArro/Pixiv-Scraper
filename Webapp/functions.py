import glob

# figure out how to use glob.glob instead of i glob sorted(glob.glob("Webapp/static/28793893/*.jpg"), key=os.path.getmtime)
def getImglist(pixivID):
    print(pixivID)
    img_list = []
    for filename in glob.iglob("Webapp/static/"+ pixivID +"/*.jpg"):
        print(filename)
        img_list.append(filename.split("\\")[-1].split(".")[0])
        
    return  img_list

#print(getImglist(28793893))