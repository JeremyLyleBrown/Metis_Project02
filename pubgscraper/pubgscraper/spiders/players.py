import scrapy
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import pickle

class PlayerSpider(scrapy.Spider):

    name = 'pubg_players'

    custom_settings = {
        "DOWNLOAD_DELAY": 1,# temporary - hopefully I don't get kicked!
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'https://pubgtracker.com/leaderboards/pc/Rating?page=%s&mode=1&region=1' % page for page in range(1,201)#1811
    ]
    # https://pubgtracker.com/leaderboards/pc/Rating?page=1810&mode=1&region=1
    # end of player list for NA region, Solo mode


    def __init__(self):
        chromedriver = "/Applications/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

    def parse(self, response):

        player_names = response.xpath('//tbody/tr/td/a/text()').extract()

        for p in player_names:
            yield scrapy.Request(
                url = ('https://pubgtracker.com/profile/pc/' + p + '/solo?region=na'),# need to generate urls based on player names
                callback=self.parse_player
            )

    def parse_player(self, response):

        self.driver.get(response.url)

        url = response.url

        timesurvived = self.driver.find_elements_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Time Survived")]/../span[@class="value"]')[0].text
        roundsplayed = self.driver.find_element_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Rounds Played")]/../span[@class="value"]').text
        wins = self.driver.find_element_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Wins")]/../span[@class="value"]').text
        toptens = self.driver.find_elements_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Top 10s")]/../span[@class="value"]')[0].text
        losses = self.driver.find_element_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Losses")]/../span[@class="value"]').text
        kills = self.driver.find_elements_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Kills")]/../span[@class="value"]')[4].text
        assists = self.driver.find_element_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Assists")]/../span[@class="value"]').text
        suicides = self.driver.find_element_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Suicides")]/../span[@class="value"]').text
        headshotkills = self.driver.find_elements_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Headshot Kills")]/../span[@class="value"]')[1].text
        vehicledestroys = self.driver.find_element_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Vehicle Destroys")]/../span[@class="value"]').text
        roadkills = self.driver.find_elements_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Road Kills")]/../span[@class="value"]')[1].text
        dailykills = self.driver.find_element_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Daily Kills")]/../span[@class="value"]').text
        weeklykills = self.driver.find_element_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Weekly Kills")]/../span[@class="value"]').text
        roundmostkills = self.driver.find_element_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Round Most Kills")]/../span[@class="value"]').text
        maxkillstreaks = self.driver.find_element_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Max Kill Streaks")]/../span[@class="value"]').text
        days = self.driver.find_element_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Days")]/../span[@class="value"]').text
        longesttimesurvived = self.driver.find_element_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Longest Time Survived")]/../span[@class="value"]').text
        walkdistance = self.driver.find_elements_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Walk Distance")]/../span[@class="value"]')[0].text
        ridedistance = self.driver.find_elements_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Ride Distance")]/../span[@class="value"]')[0].text
        longestkill = self.driver.find_element_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Longest Kill")]/../span[@class="value"]').text
        heals = self.driver.find_elements_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Heals")]/../span[@class="value"]')[1].text
        boosts = self.driver.find_element_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Boosts")]/../span[@class="value"]').text
        damagedealt = self.driver.find_element_by_xpath('//div[@class="pubg-overview-item"]//*[contains(text(), "Damage Dealt")]/../span[@class="value"]').text

        data = {
            "url" : url,
            "Time_Survived" : timesurvived,
            "Rounds_Played" : roundsplayed,
            "Wins" : wins,
            "Top_10s" : toptens,
            "Losses" : losses,
            "Kills" : kills,
            "Assists" : assists,
            "Suicides" : suicides,
            "Headshot_Kills" : headshotkills,
            "Vehicle_Destroys" : vehicledestroys,
            "Road_Kills" : roadkills,
            "Daily_Kills" : dailykills,
            "Weekly_Kills" : weeklykills,
            "Round_Most_Kills" : roundmostkills,
            "Max_Kill_Streaks" : maxkillstreaks,
            "Days" : days,
            "Longest_Time_Survived" : longesttimesurvived,
            "Walk_Distance" : walkdistance,
            "Ride_Distance" : ridedistance,
            "Longest_Kill" : longestkill,
            "Heals" : heals,
            "Boosts" : boosts,
            "Damage_Dealt" : damagedealt
        }

        # use try except
        try:
            with open("my_data.pkl", 'rb') as picklefile:
                my_old_data = pickle.load(picklefile)
        except:
            my_old_data = []

        my_old_data.append(data)

        with open('my_data.pkl', 'wb') as picklefile:
            pickle.dump(my_old_data, picklefile)

        yield data
