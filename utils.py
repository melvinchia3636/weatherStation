import cairosvg
import io
import pygame
import numpy as np
import requests


def load_svg(filename):
    new_bites = cairosvg.svg2png(url=filename)
    byte_io = io.BytesIO(new_bites)
    return pygame.image.load(byte_io)


def wrap_text(text, font, max_width):
    texts = text.replace("\t", "    ").split("\n")
    lines = []

    for text in texts:
        text = text.rstrip(" ")

        if not text:
            lines.append("")
            continue

        a = len(text) - len(text.lstrip(" "))

        a = text.index(" ", a) if " " in text else len(text)
        line = text[:a]

        while a + 1 < len(text):
            if " " not in text[a + 1:]:
                b = len(text)
                bline = text

            else:
                b = text.index(" ", a + 1)
                while text[b - 1] == " ":
                    if " " in text[b + 1:]:
                        b = text.index(" ", b + 1)
                    else:
                        b = len(text)
                        break
                bline = text[:b]

            bline = text[:b]

            if font.size(bline)[0] <= max_width:
                a, line = b, bline

            else:
                lines.append(line)
                text = text[a:].lstrip(" ")
                a = text.index(" ", 1) if " " in text[1:] else len(text)
                line = text[:a]

        if text:
            lines.append(line)
    return lines


def create_text(text, font, color, pos, max_width=None):
    if max_width is not None:
        lines = wrap_text(text, font, max_width)
    else:
        lines = text.replace("\t", "    ").split("\n")

    line_ys = (
        np.arange(len(lines))
    ) * 1.05 * font.get_linesize() + pos[1]

    text_objects = []

    for line, y_pos in zip(lines, line_ys):
        text_surface = font.render(line, True, color)
        text_objects.append((text_surface, (pos[0], y_pos)))

    return text_objects


def request(url):
    return requests.get(url).json()
