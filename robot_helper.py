from urllib.robotparser import RobotFileParser
import requests as rq
rb_txt = dict()

def robot_check(parsed):
    rb_txt[parsed.hostname] = False
    try:
        #construct url to gather robots.txt file
        rb_url = "http://" + parsed.hostname + "/robots.txt"
        sitemap = rq.get(rb_url)

        #if this extension cannot be found, we are allowed to crawl regardless
        if(sitemap.status_code == 200):
            return False
        
        #store the robot information of our constructed url inside rb_parsed
        rb_parsed = RobotFileParser(rb_url) 

        #reads robots.txt and feeds it to our parser
        rb_parsed.read()    

        #returns true if we are allowed to fetch the url according to rules in robots.txt
        if rb_parsed.can_fetch('*', rb_url):    #(useragent,url)
            rb_txt[parsed.hostname] = True

        #if we are allowed to crawl the site, return the hostname of the site
        return rb_txt[parsed.hostname]
        
    except:
        return False