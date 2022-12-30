#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# get data from ~/.esse3rc


from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from six.moves import input
__version__='2022-12-30'

__doc__=r"""
USAGE: esse3.py [options] [argument]


# Version: 2022-12-30

OPTIONS:
    --help|-h
    --uid Nomefile.xls  # lista iscritti :cognome,nome:matricola:
    --pdf Nomefile.xls  # registro pdf
    --guid              # Simple GUI per convertire XLSX -> UID
    --call              # chiama per firma digitale (obsoleto)
    --yml               # genera il file csv del registro delle lezioni da yml
    --blankyml          # genera il un file blank yml: sem-start e sem-end formato ISO
    --baseoutput|-b=[base]

FILES:
~/.esse3rc  (options file)
---

(C) DLFerrario http://www.dlfer.xyz
"""
XLRD_URL='http://pypi.python.org/pypi/xlrd'
PYSIMPLEGUI_URL='https://pypi.org/project/PySimpleGUI/'
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
import io
import six.moves.configparser
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
  config = io.StringIO()
  config.write("[dummysection]\n\n")
  config.write(open(filename, 'r').read())
  config.seek(0, os.SEEK_SET)
  cp = six.moves.configparser.SafeConfigParser()
  cp.readfp(config)
  for k in ESSE3KEYS:
    if cp.has_option('dummysection',k):
      db[k]= cp.get('dummysection',k)
    else:
      sys.stdout.write("Option '%s' missing in options file %s...\n" % (k,filename))
      sys.stdout.write("Enter value of '%s'" % k)
      db[k]=input(" >> ")
 else:
  sys.stdout.write("Options file %s missing... creating one...\n" % (filename,))
  fd=open(filename,'w')
  fd.write("## File generato automaticamente....\n" )
  for k in ESSE3KEYS:
    sys.stdout.write("Enter value of '%s'" % k)
    db[k]=input(" >> ")
    fd.write("%s = %s\n" % (k,db[k]))
  fd.close()
  sys.stdout.write(" => File %s generated!\n" % filename)
 return [db[k] for k in ESSE3KEYS] 
