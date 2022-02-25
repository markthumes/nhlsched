import sys
import requests
import json
import io

class Team:
	def __init__(self, name, wins, losses, games, sos):
		self.name = name;
		self.wins = wins;
		self.losses = losses;
		self.games = games;
		self.sos = sos; # strength of schedule

par = {
	"startDate": "2022-04-4",
	"endDate": "2022-04-17",
}

url_base="https://statsapi.web.nhl.com/api/v1/"

url = url_base + "schedule";

r = requests.get(url, params=par);

schedule = r.json();
#print(json.dumps(schedule))

schedule["copyright"] = "Hello World";

#Get all team names

par = {
	"expand" : "team.stats"
}

url = url_base + "teams";
r = requests.get(url, params=par);
ret = r.json();


teams = []
for t in ret["teams"]:
	n = t["name"];
	w = t["teamStats"][0]["splits"][0]["stat"]["wins"];
	l = t["teamStats"][0]["splits"][0]["stat"]["losses"];
	teams.append(Team(n,w,l,0,0))

#Print teams schedule
for dates in schedule["dates"]:
	for games in dates["games"]:
		away = Team("",0,0,0,0);
		home = Team("",0,0,0,0);
		away.name = games["teams"]["away"]["team"]["name"];
		home.name = games["teams"]["home"]["team"]["name"];
		away.wins = games["teams"]["away"]["leagueRecord"]["wins"];
		home.wins = games["teams"]["home"]["leagueRecord"]["wins"];
		for t in teams:
			if( t.name == home.name ):
				t.games += 1;
				t.sos += away.wins;
			if( t.name == away.name ):
				t.games += 1;
				t.sos += home.wins;

print( "Team, Games, Strength" );
for t in teams:
	t.sos = t.wins / ( t.sos / t.games )
	print( t.name + ", " + str(t.games) + ", " + str(t.sos) )
