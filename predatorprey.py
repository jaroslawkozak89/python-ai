import arcade
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Predator Prey Behaviour"

random.seed()

creatures = [["predator", 20, (255, 0, 0)],
             ["prey", 8, (0, 128, 0)],
             ["prey", 8, (0, 128, 0)],
             ["prey", 8, (0, 128, 0)],
             ["prey", 8, (0, 128, 0)],
             ["prey", 8, (0, 128, 0)],
             ["prey", 8, (0, 128, 0)],
             ["prey", 8, (0, 128, 0)],
             ["prey", 8, (0, 128, 0)],
             ["prey", 8, (0, 128, 0)],
             ["prey", 8, (0, 128, 0)],
             ["preyleader", 12, (34, 139, 34)]]


SPEED = [-2, -1.9, -1.8, -1.7, -1.6, -1.5, -1.4, -1.3, -1.2, -1.1, -1, 0, 1, 1.1, 1.2, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]

class Ball:
    def __init__(self, role, size, color):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.steer_x = 0
        self.steer_y = 0
        self.role = role
        self.size = size
        self.color = color
        self.state = "randomlywandering"

    def wander(self):

        if self.steer_x != self.change_x:
            if self.steer_x > self.change_x:
                self.change_x += 0.05
            else:
                self.change_x -= 0.05

        if self.steer_y != self.change_y:
            if self.steer_y > self.change_y:
                self.change_y += 0.05
            else:
                self.change_y -= 0.05

        self.x += self.change_x
        self.y += self.change_y

        if random.random() < 0.01:
            self.steer_x = SPEED[random.randint(0,len(SPEED)-1)]
            self.steer_y = SPEED[random.randint(0,len(SPEED)-1)]


    def seek(self, preyX, preyY):
    
        if preyX > self.x:
            self.change_x = 2
        elif preyX < self.x:
            self.change_x = -2
        else: 
            self.change_x = 0

        if preyY > self.y:
            self.change_y = 2
        elif preyY < self.y:
            self.change_y = -2
        else: 
            self.change_y = 0
   
        self.x += self.change_x
        self.y += self.change_y

    def flee(self, predatorX, predatorY):
        if predatorX > self.x:
            self.change_x = -2.5
        elif predatorX < self.x:
            self.change_x = 2.5
        else: 
            self.change_x = 0

        if predatorY > self.y:
            self.change_y = -2.5
        elif predatorY < self.y:
            self.change_y = 2.5
        else: 
            self.change_y = 0
   
        self.x += self.change_x
        self.y += self.change_y

    def avoid_obstacles(self):

        self.x += self.change_x
        self.y += self.change_y

        if self.x < self.size + 50:
            self.change_x += 0.1

        if self.y < self.size + 50:
            self.change_y += 0.1

        if self.x > SCREEN_WIDTH - self.size - 50:
            self.change_x -= 0.1

        if self.y > SCREEN_HEIGHT - self.size - 50:
            self.change_y -= 0.1

    def follow_leader(self, leaderX, leaderY, leaderSize, leaderDistance):

        if leaderDistance >30:
            if leaderX > self.x:
                self.change_x = 2
            elif leaderX < self.x:
                self.change_x = -2
            else: 
                self.change_x = 0

            if leaderY > self.y:
                self.change_y = 2
            elif leaderY < self.y:
                self.change_y = -2
            else: 
                self.change_y = 0
        elif leaderDistance < leaderSize*2:
            self.change_x = 0
            self.change_y = 0
        else:
            if leaderX > self.x:
                self.change_x = 1
            elif leaderX < self.x:
                self.change_x = -1
            else: 
                self.change_x = 0

            if leaderY > self.y:
                self.change_y = 1
            elif leaderY < self.y:
                self.change_y = -1
            else: 
                self.change_y = 0

        self.x += self.change_x
        self.y += self.change_y

def make_ball(role, size, color):

    ball = Ball(role, size, color)

    ball.x = random.randrange(ball.size+50, SCREEN_WIDTH - ball.size-50)
    ball.y = random.randrange(ball.size+50, SCREEN_HEIGHT - ball.size-50)

    ball.change_x = SPEED[random.randint(0,len(SPEED)-1)]
    ball.change_y = SPEED[random.randint(0,len(SPEED)-1)]

    return ball

class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.ball_list = []

        for creature in creatures:
            ball = make_ball(creature[0], creature[1], creature[2])
            self.ball_list.append(ball)

    def on_draw(self):

        arcade.start_render()

        for ball in self.ball_list:
            arcade.draw_circle_filled(ball.x, ball.y, ball.size, ball.color)

    def on_update(self, delta_time):

        for ball in self.ball_list:
            leaderDistance = SCREEN_WIDTH + SCREEN_HEIGHT
            predatorDistance = SCREEN_WIDTH + SCREEN_HEIGHT
            closestPrey = len(creatures)

            if ball.role == "prey":
                leaderDistance = math.sqrt((ball.x - self.ball_list[len(creatures)-1].x)**2 + (ball.y - self.ball_list[len(creatures)-1].y)**2)
                predatorDistance = math.sqrt((ball.x - self.ball_list[0].x)**2 + (ball.y - self.ball_list[0].y)**2)
            elif ball.role == "predator": 
                for i in self.ball_list:
                    if (predatorDistance > math.sqrt((ball.x - i.x)**2 + (ball.y - i.y)**2)) and (math.sqrt((ball.x - i.x)**2 + (ball.y - i.y)**2) != 0):
                        predatorDistance = math.sqrt((ball.x - i.x)**2 + (ball.y - i.y)**2)
                        closestPrey = self.ball_list.index(i)
            else:
                predatorDistance = math.sqrt((ball.x - self.ball_list[0].x)**2 + (ball.y - self.ball_list[0].y)**2)

            if ball.role == "predator" and predatorDistance < 150:
                ball.state = "preyclose"
            elif ball.x < ball.size + 50 or ball.y < ball.size + 50 or ball.x > SCREEN_WIDTH - ball.size - 50 or ball.y > SCREEN_HEIGHT - ball.size - 50:
                ball.state = "obstacledetected"
            elif (ball.role == "prey" or ball.role == "preyleader") and predatorDistance < 150:
                ball.state = "predatorclose"
            elif ball.role == "prey" and leaderDistance < 100:
                ball.state = "leaderclose"
            else:
                ball.state = "randomlywandering"

            if ball.state == "preyclose":
                ball.seek(self.ball_list[closestPrey].x, self.ball_list[closestPrey].y)
            elif ball.state == "predatorclose":
                ball.flee(self.ball_list[0].x, self.ball_list[0].y)
            elif ball.state == "leaderclose":
                ball.follow_leader(self.ball_list[len(creatures)-1].x, self.ball_list[len(creatures)-1].y, self.ball_list[len(creatures)-1].size, leaderDistance)
            elif ball.state == "obstacledetected":
                ball.avoid_obstacles()
            else:
                ball.wander()


def main():
    MyGame()
    arcade.run()


if __name__ == "__main__":
    main()