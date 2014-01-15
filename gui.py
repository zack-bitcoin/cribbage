from xmlrpclib import ServerProxy
try:
    from jsonrpc import ServiceProxy
except:
    from bitcoinrpc import AuthServiceProxy as ServiceProxy       
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import string,cgi,time, json, random, copy, pickle
PORT=8090

def fs2dic(fs):
    dic={}
    for i in fs.keys():
        a=fs.getlist(i)
        if len(a)>0:
            dic[i]=fs.getlist(i)[0]
        else:
            dic[i]=""
    return dic

Z='''iVBORw0KGgoAAAANSUhEUgAAABQAAAAyCAIAAADTHmxxAAAACXBIWXMAAAsTAAALEwEAmpwYAAAA
B3RJTUUH3gEPAxslYZdPnQAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAEn
SURBVEjH3ZY9DsIwDIWfLe7C1KFbOQc5prlHNhhYOI0ZmqYQ5dcdkMhUNfli+8VxTGgO2T4c/nfI
R5zVQapKN8pPuoJ4rgeuDAdVZVtkqgqAzcoQEZtJq+VNMDaTAE7J1P281NlZfN5ykwxrJAjOQ2Sy
cofnlz90VKN8KliJzwbFQ0Fa4NS7ye+wXtVg1mI5mjW5LXu1YWOd6rFcTzseIkMWOKwys42EA926
K8kXuV1sHgtVWjEXHW4K1ialAPfWg3jO9eci73B8buI2FbPJFvfzsmZ4gHscXreIK+fJD8B5tW0k
ADaT88uTqj6el7q8mcOffLjPEShlUvI/FBNn6AwcDpchc+mNZcz6uMt3eg5Fu9nvbtmKTdEPukwy
kwB4zG2BqkaN3jPigVWlUY+NAAAAAElFTkSuQmCC
'''
L='''iVBORw0KGgoAAAANSUhEUgAAABQAAAAyCAIAAADTHmxxAAAACXBIWXMAAAsTAAALEwEAmpwYAAAA
B3RJTUUH3gEPAxwEYr/JBAAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAFY
SURBVEjH3ZYxbsMwDEU/ia69RYBMHrS5Q04RHaHHyhGUU3TR5gLpEiC36AHYQbblKpYs0UOBckpg
P3/qk6JE2Aw3/bD4v+EW6ywGiQhdaf2hzZhna+BCWIgI61YmIgBY7QwRsZrUKk+GsZoE8JI8Go59
mTXOrytvkuM7bjScm8jkzQibuwdwOGlLFch6Phr2/d4vv/J68Zt2cNMiNXBarc5HWM6ikNUoz7Kq
tF2cNll4aX5uGEc4qU1N23GTVaELw8aQc8sYWpKwoGv1JPlFThubNVY3lWqUVTRJSrp9vR3rXD4u
1hO2i/0c+NV+GI7982x43MYOp5BDIOtnyOMDpvOczKDKOJww3HrO5bapDIBDwuFPE2nunkTk8+ut
nPnzp03n4abDPejnOimpxTxM2m8GFrvH0N72dOrD3SF2WOtqJ/3qK1v2UvQHt0xSkwC4LW0HEZk9
+gGfu4WjzVRGRAAAAABJRU5ErkJggg==

'''
M='''iVBORw0KGgoAAAANSUhEUgAAABQAAAAyCAIAAADTHmxxAAAACXBIWXMAAAsTAAALEwEAmpwYAAAA
B3RJTUUH3gEPAx0ehsYBPwAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAGx
SURBVEjH3ZaxbsIwEIb/szIWKSzlBZCYu7EwMzKQR+AtOvcteAQzZOzMwsaMxAvAUqSwXwc72HHs
2HG3Whliy5/PvvvvdITokO1Phf87pPXOwSGYWe+WgETZfLl+Cp9LzEwHUpNyrcnH92fEaAVmFq/p
i3T+vYvMDMDAtrW+ZUXaPBEJe4diQqT9T0TumwdGxx2t1ERi+MylqoC3AZwXy+FTPi4nv+UoqfdI
7fDCXp2v6pQnNABKPKd3YzmR7MhTH7a7ZSSBhif7WT4MANiMhYvu1PCT/akfBccvAgBvORKbgEfF
X6pGPjzZz4Jws+uozasC4fWQ8+A+qUIrUlzlko+ZcnP8zX7ZVqADFaMxix+wXA/c2auwCAmgKW8h
uM4USUZWEiR4y8/pPVOeKaV36NrXY2Iyb9rPddimdVj0oNrA58VyvkovJiYiohVwYpA624jZdrXf
8vXoV2vRDVLtL6MXf4alVhJPSj96lcSrs/6iSg/x9vOeUb1UczOUz0G1V7onIsjRKaFTWo4vvaYY
VKozILJTPInUKekrEVFMXZtCJSbIWM2lvnZ6T8tb0wD9AsX1rfjk+0l6AAAAAElFTkSuQmCC

'''
divider='''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

'''
piece='''iVBORw0KGgoAAAANSUhEUgAAABQAAAAyCAIAAADTHmxxAAAACXBIWXMAAAsTAAALEwEAmpwYAAAA
B3RJTUUH3gEPAyMbt2nuzQAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAACe
SURBVEjH7VYxDoAgDARmSc4H+P83OfsASOqOAwnBTa+GmmgnBi7t9a5NvaMCAqcJLd4uPFF6jrk+
At0qCLymaUHDmQRX2mMb1pDDOfc0jXTOMaukCjRSxZmXquL5siEgHcZ4u/fm7bL7TEzZzV7kSJpu
km+toRdskuHL4J8qs6lKU7r+e1vW0zVUSpn3mcxMIJ9xmIOAV8vueNVkPgBHQFc/xCUyBQAAAABJ
RU5ErkJggg==

'''
form='''
<form name="first" action="{}" method="post">
<input type="submit" value="{}">{}
</form> {}
'''
character={'L':L, 'M':M, 'Z':Z}
def easyForm(action, value, moreHtml=''):
    return form.format(action, value, moreHtml, "{}")

