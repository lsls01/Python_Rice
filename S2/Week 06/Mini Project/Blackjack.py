# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self._cards = []	# create Hand object

    def __str__(self):
        # return a string representation of a hand
        hand_str = 'There are '
        for card in self._cards:
            hand_str += str(card) + ' '
        return hand_str + 'in hand'

    def add_card(self, card):
        self._cards.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        hasA = False
        for card in self._cards:
            rank = card.get_rank()
            if rank == 'A':
                hasA = True
            value += VALUES[rank]
        if hasA and value + 10 <= 21:
            value += 10
        return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self._cards:
            pos[0] += 85
            card.draw(canvas, pos)
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self._cards = [Card(suit,rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self._cards)    # use random.shuffle()

    def deal_card(self):
        # deal a card object from the deck
        return self._cards.pop()
    
    def __str__(self):
        # return a string representing the deck
        hand_str = 'There are '
        for card in self._cards:
            hand_str += str(card) + ' '
        return hand_str + 'on deck'



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, hand_player, hand_dealer, score
    
    if in_play:
        score -= 1
        outcome = 'You lose'
    
    deck = Deck()
    deck.shuffle()
    
    hand_player = Hand()
    hand_dealer = Hand()
    hand_player.add_card(deck.deal_card())
    hand_dealer.add_card(deck.deal_card())
    hand_player.add_card(deck.deal_card())
    hand_dealer.add_card(deck.deal_card())

    print "Player:" + str(hand_player)
    print "Dealer:" + str(hand_dealer)
    
    in_play = True
    outcome = ''

def hit():
    global deck, score, outcome, in_play, hand_player
    # if the hand is in play, hit the player
    if in_play:
        hand_player.add_card(deck.deal_card())
        print "Player:" + str(hand_player)
        player_value = hand_player.get_value()
        
        # if busted, assign a message to outcome, update in_play and score
        if player_value > 21:
            outcome = "You have busted"
            in_play = False
            score -= 1
        print outcome
       
def stand():
    # replace with your code below
    global outcome, score, in_play, hand_dealer, deck
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while hand_dealer.get_value() < 17:
            hand_dealer.add_card(deck.deal_card())
            
        print "Dealer:" + str(hand_dealer)
        dealer_value = hand_dealer.get_value()
        if hand_dealer > 21:
            outcome = "Dealer has busted. You win"
            score+=1
            in_play = False
        elif dealer_value >= hand_player.get_value():
            outcome = "Dealer Wins"
            score -= 1
            in_play = False
        else:
            outcome = "You Win"
            score += 1
            in_play = False
            
    # assign a message to outcome, update in_play and score
    print outcome

    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome, score
    
    canvas.draw_text('Blackjack', [235,35], 26, "White")
    canvas.draw_text('Player Score: ' + str(hand_player.get_value()), [235,80], 18, "Black")
    canvas.draw_text('Dealer Score: ' + str(hand_dealer.get_value()), [235,280], 18, "Black")
    
    hand_player.draw(canvas,[50,100])
    hand_dealer.draw(canvas,[50,300])
    
    canvas.draw_text(outcome,[250,500],26 , "White")
    if outcome == "":
        canvas.draw_text("Hit or Stand?",[250,500],26 , "White")
    
    if not in_play:
        canvas.draw_text("New Deal?",[250,550],26 , "White")
    else:
        card_pos = (CARD_CENTER[0], CARD_CENTER[1])
        canvas.draw_image(card_back, card_pos, CARD_SIZE, [50+80 + CARD_CENTER[0], 300 + CARD_CENTER[1]], CARD_SIZE)
        
    canvas.draw_text('Games Won: ' + str(score) ,[400,80],18 , "Black")

    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric