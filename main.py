import time
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)

from Box2D import *

from network import Network
from genetic import *
from constants import *
from demographic import *

import sys

if DEBUG_DRAW or __name__ != '__main__':
	import pygame
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
	pygame.display.set_caption('Simple pygame example')
	clock = pygame.time.Clock()

world = b2World(gravity=(0, -10), doSleep=True)

class Snake:
	body = []
	joints = [None] * (SNAKE_LEN - 1)

	pos = b2Vec2(0, 1.25)
	node_len = 0.25
	node_wid = 0.15

	joint_bound = 30.0 / 180.0 * b2_pi

	max_val = 0

	def getFitness(self):
		return self.body[0].position.x

	def createJoint(self, bodyA, bodyB):
		return world.CreateRevoluteJoint(
					bodyA=bodyA,
					bodyB=bodyB,
					anchor=bodyB.position + (self.node_len, 0),
					lowerAngle=-self.joint_bound,
					upperAngle=self.joint_bound,
					enableLimit=True,
					maxMotorTorque=10.0,
					motorSpeed=0.0,
					enableMotor=True
					)

	def reset(self):
		max_val = 0
		world.ClearForces()

		for joint in self.joints:
			world.DestroyJoint(joint)

		for i in range(SNAKE_LEN):
			self.body[i].position = self.pos + (-2 * i * self.node_len, 0)
			self.body[i].angle = 0.0
			self.body[i].linearVelocity = (0, 0)
			self.body[i].angularVelocity = 0

			#Head node
			if i == 0:
				continue
			
			self.joints[i - 1] = self.createJoint(self.body[i - 1], self.body[i])

	def setGenome(self, genome):
		self.network.setGenome(genome)


	inp = np.zeros((SNAKE_LEN, 1))
	inp[-1][0] = 1

	def act(self):
		val = self.body[0].position.y
		if val > self.max_val:
			self.max_val = val

		for i in range(SNAKE_LEN - 1):
			self.inp[i][0] = self.joints[i].angle / self.joint_bound

		#print(self.inp)

		output = self.network.feedforward(self.inp)[:,0]
		for i in range(SNAKE_LEN - 1):
			self.joints[i].motorSpeed = output[i]


	def __init__(self):
		node_fix = b2FixtureDef(
				shape=b2PolygonShape(box=(self.node_len, self.node_wid)),
				density=1.5,
				friction=0.5,
				userData=(100,100,100))

		for i in range(SNAKE_LEN):
			self.body.append(world.CreateDynamicBody(allowSleep = False, position = self.pos + (-2 * i * self.node_len, 0)))
			self.body[i].CreateFixture(node_fix)

			#Head node
			if i == 0:
				continue
			
			self.joints[i - 1] = self.createJoint(self.body[i - 1], self.body[i])
			
		self.network = Network()

class Camera:
	PPM = 60.0
	x = 0
	y = HLF_HEIGHT / PPM


def init_bodies():
	ground_fix = b2FixtureDef(shape=b2PolygonShape(box=(100, 1, (90, 0), 0)), density=1, friction=0.3)

	ground_body = world.CreateStaticBody()
	ground_body.CreateFixture(ground_fix)


def draw_world():
	screen.fill((0, 0, 0, 0))
	for body in world.bodies:
		for fixture in body.fixtures:
			shape = fixture.shape
			vertices = [(body.transform * v) * Camera.PPM  for v in shape.vertices]
			vertices = [(v[0] + HLF_WIDTH - Camera.x * Camera.PPM, 
						SCREEN_HEIGHT - (v[1] + HLF_HEIGHT - Camera.y * Camera.PPM))
						for v in vertices]

			color = (255, 255, 255)

			if (fixture.userData != None):
				color = fixture.userData
				pygame.draw.polygon(screen, color, vertices)

			else:
				pygame.draw.polygon(screen, color, vertices)

				for i in range(100):
					x = i * Camera.PPM + HLF_WIDTH - Camera.x * Camera.PPM
					pygame.draw.line(screen, (0, 150, 0), (x, SCREEN_HEIGHT), (x, SCREEN_HEIGHT - (1.5 * Camera.PPM)), 3)


			



def debug_draw():
	#keys = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == QUIT:
			return 1

		#if event.type == pygame.KEYDOWN:
		#	if event.key == pygame.K_SPACE:
		#		snake.network.randomize()

	draw_world()

	pygame.display.flip()

	if DEBUG_KEEP_FPS:
		clock.tick(TARGET_FPS)

	return 0

def evolution(snake):
	epoch_pop = [Individual() for i in range(GEN_POPULATION)]

	for epoch in range(GEN_ERAS):
		for i in range(GEN_POPULATION):
			snake.setGenome(epoch_pop[i].genome)

			for t in range(TARGET_FPS * GEN_LIFE_TIME):
				if (t % 5 == 0):
					snake.act()

				world.Step(TIME_STEP, PHYS_VEL_ITER, PHYS_POS_ITER)

				if DEBUG_DRAW:
					if debug_draw():
						return

			epoch_pop[i].result = snake.getFitness()
			snake.reset()

			#print("%d%%" % (i + 1), end = "\r")

		epoch_pop.sort(reverse = True)

		statistics(epoch_pop, epoch)
		proliferation(epoch_pop)

def main():
	init_bodies()
	snake = Snake()

	old = time.time()

	evolution(snake)

	if DEBUG_DRAW:
		pygame.quit()

	print('Done!')
	print(time.time() - old)

if __name__ == '__main__':
	main()