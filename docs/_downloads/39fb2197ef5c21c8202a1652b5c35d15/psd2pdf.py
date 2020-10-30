#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
psd2pdf.py 

Tools for drawing vector slides and images. 

DOCS: https://www.dlfer.xyz/var/psd2pdf

[help void]
Important: in imagemagick policy.xml: comment
<!-- <policy domain="coder" rights="none" pattern="PDF" /> -->
"""

import os
import sys
import tempfile, shutil
import argparse
import subprocess

#--------------------------------------------------------------------------
__version__='2019-03-11'
#--------------------------------------------------------------------------


#--------------------------------------------------------------------------
def convert_file(infile,outfile,cmd=[],doing='Converting',from_stdout=False):
        sys.stderr.write('{}: {} to {} ...\n'.format( doing, infile , outfile )  )
        if from_stdout:
            proc = subprocess.Popen(cmd,stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
            output,error=proc.communicate()
            if proc.returncode: 
                raise Exception("({}) ERROR with command {}!\n`{}`" .format (doing, cmd, error))
            fd=open(outfile,'wb')
            fd.write(output)
            fd.close()
        else:
            proc = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output,error=proc.communicate()
            if proc.returncode: 
                raise Exception("({}) ERROR with command {}!\n`{}`" .format (doing,cmd, error))
        return output   

#--------------------------------------------------------------------------
def get_image_size(pngfile):
    'identify -format "%w %h" tmpfile.png'
    out=convert_file(pngfile,None,cmd=['identify','-format','%w %h',pngfile],doing='Getting image size')
    w,h=out.split(b' ')
    return (int(w),int(h))

#--------------------------------------------------------------------------
def make_vect_potrace(psdfile,crop=False):
    "make a vector version with potrace"
    TMPFILEPNG='tmpfile.png'
    TMPFILEPNM='tmpfile.pnm'
    TMPFILENEXTPNM='tmpfilenext.pnm'
    TMPFILEPDF='tmpfile.pdf'
    bn,_=os.path.splitext(psdfile)
    OUTPUTPDF=bn+ '_vect.pdf' 
    convert_file( psdfile, TMPFILEPNG, cmd = ['convert',  "{}[0]".format(psdfile), TMPFILEPNG ] )
    width,height=get_image_size(TMPFILEPNG)
    turdsize = width*height / 16000
    sys.stderr.write("File size={} => turdsize={}\n".format((width,height),turdsize ))
    convert_file(TMPFILEPNG,TMPFILEPNM, cmd = ['pngtopnm', "-mix",  TMPFILEPNG ], from_stdout=True)
    # convert_file(TMPFILEPNM,TMPFILENEXTPNM,cmd = ['mkbitmap','--filter', '1',  '-xb2', '--grey',  TMPFILEPNM, '--output',TMPFILENEXTPNM ],doing='mkbitmap')
    convert_file(TMPFILEPNM,TMPFILENEXTPNM,cmd = ['mkbitmap','--filter', '4', '--blur','1', '--grey',  TMPFILEPNM, '--output',TMPFILENEXTPNM ],doing='mkbitmap')
    # convert_file(TMPFILENEXTPNM,OUTPUTPDF,cmd = ['potrace', '-b', 'pdf', '-c', '-q',  '-t', '0.1',  '--tight', '--output',OUTPUTPDF,TMPFILENEXTPNM ],doing='Potracing')
    convert_file(TMPFILENEXTPNM,OUTPUTPDF,cmd = ['potrace', '-b', 'pdf', '-c', '-q',  '-t', '100',  '--tight', '--output',OUTPUTPDF,TMPFILENEXTPNM ],doing='Potracing')
    return  OUTPUTPDF

#--------------------------------------------------------------------------
def make_vect_autotrace(psdfile,crop=False):
    "make a vector version with autotrace"
    # first  get a temporary directory? 

    TMPFILEPNG='tmpfile.png'
    TMPFILEPNM='tmpfile.pnm'
    TMPFILEPDF='tmpfile.pdf'
    bn,_=os.path.splitext(psdfile)
    OUTPUTPDF=bn+ '_vect.pdf' 

    convert_file( psdfile, TMPFILEPNG, cmd = ['convert',  "{}[0]".format(psdfile), TMPFILEPNG ] )
    sys.stderr.write("File size={}\n".format(get_image_size(TMPFILEPNG)))
    convert_file(TMPFILEPNG,TMPFILEPNM, cmd = ['pngtopnm', "-mix",  TMPFILEPNG ], from_stdout=True)
    convert_file(TMPFILEPNM,TMPFILEPDF,cmd = ['autotrace', TMPFILEPNM , '-despeckle-level','14', '--output-file' , TMPFILEPDF ],doing='Autotracing')
    if crop:
        convert_file(TMPFILEPDF,OUTPUTPDF,cmd= ['pdfcrop', TMPFILEPDF ,OUTPUTPDF ],doing='Cropping')
    else:
        convert_file(TMPFILEPDF,OUTPUTPDF, cmd= ['cp', TMPFILEPDF ,OUTPUTPDF ], doing='NOT Cropping')
    return  OUTPUTPDF


#--------------------------------------------------------------------------
def make_vect_png(psdfile,crop=False):
    "simply extract a PNG image"
    # first  get a temporary directory? 
    TMPFILEPNG='tmpfile.png'
    bn,_=os.path.splitext(psdfile)
    OUTPUT=bn+ '.png' 
    convert_file( psdfile, TMPFILEPNG, cmd = ['convert',  "{}[0]".format(psdfile), TMPFILEPNG ] )
    sys.stderr.write("File size={}\n".format(get_image_size(TMPFILEPNG)))
    if crop:
        convert_file(TMPFILEPNG,OUTPUT,cmd= ['convert', TMPFILEPNG ,'-trim', OUTPUT ],doing='Cropping')
    else:
        convert_file(TMPFILEPNG,OUTPUT, cmd= ['cp', TMPFILEPNG ,OUTPUT ], doing='NOT Cropping')
    return  OUTPUT

#--------------------------------------------------------------------------
def extract_all_layers(todo):
 lout=subprocess.check_output( ["identify", "-format", "\"%[scene] \"", todo ] , universal_newlines=True )
 lout=lout.replace("\"","").strip()
 layers=lout.split(" ")
 layers_png=[]
 for x in layers[1:]:
  sys.stderr.write("Extracting layer %s...\n"  % x)
  os.system("convert %s[0] %s[%s] \( -clone 0 -alpha transparent \) -swap 0 +delete -coalesce -compose src-over -composite %s-%s.png" % (todo,todo,x,todo,x))
  layers_png += ["%s-%s.png" % (todo,x)]
 # now composite and convert to pdf
 n_layers=len(layers_png)
 # first j=0
 output="output%02d.png"
 oldfile=layers_png[0]
 sys.stderr.write("""DEBUG: convert \"%s\" \"%s.pdf\"\n""" % (layers_png[0],output%0))
 os.system(""" convert \"%s\" \"%s.pdf\" """ % (layers_png[0],output%0))
 for j in range(1,n_layers):
  # sys.stderr.write("Trying j=%s...\n" % j )
  os.system("""convert \"%s\" \"%s\" -composite %s""" % (oldfile,layers_png[j],output % j) )
  # sys.stderr.write("Copying `%s'... \n" % (output % j ))
  oldfile=output%j
  # shutil.copy(output % j ,os.path.join(curdir,output % j ) )
  sys.stderr.write("""DEBUG: convert %s %s.pdf\n""" % (output%j,output%j))
  os.system(""" convert %s %s.pdf """ % (output%j,output%j))
 # then j>0
 return layers

