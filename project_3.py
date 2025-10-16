
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


# call this function to get an array of hex colors to test against
def select_test_colors(color):

    return []  # TODO: write logic for returning an array of hex colors to display against the passed color value


class colorTest:

    def __init__(self, color, ):
        self.color = color
        self.color_options = select_test_colors(color)  # possible colors to choose from
        self.chosen_color = None  # color that was chosen by user
        self.time = None  # time taken to pick this color


    def __str__(self):
        return f"{self.color},{self.color_options},{self.chosen_color},{self.time}"  # csv separated string for logging


