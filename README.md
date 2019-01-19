**# game_play**

<!DOCTYPE html>
<html>
  <body>
Functions in Python for adversarial game playing including minimax and alpha-beta pruning.<br/>
Only bg2625_ai.py contains my work. All the other files are supporting documents which were provided for the assignment.
The project creates an AI player for the game Reversi, also known as Othello. After downloading the files, the game can be run using the following command:<br/>

`$python othello_gui.py randy_ai.py bg2625_ai.py` for 2 AI players and <br/>
`$python othello_gui.py randy_ai.py` if you want to play against an AI player. <br/>

`randy` is an AI player that selects a random move. <br/>

Description of the files:
- othello_gui.py - Contains a simple graphical user interface (GUI) for Othello. <br/>
- othello_game.py - Contains the game "manager", which stores the current game state and communicates with different player AIs.<br/>
- othello_shared.py - Functions for computing legal moves, captured disks, and successor game states. These are shared between the game manager, the GUI and the AI players. <br/>
- randy_ai.py - Randy is an "AI" player that randomly selects a legal move.<br/>
- bg2625_ai.py - My AI player.`<br/>

`compute_utility(board, color)` computes the utility of the given board state (represented as a tuple of tuples) from the perspective of the player "color" (1 for dark, 2 for light) <br/>
`select_move_minimax(board, color)` selects the action that leads to the state with the highest minimax value. <br/>
`minimax_max_node(board, color)` and `minimax_min_node(board, color)` are used recursively to implement `select_move_minimax(board, color)`. <br/>
`select_move_alphabeta(board, color)` is impolemented for alpha-beta pruning using the following funcrions: `alphabeta_min_node(board, color, alpha, beta)` and `alphabeta_max_node(board,color, alpha, beta)` which are used recursively.<br/>
Alpha-beta pruning is implemeented so that states with better utilities are explored first. <br/>
States whose utilities have been computed are cached, to avoid the overhead of computing them again. <br/>
The level and limit for the search can be controlled using the `level` and `limit` parameters in the modified version of `alphabeta_min_node()` and `alphabeta_max_node()`. <br/>


</body>
</html>
