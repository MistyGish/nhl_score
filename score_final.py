import json
from time import sleep
import sys
import requests
import datetime
import os
import itertools 
import argparse
import pprint
from gpiozero import LED
 
# creating game data
class Game:
    def __init__(self,game_info):
        self.link = game_info['link']
        self.date = game_info['gameDate']
        self.away = game_info['teams']['away']['team']['name']
        self.home = game_info['teams']['home']['team']['name']

def main():

    team = "Toronto Maple Leafs"
    game = get_games(team)
    try:
        live = get_live(game.link)
    except:
        print("No game today... :(")
    allPlays = 0
    start_scoreHome = 0
    start_scoreAway = 0

    if True:
        print("It's game day! Go Leafs Go!")

    # loop to print 
    while True:
        try:
            data = get_data(live)
            plays = data['liveData']['plays']['allPlays']

            # get current score and team names
            home_score = data['liveData']['linescore']['teams']['home']['goals']
            away_score = data['liveData']['linescore']['teams']['away']['goals']
            home_team = data['liveData']['linescore']['teams']['home']['team']['name']
            away_team = data['liveData']['linescore']['teams']['away']['team']['name']

            

            # check for goals
            if len(plays) > allPlays:
                allPlays = len(plays)
                #print(plays[len(plays) - 1])
                #print(datetime.datetime.now().time())
                currentPlay = plays[len(plays) - 1]

                if currentPlay['result']['event'] == "Goal" and currentPlay['team']['name'] == team:
                    goal()

            # print any score updates
            if home_score > start_scoreHome:
                start_scoreHome = home_score
                print(home_team + ": " + str(home_score))
                print(away_team + ": " + str(away_score))

            elif away_score > start_scoreAway:
                start_scoreAway = away_score
                print(home_team + ": " + str(home_score))
                print(away_team + ": " + str(away_score))
            
            # else:
            #     print(home_team + ": 0")
            #     print(away_team + ": 0")
                


                    

        except KeyboardInterrupt:
            print("No game today... :(")
            os._exit(0)

# retrieves game data
def get_games(team):
    data = get_data("https://statsapi.web.nhl.com/api/v1/schedule")

    for game_info in data['dates'][0]['games']:
        game = Game(game_info)

        if team in game.away or team in game.home:
            return game

# retrieve JSON response
def get_data(url):
    response = (requests.get(url)).json()
    #formatted_response = json.dumps(response.get(url).json(), indent = 4)
    return response

# create a game's live feed link
def get_live(url):
    default = "https://statsapi.web.nhl.com"
    liveURL = default + url
    return liveURL

# run goal notification (light change in future)
def goal():

    red = LED(18)
    white = LED(23)
    
    for x in range(0,4):
        print("GOAL!")
        
        red.on()
        sleep(.05)
        red.off()
        sleep(.05)
        white.on()
        sleep(.05)
        white.off()
        sleep(.05)
        red.on()
        sleep(.05)
        red.off()
        sleep(.01)
        white.on()
        sleep(.05)
        white.off()
        sleep(.05)
        red.on()
        sleep(.05)
        red.off()
        sleep(.05)
        white.on()
        sleep(.05)
        white.off()
        sleep(.05)

def gameLED():
    green = LED()
    
    while True:
        green.on()
        


if __name__ == "__main__":
    main()
