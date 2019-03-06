#!/usr/bin/env python
# -*- coding: utf-8 -*-

# get data from ~/.esse3rc


__version__='Wednesday 2019-03-06'

__doc__=r"""
USAGE: esse3.py [options] [argument]


# Version: Wednesday 2019-03-06

OPTIONS:
	--help|-h
	--uid Nomefile.xls 	# lista iscritti :matricola:cognome,nome:
	--pdf Nomefile.xls 	# registro pdf
	--call 			# chiama per firma digitale
	--yml 			# genera il file csv del registro delle lezioni da yml
	--baseoutput|-b=[base]

FILES:
	~/.esse3rc 	(options file)
---

(C) DLFerrario http://www.dlfer.xyz
"""
XLRD_URL='http://pypi.python.org/pypi/xlrd'
SERIAL_URL='http://pypi.python.org/pypi/pyserial'
VERBOSE=False

#-------------------------------------------------------------------


latex_template=r"""
\documentclass[12pt,twoside,a4paper]{article}
\RequirePackage{lastpage}
\RequirePackage{fancyhdr}
\usepackage[includeheadfoot,a4paper]{geometry}
\geometry{a4paper,margin={0.8in,1in}}
\usepackage{color}
\definecolor{gray}{gray}{0.60}
\usepackage[no-math]{fontspec}
\RequirePackage{xltxtra}
\RequirePackage{xunicode}
\setmainfont[Mapping=tex-text]{Linux Libertine}
\defaultfontfeatures{Mapping=tex-text}
\fancypagestyle{plain}{%%
\renewcommand{\headrulewidth}{0.6pt}
\chead{}
\lhead{\tt %(headline)s}
\rhead{\tt \thepage/\pageref{LastPage}}
\lfoot{{}}
\cfoot{{}}
\rfoot{{}}
}
\setlength{\headheight}{16pt}
\pagestyle{plain}
\RequirePackage{enumerate}
\renewcommand{\labelenumi}{{\itshape(\alph{enumi})}}
\usepackage{multirow}
\usepackage[italian]{babel}
\usepackage{tikz}
\begin{document}
%% BEGIN content
%(body)s
%% END content
\end{document}
"""


#-------------------------------------------------------------------
import string,os
import time,sys
import getopt
import tempfile, shutil
import StringIO
import ConfigParser
import re
import datetime

#-------------------------------------------------------------------
ESSE3FILENAME='.esse3rc'
ESSE3KEYS=['SERIAL_PORT', 'TELENUMBER', 'PIN']

def getesse3values():
 db={}
 for k in ESSE3KEYS:
   db[k]=None
 filename=os.path.expanduser('~/'+ESSE3FILENAME)
 if os.path.exists(filename):
  config = StringIO.StringIO()
  config.write("[dummysection]\n\n")
  config.write(open(filename, 'r').read())
  config.seek(0, os.SEEK_SET)
  cp = ConfigParser.SafeConfigParser()
  cp.readfp(config)
  for k in ESSE3KEYS:
    if cp.has_option('dummysection',k):
      db[k]= cp.get('dummysection',k)
    else:
      sys.stdout.write("Option '%s' missing in options file %s...\n" % (k,filename))
      sys.stdout.write("Enter value of '%s'" % k)
      db[k]=raw_input(" >> ")
 else:
  sys.stdout.write("Options file %s missing... creating one...\n" % (filename,))
  fd=open(filename,'w')
  fd.write("## File generato automaticamente....\n" )
  for k in ESSE3KEYS:
    sys.stdout.write("Enter value of '%s'" % k)
    db[k]=raw_input(" >> ")
    fd.write("%s = %s\n" % (k,db[k]))
  fd.close()
  sys.stdout.write(" => File %s generated!\n" % filename)
 return [db[k] for k in ESSE3KEYS] 
