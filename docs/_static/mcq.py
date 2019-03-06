#!/usr/bin/env python2.7
# -*- coding: utf8 -*-

# LICENZA: Quest'opera e' stata rilasciata con licenza Creative Commons Attribuzione - Non commerciale - Non opere derivate 3.0 Unported. Per leggere una copia della licenza visita il sito web http://creativecommons.org/licenses/by-nc-nd/3.0/ o spedisci una lettera a Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
# (C) DLFerrario http://www.matapp.unimib.it/~ferrario/var/mcqxelatex.html

r"""
# Version: Thursday 2019-02-07
mcq.py [options] [filename]

RUN: `mcq.py` without arguments to use the interactive CLI. 

OPTIONS:
	--help|-h		questo aiuto
	-v			verbose output
	--gift|-g		GIFT output
	--xhtml|-x		XHTML output
	--output=|-o [FILENAME] explicit output=[FILENAME]
	--number=|-n [N]	number of copies = [n]
	--db= [FILENAME]	dati per la correzione 
	--stats= [FILENAME]	produce file con le statistiche
	--omr= [BASENAME] [SCANFILES]	OMR scan di [BASENAME].tex e [SCANFILES]
	--uid= [FILENAME][:3:2] [FILE]	completa NomeCognome dal file [FILENAME]
	--join  [FILE1_exam.csv] [FILE2_exam.csv] unisce le tabelle csv	
	--choose= [N] [files*.tex] random choose N from files*.tex
---

EXAMPLES:
	$ mcq.py -n 4  file.tex 
	genera un file "file_exam.tex" (da compilare)
        con n=4 copie permutate di file.tex
	vengono generati anche 
             file_exam.sols (soluzioni, in formato testo/leggibile)
	     skel_exam.db   (soluzioni, in formato interno)
	
	$ mcq.py --db=file_exam.db file.txt > file_exam.txt
	correzione: file_exam.db è quello generato prima,
	"file.txt" è un file con righe (esclusi commenti che iniziano 
        per "#" e righe vuote) del tipo
		FXZH:Cognome, Nome:193146:Adba:30
	cioè codice del compito:cognomenome:matricola:soluzionirispostamult:voto
	la stringa di soluzioni per scelta multipla contiene le lettere e 0 per
	le risposte non date.
	nei commenti di "file.txt" si può aggiungere il parametro 
	"# target=[voto]",
	che fa sì che la media risulti più o meno uguale a [voto].
	
	$ mcq.py --stats=file_exam_stats.db file.tex >file_stats.tex
	genera le statistiche (un file tex come l'originale con le statistiche)
	
	$ mcq.py --gift file.tex > file.gift
	genera un file GIFT (per moodle).
	
	$ mcq.py --xhtml file.tex > file.html
	genera un file xhtml (da includere con css).

	$ mcq.py --omr=file.tex scan/file1.pdf scan/file2.pdf scan/file3.pdf > output.txt
	corregge (Optical Mark Reader) i bubblesheets 

	$ mcq.py --uid=uidfile.txt output.txt > output2.txt
	riempie il campo CognomeNome del file output.txt, prendendo i dati di matricola da uidfile.txt (uidfile deve avere lo stesso formato <tag>:<nome>:<matricola>:<risposte>:<voto opzionale> di output.txt).
	Se si ha un file CSV, invece, con delimitatore uguale a ";", per esempio, in cui la matricola e' nella colonna 1 e il nome nella colonna 4, si puo' usare il formato
	
	$ mcq.py --uid="uidfile.txt:1;4" output.txt > output2.txt
	[Osservazione: nel nome del file non ci devono essere ":", e occorre mettere tra virgolette l'argomento di --uid]. Sia i numeri delle colonne che il delimitatore devono essere lunghi un carattere. Se il delimitatore e' ",", ricordarsi di salvare il file CSV mettendo tra virgolette i nomi con la virgola.
	
	$ mcq.py --join c1_exam.csv c2_exam.csv c3_exam.csv > c_all.csv
	unisce i tre risultati (lasciando in bianco dove le prove non ci sono)

	$ mcq.py --choose= 14 file1.tex file2.tex file3.tex > c.tex
	sceglie a caso 14 domande tra tutte quelle che compaiono nei file

LATEX:
	Il file "file.tex" deve contenere il comando
	\usepackage[sol]{mcq} (per vedere il feedback)
	oppure
	\usepackage{mcq}
	oppure
	\usepackage[bubblesheet]{mcq}
	oppure
	\usepackage[bubblesheet,extrasheet]{mcq} % per avere due copie del bubblesheet 

	Comandi possibili:
	\headline{Geometria I - 24 giu 2009 (14:30 - U1-01)}
	\puntigiusta{3}
	\puntisbagliata{-1}
	\puntiempty{0}
	\formulavoto{(x**2+y)/2} %% sintassi di python
	\variantlabel{X} %% i codici identificativi avranno il prefisso 'X'
			 %% serve nel caso in cui diversi file generano
			 %% compiti che poi verranno corretti tutti insieme

	\nomeesame % stampa Nome-Cognome-Matricola
	\begin{esercizi}{Titolo}...\end{esercizi}
	\begin{esercizi*}{Titolo}...\end{esercizi*}
	
	\bubblesheet[2]{4}{20} % per OMR


\begin{exerm}[Commento dell'esercizio] 
\qtitle{Esercizio di esempio}
Testo dell'esercizio
\begin{rispm}[3] % risposte su 3 colonne
\risp[=] risposta giusta
\risp risposta sbagliata
\fb{feedback}
\risp[-2] risposta sbagliata che vale -2 punti.
\risp[0.01] Risposta che vale 0.01 punti. 
\end{rispm}
\end{exerm}

\begin{exerm}\qtitle{Esercizio vero falso}
Questo è un esercizio vero/falso.
\vero[
Feedback per chi dà la risposta sbagliata.
]
\end{exerm}


\begin{exerm}
\begin{varianti} 
%% Esercizio con varianti: il programma ne sceglie una a caso per ogni
%% copia del compito.
%% Le varianti devono tutte avere lo stesso numero di risposte possibili.
%% Esercizi come questi non possono essere convertiti al 100% in GIFT o XHTML
%% e, nel file delle statistiche, solo la prima variante viene mostrata.
%% I numeri accanto alle risposte possibili saranno privi di senso, però.
\varitem 
testo prima variante 
\begin{rispm} \risp .... \end{rispm}
\varitem
testo seconda variante
\begin{rispm}\risp ... \end{rispm}
\end{varianti}
\end{exerm}

-------
ENVIRONMENT VARIABLES:
	MCQRANDOMSEED [alternative random seed]
	OMARSERVICE   [alternative Optical Mark Recognition remote service URL]
        ANSI_COLORS_DISABLED [disable ANSI colors in some terminals]
-------

[Quest'opera e' stata rilasciata con licenza Creative Commons Attribuzione - Non commerciale - Non opere derivate 3.0 Unported. Per leggere una copia della licenza visita il sito web http://creativecommons.org/licenses/by-nc-nd/3.0/ o spedisci una lettera a Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.]

(C)  DLFerrario http://www.matapp.unimib.it/~ferrario/var/mcqxelatex.html
""" 
#-----------------------------------------------------------------------
#import sys
#import os
#if sys.version_info[0] != 2:
# sys.stderr.write("WARNING: It is not compatible with Python Version %s !\nTrying to reload myself with another version..." % sys.version_info[0] )
# for x in ['python2', 'python2.7', 'python2.6', 'python2.5']:
#  sys.stderr.write("Trying version `%s`...\n" % x)
#   # if not os.system("%s %s" % (x, os.path.abspath(__file__) ) ):
#  if not os.system("%s -V" % (x, ) ):
#   # binary exists 
#   os.system("%s %s" % (x, os.path.abspath(__file__) ) )
#   sys.exit(0)
# sys.sterr.write("TOTALE FAILURE\n") 
# sys.exit(1)
#-----------------------------------------------------------------------
aalogo=r""" OMaRScan @%s
     ==================
      |@@@@----@|@@--|
      |@@@----@@|--@@|
      |@@----@@@|@--@|
      |@@@@----@|--@@|
      |@@@@@----|@--@|
      |@----@@@@|@--@|
     ==================
"""


#-----------------------------------------------------------------------
translate_math={
r"([<])"             : u"\\\lt ",
r"([>])"             : u"\\\gt ",
r"(\\implies)"       : u"\Longrightarrow",
r"(\\from)"          : u"\colon",
r"(\\textellipsis)"       : u"...",
r"(\\AA)"       : u"\mathbb{A}",
r"(\\CC)"       : u"\mathbb{C}",
r"(\\RR)"       : u"\mathbb{R}",
r"(\\ZZ)"       : u"\mathbb{Z}",
r"(\\QQ)"       : u"\mathbb{Q}",
r"(\\EE)"       : u"\mathbb{E}",
r"(\\PP)"       : u"\mathbb{P}",
r"(\\FF)"       : u"\mathbb{F}",
r"(\\KK)"       : u"\mathbb{K}",
r"(\\HH)"       : u"\mathbb{H}",
r"(\\NN)"       : u"\mathbb{N}",
r"(\\smallsetminus)" : u"-"
}

#-----------------------------------------------------------------------
lettere='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#-----------------------------------------------------------------------
translate_dictionary={
r"(\\`a|\\`{a})" : u"à" ,
r"(\\`e|\\`{e})" : u"è" ,
r"(\\`i|\\`{i})" : u"ì" ,
r"(\\`o|\\`{o})" : u"ò" ,
r"""(\\"o|\\`{o})""" : u"ö" ,
r"(\\`u|\\`{u})" : u"ù" ,
r"(\\`A|\\`{A})" : u"À" ,
r"(\\`E|\\`{E})" : u"È" ,
r"(\\`I|\\`{I})" : u"Ì" ,
r"(\\`O|\\`{O})" : u"Ò" ,
r"(\\`U|\\`{U})" : u"Ù" ,
r"(\\'a|\\'{a})" : u"á" ,
r"(\\'e|\\'{e})" : u"é" ,
r"(\\'i|\\'{i})" : u"í" ,
r"(\\'o|\\'{o})" : u"ó" ,
r"(\\'u|\\'{u})" : u"ú" ,
r"(\\'A|\\'{A})" : u"Á" ,
r"(\\'E|\\'{E})" : u"É" ,
r"(\\'I|\\'{I})" : u"Í" ,
r"(\\'O|\\'{O})" : u"Ó" ,
r"(\\'U|\\'{U})" : u"Ú" 
}

#-----------------------------------------------------------------------
import os
import sys
import re
import getopt
import random
if 'MCQRANDOMSEED' in os.environ.keys():
  MCQRANDOMSEED=os.environ['MCQRANDOMSEED']
  sys.stderr.write("Warning: Local MCQRANDOMSEED found! `%s'\n" %  MCQRANDOMSEED)
else:
  MCQRANDOMSEED=106
random.seed(MCQRANDOMSEED)
import pickle
import math
import csv
#-----------------------------------------------------------------------
VERBOSE=False
output = sys.stdout
explicit_output=False
NUMBER_OF_COPIES=1
EVALUATE=False
VALFILE=None
GIFT=False
XHTML=False
MAKE_STATS=False
BASENAMEFILE=None
MERGEFILES=False
ZIPPASSWORD='SECRET'
OMARSERVICE='https://peano.matapp.unimib.it/omar/cgi-bin/omrgw.cgi'
# OMARSERVICE='https://failsafe.matapp.unimib.it/cgi-bin/omrgw.cgi'
ISUI=False
MAX_HISTORY_LENGTH=1024 # number of terms in the history of readline
MCQXELATEXURL='http://www.matapp.unimib.it/~ferrario/var/mcqxelatex.html'
DATETIME_FORMAT="%Y-%m-%d %H:%M:%S"
NUM_OF_TERMCOLS=79

#-----------------------------------------------------------------------

def default_combina_voti(x,y):
 return x+y
 # return max(0.0,x)**(0.5) * y

#-----------------------------------------------------------------------
def ssclient(basetexfile,scanfiles,outputtype=None,outputfile='omr-output.pdf'):
 global ZIPPASSWORD, OMARSERVICE
 import os
 import zipfile
 import hashlib,hmac
 import time
 import xmlrpclib, ssl ## __HERE__  : for version>= 2.7.9 needs _create_unverified_context()
 import tempfile
 fdtmp,TMPZIP=tempfile.mkstemp(suffix='zip')
 start_time=time.time()
 if 'OMARSERVICE' in os.environ.keys():
    OMARSERVICE=os.environ['OMARSERVICE']
    sys.stderr.write("Environment variable OMARSERVICE='%s' found!\nTrying...\n"%OMARSERVICE)
 if sys.version_info>=(2,7,9):
   my_service = xmlrpclib.ServerProxy( OMARSERVICE , context=ssl._create_unverified_context())
 else:
   my_service = xmlrpclib.ServerProxy( OMARSERVICE )
 files = [basetexfile+'.xml',basetexfile+'.pdf'] + [x for x in scanfiles]
 zip=zipfile.ZipFile(TMPZIP,'w')
 for f in files:
  zip.write(f)
 zip.close()
 fd=open(TMPZIP,'rb')
 data=fd.read()
 fd.close() 
 os.close(fdtmp)
 os.remove(TMPZIP)
 # data=file(TMPZIP).read()
 hm=hmac.new(ZIPPASSWORD,data,digestmod=hashlib.sha256)
 digest=hm.hexdigest()
 sys.stderr.write(aalogo % OMARSERVICE)
 sys.stderr.write("Sending data... ")
 if outputtype=='XML':
  job_id = my_service.add_to_queue(xmlrpclib.Binary(data),[digest,'XML'])
 else:
  job_id = my_service.add_to_queue(xmlrpclib.Binary(data),digest)
 sys.stderr.write("Done!\n")
 if job_id[:4]!='FAIL':
  sys.stderr.write("Working... \n")
 else:
  sys.stderr.write("%s failed\n" % job_id)
  # sys.exit(1)
  exit_on_error('ERROR')
 for x in range(20000):
   status=my_service.check_status(job_id)
   sys.stderr.write(status)
   if status[:4]=='FAIL':
    exit_on_error('ERROR')
    # sys.exit(1)
   if status=='DONE':
    break
   else:
    for x in range(20):
     sys.stderr.write(".")
     time.sleep(3.0/20)
 txt,pdf=my_service.get_result(job_id)
 # file('omr-output.pdf','w').write(pdf.data)
 fd=open(outputfile,'wb')
 fd.write(pdf.data)
 fd.close()
 sys.stderr.write("\nFile `%s' created.\n" % outputfile )
 end_time=time.time()
 sys.stderr.write("Elapsed time: %i seconds.\n" % int(end_time-start_time))
 if outputtype=='XML':
  return str(pickle.loads(txt))
 else:
  return txt



