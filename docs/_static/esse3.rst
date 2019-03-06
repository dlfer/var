ESSE3.py: a few useful functions for u-gov S3
=============================================

A damn literal block:

USAGE::

 esse3.py [options] [argument]
 # Version: __INCLUDE_DATE__
  
 OPTIONS:
     --help|-h
     --uid Nomefile.xls	# lista iscritti 
                        # :matricola:cognome,nome:
     --pdf Nomefile.xls	# registro pdf
     --call 		# chiama per firma digitale
     --yml 		# genera il file csv del registro 
                        # delle lezioni da yml
     --baseoutput|-b=[base]
  
 FILES:
     ~/.esse3rc 	(options file)
 ---
  
 (C) DLFerrario http://www.dlfer.xyz




Options with the dictionary syntax:  

  **--help, -h**
    Aiuto (this)
 

  **--uid Nomefile.xls** 

    lista iscritti :matricola:cognome,nome:

  pdf Nomefile.xls | and what

    registro pdf

  call | and therefore

    chiama

  yml xmlfile | e su e giu'

    Crea registro  



Options as option lists:

  --help, -h
    aiuto

  --uid <Nomefile.xls>    
    lista iscritti :matricola:cognome,nome:  
    Questa dovrebbe essere una lunga cosa, che 
    forse funziona e forse no. 
  
  --pdf <Nomefile.xls>    
    crea registro pdf
  
  --call
    chiama per firma digitale
  
  --yml <Nomefile.yml>    
   genera il file csv del registro delle lezioni da yml
  
  --baseoutput,-b=<base>  
    output 



Examples:

 First example::

   $ esse3.py --yml


 Another example::

   $ esse3.py --pdf Lista.xls

 Last example::

   $ esse3.py --uid Lista.xls



This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
