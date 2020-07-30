import time
import urllib
import requests
import jira.client
from jira.client import JIRA
from selenium import webdriver

s = requests.Session() #idk just in case
s.headers.update({
        'Referer': 'http://www.linkedin.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    })

driver = webdriver.Chrome('/Users/max/Downloads/chromedriver')   #linkedin login
driver.get('https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fmwlite%2F&fromSignIn=true&trk=uno-reg-join-sign-in')
username = driver.find_element_by_id('username')
username.send_keys('email')

password = driver.find_element_by_id('password')
password.send_keys('password')

log_in_button = driver.find_element_by_class_name('btn__primary--large.from__button--floating')   #linkedin search
log_in_button.click()
search = driver.find_element_by_id('search-input')
search.send_keys('itiviti'+'\n')

time.sleep(0.5)
from parsel import Selector
driver.page_source
names = driver.find_elements_by_class_name('large-semibold.name') #getting names
names = [name.text for name in names]
print(names)

names1=(','.join(names))   #comma-separated names
print(names1)

fl = open("names.txt", "w") #writing comma-separated names in file
fl.write(names1)
fl.close()


with open('names.txt') as file:
    for line in file.readlines():
     name = line.split(",")
     name1=('\n'.join(name)) #creating readable names
     print(name1)
     fl = open("name1.txt","w")
     fl.write((name1).strip(' ')) #deleting spaces and writing in file
     fl.close()
     file.close()




with open('name1.txt') as file:
    for line in file.readlines():
     name,surname = line.split(" ") #separating name and surname
     email=name+"."+surname[:-4]+"@pochta.ru" #creating email adress
     fullname=line[:-4] #deleting 1st and 2nd words from surname 
     fullmail=(''.join(email.split())) #creating full email
     full=(''.join((fullname).strip('\n')+","+fullmail))
     print(full)
     fl = open("nameemail.txt", "a") #creating file with names and emails of users
     fl.write(full)
     fl.write('\n')
     fl.close()
     fl = open("cleanname.txt", "a") #creating of file with clean names for further use
     fl.write(fullname+",")
     #fl.write('\n')
     fl.close()

with open('cleanname.txt') as file: #other clean names file creating
    for line in file.readlines():
     name = line.split(",")
     name1=('\n'.join(name))
     print(name1)
     fl = open("fullcleanname.txt","w")
     fl.write((name1).strip(' ')) #deleting of spaces and writing in new file
     fl.close()
     file.close()


img = driver.find_elements_by_class_name('person-entity-medium') #selenium image finder
i=0

with open('cleanname.txt') as file: #avatar download and renaming to users names 
 for line in file.readlines():
     line[:-1]
     name = line.split(",")
     for myimg in img:
         src=myimg.get_attribute('src')
         p = requests.get(src)
         str(i)
         name2=name[i]+".jpg"
         i=i+1
         out = open(name2, "wb")
         out.write(p.content)
         out.close()


time.sleep(5) #just in case of lags

#---------------------------------------------------------------------
#----------------------------Jira part--------------------------------
#---------------------------------------------------------------------

print('start user add script')  #jira login
api_token = 'admin'
options = {'server' : 'http://localhost:2990/jira/'}
jira = JIRA(
  options, 
   basic_auth=('admin', api_token))

with open('nameemail.txt') as file:   #jira add user
 for line in file.readlines():
     name, email = line.split(",")
     print(name,email)
     full=name
     jira.add_user(name, email, fullname=name)


with open('fullcleanname.txt') as file:  #unpacking file with names, creating Jira user links and avatar download
    for line in file.readlines():
         name, surname = line.split(' ')
         namelink = name + "+" + surname  #creating jira user login for link
         driver = webdriver.Chrome('/Users/max/Downloads/chromedriver')
         link = ('http://localhost:2990/jira/secure/ViewProfile.jspa?atl_token=BWP3-NZB2-6EDY-6C7K%7C06d1e5c3cbde8d81f62871a2e0753d3295b147c5%7Clin&name='+namelink)
         driver.get(link)
         username = driver.find_element_by_id('login-form-username') #login to jira 
         username.send_keys('admin')
         password = driver.find_element_by_id('login-form-password')
         password.send_keys('admin')
         log_in_button = driver.find_element_by_id('login-form-submit')
         log_in_button.click()
         time.sleep(0.5)
         avatar = driver.find_element_by_id('details-user-avatar-trigger') #avatar change
         avatar.click()
         time.sleep(0.5)
         img_name = (name + " " + surname[:-1] + ".jpg") #generating name for Selenium downloaded user jpg photo
         img_path = ("/Users/max/Desktop/scripts/" + img_name) #generating path of user photo
         driver.find_element_by_id('jira-avatar-uploader').send_keys(img_path); #send user photo path to the 'input' element
         time.sleep(0.5)
         submit = driver.find_element_by_class_name('aui-button.aui-button-primary') #submit button search
         submit.click()
         time.sleep(2)
         driver.close()