#-----------------------------------------------------------------------
#--BEGINSIG--
import base64;eval(compile(base64.b64decode('CmRlZiBjaGVja19zZWxmKCk6CiByZXR1cm4gVHJ1ZQoKZGVmIGdldF9vcHQoKToKIGdsb2JhbCBWRVJCT1NFLG91dHB1dCxleHBsaWNpdF9vdXRwdXQsTlVNQkVSX09GX0NPUElFUywgU09MVVRJT05TX0ZJTEUsIERCX0ZJTEUsIEVWQUxVQVRFLCBHSUZULCBYSFRNTCwgVkFMRklMRSwgTUFLRV9TVEFUUywgREJfU1RBVFNfRklMRSwgQkFTRU5BTUVGSUxFLCBNRVJHRUZJTEVTLCBJU1VJCiBpZiBub3QgY2hlY2tfc2VsZigpIDoKICBzeXMuc3RkZXJyLndyaXRlKCJTZWxmLWludGVncml0eSBjaGVja3N1bSBmYWlsZWQhIEFib3J0aW5nLi4uXG5JbnN0YWxsIGEgbmV3IGNsZWFuIHZlcnNpb24hXG4iICkKICBzeXMuZXhpdCgxKQogT01BUlNDQU49RmFsc2UKIENTVkpPSU49RmFsc2UKIFJBTkRPTUNIT09TRT1GYWxzZQogdHJ5OgogIG9wdHMsIGFyZ3MgPSBnZXRvcHQuZ2V0b3B0KHN5cy5hcmd2WzE6XSwgImhneG46bzp2IiwgWyJoZWxwIiwgIm91dHB1dD0iLCJudW1iZXI9IiwiZGI9IiwiZ2lmdCIsInhodG1sIiwgInN0YXRzPSIsInVpZD0iLCJvbXI9Iiwiam9pbiIsImNob29zZT0iLCJ2ZXJib3NlIl0pCiBleGNlcHQgZ2V0b3B0LkdldG9wdEVycm9yLCBlcnI6CiAgcHJpbnQgc3RyKGVycikgCiAgcHJpbnQgIltvcHRpb24gLS1oZWxwIGZvciBoZWxwXSIKICBzeXMuZXhpdCgyKQogaWYgbGVuKGFyZ3MpPT0wOgogIElTVUk9VHJ1ZQogZm9yIG8sIGEgaW4gb3B0czoKICBpZiBvICBpbiAoIi12IiwiLS12ZXJib3NlIik6CiAgICBWRVJCT1NFID0gVHJ1ZQogIGVsaWYgbyBpbiAoIi1oIiwgIi0taGVscCIpOgogICAgcHJpbnQgX19kb2NfXwogICAgc3lzLmV4aXQoKQogIGVsaWYgbyBpbiAoIi1nIiwgIi0tZ2lmdCIpOgogICAgR0lGVD1UcnVlCiAgZWxpZiBvIGluICgiLXgiLCAiLS14aHRtbCIpOgogICAgWEhUTUw9VHJ1ZQogIGVsaWYgbyBpbiAoIi1vIiwgIi0tb3V0cHV0Iik6CiAgICBiLGU9b3MucGF0aC5zcGxpdGV4dChhKQogICAgb3V0cHV0ID0gZmlsZShhLCd3JykKICAgIFNPTFVUSU9OU19GSUxFPWZpbGUoYisiX2V4YW0uc29scyIsJ3cnKQogICAgREJfRklMRT1maWxlKGIrIl9leGFtLmRiIiwnd2InKQogICAgZXhwbGljaXRfb3V0cHV0PVRydWUKICBlbGlmIG8gaW4gKCItLWRiIiwgKToKICAgIGIsZT1vcy5wYXRoLnNwbGl0ZXh0KGEpCiAgICBEQl9GSUxFPWZpbGUoYSwncmInKQogICAgREJfU1RBVFNfRklMRT1maWxlKGIrIl9zdGF0cy5kYiIsJ3diJykKICAgIG91dHB1dCA9IGZpbGUoYisiLmNzdiIsJ3cnKQogICAgRVZBTFVBVEU9VHJ1ZQogIGVsaWYgbyBpbiAoIi0tdWlkIiwgKToKICAgIFVJREZJTEU9YQogICAgTUVSR0VGSUxFUz1UcnVlCiAgZWxpZiBvIGluICgiLS1jaG9vc2UiLCApOgogICAgQ0hPT1NFTlVNQkVSPWludChhKQogICAgUkFORE9NQ0hPT1NFPVRydWUKICBlbGlmIG8gaW4gKCItLW9tciIsICk6CiAgICBPTUFSQkFTRSxfPW9zLnBhdGguc3BsaXRleHQoYSkKICAgIE9NQVJTQ0FOPVRydWUKICBlbGlmIG8gaW4gKCItLWpvaW4iLCApOgogICAgQ1NWSk9JTj1UcnVlCiAgZWxpZiBvIGluICgiLS1zdGF0cyIsICk6CiAgICBiLGU9b3MucGF0aC5zcGxpdGV4dChhKQogICAgREJfU1RBVFNfRklMRT1maWxlKGEsJ3JiJykKICAgICMgb3V0cHV0ID0gZmlsZShiKyIudGV4IiwndycpCiAgICBNQUtFX1NUQVRTPVRydWUKICBlbGlmIG8gaW4gKCItbiIsICItLW51bWJlciIpOgogICAgTlVNQkVSX09GX0NPUElFUz1pbnQoYSkKICBlbHNlOgogICAgYXNzZXJ0IEZhbHNlLCAidW5oYW5kbGVkIG9wdGlvbiIKIGlmIGxlbihhcmdzKT09MDoKICB1aWxvb3AoKQogIHN5cy5leGl0KDApCiAgcmV0dXJuIChzeXMuc3RkaW4ucmVhZCgpLG91dHB1dCkKIGlmIEVWQUxVQVRFIG9yIEdJRlQgb3IgWEhUTUwgb3IgTUFLRV9TVEFUUzoKICBWQUxGSUxFPWFyZ3NbMF0KICByZXR1cm4gKGZpbGUoYXJnc1swXSwncicpLnJlYWQoKSxvdXRwdXQpCiBpZiBNRVJHRUZJTEVTOgogIG91dHB1dC53cml0ZShtZXJnZV9maWxlcyhmaWxlKGFyZ3NbMF0sJ3InKS5yZWFkbGluZXMoKSxVSURGSUxFKSkKICBzeXMuZXhpdCgwKQogaWYgT01BUlNDQU46CiAgb3V0cHV0LndyaXRlKHNzY2xpZW50KE9NQVJCQVNFLGFyZ3MpKQogIHN5cy5leGl0KDApCiBpZiBDU1ZKT0lOOgogIG91dHB1dC53cml0ZShjc3Zqb2luKGFyZ3MpKQogIHN5cy5leGl0KDApCiBpZiBSQU5ET01DSE9PU0U6CiAgb3V0cHV0LndyaXRlKHJhbmRvbV9jaG9vc2UoQ0hPT1NFTlVNQkVSLGFyZ3MpKQogIHN5cy5leGl0KDApCiBpZiBvcy5wYXRoLmV4aXN0cyhhcmdzWzBdKSBhbmQgbm90IGV4cGxpY2l0X291dHB1dDoKICBiLGU9b3MucGF0aC5zcGxpdGV4dChhcmdzWzBdKQogIEJBU0VOQU1FRklMRT1iCiAgb3V0cHV0PWZpbGUoYisiX2V4YW0udGV4IiwndycpCiAgU09MVVRJT05TX0ZJTEU9ZmlsZShiKyJfZXhhbS5zb2xzIiwndycpCiAgREJfRklMRT1maWxlKGIrIl9leGFtLmRiIiwnd2InKQogaWYgb3MucGF0aC5leGlzdHMoYXJnc1swXSk6CiAgcmV0dXJuIChmaWxlKGFyZ3NbMF0sJ3InKS5yZWFkKCksb3V0cHV0KQogZWxzZToKICByYWlzZSBFeGNlcHRpb24oImZpbGUgJXMgZG9lcyBub3QgZXhpc3QhIiAlIGFyZ3NbMF0gKQoKZGVmIGNoZWNrX3NlbGYoKToKIGltcG9ydCBvcywgaGFzaGxpYixyZQogTUVfYmFzZSxNRV9leHQ9b3MucGF0aC5zcGxpdGV4dChvcy5wYXRoLmFic3BhdGgoX19maWxlX18pKQogTUU9TUVfYmFzZSsnLnB5JwogYWxsPWZpbGUoTUUpLnJlYWQoKQogcD1hbGwuaW5kZXgoIlxuIikKIHJlZz1yZS5jb21waWxlKCIjLS1CRUdJTiIrIlNJRy0tfCMtLUVORCIrIlNJRy0tIixyZS5NIGFuZCByZS5ET1RBTEwgKQogYm9keV9maXJzdCxoaWRkZW4sYm9keV9sYXN0PXJlcz1yZWcuc3BsaXQoYWxsW3ArMTpdKQogbD1sZW4oYm9keV9maXJzdC5zdHJpcCgpKStsZW4oYm9keV9sYXN0LnN0cmlwKCkpCiBsPWhhc2hsaWIuc2hhMjI0KGJvZHlfZmlyc3Quc3RyaXAoKSArIGJvZHlfbGFzdC5zdHJpcCgpKS5oZXhkaWdlc3QoKQogZXhwZWN0X2w9J2ZmNzkwZGE2NTJhZWE0NGM2NTI1NTBjN2M3NTZkNmM0MzQ4ZTg3ZGM5MGFkNjhlN2VmNWE2ZjEzJwogaWYgbCAhPSBleHBlY3RfbDoKICByZXR1cm4gRmFsc2UKIGVsc2U6CiAgcmV0dXJuIFRydWUK'),'<string>','exec'))
#--ENDSIG--
#-----------------------------------------------------------------------
def random_choose(n,files):
 random.seed()
 eserlist=[]
 for f in files:
  data=file(f,'r').read()
  data=strip_latex_comments(data)
  if input_enc(data) == 'latin1':
          data=convert_to_utf(data)
  eserlist += extract_esercizi(data)
 result=[]
 if VERBOSE:
   sys.stderr.write("Choosing %i from a list of %i exerms...\n" % (n,len(eserlist)))
 for i in range(n):
  L=len(eserlist)
  # sys.stderr.write("len(eserlist)=%s\n" % L)
  thisese=eserlist.pop(random.randint(0,L-1))
  result.append(thisese)
 latex_header=r"""
%===================================================================
\documentclass[twoside,a4paper,leqno]{article}
%===================================================================
\usepackage{mathpazo}
\usepackage[bubblesheet]{mcq}
% \usepackage[italian]{babel} 
\usepackage{polyglossia}
\setdefaultlanguage{italian} 
\usepackage{titlesec}
\titlespacing{\subsection}{0pt}{-20pt}{-20pt}

%===================================================================
\headline{---}

\puntigiusta{3}
\puntisbagliata{-1}
\puntiempty{0}

%===================================================================
% NEW COMMANDS
\newcommand{\RR}{\mathbb{R}}
\newcommand{\CC}{\mathbb{C}}
\newcommand{\ZZ}{\mathbb{Z}}
\newcommand{\NN}{\mathbb{N}}
\renewcommand{\AA}{\mathbb{A}}
\newcommand{\EE}{\mathbb{E}}
\newcommand{\QQ}{\mathbb{Q}}
\newcommand{\PP}{\mathbb{P}}
\newcommand{\FF}{\mathbb{F}}
\newcommand{\KK}{\mathbb{K}}
\newcommand{\from}{\colon}
\newcommand{\vx}{\boldsymbol{x}}
\newcommand{\vy}{\boldsymbol{y}}
\newcommand{\vz}{\boldsymbol{z}}
\newcommand{\zero}{\boldsymbol{0}}
\newcommand{\va}{\boldsymbol{a}}
\newcommand{\vb}{\boldsymbol{b}}
\newcommand{\vv}{\boldsymbol{v}}
\newcommand{\vw}{\boldsymbol{w}}
\newcommand{\vect}[1]{\overrightarrow{#1}}
\def\presuper#1#2{\mathop{}%
   \kern 2\scriptspace
   \mathopen{\vphantom{#2}}^{#1}%
   \kern-2\scriptspace#2}
\newcommand{\trasposta}[1]{%
{\presuper{t}{}{#1}}%
}
\usepackage{scalefnt}
%===================================================================
\begin{document}
"""  + ( "\\bubblesheet[2]{%i}{4}\n\n\n\\begin{esercizi*}{}" % n ) + r"""
{\itshape\small\noindent
(Segnare \textbf{la} risposta corretta, e riportarla poi nella prima
pagina.
Una risposta giusta vale $+3$,
una risposta sbagliata $-1$, nessuna risposta o più di una risposta
segnata: $0$.
}
"""
 latex_footer=r"""
\end{esercizi*}
\end{document}
""" 
 s=latex_header
 for exe in result:
  s += """
\\begin{exerm}
%s
\\end{exerm}
""" % exe
 s += latex_footer
 if VERBOSE:
   sys.stderr.write("Done!\n")
 return s
#-----------------------------------------------------------------------
def csvjoin(files):
 import csv
 matr_db={}
 tables=[]
 for f in files:
  thistable=[]
  csvreader=csv.reader(open(f,'rb'),delimiter=";")
  for x in csvreader:
   _, fullname, matricola, _, _, voto  = x
   thistable.append( (matricola,fullname,voto) )
   if not matricola  in matr_db:
    matr_db[matricola]=[fullname]+[""]*len(files)
  tables.append(thistable)
 ii=0
 for table in tables:
  ii +=1
  for matricola,fullname,voto in table:
   matr_db[matricola][ii] = voto
 res=""
 for matricola in matr_db:
  res += ("%s;%s;" % (matr_db[matricola][0],matricola)) + ";".join(matr_db[matricola][1:] ) + "\n"
 return res
#-----------------------------------------------------------------------
def merge_files(s,uidfile):
 matr_db={} 
 res = ""
 tokens=uidfile.split(":")
 if len(tokens)==1:
   uidfile_name=tokens[0]
   name_pos=1
   matr_pos=2
   csv_sep=":"
 elif len(tokens) == 2:
   uidfile_name=tokens[0]
   if len(tokens[1]) != 3:
    raise Exception("Bad CSV format %s!\n" % tokens[1] )
   name_pos=int(tokens[1][2])-1
   csv_sep=tokens[1][1]
   matr_pos=int(tokens[1][0])-1
 elif len(tokens) == 3:
   uidfile_name=tokens[0]
   name_pos=int(tokens[2])-1
   csv_sep=":"
   matr_pos=int(tokens[1])-1
 else:
  raise Exception("Bad UID filename %s!\n"  % uidfile) 
 sys.stderr.write("Reading UID data from file %s with columns %s %s, delimiter=%s\n" % (uidfile_name, name_pos, matr_pos, csv_sep )) 
 csvReader = csv.reader(open(uidfile_name, 'rb'), delimiter=csv_sep)
 for x in csvReader:
   try: 
     name=x[name_pos]
     matr=x[matr_pos]
     name=name.strip()
     matr=matr.strip()
     if matr in matr_db:
      raise Exception("duplicate uid %s!!!!\n" % matr )
     matr_db[matr]=name
   except Exception , v :
     if VERBOSE: sys.stderr.write("UID line `%s' skipped....with error: %s\n" % (str(x).strip(),v) )
 for x in s: 
   if len(x)<=4:
    res += x
    continue
   try:
     codice,name,matr, risposte, voto = x.split(":")
     name=name.strip()
     matr=matr.strip()
     if name == '' and matr in matr_db:
       res += "%s:%s\t:%s:%s:%s" % (codice,matr_db[matr],matr,risposte,voto)
     else:
       res += x 
   except Exception , v:
     if VERBOSE: sys.stderr.write("line `%s' skipped.... with error: %s\n" % (x.strip(),v) )
     res += x
 return res
#-----------------------------------------------------------------------

import xml.etree.ElementTree as ET
import re

# A4_width=210.0 ##mm
# A4_height=297.0 ## mm
# bubble_offset=(-2.0,-2.0)

def convert_to_mm(sp):
 return (float(sp) / 186467.98110236222)

def getdb_labels(basename):
 LBLFILE=basename+'.lbl'
 POSFILE=basename+'.pos'
 lbl=open(LBLFILE).readlines()
 pos=open(POSFILE).readlines()
 
 lblreg=re.compile(r'{(?P<n>.*?)}{(?P<c>.*?)}{(?P<v>.*?)}')
 posreg=re.compile(r'{(?P<v>.*?)}{(?P<X>.*?)}{(?P<Y>.*?)}')

 result=[]
 N = len(lbl)
 if N <> len(pos):
  raise Exception("WARNING: lbl <> pos!!\n")
 ii = 0 
 for x in lbl:
  if lblreg.search(x):
   n,group,numitem = lblreg.search(x).groups()
   if int(n) != ii+1:
    raise Exception ("n != ii+1")
   result.append( (group,numitem) )
  else:
   raise Exception("riga %s non va...\n" % x )
  ii += 1 
 ii = 0 
 for x in pos:
  if posreg.search(x):
   valore,X,Y = posreg.search(x).groups()
   X = convert_to_mm(X) #+ bubble_offset[0]
   Y = convert_to_mm(Y) #+ bubble_offset[1]
   result[ii] += (valore, X, Y) 
  else:
   raise Exception("riga %s non va...\n" % x )
  ii += 1
 result_db={}
 for group,numitem,valore,X,Y in result:
  if not group in result_db:
   result_db[group]={}
  if group=='head':
   result_db[group][numitem]=valore
  else:
   result_db[group][numitem]=(X,Y)
 return result_db 
 
def txt2py(t,s):
 if t=='float':
  return float(s)
 elif t=='int':
  return int(s)
 elif t=='coord':
  return tuple([float(x) for x in s.split(',')])
 else:
  if s[-2:]=='pt':
   # convert to mm
   s=float(s[:-2]) * 0.3515  
  return s
 
def py2txt(s):
 if type(s)==type((1,2)): 
  return ('coord',",".join( [str(x) for x in s ]))
 elif type(s)==type(1):
  return ('int',str(s))
 elif type(s)==type(1.0):
  return ('float',str(s) )
 else:
  return ('str',s)
 
def db2xml(db,filename):
 root = ET.Element("OMRdata")
 root.tail="\n"
 for gr in db:
  tmp=ET.SubElement(root,gr)
  tmp.tail="\n"
  for k in db[gr]:
    t,v=py2txt(db[gr][k])
    tmpk=ET.SubElement(tmp,"item")
    tmpk.attrib['n']=k
    tmpk.attrib['type']=t
    tmpk.text=v
    tmpk.tail="\n"
 tree = ET.ElementTree(root)
 tree.write(filename)
 return 
 
def xml2db(xmlfile):
 ndb={}
 parser = ET.XMLParser(encoding="utf-8")
 ntree = ET.parse(xmlfile,parser=parser)
 root=ntree.getroot()
 for node in root:
  tmpdb={}
  for item in node:
   n=item.attrib['n']
   t=item.attrib['type']
   content=item.text
   tmpdb[n]=txt2py(t,content)
  ndb[node.tag]=tmpdb
 return ndb 


#if __name__=='__main__':
# db=getdb_labels('c2')
# db2xml(db,'c2.xml')
# print xml2db('c2.xml')

#-----------------------------------------------------------------------

def transform_tex_entities(s):
 for k in translate_dictionary.keys():
   s = re.sub(k.encode('utf-8'), translate_dictionary[k].encode('utf-8'), s )
 return s

def translate_math_chars(s):
 for k in translate_math.keys():
  s = re.sub(k.encode('utf-8'), translate_math[k].encode('utf-8'), s )
 return s

def escape_control_characters(s):
 s=transform_tex_entities(translate_math_chars(s))
 return re.sub(r"[\\~=#{}:]", lambda x: "\\"+x.group(), s )

def prepare_xhtml(s):
 s=remove_empty_lines(s)
 return replace_url(transform_tex_entities(translate_math_chars(s)))

def remove_empty_lines(s):
 newlist=[x for x in s.split("\n") if len(x.strip())>0 ]
 return  "\n".join(newlist)

#-----------------------------------------------------------------------
class Esercizio:
 def __init__(self,testo,type='EXERM',numero_colonne=1,risposte=None,src='',fb=None):
  self.qtitle,self.testo=get_qtitle(testo)
  self.type=type #vero|falso,exerm
  self.numero_colonne=numero_colonne
  self.risposte=risposte
  self.src=src
  self.fb=fb
 def __repr__(self):
  return self.__str__()
 def __str__(self):
  risposte=''
  fb=self.fb
  if not fb: 
   fb=''
  if self.risposte:
   risposte="\n".join([str(x) for x in self.risposte])
  return """%% type: %s fbbegin--%s--fbend
%s
%s""" % ( self.type,fb, self.testo,risposte)
 def numero_risposte(self):
  if self.risposte:
   return len(self.risposte)
  else:
   return 0
 def latex_perm(self,perm):
  res="\\begin{exerm}\n" + self.testo + "\n"
  if self.risposte:
   res += "\\begin{rispm}[%i]\n" % self.numero_colonne
   n=len(self.risposte)
   for i in range(n):
    res += (self.risposte[perm[i]]).latex()
   res += "\\end{rispm}\n"
  else:
   if self.type=="VERO":
    res +="\\vero\n"
   elif self.type=="FALSO":
    res +="\\falso\n"
   else:
    # res += "%%BOH\n"
    raise Exception("boh") 
  res += "\\end{exerm}\n"
  return res
 def latex_withstats(self,stats):
  res="\\begin{exerm}\n" + self.testo + "\\nopagebreak\\newline\n"
  res += stats[-1]
  if self.risposte:
   res += "\\begin{rispm}[%i]\n" % self.numero_colonne
   n=len(self.risposte)
   for i in range(n):
    res += (self.risposte[i]).latex()
    res += stats[i]
   res += "\\end{rispm}\n"
  else:
   if self.type=="VERO":
    res +="\\vero\n"
   elif self.type=="FALSO":
    res +="\\falso\n"
   else:
    raise Exception("boh") 
  res += "\\end{exerm}\n"
  return res
 def solution_perm(self,perm):
  res=[]
  # lettere='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  if self.risposte:
   n=len(self.risposte)
   for i in range(n):
    ri=self.risposte[perm[i]]
    lt=lettere[i]
    if ri.giusta:
     res += [lt]
    elif ri.punti is not None: ## anche se e' zero! 
     res += ["%s[%f]" % (lt,ri.punti)]
  else:
     if self.type=="VERO":
      res += ["vero"]
     elif self.type=="FALSO":
      res += ["falso"]
     else:
      # res += ["None"]  __HERE__
      raise Exception("boh") 
  return (", ".join(res))+";"

 def solution_db_perm(self,perm):
  res={}
  if self.risposte:
   n=len(self.risposte)
   for i in range(n):
    ri=self.risposte[perm[i]]
    lt=lettere[i]
    if ri.giusta:
     res[lt] = "giusta"
    elif ri.punti is not None:
     res[lt] = ri.punti
  else:
     if self.type=="VERO":
      res['A'] = "giusta"
     elif self.type=="FALSO":
      res['B'] = "giusta"
     else:
      raise Exception("boh") 
  return res

 def gift(self):
  if self.type=='EXERM':
   return """%s%s
{
%s
}
""" %  (self.qtitle,escape_control_characters(remove_empty_lines(self.testo)), "\n".join( [ris.gift() for ris in self.risposte]))
  elif self.type in ("VERO","FALSO"):
   if self.type=="VERO": 
    ans="TRUE"
   elif self.type=="FALSO":
    ans="FALSE"
   else:
    raise Exception("big problem")
   if self.fb:
    fb="#" + escape_control_characters(remove_empty_lines(self.fb))
   else:
    fb=""
   return """%s%s
{%s%s}
""" % (self.qtitle,escape_control_characters(remove_empty_lines(self.testo)), ans ,fb) 
#-----------------------------------------------------------------------
 def xhtml(self):
  if self.type=='EXERM':
   return """%s%s
<ol class="toggle-view">
%s
</ol>
""" %  (self.qtitle,prepare_xhtml(self.testo), "\n".join( [ris.xhtml() for ris in self.risposte]))
  elif self.type in ("VERO","FALSO"):
   # __HERE__ CHECK
   if self.type=="VERO": 
    newrisposte=[ Risposta("Vero",giusta=True), Risposta("Falso", giusta=False, fb=self.fb) ]
   elif self.type=="FALSO":
    newrisposte=[ Risposta("Vero",giusta=False,fb=self.fb), Risposta("Falso", giusta=True) ]
   else:
    raise Exception("big problem")
   newself=Esercizio(self.testo, risposte=newrisposte)
   return newself.xhtml()

#-----------------------------------------------------------------------
def get_qtitle(s):
  s=s.strip()
  reg=re.compile(r"\\qtitle{(?P<p>.+?)}", re.M)
  regx=re.compile(r"\\qtitle{.+?}", re.M )
  qtitle=""
  if reg.search(s):
   qtitle="::"+reg.search(s).group('p').strip()+"::\n"
   s=regx.sub("",s).strip()
  return qtitle,s
