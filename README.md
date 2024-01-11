# Chess-Engine
My Python Chess Engine ♔

_**How to play:**_

  Simply run the main.exe provided in the repository. 
 
_**Setting up the game:**_
   
  The board is initialy stored as a 2D list representing an 8x8 grid. From there, the list 
  can be accessed by indexing the row and column to access a specific location on the board.
  
  The GUI was largely implemented using the Pygame library to handle all user inputs on screen. 
    
   ![image](https://github.com/nasrAnthony/Chess-Engine/assets/132410219/4c5ecafa-e942-495f-9d76-ced641e0706c)


_**Getting all legal moves:**_

  Legal moves are determined using an Arbitter class that parses the board looking for 
  possible squares and returns a list of coordinates the specific piece can move to 
  all while adhering to the rules of Chess. 

  When the player clicks on a piece, possible moves are highlighted as orange squares on the board. 
  
   ![image](https://github.com/nasrAnthony/Chess-Engine/assets/132410219/0fe76247-d877-4912-b499-712e92edc2fa)
   ![image](https://github.com/nasrAnthony/Chess-Engine/assets/132410219/f73f61bf-1005-4e01-a85b-a977dac6d1e8)
   ![image](https://github.com/nasrAnthony/Chess-Engine/assets/132410219/b7f06602-fac6-4629-989d-0ce206d5a01b)

  The user can right click to undo the drag once a piece is selected, then chose another piece. 
  Pieces are also not allowed to move if that would cause a check on their king. Hence, they would be a pinned piece. 

  When a check occurs from the opponent, it is highlighted in red when selecting the next move. All valid moves will collapse
  to only the ones that will save the player's king from the opponent threat when the next move is selected. 
  
  Pawn on c2 possible moves:
  
   ![image](https://github.com/nasrAnthony/Chess-Engine/assets/132410219/59b41b67-313d-42f7-997b-9b00e059bec3)
   
  Queen on d3 possible moves:
  
   ![image](https://github.com/nasrAnthony/Chess-Engine/assets/132410219/fa092cbe-1f11-446b-9e42-35a7d68f906b)

  Additionally, the engine allows for castling short-side, and long-side if all rules are respected.
  
   ![image](https://github.com/nasrAnthony/Chess-Engine/assets/132410219/d8bfdd03-3aab-4e2a-9650-e44dc8cf6e4f)
   ![image](https://github.com/nasrAnthony/Chess-Engine/assets/132410219/2c6053c7-cf54-48ac-a5b1-eaab25e8b134)

  Once checkmate/stalemate occurs, the terminal will print the winner and you press the Reset button to play again.

   White checkmates black:
   
   ![image](https://github.com/nasrAnthony/Chess-Engine/assets/132410219/b7acddfb-3f29-4ea8-b805-6e66279e6527)

   Resulting terminal output:
   
   ![image](https://github.com/nasrAnthony/Chess-Engine/assets/132410219/ea701bed-69ef-441e-bd70-c56c0c1e212f)

_**The AI:**_

  The engine opperates based off a minmax approach. When the player makes a move, it iterates through all of its possible moves.
  Each possible move is then made on a fake board in memory as to not alter the main board displayed to the user. From there, 
  the engine will determine the best move for white if that specific move is made. The goal is to select the move which will give 
  the lowest evaluation after the opponent's next move. 

  When evaluating the board, the engine will parse through all pieces on the board and subtract the value of black pieces, and add 
  add the value of white pieces. The evaluation is 0.0 upon starting a game. Material advantage directly corelates with the color of the player. 
  A negative evaluation will point to black having an advantage, while a positive value will point to white having an advantage. 
  This relation is why the engine aims to make the move that will induce the lowest evaluation (best for black) assuming the opponent will 
  make the best move in return. 
  
_**Improvements:**_

  The engine is still a work in progress. Some things I'm working on changing/improving: 
  
   1 - Implementing a bitboard approach to representing the board/current position. 
   
   2 - Increasing speed at which valid moves are computed. (Will help speed up the AI)
   
   3 - Add more bias to better positioned pieces. (A rook with no valid moves is worth far less than a rook that controls a file). 
   
   4 - Implement recursive minmax. (This will better the AI's decision making by increasing the depth of recursion.)
