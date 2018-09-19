TARGET_FPS = 30
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
HLF_WIDTH = SCREEN_WIDTH / 2
HLF_HEIGHT = SCREEN_HEIGHT / 2

PHYS_VEL_ITER = 10
PHYS_POS_ITER = 10

DEBUG_KEEP_FPS = False
DEBUG_DRAW = True

SNAKE_LEN = 10

NET_SIZES = [SNAKE_LEN - 1, 10, 6, SNAKE_LEN - 1]

GEN_LIFE_TIME = 10
GEN_POPULATION = 128
GEN_ERAS = 200

CROSSOVER_POINTS = 6

MUTATION_RATE = 15 #percentage chance of mutation for each weight
MUTATION_FACTOR = 1.6

FITNESS_SCALE = 3.1
FITNESS_SCALE_PARENT = 5