#-------------------------------------------------------------------
#--BEGINSIG--
import base64;eval(compile(base64.b64decode(b'CmRlZiBjaGVja19zZWxmKCk6CiByZXR1cm4gVHJ1ZQoKZGVmIGdldF9vcHQoKToKIGlmIG5vdCBjaGVja19zZWxmKCkgOgogIHN5cy5zdGRlcnIud3JpdGUoIlNlbGYtaW50ZWdyaXR5IGNoZWNrc3VtIGZhaWxlZCEgQWJvcnRpbmcuLi5cbkluc3RhbGwgYSBuZXcgY2xlYW4gdmVyc2lvbiFcbiIgKQogIHN5cy5leGl0KDEpCiBET1BERj1GYWxzZQogRE9VSUQ9RmFsc2UKIERPTk9USElORz1UcnVlCiBCQVNFT1VUUFVUPSdlc3NlM19vdXRwdXQnCiBVU0VTVERPVVQ9VHJ1ZQogdHJ5OgogIG9wdHMsIGFyZ3MgPSBnZXRvcHQuZ2V0b3B0KHN5cy5hcmd2WzE6XSwgImhiOiIsIFsiaGVscCIsICJiYXNlb3V0cHV0PSIsInVpZCIsInBkZiIsImNhbGwiLCJndWlkIiwieW1sIiwiYmxhbmt5bWwiXSkKIGV4Y2VwdCBnZXRvcHQuR2V0b3B0RXJyb3IgYXMgZXJyOgogIHN5cy5zdGRlcnIud3JpdGUoIiVzXG4iICUgc3RyKGVycikgKQogIHN5cy5zdGRlcnIud3JpdGUoIltvcHRpb24gLS1oZWxwIGZvciBoZWxwXVxuIikKICBzeXMuZXhpdCgxKQogZm9yIG8sYSBpbiBvcHRzOgogIGlmIG8gaW4gKCItaCIsICItLWhlbHAiKToKICAgcHJpbnQoX19kb2NfXykKICAgcmV0dXJuIAogIGVsaWYgbyBpbiAoIi1iIiwgIi0tYmFzZW91dHB1dCIpOgogICBCQVNFT1VUUFVUID0gYQogICBVU0VTVERPVVQ9RmFsc2UKICBlbGlmIG8gaW4gKCItLWNhbGwiLCk6CiAgIHByaW50KCJQcm92aWFtbyBpbCBnc20uLi4iKQogICBTRVJJQUxfUE9SVCxURUxFTlVNQkVSLFBJTj1nZXRlc3NlM3ZhbHVlcygpCiAgIGNhbGxnc20oU0VSSUFMX1BPUlQsVEVMRU5VTUJFUixQSU4pCiAgIHJldHVybiAKICBlbGlmIG8gaW4gKCItLXVpZCIsKToKICAgRE9VSUQ9VHJ1ZQogICBET05PVEhJTkc9RmFsc2UKICBlbGlmIG8gaW4gKCItLXBkZiIsKToKICAgRE9QREY9VHJ1ZQogICBET05PVEhJTkc9RmFsc2UKICBlbGlmIG8gaW4gKCItLXltbCIsKToKICAgdG9kb2ZpbGU9YXJnc1swXQogICBiLF89b3MucGF0aC5zcGxpdGV4dCh0b2RvZmlsZSkKICAgeW1sdG9jc3YoYXJnc1swXSxiICsgIi5jc3YiKQogICByZXR1cm4gCiAgZWxpZiBvIGluICgiLS1ibGFua3ltbCIsKToKICAgdG9kb2ZpbGU9YXJnc1swXQogICBiLF89b3MucGF0aC5zcGxpdGV4dCh0b2RvZmlsZSkKICAgeW1sdG9ibGFua3ltbChhcmdzWzBdLGIgKyAiX2JsYW5rLnltbCIpCiAgIHJldHVybiAKICBlbGlmIG8gaW4gKCItLWd1aWQiLCk6CiAgIGd1aWQoKQogICByZXR1cm4gCgogaWYgbGVuKGFyZ3MpPT0wIG9yIERPTk9USElORzoKICBwcmludCgiW2Vzc2UzLnB5IC0taGVscCBmb3IgaGVscF0iKQogIHN5cy5leGl0KDEpCiB4bHNmaWxlPWFyZ3NbMF0KIEVTPUVzc2UzKHhsc2ZpbGUpCiBpZiBET1VJRDoKICBpZiBVU0VTVERPVVQ6CiAgIEVTLm1ha2V1aWQoc3lzLnN0ZG91dC5idWZmZXIpCiAgZWxzZToKICAgRVMubWFrZXVpZChvcGVuKEJBU0VPVVRQVVQrJy51aWQnLCd3YicpKQogICBwcmludCgiXG4gPT0+IGZpbGUgIiwgQkFTRU9VVFBVVCsnLnVpZCcsICIgZ2VuZXJhdG8uIikKIGlmIERPUERGOgogIEVTLm1ha2VwZGYoQkFTRU9VVFBVVCkKICAKCmRlZiBjaGVja19zZWxmKCk6CiBpbXBvcnQgb3MsIGhhc2hsaWIscmUsIHN5cwogTUVfYmFzZSxNRV9leHQ9b3MucGF0aC5zcGxpdGV4dChvcy5wYXRoLmFic3BhdGgoX19maWxlX18pKQogTUU9TUVfYmFzZSsnLnB5JwogaWYgc3lzLnZlcnNpb25faW5mb1swXSA+IDI6CiAgIGFsbD1vcGVuKE1FLCdyJyxlbmNvZGluZz0ndXRmLTgnKS5yZWFkKCkKICAgZGVmIG15X2hhc2goaW5wdXRfY29udGVudCk6CiAgICAgcmV0dXJuIGhhc2hsaWIuc2hhMjI0KGlucHV0X2NvbnRlbnQuZW5jb2RlKGVuY29kaW5nPSd1dGYtOCcpKS5oZXhkaWdlc3QoKQogZWxzZToKICAgYWxsPW9wZW4oTUUsJ3InKS5yZWFkKCkKICAgZGVmIG15X2hhc2goaW5wdXRfY29udGVudCk6CiAgICAgcmV0dXJuIGhhc2hsaWIuc2hhMjI0KGlucHV0X2NvbnRlbnQpLmhleGRpZ2VzdCgpCiBwPWFsbC5pbmRleCgiXG4iKQogcmVnPXJlLmNvbXBpbGUoIiMtLUJFR0lOIisiU0lHLS18Iy0tRU5EIisiU0lHLS0iLHJlLk0gYW5kIHJlLkRPVEFMTCApCiBib2R5X2ZpcnN0LGhpZGRlbixib2R5X2xhc3Q9cmVzPXJlZy5zcGxpdChhbGxbcCsxOl0pCiBsPW15X2hhc2goYm9keV9maXJzdC5zdHJpcCgpICsgYm9keV9sYXN0LnN0cmlwKCkpCiBleHBlY3RfbD0nYmQwNDc4ODhhMGI4NzY4ODM2NDdiMDQzMGQ0YjdhMGUxM2FjZjA2MmUxZjMyMGE0MGQ5ODI4YjAnCiBpZiBsICE9IGV4cGVjdF9sOgogIHJldHVybiBGYWxzZQogZWxzZToKICByZXR1cm4gVHJ1ZQo=').decode('utf-8'),'<string>','exec'))
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
      DECLARED_FIRST_ROW=int(self.sheet.row_values(4)[1])
      COMPUTED_FIRST_ROW=self.sheet.col_values(0).index('#')+1
      if COMPUTED_FIRST_ROW != DECLARED_FIRST_ROW:
          sys.stderr.write("WTF! Its 2021 and Wrong Format Again...\nPlease check....\n")
      # TMP_CONTENT=int( self.sheet.row_values(DECLARED_FIRST_ROW-1)[0] ) #contenuto della prima cella della DECLARED_FIRST_ROW 
      self.FIRST_ROW=COMPUTED_FIRST_ROW
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

 def makepdf(self,baseoutput,curdir=os.getcwd()):
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
  # curdir=os.getcwd()
  os.chdir(tmpdir)
  fd=open('%s.tex' % baseoutput,'wb') ## __TODO__ output file
  fd.write( (latex_template % {'body':BODY, 'headline':self.HEADLINE}).encode('utf-8') )
  fd.close()
  os.system('xelatex %s.tex' % baseoutput)
  os.system('xelatex %s.tex' % baseoutput )
  shutil.copy('%s.pdf' % baseoutput ,os.path.join(curdir,baseoutput+'.pdf'))
  shutil.rmtree(tmpdir)
  print("\n  ==>file ", baseoutput + '.pdf', "generato")
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
 ser.write(b'ATI\r\n')
 sys.stdout.write(expectprompt(ser))
 ser.write(b'ATM2\r\n')
 sys.stdout.write(expectprompt(ser))
 ser.write(b'ATL3\r\n')
 sys.stdout.write(expectprompt(ser))
 return ser


