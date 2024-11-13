import tkinter as tk

#*******************************************************************
#                       Graphics Interpreter                       *
#                                                                  *
# PROGRAMMER: Josh Byers                                           *
# COURSE: CS340                                                    *
# DATE: 11/4/24                                                    *
# REQUIREMENT: Assignment 6                                        *
#                                                                  *
# DESCRIPTION:                                                     *
# The following program uses tkinter to create an interpreter      *
# that draws pictures. The user types in commands for shapes       *
# and the interpreter executes the drawing commands.               *
#                                                                  *
# COPYRIGHT: This code is copyright (C) 2024 Josh Byers            *
# and Dean Zeller.                                                 *
#                                                                  *
# CREDITS: This code was written with the help of ChatGPT and      *
# the tkinter website.                                             *
#                                                                  *
#******************************************************************

class GraphicsInterpreter:
    def __init__(self, root):
        self.root = root
        self.root.title("Graphics Interpreter")

        # Canvas to draw shapes
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        # Input field and button to submit commands
        self.entry = tk.Entry(root, width=50)
        self.entry.pack()
        self.entry.bind("<Return>", self.process_command)

        self.button = tk.Button(root, text="Draw", command=self.process_command)
        self.button.pack()

        # Label to display coordinates
        self.coord_label = tk.Label(root, text="Coordinates: (0, 0)")
        self.coord_label.pack()

        # History display
        self.history_label = tk.Label(root, text="Command History:")
        self.history_label.pack()
        
        self.history_text = tk.Text(root, height=10, width=50, wrap="word", state=tk.DISABLED)
        self.history_text.pack()

        # Tag for red color
        self.history_text.tag_configure("red", foreground="red")

        # Bind mouse motion to display coordinates
        self.canvas.bind("<Motion>", self.show_coordinates)

    #**********************************************************
    # METHOD: process_command()                               *
    # DESCRIPTION: takes in the user input and checks if it   *
    # is a valid command. Then it executes a drawing command  *
    # PARAMETERS: self: an instance of a class, event         *
    # RETURN VALUE: none                                      *
    #*********************************************************/
    def process_command(self, event=None):
        command = self.entry.get()
        self.entry.delete(0, tk.END)

        # Parse the command and execute it
        tokens = command.split()
        is_valid = False

        # Default to black if no valid color is given
        color = tokens[-1] if tokens[-1].isalpha() else "black"

        try:
            # Trapezoid
            if len(tokens) == 10 and (tokens[0].lower() == "trapezoid" or tokens[0].lower() == "ftrapezoid"):
                x1, y1, x2, y2, x3, y3, x4, y4 = map(int, tokens[1:9])
                self.draw_trapezoid(x1, y1, x2, y2, x3, y3, x4, y4, color, fill=(tokens[0].lower() == "ftrapezoid"))
                is_valid = True

            # Line
            elif len(tokens) == 6 and tokens[0].lower() == "line":
                x1, y1, x2, y2 = map(int, tokens[1:5])
                self.draw_line(x1, y1, x2, y2, color)
                is_valid = True

            # Circle
            elif len(tokens) == 5 and (tokens[0].lower() == "circle" or tokens[0].lower() == "fcircle"):
                x, y, radius = map(int, tokens[1:4])
                self.draw_circle(x, y, radius, color, fill=(tokens[0].lower() == "fcircle"))
                is_valid = True

            # Rectangle
            elif len(tokens) == 6 and (tokens[0].lower() == "rectangle" or tokens[0].lower() == "frectangle"):
                x, y, width, height = map(int, tokens[1:5])
                self.draw_rectangle(x, y, width, height, color, fill=(tokens[0].lower() == "frectangle"))
                is_valid = True

            # Triangle
            elif len(tokens) == 8 and (tokens[0].lower() == "triangle" or tokens[0].lower() == "ftriangle"):
                x1, y1, x2, y2, x3, y3 = map(int, tokens[1:7])
                self.draw_triangle(x1, y1, x2, y2, x3, y3, color, fill=(tokens[0].lower() == "ftriangle"))
                is_valid = True

            # Square
            elif len(tokens) == 5 and (tokens[0].lower() == "square" or tokens[0].lower() == "fsquare"):
                x, y, side_length = map(int, tokens[1:4])
                self.draw_square(x, y, side_length, color, fill=(tokens[0].lower() == "fsquare"))
                is_valid = True

            # Background
            elif len(tokens) == 2 and tokens[0].lower() == "background":
                self.canvas.config(bg=tokens[1])
                is_valid = True

        except ValueError:
            pass

        # Add the command to the history (set to red if invalid)
        self.history_text.config(state=tk.NORMAL)  # Enable editing
        if is_valid:
            self.history_text.insert(tk.END, f"{command}\n")
        else:
            self.history_text.insert(tk.END, f"{command}\n", "red")
        self.history_text.see(tk.END)  # Scroll to the bottom
        self.history_text.config(state=tk.DISABLED)  # Disable editing

    def show_coordinates(self, event):
        x, y = event.x, event.y
        self.coord_label.config(text=f"Coordinates: ({x}, {y})")

    def draw_trapezoid(self, x1, y1, x2, y2, x3, y3, x4, y4, color, fill):
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4,
                                   outline=color, fill=color if fill else "", width=2)

    def draw_line(self, x1, y1, x2, y2, color):
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

    def draw_circle(self, x, y, radius, color, fill):
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                outline=color, fill=color if fill else "")

    def draw_rectangle(self, x, y, width, height, color, fill):
        self.canvas.create_rectangle(x, y, x + width, y + height,
                                     outline=color, fill=color if fill else "")

    def draw_triangle(self, x1, y1, x2, y2, x3, y3, color, fill):
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3,
                                   outline=color, fill=color if fill else "", width=2)

    def draw_square(self, x, y, side_length, color, fill):
        self.canvas.create_rectangle(x, y, x + side_length, y + side_length,
                                     outline=color, fill=color if fill else "")

root = tk.Tk()
app = GraphicsInterpreter(root)
root.mainloop()