# -*- coding:utf-8 -*-

import os,base64,time,json

import tornado.ioloop
import tornado.web

import os
import os.path
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options
#import models
import datetime

from collections import deque
from settings import static_path,IP,PORT

ALLOW_FILETYPE = ['.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.close()
       return self.render('web/home.html')
   
class Main1Handler(tornado.web.RequestHandler):
    def get(self):
        return self.render('web/index1.html')

class Main2Handler(tornado.web.RequestHandler):
    def get(self):
        return self.render('web/index2.html')
    
class Downloads(tornado.web.RequestHandler):
    def get(self):
        filename = "ans"
        print('i download file handler : ',filename)

        ifile  = open(filename+".txt", "r")
        self.set_header ('Content-Type', 'text')
        self.set_header ('Content-Disposition', 'attachment; filename='+filename+'')
        self.write (ifile.read())
        
        
    def post(self):
        print("post")

class UploadFile2Handler(tornado.web.RequestHandler):

    @staticmethod
    def tail(file, n=1, bs=1024):
        f = open(file)
        f.seek(0,2)
        l = 1-f.read(1).count('\n')
        B = f.tell()
        while n >= l and B > 0:
                block = min(bs, B)
                B -= block
                f.seek(B, 0)
                l += f.read(block).count('\n')
        f.seek(B, 0)
        l = min(l,n)
        lines = f.readlines()[-l:]
     
        f.close()
        return lines

   
    def post(self):
        from settings import upload_path
        from ocr import OCR
        from question import QUESTION

        now_time = time.strftime('%Y-%m-%dT%H-%M-%S',time.localtime(time.time()))
        dir_prefix = now_time

        try:
            file_metas = self.request.files['file']
        except:
            return self.render('web/result.html', result='negative', result_header='Something went wrong', result_content='Please select the file to be printed.')

        for meta in file_metas:
            filename = meta['filename']
            # valid filetype
            if not os.path.splitext(filename)[1] in ALLOW_FILETYPE:
                return self.render('web/result.html', result='negative', result_header='upload failed',
                                       result_content='File format is not supported')

            try:
                os.makedirs(os.path.join(upload_path, dir_prefix))
            except:
                pass
            # save file
            filepath = os.path.join(upload_path, dir_prefix, "img"+os.path.splitext(filename)[1])
            with open(filepath,'wb') as up:
                up.write(meta['body'])
            # ocr
            ocrinstance = OCR()
            res = ocrinstance.getResult(filepath)
            # print(res)
            statusCode = res['code']
            status = 'Scanned successful' if (statusCode == 1) else 'Something went wrong'
            text = res['text']
            #write file for question anaylsis
            path="en"
            file = open(path +"/sentences.txt","a",encoding="utf-8")
            file.write(text)
            file.close()
            
            # save res
            respath = os.path.join(upload_path, dir_prefix, 'result.txt')
            with open(respath, 'w',encoding="utf-8") as info:
                info.write(status+'\n'+text)

            quest= QUESTION()
            answ= quest.resultq()
            # print(answ)
            # file = open('answer.txt','w')
            # file.write(answ)
            # file.close()

            f = open("ans.txt", "r")
            ans=f.readlines()
            filepath='ans.txt'
            with open(filepath) as fp:
                line = fp.readline()
                cnt = 1
                while line:
                    data="Line {}: {}".format(cnt, line.strip())
                    line = fp.readline()
                    cnt += 1
                    # print(data)

            with open('ans.txt') as myfile:
                
                data1= (list(myfile)[-1])

            lines = UploadFile2Handler.tail("ans.txt", 10)
            # for line in lines:
            data2= lines

            # print(ans)

            # render
            if(statusCode == 1):
                return self.render('web/result.html', result='positive', result_header=status, result_content=text)
            else:
                return self.render('web/result.html', result='negative', result_header=status, result_content=text)


class UploadFile1Handler(tornado.web.RequestHandler):

    def post(self):
        from settings import upload_path
        from ocr import OCR
        from question import QUESTION
        
        now_time = time.strftime('%Y-%m-%dT%H-%M-%S', time.localtime(time.time()))
        dir_prefix = now_time

        try:
            base64ImgData = self.request.arguments['data'][0].decode("utf-8")
            # Remove the description in front of the base64 picture str
            base64ImgData = base64ImgData[base64ImgData.find(',') + 1:]
            imgData = base64.b64decode(base64ImgData)
        except:
            self.finish({
                'code': 0,
                'message': "error"
            })

        try:
            os.makedirs(os.path.join(upload_path, dir_prefix))
        except:
            pass

        # save file
        filepath = os.path.join(upload_path, dir_prefix, "img.png" )
        with open(filepath, 'wb') as up:
            up.write(imgData)
        # ocr
        ocrinstance = OCR()
        res = ocrinstance.getResult(filepath)
        statusCode = res['code']
        status = 'success' if (statusCode == 1) else 'failure'
        text = res['text']
       #write file for question anaylsis
        path="en"
        file = open(path +"/sentences.txt","a",encoding="utf-8")
        file.write(text)
        file.close()

        # save res
        respath = os.path.join(upload_path, dir_prefix, 'result.txt')
        with open(respath, 'w', encoding="utf-8") as info:
            info.write(status + '\n' + text)

        quest= QUESTION()
        ans= quest.resultq()
        # print(answ)
        # file = open('answer.txt','w')
        # file.write(answ)
        # file.close()
        f = open("ans.txt", "r")
        answ=f.readlines() 
        filepath='ans.txt'
        with open(filepath) as fp:
            line = fp.readline()
            cnt = 1
            while line:
                data="Line {}: {}".format(cnt, line.strip())
                line = fp.readline()
                cnt += 1
                #print(data)

        with open('ans.txt') as myfile:
                
            data1= (list(myfile)[-1])

        self.finish({
            'code': statusCode,
            'message': text
        })

application = tornado.web.Application([
    (r"/", tornado.web.RedirectHandler,{"url":"/home","permanent":True}),
    (r"/home", MainHandler),
    (r"/1", Main1Handler),
    (r"/2", Main2Handler),
    (r"/1/upload", UploadFile1Handler),
    (r"/2/upload", UploadFile2Handler),
    (r"/2/download",Downloads),
    (r"/download",Downloads)],
    static_path=static_path)

if __name__ == "__main__":
    application.listen(PORT, address=IP)
    # IP = '127.0.0.1'
    # PORT = 9999
    print('listening to 127.0.0.1:9999')
    tornado.ioloop.IOLoop.instance().start()


    #python app.py