def expectprompt(ser):
 time.sleep(1)
 out=b''
 while ser.inWaiting() > 0:
  buf=ser.read(1)
  out += buf
 return out.decode('ascii')
 
ALLOWEDCHARS='0123456789'

def partial_string(i,n):
 return "\r[" + ("#"*i) + ("-"*(n-i) ) + "]"

def callgsm(serial_port,telenumber,pin):
 ser = getgsm(serial_port)
 print('Calling...')
 ser.write( ('ATD ' + telenumber + ';' + '\r\n').encode() )
 exp=expectprompt(ser)
 if VERBOSE: 
  sys.stderr.write(exp)
 else:
  sys.stderr.write("\n"+("-"*80)+"\n")
 sys.stdout.write("Input 4 cifre + <Return>: ")
 cifre=input(">> ")
 cifre=cifre.strip()
 numcifre=len(cifre);
 tmpii=0
 for x in cifre:
  if not x in ALLOWEDCHARS:
   print("Cifre Sbagliate: ", x, " not in ", ALLOWEDCHARS)
  else:
   tmpii += 1
   ser.write(( 'AT+VTS=' + x + '\r\n').encode() )
   exp=expectprompt(ser)
   if VERBOSE: 
    sys.stderr.write(exp)
   else:
    sys.stderr.write(partial_string(tmpii,numcifre))
 sys.stdout.write("\nPress <Return> per inviare il PIN di otto cifre...")
 ret=input(">> ")
 lenpin=len(pin)
 tmpii=0
 for x in pin:
  tmpii += 1
  ser.write(( 'AT+VTS=' + x + '\r\n').encode() )
  exp=expectprompt(ser)
  if VERBOSE: 
   sys.stderr.write(exp)
  else:
   sys.stderr.write(partial_string(tmpii,lenpin))
 sys.stdout.write("\nPress <Return> per riagganciare..." )
 ret=input(">> ")
 ser.write(b'AT+CHUP\r\n')
 sys.stderr.write(expectprompt(ser))
 print("\n...closing....")
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
    if 'target' in db:
        result['target_letter']=db['target']
    else:
        result['target_letter']=''
    for x in ANNO_NAMES:
        if x in db:
            result['anno']=int(db[x])
            break
    for x in TYPE_NAMES:
        if x in db:
            result['type']=db[x]
            break
    for x in ORARIO_NAMES:    
        if x in db:
            orario={}
            for giorno in db[x].keys():
                if not giorno in GIORNI_NAMES:
                    raise Exception("Giorno {} not valid\n".format(giorno))
                orario[giorno]=(db[x][giorno]).split('-')
            result['orario']=orario
            break
    for tok in ['sem-start','sem-end','vac']:
        if tok in db:
            result[tok]=db[tok]
    return result

