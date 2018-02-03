import requests
import PyV8
from bs4 import BeautifulSoup
dict_ = {
	'ﾟωﾟﾉ':'a',
	'ﾟｰﾟ':'b',
	'ﾟΘﾟ':'d',
	'ﾟДﾟ':'e',
	'o^_^o':'g',
	'ﾟεﾟ': 'p',
	'ﾟoﾟ':'q'
};
ctxt = PyV8.JSContext()
ctxt.__enter__()
ctxt.eval(open('js_pre.js').read())
#url = 'http://h1.aayyc.com/ckplayer/youku/?vid=1a87Pa2fPGLhIbrv0QHWnidhVdqexRXVvluA1NU6QLt6Hdh4tzn2tZwvs6Yg8w&height=449'
#url = 'http://h1.aayyc.com/ckplayer/youku/?vid=0b07vcAFVNUdg1vaNjy5SOOjDixm35jwbZ9RZvX7K6C9iQWk2090GPlnOvi9Sw&height=449'
url = 'http://h1.aayyc.com/ckplayer/iqiyi/indexh5.m3u8?tvid=3926uy7TJiqsGzP+kN5ON2VYdd2AqvIqX24IwpPktvPF4/rzKgw&height=449'
r = requests.get(url)
r.charset = 'utf-8'
soup = BeautifulSoup(r.content,'html.parser')
js_text = soup.findAll('script')[4].text
str_ = (js_text.split('\r\n')[1].split(';')[-2])
for (d,x) in dict_.items():
	str_=str_.replace(d,x)
print(ctxt.eval(str_+';'))
print(123)
print(ctxt.eval('sm'))