#-----------------------------------------------------------------------
def split_variants(s):
 s=s.strip()
 reg=re.compile(r"\\begin{varianti}(?P<x>.+?)\\end{varianti}", re.M and re.DOTALL)
 #__ reg_split=re.compile(r"\\varitem",re.M) # BUG!!! \varitem can be commented...
 #__  reg_split=re.compile(r"^([^%$]*)\\varitem",re.M) # New regex 2018-10-30
 # reg_split=re.compile(r"^[^%\n\r]*\\varitem",re.M) # New regex 2018-10-30
 reg_split=re.compile(r"\\varitem",re.M) # BUG!!! \varitem can be commented... strip comments first.
 if reg.search(s) and reg_split.search(s):
  data=reg_split.split(reg.search(s).group('x').strip())[1:]
  return data
 else:
  return [s]
  
 
#-----------------------------------------------------------------------
class MultiEsercizio:
 def __init__(self,s):
  self.src=s
  self.type='Multiesercizio'
  s=strip_latex_comments(s)
  if VERBOSE: sys.stderr.write("DEBUG: MultiEsercizio __init__(self,s) with s=\n```%s```\n" % s)
  if VERBOSE: sys.stderr.write("DEBUG: split_variants=```%s```\n" % split_variants(s))
  self.esercizi=[parse_esercizio(x) for x in split_variants(s)]
  numq=[x.numero_risposte() for x in self.esercizi]
  numq.sort()
  if numq[0] != numq[-1]:
   raise Exception(r"MultiEsercizio \begin{varianti}\end{varianti} with wrong answer numbers!")
  self.numrisposte=numq[0]
  ## __HERE__  
  if VERBOSE: sys.stderr.write("WARNING: MultiEsercizio stats (should) work only if its (multi)answers are all aligned!!!!\n")
  self.risposte= self.esercizi[0].risposte
 def numero_risposte(self):
  return self.numrisposte
 def latex_withstats(self,stats):
  ese = self.esercizi[0]
  sys.stderr.write(r"MultiEsercizio \begin{varianti}\end{varianti}: variant 1 chosen."+"\n  => Answers count might be wrong!\n")
  return ese.latex_withstats(stats)
 def gift(self):
  res=''
  ii=0
  for x in self.esercizi:
   ii += 1
   res += ("\n// [Var. %i]\n" % ii) + x.gift()
  sys.stderr.write((r"MultiEsercizio \begin{varianti}\end{varianti}: %i variants." % ii )+"\n")
  return res
 def xhtml(self):
  sys.stderr.write("Warning: MultiEsercizio XHTML... not sure the output will be OK...\n")
  res=''
  ii=0
  for x in self.esercizi:
   ii += 1 
   res += "\n" + x.xhtml()
  sys.stderr.write((r"MultiEsercizio \begin{varianti}\end{varianti}: %i variants." % ii) + "\n" )
  return res

#-----------------------------------------------------------------------
class Risposta:
 def __init__(self,testo,giusta=False,punti=None,fb=None,src=''):
  self.testo = testo.strip()
  self.giusta=giusta
  self.punti=punti
  if fb:
   self.fb=fb.strip()
  else:
   self.fb=fb
  self.src=''
 def __repr__(self):
  return self.__str__()
 def __str__(self):
  comment=''
  if self.giusta: 
   comment += "giusta;"
  if self.punti is not None: 
   comment += "punti=%s;" % self.punti
  if self.fb: 
   comment += "fb=%s" % self.fb
  return """%% risposta %s
%s""" % (comment, self.testo  ) 
 def latex(self):
  res="\\risp"
  if self.giusta: 
   res += "[=]\n"
  if self.punti is not None:
   res += "[%s]\n"  % self.punti
  return res + " "+ self.testo +"\n"
 def gift(self):
  if self.giusta:
   risp = "="
  else:
   risp="~"
  if self.punti is not None:
   risp += "%%%i%% " % int(self.punti  * 100.0)
  risp += " " + escape_control_characters(remove_empty_lines(self.testo))
  if self.fb:
   risp += "\n#%s" % escape_control_characters(remove_empty_lines(self.fb))
  return risp
 def xhtml(self):
  risp="<li>"
  risp += prepare_xhtml(self.testo)
  risp += """<span class="mymark">+</span>"""
  if self.giusta:
   risp += """\n<p class="giusto"><strong>S&Igrave;!</strong>\n<br/>\n"""
  else:
   risp += "\n<p><strong>NO!</strong>\n<br/>\n"
  if self.fb:
   risp += "%s" % prepare_xhtml(self.fb)
  risp += "</p></li>"
  return risp

#-----------------------------------------------------------------------
def strip_latex_comments(s):
 reg_comment=re.compile(r"\\%",re.M)
 reg_comment_back=re.compile(r"__PERCENT__",re.M)
 s=reg_comment.sub("__PERCENT__",s)
 reg=re.compile(r"(%+.*?\n)",re.M) 
 s=reg.sub("", s)
 s=reg_comment_back.sub(r"\\%",s)
 reg=re.compile(r"( +)",re.M)
 s=reg.sub(" ", s)
 return s
#-----------------------------------------------------------------------
def extract_esercizi(s):
 reg=re.compile(r"\\begin{exerm}(.+?)\\end{exerm}", re.M and re.DOTALL)
 return [x.strip() for x in reg.findall(s)]
#-----------------------------------------------------------------------
def make_template(s):
 reg=re.compile(r"\\begin{exerm}.+?\\end{exerm}", re.M and re.DOTALL)
 s=reg.sub("%%__EXERM_REMOVED__%%",s)
 reg=re.compile(r"^(?P<header>.+?)\\begin{document}(?P<body>.+?)\\end{document}",re.M and re.DOTALL)
 body="\\setcounter{subsection}{0}\setcounter{page}{1}\n" + reg.search(s).group('body')
 header=reg.search(s).group('header')
 return (header,body)
#-----------------------------------------------------------------------
def parse_risposta(s):
 fb=None
 punti=None
 giusta=False
 s=s.strip()
 reg=re.compile(r"^(?P<punti>\[.+?\])",re.M )
 if reg.match(s):
  punti=reg.match(s).group('punti')[1:-1] 
  s=reg.sub("",s).strip()
  if punti=='=':
   giusta=True
   punti=None
  else:
   punti=float(punti)
 reg=re.compile(r"(?P<fb>\\fb{.+})",re.M and re.DOTALL)   # greedy
 if reg.search(s):
  fb=reg.search(s).group('fb')[4:-1]
  s=reg.sub("",s).strip()
 return Risposta(s, punti=punti,giusta=giusta, fb=fb) 

#-----------------------------------------------------------------------
def parse_esercizio(s):
 if VERBOSE: sys.stderr.write("DEBUG: parse_esercizio\n")   
 # reg=re.compile(r"(.+?)\\begin{rispm}(.+?)\\end{rispm}", re.M and re.DOTALL) # IT IS OK TO BE EMPTY...
 reg=re.compile(r"(.*?)\\begin{rispm}(.+?)\\end{rispm}", re.M and re.DOTALL)
 strings_found=[x for x in reg.findall(s)]
 if strings_found == []:
 #allora e' vero-falso:
  reg=re.compile(r"(?P<verofalso>\\vero|\\falso)(?P<fb>\[.+\])*", re.M and re.DOTALL)
  if reg.search(s):
   fb=reg.search(s).group('fb')
   if fb:
    fb=fb[1:-1].strip()
   if reg.search(s).group('verofalso') == "\\vero":
    result = Esercizio(reg.sub("",s).strip(),type="VERO",fb=fb)
    # result = ("VERO", reg.sub("",s) ) 
   else:
    result = Esercizio(reg.sub("",s).strip(),type="FALSO",fb=fb)
    # result = ("FALSO", reg.sub("",s) ) 
  #else:
  #  result = Esercizio(reg.sub("",s).strip()) #__HERE__ 
  # TODO RAISE EXCEPTION __TODO__
  raise Exception("ERROR: the following is not a proper exer!\n<<<<<<\n%s\n>>>>>>\n" % s)
  return None
 elif len(strings_found)>1:
  # si tratta di un esercizio con varianti.
  return MultiEsercizio(s)
  for x in strings_found:
   sys.stderr.write("ITEM:\n%s\n" % str(x))
  raise Exception("Errore strano")
  sys.exit(2)  
 # quindi supponiamo che sia a risposta multipla: 
 # per prima cosa il numero di colonne.
 reg=re.compile(r"^(?P<numcols>\[[0-9]+?\])",re.M )
 testo,rispm=strings_found[0]
 if reg.match(rispm):
  numero_colonne=int(reg.match(rispm).group('numcols')[1:-1] )
  rispm=reg.sub("",rispm).strip()
 else:
  numero_colonne=1 # default
 reg=re.compile(r"\\risp",re.M)
 tokens=[parse_risposta(x) for x in reg.split(rispm)[1:]]
 result = Esercizio(testo,type="EXERM",numero_colonne=numero_colonne,risposte=tokens)
 return result
 
#-----------------------------------------------------------------------
RG=random.Random(MCQRANDOMSEED)
def random_permutation(n):
 tmplist=range(n)
 # random.shuffle(tmplist)
 RG.shuffle(tmplist)
 return tmplist
#-----------------------------------------------------------------------
RGC=random.Random(MCQRANDOMSEED)
def genera_codice(vl):
 if not vl:
  pref=""
 else:
  pref=vl
 generati=[]
 simboli="ABEFGHxyz12367"
 lunghezza=4
 tentativi=0
 max_tentativi=10000
 while tentativi<max_tentativi:
  tentativi += 1
  tmpc=pref+"".join([ RGC.choice(simboli) for x in range(lunghezza) ])
  if not tmpc in generati:
    generati += [tmpc]
    yield tmpc
 raise Exception("genera_codice: troppi tentativi")
#-----------------------------------------------------------------------
def extract_punti(s):
  giusti=1
  sbagl=-1
  empty=0
  reg_giusti=re.compile(r"\\puntigiusta{(?P<p>.+?)}", re.M)
  reg_sbagl=re.compile(r"\\puntisbagliata{(?P<p>.+?)}", re.M)
  reg_empty=re.compile(r"\\puntiempty{(?P<p>.+?)}", re.M)
  if reg_giusti.search(s):
    giusti=float(reg_giusti.search(s).group('p').strip())
  if reg_sbagl.search(s):
    sbagl=float(reg_sbagl.search(s).group('p').strip())
  if reg_empty.search(s):
    empty=float(reg_empty.search(s).group('p').strip())
  sys.stderr.write("Extracted Punti: %2.2f %2.2f %2.2f\n" % (giusti,sbagl,empty))
  return (giusti,sbagl,empty)

#-----------------------------------------------------------------------
def extract_formula(s):
  formula=None
  reg_formula=re.compile(r"\\formulavoto{(?P<p>.+?)}", re.M)
  if reg_formula.search(s):
    formula=reg_formula.search(s).group('p').strip()
  return formula
#-----------------------------------------------------------------------
def extract_headline(s):
  headline=None
  reg_headline=re.compile(r"\\headline{(?P<p>.+?)}", re.M)
  if reg_headline.search(s):
    headline=reg_headline.search(s).group('p').strip()
  return headline
#-----------------------------------------------------------------------
def extract_variant(s):
  variant=None
  reg_variant=re.compile(r"\\variantlabel{(?P<p>.+?)}", re.M)
  if reg_variant.search(s):
    variant=reg_variant.search(s).group('p').strip()
  return variant
#-----------------------------------------------------------------------
def extract_bubblesheet_numbers(s):
 reg_bc=re.compile(r"\\bubblesheet(\[.*\]|){(?P<questions>.+?)}{(?P<answers>.+?)}", re.M)
 res=reg_bc.search(s)
 if res:
  questions=res.group('questions')
  answers=res.group('answers')
  return (int(questions), int(answers))
 else:
  return None
#-----------------------------------------------------------------------
def extract_mcq_options(s):
 reg_options=re.compile(r"\\usepackage\[(?P<options>.+?)\]{mcq}", re.M)
 res=reg_options.search(s)
 if res:
  options=res.group('options')
  return options.split(",")
 else:
  return None
#-----------------------------------------------------------------------
def extract_variant(s):
  variant=None
  reg_variant=re.compile(r"\\variantlabel{(?P<p>.+?)}", re.M)
  if reg_variant.search(s):
    variant=reg_variant.search(s).group('p').strip()
  return variant
#-----------------------------------------------------------------------
def generate_copies(s,num_copies):
 global SOLUTIONS_FILE, DB_FILE, DB_STATS_FILE
 DB_LIST={}
 DB_LIST['__punti__'] = extract_punti(s)
 DB_LIST['__formula__'] = extract_formula(s)
 VARIANT_LABEL = extract_variant(s)
 DB_LIST['__variantlabel__']=VARIANT_LABEL
 DB_LIST['__permutations__'] = {}
 header,body=make_template(s) 
 esercizi=[parse_esercizio(es) for es in extract_esercizi(s)]
 numero_esercizi=len(esercizi)
 numero_maxrisposte=0
 sys.stderr.write("# number of questions: %i\n" % numero_esercizi )
 DB_LIST['__stats__'] = [{'0':0 } for x in range(numero_esercizi) ]
 stats_punti_right=DB_LIST['__punti__'][0]
 stats_punti_wrong=DB_LIST['__punti__'][1]
 stats_punti_zero=DB_LIST['__punti__'][2]
 DB_LIST['__stats_punti__'] = [{'0': stats_punti_zero } for x in range(numero_esercizi) ]
 for i in range(numero_esercizi):
  ese=esercizi[i]
  if ese.numero_risposte()>numero_maxrisposte:
    numero_maxrisposte=ese.numero_risposte()
  for x in range(ese.numero_risposte()):
   DB_LIST['__stats__'][i][lettere[x]] = 0
   if ese.risposte[x].giusta: 
    tmp_punti = stats_punti_right
   else:
    tmp_punti=stats_punti_wrong
   DB_LIST['__stats_punti__'][i][lettere[x]] =  tmp_punti
  if ese.numero_risposte() ==0:
   DB_LIST['__stats__'][i]['A'] = 0 
   DB_LIST['__stats__'][i]['B'] = 0 
 reg=re.compile(r"%%__EXERM_REMOVED__%%",re.M)
 sys.stderr.write("# max number of answers:  %i\n" % numero_maxrisposte)
 bubble_data=extract_bubblesheet_numbers(s) 
 if bubble_data:
  if numero_esercizi != bubble_data[0] or numero_maxrisposte != bubble_data[1]:
   sys.stderr.write("""\n  *** ERROR *** : WRONG BUBBLESHEET DATA!
  *** there are %i exercises with at most %i answers!!!
  *** but the bubblesheet has %i questions and %i answers,
  *** change \\bubblesheet args in XeLaTeX main file!!!
""" % (numero_esercizi, numero_maxrisposte, bubble_data[0],bubble_data[1]))
   exit_on_error('') #sys.exit(1) 
 mcq_options=extract_mcq_options(s)
 if mcq_options:
  if 'sol' in mcq_options:
    sys.stderr.write("\n  *** WARNING *** : mcq option `sol' !!! IT IS YOUR RESPONSIBILITY TO REMOVE IT !!!\n\n")
 splitted_body=reg.split(body)
 res=header  + "\\checkhassol\\writelblfilefalse\n\\begin{document}\n"
 gc=genera_codice(VARIANT_LABEL)
 for nperm in range(num_copies):
   codice=gc.next()
   solutionline="%s: \t" % codice
   solutionarray=[]
   DB_solutions=[]
   if num_copies>1:
    perm=random_permutation(numero_esercizi)
   else:
    perm= range(numero_esercizi)
   DB_LIST['__permutations__'][codice.upper()]={'perm_esercizi':perm,'ese_perm':[] }
   res += "\\setcodice{%s}\n" % codice
   res += splitted_body[0]
   # res += "\\rhead{{\\tt [%s]-p\\thepage/\\pageref{LastPage}}}\n" % codice
   for i in range(numero_esercizi):
    ese=esercizi[perm[i]]
    if isinstance(ese,MultiEsercizio):
     ese=random.choice(ese.esercizi)
    if num_copies>1:
     eseperm=random_permutation(ese.numero_risposte())
    else:
     eseperm=range(ese.numero_risposte())
    res += ese.latex_perm(eseperm)
    res += splitted_body[i+1]
    solutionarray += [("(%i) " % ( i+1)) + ese.solution_perm(eseperm) ] 
    DB_solutions += [ ese.solution_db_perm(eseperm) ]
    DB_LIST['__permutations__'][codice.upper()]['ese_perm'] += [eseperm]
   solutionline += "\t".join(solutionarray)
   if VERBOSE: sys.stderr.write("WRITING Solution Line: '%s' on file %s \n" % (solutionline,SOLUTIONS_FILE.name))
   SOLUTIONS_FILE.write(solutionline + "\n")
   DB_LIST[codice.upper()] =  DB_solutions
   res += "\\cleardoublepage\n"
 res += "\\end{document}\n"
 pickle.dump(DB_LIST,DB_FILE); DB_FILE.close()
 SOLUTIONS_FILE.close()
 return res  
#-----------------------------------------------------------------------
def make_combina_voti(s):
 sys.stderr.write("formulavoto: %s\n" % s )
 if not s:
  return default_combina_voti
 else:
  ss="""def ff(x,y):
  x=float(x)
  y=float(y)
  return """ + s 
  exec (ss)
  return ff
#-----------------------------------------------------------------------
def permutazione_inversa(p):
 n=len(p)
 return [p.index(i) for i in range(n)] 

#-----------------------------------------------------------------------
def number_of_items(dbl):
 for x in dbl.keys():
  if x[0]=='_':
   continue
  return len(dbl[x])

#-----------------------------------------------------------------------
def correggi(dbl,data):
 dbl['__stats_lista__']=[]
 result = []
 lista_corrette =[] 
 # lettere='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
 ptg,pts,pte=dbl['__punti__']
 sys.stderr.write("pts: %2.2f %2.2f %2.2f\n" % (ptg,pts,pte) )
 combina_voti=make_combina_voti(dbl['__formula__'])
 comment= ""
 line_number=0
 for l in data.split("\n"):
  line_number += 1
  if l and  l[0] != "#":
   try:
     codice,name,matr, risposte, voto = l.split(":")
     codice=codice.strip().upper()
     name=name.strip()
     matr=matr.strip()
     risposte=risposte.strip()
     #eliminare spazi
     risposte=re.sub(r'\s','',risposte)
     if voto:
      voto = float(voto)
     else:
      voto = 0
   except Exception , v:
     sys.stderr.write("** riga %s : Errore %s\n" %( l,v) )
     exit_on_error('ERROR') #sys.exit(1)
   if codice not in dbl.keys():
     if dbl['__variantlabel__']:
      if VERBOSE: sys.stderr.write("WARNING! Codice %s not found!\n" % codice )
      continue ## __HERE__
     else:
      nono=[x for x in dbl.keys() if not x.startswith('__')]
      nono.sort()
      sys.stderr.write("Exam Code `%s` not found!\n" % codice )
      sys.stderr.write("Available codes:\n%s\n" % (" ".join(nono),) )
      exit_on_error('ERROR') #sys.exit(1)
   dbsols=dbl[codice] 
   reversepermdb=dbl['__permutations__'][codice]
   votoparziale=0.0; 
   if len(dbsols) != len(risposte):
    raise Exception("Not enough answers in valutfile `%s' for key %s (%i<>%i)! " % (VALFILE,codice,len(dbsols), len(risposte))  )
   corrette=[]
   for i in range(len(dbsols)):
    cer=risposte[i].upper()
    if cer=='0':
     dbl['__stats__'][reversepermdb['perm_esercizi'][i]]['0'] +=1  
    else:
     permutazione = (reversepermdb['ese_perm'][i])
     if not cer in lettere:
      sys.stderr.write("answer key '%s' not valid (codice=%s):\n%s\n" % (str(cer),codice,l))
      exit_on_error('ERROR') #sys.exit(1)
     if VERBOSE: sys.stderr.write("perm= %s\n" % str(permutazione))
     if len(permutazione)>1:
      if lettere.index(cer) in permutazione:
       origA =permutazione[lettere.index(cer)]
      else:
       sys.stderr.write("FATAL ERROR: answer '%s' (n. %i at line %i) for key %s  not in range %s-%s\n" % (cer,i+1,line_number,codice,lettere[0],lettere[len(permutazione)-1]) )
       sys.stderr.write("** FIX THE DATA FILE and then re-run! **\n" )
       exit_on_error('ERROR') #sys.exit(1)
     else:
      origA=lettere.index(cer)
     try:
      dbl['__stats__'][(reversepermdb['perm_esercizi'])[i]][lettere[origA]] +=1 
     except:
      sys.stderr.write("stats are not working!\n")
    if cer in dbsols[i].keys():
     if dbsols[i][cer] == 'giusta':
       votoparziale += ptg
       corrette += [ptg]
     else: 
       votoparziale += dbsols[i][cer] # *1.0 / 100.0
       corrette += [dbsols[i][cer]]
    elif cer != '0':
       votoparziale  +=  pts
       corrette += [ pts ] 
    else:
       votoparziale += pte
       corrette += [pte] 
   # votototale=combina_voti(votoparziale/len(dbsols) , voto )
   votototale=combina_voti(votoparziale , voto )
   # result += "%s;%s;%s;%0.2f;%0.2f;%0.2f\n" % (codice,name,matr,votoparziale,voto,votototale ) 
   result += [ (codice,name,matr,votoparziale,voto,votototale )  ]
   dbl['__stats_lista__'] += [ (votoparziale,voto,votototale)] 
   lista_corrette += [ [ corrette[i] for i in permutazione_inversa(reversepermdb['perm_esercizi']) ] ]
   # print "TMP: ", sum(corrette), votoparziale
 riordina_somme(lista_corrette)
 #print "TOT=",  sum([sum([x for x in xx]) for xx in lista_corrette])
 #print "TOT2=",  sum([xx[-1] for xx in result ])
 dbl['__indici__'] = calcola_indici(lista_corrette,ptg)
 return result
