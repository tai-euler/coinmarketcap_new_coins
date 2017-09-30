# coding=utf-8
from BeautifulSoup import BeautifulSoup
import urllib2
import re
from random import choice
from bs4 import BeautifulSoup as soup


###--------------------------------------------------------------------------------
user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19',
    'Mozilla/5.0 (X11; Linux x86_64; rv:2.2a1pre) Gecko/20110324 Firefox/4.2a1pre',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b11pre) Gecko/20110128 Firefox/4.0b11pre',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b11pre) Gecko/20110131 Firefox/4.0b11pre',
    'Mozilla/5.0 (X11; Linux i686; rv:2.0b10) Gecko/20100101 Firefox/4.0b10',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:2.0b10) Gecko/20110126 Firefox/4.0b10',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0b10) Gecko/20110126 Firefox/4.0b10',
    'Mozilla/5.0 (X11; U; Linux x86_64; pl-PL; rv:2.0) Gecko/20110307 Firefox/4.0',
    'Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:2.0) Gecko/20110404 Fedora/16-dev Firefox/4.0',
    'Mozilla/5.0 (X11; Arch Linux i686; rv:2.0) Gecko/20110321 Firefox/4.0',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0) Gecko/20110319 Firefox/4.0',
    'Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.2) Gecko/20121223 Ubuntu/9.25 (jaunty) Firefox/3.8',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.3) Gecko/20100401',
    'Mozilla/5.0 (X11; U; Linux i686; it-IT; rv:1.9.0.2) Gecko/2008092313 Ubuntu/9.25 (jaunty) Firefox/3.8',
    'Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.3a5pre) Gecko/20100526 Firefox/3.7a5pre',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2b5) Gecko/20091204 Firefox/3.6b5',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2b5) Gecko/20091204 Firefox/3.6b5',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.9.2b5) Gecko/20091204 Firefox/3.6b5',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2) Gecko/20091218 Firefox 3.6b5',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.9.2b4) Gecko/20091124 Firefox/3.6b4 (.NET CLR 3.5.30729)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2b4) Gecko/20091124 Firefox/3.6b4',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2b1) Gecko/20091014 Firefox/3.6b1 GTB5',
    'Mozilla/5.0 (X11; U; Linux i686; ru-RU; rv:1.9.2a1pre) Gecko/20090405 Ubuntu/9.04 (jaunty) Firefox/3.6a1pre',
    'Mozilla/5.0 (Windows; Windows NT 5.1; es-ES; rv:1.9.2a1pre) Gecko/20090402 Firefox/3.6a1pre',
    'Mozilla/5.0 (Windows; Windows NT 5.1; en-US; rv:1.9.2a1pre) Gecko/20090402 Firefox/3.6a1pre',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2a1pre) Gecko/20090402 Firefox/3.6a1pre (.NET CLR 3.5.30729)',
    'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.9) Gecko/20100915 Gentoo Firefox/3.6.9',
    'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.9.2.9) Gecko/20100913 Firefox/3.6.9',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9 ( .NET CLR 3.5.30729; .NET CLR 4.0.20506)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-GB; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9',
    'Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.9.2.8) Gecko/20101230 Firefox/3.6.8'
]

###--------------------------------------------------------------------------------
# coins we want to find (saved in a array)

searched_coins = ['rivetz', 'ormeus', 'buzzcoin']

###--------------------------------------------------------------------------------
# iterate trough new coins and save their name, abbreviation and date in a array (limit is set to latest 50 coins)

# get the new coins from URL
version = choice(user_agents)
headers = { 'User-Agent' : version }
# and use a random user_agent in GET request
req = urllib2.Request("https://coinmarketcap.com/new", '', headers)
html_page = urllib2.urlopen(req).read()
soup = BeautifulSoup(html_page)

new_coins_data = []

for link in soup.findAll('tbody'):

            # find all 'tr' tags
            for k in link.findAll('tr', limit=50):

                # find all 'td' tags and save in array first 3 elements (limit=3) :
                # name of coin, abbreviation, date added, name of coin, abbreviation, date added...
                for p in k.findAll('td', limit=3):
                    string = str(p.getText())
                    # save string in lower letters into array Rivetz -> rivetz
                    new_coins_data.append(string.lower())
                    #print(len(k))
                    #print(string)

###--------------------------------------------------------------------------------
# helper function to search for the markets for a specific coin
# call url and find market names in html
# save market names in array and return that array

def getMarkets(replacedWhiteSpacesInCoinName):

                        url = "https://coinmarketcap.com/currencies/" + replacedWhiteSpacesInCoinName + "/#markets"
                        marketNamesforCoin = []
                        req2 = urllib2.Request(url)
                        html_page2 = urllib2.urlopen(req2).read()
                        soup2 = BeautifulSoup(html_page2)
                        #print(soup2)
                        for tbody in soup2.findAll('tbody', limit = 1):

                                    print('Exchanges: ')
                                     # find all 'tr' tags
                                    for tr in tbody.findAll('tr'):
                                     # find all 'td' tags
                                     for number, td in enumerate(tr.findAll('td', limit=2)):
                                                # print just exchange names and skip numbers
                                                 if number % 2 is 1:
                                                        element = td.getText()
                                                        marketNamesforCoin.append(str(element))
                                    return marketNamesforCoin

###--------------------------------------------------------------------------------
# iterate trough new coins arrays and find specific coins
# and find their exchanges

for coinName in searched_coins:

        for number, element_from_new_coins_data in enumerate(new_coins_data):


                    if coinName in element_from_new_coins_data:
                                 print('**' + coinName.upper() + ' was added to exchanges')
                                 print(element_from_new_coins_data+ ' (' + new_coins_data[number+1].upper() + ')')
                                 coin_abbr = new_coins_data[number+1]
                                 print(new_coins_data[number+2])
                                 # print(20*'-')

                                 # replace white spaces in coin name "ormeus coin" --> "ormeus-coin"
                                 # this is needed for a proper URL call for the markets later
                                 # example https://coinmarketcap.com/currencies/ormeus-coin/#markets
                                 replacedWhiteSpacesInCoinName = element_from_new_coins_data.replace(" ", "-")

                                 # call helper function to get markets
                                 print(getMarkets(replacedWhiteSpacesInCoinName))


# output example:
#
# **RIVETZ was added to exchanges
# rivetz (RVT)
# 5 days ago
# Exchanges:
# ['EtherDelta', 'HitBTC']
# **ORMEUS was added to exchanges
# ormeus coin (ORME)
# 1 day ago
# Exchanges:
# ['HitBTC', 'Cryptopia']

###--------------------------------------------------------------------------------

