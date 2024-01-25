A digital, command line-based implementation of the Timeline board game, originally designed by Zygomatic Games and published by Asmodee.

This is intended as practice for an amateur developer, not to substitute the physical game. Please support the original creators and buy their games.

The gameplay loop is as follows:
  On a player's turn, that player selects a card from their hand which represents a historical event, and the year it occurred (hidden to the players).
  That player then selects a spot on the timeline which they believe corresponds to when their event occurred.
  Then, the year of the chosen event card is revealed, indicating if the player was right or not.
  If they're correct, the event card is moved from their hand to the correct place in the timeline, and their turn ends.
  If they're incorrect, the event card is discarded and the player draws a random replacement card from the deck.
Then the next player takes their turn the same way. The game ends when a player has an empty hand at the end of their turn.
The first player to empty their hand by playing a card successfully, wins!

The comment at the top of main.py lists a bunch of potential features which could be added in future versions.
