from datetime import datetime, timedelta  # , timezone
from pytz import UTC  # timezone
from icalendar import Calendar, Event
import core.peripherals as peripherals
import core.graphics as graphics
import config
import random
import time
import os
import sys
import pi3d
from random import randint
import numpy as np
import math

sys.path.insert(1, os.path.join(sys.path[0], '..'))


try:
    import arrow
except ImportError:
    exit("Please run: (sudo) pip3 install arrow")


text6 = None

actualy = 0
displayheight = 480
lasticalrefresh = 0


def init():
    global text6, actualy, displayheight

    if config.icallink.startswith('http'):
        icalfile = requests.get(config.icallink).text
    else:
        icalfile = open(config.installpath + config.icallink, 'r')

    gcal = Calendar.from_ical(icalfile.read())
    components = gcal.walk()
    now2 = datetime.now()
    components = filter(lambda c: c.name == 'VEVENT', components)
    components = filter(lambda c: c.get('dtstart').dt.replace(
        tzinfo=None) - now2 > timedelta(0), components)  # filter out past events
    components = sorted(components, key=lambda c: c.get('dtstart').dt.replace(
        tzinfo=None) - now2, reverse=False)  # order dates soonist to now to farthest

    text6 = pi3d.PointText(
        graphics.pointFont, graphics.CAMERA, max_chars=1000, point_size=128)
    count = 0
    mystring = ''
    actualy = -100

    for e in components:

        if count < 5:
            start = arrow.get(e.get('dtstart').dt)
            size = 0.79
            titles = pi3d.TextBlock(-390, ((displayheight/2) + actualy - (graphics.pointFont.height*size*0.5)), 0.1,
                                    0.0, 30, text_format=start.humanize().title(), size=size, spacing="F", space=0.02, colour=(1, 0, 0, 1))
            text6.add_text_block(titles)

            actualy -= titles.size * graphics.pointFont.height

            size = 0.29
            date = pi3d.TextBlock(-380, ((displayheight/2) + actualy - (graphics.pointFont.height*size*0.5)), 0.1, 0.0, 12,
                                  text_format='(' + start.format('DD.MM.YYYY') + ')', size=size, spacing="F", space=0.02, colour=(1, 1, 1, 1))
            text6.add_text_block(date)

            actualy -= date.size * graphics.pointFont.height
            size = 0.4

            width = 0
            subtext = ''
            actualword = ''
            g_scale = float(text6.point_size) / graphics.pointFont.height

            for c in e.get('summary'):
                width += graphics.pointFont.glyph_table[c][0] * g_scale * size

                actualword += c
                if c in (' ', '-', ',', '.', '+', ':'):
                    subtext += actualword
                    actualword = ''

                if width > 730:
                    event = pi3d.TextBlock(-350, (displayheight/2) + actualy - (graphics.pointFont.height*size*0.5),
                                           0.1, 0.0, 40, text_format=subtext, size=size, spacing="F", space=0.02, colour=(1, 1, 1, 1))
                    text6.add_text_block(event)
                    subtext = ''
                    width = 0
                    actualy -= event.size * graphics.pointFont.height

            if (subtext != '') or (actualword != ''):
                event = pi3d.TextBlock(-350, (displayheight/2) + actualy - (graphics.pointFont.height*size*0.5), 0.1,
                                       0.0, 40, text_format=subtext + actualword, size=size, spacing="F", space=0.02, colour=(1, 1, 1, 1))
                text6.add_text_block(event)
                actualy -= event.size * graphics.pointFont.height

            actualy -= 20
            count += 1

        else:
            break

    icalfile.close()


background2 = pi3d.Sprite(camera=graphics.CAMERA, w=780, h=460, z=2, x=0, y=0)
background2.set_shader(graphics.MATSH)
background2.set_material((0.0, 0.0, 0.0))
background2.set_alpha(0.6)
upperboarder = pi3d.Sprite(camera=graphics.CAMERA,
                           w=780, h=20, z=0.1, x=0, y=240)
upperboarder.set_shader(graphics.MATSH)
upperboarder.set_material((0.0, 0.0, 0.0))
upperboarder.set_alpha(0.0)
lowerboarder = pi3d.Sprite(camera=graphics.CAMERA,
                           w=780, h=20, z=0.1, x=0, y=-240)
lowerboarder.set_shader(graphics.MATSH)
lowerboarder.set_material((0.0, 0.0, 0.0))
lowerboarder.set_alpha(0.0)


scrolloffset = 0
updown = 0


def inloop(textchange=False, activity=False, offset=0):

    global actualy, scrolloffset, updown, displayheight, lasticalrefresh

    if lasticalrefresh < time.time():
        init()
        lasticalrefresh = time.time() + config.ICAL_TM

    if offset != 0:
        offset = graphics.slider_change(text6.text, offset)
    if offset == 0:

        background2.draw()
        lowerboarder.draw()
        upperboarder.draw()

        if actualy < -displayheight:
            if scrolloffset < actualy + displayheight:
                updown = 1
            if scrolloffset > 0:
                updown = 0
            if updown:
                scrolloffset += 15
            else:
                scrolloffset -= 1
            text6.text.positionY(-scrolloffset)

    activity = True  # for smooth movement
    text6.draw()
    return activity, offset
