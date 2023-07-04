#!/usr/bin/env python3
r"""
omarscan [--verbose] [--Debug] [--help] --xml=<file.xml> scannedsheets.pdf

<-dlf> 2023-07-04
Local OMRscan for MCQ-XeLaTeX

UBUNTU:
apt install python3-opencv python3-pylibdmtx
python -m pip install pypdf [--upgrade]

(C)  DLFerrario http://www.dlfer.xyz/var/mcqxelatex.html
"""


import sys
import math
import numpy as np
import getopt
import os
import glob
import subprocess
import tempfile
import shutil
import defusedxml.ElementTree as ET

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import __version__ as PIL_version
PIL_M_version= int( PIL_version.split(".")[0])

import time
import datetime
from six.moves import range
import socket


import cv2 as cv
from pylibdmtx import pylibdmtx
from pylibdmtx import __version__ as DMTX_version
import pypdf as pyPdf


#-----------------------------------------------------------------
A4_width = 210.0  # mm
A4_height = 297.0  # mm
barcode_width = 25.4 / 1.8
barcode_height = 25.4 / 1.8
BLUR_RADIUS = 5 # pixel  
MINRADIUS_RATIO=0.8 # minimal radius_ratio of blob's enclosing circle.
MAXRADIUS_RATIO=1.8 # maximal radius_ratio of blob's enclosing circle
MINAREA_RATIO=1.0 # 0.5
MAXAREA_RATIO=2.2

FILLED_THRES = 150 # threshold for filled bubbles  (grayscale 0..255 mean) 
FILLED_THRES_CONTOUR = 140 # threshold for filled contours (grayscale 0..255 mean) 
# isoperimetric inequality: L^2 >= 4 Pi A, with equality on circle 
ISOPERIMETRIC_CONSTANT= 28 # >= 4 
# consider ( h * k h  ) : L= 2h + 2kh = 2h(k+1); A = k h^2 
# => L^2 / (pi A) = 4 h^2 (k+1)^2 / (pi k h^2) =  4/pi *  (k+1)^2/k 
# 15 is more or less something 1x10 
# 28 is more or less something 1x20

# UIDlength=6
# anslength=10

VERBOSE = True
VVERBOSE = False
DEBUG=False

TMPBASE = 'omr-form'
TMPTODOBASE = 'omr-marks-'
FQDN = socket.gethostname() #'u53040a.matapp.unimib.it'
MAX_PAGES = 999
MOGRIFY=False

STDERR = sys.stderr



