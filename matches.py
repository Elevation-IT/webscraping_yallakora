import requests
from bs4 import BeautifulSoup
import csv
import lxml

date = input("Please enter a date with the following format MM/DD/YYYY: ")
page = requests.get(f'https://www.yallakora.com/match-center/?date={date}')

def main(page):
    src = page.content
    soup = BeautifulSoup(src , "lxml")
    matches_details = []
    championships = soup.find_all("div" , {'class' : 'matchCard'})

    def get_details(championships):
        champion_title = championships.find("h2").text.strip()
        all_matches = championships.contents[3].find_all("div" , {'class' : 'liItem'})
        num_of_matches = len(all_matches)
        #print(num_of_matches)

        for i in range(num_of_matches):
            #Teams Name
            teamA = all_matches[i].find("div" , {'class' : 'teamA'}).text.strip()
            teamB = all_matches[i].find("div" , {'class' : 'teamB'}).text.strip()
            #Match Result
            match_result = all_matches[i].find("div" , {'class' : 'MResult'}).find_all("span" , {'class' : 'score'})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"
            #Match Time
            match_time = all_matches[i].find("div" , {'class' : 'MResult'}).find("span" , {'class' : 'time'}).text.strip()
            matches_details.append({"نوع البطولة" : champion_title ,
                                    "الفريق الاول" : teamA ,
                                    "الفريق الثاني" : teamB ,
                                    "ميعاد المباراة" : match_time ,
                                    "النتيجة" : score})

    #get all championships and pass to method get_details to get all matches for each championship
    for i in range(len(championships)):
        get_details(championships[i])
    
    #pass data to csv file
    keys = matches_details[0].keys()
    with open('yallakora.csv' , 'w', encoding="utf-8") as f:
        dic_writer = csv.DictWriter(f , keys)
        dic_writer.writeheader()
        dic_writer.writerows(matches_details)
        print("File Saved!")

main(page)