#-----------------------------------------------------------------------
def calcola_indici(li,ptg):
  n=len(li)
  if n==0:
   return None
  numq=len(li[0])
  quota=max(int(0.27 * n),1) ## 27% ? 
  if int(0.27*n) == 0:
     sys.stderr.write("WARNING: quota == 0 => quota = 1 \n")
  UG=li[:quota]
  LG=li[-quota:]
  if VERBOSE: sys.stderr.write("UG,LG: %s %s\n" % ( len(UG), len(LG) ))
  discr_ind=[0 for x in range(numq)]
  facil_ind=[0 for x in range(numq)]
  for i in range(numq):
    # print "i= ", i, "ptg= ", ptg
    numc_UG=len([x[i] for x in UG if x[i] == ptg ] )
    numc_LG=len([x[i] for x in LG if x[i] == ptg ] )
    # sys.stderr.write("%s - %s / %s = %s / %s \n" % (numc_UG, numc_LG,quota,numc_UG-numc_LG,quota) )
    discr_ind[i] = (numc_UG - numc_LG ) * 1.0 / quota
    facil_ind[i] = len( [x[i] for x in li if x[i] == ptg ] ) * 1.0 / n
    tmpli=[x[i] for x in li] 
    # print sum(tmpli), len([x for x in tmpli if x == ptg] ), facil_ind[i]
    if VERBOSE: sys.stderr.write("ind %s: %s %s\n" % (i,discr_ind[i],facil_ind[i]) )
  return [(discr_ind[i],facil_ind[i]) for i in range(numq) ]
#-----------------------------------------------------------------------
def display(li):
  result = ''
  for r in li:
   result += "%s;%s;%s;%0.2f;%0.2f;%0.2f\n" % r
  return result
#-----------------------------------------------------------------------
def display_pub(li,mp):
  result = ''
  for r in li:
   # result += "%s:%0.2f/%0.2f\n" % (r[2],r[-3],mp)  __HERE__ changed to after formulavoto
   # result += "%s:%0.2f/%0.2f\n" % (r[2],r[-1],mp) 
   result += "%s:%0.2f/%0.2f\n" % (r[2],r[-3],mp) 
  return result
#-----------------------------------------------------------------------
def compare_matr(l,r):
 if l[2] < r[2]:
  return -1
 elif l[2] > r[2]:
  return 1
 else:
  return 0
def compare_nome(l,r):
 if l[1] < r[1]:
  return -1
 elif l[1] > r[1]:
  return 1
 else:
  return 0
def max_voto(li):
 return max ([ r[-1] for r in li] )
def min_voto(li):
 return min ([ r[-1] for r in li] )
def media(li):
 return sum([ r[-1] for r in li] ) *1.0/ len(li)  
def mediana(li):
 v=[r[-1] for r in li]
 v.sort()
 # sys.stderr.write("%s\n" % str(v))
 return v[(len(v)-1)/2]
def percent(li):
 insuff=0;medi=0;bene=0
 for r in li:
  if r[-1] >= 24:
   bene += 1
  elif r[-1] < 18:
   insuff += 1
  else:
   medi += 1
 tot=float(len(li)) / 100.0
 return (insuff/tot,medi/tot,bene/tot)
#-----------------------------------------------------------------------
def riarrangia(li,target):
  if len(li)==0:
   return li
  M=max_voto(li)
  m=min_voto(li)
  med=media(li)
  comment= ("*" * 60) + "\n"
  if target:
   a=(30.0-target)/(30.0-med)
   if a>1: a=1
   b=30.0  - a * 30.0
   comment +='target=%2.2f\n' % (target,)
  else:
   a=1; b=0; comment +="target= None\n"
  comment += "a,b= %2.2f, %2.2f\n" % (a,b)
  nli=[]
  for r in li:
   origr=r
   r=list(r); 
   # r[-1] = min(30, int(math.ceil(a*r[-1] +b)))
   r[-1] = ((a*r[-1] +b))
   nli.append(tuple(r))
   sys.stderr.write("%s: \t%s => %s\n" % (r[1],origr[-1],r[-1]) )
  nli.sort(compare_matr)
  if target:
   comment += ("-" * 60 ) + "\noriginal: \n"
   comment += "ins, medi, bene= %02.1f%%\t%02.1f%%\t%02.1f%%\n" % percent(li)
   comment += "min, max, media, mediana= %02.2f\t%02.2f\t%02.2f\t%2.2f\n" % ( min_voto(li),max_voto(li),media(li) ,mediana(li))
   comment += ("-" * 60 ) + "\nafter trans: \n"
   comment += "ins, medi, bene= %02.1f%%\t%02.1f%%\t%02.1f%%\n" % percent(nli)
   comment += "min, max, media, mediana= %02.2f\t%02.2f\t%02.2f\t%2.2f\n" % ( min_voto(nli),max_voto(nli),media(nli) ,mediana(nli))
   comment += ("*" * 60) + "\n"
  sys.stderr.write(comment)
  return nli

#-----------------------------------------------------------------------
def extract_target(data):
  # reg=re.compile(r"##target= *(?P<target>.+?)$", re.M)
  reg=re.compile(r"# *target *= *(?P<target>\S+)")
  if VERBOSE: 
      sys.stderr.write("DEBUG: Extracting target...")
  if reg.search(data):
    target=float(reg.search(data).group('target').strip())
    if VERBOSE: sys.stderr.write("DEBUG: `%s` found!\n" % target)
    return target
  else:
    if VERBOSE: sys.stderr.write("DEBUG: target not found!\n---\n%s\n---\n" % data)
    return None
#-----------------------------------------------------------------------
def generate_gift(data):
  esercizi=[parse_esercizio(es).gift() for es in extract_esercizi(data)]
  return "\n\n".join(esercizi)

#-----------------------------------------------------------------------
def generate_xhtml(data):
  "Generate html + wrapper (CSS+MathJax)"
  esercizi=[("<li>" + parse_esercizio(es).xhtml() + "</li>") for es in extract_esercizi(data)]
  return "<ol>" + ( "\n\n".join(esercizi)) + "</ol>"
#-----------------------------------------------------------------------
def purify(s):
 return re.sub(r"\\","",s)

def replace_url(data):
 regemph=re.compile(r"\\emph{(?P<target>.+?)}", re.M )
 if regemph.search(data):
  sys.stderr.write("emph found! %s\n"  % regemph.search(data).group('target') )
 data= regemph.sub(lambda x: """<strong>%s</strong>""" % x.group('target'), data )
 reg=re.compile(r"\\url{(?P<url>.+?)}", re.M )
 if reg.search(data):
  sys.stderr.write("url found! %s\n"  % reg.search(data).group('url') )
 return reg.sub(lambda x: """<a href="%s">%s</a>""" % (purify(x.group('url')),purify(x.group('url'))), data )
#-----------------------------------------------------------------------
def input_enc(data):
 reg=re.compile(r"\usepackage\[(?P<enc>.+?)\]{inputenc}", re.M )
 if reg.search(data):
  enc=reg.search(data).group('enc').strip()
 else:
  enc=None
 if VERBOSE: sys.stderr.write("encoding found: %s\n"  % enc )
 if enc==None:
  if VERBOSE: sys.stderr.write("  => Assuming UTF8\n")
 return enc

def convert_to_utf(data):
 sys.stderr.write("converting to UTF-8...\n"  )
 udata=unicode(data,'latin1')
 return udata.encode('utf-8')

#-----------------------------------------------------------------------
def riordina_cmp(x,y):
 if x[-1] < y[-1] :
  return 1
 elif x[-1] > y[-1] :
  return -1
 else:
  return 0
#-----------------------------------------------------------------------
def riordina(li):
 li.sort(riordina_cmp)
#-----------------------------------------------------------------------
def riordina_somme_cmp(x,y):
 sx=sum(x); sy=sum(y)
 if sx < sy:
  return 1
 elif sx > sy:
  return -1
 else:
  return 0
#-----------------------------------------------------------------------
def riordina_somme(li):
 li.sort(riordina_somme_cmp)
#-----------------------------------------------------------------------

def produce_stats(db):
 STATFILE='rispostamultipla.csv'
 xx=db[0]
 kk=xx.keys()
 kk.sort()
 res=",".join([str(k) for k in kk]+["tot."]) + "\n"
 for xx in db:
  kk=xx.keys()
  kk.sort()
  res += ",".join([str(xx[k]) for  k in kk]+[str(sum([xx[k] for k in kk])) ] )  + "\n"
 fd=file(STATFILE,'w')
 fd.write(res)
 fd.close()
 sys.stderr.write("Stats table saved in %s.\n" % STATFILE) 
 return

#-----------------------------------------------------------------------
def produce_stats_string(xx,indici):
 kk=xx.keys()
 kk.sort()
 zero=kk[0]
 lettere=kk[1:]
 res = ["[%s]" % xx[k] for k in lettere ] 
 res += [ "[$f=%0.2f\\%%$, $d=%0.2f\\%%$, non-responses: %s ]" % (indici[1]*100,indici[0]*100, xx[zero])  ] 
 return [ "\\hfill\\textbf{%s}\n" % x for x in res ]
#-----------------------------------------------------------------------
def median(data_list):
	n = len(data_list)
	# Test whether the n is odd
	if n & 1:
		index = n / 2 
		return data_list[index]
	else:
		low_index = n / 2 - 1
		high_index = n / 2
		average = (data_list[low_index] + data_list[high_index]) / 2.0
		return average


#-----------------------------------------------------------------------
def generate_stats_summary(db):
 dbs=db['__stats__']
 dbs_punti=db['__stats_punti__']
 dbt={}
 dbt['NumberOfQuestions']=len(dbs)
 dbt['NumberOfStudents']=0
 for k in dbs[0]:
  dbt['NumberOfStudents'] += dbs[0][k] 
 dbt['MeanScore']=0
 for q in range(dbt['NumberOfQuestions']): 
  for k in dbs[q].keys():
   dbt['MeanScore'] +=  dbs[q][k] * dbs_punti[q][k] 
 dbt['MeanScore'] = dbt['MeanScore'] / float(dbt['NumberOfStudents'])   
 lista_voti=sorted( [ x[2] for x in db['__stats_lista__'] ] )
 dbt['MedianScore']=median(lista_voti)
 dbt['Maximum']=lista_voti[-1]
 dbt['Minimum']=lista_voti[0]
 dbt['PossibleMaximum']=dbt['NumberOfQuestions'] * db['__punti__'][0]
 dbt['PossibleMinimum']=dbt['NumberOfQuestions'] * db['__punti__'][1]
 M=dbt['MeanScore']
 variance = sum ( (x-M)**2 for x in lista_voti ) / float(len(lista_voti) )
 dbt['StandardDeviation'] = math.sqrt(variance) 
 dbt['SuffScore'] = 0.6*dbt['PossibleMaximum']
 dbt['HalfScore'] = 0.5*dbt['PossibleMaximum']
 lista_voti_suff=[x for x in lista_voti if x >= dbt['SuffScore'] ]
 if len(lista_voti_suff) > 0:
  dbt['MeanScoreSuff'] = sum(lista_voti_suff) * 1.0 / len(lista_voti_suff) 
 else:
  dbt['MeanScoreSuff'] = 'None'
 dbt['PercOfSuff'] = len( [x for x in lista_voti if x>= dbt['SuffScore'] ] ) / float( dbt['NumberOfStudents']) * 100.0
 dbt['PercOfHalf'] = len( [x for x in lista_voti if x>= dbt['HalfScore'] ] ) / float( dbt['NumberOfStudents']) * 100.0
 dbt['ReliabilityKR20']=0
 dbt['StandardError']=0
 dbt['ReliabilityKR21']=0
 dbt['hist_bins']=(dbt['Maximum']-dbt['Minimum']) //2
 dbt['hist_data']=r"\\".join([str(x) for x in lista_voti])
 result=r"""
\renewcommand{\bubblesheet}[3][1]{}
\begin{center}
  \begin{tikzpicture}
        \begin{axis}[
	    scale only axis,
	    enlarge x limits=-1,
	    width=0.9\textwidth,
            ybar,
            %% xticklabel=
            %% \pgfmathprintnumber\tick--\pgfmathprintnumber\nexttick,
	    x tick label style={font=\small},
	    xlabel={Voti},
	    xtick=data
        ]
            \addplot+[hist={bins=%(hist_bins)i}]
            table[row sep=\\,y index=0] {
            data\\
            %(hist_data)s\\
            };
        \end{axis}
    \end{tikzpicture}
\end{center}

\begin{verbatim}
Number of Questions: %(NumberOfQuestions)s
Number of Students: %(NumberOfStudents)s
Mean Score: %(MeanScore)s
Median Score: %(MedianScore)s
Standard Deviation: %(StandardDeviation)s
Obtained Maximum: %(Maximum)s; Possible Maximum: %(PossibleMaximum)s 
Obtained Minumum: %(Minimum)s; Possible Minimum: %(PossibleMinimum)s 
Percentage with >= %(SuffScore)s:  %(PercOfSuff)5.2f%% 
Percentage with >= %(HalfScore)s:  %(PercOfHalf)5.2f%% 
Mean Score with >= %(SuffScore)s: %(MeanScoreSuff)s 
\end{verbatim}
\noindent
Item analysis: $f=$ facility index; $d=$ discrimination index. 



\hrule
\vspace{2\baselineskip}
\null
\vspace{\baselineskip}


""" % dbt
 return result 
 

#-----------------------------------------------------------------------
def generate_stats_texfile(s,db):
 dbstats=db['__stats__']
 dbindici=db['__indici__']
 header,body=make_template(s) 
 esercizi=[parse_esercizio(es) for es in extract_esercizi(s)]
 numero_esercizi=len(esercizi)
 reg=re.compile(r"%%__EXERM_REMOVED__%%",re.M)
 splitted_body=reg.split(body)
 res=header  + "\\usepackage{pgfplots, pgfplotstable}\\usepgfplotslibrary{statistics}\\pgfplotsset{compat=1.9}\\writelblfilefalse\n\\begin{document}\n"
 res += generate_stats_summary(db)
 res += splitted_body[0]
 res += "\\rhead{{\\tt [%s]-p\\thepage/\\pageref{LastPage}}}\n" % "--STATS--"
 for i in range(numero_esercizi):
    ese=esercizi[i]
    eseperm=range(ese.numero_risposte())
    res += ese.latex_withstats(produce_stats_string(dbstats[i],dbindici[i]))
    res += splitted_body[i+1]
 res += "\\cleardoublepage\n"
 res += "\\end{document}\n"
 return res  
 # return "%s, %s" % (len(data), len(db))

#-----------------------------------------------------------------------
def exit_on_error(s):
 global ISUI
 if ISUI:
  raise Exception(s)
 else:
  sys.stderr.write(s)
  sys.exit(1)
#-----------------------------------------------------------------------
# import sys
# import os
import subprocess
import glob 
import cmd
import datetime
import time