#--------------------------------------------------------------------------
def get_into_tmpdir(todo):
 tmpdir=tempfile.mkdtemp()
 sys.stderr.write("Creating tempdir `{}'...\n" .format( tmpdir ) )
 curdir=os.getcwd()
 todofile=os.path.join(curdir,todo)
 output_basename,_=os.path.splitext(todofile)
 shutil.copy(todofile, os.path.join(tmpdir,todo))
 os.chdir(tmpdir)
 return tmpdir,curdir,output_basename


#--------------------------------------------------------------------------
def make_presentation(todo):
 tmpdir,curdir,output_basename=get_into_tmpdir(todo)
 extract_all_layers(todo)
 os.system("qpdf --empty --pages  output??.png.pdf  1-z -- \"%s\".pdf " % os.path.join(curdir,output_basename))
 sys.stderr.write("File `%s.pdf' created!\n" % output_basename) 
 sys.stderr.write("Cleaning up...\n")
 shutil.rmtree(tmpdir) 

#--------------------------------------------------------------------------
def old_make_presentation(psdfile):
    "make the multi-page PDF  presentation of a PSD"
    return 

#--------------------------------------------------------------------------

def do_make_vect(psdfile,crop=False,method='potrace'):
 tmpdir,curdir,output_basename=get_into_tmpdir(psdfile)
 if method=='autotrace':
     outputpdf=make_vect_autotrace(psdfile,crop=crop)
 elif method =='potrace':
     outputpdf=make_vect_potrace(psdfile,crop=crop)
 elif method =='png':
     outputpdf=make_vect_png(psdfile,crop=crop)
 else:
     raise Exception("Method {} not found!".format(method))
 os.system("cp {} {}" .format(outputpdf, os.path.join(curdir,outputpdf) ))
 sys.stderr.write("File `{}' created!\n" .format( outputpdf ) ) 
 sys.stderr.write("Cleaning up...\n")
 shutil.rmtree(tmpdir) 

