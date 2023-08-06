from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep, strftime
from random import randint,uniform
from datetime import datetime,timedelta
from sys import exit, exc_info, argv
from re import sub, search
from glob import glob
from dateutil.parser import parse
import os
import numbers
import requests


def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False
class Client:
    def __init__ (self, config = {}):
        self.user  = config.get("user", False)
        self.password =  config.get("password", False)
        if not self.user:
            print ("Config is missing 'user'")
            sys.exit()
        if not self.password:
            print ("Config is missing 'password'")
            sys.exit()
        self.hashtag_list = config.get("hashtag_list","photos")
        self.current_hashtag = None
        self.path = os.path.abspath(os.path.dirname(__file__))
        self.debug = settings.get("debug", False)
        self.follow_profiles_list = follow_profiles_list
        #self.chromedriver_path = "/usr/lib/chromium-browser/chromedriver"
        self.likes_max = config.get("likes", 15)
        self.watch_stories_minutes = config.get("watch_stories_min", 5)
        self.follows_max = config.get("follow", 0)
        self.unfollows_max = config.get("unfollow", 0)
        self.wait_between = config.get("wait_between_runs", 2)
        self.api = config.get("api", False)
        self.likes = 0
        self.give_likes_when = config.get("give_likes_when", 0)
        self.follows = 0
        self.follow_recent_liked = 0
        self.unfollows = 0
        self.start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.page_height = 400
        self.profiles_pp = 6
        self.home_screen_likes = 0
        self.followers_count = 0
        self.file_name_time_pattern = datetime.now().strftime("%Y-%m-%d %H")
        self.css_selectors = {
            "home_feed_username":"> header > div.o-MQd.z8cbW > div.RqtMr > div > span > a",
            "home_feed_like_button":"> div.eo2As > section.ltpMr.Slqrh > span.fr66n > button",
            "watch_stories_home_feed":"#react-root > section > main > section > div.cGcGK > div.zGtbP.IPQK5.VideM > div > div > div > div > ul > li:nth-child(3)",
            "watch_stories_hashtag":"#react-root > section > main > header > div > div",##react-root > section > main > header > div.T7reQ._0FuTv.pkWJh
            "unfollow_dialog": "#react-root > section > main > div > header > section > ul > li:nth-child(3) > a",
            "follow_dialog":"#react-root > section > main > div > header > section > ul > li:nth-child(2) > a > span",
            "followers_count":"#react-root > section > main > div > header > section > ul > li:nth-child(2) > a > span",
            "flw_button_zero_scroll":"div div:nth-child(3) button",#follow button
            "flw_button_nonzero_scroll":"div.Pkbci button",
            "flw_profile_name_zero_scroll":"div div:nth-child(2) a",#profile name
            "flw_profile_name_nonzero_scroll":"div.d7ByH a",
            "home_feed_popups":['body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.bIiDR','body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm','#react-root > section > main > div > div > div > div > button'],
            "post_contains_hashtags":"li div.C4VMK",
            "hashtag_next_post":"button.UP43G",
            "hashtag_recent_posts":"#react-root > section > main > article > div:nth-child(3) > div > div:nth-child(3) > div:nth-child(1) > a",
            "hashtag_top_posts":"#react-root > section > main > article > div.EZdmt > div > div > div:nth-child(1) > div:nth-child(1) > a",
            "post_like_dialog":"_1XyCr",
            "follow_post_liked_dialog":"body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div > div",
            "follow_post_liked_dialog_close":"body > div.RnEpo.Yx5HN > div > div > div:nth-child(1) > div > div:nth-child(3) > button",
            "follow_post_liked_dialog_link":"body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > section.EDfFK.ygqzn > div > div > button",
            "follow_post_liked_dialog_profiles":"body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div > div > div"
        
        }
        self.mobile_devices =  {
               "ios": {
                        "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
                        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1"
                },
                "android":{
                        "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
                        "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
                }
        }
        self.mobile = False
        self.post_caption = settings.get("add_to_post_caption")

        if self.follow_profiles_list != None:
            self.followers_window_posY = [0]*len(self.follow_profiles_list)
        
        
        if self.is_runable():
            #switch off the mobile version
            self.mobile = False
            self.print_to_log(self.start + ", ", "log")
            self.wd = self.open_webdriver()
            self.wd.maximize_window()
            self.open_session()
            self.run()
    def get_popup(self):
        for i in range(len(self.css_selectors.get("home_feed_popups"))):
            try:
                popup =  self.wd.find_element_by_css_selector(self.css_selectors.get("home_feed_popups")[i])
                if  popup.is_enabled() and popup.is_displayed():
                    self.log("[get_popup] [found]  selector=" + self.css_selectors.get("home_feed_popups")[i])
                    return popup
            except:
                self.log("[get_popup] [not found, enabled or displayed]  selector=" + self.css_selectors.get("home_feed_popups")[i])
        return False      
    def close_all_popups(self):
        for _ in range(len(self.css_selectors.get("home_feed_popups"))):
            popup = self.get_popup()
            if popup:
                popup.click()
                sleep(5)
        return
             
    def is_non_zero_file(self,fpath):  
        return os.path.isfile(fpath) and os.path.getsize(fpath) > 0
    def is_file(self,fpath):
        return os.path.isfile(fpath)
    def sleepRand (self,max):
        sleep(randint(1,max))

    def open_webdriver (self):
        chrome_options=Options()
        chrome_options.add_argument("headless")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36")
        if self.mobile:
            mobile_emulation = self.mobile
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        else:
            chrome_options.add_argument("--window-size=1920x1080")
        return webdriver.Chrome(executable_path=self.chromedriver_path, chrome_options = chrome_options)
    
    def save_followers_to_file(self,profile,followers_list):
        followers = "\n".join(followers_list)
        f = open(self.path + profile + ".followers", "a")
        if self.is_non_zero_file(self.path + profile + ".followers"):
            f.write("\n")
        f.write (followers) 
        f.close()
        return
    def log(self, message):
        if self.debug == False:
            return
        self.print_to_log(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "  " + message + "\n","debug")
    def print_to_log(self, message, log):
        f = open(self.path + self.user + "." + log, "a")
        f.write (str(message))
        f.close()
        return
    def hours_between(self,d1, d2):
        d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
        d2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
        return round(abs((d2 - d1).total_seconds()/3600),1)
    def is_runable(self):
        userblock_exists = os.path.isfile(self.path  + "block.user")
        log_exists = os.path.isfile(self.path  + self.user + ".log")
        lastRun = False
        if log_exists:
            with open(self.path  + self.user + ".log", "r") as log:
                lines = list(log)
                if len(lines) > 0:
                    lastRun_arr = lines[-1].split(",")
                    if len(lastRun_arr) > 1:# and isinstance(lastRun_arr[2].strip(), numbers.Number):
                        lastRun = lastRun_arr[1].strip()
                        if  lastRun == "":
                            lastRun = lastRun_arr[0].strip()
                            #bot was stuck - reset the bot trigger
                            print(lastRun)
                            if is_date(lastRun)  and self.wait_between > 0 and self.hours_between(str(self.start),lastRun) > self.wait_between:
                                with open(self.path  + self.user + ".log", "a") as f:
                                    f.write("\n")
                                return False
                            else:
                                return False
                        #logged more information than needed - reset the bot trigger
                        elif isinstance(lastRun.strip(), numbers.Number) or len(lastRun_arr) != 6:
                            with open(self.path  + self.user + ".log", "a") as f:
                                f.write("\n")
                            return False
                    else:
                        lastRun = False
                else:
                    lastRun = False
        if lastRun:
            if not (is_date(lastRun) and not isinstance(lastRun.strip(), numbers.Number)):
                return False
            if self.wait_between > 0 and self.hours_between(str(self.start),lastRun) < self.wait_between:
                return False
        if userblock_exists:
            with open(self.path + "block.user") as userblock:
                if self.user in userblock.read(): 
                    return False
        return True
    def open_session(self):
        self.wd.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        self.sleepRand(4)
        self.close_all_popups()
        uname = self.wd.find_element_by_name('username')
        self.send_keys_random_delay(uname, self.user)
        upwd = self.wd.find_element_by_name('password')
        self.send_keys_random_delay(upwd, self.password)
        sleep(2)
        # login
        loginbutton = self.wd.find_element_by_css_selector('button[type=submit].sqdOP.L3NKy.y3zKF')
        loginbutton.click()
        sleep(10)
        #close all after login popups
        self.close_all_popups()
        return
    def send_keys_random_delay(self, controller, keys, min_delay=0.25, max_delay=0.6):
        for key in keys:
            controller.send_keys(key)
            sleep(uniform(min_delay, max_delay))
        return
    def get_profile_indent(self, posY):
        if posY == 0:
            return 1
        else:
            return int((posY / self.page_height) * self.profiles_pp + 1)
    def post_contains_hashtags(self):
        post_hashtags = self.wd.find_element_by_css_selector(self.css_selectors.get("post_contains_hashtags")).text
        
        at_least_found = 0 
        for hashtag in self.hashtag_list:
            found =  search(hashtag, post_hashtags)
            if found and self.current_hashtag != hashtag:
                at_least_found +=1
        if (at_least_found >= self.give_likes_when):
            self.log("[post_contains_hashtags] post_hashtags=" + str(post_hashtags) + " return=True")
            return True
        else:
            self.log("[post_contains_hashtags] post_hashtags=" + str(post_hashtags) + " return=True")
            return False

    def set_profiles_posY(self, posY= 0, operation = "follow"):
        button_label = "Follow"
        if operation == "unfollow":
            button_label = "Following"
        try:
            flw_button_selector =  self.css_selectors.get("flw_button_nonzero_scroll")
            profile_name_selector = self.css_selectors.get("flw_profile_name_nonzero_scroll")
            if posY == 0:
                flw_button_selector =  self.css_selectors.get("flw_button_zero_scroll")
                profile_name_selector = self.css_selectors.get("flw_profile_name_zero_scroll")
            
            loop = True
            dialog = self.wd.find_element_by_css_selector('div.isgrP')
            indent = self.get_profile_indent(posY)
            self.log("[set_profiles_posY]   indent_init=" + str(indent))
            if posY != 0:
                posY_temp = 0
                for i in range(int(posY / self.page_height)):
                    self.log("[set_profiles_posY] scroll_to_pos_y="+ str(posY))
                    posY_temp += self.page_height
                    self.wd.execute_script("arguments[0].scrollTop = " + str(posY_temp), dialog)
                    sleep(2)
            while loop:
                profiles_discovered = 0
                
                for i in range(self.profiles_pp):
                    self.log('[set_profiles_posY]  fb_selector= ul li:nth-child(' + str(i + indent) + ') ' + flw_button_selector)
                    self.log('[set_profiles_posY]  fp_selector= ul li:nth-child(' + str(i + indent) + ') ' + profile_name_selector)
                    
                    follower = self.wd.find_element_by_css_selector('ul li:nth-child(' + str(i + indent) + ') ' + flw_button_selector)
                    follower_name = self.wd.find_element_by_css_selector('ul li:nth-child(' + str(i + indent) + ') ' + profile_name_selector).text
                    if follower.text == button_label:
                        if operation == "unfollow" and self.already_followed(follower_name,"followers.lock"):
                            continue
                        profiles_discovered += 1
                self.log("[set_profiles_posY]   profiles_discovered="+ str(profiles_discovered))
                if profiles_discovered*2 >= self.profiles_pp:
                    loop = False
                else:
                    posY += self.page_height
                    #page scrolled change button selector
                    flw_button_selector =  self.css_selectors.get("flw_button_nonzero_scroll")
                    profile_name_selector = self.css_selectors.get("flw_profile_name_nonzero_scroll")
                    
                    self.wd.execute_script("arguments[0].scrollTop = " + str(posY), dialog)
                    
                    #increase indent
                    self.log("[set_profiles_posY]   new_indent=" + str(int((posY/ self.page_height) * self.profiles_pp + 1)))
                    indent = int((posY / self.page_height) * self.profiles_pp + 1)
                    sleep(2)
            return posY
        except:
            self.parse_error("[handle_followers] [set_profiles_posY] [" + operation + "] [" + str(exc_info()[0]) + "] " + str(exc_info()[1]))
            return 0
    def open_profile(self, username):
        username = str(username)
        if username not in self.wd.current_url:
            self.navigate_to('https://www.instagram.com/' + username)
        return
    def next_post (self,sleep_for = 7):
        try:
            sleep(1)
            self.log("[next_post] likes_given=" + str(self.likes) + ", follows_given=" + str(self.follows))
            next = self.wd.find_element_by_link_text('Next')
            next.click()
            sleep(sleep_for)
            return True
        except:
            self.parse_error("[run] [next_button]" + str(exc_info()[1]))
            return False
    def open_hashtag(self, hashtag):
        hashtag =  str(hashtag)
        if hashtag not in self.wd.current_url:
            self.navigate_to('https://www.instagram.com/explore/tags/' + hashtag)
            sleep(3)
        return  self.wd.current_url
    def open_hashtag_recent_post(self, hashtag):
        self.open_hashtag(hashtag)
        rp_selector = self.css_selectors.get("hashtag_recent_posts")
        first_thumbnail = self.wd.find_element_by_css_selector(rp_selector)
        first_thumbnail.click()
        sleep(7)
        return
    def follow_hashtag_recent_post(self, min_likes = 10):
        if self.hashtag_list==None or self.follows_max == 0:
            return
        loop = True
        
        self.open_hashtag_recent_post(self.hashtag_list[0])

        while loop:
            try:          
                likes = self.wd.find_element_by_css_selector(self.css_selectors.get("follow_post_liked_dialog_link"))
                if  likes.text != "like this":
                    likes.click()
                    sleep(5)
                    dialog = self.wd.find_element_by_css_selector(self.css_selectors.get("follow_post_liked_dialog"))
                    self.wd.execute_script("arguments[0].scrollTop = 100" , dialog)
                    profiles = self.wd.find_elements_by_css_selector(self.css_selectors.get("follow_post_liked_dialog_profiles")) 
                    if len(profiles) > min_likes:
                        loop = False
                        for i in range(self.follows_max):
                            profile_follow = self.wd.find_element_by_css_selector(self.css_selectors.get("follow_post_liked_dialog_profiles")+":nth-child(" + str(i+1) + ") div:nth-child(3) button")
                            profile_name = self.wd.find_element_by_css_selector(self.css_selectors.get("follow_post_liked_dialog_profiles")+":nth-child(" + str(i+1) + ") div:nth-child(2) div div span a").text
                            if (profile_follow.text == "Follow"):
                                profile_follow.click()
                                self.follow_recent_liked += 1
                                self.print_to_log(message=profile_name + "\n",log="followed.lock")
                                sleep(2)
                    else:
                        close = self.wd.find_element_by_css_selector(self.css_selectors.get("follow_post_liked_dialog_close"))
                        close.click()
                        sleep(1)
                if loop == True: self.next_post()
            except NoSuchElementException:
                #do nothing
                if loop == True: self.next_post()
            except:
                self.parse_error("[follow_hashtag_recent_post] [" + str(exc_info()[0]) + "] " + str(exc_info()[1]))
                loop = False
        return



    def handle_followers(self,operation= "follow"):
        if operation == "follow" and (self.follow_profiles_list == None or self.follows_max == 0):
            return
        profiles_list = None
        if operation == "follow":
            profiles_list =  self.follow_profiles_list
        stop = len(profiles_list) if profiles_list != None  else 1
        posY = 0
        # actions_max = int(self.follows_max/2)
        # actions_min =  2
        loop = True
        while loop:
            actions_taken = 0
            #create array of zeroes           
            for _ in range(stop):
                #get random index so we follow equally all followers of set profiles
                try:
                    if operation == "follow" and self.follows == self.follows_max:
                        break
                    if operation == "unfollow" and self.unfollows == self.unfollows_max:
                        break
                    if operation == "follow":
                        profile_index = randint(0, len(profiles_list)-1)
                        posY = self.followers_window_posY[profile_index]
                        self.open_profile(profiles_list[profile_index])
                    
                    
                    followersDialog = self.wd.find_element_by_css_selector(self.css_selectors.get(operation + "_dialog"))
                    #followers_total = int(followersDialog.text)
                    followersDialog.click()
                    sleep(5)
        
                    posY = self.set_profiles_posY(posY, operation)
                    indent = self.get_profile_indent(posY)
                    
                    if operation == "follow":
                        self.followers_window_posY[profile_index] = posY

                    self.log("[handle_followers] actual_indent="+ str(indent))
                    
                    sleep(3)
                    
                    for i in range(randint(3,5)):
                        if operation == "follow" and self.follows == self.follows_max:
                            break
                        if operation == "unfollow" and self.unfollows == self.unfollows_max:
                            break
                            
                        #html markup changes when scrolling
                       
                        flw_button_selector = self.css_selectors.get("flw_button_nonzero_scroll")
                        profile_name_selector = self.css_selectors.get("flw_profile_name_nonzero_scroll")
                        if posY == 0:
                           flw_button_selector =  self.css_selectors.get("flw_button_zero_scroll")
                           profile_name_selector = self.css_selectors.get("flw_profile_name_zero_scroll")
                           
                        follower = self.wd.find_element_by_css_selector('ul li:nth-child(' + str(indent+i) + ') ' + flw_button_selector)
                        follower_name =   self.wd.find_element_by_css_selector('ul li:nth-child(' + str(indent+i) + ') ' + profile_name_selector).text
                        self.log("[handle_followers]    actual_profile_selector="+ str('ul li:nth-child(' + str(indent+i) + ') ' + flw_button_selector))
                        self.log("[handle_followers]    actual_profile_name="+ str(follower_name))
                        
                        if operation == "follow"  and follower.text == "Follow" and self.follows <= self.follows_max and not(self.already_followed(follower_name,"followers.lock") or self.already_followed(follower_name,"followed.lock")):
                            follower.click()
                            self.follows += 1
                            actions_taken += 1
                            self.print_to_log(message=follower_name + "\n",log="followed.lock")
                            sleep(2)
                        if operation == "unfollow" and follower.text == "Following" and self.unfollows <= self.unfollows_max and not(self.already_followed(follower_name,"followers.lock")):
                            follower.click()
                            sleep(2)

                            confirm_unfollow = self.wd.find_element_by_css_selector('.mt3GC button:nth-child(1)')
                            confirm_unfollow.click()

                            self.unfollows += 1
                            actions_taken += 1
                            self.print_to_log(message=follower_name + "\n",log="followers.lock")
                            sleep(2)
                    if operation == "follow":       
                        self.followers_window_posY[profile_index] += self.page_height
                    else:
                        posY += self.page_height    
                except:
                    self.parse_error("[handle_followers] [" + operation + "] [" + str(exc_info()[0]) + "] " + str(exc_info()[1]))  
            if (operation == "follow" or operation == "follow_post_liked") and actions_taken == 0 or self.follows >= self.follows_max:
                loop = False
            if operation == "unfollow" and actions_taken == 0 or self.unfollows >= self.unfollows_max:
                loop = False
        self.navigate_to()
        return 
    def already_followed(self, username, log):
        user_follow_log_exists = os.path.isfile(self.path  + self.user + "." + log)
        if user_follow_log_exists:
            with open(self.path  + self.user + "." + log) as user_follow_log:
                if username in user_follow_log.read(): 
                    return True
        return False      
       
    def like_home_feed_photos(self, max = 10):
        if self.wd.current_url != 'https://instagram.com':
            self.navigate_to()
        #posY = 100
        #body = self.wd.find_element_by_tag_name("body")
        for i in range(randint(4,max)):
            ##react-root > section > main > section > div.cGcGK > div:nth-child(2) > div > article:nth-child(1) > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button
            ##react-root > section > main > section > div.cGcGK > div:nth-child(2) > div > article:nth-child(1) > header > div.o-MQd.z8cbW > div.RqtMr > div > span > a
            try:
                username = self.wd.find_element_by_css_selector('#react-root > section > main > section > div.cGcGK > div:nth-child(2) > div > article:nth-child(' + str(i+1) + ') ' + self.css_selectors.get('home_feed_username'))
                if username.text != self.user:
                    likeButton = self.wd.find_element_by_css_selector('#react-root > section > main > section > div.cGcGK > div:nth-child(2) > div > article:nth-child(' + str(i+1) + ') ' + self.css_selectors.get('home_feed_like_button'))
                    if likeButton.find_element_by_tag_name('svg').get_attribute("aria-label") == "Like":
                        likeButton.click()
                        self.home_screen_likes +=1
                    #self.wd.execute_script("arguments[0].scrollTop = " + str(posY), body)
                    sleep(2)
                    #posY+=100
            except:
                self.parse_error("[like_home_feed_photos] [" + str(exc_info()[0]) + "] " + str(exc_info()[1])) 
        self.navigate_to()         
        return   
    def watch_stories(self, story_type = None, redirect_to = False):
        sleep(2)
        try:
            if self.watch_stories_minutes == 0 or story_type == None:
                return 
            watchallButton = self.wd.find_element_by_css_selector(self.css_selectors.get("watch_stories_" + story_type))
            watchallButton.click()
            #let it load
            sleep(3)

            #if stories are not long as the setting  watch_stories_minutes finish earlier when url changes
            self.log("[watch_stories]   first_url:"+ self.wd.current_url)
            for _ in range(self.watch_stories_minutes):
                sleep(60)
                self.log("[watch_stories]   url_after_sleep=" + self.wd.current_url)
                if not "stories" in self.wd.current_url:
                    break
        except:
            self.parse_error("[watch_stories]   [" + story_type + "] [" + str(exc_info()[0]) + "] " + str(exc_info()[1]))
        self.navigate_to(redirect_to)
        return  
    def navigate_to(self, url= False):
        if not(url):
            url = 'https://www.instagram.com/'
        self.wd.get(url)
        sleep(5)
        #sometimes there is a popup 
        self.close_all_popups()
        return 
    def parse_error (self, error):
        self.print_to_log(message=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "," + error + "\n", log='error')
        block = False#search("element not interactable", error)
        if block:
            self.block_user()
            #self.print_to_log(message= self.start + ", " + str(self.likes) + ", " + str(self.follows) + ", " + str(self.unfollows), log = 'log')
            self.wd.quit()
            exit()
        return
    def block_user (self):
        f = open(self.path +  "block.user", "a")
        if self.is_non_zero_file(self.path +  "block.user"):
            f.write("\n")
        f.write (str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "," + self.user)
        f.close()
        return
    
    #mobile device functions
    def go_back(self):
        self.wd.find_element_by_css_selector('.Iazdo').click()
        sleep(5)
        self.wd.find_element_by_css_selector('div.Nnq7C.weEfm:nth-child(' + str(randint(4, 15)) + ') div a').click()
        sleep(5)
        return
    def upload_photos_available(self):
        try:
            os.chdir(self.path + self.user)
            for _ in glob(self.file_name_time_pattern + '*'):
                return True
        except:
            return False
        return False
    
    def ig_new_line(self):
        for _ in range(3):
            self.keyboard.press(Key.shift)
            sleep(0.1)
            self.keyboard.press(Key.enter)
            sleep(0.1)
            self.keyboard.release(Key.enter)
            sleep(0.1)
            self.keyboard.release(Key.shift)
            sleep(0.5)
        return
    def ensure_dir(self, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return
    def set_followers_count (self):
        try:
            self.navigate_to('https://www.instagram.com/' + self.user)
            followers_count =  self.wd.find_element_by_css_selector(self.css_selectors.get("followers_count")).text
            self.followers_count = followers_count.replace(",","")
        except:
            self.parse_error("[get_followers_count] [" + str(exc_info()[0]) + "] " + str(exc_info()[1]))

    def send_data(self):
        URL = "https://daboi.memews.com/sys/write.php"
        if not self.api:
            return
        PARAMS = {"q":self.api, "data": self.start +"," + self.end + "," + str(self.followers_count) + "," + str(self.home_screen_likes + self.likes) + "," + str(self.follows + self.follow_recent_liked) + "," + str(self.unfollows) + ",11"}
        r = requests.get(url = URL,params = PARAMS)

    def run (self):
        try:
            loop_num = 0
            loop = True
            # reach_max = int(self.likes_max/len(self.hashtag_list)/2)
            # reach_min = int(reach_max/2)
            self.set_followers_count()
            #unfollow / follow profiles 
            self.handle_followers("unfollow")
            self.handle_followers("follow")
            #follow profiles who liked a photo on hashtag recent posts with at least 10 follows
            self.follow_hashtag_recent_post()
            
            #like home feed photos
            self.like_home_feed_photos()

            #watch home feed stories
            self.watch_stories(story_type = "home_feed")
           
            
            while loop:
                actions_taken = 0
                #like your own feed
                for i in range(len(self.hashtag_list)):
                    self.current_hashtag = self.hashtag_list[i]
                    if self.likes == self.likes_max:
                        break
                    url = self.open_hashtag(self.current_hashtag)
                    
                    if loop_num == 0:
                        #watch hashtag stories
                        self.watch_stories(story_type = "hashtag",redirect_to=url)
                    self.open_hashtag_recent_post(self.current_hashtag)
                    sleep(3)
                    for _ in range(10 + len(self.hashtag_list) - i, 20 + len(self.hashtag_list) - i ):
                        try:
                            followButton = self.wd.find_element_by_css_selector('div.bY2yH button')
                            if self.follows_max > 10:
                                limit = 5
                            else:
                                limit = 7

                            if randint(0,10) >= limit and followButton.text == 'Follow' and self.follows_max > 0 and self.follows_max > self.follows and self.follow_profiles_list == None:
                                followButton.click()
                                self.follows += 1
                                actions_taken += 1
                                sleep(3)
                        except:
                            # sometimes it freezes and the program crashes this is error handler to catch it and continue on the like spree
                            # unless they will block us which will be saved in the error log as well and we will not continue in the spree 
                            self.parse_error("[action_follow] [" + str(exc_info()[0]) + "] " + str(exc_info()[1]))    
                   
                        # Liking the picture
                        try:
                            if  randint(0,10) >= 4 and self.likes_max > self.likes:
                                likeButton = self.wd.find_element_by_css_selector('span.fr66n button')
                                if likeButton.find_element_by_tag_name('svg').get_attribute("aria-label") == "Like":
                                    if self.give_likes_when > 0:
                                        if  self.post_contains_hashtags():
                                            likeButton.click()
                                            self.likes += 1
                                            actions_taken += 1
                                            sleep(3)
                                    else:
                                        likeButton.click()
                                        self.likes += 1
                                        actions_taken += 1
                                        sleep(3)
                        except:
                            # sometimes it freezes and the program crashes this is error handler to catch it and continue on the like spree
                            # unless they will block us which will be saved in the error log as well and we will not continue in the spree 
                            self.parse_error("[action_like] [" + str(exc_info()[0]) + "] " + str(exc_info()[1]))
                        
                        # Next picture
                        if self.next_post() == False: break
                       
                if (self.likes >= self.likes_max and self.follows >= self.follows_max) or actions_taken == 0:
                    loop = False
                else:
                    #after every hashtag visit like some home feed photos
                    self.like_home_feed_photos(max = 5)
                    loop_num +=1
            
            #last time like home screen photos
            self.like_home_feed_photos(max = 5)
        except:
            # sometimes it freezes and the program crashes this is error handler to catch it and continue on the like spree
            # unless they will block us which will be saved in the error log as well and we will not continue in the spree 
            self.parse_error("[run] [" + str(exc_info()[0]) + "] " + str(exc_info()[1]))
        #close session
        self.wd.quit()
        self.end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.send_data()
        self.print_to_log(message= self.end + ", " + str(self.followers_count) + ", " + str(self.home_screen_likes) + " + " + str(self.likes) + ", " + str(self.follows) + " + " + str(self.follow_recent_liked) + ", " + str(self.unfollows) + "\n", log = 'log')
        return