# import pickle
# 
# import rlcompleter
# import readline
# readline.parse_and_bind ("bind ^I rl_complete")
# 
# term=sys.stdout
mcqlogo=r""" mcq.py <%s>
     ==================
      |@@@@----@|@@--|           _ __ ___   ___ __ _ 
      |@@@----@@|--@@|          | '_ ` _ \ / __/ _` |
      |@@----@@@|@--@|          | | | | | | (_| (_| |
o_--_ |@@@@----@|--@@| __-.-.__ |_| |_| |_|\___\__, | - XeLaTeX __--.-_o
      |@@@@@----|@--@|                            | |
      |@----@@@@|@--@|                            |_|
     ==================
""" % MCQXELATEXURL

                     
class myTerm:
 def __init__(self,output=sys.stdout,prompt='mcq-> ',number_of_columns=NUM_OF_TERMCOLS):
  self.prompt=prompt 
  self.number_of_columns=number_of_columns
  #__HERE__ changed self.ANSIesc = '\033[1;'
  self.ANSIesc = '\033['
  #__HERE__ changed self.ANSIreset = '%sm' % self.ANSIesc
  self.ANSIreset = '%s0m' % self.ANSIesc
  self.ANSIformat = '%dm'
  self.ANSIfgoffset, self.ANSIbgoffset = 30, 40
  ANSIattrs='none bold faint italic underline blink fast reverse concealed'
  ANSIcolors='grey red green yellow blue magenta cyan white'
  self.ANSIattrs=dict((s,i) for i,s in enumerate(ANSIattrs.split()))
  self.ANSIcolors=dict((s,i) for i,s in enumerate(ANSIcolors.split()))
  self.beep="\a"
  self.output=output 
  self.platform=None
  self.has_history=False
  self.req_db={}
  if sys.platform.startswith('darwin'):
   import readline 
   import rlcompleter
   if 'libedit' in readline.__doc__:
    readline.parse_and_bind ("bind ^I rl_complete")
   else:
    readline.parse_and_bind ("tab: complete")
   self.platform="mac"
   self.has_history=True
  elif sys.platform.startswith('cygwin'):
   import readline 
   import rlcompleter
   if 'libedit' in readline.__doc__:
    readline.parse_and_bind ("bind ^I rl_complete")
   else:
    readline.parse_and_bind ("tab: complete")
   readline.set_completer_delims(' \t\n`~!#$%^&*()[{]}\\|;\'",<>?')
   self.has_history=True
   self.platform="cygwin"
  elif os.name == 'nt':
   try:
    import pyreadline
   except:
    self.msg("Try to install `pyreadline`!\nOtherwise you will not have TAB-completion support!")
    s=raw_input('Press <Return> to continue...')
   import rlcompleter
   self.platform="win"
  elif os.name == 'posix':
   import readline 
   import rlcompleter
   if 'libedit' in readline.__doc__:
    readline.parse_and_bind ("bind ^I rl_complete")
   else:
    readline.parse_and_bind ("tab: complete")
   readline.set_completer_delims(' \t\n`~!#$%^&*()[{]}\\|;\'",<>?')
   self.has_history=True
   self.platform="linux"  
  if self.platform in ['linux','mac','cygwin']: 
   # readline.parse_and_bind ('"\e[A": history-search-backward')
   # readline.parse_and_bind ('"\e[B": history-search-forward')
   # it does not work on mac... but just try...
   if os.path.exists(os.path.expanduser("~/.inputrc")) :
    readline.read_init_file(os.path.expanduser("~/.inputrc"))
   try:
    t_rows, t_columns = subprocess.check_output(['stty', 'size']).split()
    self.number_of_columns=int(t_columns)
   except: 
    pass
  self.home=os.path.expanduser("~")
  self.persistdb_path=os.path.join(self.home,'.mcqdb.pkl')
  self.histfile=os.path.join(self.home,'.mcq_history')
  self.logfile=os.path.join(self.home,'.mcq_log')
  self.lockfile=os.path.join(self.home,'.mcq_lock') 
  self.logfile_fd=file(self.logfile,'a')
  # 
  import atexit
  atexit.register(self.del_lockfile)
  if self.isfile_lockfile():
    sys.stdout.write("""****************************************************
***             WARNING !!!!!!!!!        ***********
****************************************************
***    ANOTHER MCQ.PY seems running      ***********
****************************************************
!!!!!!!!!! DANGER !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
=> If you continue, you will risk losing all your work! 
""")
    s=raw_input('Press <Return> to continue...')
    self.lockfile=os.path.join(self.home,'.mcq_lock_danger') 
  else:
    self.touch_lockfile()
  
  # now try to set the history readline mechanism.
  if self.has_history:
   try: 
    readline.set_history_length(MAX_HISTORY_LENGTH)
    readline.read_history_file(self.histfile)
   except IOError:
    pass
   import atexit 
   atexit.register(readline.write_history_file,self.histfile)
  try:
   import getpass
   self.username=getpass.getuser().capitalize()
  except:
   self.username='User'
  self.check_requirements()
 def termcmd(self,arg=None, sep=' ', end='\n'):
  # better: check from os.environi.get('TERM') variable in 
  # term_with_colors = ['xterm', 'xterm-color', 'xterm-256color', 'linux', 'screen', 'screen-256color', 'screen-bce'] 
  # added 2018-12-01 to fix a strange macosx behaviour.
  if not self.platform or self.platform=='win' or os.getenv('ANSI_COLORS_DISABLED'):
   return ""
  # cmd = [self.ANSIreset, self.ANSIformat % self.ANSIattrs['bold'] ]
  cmd = [self.ANSIreset]
  if arg:
        arglist=arg.split(sep)
        for offset in (self.ANSIfgoffset, self.ANSIbgoffset):
            if arglist and arglist[0] in self.ANSIcolors:
                cmd.append(self.ANSIformat % (self.ANSIcolors[arglist.pop(0)]+offset))
        for a in arglist:
            if a in self.ANSIattrs:
             c=self.ANSIformat % self.ANSIattrs[a]
            else:
             c=None
            if c and c not in cmd:
                cmd.append(c)
  return self.ANSIesc.join(cmd)
 def boxed_message(self, msg):
  l=self.number_of_columns
  U_UL=u"\u250f"
  U_UR=u"\u2513"
  U_LL=u"\u2517"
  U_LR=u"\u251b"
  U_HLINE=u"\u2501"
  U_VLINE=u"\u2503"
  if self.platform=='unknown' or os.getenv('ANSI_COLORS_DISABLED') or self.platform=='win':
   U_UL="+"; U_UR="+"; U_LL="+"; U_LR="+"
   U_HLINE="-"; U_VLINE="|"
  res= U_UL + U_HLINE * (l-2) + U_UR + "\n" 
  for x in msg.splitlines():
   x=x[:l-3]
   res += U_VLINE + " " + x +  (" " *(l - len(x) -3 )) +  U_VLINE + "\n"
  res += U_LL + U_HLINE * (l-2) + U_LR +"\n"
  return res 
 def say(self,msg):
  import tempfile
  fdtmp,tmpfile=tempfile.mkstemp(suffix="txt")
  fd=open(tmpfile,'w')
  fd.write(msg)
  fd.close()
  if self.platform=='mac':
   os.system("say -v Vicki -f %s  & " % (tmpfile,) )
  # on linux ? 
 def write(self,msg):
  self.output.write(msg.encode('utf-8'))
 def msg(self,msg):
  for x in msg.splitlines():
   self.output.write(self.termcmd('yellow black bold')+": "+ x +self.termcmd()+"\n")
 def error(self,msg):
  self.output.write((self.beep*3)+self.termcmd('yellow red bold')+"!!"+ msg+self.termcmd()+"\n")
  try:
   self.output.flush()
  except:
   pass
 def input(self):
  s=raw_input(self.prompt)
  return s
 def open(self,filepath):
  self.msg("Trying to open file `%s` on %s..." % (filepath,self.platform) )
  if self.platform=='mac':
   return subprocess.call(('open', filepath))
  elif self.platform=='win':
   return os.startfile(filepath)
  elif self.platform=='linux':
   return subprocess.call(('xdg-open', filepath))
  elif self.platform=='cygwin':
   return subprocess.call(('cygstart', filepath))
  else:
   self.error("Unknown platform %s. Please manually open file: %s" % (self.platform,filepath))
   return -1
 def read_persistdb(self):
  persistdb_path=self.persistdb_path 
  result = {'recentfiles':[], 'activefile':None}
  if os.path.exists(persistdb_path):
   try:
    fd=open(persistdb_path,'rb')
    result = pickle.load(fd)
    fd.close()
   except Exception , v:
    sys.stderr.write("Something wrong with pickle db %s (error %s)\n" % (persistdb_path,v))
  return result
 def write_persistdb(self,db):
  persistdb_path=self.persistdb_path 
  fd=open(persistdb_path,'wb')
  pickle.dump(db,fd)
  fd.close()
 def get_requirements(self):
  result=""
  if self.platform=="win" or sys.version_info<(2,7):
   return result
  if not self.req_db.get('xelatex'):
   result += "WARNING: missing `xelatex` executable. Please install it first\n"
  if not self.req_db.get('has_mcq'):
   result += "WARNING: missing `mcq.sty`. Please install it first.\n"
  if not self.req_db.get('has_linuxlibertinettf'):
   result += "WARNING: missing `Linux Libertine` TTF font. Please install it first.\n"
  return result 
 def check_requirements(self):
  if self.platform=="win" or sys.version_info < (2,7):
   return 
  if VERBOSE: self.msg("Checking requirements:")
  check_commands =[ ['kpsewhich','--version'] , ['xelatex','--version'], ['gs','--version'], ['fc-list','--version'],['pdfimages','-v'] ]
  check_output_list= [ ['has_mcq','kpsewhich', 'mcq.sty'] ,['has_linuxlibertinettf','fc-list',":fullname=\"Linux Libertine\""]]
  for p in check_commands:
   if VERBOSE: self.write(" * %s...   " % p[0])
   try:
    o=subprocess.check_output(p) 
    if VERBOSE: self.write(self.termcmd("green black") + "[OK]\n" + self.termcmd() )
    self.req_db[p[0]]=True
   except Exception , v:
    if VERBOSE: self.write(self.termcmd("red") + "[FAIL]\n" + self.termcmd() ) 
    if VERBOSE: self.error("ERROR: %s" % v)
    self.req_db[p[0]]=False
  for p in check_output_list:
   if VERBOSE: self.write(" ** %s ... " % p[0] )
   try:
    o=subprocess.check_output(" ".join(p[1:]),shell=True) 
    if len(o)>2:
     if VERBOSE: self.write(self.termcmd("green black") + "[OK]\n" + self.termcmd() )
     if VERBOSE: self.write("( %s )\n" % o.strip())
     self.req_db[p[0]]=True
    else:
     if VERBOSE: self.write(self.termcmd("red") + "[FAIL]\n" + self.termcmd() ) 
     self.req_db[p[0]]=False
   except Exception , v:
    if VERBOSE: self.write(self.termcmd("red") + "[FAIL]\n" + self.termcmd() ) 
    if VERBOSE: self.error("ERROR: %s" % v)
    self.req_db[p[0]]=False
  if self.platform=="mac" :
   try:
    import Cocoa
    manager = Cocoa.NSFontManager.sharedFontManager()
    font_families = list(manager.availableFontFamilies())
    if "Linux Libertine" in font_families:
     if VERBOSE: self.write(self.termcmd("green black") + "[OK - Confirmed]\n" + self.termcmd() )
     self.req_db['has_linuxlibertinettf']=True
    else:
     if VERBOSE: self.write(self.termcmd("red") + "[NO]\n" + self.termcmd() )
     self.req_db['has_linuxlibertinettf']=False
   except Exception, v:
    if VERBOSE: self.write(self.termcmd("red") + "[FAIL]\n" + self.termcmd() ) 
    if VERBOSE: self.error("ERROR: %s" % v)
  if VERBOSE: self.write("DONE!\n\n")
 def touch_lockfile(self):
  fd=file(self.lockfile,'w')
  fd.write(".")
  fd.close() 
  return 
 def isfile_lockfile(self):
  return os.path.isfile(self.lockfile)
 def del_lockfile(self):
  try:
    os.remove(self.lockfile)
  except Exception, v:
    sys.stderr.write("WARNING: lock file %s is missing.\nThis is bad.\n" % self.lockfile) 


class ExamFile:
 def __init__(self,abspath):
  global DB_STATS_FILE, DB_FILE, SOLUTIONS_FILE
  self.dir,self.filename=os.path.split(abspath)
  self.basename ,_ = os.path.splitext(self.filename)
  self.abspath=abspath
  self.pdffile=self.basename+'.pdf'
  self.xmlfile=self.basename+'.xml'
  self.uidfile=self.basename+'.uid'
  self.exam_db=self.basename+'_exam.db'
  self.exam_csv=self.basename+'_exam.csv'
  self.exam_pub=self.basename+'_exam.txt'
  self.exam_tex=self.basename+'_exam.tex'
  self.exam_pdf=self.basename+'_exam.pdf'
  self.exam_sols=self.basename+'_exam.sols'
  self.exam_stats_db=self.basename+'_exam_stats.db' 
  self.exam_stats_tex=self.basename+'_stats.tex'
  self.exam_stats_pdf=self.basename+'_stats.pdf'
  self.answers=self.basename+'_answers.txt'
  self.omr_output=self.basename+'_answers.pdf'
  self.data=''
  self.refresh()
  self.status={}
 def refresh(self):
  data=file(self.abspath).read()
  if input_enc(data) == 'latin1':
   data=convert_to_utf(data)
  self.data=strip_latex_comments(data)
 def get_n(self):
  reg=re.compile(r"\\setcodice{(?P<p>.+?)}", re.M)
  if os.path.exists(self.exam_tex):
   examdata=file(self.exam_tex).read()
   return len(reg.findall(examdata) )
  else:
   return None
 def check_time(self,f):
  if os.path.exists(os.path.join(self.dir,f)):
   return datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(self.dir,f)))
  else:
   return None
 def check_time_str(self,f):
  t=self.check_time(f)
  if t:
   return t.strftime(DATETIME_FORMAT)
  else:
   return "Never"
 def number_of_lines(self,f):
  target=os.path.join(self.dir,f)
  if os.path.exists(target) and os.path.isfile(target):
   return len([x for x in file(f,'r').read().splitlines() if len(x)>2 and not x.startswith('#')])
  else:
   return None
 def show_status(self):
  'Check the poset of dependencies'
  file_content=self.data
  esercizi=[parse_esercizio(es) for es in extract_esercizi(file_content)]
  numero_esercizi=len(esercizi)
  numero_maxrisposte=0
  for ese in esercizi:
   if ese.numero_risposte()>numero_maxrisposte:
    numero_maxrisposte=ese.numero_risposte()
  headline=extract_headline(file_content)
  workdir,filename = self.dir, self.filename
  dbstrings={ 
  'filename' : self.filename,
  'dir' : self.dir,
  'headline' : headline, 
  'last_xelatexed': self.check_time_str(self.pdffile),
  'last_edited' : self.check_time_str(self.filename),
  'number_of_exer': numero_esercizi,
  'number_of_answers': numero_maxrisposte,
  'exam_pdf_time' : self.check_time_str(self.exam_pdf),
  'exam_pdf' : self.exam_pdf,
  'n' : self.get_n(),
  'exam_csv' : self.check_time_str(self.exam_csv),
  'answers' : self.answers,
  'answers_time' : self.check_time_str(self.answers),
  'answers_n': self.number_of_lines(self.answers) or 'No',
  'uidfile': self.uidfile,
  'uidfile_n': self.number_of_lines(self.uidfile) or 'No',
  'uidfile_time': self.check_time_str(self.uidfile),
  'results_csv': self.exam_csv,
  'results_csv_time': self.check_time_str(self.exam_csv),
  'results_csv_n': self.number_of_lines(self.exam_csv) or 'No',
  'stats' : self.exam_stats_pdf,
  'stats_time' : self.check_time_str(self.exam_stats_pdf)
  }
  slist= [ (">Main File: `%(filename)s` [%(headline)s]", ""), 
("Number of exercises: %(number_of_exer)i --  Number of (max) answers: %(number_of_answers)i", ""), 
("Last edited on: ","%(last_edited)s"),
("Last XeLaTeX'ed on: ", "%(last_xelatexed)s" ),
("Generated %(n)s permuted copies in `%(exam_pdf)s`:","%(exam_pdf_time)s"),
("Answers file `%(answers)s` (%(answers_n)s lines):","%(answers_time)s"),
("UIDs file `%(uidfile)s` (%(uidfile_n)s lines):", "%(uidfile_time)s"),
("Results CSV file `%(results_csv)s`(%(results_csv_n)s lines):","%(results_csv_time)s"),
("STATS file `%(stats)s`:","%(stats_time)s")
]
  result=""
  ncols=NUM_OF_TERMCOLS # TODO: get it form the terminal 
  for pre,post in slist:
   spre=pre % dbstrings; spost = post % dbstrings
   result += spre + (" "*( ncols -3  - len(spre) - len(spost))) + spost + "\n"
  return result
 def view(self,arg):
  'View status, log, ...'
  pass
 def multiple_answersfile(self):
  bn,_=os.path.splitext(self.answers)
  extra_answers=glob.glob(bn+"_*.txt")
  return extra_answers
 def check_progress(self,cmdname):
  if cmdname=='exam':
   if not os.path.exists(self.pdffile):
    sys.stderr.write("**ERROR**: PDF file `%s` does not exist!\nCompile the main file `%s` typing `make` first...\n" % (self.pdffile, self.filename))
    return -1
   if self.check_time(self.filename) > self.check_time(self.pdffile):
    sys.stderr.write("**ERROR**: the main TeX file `%s` is newer than its PDF output `%s`!\nType `make` first!\n" % (self.filename,self.pdffile) )
    return -1
   for f in [self.basename + ".lbl", self.basename+".pos"]:
    if not os.path.exists(f):
     sys.stderr.write("**FATAL, RARE AND UNRECOVERABLE ERROR**: internal file `%s` missing!\nTry to ask help!\n" % f )  
     return -1
   return 
  elif cmdname == 'omr':
   if self.check_progress('exam'):
    return -1
   if not os.path.exists(self.xmlfile):
    sys.stderr.write("**ERROR**: necessary XML file `%s` does not exist!\nRe-run `exam` first... or check logs\n" % (self.xmlfile, ))
    return -1
   if self.check_time(self.xmlfile) < self.check_time(self.pdffile):
    sys.stderr.write("**ERROR**: the PDF file `%s` is newer than the XML file `%s`!\nRe-run `exam` first or check logs...\n" % (self.pdffile,self.xmlfile) )
    return -1 
   if not os.path.exists(self.exam_db):
    sys.stderr.write("**ERROR**: necessary internal file `%s` does not exist!\nRe-run `exam` first or check logs...\n" % (self.exam_db, ))
    return -1
   return  

###############################################################################
def has_BW_image(pdf_path):
    # do this first! pdf_images_check()
    # according to manual:
    #gray - Gray
    #rgb - RGB
    #cmyk - CMYK
    #lab - L*a*b
    #icc - ICC Based
    #index - Indexed Color
    #sep - Separation
    #devn - DeviceN
    cmd = ['pdfimages', '-list', pdf_path]
    sys.stderr.write('Extracting images info from file %s...\n' % (pdf_path,) )
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = [] 
    output,error=proc.communicate()
    if proc.returncode: 
      raise Exception("pdfimages ERROR with command %s %s!\n%s" % (cmd,pdf_path, error))
    # for image in proc.stdout.readlines()[2:]:
    for image in output.splitlines()[2:]:
      img_page, img_num, img_type, img_width, img_height, img_color, img_comp, img_bpc, img_enc, img_interp, img_object, img_ID, x_ppi, y_ppi, img_size, img_ratio = image.split()
      if VERBOSE: sys.stderr.write("Image %s (%sx%s %s) found! Color=%s with bits=%s\n" % ( img_num, img_width,img_height, img_enc, img_color,img_bpc ))
      result += [img_color=='gray' and int(img_bpc)==1]
    return  True in result
###############################################################################

class uiShell(cmd.Cmd):
 def __init__(self,name,term=None): 
  cmd.Cmd.__init__(self,completekey='Tab')
  # term=myTerm(output=sys.stdout) 
  self.term=term
  self.name=name
  self.intro = 'Type help or ? to list all commands.\n'
  self.use_rawinput=True
  self.doc_header = 'Main Commands (type `help` or `? <topic>`):'
  self.ruler='~'
  self.lsfiles=[]
  self.lsdir=[]
  self.updateprompt()
 def emptyline(self):
  # self.do_help('')
  sys.stdout.write(self.intro)
 def do_shell(self,args):
  'Shell (direct) commands'
  os.system(args)
 def do_open(self,args):
  """USAGE: open <file>
	Open PDF/TXT/CVS/... file with the appropriate program
	(according to system configuration / mime-types / OS... )
	EXAMPLES:
	 open main_answers.pdf
	 open main_answers.txt"""
  try:
   if self.term.open(args):
    self.term.error("ERROR: `open %s` did not work...\nCheck your input." % args)
  except:
   self.term.error("I could not open file `%s`...\nCheck your input." % args)
 def precmd(self,line):
  if not line:
   return line
  # sys.stderr.write("DEBUG: executing `%s`...\n" % line )
  now=time.strftime(DATETIME_FORMAT)
  af=persistdb['activefile'] or '---'
  self.term.logfile_fd.write("%s [%s] : `%s`\n" %(now,af,line ) )
  return line
 def updateprompt(self):
  number_of_columns=self.term.number_of_columns
  remaining_chars=number_of_columns - len( "(%s)mcq[]->> " % self.name ) - 49
  localdir=os.getcwd()
  if len(localdir) > remaining_chars:
      localdir="..."+localdir[-remaining_chars:]  
  self.prompt=self.term.termcmd("green black bold") + "(%s)mcq[%s]->> " % (self.name,localdir) + self.term.termcmd() 
  self.lsdir,self.lsfiles=self.thisdir_ls('')
 def do_EOF(self,args):
  'EndOfFile'
  # self.term.msg("Quitting from %s..." % self.name )
  return self.do_q(args)
 def do_x(self,args):
  'Exit'
  self.term.msg("Exiting from %s..." % self.name )
  return -1
 def help_help(self):
  'help'
  pass
 def get_names(self):
  #sys.stderr.write("%s" % [x for x in dir(self.__class__) if x != 'do_EOF'])
  return [x for x in dir(self.__class__) if x != 'do_EOF']
 def do_q(self,args):
  'Quit'
  self.term.msg("Quitting from %s..." % self.name )
  self.term.write_persistdb(persistdb)
  sys.exit(0)
 def completedefault(self,text, line, begidx, endidx):
  #sys.stderr.write("\ncompetedefault called: text=`%s`, line=`%s`, begidx=`%s`, endidx=`%s`\n" % (text,line,begidx,endidx) )
  # text=''
  # for c in line[::-1]:
  # if c!=" ":
  #  text = c + text
  # else:
  #  break
  #sys.stderr.write("\nnew text=`%s`, line=`%s`, begidx=`%s`, endidx=`%s`\n" % (text,line,begidx,endidx) )
  targetdir,rest=os.path.split(text)
  lsdir,lsfiles=self.thisdir_ls(targetdir)
  longlist=[os.path.join(targetdir,i) for i in lsdir+lsfiles]
  return [i for i in longlist if i.startswith(text)]
  # return [i for i in self.lsdir+self.lsfiles if i.startswith(text)]
 def thisdir_ls(self,args,filtered=None):
  # sys.stderr.write("\nthisdir_ls args=%s\n" % args)
  thisdir=os.getcwd()
  if args:
   target=os.path.join(thisdir,args)
  else:
   target=thisdir
  if not os.path.exists(target):
   self.term.error("Error: Path `%s` does not exist!" % args)
   return ([],[])
  if not os.path.isdir(target):
   return ([],[target])
  result_dir=[ (f+"/") for f in os.listdir(target) if os.path.isdir(os.path.join(target,f)) and f[0]!="." ]
  result_dir.sort()
  result_dir = ['..'] + result_dir
  result_files=[f for f in os.listdir(target) if os.path.isfile(os.path.join(target,f)) and ( not filtered or f[-len(filtered):].lower() == filtered )]
  result_files.sort()
  return (result_dir , result_files)

