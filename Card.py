from collections import Counter
import numpy as np
from PrintCard import ascii_version_of_card
class Card():
    '''
    Class definition for the Card
    '''
    faces = ["T","J","Q","K","A"]
    suits = ["Spades","Hearts","Clubs","Diamonds"]
    suits_symbols = ['♠', '♥', '♣','♦']
    def __init__(self,number,suit):
        self.number = None
        self.suit = None
        if not number.isnumeric():
            self.number = 10+self.faces.index(str(number))
        else:
            self.number = int(number)
        self.suit = suit
    
    def __str__(self):
        retstr = "{}".format(self.number)
        retstr+= "{}".format(self.suits_symbols[self.suits.index(self.suit)])
        return retstr

    
class Player():
    '''
    Class definition for Player
    '''
    
    def __init__(self,playernum,cards):
        self.PlayerNum = playernum
        self.Cards = cards
        if len(cards)==5:
            self.evaluateCards()
        
    def evaluateCards(self):
        
        self.CardScore = 0
        self.HighestCard = 0
        self.SortedCards = None
        self.LowestCard = 0
        self.HighCard = 0
         
        self.ResultDict = {
            "OnePair":False,
            "TwoPair": False,
            'ThreeKind':False,
            'Straight':False,
            'Flush':False,
            'FullHouse':False,
            'FourKind':False,
            'StraightFlush':False,
            'RoyalFlush':False,    
        }
        
        nums = [card.number for card in self.Cards]
        numdictcount = Counter(nums)
        suits = [card.suit for card in self.Cards]
        suitdictcount = Counter(suits)
        
        self.SortedCards = np.sort(np.array(nums))
        self.HighestCard = self.SortedCards[-1]
        self.LowestCard = self.SortedCards[0]
        
        if  4 in numdictcount.values():
            self.ResultDict['FourKind']=True
        
        elif 3 in numdictcount.values():
            self.ResultDict['ThreeKind']=True
            if 2 in numdictcount.values():
                self.ResultDict['FullHouse']=True
      
        elif 2 in numdictcount.values():
            if len(numdictcount)>3:
                self.ResultDict['OnePair']=True
                
            else:
                self.ResultDict['TwoPair']=True

        # if self.ResultDict['ThreeKind'] & self.ResultDict['OnePair']:
            
            
        issorted = True
        if self.HighestCard == 14:
            for i in range(len(self.SortedCards)-2):
                if self.SortedCards[i+1] - self.SortedCards[i]!=1:
                    issorted = False
                if self.SortedCards[-2]!=13 and self.SortedCards[0]!=2:
                    issorted = False
        else:
            for i in range(len(self.SortedCards)-1):
                if self.SortedCards[i+1]-self.SortedCards[i]!=1:
                    issorted = False
        
        if issorted:
            self.ResultDict['Straight']=True
            if self.SortedCards[0]==2:
                highcard = self.SortedCards[-2]
            else:
                highcard = self.HighestCard
            
        if  5 in suitdictcount.values():
            self.ResultDict['Flush'] = True
        
        if self.ResultDict['Straight'] and self.ResultDict['Flush']:
            self.ResultDict['StraightFlush'] = True
        
        if self.ResultDict['Straight'] and self.ResultDict['Flush'] and self.LowestCard==10:
            self.ResultDict['RoyalFlush'] = True
            
        if self.ResultDict['RoyalFlush']:
            self.CardScore = 900
        elif self.ResultDict['StraightFlush']:
            self.CardScore = 800+self.SortedCards[-1]
        elif self.ResultDict['FourKind']:
            self.CardScore = 700+4*sum([key for key in numdictcount.keys() if numdictcount[key]==4])
        elif self.ResultDict['FullHouse']:
            self.CardScore = 600+3*sum([key for key in numdictcount.keys() if numdictcount[key]==3]) 
        elif self.ResultDict['Flush']:
            self.CardScore = 500+ self.HighestCard
        elif self.ResultDict['Straight']:
            self.CardScore = 400 + highcard
        elif self.ResultDict['ThreeKind']:
            self.CardScore = 300 + 3*sum([key for key in numdictcount.keys() if numdictcount[key]==3])
        elif self.ResultDict['TwoPair']:
            self.CardScore = 200 + 2*(max([key for key in numdictcount.keys() if numdictcount[key]==2]))
        elif self.ResultDict['OnePair']:
            self.CardScore = 100 +  2*sum([key for key in numdictcount.keys() if numdictcount[key]==2])
        else:
            self.CardScore = self.HighestCard
    
    def __str__(self):
        # self.evaluateCards()
        retstr = "Player {} has following cards\n".format(self.PlayerNum)
        retstr += ascii_version_of_card(self.Cards[0],self.Cards[1],self.Cards[2],self.Cards[3],self.Cards[4])
        retstr += "\n"
        cardstats = [key for key in self.ResultDict.keys() if self.ResultDict[key]==True]
        for stats in cardstats:
            retstr += "{}\t".format(stats)
        retstr += "\nCard Score: {}".format(self.CardScore)
        return retstr