#-------------------------------------------------------------------
#--BEGINSIG--
import base64;eval(compile(base64.b64decode('CmRlZiBjaGVja19zZWxmKCk6CiByZXR1cm4gVHJ1ZQoKZGVmIGdldF9vcHQoKToKIGlmIG5vdCBjaGVja19zZWxmKCkgOgogIHN5cy5zdGRlcnIud3JpdGUoIlNlbGYtaW50ZWdyaXR5IGNoZWNrc3VtIGZhaWxlZCEgQWJvcnRpbmcuLi5cbkluc3RhbGwgYSBuZXcgY2xlYW4gdmVyc2lvbiFcbiIgKQogIHN5cy5leGl0KDEpCiBET1BERj1GYWxzZQogRE9VSUQ9RmFsc2UKIERPTk9USElORz1UcnVlCiBCQVNFT1VUUFVUPSdlc3NlM19vdXRwdXQnCiBVU0VTVERPVVQ9VHJ1ZQogdHJ5OgogIG9wdHMsIGFyZ3MgPSBnZXRvcHQuZ2V0b3B0KHN5cy5hcmd2WzE6XSwgImhiOiIsIFsiaGVscCIsICJiYXNlb3V0cHV0PSIsInVpZCIsInBkZiIsImNhbGwiLCJ5bWwiXSkKIGV4Y2VwdCBnZXRvcHQuR2V0b3B0RXJyb3IsIGVycjoKICBzeXMuc3RkZXJyLndyaXRlKCIlc1xuIiAlIHN0cihlcnIpICkKICBzeXMuc3RkZXJyLndyaXRlKCJbb3B0aW9uIC0taGVscCBmb3IgaGVscF1cbiIpCiAgc3lzLmV4aXQoMSkKIGZvciBvLGEgaW4gb3B0czoKICBpZiBvIGluICgiLWgiLCAiLS1oZWxwIik6CiAgIHByaW50IF9fZG9jX18KICAgcmV0dXJuIAogIGVsaWYgbyBpbiAoIi1iIiwgIi0tYmFzZW91dHB1dCIpOgogICBCQVNFT1VUUFVUID0gYQogICBVU0VTVERPVVQ9RmFsc2UKICBlbGlmIG8gaW4gKCItLWNhbGwiLCk6CiAgIHByaW50ICJQcm92aWFtbyBpbCBnc20uLi4iCiAgIFNFUklBTF9QT1JULFRFTEVOVU1CRVIsUElOPWdldGVzc2UzdmFsdWVzKCkKICAgY2FsbGdzbShTRVJJQUxfUE9SVCxURUxFTlVNQkVSLFBJTikKICAgcmV0dXJuIAogIGVsaWYgbyBpbiAoIi0tdWlkIiwpOgogICBET1VJRD1UcnVlCiAgIERPTk9USElORz1GYWxzZQogIGVsaWYgbyBpbiAoIi0tcGRmIiwpOgogICBET1BERj1UcnVlCiAgIERPTk9USElORz1GYWxzZQogIGVsaWYgbyBpbiAoIi0teW1sIiwpOgogICB0b2RvZmlsZT1hcmdzWzBdCiAgIGIsXz1vcy5wYXRoLnNwbGl0ZXh0KHRvZG9maWxlKQogICB5bWx0b2NzdihhcmdzWzBdLGIgKyAiLmNzdiIpCiAgIHJldHVybiAKCiBpZiBsZW4oYXJncyk9PTAgb3IgRE9OT1RISU5HOgogIHByaW50ICJbZXNzZTMucHkgLS1oZWxwIGZvciBoZWxwXSIKICBzeXMuZXhpdCgxKQogeGxzZmlsZT1hcmdzWzBdCiBFUz1Fc3NlMyh4bHNmaWxlKQogaWYgRE9VSUQ6CiAgaWYgVVNFU1RET1VUOgogICBFUy5tYWtldWlkKHN5cy5zdGRvdXQpCiAgZWxzZToKICAgRVMubWFrZXVpZChmaWxlKEJBU0VPVVRQVVQrJy51aWQnLCd3JykpCiAgIHByaW50ICJcbiA9PT4gZmlsZSAiLCBCQVNFT1VUUFVUKycudWlkJywgIiBnZW5lcmF0by4iCiBpZiBET1BERjoKICBFUy5tYWtlcGRmKEJBU0VPVVRQVVQpCiAgCgpkZWYgY2hlY2tfc2VsZigpOgogaW1wb3J0IG9zLCBoYXNobGliLHJlCiBNRV9iYXNlLE1FX2V4dD1vcy5wYXRoLnNwbGl0ZXh0KG9zLnBhdGguYWJzcGF0aChfX2ZpbGVfXykpCiBNRT1NRV9iYXNlKycucHknCiBhbGw9ZmlsZShNRSkucmVhZCgpCiBwPWFsbC5pbmRleCgiXG4iKQogcmVnPXJlLmNvbXBpbGUoIiMtLUJFR0lOIisiU0lHLS18Iy0tRU5EIisiU0lHLS0iLHJlLk0gYW5kIHJlLkRPVEFMTCApCiBib2R5X2ZpcnN0LGhpZGRlbixib2R5X2xhc3Q9cmVzPXJlZy5zcGxpdChhbGxbcCsxOl0pCiBsPWxlbihib2R5X2ZpcnN0LnN0cmlwKCkpK2xlbihib2R5X2xhc3Quc3RyaXAoKSkKIGw9aGFzaGxpYi5zaGEyMjQoYm9keV9maXJzdC5zdHJpcCgpICsgYm9keV9sYXN0LnN0cmlwKCkpLmhleGRpZ2VzdCgpCiBleHBlY3RfbD0nNzRmODM1NjQzMDU1YzVkOWYyZTI1NjFjYTAyMTFkMzk4ODdiNGI4YjFjZDExYWU2YjFjMDhkNjknCiBpZiBsICE9IGV4cGVjdF9sOgogIHJldHVybiBGYWxzZQogZWxzZToKICByZXR1cm4gVHJ1ZQo='),'<string>','exec'))
#--ENDSIG--
#-------------------------------------------------------------------
class Esse3:
 def __init__(self,xlsfile):
  try:
   import xlrd
  except:
   sys.stderr.write("Please first install XLRD: %s\n" % XLRD_URL)
   sys.stderr.write("[Try 'easy_install -U xlrd'] or [Try 'apt install python-xlrd'] or ['pip install xlrd'] \n")
   sys.exit(1)
  self.xlsfile=xlsfile
  book=xlrd.open_workbook(xlsfile)
  self.sheet=book.sheet_by_name('esse3')
  self.nrows=self.sheet.nrows
  self.SUBSET=int(self.sheet.row_values(0)[3])
  if self.sheet.row_values(4)[1]=='FIRST_DYN_COL':
      sys.stderr.write("WTF! It's 2019 and Wrong Format Again...\n")
      self.FIRST_ROW=self.sheet.col_values(0).index('#')+1
  else:    
      self.FIRST_ROW=int(self.sheet.row_values(4)[1])
  ## self.FIRST_DYN_COL=int(self.sheet.row_values(4)[3]) # NEVER USED ANYWAY...
  cellcontent=self.sheet.row_values(self.FIRST_ROW-1)[0]
  if cellcontent != '#':
   errmsg="Content of cell [%i,%i] should be '#' but is '%s' instead...\nXLS TABLE FORMAT ERROR!!!\n" %( self.FIRST_ROW,0,cellcontent)
   sys.stderr.write(errmsg)
   if cellcontent == '1': 
    sys.stderr.write("WARNING: CHANGING WRONG FIRST_ROW...\n")
    self.FIRST_ROW += -1 
   else:
    raise Exception("UNRECOVERABLE FORMAT ERROR\n")
  # ugly hack... 
  if self.nrows != self.FIRST_ROW+self.SUBSET :
   errmsg="nrows(%i) != FIRST_ROW(%i) + SUBSET(%i)\n" % (self.nrows, self.FIRST_ROW,self.SUBSET) 
   raise Exception(errmsg)
  self.ALLTT=''
  self.DESCRIZIONE=''
  for x in range(5,self.FIRST_ROW-2):
   r=self.sheet.row_values(x)
   nl=" ".join(r)
   self.ALLTT += nl + "\n" 
   if r[0] == u'Descrizione Appello':
    self.DESCRIZIONE=r[3]
  self.HEADLINE=self.sheet.row_values(6)[0] + " -- " + self.DESCRIZIONE.upper() 
  self.iscritti=[]
  for x in range(self.FIRST_ROW,self.nrows):
   # print sheet.row_types(x)
   dati=self.sheet.row_values(x)
   cognome,nome,matricola=dati[3],dati[4],dati[2]
   cognome=string.capwords(cognome.lower()) # elminare maiuscolo COBOL
   nome=string.capwords(nome.lower())
   self.iscritti.append( (cognome,nome,matricola))

 def makeuid(self,out):
  for x in self.iscritti:
   out.write((":%s, %s:%s:\n" % x).encode('utf-8'))
  return 

 def makepdf(self,baseoutput):
  BODY=r"""{\footnotesize
\noindent\begin{verbatim}
""" +  self.ALLTT + r"""\end{verbatim}}""" + "\\hrule\\vspace{2mm}\\hrule\n\n\\vspace{1cm}"
  progressivo=0
  for cognome,nome,matricola in self.iscritti:
   # print sheet.row_types(x)
   progressivo += 1
   usercomment="? " + self.sheet.row_values(6)[0] + " - 4 CFU ?" ## __TODO__ attività giusta
   # TODO: get number of CFU and Codice attività
   BODY += r"""
\noindent
\begin{tikzpicture}
\node (tbl) [inner sep=0pt] {%%
\begin{tabular}{p{0.57\textwidth}|p{0.2\textwidth}|p{0.15\textwidth}}
%%\hline
\rule[-0.3cm]{0pt}{1.8cm}
{\tt\bfseries %i.~%s, %s \hfill %s} &
{\tt\bfseries data:} \color{gray}\hrulefill &
{\tt\bfseries voto:} \color{gray}\hrulefill \\
%% \hline
%% \multicolumn{3}{l}{%%
%% \rule[0.0cm]{0pt}{12pt}
%% {\tt %s} } \\
\hline
\multicolumn{3}{l}{
\rule[-0.3cm]{0pt}{2.4cm}
}
\\
%% \hline
\end{tabular}
};
 \draw [rounded corners=.5em] (tbl.north west) rectangle (tbl.south east);
 \end{tikzpicture}
 
 \vspace{12pt}
""" % (progressivo,cognome, nome, matricola,usercomment)
  tmpdir=tempfile.mkdtemp()
  curdir=os.getcwd()
  os.chdir(tmpdir)
  fd=open('%s.tex' % baseoutput,'w') ## __TODO__ output file
  fd.write( (latex_template % {'body':BODY, 'headline':self.HEADLINE}).encode('utf-8') )
  fd.close()
  os.system('xelatex %s.tex' % baseoutput)
  os.system('xelatex %s.tex' % baseoutput )
  shutil.copy('%s.pdf' % baseoutput ,os.path.join(curdir,baseoutput+'.pdf'))
  shutil.rmtree(tmpdir)
  print "\n  ==>file ", baseoutput + '.pdf', "generato"
  return 

