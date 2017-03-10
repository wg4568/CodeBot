with open("data.txt") as file:
	raw = file.read()
	raw = raw.split("-----\n")[-1:][0].split("\n")
	print raw

import math, pygame, sys
from pygame.locals import *

data = []
coords = []

def pot_to_rad(val):
	# 300 1900 3600
	val -= 300
	val -= 1500
	val *= 0.06
	return math.radians(val)

for dp in raw:
	try:
		rot, dis = dp.split(", ")
		rot, dis = map(int, [rot, dis])
		rot = pot_to_rad(rot)
		data.append([rot, dis])
	except Exception as e:
		print "\"%s\" Error: %s" % (dp, e)

points = []

scale = 0.1
for dp in data:
	x = (dp[1] * scale) * math.sin(dp[0])
	y = (dp[1] * scale) * math.cos(dp[0])
	points.append([x, y])

print points

def run_game():
	pygame.init()

	SIZE = (500, 500)
	BG_COLOUR = (255, 255, 255)

	screen = pygame.display.set_mode(SIZE)
	clock = pygame.time.Clock()

	while True:
		time_passed = clock.tick(30)
		for event in pygame.event.get():
			if event.type == QUIT:
				exit_game()

		screen.fill(BG_COLOUR)
		pygame.draw.ellipse(screen, (0, 0, 255), [250, 250, 10, 10])
		for point in points:
			x = int(point[0] + 255)
			y = SIZE[1] - int(point[1] + 255)
			pygame.draw.ellipse(screen, (255, 0, 0), [x, y, 5, 5])
		pygame.display.update()

def exit_game():
	sys.exit()

if __name__ == "__main__":
	run_game()
