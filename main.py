"""
Title: UNO
Purpose: Demonstrate Python proficiency by replicating a card game
Github Repo: https://github.com/Saidaiii/UNO
"""

#Shuffle - Shuffle cards
#Randint - Pick random player at start
#Choice - Random Pick for bots
from random import shuffle, randint, choice
#termcolor - Have colored cards
from termcolor import *
#System - clear screen method
from os import system
#get_first_name = get names for bots
from names import get_first_name
#Sleep - Have some delay for the player to see what happens
from time import sleep
#cc = card color
cc = 'on_white'

#Class Hierarchy
# -----------------------------Card---------------------------
#      ↑                        ↑                       ↑
# NumberCard                ActionCard               WildCard

#Card Class - Base Class
class Card:
  #Initializes the face value of the card and its color
  def __init__(self, aValue = "", aColor = ""):
      self.value = aValue
      self.color = aColor
  
  #Returns the face value with print
  def __str__(self):
      return self.value

  #Returns the color of the card - associated with termcolor values
  def getColor(self):
    return self.color
  
  #Returns the value of the card
  def getValue(self):
    return self.value

#NumberCard Class - Child Class - Represents cards with face values 0-9
class NumberCard(Card):
  #Initializes the base class and its color
  def __init__(self, aValue = "", aColor = ""):
    Card.__init__(self, aValue, aColor)

#ActionCard Class - Child Class - Represents cards with actions such as Draw 2, Skip and Reverse
class ActionCard(Card):
  #Initializes the base class, color and the type of Action Card - "d2", "r", "s"
  def __init__(self, aValue = "", aColor = "", aType = ""):
    Card.__init__(self,aValue, aColor)
    self.type = aType

#WildCard Class - Child Class - Represents wild cards such as Draw 4 and Wild
class WildCard(Card):
  #Initializes the base class, color and the type of Wild Card - "+4", "w"
  def __init__(self, aValue = "", aType = ""):
    Card.__init__(self,aValue,'grey')
    self.type = aType

#Player Class - Stores the players hand and name
class Player:
  #Initializes the players hand and name
  def __init__(self, aHand = [], aName = ""):
      self.hand = aHand
      self.name = aName
      self.win = False
      self.UNO = False
  
  #Print Name and amount of cards of Player
  def __str__(self):
    print(self.getName() + ": " + self.lenHand() * "🂠 ",end="")
    if self.lenHand() == 1 and self.UNO:
      self.colorTitle()
    return ('')
  
  #Prints all cards with its respective colors and face values with indexing for player option
  def showHand(self):
      for card in range(self.lenHand()):
          cprint(self.hand[card], self.hand[card].getColor(), cc, end = "")
          print(" ", end="")
          if card >= 9 and (self.hand[card].value != "+2" and self.hand[card].value != "+4"):
            print(" ", end="")
      print("")
      for i in range(1, self.lenHand() + 1):
        print(str(i) + " ", end = "")
        if isinstance(self.hand[i-1], (ActionCard, WildCard)):
          if (self.hand[i-1].type == "d2" or self.hand[i-1].type == "d4") and i < 10:
            print(" ", end="")
  
  #Appends a card to the hand, reset UNO property
  def draw(self, card):
    self.hand.append(card)
    self.UNO = False

  #Appends many cards to the hand, reset UNO property
  def drawN(self, cardStack):
    for card in cardStack:
      self.hand.append(card)
    self.UNO = False
  
  #Returns the amount of cards in the players hand
  def lenHand(self):
     return len(self.hand)

  #Returns Players name
  def getName(self):
    return self.name
  
  #Sort Players hand by colors
  def sortHand(self):
    colorList = ['blue', 'red', 'green', 'yellow']
    startWindow = 0
    currPtr = 0

    for color in colorList:
      while currPtr != self.lenHand():
        if self.hand[currPtr].getColor() == color:
          self.hand[currPtr], self.hand[startWindow] = self.hand[startWindow], self.hand[currPtr]
          startWindow += 1
        currPtr += 1
      currPtr = startWindow
  
  #Player says UNO!
  def setUNO(self):
    self.UNO = True

  #Check if player said UNO for himself
  def selfUNO(self):
    if self.UNO and self.lenHand() == 1:
      return True
    else:
      return False
  
  #Check if player forgot to say UNO
  def forgotSelfUNO(self):
    if not self.UNO and self.lenHand() == 1:
      return True
    else:
      return False

  #Checks if the player wins
  def checkWin(self):
    if len(self.hand) == 0:
      return True
    else:
      return False
  
  #Prints UNO! title for the player who said UNO! and is close to winning
  def colorTitle(self):
    cprint("U", 'blue', cc, end="")
    cprint("N", 'yellow', cc, end="")
    cprint("O", 'green', cc, end="")
    cprint("!", 'red', cc, end="")