#-----------------------------------------------------------------------

def getgsm(serial_port):
 """ TODO: get a working gsm by scanning """
 try:
  import serial
 except:
  sys.stderr.write("Please first install pySerial: %s\n" % SERIAL_URL )
  sys.stderr.write("[Try 'easy_install -U pyserial']\n")
  sys.exit(1)
 ser = serial.Serial(
    port=serial_port,
    baudrate=115200,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS,
    timeout=1
)
 if not ser.isOpen() :
  raise Exception("Serial Line Down")
 ser.write('ATI\r\n')
 sys.stdout.write(expectprompt(ser))
 ser.write('ATM2\r\n')
 sys.stdout.write(expectprompt(ser))
 ser.write('ATL3\r\n')
 sys.stdout.write(expectprompt(ser))
 return ser


def expectprompt(ser):
 time.sleep(1)
 out=''
 while ser.inWaiting() > 0:
  buf=ser.read(1)
  out += buf
 return out
 
ALLOWEDCHARS='0123456789'

def partial_string(i,n):
 return "\r[" + ("#"*i) + ("-"*(n-i) ) + "]"

def callgsm(serial_port,telenumber,pin):
 ser = getgsm(serial_port)
 print 'Calling...'
 ser.write('ATD ' + telenumber + ';' + '\r\n')
 exp=expectprompt(ser)
 if VERBOSE: 
  sys.stderr.write(exp)
 else:
  sys.stderr.write("\n"+("-"*80)+"\n")
 sys.stdout.write("Input 4 cifre + <Return>: ")
 cifre=raw_input(">> ")
 cifre=cifre.strip()
 numcifre=len(cifre);
 tmpii=0
 for x in cifre:
  if not x in ALLOWEDCHARS:
   print "Cifre Sbagliate: ", x, " not in ", ALLOWEDCHARS
  else:
   tmpii += 1
   ser.write('AT+VTS=' + x + '\r\n')
   exp=expectprompt(ser)
   if VERBOSE: 
    sys.stderr.write(exp)
   else:
    sys.stderr.write(partial_string(tmpii,numcifre))
 sys.stdout.write("\nPress <Return> per inviare il PIN di otto cifre...")
 ret=raw_input(">> ")
 lenpin=len(pin)
 tmpii=0
 for x in pin:
  tmpii += 1
  ser.write('AT+VTS=' + x + '\r\n')
  exp=expectprompt(ser)
  if VERBOSE: 
   sys.stderr.write(exp)
  else:
   sys.stderr.write(partial_string(tmpii,lenpin))
 sys.stdout.write("\nPress <Return> per riagganciare..." )
 ret=raw_input(">> ")
 ser.write('AT+CHUP\r\n')
 sys.stderr.write(expectprompt(ser))
 print "\n...closing...."
 ser.close()