def parse_body_parts(body_parts,header_db):
    j=0
    result=[]
    for body_db in body_parts:
        sys.stderr.write("PARSING body part #{}\n".format(j+1) )
        result += parse_body(body_db,header_db,year_offset=j)
        j += 1
    return result     


def parse_body(body_db,header_db,year_offset=0):
    result = [] 
    target_letter=header_db['target_letter']
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
            if not week_day in header_db['orario']:
                raise Exception("Problem: week_day '{} {}' not in orario!".format(week_day,day_date))
            orario=header_db['orario'][week_day]
            act_type=header_db['type']
            if day_tokens[1][0]=='*':
                desc= " ".join(day_tokens[2:]) 
            else:
                desc= " ".join(day_tokens[1:]) 
            if target_letter and day_tokens[1][:2]!=('*'+target_letter): 
                continue
            desc=dirty_trick(desc,back=True)
            sys.stderr.write("  -> ore= {}\n".format(numero_ore(orario[0],orario[1])))
            ## result += [(day_date.strftime("%d/%m/%Y"), orario[0],orario[1], "" , "{}".format(act_type).encode('utf-8'), "", desc.encode('utf-8'),desc  ) ]
            result += [[day_date.strftime("%d/%m/%Y"), orario[0],orario[1], "" , act_type, "", desc,desc ] ]
    return result

def dirty_trick(s, back=False):
    if back:
        return re.sub('__COLON_XXX_SPACE__',': ',s)
    else:    
        return re.sub(': ','__COLON_XXX_SPACE__',s)


def numero_ore(a,b):
    time_FMT = '%H:%M'
    return (datetime.datetime.strptime(b, time_FMT) - datetime.datetime.strptime(a, time_FMT)).total_seconds() / (60*60.0)
    

