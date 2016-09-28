# -*- coding: utf-8 -*- 
#! /usr/bin/env python
import csv
from bs4 import BeautifulSoup
import requests
import time

MY_URL = "http://inter.if.ua/category/59"

def get_url(url):
    r = requests.get(url)
    return r.content

def get_page(html):
    soup = BeautifulSoup(html, "html.parser")
    num_of_page = soup.find("div", {"class": "total_found"})
    return int(num_of_page.find("b").text)/20 + 1

def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("div", {"class": "rows"})
   
    list_of = []
    
    for row in table.find_all("div", {"class": "row"}):
        cols = row.find_all("div")
        
        list_of.append({
            "title": cols[1].h3.a.text.encode("utf8"),
            "prise": cols[11].span.text.encode("utf8")
            
            })
    return list_of
   
def save_where(list_of, where):
    with open(where, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(("TITLE", "PRISE"))
        for i in list_of:
            writer.writerow((i["title"], i["prise"]))

     
def main():
    total_page = get_page(get_url(MY_URL))
    print "Total pages are %d" %total_page
    list_of = []

    time_start = time.time()
        
    for page in range(1, total_page + 1):
       print "Complete page - %d" % page 
       list_of.extend(parse(get_url(MY_URL + "/sort/title/filter/-,-,-/page/%d" % page)))
        
    save_where(list_of, "list_of.txt")
    
    time_finish = time.time()
    how_long = time_finish - time_start
    print "Scraping is complete, elapsed time are %d seconds" % how_long

   
if __name__== "__main__":
    main()