#-----------------------------------------------------------------
#--BEGINSIG--
import base64;eval(compile(base64.b64decode(b'CmRlZiBjaGVja19zZWxmKCk6CiAgICByZXR1cm4gVHJ1ZQoKZGVmIGdldF9vcHQoKToKICAgIGdsb2JhbCBWRVJCT1NFLCBERUJVRywgTU9HUklGWQogICAgaWYgbm90IGNoZWNrX3NlbGYoKToKICAgICAgICBzeXMuc3RkZXJyLndyaXRlKAogICAgICAgICJTZWxmLWludGVncml0eSBjaGVja3N1bSBmYWlsZWQhIEFib3J0aW5nLi4uXG5JbnN0YWxsIGEgbmV3IGNsZWFuIHZlcnNpb24hXG4iKQogICAgICAgIHN5cy5leGl0KDEpCiAgICB0cnk6CiAgICAgICAgb3B0cywgYXJncyA9IGdldG9wdC5nZXRvcHQoc3lzLmFyZ3ZbMTpdLCAiaHg6dkRtIiwgWwogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJoZWxwIiwgInhtbD0iLCAidmVyYm9zZSIsJ0RlYnVnJywibW9ncmlmeSJdKQogICAgIyBleGNlcHQgZ2V0b3B0LkdldG9wdEVycm9yLCBlcnI6CiAgICBleGNlcHQ6CiAgICAgICAgU1RERVJSLndyaXRlKCIqKipHRVRPUFQgRVJST1IqKipcbltvcHRpb24gLS1oZWxwIGZvciBoZWxwXVxuIikKICAgICAgICBzeXMuZXhpdCgxKQogICAgaWYgbGVuKGFyZ3MpID09IDA6CiAgICAgICAgcHJpbnQoX19kb2NfXykKICAgICAgICBwcmludF92ZXJzaW9ucygpCiAgICAgICAgc3lzLmV4aXQoMSkKICAgIEhBU1hNTEZJTEUgPSBGYWxzZQogICAgZm9yIG8sIGEgaW4gb3B0czoKICAgICAgICBpZiBvID09ICItdiI6CiAgICAgICAgICAgIFZFUkJPU0UgPSBUcnVlCiAgICAgICAgZWxpZiBvID09ICItRCI6CiAgICAgICAgICAgIERFQlVHID0gVHJ1ZQogICAgICAgIGVsaWYgbyBpbiAoIi1tIiwiLS1tb2dyaWZ5Iik6CiAgICAgICAgICAgIE1PR1JJRlkgPSBUcnVlCiAgICAgICAgZWxpZiBvIGluICgiLWgiLCAiLS1oZWxwIik6CiAgICAgICAgICAgIHByaW50KF9fZG9jX18pCiAgICAgICAgICAgIHByaW50X3ZlcnNpb25zKCkKICAgICAgICAgICAgc3lzLmV4aXQoKQogICAgICAgIGVsaWYgbyBpbiAoJy14JywgJy0teG1sJyk6CiAgICAgICAgICAgIFhNTEZJTEUgPSBhCiAgICAgICAgICAgIEhBU1hNTEZJTEUgPSBUcnVlCiAgICBpZiBIQVNYTUxGSUxFIGFuZCBvcy5wYXRoLmV4aXN0cyhYTUxGSUxFKToKICAgICAgICByZXR1cm4gKG9zLnBhdGguYWJzcGF0aChYTUxGSUxFKSwgW29zLnBhdGguYWJzcGF0aCh4KSBmb3IgeCBpbiBhcmdzXSkKICAgIGVsc2U6CiAgICAgICAgcmFpc2UgRXhjZXB0aW9uKCJ4bWwgZmlsZSBub3QgZm91bmQhXG4iKQoKZGVmIGNoZWNrX3NlbGYoKToKIGltcG9ydCBvcywgaGFzaGxpYiwgcmUsIHN5cywgZGF0ZXRpbWUKIE1FX2Jhc2UsTUVfZXh0PW9zLnBhdGguc3BsaXRleHQob3MucGF0aC5hYnNwYXRoKF9fZmlsZV9fKSkKIE1FPU1FX2Jhc2UrJy5weScKIGlmIChkYXRldGltZS5kYXRldGltZS50b2RheSgpIC0gZGF0ZXRpbWUuZGF0ZXRpbWUuc3RycHRpbWUoJzIwMjMtMDctMDQnLCAnJVktJW0tJWQnKSkuZGF5cz4gNzIwOgogICAgIHN5cy5zdGRlcnIud3JpdGUoIlxuID4+PldBUk5JTkchISEgVmVyeSBvbGQgc2NyaXB0ISBDaGVjayBpZiB5b3UgY2FuIGRvd25sb2FkIGEgbmV3IG9uZSE8PDxcblxuIikKICAgICBpbnB1dCgnUHJlc3MgPFJldHVybj4gdG8gQ29udGludWUuLi4nKQogaWYgc3lzLnZlcnNpb25faW5mb1swXSA+IDI6CiAgIGFsbD1vcGVuKE1FLCdyJyxlbmNvZGluZz0ndXRmLTgnKS5yZWFkKCkKICAgZGVmIG15X2hhc2goaW5wdXRfY29udGVudCk6CiAgICAgcmV0dXJuIGhhc2hsaWIuc2hhMjI0KGlucHV0X2NvbnRlbnQuZW5jb2RlKGVuY29kaW5nPSd1dGYtOCcpKS5oZXhkaWdlc3QoKQogZWxzZToKICAgYWxsPW9wZW4oTUUsJ3InKS5yZWFkKCkKICAgZGVmIG15X2hhc2goaW5wdXRfY29udGVudCk6CiAgICAgcmV0dXJuIGhhc2hsaWIuc2hhMjI0KGlucHV0X2NvbnRlbnQpLmhleGRpZ2VzdCgpCiBwPWFsbC5pbmRleCgiXG4iKQogcmVnPXJlLmNvbXBpbGUoIiMtLUJFR0lOIisiU0lHLS18Iy0tRU5EIisiU0lHLS0iLHJlLk0gYW5kIHJlLkRPVEFMTCApCiBib2R5X2ZpcnN0LGhpZGRlbixib2R5X2xhc3Q9cmVzPXJlZy5zcGxpdChhbGxbcCsxOl0pCiBsPW15X2hhc2goYm9keV9maXJzdC5zdHJpcCgpICsgYm9keV9sYXN0LnN0cmlwKCkpCiBleHBlY3RfbD0nYTNhYzA3ZTE3ZTkwY2VlY2YxY2FiZTczNzQxY2IzMGViZTFiYWY0ZDU5NDcxY2Y0YWNjZmYzZTUnCiBpZiBsICE9IGV4cGVjdF9sOgogIHJldHVybiBGYWxzZQogZWxzZToKICByZXR1cm4gVHJ1ZQo=').decode('utf-8'),'<string>','exec'))
#--ENDSIG--
#-----------------------------------------------------------------

def print_versions():
    STDERR.write("python version: %s\n" % sys.version)
    STDERR.write("PIL version: %s\n" % PIL_version)
    STDERR.write("OpenCV version: %s\n" % cv.__version__)
    STDERR.write("pylibdmtx version: %s\n" % DMTX_version )
    STDERR.write("pyPdf version: %s\n" % pyPdf.__version__)

#-----------------------------------------------------------------
def txt2py(t, s):
    if t == 'float':
        return float(s)
    elif t == 'int':
        return int(s)
    elif t == 'coord':
        return tuple([float(x) for x in s.split(',')])
    else:
        if s[-2:] == 'pt':
            # convert to mm
            s = float(s[:-2]) * 0.3515
        return s


def xml2db(xmlfile):
    ndb = {}
    # parser = ET.XMLParser(encoding="utf-8") __HERE__
    parser = ET.XMLParser()
    ntree = ET.parse(xmlfile, parser=parser)
    root = ntree.getroot()
    for node in root:
        tmpdb = {}
        for item in node:
            n = item.attrib['n']
            t = item.attrib['type']
            content = item.text
            tmpdb[n] = txt2py(t, content)
        ndb[node.tag] = tmpdb
    return ndb

