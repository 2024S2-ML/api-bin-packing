import random
from matplotlib import patches, pyplot as plt

def get_rects():

  rectangles = []
  shirts_sizes = {
      "P": {
        "body": {
          "height": 68,
          "width": 48
        },
        "sleeve": {
          "length": 63,
          "width": 16
        },
        "shoulders": 42
      },
      "M": {
        "body": {
          "height": 70,
          "width": 51
        },
        "sleeve": {
          "length": 65,
          "width": 17
        },
        "shoulders": 44
      },
      "G": {
        "body": {
          "height": 72,
          "width": 54
        },
        "sleeve": {
          "length": 67,
          "width": 18
        },
        "shoulders": 46
      },
      "GG": {
        "body": {
          "height": 74,
          "width": 57
        },
        "sleeve": {
          "length": 69,
          "width": 19
        },
        "shoulders": 48
      }
  }

  def get_random_shirt_type():
    return random.choice(list(shirts_sizes.keys()))

  def add_shirt(rectangles, shirt_type, sizes):
    rectangles.append((sizes["body"]["height"], sizes["body"]["width"], shirt_type + str(random.randint(1, 1000))))
    rectangles.append((sizes["sleeve"]["length"], sizes["sleeve"]["width"], shirt_type + str(random.randint(1, 1000))))
    rectangles.append((sizes["sleeve"]["length"], sizes["sleeve"]["width"], shirt_type + str(random.randint(1, 1000))))

  for i in range(50):
    shirt_type = get_random_shirt_type()
    add_shirt(rectangles, shirt_type, shirts_sizes[shirt_type])

  return rectangles

def plot_bin_packing(rectangles, bin):
  bin_width, bin_height = bin
  fig, ax = plt.subplots(figsize=(bin_width / 10, bin_height / 10))

  for rect in rectangles:
      count, x, y, width, height, bin = rect
      ax.add_patch(patches.Rectangle((x, y), width, height, edgecolor='red', facecolor='blue'))

  ax.set_xlim(0, bin_width)
  ax.set_ylim(0, bin_height)
  ax.set_aspect('equal', 'box')
  plt.xlabel('Width')
  plt.ylabel('Height')
  plt.title('Bin Packing')
  plt.grid(False)

  return plt
