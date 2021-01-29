import requests


def fetchResults(startDate,endDate):

    teamRankingUrl='https://delivery.chalk247.com/team_rankings/NFL.json?api_key=74db8efa2a6db279393b433d97c2bc843f8e32b0'
    #getting a response from given url
    response=requests.get(teamRankingUrl)
    #converting data from url into json format
    rankingData=response.json()

    #Making a dictonary with key as team Id and values contain rank, rank points and team name just in case we need it
    #Rounded the points to 2 as required
    teamRankAndPoint=dict()
    for oneDataObj in rankingData['results']['data']:
        teamRankAndPoint[oneDataObj['team_id']]=[oneDataObj['rank'],str(round(float(oneDataObj['adjusted_points']),2)),oneDataObj['team']]
        
    scorecardUrl='https://delivery.chalk247.com/scoreboard/NFL/'+startDate+'/'+endDate+'.json?api_key=74db8efa2a6db279393b433d97c2bc843f8e32b0'
    #getting a response from given url
    response=requests.get(scorecardUrl)
    #converting data from url into json format
    scoreData=response.json()

    #Created an array to hold our results
    finalData=[]

    for eachDate in scoreData['results']:
        oneDateEventsData=scoreData['results'][eachDate]
        if len(oneDateEventsData)!=0:
            for eachEventId in oneDateEventsData['data']:
                oneEventData=oneDateEventsData['data'][eachEventId]
                singleDict=dict()
                singleDict['event_id']=oneEventData['event_id']
                #Used split to seperate Date and Hours
                oldDateFormat=oneEventData['event_date'].split(' ')[0]
                #By using split function changed the format of date as required
                oldDate=oldDateFormat.split('-')
                newDate=oldDate[2]+'-'+oldDate[1]+'-'+oldDate[0]
                singleDict['event_date']=newDate
                singleDict['event_time']=oneEventData['event_date'].split(' ')[1]
                singleDict['away_team_id']=oneEventData['away_team_id']
                singleDict['away_nick_name']=oneEventData['away_nick_name']
                singleDict['away_city']=oneEventData['away_city']
                singleDict['away_rank']=teamRankAndPoint[oneEventData['away_team_id']][0]
                singleDict['away_rank_points']=teamRankAndPoint[oneEventData['away_team_id']][1]
                singleDict['home_team_id']=oneEventData['home_team_id']
                singleDict['home_nick_name']=oneEventData['home_nick_name']
                singleDict['home_city']=oneEventData['home_city']
                singleDict['home_team_id']=oneEventData['home_team_id']
                singleDict['home_rank']=teamRankAndPoint[oneEventData['home_team_id']][0]
                singleDict['home_rank_points']=teamRankAndPoint[oneEventData['home_team_id']][1]
                finalData.append(singleDict)
                
    return finalData
    

if __name__=="__main__":
    #Giving a range of date will be more convinent for the user and change as per required
    
    startDate='2020-01-12'
    endDate='2020-01-19'
    resultsForGivenDates=fetchResults(startDate,endDate)
    print(resultsForGivenDates)