def ymltocsv(yamlfile,outfile,blankyml=False):
    # import oyaml as yaml to have it ordered?
    import yaml
    import csv
    # import StringIO
    import re
    reg_itemline=re.compile(r"(?P<blank>\s*?)- (?P<content>.*?)$")
    yaml_content=''
    for raw_line in open(yamlfile).readlines():
        reg_search=reg_itemline.search(raw_line)
        if reg_search:
            yaml_content += "%s- %s\n" % (reg_search.group('blank'), dirty_trick( reg_search.group('content') ) ) 
        else:
            yaml_content += raw_line
    # yaml_stream=StringIO.StringIO()
    # yaml_stream.write(yaml_content)
    # yaml_stream.seek(0)
    # try here
    yaml_stream = yaml_content
    tokens=list(yaml.safe_load_all(yaml_stream))

    # tokens=list(yaml.safe_load_all(file(yamlfile)))
    header=tokens[0]
    hdb=parse_header(header)
    if blankyml: 
        # generate the blank
        if not ( 'sem-start' in hdb and 'sem-end' in hdb ):
            raise Exception("sem-start and sem-end missing!")
        other_data=''
        tot_ore = 0
        thismonth=hdb['sem-start'].month
        thisyear=hdb['sem-start'].year
        if 'vac' in hdb:
            vac=hdb['vac'] 
        else:
            vac=[]
        other_data += ("\n{}:\n\n".format( MESE_NAMES[thismonth-1]) ) 
        for x in range( (hdb['sem-end'] - hdb['sem-start']).days +1 ):
            thisday= hdb['sem-start'] + datetime.timedelta(x) 
            if thisday.year != thisyear:
                thisyear=thisday.year
                other_data += ("\n---\n") 
            if thisday.month != thismonth:
                # changed the month...
                thismonth=thisday.month
                other_data += ("\n{}:\n\n".format( MESE_NAMES[thismonth-1]) ) 
            if GIORNI_NAMES[thisday.weekday()] in hdb['orario']:
                # how many hours? 
                if thisday in vac:
                    sys.stderr.write("GROOVY: VACATION DAY {}\n".format(thisday,) )
                    continue
                orario=hdb['orario'][GIORNI_NAMES[thisday.weekday()]]
                n_ore=numero_ore(*orario)  
                tot_ore += n_ore
                other_data += (" - {} *{} {}/{}\n".format( thisday.day ,GIORNI_NAMES[thisday.weekday()],
                    n_ore, tot_ore) )
            if thisday.weekday() == 6:
                other_data += "\n" 
        with open(outfile, 'w') as outf:
            outf.write(yaml_content + other_data )
            outf.close()        
            sys.stderr.write("""File {} created\n""".format(outf.name))
        return 
    body_parts=tokens[1:]
    all_data= parse_body_parts(body_parts,hdb) 
    total_time=0 
    with open(outfile, 'w' ) as outf:
        csvwriter = csv.writer(outf, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in all_data:
            ore_da_aggiungere=numero_ore(row[1],row[2])
            lecture_numbers=[str( int( total_time ) + 1 + x ) for x in range(int(ore_da_aggiungere)) ]
            lecture_title="Lez. N° " + (", ".join(lecture_numbers) )
            row[6] = lecture_title
            total_time += ore_da_aggiungere
            # replace column 
            csvwriter.writerow( row )
    outf.close()        
    sys.stderr.write(
"""
Number of hours: {}
File {} created
Open with options:   Unicode, Italia, separated by semicolon, text_delimiter=\", Quoted field as text.
""".format(total_time, outf.name))
    return 

#-----------------------------------------------------------------------

def ymltoblankyml(yamlfile,blankymlfile):
    return ymltocsv(yamlfile,blankymlfile,blankyml=True)

#-----------------------------------------------------------------------
def guid():
    try:
        import xlrd
    except:
        sys.stderr.write("Please first install XLRD: %s\n" % XLRD_URL)
        sys.stderr.write("[Try 'python3 -m pip install xlrd'] or [Try 'apt install python-xlrd'] or ['pip install xlrd'] \n")
        sys.exit(1)
    try:
        import PySimpleGUI as sg
    except:
        sys.stderr.write("Please first install PySimpleGUI : %s\n" % PYSYMPLEGUI_URL)
        sys.stderr.write("[Try 'python3 -m pip install PySimpleGUI '] or ['pip install PySimpleGUI'] \n")
        sys.exit(1)
    font = ("Courier New", 14)  # TODO: font
    sg.theme("Darkblue3")
    sg.set_options(auto_size_buttons=True, font=font)
    num_rows = 5
    num_cols = 5
    output_filename=None
    output_filename_basename=None

    data = [["" for x in range(num_rows)] for y in range(num_cols)]
    headings = ["" for x in range(num_cols)]
    HAS_HEADER=True
    IS_ESSE3=False
    TABLE_COLS=["A","B","C","D","E","F","G","H"]
    TABLE_DATA=[]
    TO_TABLE_DATA=[]
    TO_TABLE_COLS=['','Cognome, Nome','UID','']
    TO_TABLE_COL_W=[1,70,8,1]

    layout = [
        [sg.Text("Choose a file: "), sg.Input(key='_FILEBROWSE_', enable_events=True, visible=False),\
                sg.FileBrowse(file_types=(('XLSX files','*.xlsx *.xls'),), target='_FILEBROWSE_' ) ,
                sg.Push(), sg.Button('Info') ], 
        [sg.Text(" "*80, key='STATUSBAR') ], 
        [sg.Table(values=TABLE_DATA,headings=TABLE_COLS, max_col_width=10,
            auto_size_columns=False,
            display_row_numbers=False,
            justification='left',
            num_rows=6,
            key='FROM_TABLE',
            tooltip='This is the from-table')],
        [sg.Checkbox("First row is header?" , key="HAS_HEADER",default=HAS_HEADER, enable_events=True)], 
        [sg.Text("Cognome Col: "), sg.Combo([], key='-COGNOME-', enable_events=True,disabled=True), 
        sg.Text("Name Col: "), sg.Combo([], key='-NOME-',enable_events=True,disabled=True), 
        sg.Text("UID Col: "), sg.Combo([], key='-UID-', enable_events=True,disabled=True) ],
        [sg.Table(values=TO_TABLE_DATA,headings=TO_TABLE_COLS, max_col_width=4,
            auto_size_columns=False,
            col_widths=TO_TABLE_COL_W,
            display_row_numbers=False,
            justification='left',
            num_rows=6,
            key='TO_TABLE',
            tooltip='This is the to_table') ], 
        [ sg.Text(" "*80, key='OUTPUTFILE') ], 
        [ sg.Button("Save"), sg.Button("Registro PDF"), sg.Push(), sg.Button("Exit") ] 
        ]
    window = sg.Window('ESSE3 multi-tool', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            break
        elif event == "Info":
            sg.popup("""{} version {}
------------------------------
OS: {} 
Python version: {}
PySimpleGUI version: {} 
-----------------------------
(C) Copyright DLFerrario www.dlfer.xyz        
""".format( sys.argv[0], __version__ , sys.platform , sys.version.split("\n")[0], sg.version ) , title='Info',
background_color='black')
        elif event == "Save":
            if output_filename is None:
                sg.popup("WRONG STEP", background_color="red")
                continue
            elif os.path.exists(output_filename):
                retval = sg.popup_ok_cancel("File  {} already exists! Overwrite?".format(output_filename) ,
                        background_color='red')
                if retval == 'Cancel':
                    continue
            with open(output_filename,'w') as fd:
               for l in TO_TABLE_DATA:
                  fd.write(":".join(l) + "\n" )
               fd.close()    
            window['OUTPUTFILE'].update("Output: {} [SAVED]".format(output_filename), 
                    background_color='green')
        elif event == "Registro PDF":
            if not IS_ESSE3 or output_filename_basename is None:
                sg.popup("WRONG STEP", background_color="red")
                continue
            ES.makepdf(output_filename_basename,curdir=output_curdir)
            window['OUTPUTFILE'].update("Output: {} [SAVED]".format(output_filename_basename+".pdf"), 
                    background_color='darkorange')
        elif event == '_FILEBROWSE_':
            # xlsx only
            xlsx_file = values['Browse']
            r,e = os.path.splitext(xlsx_file)
            output_filename = "{}_mcq.uid".format(r)
            output_filename_basename = "{}_mcq".format(os.path.basename(r))
            output_curdir=os.path.dirname(xlsx_file)
            wb=xlrd.open_workbook(xlsx_file)
            sheet_names = wb.sheet_names()
            target_sheet=sheet_names[0]
            sheet=wb.sheet_by_name(target_sheet)
            window['STATUSBAR'].update("Input: {} ({} rows)".format(xlsx_file,sheet.nrows) )
            window['OUTPUTFILE'].update("Output: {}".format(output_filename) )
            if VERBOSE:
                sys.stderr.write("Sheets <{}> found! Trying the first...\n".format(sheet_names) )
            # first try Esse3
            if target_sheet=='esse3':
              IS_ESSE3=True  
              for k in [ '-COGNOME-', '-NOME-', '-UID-' ]:
                window[k].update(disabled=True)
              try:
                ES=Esse3(xlsx_file)
                TABLE_DATA=[["ESSE3 table"]]
                window['FROM_TABLE'].update(TABLE_DATA)
                #if os.path.exists(output_filename):
                #    retval = sg.popup_ok_cancel("File  {} already exists! Overwrite?".format(output_filename) ,
                #            background_color='red')
                #    if retval == 'Cancel':
                #        continue
                #with open(output_filename,'wb') as fd:
                #    ES.makeuid(fd)
                #    fd.close()
                #if sg.popup_ok_cancel("File {} generato!\n Quit?".format(output_filename), background_color="green") == 'OK':
                #    break
                #else:
                #    continue
              except Exception as v:
                sg.popup_error_with_traceback('An error happened.  Here is the info: ', v)
                continue
            else:
              IS_ESSE3=False  
              NCOLS=sheet.ncols
              TABLE_DATA=[]
              for r in range(sheet.nrows):
                row=sheet.row_values(r)
                TABLE_DATA.append(row)
                # Cognome, Nome, UID =  row[Cognome_i],row[Nome_i],row[UID_i]
              window['FROM_TABLE'].update(TABLE_DATA)
              ii=0
              for k in [ '-COGNOME-', '-NOME-', '-UID-' ]:
                window[k].update(value=TABLE_COLS[ii], values=TABLE_COLS[:NCOLS],disabled=False)
                ii +=1 
              Cognome_i=0
              Nome_i=1
              UID_i=2
        elif event in [ '-COGNOME-', '-NOME-', '-UID-']:    
            Cognome_i=TABLE_COLS.index(values['-COGNOME-'])
            Nome_i=TABLE_COLS.index(values['-NOME-'])
            UID_i=TABLE_COLS.index(values['-UID-'])
            window['OUTPUTFILE'].update("Output: {}".format(output_filename) ,
                    background_color = sg.theme_element_background_color() )
        elif event == 'HAS_HEADER':
            HAS_HEADER=values['HAS_HEADER']
            window['OUTPUTFILE'].update("Output: {}".format(output_filename) , 
                    background_color = sg.theme_element_background_color() )
        if HAS_HEADER and not IS_ESSE3:
            starting_row=1
            window['FROM_TABLE'].update(row_colors=[[0,'green']] ) 
        else:
            starting_row=0
            window['FROM_TABLE'].update(row_colors=[[0,sg.theme_element_background_color()]]) 
        if TABLE_DATA == [] :
            continue

        try:
          TO_TABLE_DATA=[]
          if IS_ESSE3:
            for Cognome,Nome,UID in ES.iscritti:  
                TO_TABLE_DATA.append([ "" , "{}, {}".format(Cognome,Nome), UID, "" ] )
          else:    
            for row in TABLE_DATA[starting_row:]:
                Cognome, Nome, UID =  row[Cognome_i],row[Nome_i],row[UID_i]
                TO_TABLE_DATA.append([ "" , "{}, {}".format(Cognome,Nome), UID, "" ] )
          window['TO_TABLE'].update(TO_TABLE_DATA)
        except Exception as v:
          sg.popup_error_with_traceback(f'An error happened.  Here is the info:', v)
          print("ERROR: {}".format(v), event, values)
          continue 

#-----------------------------------------------------------------------

if __name__=='__main__':
 get_opt()