#####FUNCTIONS######

#Function that develops the initial deck and shuffles it pre-game
def createDeck():
  #Create Deck list
  Deck = []
  
  #Create Color list to easily index the colors
  colors = ['red', 'blue', 'green', 'yellow']
  for color in range(len(colors)):
      #Create 0-9 Cards with respective colors
      for value in range(0,10):
          for double in range(2):
              deckCard = NumberCard(str(value), colors[color])
              Deck.append(deckCard)
      #Create Action Cards
      for action in range(2):
          draw2Card = ActionCard("+2", colors[color], "d2")
          reverseCard = ActionCard("⇄", colors[color], "r")
          skipCard = ActionCard("X", colors[color], "s")
          Deck.append(draw2Card)
          Deck.append(reverseCard)
          Deck.append(skipCard)
  #Create Wild Cards
  for wild in range(4):
    draw4Card = WildCard("+4", "d4")
    wildCard = WildCard("☯", "w")
    Deck.append(draw4Card)
    Deck.append(wildCard)

  #Shuffle the deck
  shuffle(Deck)
  
  return Deck

#Function that prints the UNO! Title in colors
def colorTitle():
  cprint("U", 'blue', cc, end="")
  cprint("N", 'yellow', cc, end="")
  cprint("O", 'green', cc, end="")
  cprint("!", 'red', cc)

#Function that prints the menu
def menu():
  colorTitle()
  print("\nCHOOSE MODE!\n")
  print("1. Single Player (Play VS Bots)")
  print("2. Multi-Player (Coming Soon!)")
  print("3. Read Rules")
  print("4. EXIT\n")
  print("Developed by Saidaiii\n")
  try:
    option = int(input("Option: "))
  except:
    option = -1

  #Make sure the user picks a number in the range and no errors produce
  while True:
    try:
      while option < 1 and option > 4:
        option = int(input("Option must be 1-4: "))
      break
    except:
      option = -1
  system('clear')
  return option

