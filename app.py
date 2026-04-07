import streamlit as st
import random
import graphviz
import json
import os

# ==========================================
# 1. THE FSM AGENT (Loads from JSON)
# ==========================================
class FSMAgent:
    def __init__(self, dna):
        self.dna = dna
        self.num_states = len(dna)
        self.current_state = 0
        self.move_to_index = {'R': 1, 'P': 2, 'S': 3}

    def get_action(self): 
        return self.dna[self.current_state][0]
    
    def update_state(self, opponent_move):
        self.current_state = self.dna[self.current_state][self.move_to_index[opponent_move]]
        
    def reset(self): 
        self.current_state = 0

def load_dna(filepath='champion_dna.json'):
    if not os.path.exists(filepath):
        st.error(f"🚨 Missing File: '{filepath}' not found. Please run agent.py first!")
        st.stop()
    with open(filepath, 'r') as f:
        raw_dna = json.load(f)
        # JSON saves dictionary keys as strings ("0", "1"). Convert them back to integers.
        return {int(k): v for k, v in raw_dna.items()}

# ==========================================
# 2. ANT COLONY OPTIMIZATION BOT
# ==========================================
class ACOAgent:
    def __init__(self):
        self.moves = ['R', 'P', 'S']
        self.beats = {'R': 'P', 'P': 'S', 'S': 'R'}
        self.pheromones = {
            'R': {'R': 1.0, 'P': 1.0, 'S': 1.0},
            'P': {'R': 1.0, 'P': 1.0, 'S': 1.0},
            'S': {'R': 1.0, 'P': 1.0, 'S': 1.0}
        }
        self.evaporation_rate = 0.85 
        self.deposit_amount = 2.0    
        self.last_human_move = None

    def get_action(self):
        if not self.last_human_move: 
            return random.choice(self.moves)
        trails = self.pheromones[self.last_human_move]
        predicted_move = max(trails, key=trails.get)
        return self.beats[predicted_move]

    def update_pheromones(self, human_move):
        if self.last_human_move:
            for m1 in self.moves:
                for m2 in self.moves:
                    self.pheromones[m1][m2] *= self.evaporation_rate
            self.pheromones[self.last_human_move][human_move] += self.deposit_amount
        self.last_human_move = human_move

# ==========================================
# 3. STREAMLIT UI
# ==========================================
st.set_page_config(page_title="Evolutionary RPS", layout="wide")

# Initialize Bots and Scores in Session State
if 'champion' not in st.session_state:
    dna = load_dna()
    st.session_state.champion = FSMAgent(dna=dna)
    st.session_state.aco_bot = ACOAgent()
    st.session_state.fsm_scores = {'Human': 0, 'Bot': 0, 'Ties': 0}
    st.session_state.aco_scores = {'Human': 0, 'Bot': 0, 'Ties': 0}

st.title("🤖 Evolutionary Rock, Paper, Scissors")
tab1, tab2, tab3 = st.tabs(["🎮 Play Champion FSM", "🧠 Visualize FSM Brain", "🐜 Challenge: ACO Swarm Bot"])

beats = {'R': 'P', 'P': 'S', 'S': 'R'}
full_name = {'R': 'Rock', 'P': 'Paper', 'S': 'Scissors'}

# --- TAB 1: PLAY FSM ---
with tab1:
    st.header("Vs. The Evolved FSM Champion")
    st.write("This bot is driven by the exact DNA you evolved offline.")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.subheader("Make your move:")
        # Draw buttons unconditionally to prevent disappearing UI
        r_clicked = st.button("🪨 Rock", key="f1")
        p_clicked = st.button("📄 Paper", key="f2")
        s_clicked = st.button("✂️ Scissors", key="f3")
        
        if r_clicked: human_move = 'R'
        elif p_clicked: human_move = 'P'
        elif s_clicked: human_move = 'S'
        else: human_move = None

    if human_move:
        bot_move = st.session_state.champion.get_action()
        
        if human_move == bot_move:
            result = "It's a Tie!"
            st.session_state.fsm_scores['Ties'] += 1
        elif beats[human_move] == bot_move:
            result = "Champion Wins!"
            st.session_state.fsm_scores['Bot'] += 1
        else:
            result = "You Win!"
            st.session_state.fsm_scores['Human'] += 1
            
        st.session_state.champion.update_state(human_move)
        
        with col2:
            st.write(f"You: **{full_name[human_move]}**")
            st.write(f"Bot: **{full_name[bot_move]}**")
            st.subheader(result)

    with col3:
        st.metric("Your Score", st.session_state.fsm_scores['Human'])
        st.metric("Bot Score", st.session_state.fsm_scores['Bot'])

# --- TAB 2: VISUALIZE FSM ---
with tab2:
    st.header("Live FSM Visualization")
    current = st.session_state.champion.current_state
    st.write(f"**Active State:** Node {current}")
    st.info("Play a move in Tab 1, then come back here to see how the active node changes based on your input!")
    
    dot = graphviz.Digraph(engine='dot')
    dot.attr(rankdir='LR', size='8,5')
    
    for state_id, genes in st.session_state.champion.dna.items():
        color = 'lightgreen' if state_id == current else 'lightblue'
        dot.node(str(state_id), f"State {state_id}\nPlays: {genes[0]}", style='filled', fillcolor=color)
            
    for state_id, genes in st.session_state.champion.dna.items():
        dot.edge(str(state_id), str(genes[1]), label='If R', color='gray')
        dot.edge(str(state_id), str(genes[2]), label='If P', color='gray')
        dot.edge(str(state_id), str(genes[3]), label='If S', color='gray')

    st.graphviz_chart(dot)

# --- TAB 3: ACO BOT ---
with tab3:
    st.header("Vs. Real-Time Ant Colony Optimization")
    st.write("This bot learns from scratch using pheromone trails based on your real-time transitions.")
    
    col_a, col_b, col_c = st.columns([1, 1, 2])
    with col_a:
        st.subheader("Make your move:")
        # Draw buttons unconditionally
        a_r_clicked = st.button("🪨 Rock", key="a1")
        a_p_clicked = st.button("📄 Paper", key="a2")
        a_s_clicked = st.button("✂️ Scissors", key="a3")
        
        if a_r_clicked: a_move = 'R'
        elif a_p_clicked: a_move = 'P'
        elif a_s_clicked: a_move = 'S'
        else: a_move = None

    if a_move:
        bot = st.session_state.aco_bot
        b_move = bot.get_action()
        bot.update_pheromones(a_move)
        
        if a_move == b_move:
            res = "It's a Tie!"
            st.session_state.aco_scores['Ties'] += 1
        elif beats[a_move] == b_move:
            res = "Swarm Wins!"
            st.session_state.aco_scores['Bot'] += 1
        else:
            res = "You Win!"
            st.session_state.aco_scores['Human'] += 1

        with col_b:
            st.write(f"You: **{full_name[a_move]}**")
            st.write(f"Swarm: **{full_name[b_move]}**")
            st.subheader(res)

    with col_c:
        st.metric("Your Score", st.session_state.aco_scores['Human'])
        st.metric("Swarm Score", st.session_state.aco_scores['Bot'])
        
    st.subheader("Live Pheromone Matrix")
    st.dataframe(st.session_state.aco_bot.pheromones, use_container_width=True)