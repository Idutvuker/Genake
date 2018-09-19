from main import *

init_bodies()
snake = Snake()

working = True

weights = np.load("best.npy")

genome = Genome(weights)
snake.setGenome(genome)

for t in range(TARGET_FPS * GEN_LIFE_TIME):
	if (t % 5 == 0):
		snake.act()

	Camera.x = snake.body[0].position.x
	#print(-Camera.x)

	world.Step(TIME_STEP, PHYS_VEL_ITER, PHYS_POS_ITER)

	if debug_draw():
		working = False
		break

print(snake.getFitness())

pygame.quit()

print('Done!')