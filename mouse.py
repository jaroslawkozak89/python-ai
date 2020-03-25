#Reinforcement learning ai project
#Class MouseEnv creates a maze with mouse randomly placed, the task is to find a cheese
#Agent is modeled using reinforcement q-learning method
import random

class MouseEnv:

	def __init__(self):
		self.reset()

	def reset(self):

		self.playground = [["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
						   ["W", "C", "P", "P", "P", "W", "P", "P", "P", "P", "W", "W"],
		                   ["W", "W", "W", "W", "P", "W", "W", "P", "W", "P", "P", "W"],
		                   ["W", "P", "P", "P", "P", "P", "W", "W", "W", "W", "P", "W"],
		                   ["W", "P", "W", "W", "W", "P", "W", "P", "P", "P", "P", "W"],
		                   ["W", "P", "P", "P", "W", "W", "W", "P", "W", "W", "P", "W"],
		                   ["W", "W", "W", "P", "P", "P", "P", "P", "W", "P", "P", "W"],
		                   ["W", "P", "W", "W", "P", "W", "W", "W", "W", "P", "W", "W"],
		                   ["W", "P", "P", "W", "P", "W", "P", "W", "P", "P", "P", "W"],
		                   ["W", "P", "W", "W", "P", "W", "P", "W", "W", "W", "P", "W"],
		                   ["W", "P", "P", "P", "P", "W", "P", "P", "P", "P", "P", "W"],
		                   ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"]]
		self.mouse_position = []
		self.actions = ["up", "right", "down", "left"]
		self.rewards = []
		self.epoch_finished = False
		self.place_mouse()

		return self.mouse_position

	def place_mouse(self):
		self.mouse_position = [random.randrange(0, len(self.playground)), random.randrange(0, len(self.playground[0]))]
		while self.playground[self.mouse_position[0]][self.mouse_position[1]] != "P":
			self.mouse_position = [random.randrange(0, len(self.playground)), random.randrange(0, len(self.playground[0]))]

		self.playground[self.mouse_position[0]][self.mouse_position[1]] = "M"


		for i in range(len(self.playground)):
			self.rewards.append([])
			for j in range(len(self.playground[0])):
				if self.playground[i][j] == "C":
					self.rewards[i].append(100)
				elif self.playground[i][j] == "W":
					self.rewards[i].append(-100)
				else:
					self.rewards[i].append(-1)

	def create_q_table(self):
		q_table = [[],[]]
		for i in range(len(self.playground)):
			for j in range(len(self.playground[0])):
				q_table[0].append([i, j])
				q_table[1].append([0, 0, 0, 0])

		return q_table

	def random_action(self):
		return random.randrange(0, len(self.actions))

	def action(self, action):
		chosen_action = self.actions[action]
		if chosen_action == "up":
			chosen_action = [[self.mouse_position[0]-1, self.mouse_position[1]], self.playground[self.mouse_position[0]-1][self.mouse_position[1]]]
		if chosen_action == "right":
			chosen_action = [[self.mouse_position[0], self.mouse_position[1]+1], self.playground[self.mouse_position[0]][self.mouse_position[1]+1]]
		if chosen_action == "down":
			chosen_action = [[self.mouse_position[0]+1, self.mouse_position[1]], self.playground[self.mouse_position[0]+1][self.mouse_position[1]]]
		if chosen_action == "left":
			chosen_action = [[self.mouse_position[0], self.mouse_position[1]-1], self.playground[self.mouse_position[0]][self.mouse_position[1]-1]]

		if chosen_action[1] != "W":
			if chosen_action[1] == "C":
				self.epoch_finished = True
			self.playground[self.mouse_position[0]][self.mouse_position[1]] = "P"
			self.mouse_position = chosen_action[0] 
			self.playground[self.mouse_position[0]][self.mouse_position[1]] = "M"
			reward = self.rewards[self.mouse_position[0]][self.mouse_position[1]]
			return reward, self.mouse_position, self.epoch_finished
		else:
			reward = self.rewards[chosen_action[0][0]][chosen_action[0][1]]
			return reward, self.mouse_position, self.epoch_finished

	def draw(self):
		playground = u""
		for i in self.playground:
			for j in i:
				if j == "C":
					playground += "C"
				if j == "P":
					playground += "\u25A1"
				if j == "W": 
					playground += "\u2588"
				if j == "M":
					playground += "M"
			playground += "\n"
		print(playground)

		
class ReinforcementLearning:

	def __init__(self, env, q_table, learning_rate, discount_rate, epsilon):
		self.env = env
		self.q_table = q_table
		self.learning_rate = learning_rate
		self.discount_rate = discount_rate
		self.epsilon = epsilon
		self.current_epoch_done = False

	def train(self, train_epochs):
		for i in range(train_epochs):
			state = self.env.reset()
			self.current_epoch_done = False

			while not self.current_epoch_done:
				if random.uniform(0,1) < self.epsilon:
					next_action = self.env.random_action()
				else:
					next_action = self.q_table[1][self.q_table[0].index(state)].index(max(self.q_table[1][self.q_table[0].index(state)]))

				reward, next_state, self.current_epoch_done = self.env.action(next_action)

				old_value = q_table[1][q_table[0].index(state)][next_action]
				next_max = max(q_table[1][q_table[0].index(next_state)])

				new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (reward + self.discount_rate * next_max)
				q_table[1][q_table[0].index(state)][next_action] = new_value

				state = next_state

			if i % 1 == 0:
				print(f"Episode: {i}")

		print("Training Complete.")


	def evaluate(self, eval_epochs):
		for _ in range(eval_epochs):
			state = self.env.reset()
			self.current_epoch_done = False

			while not self.current_epoch_done:
				next_action = self.q_table[1][self.q_table[0].index(state)].index(max(self.q_table[1][self.q_table[0].index(state)]))
				reward, state, self.current_epoch_done = self.env.action(next_action)
				self.env.draw()

env = MouseEnv()

q_table = env.create_q_table()
learning_rate = 0.1
discount_rate = 0.5
epsilon = 0.1
train_epochs = 10000
eval_epochs = 10

model = ReinforcementLearning(env, q_table, learning_rate, discount_rate, epsilon)

model.train(train_epochs)

model.evaluate(eval_epochs)


