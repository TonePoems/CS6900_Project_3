import argparse
import random


# colors from the project
old_colors = {
  "red": 0xFF0000,
  "brown": 0x7F6000,
  "green": 0x9DE951,
  "orange": 0xFEBC02,
  "yellow": 0xFFFF00,
  "blue": 0x002F8E,
  "purple": 0x7030A0
}

# colors selected by Sean
new_colors = {
  "red": 0xED1E24,
  "brown": 0xD4681B,
  "green": 0x92D050,
  "orange": 0xFEBC02,
  "yellow": 0xFFFF00,
  "blue": 0x00B0F0,
  "purple": 0x7030A0
}


class colorTest:

    def __init__(self, color, hex, source):
        self.color = color  # keys in color dicts
        self.hex = hex  # values in color dicts
        self.source = source  # 'old' or 'new' to tell which dataset it comes from
        self.color_options = self.select_test_colors()  # possible colors to choose from
        self.chosen_color = None  # color that was chosen by user
        self.time = None  # time taken to pick this color


    # call this function to get an array of hex colors to test against
    def select_test_colors(self):
        color_list = []  # list of color options 

        # Add old and new versions of this color
        color_list.append(old_colors[self.color])
        color_list.append(new_colors[self.color])
        
        # Select randomly between old and new versions of the other colors
        for key in old_colors:
            if not key == self.color:
                if random.randint(0, 1) == 0:
                   color_list.append(old_colors[key])
                else:
                   color_list.append(new_colors[key])

        color_list = random.shuffle(color_list)  # shuffle to avoid testing bias
        return  color_list  


    def __str__(self):
        return f"{self.source},{self.color},{hex(self.hex)},{self.color_options},{self.chosen_color},{self.time}"  # csv separated string for logging



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--reps", nargs='?', default=20,
                        help="number of reps per color option. Default 20")
    args = parser.parse_args()


    test_colors = []
    test_per_color = int(args.reps)
    

    for key, value in old_colors.items():
        for i in range(test_per_color):
            test_colors.append(colorTest(key, value, 'old'))

    for key, value in new_colors.items():
        for i in range(test_per_color):
            test_colors.append(colorTest(key, value, 'new'))


    random.shuffle(test_colors)  # shuffle so we can avoid bias in testing order

    for test in test_colors:
        print(test)