uiFileNavigator_firstinfo="""Welcome. This is the MCQ-XeLaTeX File Navigator.
You can use the commands listed below to navigate in the filesystem,
and to load the MCQ-XeLaTeX main TeX file you want to use for the exam. 
If your Operative System is not too primitive, you can tab-complete commands
and arguments of commands. In the prompt you will see the current directory. 

Arguments of commands will be denoted by <argument>. 
Optional arguments will be denoted by [<argument>].

Main Commands (type `? <command>` for help):
load <file>      : Load main XeLaTeX file <file> 
cd [<directory>] : Change directory ( cd .. for parent directory )
ls [<dir>]       : Show content of <dir> (or current dir if <dir> is empty)
q                : Quit 
"""
class uiFileNavigator(uiShell):
 global persistdb
 def __init__(self,term=None): 
  uiShell.__init__(self,'File',term=term)
  self.lsdir,self.lsfiles=self.thisdir_ls('')
 def do_ls(self,args):
  """USAGE: ls [<path>]
	Return the list of .TeX files or directories containing TeX files
	or directories. If the optional argument <path> is missing, 
	the current dir will be listed.
	If <path> is a directory, its content will be listed.
	If <path> is a file, just this file will be listed."""
  dirs,files=self.thisdir_ls(args,filtered=".tex")
  if dirs or files:
       self.term.write("\n".join(dirs) + "\n " + "\n ".join(files) + "\n")
 def do_cd(self,arg):
  """USAGE: cd [<dir>]
	Change working directory to directory <arg>. With no <dir> argument,
	it will go to the Home Directory."""
  if arg.strip() == '':
   arg=os.path.expanduser('~')
  if os.path.exists(arg) and  os.path.isdir(arg):
   try:
    os.chdir(arg)
   except Exception , v:
    self.term.error("Error: %s" % v)
   self.lsdir,self.lsfiles=self.thisdir_ls('')
  else:
    self.term.error("Error: `%s` is not a directory!" % arg)
  self.updateprompt()
 # def completedefault(self,text, line, begidx, endidx):
 #  return [i for i in self.lsdir+self.lsfiles if i.startswith(text)]
 def do_load(self,args):
  """USAGE: load <mainfile>
	This commands simply loads the MCQ-XeLaTeX file <mainfile>. 
	Use ls, cd and tab-completion to locate the file, first.
	EQUIVALENT EXAMPLES:
	  load main.tex
	  load main
	  load mai<TAB>"""
  # TODO: properly load classes to parse the file 
  if args.strip() == '':
   self.term.error("ERROR: missing argument of `load`\nType `? load` for help.")
   return 
  bn,ext=os.path.splitext(args)
  if ext=='':
   args=bn + '.tex'
   ext='.tex'
  if os.path.exists(args) and os.path.isfile(args) and ext.lower()=='.tex':
   persistdb['activefile']  = os.path.abspath(args)
   self.term.msg('File %s loaded: back to main menu.' % args)
   return -1
  else:
   self.term.error('Error: `%s` is not a TeX file!' % args)
   return 


uiMasterFile_firstinfo=""" Main Commands (type `? <command>` for help):
status                 : show MCQ-XeLaTex status
make                   : compile the main TeX file <main>.tex (with XeLaTeX)
exam <n>               : gen <n> exam permuted copies -> *_exam.{tex,pdf}
omr <scanfiles*.pdf>   : get the OMR  answers file `<main>_answers.txt`
open <file>            : open and view/edit <file> with appropriate program
uid [<file>][:<specs>] : align UIDs with names, following specs  (in-place)
mark [<file>]          : evaluate and mark, using answers file (default given)
makestats              : generate a STATS file <main>_stats.pdf
export <filename.gift> : export to filename.gift, in GIFT moodle format
export <filename.html> : export to filename.html, in HTML format 
! <shell commands>     : execute directly shell commands
x                      : clear the status and go to main menu
q                      : quit (without clearing the status)
"""
class uiMasterFile(uiShell):
 global persistdb, MCQRANDOMSEED
 def __init__(self,term=None): 
  uiShell.__init__(self,'Work',term=term)
  self.EF=ExamFile(persistdb['activefile'])
 def do_x(self,args):
  """USAGE: x
	Clear the status and go to main menu. 
	Use with caution: you need to re-load a main MCQ-XeLaTeX file after."""
  persistdb['activefile']=None
  self.term.msg("Exiting from %s..." % self.name )
  return -1
 def do_q(self,args):
  'Quit, saving the status.'
  self.term.msg("Quitting from MCQ-XeLaTeX %s..." % self.name )
  self.term.write_persistdb(persistdb)
  sys.exit(0)
 def do_status(self,args):
  'Show the status of the job.'
  self.EF.refresh()
  self.term.write(self.term.boxed_message(self.EF.show_status()))
  self.term.write("LOG file : %s\n" % self.term.logfile )
  tempvar=self.EF.multiple_answersfile()
  if tempvar:
   self.term.error("WARNING: Multiple answers files: %s\nPlease MERGE them to `%s` or MOVE them!" % ([self.EF.answers] + tempvar,self.EF.answers) )
 def do_make(self,args):
  """USAGE: make
	Compile (XeLaTeX-ing) the TeX file <main>.tex, and generates some
	internal files necessary for the OMR scan. 
	OUTPUT: <main>.pdf
	INTERNAL: <main>.lbl, <main>.pos"""
  for i in range(2):
   retval = os.system("xelatex %s" % self.EF.filename)
   if retval:
    self.term.error("Error: compilation FAILED!\nCheck logs, edit `%s` and re-run xelatex." % self.EF.filename)
    return 2
  self.term.msg("Compilation seems OK. Check `%s` please." % self.EF.pdffile )
  return 
 def do_export(self,args):
  """USAGE: export <outputfile>
	It exports all the questions in the main TeX to <outputfile>, 
	in a format depending on the <outputfile> extension.
	If the extension is `.gift`, the format is MOODLE GIFT. 
	If the extension is `.html` or `.htm`, the format is HTML.
	EXAMPLES:
	  export file.gift
	  export file.html"""
  args=args.strip()
  bn,ext=os.path.splitext(args)
  self.EF.refresh()
  file_content=self.EF.data
  headline=extract_headline(file_content)
  if ext.lower()=='.gift':
   output=generate_gift(self.EF.data)
   fd=open(args,'w')
   fd.write(output)
   fd.close()
   self.term.msg("File %s written" % args)
  elif ext.lower() == '.html' or ext.lower() == '.htm':
   output=generate_xhtml(self.EF.data)
   fd=open(args,'w')
   dbvars={'title':headline,'mcqxelatexurl':MCQXELATEXURL,"today" : time.strftime(DATETIME_FORMAT)}
   html_page=(( generate_html_header % dbvars ) +output + (generate_html_footer % dbvars))
   fd.write(unicode(html_page,'utf-8').encode('utf-8')) # __HERE__ 
   fd.close()
   self.term.msg("File %s written" % args)
  return 
 def do_exam_nolatex(self,args):
     ## 2018-11-20 added this to meddle with marks. 
     """UNDOCUMENTED (DANGEROUS) FUNCTION: USAGE exam_nolatex <n>"""
     args=args.strip()
     if not args or not args.isdigit() or not int(args)>0 :
       return self.do_help('exam_nolatex')
     self.do_exam(args,DOLATEX=False)
     return 
 def do_exam(self,args,DOLATEX=True):
  """USAGE: exam <n>
	Generate <n> exam copies of <main>.tex, permuting the questions
	and the anwsers if <n> is at least 2. It will save the output in 
	file <main>_exam.tex and then compile it to obtain <main>_exam.pdf, 
	where <main>.tex is the name of the main TeX file. 
	If <n>=1, then it will not permute questions and answers.
	If <n> >= 2, the permutations will be pseudo-random, with a constant
	seed, so that each run will give exactly the same permutations.
	So, if a mistake in <main>.tex needs to be fixed, it is possible
	to re-generate the answer keys by XeLaTeX-ing <main>.tex and 
	re-running `exam <n>` as many times necessary.
	OUTPUT: <main>_exam.pdf
	INTERNAL: <main>_exam.tex, <main>.xml, <main>_exam.db
	HUMAN-READABLE DEBUG: <main>_exam.sols"""
  global SOLUTIONS_FILE, DB_FILE, DB_STATS_FILE, RG,RGC
  self.EF.refresh()
  args=args.strip()
  if not args or not args.isdigit() or not int(args)>0 :
   return self.do_help('exam')
  if self.EF.check_progress('exam'):
   sys.stderr.write("**ABORTING exam**...\n")
   return 
  # 
  if self.do_make(''):
    return 
  # first, initialize the random generators
  RG=random.Random(MCQRANDOMSEED)
  RGC=random.Random(MCQRANDOMSEED)
  random.seed(MCQRANDOMSEED) 
  SOLUTIONS_FILE=file(self.EF.exam_sols,'w')
  DB_FILE=file(self.EF.exam_db,'wb')
  DB_STATS_FILE=file(self.EF.exam_stats_db,'wb')
  output=file(self.EF.exam_tex,'w')
  NUMBER_OF_COPIES=int(args.strip())
  try:
   output.write(generate_copies(self.EF.data,NUMBER_OF_COPIES))
   output.close()
  except:
   self.term.error("ERROR: Failed exam... check logs above and fix-it!")
   return 
  for i in range(2):
   if DOLATEX:   
     retval = os.system("xelatex %s" % self.EF.exam_tex)
   else:  
     retval = os.system("touch %s" % self.EF.exam_pdf)
   if retval:
    self.term.error("Error: XeLaTeX compilation FAILED. Check logs, edit `%s` and re-run xelatex and exam." % self.EF.filename)
    return 
  self.term.msg("DEBUG: human readable keys file: %s" % (self.EF.exam_sols,))
  # generate xml 
  try:
   lbldb=getdb_labels(self.EF.basename)
   db2xml(lbldb,self.EF.xmlfile)
   self.term.msg("DEBUG: XML Output written to file: %s" % (self.EF.xmlfile,))
  except:
   self.term.error("XML Output failed for file: %s\n => try `xelatex` first..." % (self.EF.xmlfile,))
  if os.path.exists(self.EF.exam_pdf):  
   if self.EF.check_time(self.EF.exam_pdf) > self.EF.check_time(self.EF.pdffile) :
    self.term.msg("PDF output seems OK. Check and review `%s` please." % self.EF.exam_pdf)
   else:
    self.term.error("PDF output `%s` failed: there is a newer `%s`... re-run make before running exam please..." % (self.EF.exam_pdf, self.pdffile) ) 
  else:
   self.term.error("PDF output `%s` failed. The file does not exist..." % self.EF.exam_pdf)
  return 
 def do_omr(self,args):
  """USAGE: omr <scanfiles*.pdf>
	Parses the scanned bubblesheets in <scanfiles*.pdf>, and saves
	the list of answers in <main>_answers.txt.
	The argument is a list of PDF files (wildcard `*` is accepted).
	EXAMPLES:
	  omr scan/c1-s1.pdf scan/c1-s2.pdf scan/c2-s1.pdf 
	  omr scan/c1-*.pdf scan/c2-S*.pdf
	The annotated PDF file `<main>_answers.pdf` is created. It is possible
	to visually check the errors in the Optical Marks Recognition, 
	and (more likely) the mistakes of the humans on the bubblesheets. 
	 A RED circle means it is an out-of place mark,
	 a YELLOW circle means it is a (probably) ignorable out-of-place mark,
	 a GREEN circle means the mark was identified correctly. 
	The OMR is based on a client-server model, therefore it is necessary
	to be connected to internet, and to wait some time. 
	If running multiple times on different PDF sets, the different
	answers files can be simply manually merged.

	The format of the output, written in <main>_answers.txt
	is the format required by the subsequent `mark` process: 
 	 <CODE>:<NAME>:<UID>:<ANSWERS>:<OPTIONAL_MARK>
	with empty column name and empty <OPTIONAL_MARK>
	The strings <ANSWERS> is a string of length = number of questions,
	with a `0` for a missed answer,
	one of ABCD... for a given answer, 
	and a `*` for a multiple answer found. 
	One needs to manually check `<main>_answers.pdf` to possibly correct
	the output `<main>_answers.txt`.
        
        WARNING: Please scan the bubblesheets in GRAYSCALE format, not BW, 
                 to minimize OMR errors. 
	OUTPUT: <main>_answers.txt  <main>_answers.pdf""" 
  args=args.strip()
  glob_args=[]
  for a in args.split():
   glob_args += glob.glob(a)
  if len(glob_args)==0:
   if args!='':
    self.term.error("Error: argument `%s` is not a files list!" % args)
   return self.do_help('omr')
  if self.EF.check_progress('omr'):
   sys.stderr.write("**ABORTING OMR**...\n")
   return 
  fd,is_multiple=self.get_answers_fd()
  bn,_=os.path.splitext(fd.name)
  omr_output=bn+'.pdf'
  # check that file is not BW... 
  if VERBOSE: sys.stderr.write("Scanned images sanity check...\n")
  if self.term.req_db.get('pdfimages'):
    for pdf_file in glob_args:
      try:
        if has_BW_image(pdf_file):
          # confirm 
          self.term.error("WARNING!! Some scanned images are MONOCHROME! OMR results can be terribly wrong!\n") 
          _=raw_input('Press <Return> to continue...')
      except Exception, v:
        self.term.error("%s" % v )
  else:
    self.term.msg("No `pdfimages` found. Try to install it next time (in poppler-tools)") 
  try:
    result=ssclient(self.EF.basename,glob_args,outputfile=omr_output)
  except Exception ,v:
    self.term.error("OMR failed with error message:%s\nCannot contact OMARSERVICE %s\nPlease refer to some network guru for help.\n" % (v,OMARSERVICE))
    fd.close()
    return 
  fd.write(result)
  fd.close()
  self.term.msg("PDF annotated file `%s` created!" % omr_output)
  self.term.msg("Answers file `%s` created!\n  Please review it and compare the markings in `%s`" % (fd.name,omr_output))
  if is_multiple:
   self.term.msg("Warning: there are multiple answers files!\n  Please check the above logs, then merge all of the files into `%s`" % (self.EF.answers,) )
  # self.term.msg("Answers file `%s` created!" % self.EF.answers)
  return 
 def get_answers_fd(self):
  if not os.path.exists(self.EF.answers):
   return (file(self.EF.answers,'w') ,  False)
  else:
   thisfile=self.EF.answers
   bn,_=os.path.splitext(thisfile)
   i=0
   while os.path.exists(thisfile):
    i += 1
    newfile= (bn+"_%02i.txt"% i)
    self.term.msg("Warning: file `%s` already exists...\n  I will try to to save the output to `%s` instead.\n  Please check, then merge it with `%s`" % (thisfile,newfile,self.EF.answers) )
    thisfile=newfile     
   return (file(thisfile,'w'), True)
 def do_uid(self,args):
  r"""USAGE: uid [<UIDfile>][:<UIDcol><delim><NAMEcol>]
	Add Names to the answers list <main>_answers.txt, from a <UIDfile>.
	The file <UIDfile> is a CSV file, with delimiter <delim> 
	(default is `:`)
	EXAMPLES OF DEFAULT LINES:
	  :Verdi, Giuseppe:762809:
	  1F5G:Peano, Giuseppe:012345:
	After the optional argument <UIDfile> there is an optional
	specification of which columns contain the UID and the NAME, 
	and which character is the delimiter (for example, `:`, `;` or `,`). 
	<UIDfile>[:<UIDcol><delim><NAMEcol>]
	EXAMPLE:
	  If the file `main.uid` contains lines such as 
	    012345;Rossi,Giuseppe
	  the columns specifications are <UIDcol>=1 <delim>=; <NAMEcol>=2
	  and therefore one has to type
	    `uid main.uid:1;2`

        Omitting the optional 'spec' argument gives the default:
	`filename.uid` correponds to  `filename.uid:3:2`, i.e.,
	the third and second columns contain UID and name, with delimiter `:`.

        The default format is the output of 'esse3.py --uid Table.xls', the multi-tool
        available at www.dlfer.xyz/var/ (cf. the documentation there).

	If <UIDfile> is empty, the default is <main>.uid (if it exists),
	where <main>.tex is the main MCQ-XeLaTeX file.  
	OUTPUT: none; the file <main>_answers.txt is modified in-place.""" 
  if not os.path.exists(self.EF.answers):
   self.term.error("Error: answers file `%s` does not exist\nCreate one, or run `omr` first." % self.EF.answers)
   return 
  fd=file(self.EF.answers,'r')
  answers_list=fd.readlines()
  fd.close()
  args=args.strip()
  if args=='':
   args=self.EF.uidfile
   if not os.path.exists(args):
    self.term.error("Error: uid file `%s` does not exist\nCreate one, or run `uid <filename>` instead\n(type `? uid` for help)" % self.EF.uidfile)
    return 
  UIDFILE=args
  try:
   result=merge_files(answers_list,UIDFILE)
  except: 
   self.term.error("ERROR: updating answers on `%s` from uid file `%s` failed" % self.EF.answers, UIDfile)
   return 
  output=file(self.EF.answers,'w')
  output.write(result)
  output.close()
  self.term.msg("Answers file %s updated." % self.EF.answers)
  return 
 def do_mark(self,args):
  r"""USAGE: mark [<answersfile>] 
	Take the optional argument <answersfile>, and give marks according to 
	the answer keys generated by `exam`. 
	Default answersfile: `<main>_answers.txt` 
	The general format of the answers lines is the following:
	  FXZH:Verdi, Giuseppe:193146:ADba:30
	  <CODE>:<NAME>:<UID>:<ANSWERS>:<OPTIONAL_MARK>
	where <CODE> is the code of the permutation,
	<NAME> is the name, <UID> the User Identification number, and 
	<ANSWERS> is a string of length = number of questions, where the k-th
	character is the given answer (a case-insensitive letter), 
	or `0` if no answer was given.
	The optional field <OPTIONAL_MARK> is a number, which can be given 
	to assess other forms of exercises in the exam. 
	In general it is not used, so the line reads as
	   FXZH:Verdi, Giuseppe:193146:ADba:

	The output files are `<main>_exam.csv` and `<main>_exam.txt`.
	The format of the CSV version is 
	  FXZH;Verdi, Giuseppe;193146;15.0;14.0;29.0
	  <CODE>;<NAME>;<UID>;<MCQ_MARK>;<OPTIONAL_MARK>;<TOTAL>
	where <CODE>,<NAME>,<UID>, and <OPTIONAL_MARK> are as above.
	The new field <MCQ_MARK> is the sum of the numerical values 
	of the given answers, and <TOTAL> is the combination of 
	<MCQ_MARK> with <OPTIONAL_MARK> using the formula 
	`formulavoto` defined in the <main>.tex file (python syntax),
	where `x` stands for <MCQ_MARK> and `y` stands for <OPTIONAL_MARK>.
	EXAMPLE:
	  if in the <main>.tex file there is a
	   \formulavoto{x+2*y},
	  then in the result list the total mark will be
	   <TOTAL>=<MCQ_MARK> + 2 *<OPTIONAL_MARK> 
	
	The output file `<main>_exam.txt` is an anonymous version, with 
	just the <CODE> and <TOTAL> columns, used to publish results on-line. 

	OUTPUT: <main>_exam.csv, <main>_exam.txt"""
  if not os.path.exists(self.EF.exam_db):
   self.term.error("ERROR: the internal answer keys file `%s` does not exist!\nTry to (re-)run `exam`\nAborting..." % self.EF.exam_db)
   return 
  global DB_FILE, DB_STATS_FILE
  DB_FILE=file(self.EF.exam_db,'rb')
  DB_STATS_FILE=file(self.EF.exam_stats_db,'wb')
  output=file(self.EF.exam_csv,'w')
  if args.strip() == '':
   args=self.EF.answers
  try:
   data=file(args).read()
  except:
   self.term.error("ERROR: failed to load answersfile `%s`" % args)
   return 
  DB_LIST=pickle.load(DB_FILE); DB_FILE.close()
  num_exerm=number_of_items(DB_LIST)
  max_points=DB_LIST['__punti__'][0] * num_exerm
  try:
   li=correggi(DB_LIST,data)
  except:
   self.term.error("ERROR: marking failed... check logs... and re-try.")
   return 
  li=riarrangia(li,extract_target(data))
  riordina(li)
  output.write(display(li))
  output.close()
  output_pub=file(self.EF.exam_pub,'w')
  output_pub.write(display_pub(li,max_points))
  output_pub.close()
  pickle.dump(DB_LIST,DB_STATS_FILE); DB_STATS_FILE.close()
  # self.ui_generate_stats()
  self.term.msg("Results File `%s` created, with %i lines." % (output.name,len(li)))
  self.term.msg("You might want to publish the anonymous version `%s.`" % (output_pub.name,))
  return 
 def do_makestats(self,args):
  """USAGE: makestats
	Generate the statistics file (after marking).
	Each question will have the following indices for item analysis.
	The FACILITY INDEX $f$ is the percentage of students who 
	gave the right answer: if $f$< 30%, the question is too hard, 
	if $f$>75%, the question is too easy.  
	The DISCRIMINATION INDEX $d$ is the number of 27% top students 
	who gave the correct answer, minus the number of 27% bottom 
	students who gave the correct answer, divided by the number 
	of 27% students). If $d$>25%, it os OK. If $d$<20%, or worse,
	$d$ is negative, probably there is a mistake in the answer keys.

	OUTPUT: <main>_stats.pdf"""
  # check marks are already there...
  DB_STATS_FILE=file(self.EF.exam_stats_db,'rb')
  db=pickle.load(DB_STATS_FILE); DB_STATS_FILE.close()
  self.EF.refresh()
  data=self.EF.data
  if input_enc(data) == 'latin1':
   data=convert_to_utf(data)
  fd=file(self.EF.exam_stats_tex,'w')
  fd.write(generate_stats_texfile(data,db))
  fd.close()
  for i in range(2):
   retval = os.system("xelatex %s" % self.EF.exam_stats_tex)
   if retval:
    self.term.error("Error: STATS XeLaTeX compilation FAILED. Check logs and `%s`..." % self.EF.exam_stats_tex)
    return 
  self.term.msg("Statistics file %s generated." % self.EF.exam_stats_pdf )
  return 
 def do_pdfx(self,args):
  """USAGE: pdfx
	Attempt to convert the `<main>_exam.pdf` PDF file to a PDFX version, 
	more suitable for error-free printing, using ghostscript, if installed.
	It tries to set a proper GS_FONTPATH.  
"""
  if not os.path.exists(self.EF.exam_pdf):
   self.term.error("Error: The PDF file `%s` is missing...\nTry first to run `exam`" % self.EF.exam_pdf)
   return 
  pre_cmd=''
  if not os.environ.get('GS_FONTPATH'):
   self.term.msg("Warning: environment variable `GS_FONTPATH` is empty...\nTrying to automatically set it.\nIf the conversion fails, please check the logs and manually set `GS_FONTPATH`.")
   if self.term.platform=='mac':
    pre_cmd="GS_FONTPATH=/Library/Fonts/:%s/Library/Fonts/ " % os.path.expanduser("~") 
    self.term.msg(pre_cmd)
  todo_cmd=pre_cmd + "ps2pdf13 -dPDFX=true %s %s" % ( self.EF.exam_pdf,self.EF.basename+"_exam_pdfx.pdf")
  if os.system(todo_cmd):
   self.term.error("ERROR: Please check the logs. Running `pdfx` failed.")  
   return -1
  else:
   if os.path.exists(self.EF.basename+"_exam_pdfx.pdf"):
    self.term.msg("File `%s` generated." % (self.EF.basename+"_exam_pdfx.pdf",))
   else:
    self.term.error("ERROR: File `%s` was not generated. Unknown reason." % (self.EF.basename+"_exam_pdfx.pdf",))

