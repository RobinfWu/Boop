# Boop
An inplementation of a two-player abstract strategy board game known as Boop.

**Game Design:** Scott Brady
**Illustrations:** Curt Covert

![image](https://github.com/RobinfWu/Boop/assets/8204576/a55beb46-9a1a-4d03-bd21-77c58a7ce26d)

Boop is played on a 6x6 board (the bed) where each player starts out with 8 kittens where they takes turn placing on any empty cell:

![image](https://github.com/RobinfWu/Boop/assets/8204576/21cc7583-481f-4dfc-ba89-9e2f2f69c04c)

The signature mechanic of this game to boop neighboring kittens - regardless if it's yours or the opponent's. Any kitten placed on the board will boop any neighboring kitten one square away, including horizontal, vertical, and diagonal. This mechanic does not cascade.

![image](https://github.com/RobinfWu/Boop/assets/8204576/e5834b9a-2163-44e0-b48f-e5d2e80c3331)

When three kittens of the same color end up in a row (horizontal, vertical, or diagonal), they get taken off the board, promoted to Cats in the player's reserves. 

![image](https://github.com/RobinfWu/Boop/assets/8204576/58da4120-fcb4-475b-810d-9283800c41e0)

Cats can do anything a kitten can do except that a kitten cannot boop a cat. Conversely, a cat can boop other kittens and other cats.

Winning condition: Getting three Cats in a row. Or, getting all eight cats on the board.


