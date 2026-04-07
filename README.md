# Evolutionary Rock, Paper, Scissors

This project explores human predictability and algorithmic adaptation through the lens of a simple game: Rock, Paper, Scissors. It features two distinct Artificial Intelligence agents, each utilizing a different branch of evolutionary computing to exploit human patterns.

The frontend is built with Streamlit, providing a live interface to play against the agents and visualize their internal decision-making processes.

## Agent 1: The Co-Evolved Finite State Machine (FSM)

The first agent was trained entirely offline using **Competitive Co-Evolution**. 

In standard evolutionary algorithms, a population evolves to solve a static environment. In co-evolution, two separate populations are pitted against each other. This creates an evolutionary "arms race" (often related to the Red Queen Hypothesis). When Population A evolves a dominant strategy, Population B's fitness drops until it randomly mutates a counter-strategy, forcing Population A to adapt again.

**Implementation:**
* The "DNA" of our agent is a 10-state Finite State Machine. 
* Each state contains an action (Rock, Paper, or Scissors) and three transition pointers based on the opponent's subsequent move. 
* Through crossover (breeding) and mutation, the agents learned to construct complex, cyclical traps.
* The champion of a 1000-generation simulation was extracted and saved to a JSON file, which the Streamlit app now uses for inference.

## Agent 2: Ant Colony Optimization (The Swarm)

While the FSM relies on thousands of generations of pre-training, the second agent utilizes **Ant Colony Optimization (ACO)** to learn in real-time.

ACO is a swarm intelligence algorithm inspired by how ants find the shortest path to food. As ants walk, they leave behind pheromones. Shorter or more successful paths accumulate pheromones faster, attracting more ants, while unused paths evaporate over time.

**Implementation:**
* The agent starts with zero knowledge. The "map" is a simple 3x3 matrix representing the user's move transitions (e.g., playing Rock, then switching to Paper).
* Every time a human plays, the agent deposits a heavy "pheromone" value on that specific transition path.
* Simultaneously, a decay factor is applied to all paths, causing older habits to evaporate.
* By looking at the strongest pheromone trail leading out of the human's last move, the agent predicts the human's next move and plays the mathematical counter. 
* Because humans naturally fall into subconscious patterns (like alternating R-P-R-P), the swarm isolates and exploits these loops within seconds.

## Running the Project Locally

**Prerequisites:**
You will need Python installed, along with the Graphviz system software (required for visualizing the FSM nodes).

1. Clone the repository:
   ```bash
   git clone [https://github.com/danielronak/evolutionary_rock_paper_scissors.git](https://github.com/danielronak/evolutionary_rock_paper_scissors.git)
   cd evolutionary_rock_paper_scissors

2. insall requirements:
    pip install -r requirements.txt

3. run:
   streamlit run app.py