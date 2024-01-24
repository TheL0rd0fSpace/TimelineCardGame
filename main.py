from master_dict_of_cards import MASTER_DICT_OF_CARDS
import random

"""
CODE SUMMARY
The cards are initially stored as a dictionary in MASTER_DICT_OF_CARDS (which is stored in the master_dict_of_cards.py 
    until createDeckOfCards creates an EventCard object for each of them and adds them to the deckOfCards list.
The timeline is both the variable name and the class name for the unique timeline object.
The player objects are created on-the-fly by the getPlayerName function and stored in the playerList variable.

Possible feature creep:
    Creating a "discard pile" variable, and using it to create a new deck when the deck runs out of cards.
        This would require a rework of the currently simple discardACard method.
    Change the game from a race to empty your hand to a "scoring" system, where players always redraw at the end of
        their turn, but score a point when they're correct, and the goal is to either reach X points first, 
        or to have the most points by a pre-determined time: either Y turns or the end of the deck.
    Could combine the two for an "Endurance mode", where players must go until they've successfully played every card.
        Most points wins. That or, whichever player is still conscious by the end. Either works.
    The ability to see all players' hands, regardless of whose turn it is, for greater strategic play.
        The downside? This game has enough text, and scales poorly with more and more players.
        In addition, it would be a challenge to ensure that the most relevant information:
            the current timeline and your hand, are the ones most prominently displayed.
        This feature would be better in a video game with a proper GUI that could efficiently condense players' hands
    When a player fails to play a card, don't reveal the date and let them keep it. Optionally, add a "hot/cold" option 
    that tells them whether the date is "newer" or "older" than the slot they tried to use.
"""


class EventCard:
    def __init__(self, name, date):
        self.name = f'"{name}"'
        self.date = date

    def __str__(self):
        return "Use getCardName or getCardAll, not print!"
        # Sometimes you want to print the event without the date, sometimes you want to print both.
        # By forbidding you to use the easy "Print" option, I ensure that you won't accidentally pick the wrong one.

    def getCardName(self):
        return self.name

    def getCardDate(self):
        return self.date
        # I can't imagine any time that you'd use this to show to the player;
        # This is for behind-the-scenes comparisons of dates, like when evaluating legal plays

    def getCardAll(self):
        return f'{self.name}, {str(self.date)}'


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []

    def __str__(self):
        return self.name

    def printHand(self):
        print(f"{self.name}, you are currently holding: ")
        for i in range(0, len(self.hand)):
            print(f"Card #{i}: {self.hand[i].getCardName()}")

    def drawACard(self, card, source="the deck"):
        # The "source" argument provides some future-proofing against the possibility that you may, in the future,
        # be able to draw cards from somewhere *other* than the deck
        self.hand.append(card)
        print(f"Player {self.name} has drawn {card.getCardName()} from {source}.")

    def discardACard(self, index):
        self.hand.pop(index)

    def selectCard(self):
        # If there's only one card left, no need to deliberate over which card to pick
        handSize = len(self.hand)
        if handSize == 1:
            return 0
        self.printHand()
        selectedCard = askForInt(0, handSize - 1, "Which card would you like to play?")
        print(f"You've chosen to play {self.hand[selectedCard].getCardName()}.")
        return selectedCard

    def didIWin(self):
        if len(self.hand) == 0:
            return True
        else:
            return False


class Timeline:
    def __init__(self):
        self.centerRow = []

    def printTimeline(self):
        print("\n###CURRENT TIMELINE###\n#Oldest Events#")
        for i in self.centerRow:
            print(i.getCardAll())
        print("#Newest Events#\n")

    def listIndexes(self):
        print("The positions you can currently play a card to are:\n#Oldest Events#\n")
        index = 0
        print(f"-- Position: {index} --")
        for i in self.centerRow:
            print(i.getCardAll())
            index += 1
            print(f"-- Position: {index} --")
        target = askForInt(0, len(self.centerRow), "\n#Newest Events#\nWhere would you like to play your card?")
        return target

    def checkValidPlay(self, targetIndex, dateOfNewCard):
        # if the targeted index isn't on the far left, then check the card to its left and return false if invalid
        if targetIndex != 0:
            leftIndex = targetIndex - 1
            leftIndexDate = self.centerRow[leftIndex].getCardDate()
            if not leftIndexDate <= dateOfNewCard:
                return False
        # if the targeted index isn't on the far right, then check the card to its right and return false if invalid
        if targetIndex != len(self.centerRow):
            rightIndex = targetIndex
            rightIndexDate = self.centerRow[rightIndex].getCardDate()
            if not dateOfNewCard <= rightIndexDate:
                return False
        # if neither of the above return False statements were reached, then the play should be valid
        return True

    def addCardToIndex(self, index, card):
        self.centerRow.insert(index, card)
        self.printTimeline()


