# -*- coding: utf-8 -*-
#python 3.5.2
import heapq
import sys
from collections import Counter
import numpy as np
from Card import Card
from Card import Player
from PrintCard import ascii_version_of_card
import argparse


def distributeCards(deckofCards,nplayers,ncards=5):
    '''
    Distribute cards among the players
    '''
    hands = []
    if nplayers*ncards<=52:
        for i in range(nplayers):
            hands.append(np.random.choice(deckofCards,replace=False,size=ncards))
    else:
        raise ValueError("Number of Player Can't be greater than 10")
    return hands


def tieBreaker(player1,player2):
    '''
    Breaking the tie using high card rule
    '''
    winner = None
    if player1.ResultDict['Flush'] or player1.ResultDict['OnePair'] or  sum(player1.ResultDict.values()):
        i = 3
        while player1.CardScore == player2.CardScore and i>=0:
            player1.CardScore += player1.SortedCards[i]
            player2.CardScore += player2.SortedCards[i]
            i-=1
        if player1.CardScore > player2.CardScore:
            winner = player1
        elif player2.CardScore > player1.CardScore:
            winner = player2
             
    elif player1.ResultDict['TwoPair']:
        player1.cardscore += 2*(min([key for key in Counter(player1.SortedCards).keys if key==2]))
        player2.cardscore += 2*(min([key for key in Counter(player2.SortedCards).keys if key==2]))
        if player1.CardScore > player2.CardScore:
            winner = player1
        elif player2.CardScore > player1.CardScore:
            winner = player2
        else:
            player1.cardscore += sum([key for key in Counter(player1.SortedCards).keys if key==1])
            player2.cardscore += sum([key for key in Counter(player2.SortedCards).keys if key==1])
            if player1.CardScore > player2.CardScore:
                winner = player1
            elif player2.CardScore > player1.CardScore:
                winner = player2
    return winner
       
def determine_winner(player1,player2):
    '''
    Determining the winner based on card score
    '''
    winner = None
    if player1.CardScore > player2.CardScore:
        winner = player1
    elif player2.CardScore > player1.CardScore:
        winner = player2
    else:
        # print("There is a tie")
        winner = tieBreaker(player1,player2)
    return winner
    
def runSimulation(deckofCards,n):
    ResultDict = {
            "OnePair":0,
            "TwoPair": 0,
            'ThreeKind':0,
            'Straight':0,
            'Flush':0,
            'FullHouse':0,
            'FourKind':0,
            'StraightFlush':0,
            'RoyalFlush':0,
            'TotalGames':0    
        }
    for i in range(n):
        shuffledcards = np.random.choice(deckofCards,size=len(deckofCards),replace=False)
        newplayer = Player(1,np.random.choice(shuffledcards,size=5,replace=False))
        ResultDict['TotalGames']+=1
        for key in newplayer.ResultDict.keys():
            if newplayer.ResultDict[key]:
                ResultDict[key]+=1
    return ResultDict

def main():
    
    suits = ["Spades","Hearts","Clubs","Diamonds"]
    numbers = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
    deckofCards = np.empty(52,dtype=object)
    for i,suit in enumerate(suits):
        for j,num in enumerate(numbers):
            deckofCards[i*13+j] = Card(num,suit)
    
    shuffledcards = np.random.choice(deckofCards,size=len(deckofCards),replace=False)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-n","--numPlayers", help="Enter the Number of Players in the game Must be less than 11",type=int)
    parser.add_argument("-s","--simulation",help="Run in Simulation mode",type=int)
    args = parser.parse_args()
    
    if args.simulation:
        resultdict = runSimulation(deckofCards,args.simulation)     
        print(resultdict)
    
    else:
        numplayers = 5
        if args.numPlayers:
            numplayers = args.numPlayers
        
        Players = []
        hands = distributeCards(shuffledcards,nplayers=numplayers)
        
        for i,hand in enumerate(hands):
            Players.append(Player(i,hand))
        
        for player in Players:
            print("Player {}".format(player.PlayerNum+1))
            print(ascii_version_of_card(player.Cards[0],player.Cards[1],player.Cards[2],player.Cards[3],player.Cards[4]))
            
            cardstats = [key for key in player.ResultDict.keys() if player.ResultDict[key]==True]
            print("Player {} has {}".format(player.PlayerNum+1,cardstats))
            print("Card Score {}".format(player.CardScore))
        winner = Players[0]
        
        for i in range(1,len(Players)):
            player2 = Players[i]
            if player2 is not None:
                winneramongtwo = determine_winner(winner,player2)
                if winneramongtwo is not None:
                    winner = winneramongtwo
                else:
                    print("Tie Exists...")
                
        print("Player no: {} won".format(winner.PlayerNum+1))

      
if __name__ == "__main__":
    
    main()
    
    