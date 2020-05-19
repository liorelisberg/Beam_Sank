from graphics import *
import random

fix_ratio1 = 5  # for calc_shkia1
fix_ratio2 = 40  # for calc_shkia2
fix_ratio3 = 10  # for calc_shkia3


def open_default_win():
    windowDraw = GraphWin("Default exit window", 1000, 500)
    text = Text(Point(400, 250), "\tERROR\ndata not valid for making suitable graph")
    text.draw(windowDraw)
    text.setSize(30)
    windowDraw.getMouse()
    windowDraw.close()


def calc_E(material):
    if material == "aluminum":
        return 70 * pow(10, 9)
    elif material == "steel":
        return 200 * pow(10, 9)
    else:
        return 150 * pow(10, 9)


def calc_I(shape):
    if shape == "o":
        return 120 * pow(10, -8)
    elif shape == "t":
        return 95 * pow(10, -8)
    elif shape == "i":
        return 90 * pow(10, -8)
    elif shape == "u":
        return 100 * pow(10, -8)


def fix_points_ratio(p_list):
    for point in p_list:
        point.x = point.x + 150
        point.y = point.y + 200

    return p_list


def calc_shkia1(length, material, force, shape, div):
    shkia_points = []
    I, E = calc_I(shape), calc_E(material)
    for point in range(div + 1):
        x = (point * length) / div
        z = (x / length) - 2 * (pow(x, 3) / pow(length, 3)) + (pow(x, 4) / pow(length, 4))
        shkia = ((force * pow(length, 4)) / (24 * E * I)) * z
        shkia_points.append(Point(x * 100, shkia * fix_ratio1))
    return shkia_points


def calc_shkia2(length, material, force, shape, div):
    shkia_points = []
    I, E = calc_I(shape), calc_E(material)
    for point in range(div + 1):
        x = (point * length) / div
        z = (force * length * x) / (6 * E * I)
        shkia = z * (1 - (pow(x, 2) / pow(length, 2)))
        if shkia:
            shkia = shkia * -1
        shkia_points.append(Point(x * 100, shkia * fix_ratio2))
    return shkia_points


def calc_shkia3(length, material, force, shape, div):
    shkia_points = []
    I, E = calc_I(shape), calc_E(material)
    for point in range(div + 1):
        x = (point * length) / div
        shkia = (force * pow(x, 2)) / (2 * E * I)
        shkia_points.append(Point(x * 100, shkia * fix_ratio3))
    return shkia_points


def draw_org_beam(beam_len, attachment):
    window = GraphWin("Draw Shkia ", 1500, 500)
    text = Text(Point(100, 50), "SHKIA : ")
    text.setSize(15)
    text.draw(window)
    kora = Line(Point(150, 200), Point(150 + beam_len, 200))
    kora.setWidth(2)
    kora.setFill("blue")
    kora.draw(window)
    if attachment == "Hinge":
        triangle1 = Polygon(Point(150, 200), Point(120, 250), Point(180, 250))
        triangle1.setFill("green")
        triangle1.draw(window)
        triangle2 = Polygon(Point(150 + beam_len, 200), Point(120 + beam_len, 250), Point(beam_len + 180, 250))
        triangle2.setFill("green")
        triangle2.draw(window)
    elif attachment == "Fixed":
        fixed = Line(Point(150, 300), Point(150, 100))
        fixed.setWidth(4)
        fixed.setFill("green")
        fixed.draw(window)
    else:
        window.getMouse()
        window.close()
        open_default_win()
    return window


def draw_shkia1(beam_len, point_list):  # draw 2  hinges first
    window = draw_org_beam(beam_len, "Hinge")
    point_list = fix_points_ratio(point_list)
    for p1 in range(len(point_list) - 1):
        p2 = p1 + 1
        shkia = Line(point_list[p1], point_list[p2])
        shkia.setWidth(2)
        shkia.setFill("purple")
        shkia.draw(window)

    window.getMouse()
    window.close()


def draw_shkia2(beam_len, point_list):  # draw 2 hinges first
    window = draw_org_beam(beam_len, "Hinge")
    point_list = fix_points_ratio(point_list)
    for p1 in range(len(point_list) - 1):
        p2 = p1 + 1
        shkia = Line(point_list[p1], point_list[p2])
        shkia.setWidth(2)
        shkia.setFill("purple")
        shkia.draw(window)

    window.getMouse()
    window.close()


def draw_shkia3(beam_len, point_list):  # draw fixed first
    window = draw_org_beam(beam_len, "Fixed")
    point_list = fix_points_ratio(point_list)
    for p1 in range(len(point_list) - 1):
        p2 = p1 + 1
        shkia = Line(point_list[p1], point_list[p2])
        shkia.setWidth(2)
        shkia.setFill("purple")
        shkia.draw(window)

    window.getMouse()
    window.close()


def main():
    div = 10
    beams = ("Beam.txt", "Beam1.txt", "Beam2.txt", "Beam3.txt")
    with open(beams[random.randint(0,len(beams)-1)], "r") as beam:
        beam_len = float(beam.readline().replace("\n", ""))
        material = beam.readline().replace("\n", "").lower()
        attachment = beam.readline().replace("\n", "").lower()
        force_location = beam.readline().replace("\n", "").lower()
        force_kind = beam.readline().replace("\n", "").lower()
        force_amount = float(beam.readline().replace("\n", ""))
        shape = beam.readline().replace("\n", "").lower()
        depth = float(beam.readline().replace("\n", ""))
        height = float(beam.readline().replace("\n", ""))
        width = float(beam.readline().replace("\n", ""))

    if attachment == "hinge" and force_location == "center" and force_kind != "moment":
        point_list = calc_shkia1(beam_len, material, force_amount, shape, div)
        draw_shkia1(beam_len * 100, point_list)

    elif attachment == "hinge" and force_location == "end" and force_kind == "moment":
        point_list = calc_shkia2(beam_len, material, force_amount, shape, div)
        draw_shkia2(beam_len * 100, point_list)

    elif attachment == "fixed" and force_location == "end" and force_kind == "moment":
        point_list = calc_shkia3(beam_len, material, force_amount, shape, div)
        draw_shkia3(beam_len * 100, point_list)

    else:
        open_default_win()
        exit(-1)


if __name__ == "__main__":
    main()