#------------------------------------------------------------------------------
xelatex_template=r"""%%===================================================================
\documentclass[twoside,a4paper,leqno]{article}
%%===================================================================
\usepackage{mathpazo}
%(mcqpackage)s
\usepackage{polyglossia} %% apparently it's better than babel...
\setdefaultlanguage{%(language)s}

%%===================================================================
\headline{%(examname)s, %(examdate)s (%(examtime)s, %(examroom)s)}

\puntigiusta{%(puntigiusta)s} %% points for a correct answer
\puntisbagliata{%(puntisbagliata)s} %% points for a wrong answer (when not explicitely stated otherwise)
\puntiempty{%(puntiempty)s}  %% points for non-response.
%(advcomment)s\formulavoto{%(formulavoto)s}

%(advcomment)s%(variantlabelcmd)s

%%===================================================================
%% The following is necessary only if bubblesheet... 
%% \UIDdigits{5} 
%% change it if the default value (6) does not fit.


%%===================================================================
%% This is the text appearing on the right of the UID matrix.
%% It is safe to change it (but it should be not too long...)
%%\renewcommand{\geninfo}{%%
%%Instructions: fill \textbf{completely} the bubbles
%%with the digits of the SID (one for each column);
%%in the lower part of the sheet, fill \textbf{completely}
%%the bubble with the correct answers to the corresponding question.
%%Use a black or dark blue pen or pencil,
%%trying to fill completely the inside of the bubble.
%%Write only in the designated areas.
%%}
%%\renewcommand{\ansinfo}{\textbf{Mark the answers of the multiple-choice questions}}
%%\renewcommand{\uidname}{Student ID}
%%\renewcommand{\Cognomename}{Last Name}
%%\renewcommand{\Nomename}{First name}
%%\renewcommand{\Firmaname}{Signature}

%% the previous commands are equivalent to the command
%% \englishinfo

%% It is safe to renew \squarebox: empty for no-squarebox, 
%% or whatever Unicode character or symbol. It is the symbol appearing
%% on the left of each possible item-answer. Check that the characters
%% is included in the font...
%% \renewcommand{\squarebox}{--}

%% If changing the font, make sure that it's not too ugly. 
%% \setmainfont[Mapping=tex-text]{Linux Libertine}
%%===================================================================
\newcommand{\RR}{\mathbb{R}}
\newcommand{\CC}{\mathbb{C}}
\newcommand{\ZZ}{\mathbb{Z}}
\newcommand{\NN}{\mathbb{N}}
\renewcommand{\AA}{\mathbb{A}}
\newcommand{\EE}{\mathbb{E}}
\newcommand{\QQ}{\mathbb{Q}}
\newcommand{\PP}{\mathbb{P}}
\newcommand{\FF}{\mathbb{F}}
\newcommand{\KK}{\mathbb{K}}
\newcommand{\from}{\colon}
\newcommand{\vv}{\boldsymbol{v}}
\newcommand{\vw}{\boldsymbol{w}}


%%===================================================================
\begin{document}
\bubblesheet[2]{%(number_of_questions)s}{%(maxanswers)s}
%% the optional argument is the number of columns of the list of bubbles

\begin{esercizi*}{}
%% The second argument is the tile of the exercises section.

%(list_of_exers)s

\end{esercizi*}

\end{document}
\endinput
"""

generate_html_header=r"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">

<html>
<head>
  <meta name="generator" content="%(mcqxelatexurl)s">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

<style media="screen" type="text/css">
body {
	margin: 0px;
	padding: 0px;
	font-family: Georgia, Palatino, "Times New Roman", Times, serif;
	font-style : normal; 
	font-variant : normal;
	background-color: GhostWhite;
	color: DarkSlateGray;
	width: 100%%; 
	height: 100%%;
	text-align: center;
}

div.header {
	border-bottom: 2px solid black;
	background-color: GhostWhite;
	background-width: 100%%;
	height: 52px;
}

div.footer {
	position: relative;
	bottom: 0;
	border-top: 2px solid black;
	background-color: GhostWhite;
	width: 100%%;
	text-align: center;
	font-family: "Courier New", Courier, monospace;
	font-size: 10pt;
	padding-bottom: 14pt;
}


div.header h1 {
	float: left;
	margin-left: 12pt;
	font-family: "Courier New", Courier, monospace;
	font-size: 18pt;
	font-weight: bold;
}


div.header h2 {
	text-align: right;
	margin-right: 12pt;
	font-family: "Courier New", Courier, monospace;
	font-size: 14pt;
}

div.header h3 {
	text-align: right;
	margin-right: 12pt;
	margin-bottom: 24pt;
	font-family: "Courier New", Courier, monospace;
	font-size: 12pt;
	font-weight: normal;
}

div.body {
        position:relative;
	width: 75%%;
	padding: 10px;
	border-right: 2px dotted black;
	border-left: 2px dotted black;
	text-align: left;
	margin-left: 12.5%%;
	margin-right: 12.5%%;
	background-color: GhostWhite;
}

div.body h1, div.body h2, div.body h3, div.body h4, div.body h5, div.body h6 {
font-family: "Courier New", Courier, monospace;
}

li  {
width:90%%;
padding: 6px;
background: #FFFFBB;
border: 1px dashed black;
margin: 12px;
vertical-align: middle;
}

li li  {
border: none;
background: #F0F0B0;
padding: 6px;
}

ol li {
display: list-item;
vertical-align: top;
}


.toggle-view {
	 list-style:square;	
	 list-style-type:lower-alpha;	
	 list-style-position: outside;
}
	
.toggle-view li {
	width:82%%;
	padding: 10px;
	border: 1px dashed black;
	position:relative;
	cursor:pointer;
	}

	
.toggle-view span.mymark {
		position:absolute;
		right:5px; top:0;
		color:#22c;
	}

.toggle-view p {
		background-color:#FFF;
	        border: 2px solid #F10;
		margin: 10px;
		padding: 10px;
		display:none;
	        cursor:text;
	}
.toggle-view p.giusto {
		border: 2px solid #1F0;
	}
 
</style>

<title>%(title)s</title>
</head>
<body>
<div class="header" id="header">
    <h1>%(title)s</h1>
</div>
<div class="body" id="body">
    <script type="text/x-mathjax-config">
MathJax.Hub.Config({
    extensions: ["tex2jax.js","TeX/AMSmath.js","TeX/AMSsymbols.js"],
    jax: ["input/TeX", "output/HTML-CSS"],
    showProcessingMessages: true,
    displayAlign: "center",
    displayIndent: "0em",

    tex2jax: {
      inlineMath: [ ['$','$'], ["\\(","\\)"] ],
      displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
      processEscapes: false,
      processEnvironments: true,
      preview: "TeX"
    },
    "HTML-CSS": { availableFonts: ["TeX"] }
    });
    </script>
<script type="text/javascript"
   src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML-full.js">
</script>
 <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js">
</script>
 <script type="text/javascript">
    $(document).ready(function () {
        $('.toggle-view li').click(function () {

                var text = $(this).children('p');

                if (text.is(':hidden')) {
                        text.slideDown('200');
                         $(this).children('span.mymark').html('-');             
                } else {
                        text.slideUp('200');
                         $(this).children('span.mymark').html('+');             
                }
                
        });

    });
    </script>
 <noscript>
    <div style="color:#CC0000; text-align:center">
      <b>Warning: <a href="http://www.mathjax.org/">MathJax</a> requires JavaScript to process the mathematics on this page.<br>
      If your browser supports JavaScript, be sure it is enabled.</b>
    </div>
    <hr></noscript>
"""

generate_html_footer=r"""
</div>
<div class="footer">
<p>
%(title)s.
Generated by <a href="%(mcqxelatexurl)s">MCQ-XeLaTeX</a>, 
%(today)s.
</>
</div>
</body>
</html>
"""
##---------------------------------------------------------------------------
def my_glob(s,basedir="."):
    list_s=s.split()
    files=[]
    for chunk in list_s:
     files += glob.glob(os.path.join(basedir, chunk ) )
    return files
##---------------------------------------------------------------------------
uiChooser_firstinfo="""Welcome. This is the MCQ-XeLaTeX Questions random chooser.
You can use the commands listed below to choose random questions 
form the Question Bank.

Main Commands (type `? <command>` for help):
qbank [<directory>]  : show or set the Question Bank Directory 
load <commandsfile>  : load a commandsfile
lsbank               : list files in the Question Bank Directory
ls  <arg>            : list files  
add <n> from <files> : add <n> questions from the list of files 
			(separated by space, wildcard `*` acceptable).
del <n>	| all        : remove n-th question, or all the quesitons
make	 	     : generate `<main>.pdf`
open                 : open the file (e.g. for viewing, open main.pdf)
random all|<n>	     : draw all or just exercise <n>, and create <main>.tex
status               : show status of the chosen questions
rehash               : reload the full set of questions from the qbank
next                 : Accept the random choice and proceed. 
x                    : Exit (without accepting)
"""
##---------------------------------------------------------------------------
class uiChooser(uiShell):
 global persistdb
 def __init__(self,dbvars={},term=None): 
  uiShell.__init__(self,'qbank',term=term)
  self.lsdir,self.lsfiles=self.thisdir_ls('')
  self.db=dbvars
  self.db['list_of_exers']=''
  self.cwdir=os.getcwd()
  self.allquestions_db={}
  self.allquestions=[]
  if persistdb.get('qbank'):
    ##__HERE__ 
    self.do_rehash() 
    if VERBOSE: sys.stderr.write("qbank= %s" % persistdb.get('qbank') )
 def do_make(self,args):
  """USAGE: make
	Compile (XeLaTeX-ing) the TeX file generated file. 
	OUTPUT: <file>.pdf
"""
  for i in range(2):
   retval = os.system("xelatex %s" % self.db.get('filename'))
   if retval:
    self.term.error("Error: compilation FAILED!\nCheck logs, edit `%s` and re-run xelatex." % self.db.get('filename') )
    return 
  bn,ext=os.path.splitext(self.db.get('filename'))
  pdffile=bn+'.pdf'
  self.term.msg("Compilation seems OK. Check `%s` please." % pdffile )
  return 
 def do_add(self,args):
  """USAGE add <n> from file1.tex f2.tex ... f2*.tex

"""
  toks=args.split()
  if len(toks) < 3 or toks[1] != 'from':
    self.term.error("Syntax Error")
    return self.do_help("add")
  try:
   num=int(toks[0])
   globstring = " ".join(toks[2:])
  except:
   self.term.error("Syntax Error")
   return do_help("add")
  if 'todolist' in persistdb:
   for iinum in range(num):
    persistdb['todolist'] +=    [ [globstring, None ] ] 
  else:
   persistdb['todolist'] =  [] 
   for iinum in range(num):
    persistdb['todolist'] +=    [ [globstring, None ] ] 
 def get_exer(self,file,number):
  try:
   result=self.allquestions_db[file][number]
  except Exception , v:
   self.term.error("FAILED for filename `%s` and index `%s`" % (file,number) )
   self.term.error("FAILED with error: `%s`" % v)
   result = None
  return result 
 def do_ls(self,args):
  """USAGE: ls [<path>]
	Return the list of .TeX files or directories containing TeX files
	or directories. If the optional argument <path> is missing, 
	the current dir will be listed.
	If <path> is a directory, its content will be listed.
	If <path> is a file, just this file will be listed."""
  dirs,files=self.thisdir_ls(args)
  if dirs or files:
   self.term.write("\n".join(dirs) + " \n" + "\n ".join(files) + "\n")
 def do_lsbank(self,args):
  """USAGE: ls 
	Return the list of .TeX files in the Question Bank Directory. 
	"""
  # TODO: count the number of questions in each file. __TODO__ 
  dirs,files=self.thisdir_ls(persistdb.get('qbank'),filtered='.tex')
  decorated_files=[]
  if files: 
    for x in files:
      data=file(os.path.join(persistdb.get('qbank'),x),'r').read()
      data=strip_latex_comments(data)
      if input_enc(data) == 'latin1':
        data=convert_to_utf(data)
      numexer=len(extract_esercizi(data))
      decorated_files += [ "%s (%d)" % (x,numexer)  ]
      # self.term.write("%s: number of exer=%d\n" % (x,numexer)) 
      # get the number of exercises in the file... 
      if VERBOSE: sys.stderr.write("%s\n" % len(extract_esercizi(os.path.join(persistdb.get('qbank'),x))))
  if dirs or files:
   self.term.write("\n".join(dirs) + "\n " + "\n ".join(decorated_files) + "\n")
 def do_qbank(self,args):
  """USAGE: qbank <directory>
	This commands define the Question Bank = <directory>
	Use ls, cd and tab-completion to locate the file, first.
"""
  args=args.strip()
  if args == '':
   dbank=persistdb.get('qbank')
   if dbank:
    self.term.msg("The Question Bank is set: qbank=%s" % persistdb['qbank'])
   else:
    self.term.msg("Question Bank not yet defined...")
   return 
  if os.path.exists(args) and os.path.isdir(args):
   persistdb['qbank']  = os.path.abspath(args)
   self.term.msg('Scanning for exercises...')
   self.do_rehash()
   self.term.msg('Question Bank %s loaded: back to main menu.' % args)
   return 
  else:
   self.term.error('Error: `%s` is not a Directory!' % args)
   return 
 def do_cd(self,arg):
  """USAGE: cd [<dir>]
	Change working directory to directory <arg>. With no <dir> argument,
	it will go to the Main File Directory."""
  if arg.strip() == '':
   target,_=os.path.split(self.db['abspath'])
   arg=os.path.expanduser(target)
  if os.path.exists(arg) and  os.path.isdir(arg):
   try:
    os.chdir(arg)
   except Exception , v:
    self.term.error("Error: %s" % v)
  else:
    self.term.error("Error: `%s` is not a directory!" % arg)
  self.updateprompt()
 def do_status(self,args):
  """status: print the current status of all chosen questions form the databank"""
  tmpdb=self.db
  if isinstance(persistdb.get('todolist'),list):
   tmplist=[]
   ii=0
   for y,chosen in persistdb.get('todolist'): 
    ii += 1
    if chosen:
     try:
      description = "(%s : #%s)" % (chosen[0],chosen[1]+1)
     except Exception , v:
      description = "[%s]" %  v
    else:
     description = "(Not yet choosen)"
    tmplist += [ "%i) 1 question from %s %s" % (ii,y,description) ]
   tmpdb['pretty_todolist']="\n".join(tmplist)
  else:
   tmpdb['pretty_todolist']="None"
  tmpdb['qbank']=persistdb.get('qbank')
  self.term.write(self.term.boxed_message("""Filename %(filename)s [%(examname)s, %(examdate)s (%(examtime)s, %(examroom)s)]
%(abspath)s
Question Bank: %(qbank)s

Added list:
%(pretty_todolist)s
""" % tmpdb ) )
 def do_rehash(self,args=None):
  'Restart and rehash all'
  if VERBOSE: sys.stderr.write("DEBUG: REHASHING...\n")
  self.allquestions_db={}
  self.allquestions=[]
  for g,pair in persistdb.get('todolist'):
   # files=glob.glob(os.path.join(persistdb.get('qbank'),g))
   files=my_glob(g,basedir=persistdb.get('qbank'))
   for x in files:
    if not x in self.allquestions_db:
     eserlist=[]
     data=file(x,'r').read()
     data=strip_latex_comments(data)
     if input_enc(data) == 'latin1':
       data=convert_to_utf(data)
     eserlist += extract_esercizi(data)
     self.allquestions_db[x]= eserlist
     self.allquestions += [(x,j) for j in range(len(eserlist))]
 def update_questions(self):
  self.db['list_of_exers']=''
  for g,pair in persistdb.get('todolist'):
   if pair:
     try:
      ese=self.allquestions_db.get(pair[0])[pair[1]]
     except Exception , v:
      ese="FAILED"
      self.term.error("ERROR (update_questions): %s" % v) 
   else: 
     ese="NONE"
   self.db['list_of_exers'] += "\n" + r"""
