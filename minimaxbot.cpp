#include<vector>
using std::vector;

// Board Class
class board_class{
private:
	int board_details[9]={0, 0, 0, 0, 0, 0, 0, 0, 0};
	int turn=1;
	vector<int> moves_played;

public:
	board_class(){}

	void get_board_details(int *brd){
		for(int i=0; i<9; i++) brd[i]=board_details[i];
	}

	int get_turn(){
		return turn;
	}

	vector<int> get_possible_moves(){
		vector<int> possible_moves;
		for(int i=0; i<9; i++) 
			if(board_details[i]==0) possible_moves.push_back(i);
		return possible_moves;
	}

	int get_winner(){
		for(int i=0; i<3; i++){
			if(board_details[3*i]!=0 && board_details[3*i]==board_details[3*i+1]
				&& board_details[3*i]==board_details[3*i+2]) return board_details[3*i];
			if(board_details[i]!=0 && board_details[i]==board_details[i+3]
				&& board_details[i]==board_details[i+6]) return board_details[i];
		}
		if(board_details[4]!=0 && board_details[4]==board_details[0]
			&& board_details[4]==board_details[8]) return board_details[4];
		if(board_details[4]!=0 && board_details[4]==board_details[2]
			&& board_details[4]==board_details[6]) return board_details[4];

		return 0;
	}

	bool is_full(){
		return moves_played.size()>8;
	}

	void update_board(int move){	
		if(move<0 || move>8) return;
		if(board_details[move]!=0) return;
		board_details[move]=turn;
		turn=-turn;
		moves_played.push_back(move);
	}

	void undo_move(){
		if(moves_played.size()<1) return;
		int move=moves_played[moves_played.size()-1];
		board_details[move]=0;
		turn=-turn;
		moves_played.pop_back();
	}
};

int minimax_algo(board_class eval_brd, int move){
	eval_brd.update_board(move);
	int current_turn=eval_brd.get_turn(); 
	int best_eval= current_turn==1 ? -100 : 100;

	if(eval_brd.get_winner()!=0){
		eval_brd.undo_move();
		return best_eval;
	}
	if(eval_brd.is_full()){
		eval_brd.undo_move();
		return 0;
	}

	vector<int> possible_moves=eval_brd.get_possible_moves();
	int eval;

	for(int mv: possible_moves){
		eval=minimax_algo(eval_brd, mv);
		if((eval>best_eval && current_turn==1) || (eval<best_eval && current_turn==-1))
			best_eval=eval;
		if((current_turn==1 && best_eval==100) || (current_turn==-1 && best_eval==-1))
			break;
	}
	eval_brd.undo_move();
	return best_eval;
}

static board_class Board;

extern "C"{
void reset_board(){
	Board= board_class();
}

int get_turn_and_board(int *brd){
	Board.get_board_details(brd);
	return Board.get_turn();
}

void play_move(int move){
	Board.update_board(move);
}

int get_state(){
	int winner=Board.get_winner();
	bool filled=Board.is_full();
	if(winner!=0) return winner;
	if(filled) return 2;
	return 0;
}

void undo_board(){
	Board.undo_move();
}

int get_move_by_bot(){
	vector<int> possible_moves=Board.get_possible_moves();
	int best_move=possible_moves[0];

	int current_turn=Board.get_turn(); 
	int best_eval= current_turn==1 ? -100 : 100;
	int evaluation;

	for(int move: possible_moves){
		evaluation=minimax_algo(Board, move);
		if((evaluation>best_eval && current_turn==1) || (evaluation<best_eval && current_turn==-1)){
			best_eval=evaluation;
			best_move=move;
		}
		if((current_turn==1 && best_eval==100) || (current_turn==-1 && best_eval==-1))
			break;
	}
	return best_move;
}
}