#-----------------------------------------------------------------


def get_marked_items(l):
    db = {}
    for (gr, item, _) in l:
        if not gr in db:
            db[gr] = {}
        name, value = item.split(":")
        name = int(name)
        if not name in db[gr]:
            db[gr][name] = []
        db[gr][name].append(value)
    return db
#-----------------------------------------------------------------


def get_numitems(l):
    items = []
    for x in l:
        name, value = x.split(":")
        name = int(name)
        if not name in items:
            items.append(name)
    return len(items)
#-----------------------------------------------------------------


def check_marked_items(db, UIDlen, anslen):
    uid = ["*"] * UIDlen
    ans = ["0"] * anslen
    for gr in db:
        if gr == 'UID':
            for k in db[gr]:  # k is integer
                if len(db[gr][k]) == 1:
                    uid[k] = db[gr][k][0]
                if len(db[gr][k]) == 0:
                    uid[k] = "-"
        if gr == "ans":
            for k in db[gr]:  # k int
                # print "k=", k
                if len(db[gr][k]) == 1:
                    ans[k-1] = db[gr][k][0]
                if len(db[gr][k]) > 1:
                    ans[k-1] = "*"
    return ("".join(uid), "".join(ans))
#-----------------------------------------------------------------


def convert_to_list(db, picsize):
    # pdf origin: bottom left
    # png origin: top left
    picwidth, picheight = picsize
    paperwidth = db['head']['paperwidth']  # mm
    paperheight = db['head']['paperheight']  # mm
    bubblewidth = db['head']['bubblewidth']  # mm
    bubbleheight = db['head']['bubbleheight']  # mm
    scale_x = picwidth/paperwidth
    scale_y = picheight/paperheight
    result = []
    for gr in db:
        if gr != 'head':
            for item in db[gr]:
                X = (db[gr][item][0] - bubblewidth*0.72) * scale_x
                Y = (paperheight - db[gr][item][1] -
                     bubbleheight*0.72) * scale_y
                result.append((gr, item, (X, Y)))
    return result
#-----------------------------------------------------------------


def roundxy(pt):
    return (Round(pt[0]), Round(pt[1]))


def EuclDist(pt, qt):
    return math.sqrt((pt[0] - qt[0])**2 + (pt[1] - qt[1])**2)


def PuntoMedio(pt, qt):
    return ((pt[0] + qt[0])*0.5, (pt[1] + qt[1])*0.5)


def is_hrule(rect, width):
    # rect.ncols > max_size and x.nrows < 0.1 * max_size:
    return (rect[2] > width * 0.5) and (rect[3] < 0.1 * width)


def mySmooth(img):
    return cv.GaussianBlur(img, (BLUR_RADIUS, BLUR_RADIUS),0)


#-----------------------------------------------------------------
def get_ULUR(bp):
    uri = [x[0]+x[1] for x in bp]
    sorted_uri = sorted(uri)
    UR = bp[uri.index(sorted_uri[-1])]
    uli = [x[1] - x[0] for x in bp]
    sorted_uli = sorted(uli)
    UL = bp[uli.index(sorted_uli[-1])]
    return UL, UR
#-----------------------------------------------------------------
def View(image):
        img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        pilimg = Image.fromarray(img)
        pilimg.show()

def cvView(image):
    cv.imshow("image", image)
    cv.waitKey(0)

def CreateImage(img_size,depth,channels):
    img_width,img_height=img_size
    if depth==8:
        img_depth=np.uint8
    else:
        img_depth=np.uint16
    return ( np.zeros((img_height,img_width,channels), img_depth) )

def GetSize(img):
    if len(img.shape) == 2 :
       img_height, img_width = img.shape
    else:
       img_height, img_width, _  = img.shape
    return (img_width,img_height ) 
	
def GetSubRect(image, rect):
    x,y,w,h = rect
    return image[y:y+h,x:x+w]