#Function that will display the help section
def goHelp():
  helpV = ""
  while helpV != "--resume":
    colorTitle()
    cprint("\nSET-UP", 'red', cc)
    print("Every player will receive 7 cards at the start. One player will be chosen randomly. You will see your oponents on the top of the screen with their respective cards in conjunction to whose turn it is. In the middle you will see the discard pile which will hold the current play card. At the right of this card, you will see the draw pile. This pile will serve to distribute cards if you don't have any playable cards or if you are forced to draw.\n")

    cprint("\nGAMEPLAY", 'blue', cc)
    print("When it is your turn, you will see your name at the top of your screen and your cards will appear at the bottom. You will be permitted to select which action you desire. \nCARD NUMBER - You will input the card number that you desire to play. \nDRAW CARD - If you can't play any of the available cards, you can input 'd' to draw a card and forfeit your turn. \nSAY UNO! - If you are about to have one card or notice anybody is at one card and have not said UNO!, you can input 'u' to say UNO! Whoever gets caught with one card will receive 4 cards. If you say UNO! and no one has one card and neither do you, you will receive 6 cards. **VERY IMPORTANT** Remember to say UNO! before you throw your semifinal card!\n")
    
    cprint("\nCARDS", 'yellow', cc)
    print("You will see many cards in this game yet some may seem unfamiliar.\n")
    print("Number Cards: ", end="")
    for cards in range(0, 10):
      cprint(str(cards), 'red', cc, end=" ")
    print("\nYou can use these cards as long as the current play card is of that same color or number. You may also use these if the current play card is a wild card and the color chosen is the same. These cards have no effect on gameplay.\n")
    print("Action Cards:")
    cprint("+2", 'blue', cc, end =" ")
    print("Draw 2: You can use these cards if the current play card is the same color, if it's also a Draw 2, or if it's a wild card and the color chosen is the same. This will force the next opponent to draw 2 cards and skip his turn unless he also has a Draw 2 Card and decides to play it.")
    cprint("⇄", 'green', cc, end =" ")
    print("Reverse: You can use these cards if the current play card is the same color, if it's also a Reverse, or if it's a wild card and the color chosen is the same. This will change the direction of the order in which the players game. Ex. John -> Sally -> Steven == Steven -> Sally -> John")
    cprint("X", 'yellow', cc, end =" ")
    print("Skip: You can use these cards if the current play card is the same color, if it's also a Skip, or if it's a wild card and the color chosen is the same. This will skip the following player's turn.")
    print("\nWild Cards: ")
    cprint("+4", 'grey', cc, end =" ")
    print("Draw 4: This card is known as the 'universal' card. This card can be played on any other card, except a +2, as long as it is your turn. This will force the following player to draw 4 cards and skip his turn unless he also has a Draw 4 and decides to play it. This player will also choose what the following color may be. If the previous player drew 4 cards and the current player stacks another draw 4 on top, this will not stack since the last player already drew the previous stack.")
    cprint("☯", 'grey', cc, end =" ")
    print("Wild: You may use these cards to change the current color of the game. This card can be played on top of any card as long as it is your turn and you have not been forced to draw.\n\n")

    helpV = input("Enter --resume to continue: ")
    system('clear')

#Function that prints the roster names and their cards
def showRoster(players, index , uno, unoPlayer, direction):
  #Configure Next Player
  nextPlayer = index + direction
  if nextPlayer >= len(players):
    nextPlayer = 0
  elif nextPlayer <= -1:
    nextPlayer = len(players) - 1
  
  #Iterate through Roster
  for player in range(len(players)):
    #Print Current Player Arrow
    if player == index:
      print("►",end="")
    #Print Next Player Arrow
    elif player == nextPlayer:
      if direction == 1:
        print("▼",end="")
      else:
        print("▲",end="")
    print(players[player], end=" ")
    if uno and player == unoPlayer:
      print("UNO!")
      continue
    print("")


#Function for bot to detect if anyone has not said uno  
def botCheckUNO(players):
  for player in players:
    if player.forgotSelfUNO():
      return True
  return False

#Function that executes the skip mechanism
def skip(index, direction, playerCount):
  #If the index is near top edge, we can just subtract it with the amount of players
  if index <= 1 and direction == -1:
    return index + 2 * direction + playerCount + 1
  #If the index is near bottom edge, we can just add it with the amount of players
  elif index >= playerCount - 2 and direction == 1:
    return index + 2 * direction - playerCount - 1
  #If the index is not near edge, we can skip with the standard equation
  else:
    #Depending on the direction, we need to either send one more or one less to compensate for the algorithm on startGame indexing
    if direction == 1:
      return index + 2 * direction - 1
    else:
      return index + 2 * direction + 1

#Function that checks if a card is playable and returns the index
def canPlay(card, hand, colorOption):
  for cards in range(len(hand)):
    if (card.getValue() == hand[cards].getValue() or card.getColor() == hand[cards].getColor() or hand[cards].getColor() == colorOption or isinstance(hand[cards],WildCard)):
      return cards
  return -1

#Prints the discard pile and the deck
def printMiddle(top):
  print("")
  cprint(top, top.getColor(),cc, end="")
  print(" 🂠\n")

