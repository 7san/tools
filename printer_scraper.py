'''
Takes "HP LaserJets" of several different flavors and attemtps to scrape useful information, such as
 - User
 - Job
 - Date/Time
currently. 

was used as a proof-of-concept. 

todo:
 - more error checking
 - user input of ip/url
 - error check that
 - print output to a file? probably
 - prettier output?

will i do?:
 - not unless i ever run into one of these ever again. 

python2.7 bc this was written before python3 won the war.

'''
#for xcode parsing (you know it's gonna be a fun time when BeautifulSoup throws up on the webpage you tried to feed it)
#boy i hope this library still exists, im not going back to check rn. 
from lxml import html
#for grabbing the webpage (did you know, urllib2 /also/ doesn't like these printer pages, what are the odds)
import requests
#for fun
import datetime


#should get url from user
#but for now, just replace the hardcoded string. 
url = "http://url.com"
#should also do some error checking on this field
#or prompt for only IP, then
#url = "http://"+url #but might also have to do checking on whether the thing is http or https

#these are likely specific to the hosts i was dealing with and may not be universal. 
sub1="/info_colorUsageJobLog.html?tab=Home&menu=ColorUsageLog"
sub2="/info_jobLog.html?tab=Home&menu=JobLog"

fullurl = url+sub1
page = requests.get(fullurl)

#see if page exists
if page.status_code != 200:
  fullurl = url+sub2
  page = requests.get(fullurl)
  if page.status_code == 200:
    print "No Job Log located. Sorry!"
    print "Exiting Program."
    exit()

#grab source
tree = html.fromstring(page.content)

#grab whole table from xpath
xpath="//table[@class='mainContentArea']//text()"
table = tree.xpath(xpath)

#remove leading and trailing whitespace
#(normalize-whitespace() does not behave as advertised 
i=0
while i<len(table):
  table[i]=table[i].strip()
  i = i+1

#remove blank entries
table = filter(None, table)

#find index of User in table (used for offset calculations)
userindex = -1
for i in (i for i,x in enumerate(table) if x == "User"): 
  userindex=i  

if userindex == -1:
  print "No User field found in table. Exiting Program."
  exit()

#the meaty stuff with mod, like ew am i right
#also threw in dictionaries because yay symbolically linked information 
#calculates the correct index using mod and throws info into a list of dicts
infolist = []
rows = 7
j=0
while i < len(table):
  #i swear to you, -3 use to be the offset, now i have no idea what's happening. 
  index = (i%rows)+userindex+i-5
  if index < len(table):
    x = {"User":table[index], "Date":table[index-1], "Job":table[index+1]}
    infolist.append(dict(x))
  i = i+rows
  j = j+1

#probably ought to throw this in a list somewhere, but

print "URL:" , fullurl
print "Current Time:", datetime.datetime.now(), "\n" 

#print infolist
i=0
while i < len(infolist):
  print infolist[i]
  i = i+1

exit()

