import random, time, math
import pandas as pd
from multiprocessing import Pool, Manager

manager = Manager()
data = manager.list()

# A duel returns how many living and wights left after the duel
def duel(living_left, wights_left):
  if random.randint(0, 1) == 1:
    return living_left, wights_left -1
  else:
    return living_left - 1, wights_left + 1

# A battle returns the outcome of which side won.
def battle(living_count, wight_count):
  win = None
  while living_count >= 0 and wight_count >= 0:
    if living_count == 0:
      win =  False
      break
    elif wight_count == 0:
      win =  True
      break
    else:
      # else keep dueling
      living_count, wight_count = duel(living_count,wight_count)
  return win

# A collection of battles to return the numbers of wins and losses
def war(living_count,wight_count):
  battles_won = 0
  battles_lost = 0
  for x in range(0,100):
    #print('BATTLE NUMBER:',x)
    hoomans_win = battle(living_count,wight_count)
    if hoomans_win == True:
      battles_won = battles_won + 1
    elif hoomans_win == False :
      battles_lost = battles_lost + 1  
  return battles_won, battles_lost

def process(wight_count):
  wars, wars_won, wars_lost = 0, 0, 0
  living_count = int((wight_count * wight_count) + (wight_count * math.log(wight_count)))
  living_to_dead_ratio = []
  wins_to_losses_ratio = []
  wars_won_list = []
  wars_lost_list = []
  for x in range(0,20):
    wars_won, wars_lost = war(living_count,wight_count)
    wins_to_losses_ratio.append(float(wars_won/(wars_won+wars_lost)))
    wars_won_list.append(wars_won)
    wars_lost_list.append(wars_lost)
    wars = wars + 1
  #print('living/dead ratio:', living_to_dead_ratio) 
  #print('living:', living_count, 'dead:', wight_count) 
  #print('wins:', wars_won, 'losses:', wars_lost)
  #print('win/lose ratio:', wins_to_losses_ratio)
  #print('living_to_dead_ratio:', float(living_count/wight_count))
  #print('wins_to_losses_ratio:', (sum(wins_to_losses_ratio)/len(wins_to_losses_ratio)))
  data.append([living_count,
              wight_count,
              (sum(wars_won_list)/len(wars_won_list)),
              (sum(wars_lost_list)/len(wars_lost_list)),
              (sum(wins_to_losses_ratio)/len(wins_to_losses_ratio))])

if __name__ == '__main__':

  start = time.time()
  pool = Pool(processes=8)
  pool.map(process, list(range(5,255,5)))
  pool.close()

  print(time.time() - start)

  df = pd.DataFrame(list(data), columns=['lvings', 'wights', 'wins', 'losses', 'wins_to_losses_ratio']) 
  print(df)
  df.to_csv('~/Downloads/got_'+ time.strftime('%Y-%m-%d %H-%S') + '.csv', sep=',')