def askForInt(minimum=None, maximum=None, request="Please enter an integer."):
    # Will keep repeating this loop until the user enters a valid integer within the range if there is one
    while True:
        print(request)
        try:
            userInt = int(input())
        except:
            print("Provided input was not an integer. Please try again.")
        else:
            if minimum & minimum <= userInt:
                if maximum & userInt <= maximum:
                    return userInt
                else:
                    print("Provided input was greater than the maximum. Please try again.")
            else:
                print("Provided input was less than the minimum. Please try again.")


def askForString(request="Please enter a string."):
    userString = None
    while not isinstance(userString, str):
        print(request)
        print("Please enter a string.")
        try:
            userString = str(input())
        except:
            print("Provided input was not a string. Please try again.")
        else:
            return userString


def choosePlayerCount(cardsNeededPerPlayer, deckSize):
    # takes player count, and verifies that there are enough cards in the deck for all players
    maximumCardsAvailable = len(deckSize)
    while True:
        numberOfPlayers = askForInt(1, 10000, "How many players do you have?")
        if cardsNeededPerPlayer * numberOfPlayers < maximumCardsAvailable:
            break
        else:
            print("Too many players. Please try again.")
            continue
    print(f"You have {numberOfPlayers} players.")
    return numberOfPlayers


def createDeckOfCards():
    deckOfCards = []
    for i in MASTER_DICT_OF_CARDS:
        generatedCard = EventCard(i, MASTER_DICT_OF_CARDS[i])
        deckOfCards.append(generatedCard)
    random.shuffle(deckOfCards)
    print("Shuffling the deck...")
    return deckOfCards


def setPlayerName(currentListOfPlayers, playerNumber):
    playerNumber = playerNumber
    print(f"What is the name of player {playerNumber}?")
    if currentListOfPlayers:
        print("For your convenience, ensure that player names don't match. The current players are: ")
        for i in range(0, len(currentListOfPlayers)):
            print(currentListOfPlayers[i])
    userInput = input()
    return str(userInput)


def main():
    # Create Initial Variables:
    # Starting hand size
    # The deck of cards, populated using the createDeckOfCards function
    # The number of players
    # The starting player
    # The empty playerList
    # The Timeline
    # isAWinner declares that, in fact, no one has won the game before it's started
    # The playerList is populated with players, one at a time, until there are at least as many as playerCount indicates
    # Each player is dealt one card, in order, "STARTING_CARDS_IN_HAND" times.
    # Finally, the first card is added from the deck to the Timeline
    STARTING_CARDS_IN_HAND = 5
    deckOfCards = createDeckOfCards()
    playerCount = choosePlayerCount(STARTING_CARDS_IN_HAND, deckOfCards)
    playerNumber = 0
    playerList = []
    timeline = Timeline()
    isAWinner = False
    for i in range(0, playerCount):
        newPlayer = Player(setPlayerName(playerList, i + 1))
        playerList.append(newPlayer)
    print("Dealing starting hands...")
    for i in range(0, STARTING_CARDS_IN_HAND):
        for j in playerList:
            j.drawACard(deckOfCards.pop(), "the deck")
    print("Starting hands dealt!")
    timeline.addCardToIndex(0, deckOfCards.pop())

    # PRIMARY GAMEPLAY LOOP.
    # As long as no one has won, determine who the current turn player is with the playerNumber variable.
    # Then, ask them what card they'd like to play.
    # Then, create a list of all the places in the Timeline they could play that card, and ask them to pick one.
    # Then, checkValidPlay uses the Date value of the index and its neighbors to see if the play is legitimate
    # If so, the card is moved from the player's hand to the chosen index.
    # If not, tell the player the date of the card they chose, then
    # discard the card they chose and draw a new one from the deck, if there are any left.
    # Possible feature creep: adding a "discard pile" variable and reshuffling it into a new deck when it runs out.
    while not isAWinner:
        currentPlayer = playerList[playerNumber]
        indexOfCardToPlay = currentPlayer.selectCard()
        cardToPlay = currentPlayer.hand[indexOfCardToPlay]
        target = timeline.listIndexes()
        if timeline.checkValidPlay(target, cardToPlay.getCardDate()):
            print("Correct!")
            timeline.addCardToIndex(target, currentPlayer.hand.pop(indexOfCardToPlay))
        else:
            print(f"Sorry, the date of {cardToPlay.getCardName()} was actually {cardToPlay.getCardDate()}.")
            currentPlayer.discardACard(indexOfCardToPlay)
            try:
                currentPlayer.drawACard(deckOfCards.pop(), "the deck")
            except:
                print("There are no cards left! Keep going without drawing a new card!")

        # Checks to see if a player won, and breaks the While loop on line 193 if True
        for i in playerList:
            if i.didIWin():
                isAWinner = True
                print(f"Congratulations, {i.name}, you've won!")

        if playerNumber == len(
                playerList) - 1:  # At the end of the last player's turn, it's the first player's turn next
            playerNumber = 0
        else:
            playerNumber += 1
        continue


if __name__ == '__main__':
    main()