#-------------------------------------------------------------------
def get_opt_parser():
    "get the arguments"
    if not check_self() :
       sys.stderr.write("Self-integrity checksum failed! Aborting...\nInstall a new clean version!\n" )
       sys.exit(1)

    parser=argparse.ArgumentParser(description='''psd2pdf.py: A tool for converting PSD graphics files''',
            epilog='[https://www.dlfer.xyz/var/psd2pdf]') 
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--autotrace','-a', help='make a vector-graphics version with autotrace', 
            action='store_true')
    group.add_argument('--potrace','-p', help='make a vector-graphics version with potrace', 
            action='store_true')
    group.add_argument('--png', help='convert and trim the PSD image', 
            action='store_true')
    parser.add_argument('--crop','-c', help='crop the final image', 
            action='store_true')
    parser.add_argument('psdfile', help='The input PSD file (multi-layered or raster)')
    return parser

#-------------------------------------------------------------------
#--BEGINSIG--
import base64;eval(compile(base64.b64decode('CmRlZiBjaGVja19zZWxmKCk6CiAgICAgcmV0dXJuIFRydWUKCmRlZiBnZXRfb3B0KCk6CiAgICBwYXJzZXI9Z2V0X29wdF9wYXJzZXIoKQogICAgcmV0dXJuIHBhcnNlci5wYXJzZV9hcmdzKCkKCgpkZWYgY2hlY2tfc2VsZigpOgogaW1wb3J0IG9zLCBoYXNobGliLHJlCiBNRV9iYXNlLE1FX2V4dD1vcy5wYXRoLnNwbGl0ZXh0KG9zLnBhdGguYWJzcGF0aChfX2ZpbGVfXykpCiBNRT1NRV9iYXNlKycucHknCiBhbGw9b3BlbihNRSwncicpLnJlYWQoKS5kZWNvZGUoJ3V0Zi04JykKIHA9YWxsLmluZGV4KCJcbiIpCiByZWc9cmUuY29tcGlsZSgiIy0tQkVHSU4iKyJTSUctLXwjLS1FTkQiKyJTSUctLSIscmUuTSBhbmQgcmUuRE9UQUxMICkKIGJvZHlfZmlyc3QsaGlkZGVuLGJvZHlfbGFzdD1yZXM9cmVnLnNwbGl0KGFsbFtwKzE6XSkKIGw9bGVuKGJvZHlfZmlyc3Quc3RyaXAoKSkrbGVuKGJvZHlfbGFzdC5zdHJpcCgpKQogbD1oYXNobGliLnNoYTIyNCgoYm9keV9maXJzdC5zdHJpcCgpICsgYm9keV9sYXN0LnN0cmlwKCkpLmVuY29kZSgndXRmLTgnKSkuaGV4ZGlnZXN0KCkKIGV4cGVjdF9sPSc0ODQ3OGYxZmQ2OTg1YzY1Yjc4MzgzMmIwNGFkMjJhNmNjZTYyNDEzM2MyMDllNDkxYjRjMjY1YycKIGlmIGwgIT0gZXhwZWN0X2w6CiAgcmV0dXJuIEZhbHNlCiBlbHNlOgogIHJldHVybiBUcnVlCg=='),'<string>','exec'))
#--ENDSIG--
#-------------------------------------------------------------------


#--------------------------------------------------------------------------
def main():
    # first get the options
    args=get_opt()
    if args.autotrace:
        do_make_vect(args.psdfile,crop=args.crop,method='autotrace')
    elif args.potrace:
        do_make_vect(args.psdfile,crop=args.crop,method='potrace')
    elif args.png:
        do_make_vect(args.psdfile,crop=args.crop,method='png')
    else:
        make_presentation(args.psdfile)
    return     


#--------------------------------------------------------------------------
if __name__=='__main__':
    main()


