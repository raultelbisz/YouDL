# Program that retrieves one of my playlists on youtube and downloads the
# songs through a third party website to a specified folder on user's computer.
#
#
#
#


import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time


#Asks which playlist you want downloaded
print ('Which playlist do you want to download?')
playlist = input()

#Access my youtube playlists page
driver = webdriver.Chrome(executable_path='E:\chromedriver\chromedriver.exe')
driver.get("https://www.youtube.com/user/raultelbisz/playlists?sort=dd&view=1&shelf_id=0")

#Access the 'classic' playlist
if playlist == 'classic':
    driver.find_element_by_xpath('//a[contains(text(), "classic")]').click()

    #runs the accessed webpage through a parser that gets passed through BS4
    newurl = driver.current_url
    requrl = requests.get(newurl)
    requrlcont = requrl.content

    soup = BeautifulSoup(requrlcont, "html.parser")

    links = [] #create a list to hold all the links
    
    #Find all links to videos in the specific playlist
    for link in soup.find_all('a'):
        #print("link" + str(link))
        if re.match("/watch\?v=", link.get('href')):
            links.append(link.get('href'))

    #Remove duplicate items in the list
    links = list(set(links))

    

    #Access Youtube to mp3 converter third-party website
    dl_tab = driver.get("http://www.youtube-mp3.org/")
    time.sleep(3)#waits for the page to load

    x = 0
    y = len(links)
    

    print (links)

    #This is where you'll have to start your while loop. while x < len(links)
    urlbox = driver.find_element_by_id("youtube-url").clear() #clear preloaded url in box
    urlbox = driver.find_element_by_id("youtube-url")
    urlbox.send_keys("www.youtube.com" + links[1])  #pastes stored url in box
    driver.find_element_by_id("submit").click()

    #error troubleshoot for song
    time.sleep(6) #timer to make sure there is no error with downloading the song
    dl_tab_cur = driver.current_url
    dl_tab_req = requests.get(dl_tab_cur)
    dl_tab_cont = dl_tab_req.content
    error_pars = BeautifulSoup(dl_tab_cont, "html.parser")

    if driver.find_element_by_xpath('//*[contains(text(), "There was an Error")]'): #searches the page for an error message
        driver.find_element_by_id("youtube-url").clear()
    