def Avg(img):
    # average of the inscribed circle GRAY value
    disc_radius = min( img.shape ) // 2
    disc_center = (img.shape[0]//2 ,  img.shape[1]//2 ) 
    disc_mask = np.zeros((img.shape[0],img.shape[1]),dtype=np.uint8)
    disc_mask = cv.circle ( disc_mask , disc_center, disc_radius , 255 , -1 )  
    result  = cv.mean(img, mask= disc_mask)
    return result[0]
    

def FindContours(image):
    # try to find all contours. 
    retvalues = cv.findContours(image,
                            cv.RETR_EXTERNAL,
                            cv.CHAIN_APPROX_SIMPLE
                            )
    if len(retvalues) == 2:
        contours = retvalues[0]
    elif len(retvalues) == 3:
        contours = retvalues[1] 
    else:
        raise Exception("Well, cv.findContours returned unknown list...")
    return contours
    contours_poly = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
    return [contours_poly[ii] for ii in range(len(contours)) ]

def Round(x):
    return int( round(x) )

#-----------------------------------------------------------------
def align_markers(image):
    threshval = 128
    threshval = 0 
    img_height,img_width = image.shape
    ret, bw = cv.threshold(mySmooth(image), threshval, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    contours_poly = FindContours(bw) 
    ii = 0
    possible_markers = []
    for x in contours_poly:
        rect= cv.boundingRect(x)
        if is_hrule(rect, img_width):
            ii += 1
            boxpoints = cv.boxPoints(cv.minAreaRect(x))
            possible_markers.append(get_ULUR(boxpoints))
    markfoot = [(0, 0), (img_width, 0)]
    markhead = [(0, img_height), (img_width, img_height)]
    for (pl, pr) in possible_markers:
            # non e' detto che sia destre sinistra...
        if pl[0] > pr[0]:
            l, r = pr, pl
        else:
            l, r = pl, pr
        if l[1] < markhead[0][1]:
            markhead = [l, r]
        if l[1] > markfoot[0][1]:
            markfoot = [l, r]
    if DEBUG:
        STDERR.write("""markers found at:
 ({:4.2f},{:4.2f})--({:4.2f},{:4.2f})
        |                 |
 ({:4.2f},{:4.2f})--({:4.2f},{:4.2f})
 """.format( 
            markhead[0][0],markhead[0][1] , markhead[1][0], markhead[1][1] , 
            markfoot[0][0],markfoot[0][1] , markfoot[1][0], markfoot[1][1] 
            ))
    return [markhead, markfoot]
#-----------------------------------------------------------------


def decode_datamatrix(candidate):
    # CV_8UC3
    res = pylibdmtx.decode( ( 
                    candidate.tobytes(),
                    candidate.shape[1], 
                    candidate.shape[0]  )
                    )
    if len(res)==1:
        return res[0].data.decode()
    else:
        return [] 

#-----------------------------------------------------------------


def get_markpoints(image, minarea, maxarea, minradius, maxradius ):
    threshval = 128
    ret, bw = cv.threshold(image, threshval, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    contours_poly = FindContours(bw) 
    # ii = 0
    possible_markpoints = []
    possible_contours = [] 
    for x in contours_poly:
        ca = cv.contourArea(x)
        center, radius = cv.minEnclosingCircle(x)
        success = True
        if success and ca > minarea and ca < maxarea and radius > minradius and radius < maxradius:
            possible_markpoints.append(center)
            possible_contours.append(x)
            STDERR.write("GOOD markpoint: area={:.2f}, radius={:.2f}; center=({:.2f},{:.2f})\n".format( ca, radius, center[0], center[1] ) )
        else:
            STDERR.write("BAD  markpoint: area={:.2f} not in ({:.2f},{:.2f}) OR radius={:.2f} not in ({:.2f},{:.2f}); center=({:.2f},{:.2f})\n".format( ca, minarea, maxarea, radius, minradius, maxradius, center[0], center[1] ) )

    return (possible_markpoints, possible_contours) 

#-----------------------------------------------------------------
def contour_filled_value(img, contour):
    cimg = np.zeros_like(img)
    cv.drawContours(cimg, [contour], 0 , color=255, thickness=-1)
    return np.mean(img[cimg==255]) 
#-----------------------------------------------------------------
def get_blobs(image, minarea, maxarea  ):
    threshval = 128
    ret, bw_image = cv.threshold(image, threshval, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    possible_markpoints = []
    possible_contours = []
    possible_radii = [] 
    # try to find all minimally nested contours. 
    retvalues = cv.findContours(bw_image,
                            cv.RETR_TREE,
                            cv.CHAIN_APPROX_SIMPLE
                            )
    if len(retvalues) == 2:
        contours = retvalues[0]
        hierarchy = retvalues[1][0]
    elif len(retvalues) == 3:
        contours = retvalues[1] 
        hierarchy = retvalues[2][0]
    else:
        raise Exception("Well, cv.findContours returned unknown list...")
    if DEBUG:
        STDERR.write("get_blobs: Found {} contours...\n".format(len(contours))) 
    contours_area = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_area[i] = cv.contourArea(c)
    for i in range(len(contours)):
        if hierarchy[i][3]>= 0: # it is inside: remove area
            if DEBUG: 
                STDERR.write(".")
            contours_area[hierarchy[i][3]] += -contours_area[i]
    for i in range(len(contours)):
        if ( contours_area[i] > minarea   and  contours_area[i] <  maxarea ):
            contours_perimeter = cv.arcLength(contours[i],True)
            if not ( contours_perimeter ** 2  < ISOPERIMETRIC_CONSTANT * np.pi * contours_area[i]):
                # isoperimetric inequality: L^2 >= 4 Pi A, with equality on circle 
                if DEBUG:
                    STDERR.write("get_blobs: ISOPERIMETRIC_CONSTANT test failed...\n") 
                continue
            filled_value=contour_filled_value(image,contours[i])
            if not ( filled_value < FILLED_THRES_CONTOUR): 
                if DEBUG:
                    STDERR.write("get_blobs: FILLED_THRES_CONTOUR test failed...\n") 
                continue
            center, radius = cv.minEnclosingCircle(contours[i])
            possible_markpoints.append(center)
            possible_contours.append(contours[i])
            possible_radii.append( radius )
            if DEBUG:
                STDERR.write(
"get_blob: area={:.2f}, filled_value={:.2f} radius={:.2f}; center=({:.2f},{:.2f})\n".format(
                contours_area[i] , filled_value, radius, center[0], center[1] ) )
    return (possible_markpoints, possible_contours,possible_radii ) 


#-----------------------------------------------------------------

def numpy_convert( t ) :
    return np.array( t ).astype(np.float32)

#-----------------------------------------------------------------
def find_affine_transform(src, dst):
    """ markhead,markfoot --> rotation """
    mapA = cv.getAffineTransform(numpy_convert( [src[0][0], src[0][1], src[1][0]] ),
        numpy_convert([ dst[0][0], dst[0][1], dst[1][0] ] ) )

    mapB = cv.getAffineTransform(numpy_convert([ src[0][0], src[0][1], src[1][1] ] ),
          numpy_convert( [ dst[0][0], dst[0][1], dst[1][1] ] ))

    mapC = cv.getAffineTransform(numpy_convert( [ src[0][0], src[1][0], src[1][1]] ),
          numpy_convert( [ dst[0][0], dst[1][0], dst[1][1]] ))

    mapD = cv.getAffineTransform(numpy_convert([ src[1][1], src[0][1], src[1][0]] ),
          numpy_convert( [ dst[1][1], dst[0][1], dst[1][0]] ))

    result_map = (mapA + mapB + mapC + mapD) / 4.0
    return result_map
#-----------------------------------------------------------------

GHOSTSCRIPT_COMMAND='/usr/bin/gs'
GHOSTSCRIPT_COMMAND_ARGS = "-dSAFER -dBATCH -dNOPAUSE -r200 -sDEVICE=pnggray -sPAPERSIZE=a4 -dLastPage=1 -dTextAlphaBits=1  -dGraphicsAlphaBits=1 -sOutputFile=%s-%%03d.png"
GHOSTSCRIPT_EXTRACT_COMMAND_ARGS = "-dSAFER -dBATCH -dNOPAUSE -r200 -sDEVICE=pnggray -sPAPERSIZE=a4 -dTextAlphaBits=1  -dGraphicsAlphaBits=1 -sOutputFile=%s-%%03d.png"


ENHANCE_CONTRAST_COMMAND = "/usr/bin/mogrify"
ENHANCE_CONTRAST_ARGS = "-auto-level -sigmoidal-contrast 9x60%% %s"


#-----------------------------------------------------------------
def listify(s):
    return s.split()

#-----------------------------------------------------------------

class OMR:
    def __init__(self, xml):
        self.savedPath = os.getcwd()
        base, ext = os.path.splitext(xml)
        pdffile = os.path.abspath(base+".pdf")
        self.tempdir = tempfile.mkdtemp('_tmp')
        os.chdir(self.tempdir)
        if VERBOSE:
            STDERR.write("extracting image from pdf file %s...\n\n" % pdffile)
            STDERR.write("executing command %s...\n\n" %
                         ([ GHOSTSCRIPT_COMMAND ]  + listify(  GHOSTSCRIPT_COMMAND_ARGS  % TMPBASE) + [ pdffile ] ))
        retval = subprocess.call([ GHOSTSCRIPT_COMMAND ]  + listify(  GHOSTSCRIPT_COMMAND_ARGS  % 
            TMPBASE  ) + [ pdffile ] , shell=False, stdout=STDERR, stderr=STDERR, stdin=None, close_fds=True)
        self.img = cv.imread(TMPBASE+"-001.png", 0)
        self.img_height, self.img_width  = self.img.shape
        self.img_smooth = mySmooth(self.img) 
        self.labelsdb = xml2db(xml)
        self.UIDlength = 0
        self.anslength = 0
        if 'UID' in self.labelsdb:
            self.UIDlength = get_numitems(list(self.labelsdb['UID'].keys()))
        if 'ans' in self.labelsdb:
            self.anslength = get_numitems(list(self.labelsdb['ans'].keys()))
        self.paperwidth = self.labelsdb['head']['paperwidth']
        self.paperheight = self.labelsdb['head']['paperheight']
        # height, width, channels = img.shape 
        self.mm_x = self.img_width / self.paperwidth
        self.mm_y = self.img_height / self.paperheight
        self.barcode_width = Round(barcode_width * self.mm_x * 1.02) # enlarge it a bit, it is in pixels
        self.barcode_height = Round(barcode_height * self.mm_y * 1.02 )

        self.labelslist = convert_to_list(
            self.labelsdb, (self.img_width, self.img_height))
        tmpvalues = [
            self.labelsdb['head']['bubblewidth'] * self.mm_x,
            self.labelsdb['head']['bubbleheight'] * self.mm_y
        ]
        tmpvalues.sort()
        self.bubbleradius = tmpvalues[-1] *0.50 ## radius in pixel
        self.align_markers = align_markers(self.img)
        self.barcodeLR = (Round(
            self.align_markers[0][1][0]+1.0*self.mm_x), Round(self.align_markers[0][1][1]-1*self.mm_y))
        self.barcodeUL = (
            self.barcodeLR[0]-self.barcode_width, self.barcodeLR[1]-self.barcode_height)
        self.minarea = 3.14 * (MINAREA_RATIO * self.bubbleradius) ** 2.0 ## in pixel squared
        if VERBOSE:
            STDERR.write("minarea=\t\t%f px^2\n" % self.minarea) 
        # 7.4 * self.minarea
        self.maxarea = 3.14 * (MAXAREA_RATIO * self.bubbleradius) ** 2.0
        if VERBOSE:
            STDERR.write("maxarea=\t\t%f px^2\n" % self.maxarea)
        self.minradius = MINRADIUS_RATIO * self.bubbleradius # in pixel! * self.mm_x
        if VERBOSE:
            STDERR.write("minradius=\t\t%f px = %f mm\n" %
                         (self.minradius, self.minradius / self.mm_x))
        self.maxradius = MAXRADIUS_RATIO * self.bubbleradius
        if VERBOSE:
            STDERR.write("bubbleradius=\t\t%f px = %f mm\n" %
                         (self.bubbleradius, self.bubbleradius/self.mm_x))
        if VERBOSE:
            STDERR.write("maxradius=\t\t%f px = %f mm\n" %
                         (self.maxradius, self.maxradius / self.mm_x))
        self.miny, self.maxy = self.align_markers[0][0][1], self.align_markers[1][0][1]
        self.afterimgs = []
        if VERBOSE:
            STDERR.write("Init complete...\n\n")

    def get_allbubblesimg(self):
        other_image = cv.cvtColor(self.img, cv.COLOR_GRAY2RGB)  # fino a che PIL non riesce...
        for r in self.labelslist:
            p = r[2]
            other_image = cv.circle(other_image, roundxy(p), Round(
                self.bubbleradius), (255, 0, 0), 2)
        return other_image

    def __del__(self):
        if VERBOSE:
            STDERR.write("Removing temp directory %s...\n" % self.tempdir)
        if not DEBUG:
            shutil.rmtree(self.tempdir)
        else:    
            STDERR.write(" >>>NOT! DEBUGGING...<<<\n")

    def Load(self, imagefile):
        if VVERBOSE:
            STDERR.write("Loading image %s...\n" % imagefile)
        marked_image = cv.imread(os.path.normcase(
            os.path.join(self.savedPath, imagefile)), 0 )
        if VVERBOSE:
            STDERR.write("[with size=%i x %i]... \n" % GetSize(marked_image))
        return marked_image

    def CorrectlyAlign(self, image):
        markers_orig = self.align_markers
        markers_scan = align_markers(image)
        mymap = find_affine_transform(markers_scan, markers_orig)
        warp_dst = cv.warpAffine(image, mymap, (self.img_width, self.img_height))
        return warp_dst

    def GetDataMatrix(self, image):
        LR = self.barcodeLR
        UL = self.barcodeUL
        img_barcode = (GetSubRect(image, cv.boundingRect(numpy_convert( [UL, LR] ) )))
        return img_barcode

    def find_closest(self, p):
        minpoint_ii = 0
        mindist = EuclDist(p, self.labelslist[0][2])
        for ii in range(len(self.labelslist)):
            thisdist = EuclDist(p, self.labelslist[ii][2])
            if thisdist < mindist:
                mindist = thisdist
                minpoint_ii = ii
        return (self.labelslist[minpoint_ii], mindist)

    def get_marklabels(self, imagefile):
        if VVERBOSE:
            STDERR.write("getting marklabels on : %s\n" % str(imagefile))
        marked_image = self.Load(imagefile)
        temp = self.CorrectlyAlign(marked_image) # temp is greyscale
        color_image = ( cv.cvtColor(temp, cv.COLOR_GRAY2BGR) ) 
        img_barcode = self.GetDataMatrix(color_image)
        dm = decode_datamatrix(img_barcode)
        if VVERBOSE:
            STDERR.write("decode_datamatrix: %s\n" % str(dm))
        # begin added new... 2014-02-18
        if dm:
            color_image = cv.rectangle(color_image, self.barcodeUL,
                      self.barcodeLR, (0, 255, 0), 2)
        else:
            color_image = cv.rectangle(color_image, self.barcodeUL,
                      self.barcodeLR, (0, 0, 255), 3)
        # end added new ...
        # now mark the align markers with small squares of size LL pixels
        LL =  2 
        for x in self.align_markers:
            for y in x:
                px, py = roundxy(y)
                color_image = cv.rectangle(color_image, (px-LL, py-LL),
                          (px+LL, py+LL), (255, 15, 0), 1)

        # find the marked labels by averaging, first
        LL = Round(self.bubbleradius *1.2 )
        filled_bubbles = []
        unfilled_bubbles = [] 
        for r in self.labelslist:
            px, py = roundxy(r[2])
            aa = ( Avg(GetSubRect(temp, (px-LL, py-LL, 2 * LL, 2 *  LL))))  # __HERE__
            if aa < FILLED_THRES:
                filled_bubbles.append(r)
                if DEBUG: 
                    cv.rectangle(color_image, (px-LL,py-LL), (px+LL,py+LL) , (0,206,0), thickness=2 )
                    STDERR.write(
                            "YES Appending bubble %s\nwith avg=%g\n" % (str(r), aa))
            else:
                if DEBUG:
                    cv.rectangle(color_image, (px-LL,py-LL), (px+LL,py+LL) , (255,150,0), thickness=2 )
                    STDERR.write(
                            "NOT Appending bubble %s\n with avg=%g\n" % (str(r),aa) )
        markpoints, contours , markpoint_radii = get_blobs(
            mySmooth(temp), self.minarea, self.maxarea )
        circle_radius = self.bubbleradius*1.2
        result = []
        int_radius=Round(self.bubbleradius * 2 )
        for p_i in range(len(markpoints)):
            p=markpoints[p_i]
            p_contour=contours[p_i]
            if p[1] > self.miny and p[1] < self.maxy:
                closest, error = self.find_closest(p)
                if DEBUG:
                    STDERR.write("markpoints: p={}; closest={}; error={}\n".format( p, closest, error) ) 
                if error < 1.3*circle_radius:
                    # it's supposed to be close to some bubbles...
                    if closest in filled_bubbles:
                        # ok, remove from the filled bubbles list
                        if markpoint_radii[p_i] > self.minradius and markpoint_radii[p_i]<self.maxradius :
                            # GREEN: ok circle
                            filled_bubbles.remove(closest)
                            result.append(closest)
                            cv.circle(color_image, roundxy(p), Round(
                                circle_radius), (0, 255, 0), 3)
                            if DEBUG:
                                STDERR.write("matching bubbles with blobs: OK with radius {}: {}\n".format(markpoint_radii[p_i], closest) )
                        elif markpoint_radii[p_i] >= self.maxradius :
                            # RED: too big circle 
                            cv.circle(color_image, roundxy(p), Round( markpoint_radii[p_i] ) , (0, 0, 255), 3 )
                            filled_bubbles.remove(closest)
                            if DEBUG:
                                STDERR.write("matching bubbles with blobs: TOO BIG with radius {}: {}\n".format(markpoint_radii[p_i], closest) )
                        elif markpoint_radii[p_i] <= self.minradius :
                            # ORANGE: too small circle
                            cv.circle(color_image, roundxy(p), Round( markpoint_radii[p_i] ) + 3 , (0, 140, 255), 3 )
                            if DEBUG:
                                STDERR.write("matching bubbles with blobs: TOO SMALL with radius {}: {}\n".format(markpoint_radii[p_i], closest) )
                        else:
                            raise Exception("Wait: this should not happen...")
                    else: # not in filled_bubbles...
                        # BLUE: closest was not filled? => too small filled mean. 
                        cv.circle(color_image, roundxy(p), Round(
                           circle_radius ), (255, 35 , 35), 3)
                        if DEBUG:
                            STDERR.write("matching bubbles with blobs: UNFILLED with radius {}: {}\n".format(markpoint_radii[p_i], closest) )
                        unfilled_bubbles.append(closest) 
                    if DEBUG: 
                        color_image=cv.drawContours(color_image, [p_contour],-1,(0,250,0),2)
                else:
                    # ignore those too far from anything. YELLOW
                    cv.circle(color_image, roundxy(p), Round(
                        circle_radius), (0, 255, 255), 3)
                    if DEBUG: 
                        color_image=cv.drawContours(color_image, [p_contour],-1,(0,250,250),2) #yellow
        for r in unfilled_bubbles:
            cv.circle(color_image, roundxy(r[2]), int_radius   , (0, 0, 255), 4) # blue

        for r in filled_bubbles:
            # all the remaining filled bubbles, with no mark: some problem!
            result.append(r) #append anyway! 
            cv.circle(color_image, roundxy(r[2]), Round(circle_radius) , (0, 255, 0), 3) #green
            cv.circle(color_image, roundxy(r[2]), int_radius , (203, 192, 255), 3) #pink
            if VVERBOSE:
                STDERR.write("matching bubbles with blobs: WARNING! Appending remaining filled bubble: %s\n" % str(r))
        return dm, result, color_image

    def Run(self, imagefile):
        dm, res, img = self.get_marklabels(imagefile)
        _, tmpimagefile = os.path.split(imagefile)
        if VVERBOSE:
            STDERR.write("converting file %s to pdf...\n" % imagefile)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        pilimg = Image.fromarray(img)
        pilimg.save("omr_%s.pdf" % tmpimagefile)
        self.afterimgs.append("omr_%s.pdf" % tmpimagefile)
        uid, ans = check_marked_items(get_marked_items(
            res), self.UIDlength, self.anslength)
        return "%(dm)s:\t:%(uid)s:%(ans)s:" % {'dm': dm, 'uid': uid, 'ans': ans}

    def ExtractPNG(self, pdffile):
        base, ext = os.path.splitext(os.path.basename(pdffile))
        if VERBOSE:
            STDERR.write("Extracting pngs from %s...\n" % pdffile)
        if VERBOSE:
            STDERR.write("Executing command %s...\n\n" % (
                [GHOSTSCRIPT_COMMAND] + listify ( GHOSTSCRIPT_EXTRACT_COMMAND_ARGS % (TMPTODOBASE+base)) + [ pdffile ]  ) )
        retval = subprocess.call([GHOSTSCRIPT_COMMAND] + listify(  GHOSTSCRIPT_EXTRACT_COMMAND_ARGS % (
            TMPTODOBASE+base) ) + [ pdffile ]  , shell=False , stdout=STDERR, stderr=STDERR, stdin=None, close_fds=True)
        result = [os.path.abspath(x) for x in glob.glob(
            "%s*.png" % (TMPTODOBASE+base))]
        for x in sorted(result):
            if MOGRIFY and ENHANCE_CONTRAST_COMMAND:
                if VERBOSE:
                    STDERR.write("enhancing image: '%s'...\n" % str(x)) 
                                 # str( [ENHANCE_CONTRAST_COMMAND]  + listify( ENHANCE_CONTRAST_ARGS % (x,) )) )
                retval = subprocess.call([ ENHANCE_CONTRAST_COMMAND ] + listify(ENHANCE_CONTRAST_ARGS  % (
                    x,) ), shell=False, stdout=STDERR, stderr=STDERR, stdin=None, close_fds=True)
        result.sort()
        return result
#-----------------------------------------------------------------

    def GetReport(self, outputfile):
        ALLBUBBLES = 'omr_allbubbles.pdf'
        if VERBOSE:
            STDERR.write("creating file %s ... \n" %
                         os.path.abspath(outputfile))
        img = self.get_allbubblesimg()
        pilimg = Image.frombytes("RGB", GetSize(img), (img.tobytes()))
        pilfont_size = Round(GetSize(img)[1] / 50.0)
        pilfont = ImageFont.truetype(
            "/usr/share/fonts/libertine/LinBiolinum_R.otf", pilfont_size)
        pildraw = ImageDraw.Draw(pilimg)
        y_offset = 2*pilfont_size
        for string_to_write in ["OMaRScan", "[@%s - %s]" % (FQDN, datetime.datetime.now().strftime("%a %Y-%m-%d, %X"))]:
            if PIL_M_version > 8:
                # damn the changes in names.
                string_size = pildraw.textlength(string_to_write, font=pilfont)
                x_offset = Round((GetSize(img)[0] - string_size)/2.0)
            else:    
                string_size = pildraw.textsize(string_to_write, font=pilfont)
                x_offset = Round((GetSize(img)[0] - string_size[0])/2.0)
            y_offset += pilfont_size
            pildraw.text((x_offset, y_offset), string_to_write,
                         font=pilfont, fill=(0, 0, 240))
        pilimg.save(ALLBUBBLES)
        if VERBOSE:
            STDERR.write("created file %s ... \n" %
                         os.path.abspath(ALLBUBBLES))
        output = pyPdf.PdfWriter()
        infoDict = output._info.get_object()
        infoDict.update({
            pyPdf.generic.NameObject('/Title'): pyPdf.generic.create_string_object(u'OMaRScan processed pages'),
            pyPdf.generic.NameObject('/Author'): pyPdf.generic.create_string_object(u'PIL+GhostScript+pyPdf'),
            pyPdf.generic.NameObject('/Subject'): pyPdf.generic.create_string_object(u'Marked Bubble Sheets'),
            pyPdf.generic.NameObject('/Creator'): pyPdf.generic.create_string_object(u'OMaRScan')
        })
        for f in ([ALLBUBBLES] + self.afterimgs):
            if VERBOSE:
                STDERR.write("Adding page %s ...\n" % f )
            f = os.path.join(self.tempdir, f)
            page = pyPdf.PdfReader(open(f, "rb")).pages[0]
            output.add_page(page)
        outputStream = open(outputfile, "wb")
        output.write(outputStream)
        outputStream.close()
        if VERBOSE:
            STDERR.write("Done! file %s created.\n" % outputfile)
        return
#-----------------------------------------------------------------


def get_number_of_pages(pdfs):
    result = 0
    for f in pdfs:
        if os.path.splitext(f)[1].lower() == '.pdf':
            fd = open(f, 'rb')
            result += len( pyPdf.PdfReader(fd).pages ) 
            fd.close()
        else:
            result += 1
    return result


#-----------------------------------------------------------------

def main(xml, pdfs, pdfoutput="/tmp/omr-output.pdf", statusfile=STDERR, outputtype="TXT"):
    STDERR.write(" ¯\_(ツ)_/¯ OMaRscan starting w/ python version: {}\n".format(sys.version))
    print_versions()
    number_of_pages = get_number_of_pages(pdfs)
    statusfile.write("ETA:?? sec (%i pages)\n" % number_of_pages)
    statusfile.flush()
    if number_of_pages > MAX_PAGES:
        statusfile.write("FAIL: Panic! Aborting! Too many images=%i > %i!!!\n" % (
            number_of_pages, MAX_PAGES))
        statusfile.flush()
        raise Exception("Too many images! (%i>%i)" %
                        (number_of_pages, MAX_PAGES))
    if VERBOSE:
        STDERR.write(
            "Beginning with xml-file %s and %i images...\ninitializing (extracting images)...\n" % (xml, len(pdfs)))
    omr = OMR(xml)
    todo = []
    for f in pdfs:
        if os.path.splitext(f)[1].lower() == '.pdf':
            images = omr.ExtractPNG(f)
            todo += images
        else:
            todo.append(f)
        statusfile.write("ETA:?? sec (extracted %i/%i)\n" %
                         (len(todo), number_of_pages))
        statusfile.flush()
    res = ""
    statusfile.write("ETA:?? sec (extraction finished)\n")
    statusfile.flush()
    if VERBOSE:
        STDERR.write("Processing %i images ...\n" % len(todo))
    start_time = time.time()
    numi = 0
    for f in todo:
        if VVERBOSE:
            STDERR.write("omr.Run(%s)\n" % f)
        res += "%s\n" % omr.Run(f)
        numi += 1
        ETA = (time.time()-start_time) * \
            (len(todo)*1.0/numi - 1) # + 1+len(todo)/2
        statusfile.write("ETA:%i sec [%i/%i]\n" % (int(ETA), numi, len(todo)))
        statusfile.flush()
    if VERBOSE:
        STDERR.write("Fin!\n\n")
    statusfile.write("(now writing OMR report):%i sec \n" % int(ETA))
    statusfile.flush()
    omr.GetReport(pdfoutput)
    return res


#-----------------------------------------------------------------
if __name__ == '__main__':
    xml, pdfs = get_opt()
    print(main(xml, pdfs))


