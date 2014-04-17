import random

class Team:
  def __init__(self, name, wins, winpct):
    self.name = name
    self.wins = wins
    self.winpct = winpct
	
  def get_name(self):
    return self.name
	
  def get_wins(self):
    return self.wins
	
  def get_winpct(self):
    return self.winpct
	
class Game:
  def __init__(self, team1, team2):
    self.team1 = team1
    self.team2 = team2
	
  def run(self, home_court):
    #compute probability of team1 winning
    a = self.team1.get_winpct() * (1.0-self.team2.get_winpct())
    b = (1.0-self.team1.get_winpct()) * self.team2.get_winpct()
    team1pct = a/(a+b)
    if home_court == 1:
      team1pct += 0.1
    else:
      team1pct -= 0.1
    rand = random.random()
    if rand < team1pct:
      return self.team1.get_name()
    else:
      return self.team2.get_name()
	
class Series:
  def __init__(self, team1, team2):
    self.team1 = team1
    self.team2 = team2

  def run(self):
    team1wins = 0
    team2wins = 0
    game_number = 1
    game = Game(self.team1, self.team2)
    while team1wins < 4 and team2wins < 4:
      winner = ""
      if game_number == 1 or game_number == 2 or game_number == 5 or game_number == 7:
        winner = game.run(1)
      else:
        winner = game.run(2)
      if winner == self.team1.get_name():
        team1wins += 1
      else:
        team2wins +=1
      game_number+=1
	  
    if team1wins == 4:
      return self.team1.get_name()
    else:
      return self.team2.get_name()

class Round:
  #assume team_list has teams organized by matchup
  def __init__(self, team_list):
    self.team_list = team_list
	
  def run(self):
    winner_list = []
    count = 0
    while count < len(self.team_list):
      if(self.team_list[count].get_wins() >= self.team_list[count+1].get_wins()):
        series = Series(self.team_list[count], self.team_list[count+1])
      else:
        series = Series(self.team_list[count+1], self.team_list[count])

      winner = series.run()
      if winner == self.team_list[count].get_name():
        winner_list.append(self.team_list[count])
      else:
        winner_list.append(self.team_list[count+1])
      count+=2
	  
    return winner_list
	

class Playoffs:
  def __init__(self, team_list):
    self.team_list = team_list
  
  def run(self):
    while len(self.team_list) > 1:
      round = Round(self.team_list)
      self.team_list = round.run()
    
    #return champion
    return self.team_list[0].get_name()

	
if __name__ == "__main__":
  
  team_list = []
  f = open("C:/Users/Alex/Documents/Data/Basketball/Playoffs/PlayoffTeams.tsv", 'r')
  line = f.readline()
  while len(line) > 0:
    s = line.split()
    team_list.append(Team(s[0], int(s[1]), float(s[2])))
    line = f.readline()
	
  winners_map = {}
  for a in range(1,100000):
    temp_team_list = list(team_list)
    playoffs = Playoffs(temp_team_list)
    winner = playoffs.run()
    try:
      winners_map[winner] = winners_map[winner] + 1
    except:
      winners_map[winner] = 1
	  
  for key in winners_map.keys():
    print key + ": " + str(float(winners_map[key]/1000.0)) + "%"
	
	