#Function that prints local player options
def localOptions(player, drawAmount, colorOption, discardTop):
  player.showHand()
  print("\n\nActions: \nThrow Card - Input Card Number\nDraw Card - Input 'd' (Current Draw: ", end ="")
  if drawAmount == 0:
    print(1, end ="")
  else:
    print(drawAmount, end="")
  print(")\nSay UNO! - Input 'u' (Use before throwing)")
  if isinstance(discardTop, WildCard):
    print("\nColor Option: " + colorOption,end="")
  print("\nType --help for rules\n")

#Function to determine if a player can play a number card or action card
def canPlayActNum(playCard, discardTop, colorOption):
  if playCard.getColor() == discardTop.getColor() or playCard.getValue() == discardTop.getValue() or playCard.getColor() == colorOption:
    return True
  else:
    return False

#Function to execute drawing mechanism
def executeDraw(drawAmount, player, deck):
  if drawAmount == 0:
    player.draw(deck.pop())
  else:
    drawPile = []
    for drawing in range(drawAmount):
      drawPile.append(deck.pop())
    player.drawN(drawPile)
  return player, deck

#Function to pick a color
def pickColor(colors):
  print("\nPick Color: " ,end="")
  for color in colors:
    print(color,end=", ")
  print("")
  colorOption = input("Enter Color: ")
  while colorOption not in colors:
    colorOption = input("Invalid Color. Re-Enter Color: ")
  return colorOption