#-----------------------------------------------------------------------
# take a yaml logbook and convert it to esse3 CSV format
# Data (gg/mm/aaaa) /Ora Inizio (hh:mm) Ora Fine (hh:mm)  / Titolo / Descrizione  (con colonne vuote in mezzo)
ORARIO_NAMES=['orario']
ANNO_NAMES=['anno','year']
GIORNI_NAMES=['lun','mar','mer','gio','ven','sab','dom']
MESE_NAMES=['GEN','FEB','MAR','APR','MAG','GIU','LUG', 'AGO','SET','OTT','NOV','DIC']
TYPE_NAMES=['type','tipo']

def parse_header(db):
    result = {} 
    for x in ANNO_NAMES:
        if db.has_key(x):
            result['anno']=int(db[x])
            break
    for x in TYPE_NAMES:
        if db.has_key(x):
            result['type']=db[x]
            break
    for x in ORARIO_NAMES:    
        if db.has_key(x):
            orario={}
            for giorno in db[x].keys():
                if not giorno in GIORNI_NAMES:
                    raise Exception("Giorno {} not valid\n".format(giorno))
                orario[giorno]=(db[x][giorno]).split('-')
            result['orario']=orario
            break
    return result

def parse_body_parts(body_parts,header_db):
    j=0
    result=[]
    for body_db in body_parts:
        result += parse_body(body_db,header_db,year_offset=j)
        j += 1
    return result     