\begin{exerm}
%s
\end{exerm}
""" % ese 
  fd=open(self.db['filename'],'w')
  fd.write(xelatex_template % self.db)
  fd.close()
  self.term.msg("File %s generated! Please edit it and come back when finished!" % fd.name)
 def single_random_choose(self,filelist):
  random.seed()
  tmplist  = [] #__HERE__ TRY TO FINISH! 
  if VERBOSE: sys.stderr.write("Trying to single_random_choose from filelist:%s\n" % filelist) 
  for f in filelist:
   tmplist += [ (qf,i) for (qf,i) in self.allquestions if qf == f ]
  L=len(tmplist) 
  if L==0:
   self.term.error("SOMETHING WRONG: there are no files to choose from Filelist=%s" % str(filelist) )
   self.term.error("Probably it is a corrupted questions database. Try with `rehash`"  )
   return (None,None)
  thisese=tmplist.pop(random.randint(0,L-1))
  del self.allquestions[self.allquestions.index(thisese)]
  return thisese  
 def do_random(self,args):
  """USAGE: random [all]|[<n>] [n_2] ...
	Random choose either all questions (if no argument or `all` is given).
	Otherwise random choose just the n-th question.
	EXAMPLES:
	random all
	random
	random 3
	random 3 5 7
"""
  self.do_rehash()  ## is it necessary? 
  args=args.strip()
  if args=='all' or args=='':
   # reset allquestions
   result=[]
   newtodolist=[]
   for ii  in range(len(persistdb['todolist'])):
    x,chosen=persistdb['todolist'][ii]
    # files=glob.glob(os.path.join(persistdb.get('qbank'),x))
    files=my_glob(x,basedir=persistdb.get('qbank'))
    # todo: rewrite random_choose, to have a poplist
    qfile,qnumber = self.single_random_choose(files) 
    if qfile:
     persistdb['todolist'][ii][1]=(qfile,qnumber) 
     # result += [self.get_exer(qfile,qnumber) ]
   self.update_questions()
   return 
  try:
   numbers=[int(a) -1 for a in args.split() ]
   for ii in numbers:
    self.term.write("Replacing question %s\n" % (ii+1,))
    s=persistdb['todolist'][ii][0]
    files = my_glob(s,basedir=persistdb.get('qbank') )
    qfile,qnumber = self.single_random_choose(files) 
    if qfile:
     persistdb['todolist'][ii][1]=(qfile,qnumber)
   self.update_questions()
  except Exception , v:
   self.term.error("FAILED: `%s`" % v)
 def do_del(self,args):
  """del <n>|all: delete the n-th question from the list, or all"""
  if args=='all':
     persistdb['todolist']=[]
     return 
  try:
   n = int(args) -1
   del persistdb['todolist'][n]
  except Exception , v:
   self.term.error("Error %s: del failed..." % v)
   return 
 def do_q(self,args):
  """q: quit from the procedure."""
  self.term.msg("Quitting from MCQ-XeLaTeX %s..." % self.name )
  return -1
 def do_next(self,args):
  "Next: all finished, proceed to the Work Menu."
  return self.do_q(args)
 def do_load(self,args):
  """USAGE: load <commandsfile>
        Load a file with add commands, one per line (lines not starting with 'add' are ignored)"
	EQUIVALENT EXAMPLES:
	  load commandsfile.txt
	  load command<TAB>"""
  # TODO: properly load classes to parse the file 
  if args.strip() == '':
   self.term.error("ERROR: missing argument of `load`\nType `? load` for help.")
   return 
  if os.path.exists(args) and os.path.isfile(args):
   self.term.msg("Commands File '%s' loaded" % args)
  else:
   self.term.error('Error: `%s` is not a TeX file!' % args)
  for r in file(args).readlines():
    if r[:3] == 'add':
        tmparg=(r[3:]).strip()
        self.term.msg("Adding command: 'add %s'" %  tmparg) 
        self.do_add(tmparg)
    else:
        self.term.msg("Line '%s' ignored" % r)
  return 



##---------------------------------------------------------------------------

def newfileloop(term):
 global persistdb
 # term=myTerm(output=sys.stdout) 
 term.msg("""Comrade %s, now I will ask you some questions about the exam.
Please patiently answer the questions, and read the instructions. 
At the end, a main MCQ-XeLaTeX file will be generated. You will be able
to review, edit and modify it easily later. 
Type `!x` if you want to quit.
""" % term.username )
 vars=[
('examname',"Name of the Course","Example Course",
"""Name of the course. For example `History of Marxism`."""),
('examdate',"Date of the Exam", "No Date",
"Date of the exam. For example, `2014-04-23`"),
('examtime',"Time of the Exam", "16:00",
"Time of the exam. For example, `16:00`"),
('examroom',"Room where the Exam will be", "U1-09",
"The room, a description, an address. Short."),
('language',"What is your language", "italian",
"Language, in the format \\setdefaultlanguage{language} polyglossia understands."),
('puntigiusta',"Pts for the correct answer", "3",
"""How many points a correct answer counts. A good candidate for
a question with $n$ answers, is $n-1$."""),
('puntisbagliata',"Pts for the wrong answer", "-1",
"""How many points a wrong answer counts. A good value could be -1."""),
('puntiempty',"Pts for a non-response", "0",
"""How many points a question without any answer (a non-response).
A common choice is 0 pts."""),
('number_of_questions',"Number of questions you plan to add", 10,
"""Simply the number of Multiple Choice questions. You can change it later.
Recall that for mathematics each question should take 2-3 minutes at most."""),
('maxanswers',"Number of answers each question will have", 4,
"""Each question will have this number of answers. Please keep it constant."""),
('hassol',"Do you want to show an asterisk to mark the correct answers, and do you want to show the feedback text? (Do not use for real exam) [Yes/No]" , "Yes","""This option will show the correct answers in the PDF file. 
Review carefully the PDF before generating the permutation copies, and 
remove the `sol` option when finished."""),
('hasbubblesheet',"Do you plan to use bubblesheet and OMR? [Yes/No]", "Yes",
"""The bubblesheet is the sheet where students fill bubbles to indicate
their UID and the chosen answer, for each question.
With a scanner (and an auto-feeder) you can grade hundreds of sheets in minutes."""),
('advanced',"Do you need to set advanced options", "No", 
"Advanced options are, so to say, advanced, and not for beginngers."),
('formulavoto',"Formula to aggregate <MCQ_MARK> and <OPTIONAL_MARK>", "x",
"""The exam might consist of a Multiple-Choice part, followed by some
open-ended questions or exercises. The mark of the MCQ part will be 
computed automatically, and denoted by <MCQ_MARK>. The mark of the 
open-ended part needs to be given by your grading, comrade %s. 
This formula is simply the way to sum the two parts, in python syntax.""" % term.username),
('hasvariants',"Do you want to have questions with multiple variants? [Yes/No]","No","""Instead of just permuting the questions and the answers, you can 
randomly choose variants (with different numerical values, or different 
questions and different answers) of the questions."""),
('hasvariantlabel',"Do you need a variantlabel, to allow multiple versions of the main MCQ-XeLaTeX file? [Yes/No]" ,"No",
"""If you set a VariantLabel, the code identifying each permuted copy
will have it as prefix. This allows to manually author different versions
of the same main TeX file, and distribute them randomly in class, but
still be able to use OMR and the automatical marking."""),
('hasblankpage',"Do you need a blank page after the bubblesheet? [Yes/No]", "Yes","""If you use a duplex printer, you might want to leave a blank page after the bubblesheet."""),
('hasextrasheet',"Do you need to print two copies of the bubblesheet for each student? [Yes/No]", "No","""Some students are worse than others in filling bubbles. 
Sometimes it is better to give them two identical copies of the bubblesheet,
so they can avoid impossible corrections."""),
('UIDdigits',"How many digits does the UID have", 6,
"""The User IDentification number is necessary, if you do want to 
associate the sheet to a student. You should check the identity of the 
student, and check that the marked UID corresponds with eir UID."""),
('dochooser','Do you want to randomly import questions from a Question Bank?','Yes',"""By setting a question bank, ...."""),
('filename', "Name of the file on which to save", "firstexample.tex",
"""Choose a filename. Warning: the file will be over-written!""")
] 
 db_deps_src={ 'hasbubblesheet': ('y',['hasblankpage','hasextrasheet','UIDdigits']) ,
'advanced': ('y', ['formulavoto','hasvariants', 'hasvariantlabel', 'hasblankpage', 'hasextrasheet', 'UIDdigits','dochooser'] )
}
 # reverse the dependencies 
 needed_commands=['advanced', 'UIDdigits','formulavoto','hasvariants','hasvariantlabel','hasblankpage','hasextrasheet']
 db_deps={}
 for k in db_deps_src.keys():
  kv,values=db_deps_src[k]
  for v in values:
   db_deps[v]=(k,kv)
 db={}
 if 'saved_db' in persistdb.keys():
  saved_db=persistdb['saved_db']
 else:
  saved_db={}
 for k,desc,deft,hel in vars:
  if k in saved_db:
   deft=saved_db[k]
  # deft is the last used
  # check if deps are ok...
  if k in db_deps.keys() and db_deps[k][0] in db.keys() and not db[db_deps[k][0]].lower().startswith(db_deps[k][1]) :
   if k in needed_commands: 
    db[k] = deft
   continue
  # if it's the last
  if k == vars[-1][0]:
   term.write(term.termcmd('green black blink') + term.boxed_message(desc + "?") + term.termcmd() )
  elif k=='advanced':
   term.write(term.termcmd('cyan') + term.boxed_message(desc+"?") + term.termcmd() )
  else:
   term.msg(desc + "?")
  term.prompt = "(New)mcq-> [%s] >" % deft
  while 1:
   i=term.input().strip()
   if i=='?':
    term.write(hel+"\n")
   elif i=='!x':
    term.msg("Quitting...")
    return 
   else:
    break
  db[k] = i or deft
  if k=='filename':
   bn,ext=os.path.splitext(db[k])
   if not ext:
    db[k] = db[k] + ".tex"
   db['abspath']=os.path.abspath(db[k])
 # check options
 persistdb['saved_db']=db
 p_options=[]
 options_map={
 'bubblesheet': ('hasbubblesheet','y'),
 'noblankpage': ('hasblankpage','n') ,
 'extrasheet': ('hasextrasheet','y') ,
 'sol' : ('hassol','y') }
 for o in options_map.keys():
  k,v=options_map[o]
  if k in db.keys() and db[k].lower().startswith(v):
   p_options += [o]
 if p_options:
  db['mcqpackage']=r"\usepackage[%s]{mcq}" % (",".join(p_options))
 else:
  db['mcqpackage']=r"\usepackage{mcq}" 
 if db['hasvariantlabel'].lower().startswith('y'):
  db['variantlabelcmd']=r"\variantlabel{X}%% change the value to what needed"
 else:
  db['variantlabelcmd']=''
 # 
 if db['hasvariants'].lower().startswith('y'):
  has_variants=True
 else:
  has_variants=False
 if db.get('advanced').lower().startswith('y'):
  db['advcomment']=''
 else:
  db['advcomment']='%'
 number_of_questions=int(db['number_of_questions'])
 maxanswers=int(db['maxanswers'])
 esercizio=r"""
\begin{exerm}
Text of the question. 
\begin{rispm}
%s
\end{rispm}
\end{exerm}
""" % "\n".join([ r"\risp[=]  %This is the correct answer: use \fb{} for feedback!" ] +  ([ r"\risp  %Use \fb{} for feedback!" ] * (maxanswers -1))  )
 variantese=r"""
\begin{exerm}
%% Exercise with variants. 
\begin{varianti} 
%% Each variant is a separate \varitem 
\varitem 
text
\begin{rispm}
%s
\end{rispm}
\varitem
text
\begin{rispm}
%s
\end{rispm}
\end{varianti}
\end{exerm}
""" %  ( "\n".join([ r"\risp[=]" ] +  [ r"\risp" ] * (maxanswers -1)  ), "\n".join([ r"\risp[=]" ] +  [ r"\risp" ] * (maxanswers -1)  ) ) 
 if has_variants:
  esercizi=variantese + esercizio * (number_of_questions -1)
 else:
  esercizi= esercizio * (number_of_questions )
 db['list_of_exers']=esercizi 
 if 'dochooser' in db.keys() and db['dochooser'].lower().startswith('y'):
  uiChooser(term=term,dbvars=db).cmdloop(uiChooser_firstinfo)
  # hopefully db['list_of_exers'] is correctly updated.
 else:
  db['list_of_exers']=esercizi 
 # sys.stderr.write("UICHOOSER:\n%s" % db)
  fd=open(db['filename'],'w')
  fd.write(xelatex_template % db)
  fd.close()
  term.msg("File %s generated! Please edit it and come back when finished!" % fd.name)
 s=raw_input('Press <Return> to continue...')
 return db.get('filename') 

#------------------------------------------------------------------------------
def uiloop():
 global persistdb
 s='-'
 sys.stderr.write("MCQ-XeLaTeX Interactive Interface loading...\n")
 term=myTerm(output=sys.stdout)
 term.prompt=term.termcmd("green black bold") + " mcq->> " + term.termcmd()
 persistdb=term.read_persistdb() 
 term.write(mcqlogo)
 if not persistdb['activefile']:
  welcome_msg="""Welcome to the MCQ-XeLaTeX majestic CLI, comrade %(username)s. 
I'm a very primitive and fragile interface, so please read the messages.
You can choose to be guided in authoring a new MCQ-XeLaTeX main file, 
reviewing all its commands, or to work on an existing one.
After this menu, you will be using just Command Line Interfaces, no 
windows, and will be given further details about the procedures. 
Your progress will be saved, unless otherwise instructed or stated.  By 
proceeding further, you accept the terms of the End User Licence Agreement
available on %(mcqxelatexurl)s

Check the REQUIREMENTS at the same web-page. 
Your Python version apparently is %(pythonversion)s. 
%(requirements)s
""" % {'username': term.username, 'pythonversion': "%s.%s.%s" %(sys.version_info[0], sys.version_info[1], sys.version_info[2]) , 'mcqxelatexurl' : MCQXELATEXURL ,'requirements': term.get_requirements()} 
  term.write(term.boxed_message(welcome_msg))
  # term.say(welcome_msg)
  term.msg("Press <Return> to proceed...")
  term.input()
 # this is the first-level, main loop 
 while s!='q':
  # loop only for non-active file.
  if persistdb['activefile']:
   if not os.path.exists(persistdb['activefile']) or not os.path.isfile(persistdb['activefile']):
    term.error("ERROR: file `%s` missing or not valid file!\nPlease check the logs and re-try..." %persistdb['activefile'])
    persistdb['activefile']=None
    continue
   if VERBOSE: sys.stderr.write("DEBUG: parsing file %s\n" % persistdb['activefile']) 
   file_content=file(persistdb['activefile']).read()
   try:
     esercizi=[parse_esercizio(es) for es in extract_esercizi(file_content)]
   except Exception, v:
    term.error("ERROR: file `%s` is not valid!\nPlease check and re-try..." %persistdb['activefile'])
    sys.stderr.write("Exception: %s\n" % v) 
    persistdb['activefile']=None
    continue
   numero_esercizi=len(esercizi)
   numero_maxrisposte=0
   for ese in esercizi:
    if ese.numero_risposte()>numero_maxrisposte:
     numero_maxrisposte=ese.numero_risposte()
   headline=extract_headline(file_content)
   workdir,filename = os.path.split(persistdb['activefile'])
   last_edited=datetime.datetime.fromtimestamp(os.path.getmtime(persistdb['activefile']))
   bn,ext=os.path.splitext(filename)
   pdffile=bn+'.pdf'
   last_xelatexed='Never'
   if os.path.exists(pdffile):
    last_xelatexed=datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(workdir,pdffile)))
   os.chdir(workdir)
#    term.write(term.boxed_message(""">Current Main File: %s (%s)
# Number of exercises: %i --  Number of (max) answers: %i
# Last edited on: %s      --  Last XeLaTeX'ed on: %s
# """ % (filename,headline,numero_esercizi,numero_maxrisposte,last_edited,last_xelatexed)  ))
   term.write(term.boxed_message(  ExamFile(persistdb['activefile']).show_status() ))
   uiMasterFile(term=term).cmdloop(uiMasterFile_firstinfo)
   continue
  if not persistdb['activefile']:
   term.write(term.boxed_message("""Available single-letter commands:
o : [O]pen an existing MCQ-XeLaTeX main file.
c : [C]reate a new MCQ-XeLaTeX main file from a template.
u : Launch a G[U]I (Graphical [U]ser Interface for Pendejos).
q : [Q]uit
"""))
  term.msg("Command?")
  try:
   s=term.input()
  except:
   term.msg("Quitting (for unknown reason)...")
   break
  if s.lower()=='q':
   term.msg("Quitting (bye)...")
   break
  elif s.lower()=='o':
   uiFileNavigator(term=term).cmdloop(uiFileNavigator_firstinfo)
  elif s.lower()=='c':
   # uiMarks().cmdloop(" Create a MCQ-LaTeX main file " )
   # term.msg("Not yet functional (bye)...")
   filename=newfileloop(term)
   if filename:
    persistdb['activefile']  = os.path.abspath(filename)
   # break
  elif s.lower()=='u': 
   term.msg("Trying to launch a Graphical [U]ser Interface...")
   term.msg("(Are you sure you need a GUI? Confirm: are your really a pendejo?)")
   nopes=raw_input('Enter the answer and <Return> to continue... > ')
   if len(nopes)>0 and nopes[0].lower() == 'y':
     term.msg("Ok then. Here we are. Sorry, I did not have time for that. Bye.")
     term.open("https://en.wikipedia.org/wiki/Console_application")
     break 
   else:
     term.msg("Well then. Let us try again.")
  else:
   if s:
    term.msg("You entered: %s (unknown command)" % s )
 term.write_persistdb(persistdb)
 


#-----------------------------------------------------------------------

def main():
	global NUMBER_OF_COPIES, EVALUATE, GIFT, XHTML, BASENAMEFILE
        data,output=get_opt()
        origdata=data
        if EVALUATE:
         DB_LIST=pickle.load(DB_FILE); DB_FILE.close()
         sys.stderr.write("Evaluating...\n" )
	 num_exerm=number_of_items(DB_LIST)
         max_points=DB_LIST['__punti__'][0] * num_exerm
	 li=correggi(DB_LIST,data) 
         li=riarrangia(li,extract_target(data))
	 riordina(li)
	 output.write(display(li))
         print display_pub(li,max_points)
         # produce_stats(DB_LIST['__stats__'])
         pickle.dump(DB_LIST,DB_STATS_FILE); DB_STATS_FILE.close()
         sys.stderr.write("done! File %s created!\n" % output.name)
         return
	data=strip_latex_comments(data)
        if GIFT:
         if input_enc(data) == 'latin1':
          data=convert_to_utf(data)
         output.write(generate_gift(data))
         return
        if XHTML:
         if input_enc(data) == 'latin1':
          data=convert_to_utf(data)
         output.write(generate_xhtml(data))
         return
        if MAKE_STATS:
         db=pickle.load(DB_STATS_FILE); DB_STATS_FILE.close()
         if input_enc(data) == 'latin1':
          data=convert_to_utf(data)
         output.write(generate_stats_texfile(data,db))
         return 
        output.write(generate_copies(data,NUMBER_OF_COPIES))
	sys.stderr.write("Output written to file: %s\n" % output.name)
        try:
         lbldb=getdb_labels(BASENAMEFILE)
         db2xml(lbldb,BASENAMEFILE+'.xml')
	 sys.stderr.write("XML Output written to file: %s\n" % (BASENAMEFILE+'.xml'))
	except:
	 sys.stderr.write("XML Output failed for file: %s\n => try `xelatex %s` first...\n" % (BASENAMEFILE+'.xml',BASENAMEFILE+'.tex'))

if __name__=='__main__':
  main()