#Function that runs the single player game
def startGame(players, deck):
  #Pick a random index to start with that player
  currPlayerIndex = randint(0, len(players) - 1)
  currPlayer = players[currPlayerIndex]
  #Always Start Game with number card
  while not (isinstance(deck[-1],NumberCard)):
    shuffle(deck)
  #Place the top card at the deck in the discard
  discardPile = [deck.pop()]
  #Preset variables such as direction, drawAmount and colorOption
  direction = 1
  drawAmount = 0
  colorOption = ""
  colors = ['red', 'blue', 'green', 'yellow']
  #Sort Local Hand
  players[0].sortHand()
  #Set sayUno variable
  sUNO = False
  unoPlayer = -1

  while True:
    system('clear')
    #Set the current Player
    currPlayer = players[currPlayerIndex]
    #Print who's turn it is
    print(currPlayer.getName() + "'s turn\n")
    
    #Print the roster of players
    showRoster(players, currPlayerIndex, sUNO, unoPlayer, direction)
    
    #Print the discard pile with the draw pile
    printMiddle(discardPile[-1])

    #If TopCard is not a Wild, we can reset the colorOption
    if not isinstance(discardPile[-1], WildCard):
      colorOption = ""

    #Local Player's Turn
    if currPlayerIndex == 0:
      localOptions(currPlayer, drawAmount, colorOption, discardPile[-1])
      action = input("Action: ")

      #If Player needs help, go to function, return and re-initialize the view
      try:
        if action == "--help":
          system('clear')
          goHelp()
          continue
      except:
        pass
      
      #If player wants to draw, run the function execution
      try:
        if action == 'd':
          print("\nDrawing Card(s)...\n")
          sleep(2)
          currPlayer, deck = executeDraw(drawAmount, currPlayer, deck)
          currPlayer.sortHand()
          drawAmount = 0
      except:
        pass
      
      try:
        if action == 'u' and not sUNO:
          currPlayer.setUNO()
          sUNO = True
          print("\n" + currPlayer.getName() + " said UNO!")
          unoPlayer = currPlayerIndex
          sleep(2)
          continue
        elif action == 'u' and sUNO:
          print("\nYou already said UNO!")
          sleep(2)
          continue
      except:
        pass

      try:
        #Turn for indexing
        action = int(action) - 1
        if action >= 0 and action <= currPlayer.lenHand() - 1:
          #Store the action in a more easy accessible variable
          playCard = currPlayer.hand[action]
          #Check if it is a number card and not stacked for drawing
          if isinstance(playCard, NumberCard) and drawAmount == 0:
            if canPlayActNum(playCard, discardPile[-1], colorOption):
              pass
            else:
              print("\nInvalid Card...\n")
              sleep(3)
              continue
          #Check if it is a Action Card
          elif isinstance(playCard, ActionCard):
            if canPlayActNum(playCard, discardPile[-1], colorOption):
              #Action if card is +2
              if playCard.getValue() == "+2":
                drawAmount += 2
              #Action if card is Reverse
              elif playCard.getValue() == "⇄" and drawAmount == 0:
                direction = 1 if direction == -1 else -1
              #Action if card is Skip
              elif playCard.getValue() == "X" and drawAmount == 0:
                currPlayerIndex = skip(currPlayerIndex, direction, len(players))
              else:  
                print("\nInvalid Card...\n")
                sleep(3)
                continue
            else:
              print("\nInvalid Card...\n")
              sleep(3)
              continue
          else:
            #Action if Wild Card is +4 and the top of discard is not a +2
            if playCard.getValue() == "+4" and not (discardPile[-1].getValue() == "+2"):
              drawAmount += 4
              #Player has to choose a color
              colorOption = pickColor(colors)
            #Action if Wild Card is wild and there is no current Draw
            elif playCard.getValue() == "☯" and drawAmount == 0:
              #Player has to choose a color
              colorOption = pickColor(colors)
            else:
              print("\nInvalid Card...\n")
              sleep(3)
              continue
          
          #Player will pop the card they picked to the top of the discard pile
          discardPile.append(currPlayer.hand.pop(action))
          print("\nThrowing Card...\n")
          sleep(2)
        else:
          print("\nInvalid Option...\n")
          sleep(3)
          continue  
      except:
        if action == 'd' or action == 'u':
          pass
        else:
          print("\nInvalid Option...\n")
          sleep(2)
          continue

    #Bots Turn
    else:
      #If the bot can draw, it will draw
      if drawAmount > 0:
        print("\nDrawing Card(s)...\n")
        currPlayer, deck = executeDraw(drawAmount, currPlayer, deck)
        drawAmount = 0
      elif canPlay(discardPile[-1], currPlayer.hand, colorOption) != -1:
        #Decide wether or not to say UNO
        decision = ['yes', 'no']
        if (currPlayer.lenHand() == 2 or botCheckUNO(players)) and not sUNO:
          #Makes a choice wether or not to say UNO
          unoDecision = choice(decision)
          if unoDecision == 'yes':
            currPlayer.setUNO()
            sUNO = True
            print("\n" + currPlayer.getName() + " said UNO!")
            unoPlayer = currPlayerIndex
            sleep(2)
            continue
        #Store the card index of the card chosen
        action = canPlay(discardPile[-1], currPlayer.hand, colorOption)
        #Store the card for easy access
        playCard = currPlayer.hand[action]
        #If card is a number card, we can just keep going
        if isinstance(playCard, NumberCard):
          pass
        #If card is an action card, take the action steps and keep going
        elif isinstance(playCard, ActionCard):
          if playCard.getValue() == "+2":
            drawAmount += 2
          elif playCard.getValue() == "⇄":
            direction = 1 if direction == -1 else -1
          else:
            currPlayerIndex = skip(currPlayerIndex, direction, len(players))
        #If card is a wild card, take action steps and keep going
        elif isinstance(playCard, WildCard):
          if playCard.getValue() == "+4":
            drawAmount += 4
            #Bot will pick a random color
            colorOption = choice(colors)
          elif playCard.getValue() == "☯":
            #Bot will pick a random color
            colorOption = choice(colors)
        
        #Bot will pop the card they picked to the top of the discard pile
        discardPile.append(currPlayer.hand.pop(action))
        print("\nThrowing Card...\n")
        sleep(2)
      else:
        #Bot will draw if it can't find a playable card
        print("\nDrawing Card...\n")
        sleep(2)
        currPlayer, deck = executeDraw(drawAmount, currPlayer, deck)

    #Check if a player won
    if currPlayer.checkWin():
      system('clear')
      showRoster(players, currPlayerIndex, sUNO, unoPlayer, direction)
      print("\n" + currPlayer.getName() + " wins!\n")
      print("Returning to Main Menu in 5 seconds...")
      sleep(5)
      system('clear')
      break

    #Check if player said UNO
    if sUNO:
      system('clear')
      print(currPlayer.getName() + "'s turn\n")
      showRoster(players, currPlayerIndex, sUNO, unoPlayer, direction)
      printMiddle(discardPile[-1])
      print("")
      lied = True
      #Iterate through players to see if player or bot who said UNO said it at the wrong time
      for player in range(len(players)):
        if players[player].forgotSelfUNO():
          #Player or bot who forgot to say uno must draw
          players[player], deck = executeDraw(4, players[player], deck)
          lied = False
          print(players[player].getName() + " forgot to say UNO!")
          sleep(2)
          print("Drawing Cards...")
          sleep(2)
      #If the player or bot said uno at the wrong time and they did not say it for themself, they must draw
      if lied and not players[unoPlayer].selfUNO():
        players[unoPlayer], deck = executeDraw(6, players[unoPlayer], deck)
        print(players[unoPlayer].getName() + " said UNO at the wrong time!")
        sleep(2)
        print("Drawing Cards...")
      #If player said uno for themself, then it will just keep going
      elif players[unoPlayer].selfUNO():
        print(players[unoPlayer].getName() + " said UNO for themself!")
      sleep(2)
      #Reset All UNO Commands
      sUNO = False
      unoPlayer = -1
    
    #Check if deck is close to empty, take out top card of discardPile, reshuffle discard pile and refill deck
    if len(deck) <= 16:
      discardTop = discardPile.pop()
      shuffle(discardPile)
      for discardCards in range(len(discardPile)):
        deck.append(discardPile.pop())
      discardPile.append(discardTop)
    
    #Continue to next player
    currPlayerIndex += direction
    #Check if we are on list edge
    currPlayerIndex = 0 if currPlayerIndex > len(players) - 1 else currPlayerIndex
    currPlayerIndex = len(players) - 1 if currPlayerIndex < 0 else currPlayerIndex
    #Sleep for 4 seconds
    sleep(3)

