# Q-Learning

- Q-learning is a reinforcement learning 

## Reinforcement learning

- **agent**
- A set of state **$S$**
- A set of actions **$A$**
- By performing an action $$a \in A$$, the agent transitions from state to state
- Executing an action in a specific state provides the agent with a reward (a numerical score)
- The **goal** of the agent is to maximize its total (future) reward.


$$Q(s_t, a_t) \leftarrow (1 - \alpha) \cdot Q(s_t, a_t) + \alpha \cdot (r_t + \gamma \cdot \max_a Q(s_{t+1}, a))$$

- $r$ is the reward observed for state $s_{f}$. 
- $\alpha$ is the learning rate
- $\gamma$ is the discount factor. Determines the importance of future rewards. 


## Markov Decision Processes (MDPs)


## Policy is a map from state to action





