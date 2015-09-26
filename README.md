# pasteAnalyzer
Search in Google custom engine for a keyword in the text and analyze this for match with regular expressions.   
Support: github.com, gist.github.com, pastebin.com, pastee.org, and pastie.org.

#Dependencies (Python 2.7)
google-api-python-client ( https://github.com/google/google-api-python-client )

#Instructions
1. You need a Google Account, for use Google custom search engine (engine-id) and Google custom API (api-key).
2. Follow tutorial ... https://developers.google.com/custom-search/json-api/v1/introduction

3. ./regex is a example of regular expressions file, format is first line category started with #, second line regular expression ... and repeat ... and repeat.

4. Regular expressions ONLY allow ONE group of capture, is REQUIRED. ()

5. JSON output file format:   
[   
	  u'http://pastebin.com/AB51SAQS2',   
	  [ 'Email',[ 'email@email.com','myemail@domain.com' ] ],   
	  u'htpp://pastee.org/jw5151a',   
	  [ 'Password',[ 'Mypasswordis123', 'Mypass' ],'EMail',[ 'email@dom.com' ] ]    
]

#Command Example

./pasteAnalyzer.py -q CTF -a AIYLZ-fX33rwmo -e 016273:o_yf_nza -r regex -j JSON -v

#Arguments

 -h, --help     
 					   show this help message and exit		
 
 -q QUERY, --query QUERY		
                       Search query

 -a APIKEY, --api-key APIKEY		
                       Google custom search Api Key

 -e ENGINEID, --engine-id ENGINEID		
                       Google custom search Engine Id

 -r REGEXFILE, --regex-file REGEXFILE		
                       File with regex for analysis

 -j JSON, --json JSON  
 					   Output to JSON file		
 
 -v, --verbose         
 					   Verbose mode

 
#Faraday Plugin
The plugin add a new host "pasteAnalyzer", a new interface "Results" and a new Service "Web".
In this service all results of pasteAnalyzer are loaded.

Install is simple, copy the faradayPlugin folder of this repository to {FARADAY_INSTALL_DIR}/plugins/repo/
Rename "faradayPlugin" to parseAnalyzer.
Ready!