#Function that prints the single player menu
def SPMenu():
  colorTitle()
  print("\nCHOOSE AMOUNT OF BOTS!\n")
  print("[1] [2] [3] [4] [5] [6] [7]\n")
  print("Enter 'back' to return to Main Menu\n")
  option = (input("Option: "))
  
  #Filter the back option with a Try Statement
  try:
    if option == 'back':
      system('clear')
      return
  except:
    pass

  #Make sure the user picks a number in the range and no errors produce
  while True:
    try:
      option = int(option)
      while (option < 1) or (option > 7):
        option = int(input("Option must be between 1-7: "))
      break
    except:
      option = -1

  nameS = input("\nInput your name: ")
  #Create the Deck
  deck = createDeck()
  #Create Player List
  playerList = []
  #Create Hand
  hand = []
  #Distribute to hand from deck
  for card in range(7):
    hand.append(deck.pop())
  #Add Real Player
  player1 = Player(hand,nameS)
  playerList.append(player1)
  #Add bots
  for i in range(option):
    hand = []
    #Distribute to hand from deck
    for card in range(7):
      hand.append(deck.pop())
    bot = Player(hand, get_first_name())
    playerList.append(bot)
  
  #Initialize Game
  startGame(playerList, deck)

while True:
  #Show menu and receive option
  option = menu()

  #Option 1: Move so Single Player Menu
  if option == 1:
    SPMenu()
  #Option 2: Multi-Player not yet implemented
  elif option == 2:
    pass
  #Option 3: Show Rules
  elif option == 3:
    goHelp()
  #Option 4: Finish Program
  elif option == 4:
    break