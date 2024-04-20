from triangle import Triangle
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from triangle_with_name import TriangleWithName


def input_parameters():
    a = float(input("Enter side a: "))
    b = float(input("Enter side b: "))
    C = float(input("Enter angle C in degrees: "))
    color = input("Enter color: ")
    return a, b, C, color


def validate_parameters(a, b, C):
    if a <= 0 or b <= 0 or C <= 0 or C >= 180:
        print("Invalid parameters. All sides and the angle must be positive. The angle must be less than 180.")
        return False
    return True


def create_figure(a, b, C, color):
    return Triangle(a, b, C, color)


def print_figure(triangle):
    print(triangle)


def save_figure_to_file(triangle):
    with open("figure.txt", "w") as file:
        file.write(str(triangle))


def input_text():
    return input("Enter text: ")


def draw_triangle(a, b, C, color, text):
    # Convert C to radians
    C = np.radians(C)

    # Calculate the third side using the Law of Cosines
    c = np.sqrt(a**2 + b**2 - 2*a*b*np.cos(C))

    # Create the vertices of the triangle
    vertices = np.array([[0, 0], [b, 0], [a*np.cos(C), a*np.sin(C)]])

    # Check if the color is valid
    if color not in mcolors.CSS4_COLORS:
        color = 'red'  # Default color

    # Create a Polygon object based on the vertices
    triangle = plt.Polygon(vertices, fill=True, edgecolor=color, facecolor=color)

    # Add the triangle to the plot
    plt.gca().add_patch(triangle)

    # Add the text to the plot
    plt.figtext(0.5, 0.01, text, ha="center", fontsize=12)

    # Set the limits of the plot
    plt.xlim(-1, max(a, b) + 1)
    plt.ylim(-1, max(a, b) + 1)

    # Save the figure before showing it
    plt.savefig("figure.png")

    # Show the plot
    plt.show()


def save_figure_to_file(triangle, text):
    with open("figure.txt", "w") as file:
        file.write(str(triangle))
    plt.savefig("figure.png")


if __name__ == "__main__":
    a, b, C, color = input_parameters()
    text = input_text()
    if validate_parameters(a, b, C):
        triangle = create_figure(a, b, C, color)
        print_figure(triangle)
       #  save_figure_to_file(triangle, text)
        draw_triangle(a, b, C, color, text)
        triangle = TriangleWithName(3, 4, 5, "red", "My Triangle")
        triangle.print_details()