def page1():
    out="<p>cribbage game!!</p><br />{}"
    a=easyForm('/home', 'PLAY GAME')
    out=out.format(a)
    print('out: ' +str(out))
    return out.format('')
def picture(string):
    return '<img src="data:image/png;base64,{}">{}'.format(string, '{}')
def newline():
    return '''<br />
{}'''
database='crib.db'
initial_db={'L':[0,1], "M":[0,1], "Z":[0,1]}
def fs_load():
   try:
      return pickle.load(open(database, 'rb'))
   except:
      fs_save(initial_db)
      return pickle.load(open(database, 'rb'))      
def fs_save(dic):
    pickle.dump(dic, open(database, 'wb'))

def increase(char, num):
    fs=fs_load()
    fs[char]=fs[char][1:]
    print('fs[char]: ' +str(fs[char][0]))
    number=fs[char][0]
    print('number: ' +str(number))
    print('num: ' +str(num))
    print('number: ' +str(type(number)))
    print('num: ' +str(type(num)))
    numy=int(number)
    num=numy+num
    fs[char].append(num)
    fs_save(fs)
def home(dic_in):
    print('dic_in: ' +str(dic_in))
    if 'L_add' in dic_in:
        increase('L', int(dic_in['L_add']))
    if 'M_add' in dic_in:
        increase('M', int(dic_in['M_add']))
    if 'Z_add' in dic_in:
        increase('Z', int(dic_in['Z_add']))
    if 'restart' in dic_in:
        fs_save(initial_db)
    fs=fs_load()
    #    out='<img src="/home/zack/Hacking/cribbage/board.png">'
    out='<html><body>{}</body></html>'
    def line(out, fs, char, rang):
        for i in range(40):
            count=rang[0]+i
            print('count: ' +str(count))

            print('fs: ' +str(fs))
            #            print('char: ' +str(char))
            print('fschar: ' +str(fs[char]))
            if count in fs[char]:
                out=out.format(picture(character[char]))
            else:
                out=out.format(picture(piece))
#        print('out: ' +str(out))
        out=out.format(newline())
        return out
    def line1(out, fs, rang):
        out=line(out, fs, 'L', rang)#L
        out=line(out, fs, 'M', rang)#M
        out=line(out, fs, 'Z', rang)#Z
#        print('out: ' +str(out))
        return out
    out=line1(out, fs, [1, 40])
    out=out.format(picture(divider))
    out=out.format(newline())
    out=line1(out, fs, [41, 80])
    out=out.format(picture(divider))
    out=out.format(newline())
    out=line1(out, fs, [81, 120])
    out=out.format(easyForm('/home', 'Points to L', "<input type='text' name='L_add'>"),'')
    out=out.format(easyForm('/home', 'Points to M', "<input type='text' name='M_add'>"),'')
    out=out.format(easyForm('/home', 'Points to Z', "<input type='text' name='Z_add'>"),'')
    out=out.format('_______________________'+easyForm('/home', 'RESTART', "<input type='hidden' name='restart' value='True'>"),'')
    return out.format("")

class MyHandler(BaseHTTPRequestHandler):
   def do_GET(self):
      try:
         if self.path == '/' :    
#            page = make_index( '.' )
            self.send_response(200)
            self.send_header('Content-type',    'text/html')
            self.end_headers()
            self.wfile.write(page1())
            return    
         else : # default: just send the file    
            filepath = self.path[1:] # remove leading '/'    
            if [].count(filepath)>0:
#               f = open( os.path.join(CWD, filepath), 'rb' )
                 #note that this potentially makes every file on your computer readable bny the internet
               self.send_response(200)
               self.send_header('Content-type',    'application/octet-stream')
               self.end_headers()
               self.wfile.write(f.read())
               f.close()
            else:
               self.send_response(200)
               self.send_header('Content-type',    'text/html')
               self.end_headers()
               self.wfile.write("<h5>Don't do that</h5>")
            return
         return # be sure not to fall into "except:" clause ?      
      except IOError as e :  
             # debug    
         print e
         self.send_error(404,'File Not Found: %s' % self.path)
   def do_POST(self):
            print("path: " + str(self.path))
#         try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))    
            print(ctype)
            if ctype == 'multipart/form-data' or ctype=='application/x-www-form-urlencoded':    
               fs = cgi.FieldStorage( fp = self.rfile,
                                      headers = self.headers, # headers_,
                                      environ={ 'REQUEST_METHOD':'POST' })
            else: raise Exception("Unexpected POST request")
            self.send_response(200)
            self.end_headers()
            dic=fs2dic(fs)
            if self.path=='/home':
                self.wfile.write(home(dic))
            else:
                error('path is not programmed')
def main():
   try:
      server = HTTPServer(('', PORT), MyHandler)
      print 'started httpserver...'
      server.serve_forever()
   except KeyboardInterrupt:
      print '^C received, shutting down server'
      server.socket.close()
if __name__ == '__main__':
   main()




