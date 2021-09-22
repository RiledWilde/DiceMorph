
# Install using ... pip install --upgrade pip ; pip install pygame opencv-python
from contextlib import redirect_stdout
with redirect_stdout(None):
  import pygame

import cv2

def draw(image, game, grid, height, width, die_L) :
  ''' Draw the relevant dice and overlay for the picture. '''

  from math import ceil

  print("The number of dice needed to make this image is: {}.".format(grid[0] * grid[1]))

  # RGB triplet (decimal abbreviation)
  background = [0, 4, 114]
  foreground = [255, 165, 0]

  game.fill(background)
  pygame.display.flip()

  for j in range(grid[1]) :

    yval = j * die_L
    P = (0,yval); Q = (width,yval)
    pygame.draw.line(game, background, P, Q)


  for i in range(grid[0]) :

    xval = i * die_L
    P = (xval,0); Q = (xval,height)
    # [50, 50, 50] would be a dark black
    pygame.draw.line(game, background, P, Q)

  centres = {
    1: [(0,0)], 2: [(-1,1), (1,-1)], 3: [(-1,1), (1,-1), (0,0)],
    4: [(-1,-1), (-1,1), (1,1), (1,-1)], 5: [(-1,-1), (0,0), (-1,1), (1,-1), (1,1)],
    6: [(-1,-1), (-1,1), (1,0), (1,1), (1,-1), (-1,0)]
  }

  for x in range(grid[0]) :
    for y in range(grid[1]) :

      try:
        brightness = image[y][x]
      except IndexError:
        print('Index of image out of bounds.')
      except:
        print('Problem arose in loop when scanning through the image.')

      if (number := ceil(brightness / 40)) == 0 :
        continue

      die_x = die_L * (x + .5)
      die_y = die_L * (y + .5)

      for c in centres[number] :

        dot_x = int(die_x + .25 * c[0] * die_L)
        dot_y = int(die_y + .25 * c[1] * die_L)

        pygame.draw.circle(game, foreground, (dot_x,dot_y), dot_r)


if __name__ == '__main__' :
  pygame.init()

  try:
    image = cv2.imread('input.png',0)
  except:
    sys.exit('Image not found.')

  h, w = image.shape
  # What is the change in resolution?
  h *= 2; w *= 2

  die_L = 15
  dot_r = die_L // 10

  grid = list()
  grid.append(w // die_L)
  grid.append(h // die_L)

  display = (grid[0] * die_L, grid[1] * die_L)
  game = pygame.display.set_mode(display)

  image = cv2.resize(image,grid)

  draw(image, game, grid, h, w, die_L)

  pygame.display.update()
  pygame.image.save(game,"output.png")
  pygame.quit()