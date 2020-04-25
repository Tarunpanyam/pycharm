import lxml.html
import urllib.request
import pprint
import http.cookiejar as cookielib
from io import BytesIO
from PIL import Image
import pytesseract
import sys
import shutil
import threading
from BeautifulSoup import BeautifulSoup as soup
def form_parsing(html):
   tree = lxml.html.fromstring(html)
   data = {}
   for e in tree.cssselect('form input'):
      if e.get('name'):
         data[e.get('name')] = e.get('value')
   return data
def load_captcha(html):
   tree = lxml.html.fromstring(html)
   img_data = tree.cssselect('div#recaptcha img')[0].get('src')
   img_data = img_data.partition(',')[-1]
   binary_img_data = img_data.decode('base64')
   file_like = BytesIO(binary_img_data)
   img = Image.open(file_like)
   return img
response = urllib.request.urlopen('https://parivahan.gov.in/rcdlstatus/?pur_cd=101')
html = response.read()
text = html.decode()
# geting the no of forms to fill
form = form_parsing(html)
pprint.pprint(form)
# delling  with cpacha image
img = get_captcha(html)
img.save('captcha_original.png')
gray = img.convert('L')
gray.save('captcha_gray.png')
bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
bw.save('captcha_thresholded.png')
s=pytesseract.image_to_string(bw)
dl=input(' Enter your Driving License Number')
db=input('Enter your Date of Birth in dd-mm-yyyy format')
parameters = {'Driving Licence No.':dl, 'Date Of Birth': db,'Enter Verification Code': s}
link = requests.post('https://parivahan.gov.in/rcdlstatus/?pur_cd=101, data = parameters)
l=requests.get( link )
a=m(l)
# deling with licence picture
def m(l):
    html = l
    tags = filter( html )
    for tag in tags:
        src = tag.get( "src" )
        if src:
            src = re.match( r"((?:https?:\/\/.*)?\/(.*\.(?:png|jpg)))", src )
            if src:
                (link, name) = src.groups()
                if not link.startswith("http"):
                    link = "https://www.drivespark.com" + link
                _t = threading.Thread( target=requesthandle, args=(link, name.split("/")[-1]) )
                _t.daemon = True
                _t.start()

                while THREAD_COUNTER >= THREAD_MAX:
                    pass

    while THREAD_COUNTER > 0:
        pass

THREAD_COUNTER = 0
THREAD_MAX     = 5

def get_source( link ):
    r = requests.get( link )
    if r.status_code == 200:
        return soup( r.text )
    else:
        sys.exit( "[~] Invalid Response Received." )

def filter( html ):
    imgs = html.findAll( "img" )
    if imgs:
        return imgs
    else:
        sys.exit("[~] No images detected on the page.")

def requesthandle( link, name ):
    global THREAD_COUNTER
    THREAD_COUNTER += 1
    try:
        r = requests.get( link, stream=True )
        if r.status_code == 200:
            r.raw.decode_content = True
            f = open( name, "wb" )
            shutil.copyfileobj(r.raw, f)
            f.close()
            print ("[*] Downloaded Image: %s" % name)
    except Exception, error:
        print ("[~] Error Occured with %s : %s" % (name, error))
    THREAD_COUNTER -= 1