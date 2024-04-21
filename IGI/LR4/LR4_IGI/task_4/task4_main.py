from task_4.triangle import Triangle
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from task_4.triangle_with_name import TriangleWithName


def input_parameters():
    """Get the parameters of the triangle from the user."""

    while True:
        try:
            a = float(input("Enter side a: "))
            b = float(input("Enter side b: "))
            C = float(input("Enter angle C in degrees: "))
            color = input("Enter color: ")

            if a <= 0 or b <= 0 or C <= 0:
                print("All sides and the angle must be positive. Please try again.")
                continue

            if color not in mcolors.CSS4_COLORS:
                print("The color does not exist. Please try again.")
                continue

            return a, b, C, color

        except ValueError:
            print("Invalid input. Please enter a valid number.")


def validate_parameters(a, b, C):
    """Check if the parameters of the triangle are valid."""

    if a <= 0 or b <= 0 or C <= 0 or C >= 180:
        print("Invalid parameters. All sides and the angle must be positive. The angle must be less than 180.")
        return False
    return True


def create_figure(a, b, C, color):
    """Create a triangle with the given parameters."""

    return Triangle(a, b, C, color)


def print_figure(triangle):
    print(triangle)


def save_figure_to_file(triangle):
    """Save the triangle to a file."""

    with open("figure.txt", "w") as file:
        file.write(str(triangle))


def input_text():
    return input("Enter text: ")


def draw_triangle(a, b, C, color, text):
    """Draw a triangle with the given parameters."""

    C = np.radians(C)
    # теорема косинусов
    # c = np.sqrt(a ** 2 + b ** 2 - 2 * a * b * np.cos(C))

    # массив вершин делаем
    vertices = np.array([[0, 0], [b, 0], [a * np.cos(C), a * np.sin(C)]])

    if color not in mcolors.CSS4_COLORS:
        color = 'red'  # по умолчанию

    # создаем объект многоугольник и задаем наши вершины
    triangle = plt.Polygon(vertices, fill=True, edgecolor=color, facecolor=color)

    # добавляем на график
    plt.gca().add_patch(triangle)
    plt.figtext(0.5, 0.01, text, ha="center", fontsize=12)

    # пределы по осям, чтобы все видно было
    plt.xlim(-1, max(a, b) + 1)
    plt.ylim(-1, max(a, b) + 1)

    plt.savefig("figure.png")
    plt.show()


def main():
    """Main function of the task."""

    a, b, C, color = input_parameters()
    text = input_text()
    if validate_parameters(a, b, C):
        triangle = create_figure(a, b, C, color)
        print_figure(triangle)
        # save_figure_to_file(triangle, text)
        draw_triangle(a, b, C, color, text)
        print("Show using of super()")
        triangle = TriangleWithName(3, 4, 5, "red", "My Triangle")
        triangle.print_details()
        triangle.print_details_json()



main()
