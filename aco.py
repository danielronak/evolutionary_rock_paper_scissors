import random

class ACOAgent:
    def __init__(self):
        self.moves = ['R', 'P', 'S']
        self.beats = {'R': 'P', 'P': 'S', 'S': 'R'}
        
        # The Map: Tracks paths from [Previous Move] -> [Next Move]
        # All paths start with 1.0 pheromone
        self.pheromones = {
            'R': {'R': 1.0, 'P': 1.0, 'S': 1.0},
            'P': {'R': 1.0, 'P': 1.0, 'S': 1.0},
            'S': {'R': 1.0, 'P': 1.0, 'S': 1.0}
        }
        
        self.evaporation_rate = 0.85 # Evaporate 15% of old trails each turn
        self.deposit_amount = 2.0    # Add 2.0 pheromones to the chosen path
        self.last_human_move = None

    def get_action(self):
        # First turn: guess randomly
        if not self.last_human_move: 
            return random.choice(self.moves)
            
        # Look at the trails leaving the human's last move
        trails = self.pheromones[self.last_human_move]
        
        # Predict human's next move based on the strongest pheromone
        predicted_move = max(trails, key=trails.get)
        
        # Play the mathematical counter
        return self.beats[predicted_move]

    def update_pheromones(self, human_move):
        if self.last_human_move:
            # 1. Evaporate all trails slightly (forget distant past)
            for m1 in self.moves:
                for m2 in self.moves:
                    self.pheromones[m1][m2] *= self.evaporation_rate
                    
            # 2. Deposit heavy pheromones on the path just taken
            self.pheromones[self.last_human_move][human_move] += self.deposit_amount
            
        self.last_human_move = human_move

    def print_pheromones(self):
        print("\n--- Current Pheromone Trails ---")
        for m1 in self.moves:
            trails = [f"->{m2}: {self.pheromones[m1][m2]:.2f}" for m2 in self.moves]
            print(f"From {m1} | {' | '.join(trails)}")
        print("--------------------------------\n")

# ==========================================
# TEST THE SWARM IN THE TERMINAL
# ==========================================
if __name__ == "__main__":
    print("=== VS. THE ANT COLONY ===")
    print("Type R, P, or S. Type Q to quit.")
    
    bot = ACOAgent()
    user_score = bot_score = 0
    beats = {'R': 'P', 'P': 'S', 'S': 'R'}
    
    while True:
        bot_move = bot.get_action()
        human_move = input("\nYour move (R/P/S): ").strip().upper()
        
        if human_move == 'Q': break
        if human_move not in ['R', 'P', 'S']: continue
            
        # Score it
        if human_move == bot_move:
            print(f"Bot played {bot_move} - Tie!")
        elif beats[human_move] == bot_move:
            print(f"Bot played {bot_move} - Bot Wins!")
            bot_score += 1
        else:
            print(f"Bot played {bot_move} - You Win!")
            user_score += 1
            
        # Update and print trails
        bot.update_pheromones(human_move)
        bot.print_pheromones()
        print(f"Score: You {user_score} - {bot_score} Bot") 