def parse_body(body_db,header_db,year_offset=0):
    result = [] 
    monthes_indices=[MESE_NAMES.index(m) for m in body_db.keys()]
    monthes_indices.sort()
    for m in monthes_indices:
        month=MESE_NAMES[m]
        if not month in MESE_NAMES:
            raise Exception("MESE {} not valid\n".format(month) )
        month_number=MESE_NAMES.index(month)+1
        for day_string in body_db[month]:
            sys.stderr.write("  parsing %s: %s\n" % (month,dirty_trick(day_string,back=True)))
            day_tokens=day_string.split()
            day_date=datetime.date(header_db['anno']+year_offset,month_number,int(day_tokens[0]))
            week_day=GIORNI_NAMES[day_date.weekday()]
            orario=header_db['orario'][week_day]
            act_type=header_db['type']
            if not week_day in header_db['orario']:
                raise Exception("Problem: week_day '{}' not in orario!".format(week_day))
            if day_tokens[1][0]=='*':
                desc= " ".join(day_tokens[2:]) 
            else:    
                desc= " ".join(day_tokens[1:]) 
            desc=dirty_trick(desc,back=True)
            sys.stderr.write("  -> ore= {}\n".format(numero_ore(orario[0],orario[1])))
            result += [(day_date.strftime("%d/%m/%Y"), orario[0],orario[1], "" , "{}".format(act_type).encode('utf-8'), "", desc.encode('utf-8'),desc.encode('utf-8')  ) ]
    return result

def dirty_trick(s, back=False):
    if back:
        return re.sub('__COLON_XXX_SPACE__',': ',s)
    else:    
        return re.sub(': ','__COLON_XXX_SPACE__',s)


def numero_ore(a,b):
    time_FMT = '%H:%M'
    return (datetime.datetime.strptime(b, time_FMT) - datetime.datetime.strptime(a, time_FMT)).total_seconds() / (60*60.0)
    

def ymltocsv(yamlfile,csvfile):
    # import oyaml as yaml to have it ordered?
    import yaml
    import csv
    import StringIO
    import re
    reg_itemline=re.compile(r"(?P<blank>\s*?)- (?P<content>.*?)$")
    yaml_content=''
    for raw_line in file(yamlfile).readlines():
        reg_search=reg_itemline.search(raw_line)
        if reg_search:
            yaml_content += "%s- %s\n" % (reg_search.group('blank'), dirty_trick( reg_search.group('content') ) ) 
        else:
            yaml_content += raw_line
    yaml_stream=StringIO.StringIO()
    yaml_stream.write(yaml_content)
    yaml_stream.seek(0)
    tokens=list(yaml.safe_load_all(yaml_stream))

    # tokens=list(yaml.safe_load_all(file(yamlfile)))
    header=tokens[0]
    body_parts=tokens[1:]
    hdb=parse_header(header)
    all_data= parse_body_parts(body_parts,hdb) 
    total_time=0 
    with open(csvfile, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in all_data:
            total_time += numero_ore(row[1],row[2])
            csvwriter.writerow(row)
    csvfile.close()        
    sys.stderr.write(
"""
Number of hours: {}
File {} created
Open with options:   Unicode, Italia, separated by semicolon, text_delimiter=\", Quoted field as text.
""".format(total_time, csvfile.name))
    return 

#-----------------------------------------------------------------------

if __name__=='__main__':
 get_opt()



