## ignore this code, just used for submission
import requests
import pprint
import json
import random
import time
from copy import copy, deepcopy
from play import play
from functools import reduce

STUDENT_TOKEN = "VICTORIANOS"

class Game:
  def __init__(self, state, status, player):
    self.state = state
    self.status = status
    self.player = player

  def is_waiting(self):
    return self.status == 'waiting'

  def is_end(self):
    return self.status == 'complete'
  
  def get_board(self):
    return json.loads(self.state)

  def get_winner(self):
    return None

  def actions(self):
    return []

  def print(self):
    print(self.state)

def new_game(game_type, multi_player = False):
  for _ in range(10):
    r = requests.get('https://emarchiori.eu.pythonanywhere.com/new-game?TOKEN=%s&game-type=%s&multi-player=%s' % (STUDENT_TOKEN, game_type, 'True' if multi_player else 'False'))
    if r.status_code == 200:
      return r.json()['game-id']
    print(r.content)

def join_game(game_type, game_id):
  for _ in range(10):
    r = requests.get('https://emarchiori.eu.pythonanywhere.com/join-game?TOKEN=%s&game-type=%s&game-id=%s' % (STUDENT_TOKEN, game_type, game_id))
    if r.status_code == 200:
      return r.json()['player']
    print(r.content)

def game_state(game_type, game_id, GameClass):
  for _ in range(10):
    r = requests.get('https://emarchiori.eu.pythonanywhere.com/game-state?TOKEN=%s&game-type=%s&game-id=%s' % (STUDENT_TOKEN, game_type, game_id))
    if r.status_code == 200:
      return GameClass(r.json()['state'], r.json()['status'], r.json()['player'])
    print(r.content)

def update_game(game_type, game_id, player, move):
  for _ in range(10):
    r = requests.get('https://emarchiori.eu.pythonanywhere.com/update-game?TOKEN=%s&game-type=%s&game-id=%s&player=%s&move=%s' % (STUDENT_TOKEN, game_type, game_id, player, move))
    if r.status_code == 200:
      return r.content
    print(r.content)

def game_loop(solver, GameClass, game_type, multi_player = False, id = None):
  while id == None:
    print('Creating new game...')
    id = new_game(game_type, multi_player)

  print('Joining game with id: %s' % id)
  player = join_game(game_type, id)
  #player="X"

  print('Playing as %s' % player)

  game = game_state(game_type, id, GameClass)
  print('Waiting for the other player to join...')
  while game.is_waiting():
    time.sleep(10)
    game = game_state(game_type, id, GameClass)
  #
  player1 = game.player
  while True:
    previous_board = game.get_board()
    game = game_state(game_type, id, GameClass)
    new_board = game.get_board()
    game.print_game()
    if game.is_end():
      if game.player == '-':
        print('draw')
      else:
        print('winner' if game.player == player else 'loser')
      return
    if game.player == player:
      print('Making next move...')
      next_move = play(previous_board, new_board, player)

      update_result = update_game(game_type, id, player, json.dumps(next_move))
      print("previous board: ", previous_board)
      print("new board: ", new_board)
      print("You can still surrender 	(˵ ͡° ͜ʖ ͡°˵)")
    else:
      time.sleep(2)



class ConnectFour(Game):
  def __init__(self, state, status, player):
    Game.__init__(self, state, status, player)

  def actions(self):
    return [] # this should return the possible actions

  def get_winner(self):
    return '.' # this should return the actual winner

  def other_player(self):
    if self.player == 'O': return 'X'
    if self.player == 'X': return 'O'

  def print_game(self):
    print(self.state)


game_loop(play, ConnectFour, 'connect4big', multi_player=False, id=None)