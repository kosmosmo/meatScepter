# example usage:
#
# main(directory="\\\\somewhere\\over\\rainbow",variety=50,dispatch=50)
# main(directory="\\\\somewhere\\over\\rainbow",variety=50,dispatch=50,mode=1,key=['kitty','puppy'])
#
# mode 0 default, will dispatch dick pics
# mode 1 need to specify key words
#
# Use at your own risk


directory = '\\\\MOMO-PC\\buildTest'

# specify where you want to dump the images.
#Path need to use forwardslash "/" or double slash"\\" !!


import json,urllib2,os,random,string,re
from shutil import copyfile
class main():
    def __init__(self,directory='',mode=0,variety=50,dispatch=50,keys=[],logDest='',rs=''):
        self.mode = mode
        self.directory = directory
        self.cacheImg = []
        self.cacheFlag = False
        self.imgIndex = 0
        self.dispatch = dispatch
        self.keys = keys
        self.imgUrls = self.scrape()
        self.log = []
        self.variety = variety
        self.rs = rs
        if not logDest:
            self.logDest = directory
        else:
            self.logDest = logDest
        if self.rs:
            self.reset()
            return
        if not self.directory:
            print "need to specify directory"
            return
        elif self.variety>len(self.imgUrls):
            print "variety too large"
            return
        else:
            self.BFS()

    def scrape(self):
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        if self.mode == 0:
            url = "https://raw.githubusercontent.com/kosmosmo/meatScepter/master/CacheUrl.txt"
            imgUrls = json.load(urllib2.urlopen(urllib2.Request(url, headers=header)))

        else:
            imgUrls = []
            for key in self.keys:
                query=key.replace(' ','+')
                url = "https://www.bing.com/images/search?q="+query+"&FORM=HDRSC2"
                a = urllib2.urlopen(urllib2.Request(url, headers=header))
                elements = a.read()
                images_urls = re.findall(';,&quot;murl&quot;:&quot;(.+?)&quot;,&quot;', elements)
                imgUrls+=images_urls
        return imgUrls



    def getType(self,url):
        tp = url.split('.')[-1]
        if tp not in ["jpg","jpeg","png","gif"]:
            tp = "jpg"
        return tp

    def randomID(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))

    def dispatcher(self,dir,imgIndex):
        if self.cacheFlag == False:
            fileName = dir + '/' + self.randomID() +'.' + self.getType(self.imgUrls[imgIndex])
            try:
                imgData = urllib2.urlopen(self.imgUrls[imgIndex]).read()
                output = open(fileName, 'wb')
                output.write(imgData)
                output.close()
                self.cacheImg.append([fileName,self.getType(self.imgUrls[imgIndex])])
                self.log.append(fileName)
            except:
                pass
        else:
            src = self.cacheImg[random.randint(0,len(self.cacheImg)-1)][0]
            dst = dir+"/"+self.randomID() + '.'+self.cacheImg[self.imgIndex%len(self.cacheImg)][1]
            copyfile(src,dst)
            self.log.append(dst)


    def BFS(self):
        count = self.dispatch
        while self.dispatch > 0:
            queue = [self.directory]
            while queue:
                cur = queue.pop()
                self.dispatcher(cur,self.imgIndex)
                self.dispatch -= 1
                print str(count-self.dispatch) +" / " +str(count)
                if self.dispatch == 0:break
                self.imgIndex += 1
                if self.imgIndex == self.variety:
                    self.cacheFlag = True
                sub = os.listdir(cur)
                for item in sub:
                    newPath = cur + '/' + item
                    if os.path.isdir(newPath):
                        queue.append(newPath)
        self.toLog()


    def toLog(self):
        with open(self.logDest + '/' + 'log.txt', 'w') as outfile:
            json.dump(self.log, outfile)

    def reset(self):
        if os.path.exists(self.rs):
            with open(self.rs) as outfile:
                files = json.load(outfile)
                outfile.close()
            for item in files:
                os.remove(item)
            os.remove(self.rs)
            print "deleted"
        else:
            print "path not exists"

if not directory:"need to specify directory"
main(directory=directory)
