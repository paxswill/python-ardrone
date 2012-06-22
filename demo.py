#!/usr/bin/env python

# Copyright (c) 2011 Bastian Venthur
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""Demo app for the AR.Drone.

This simple application allows to control the drone and see the drone's video
stream.
"""


import pyglet
from pyglet.window import key

import libardrone

def main():
    W, H = 320, 240
    window = pyglet.window.Window(width=W, height=H)
    drone = libardrone.ARDrone()
    label = pyglet.text.Label(font_name=["Helvetica", "Arial"], font_size=20,
                              x=10, y=10, text="0", color=(0, 0, 0, 255, 220))
    fps_display = pyglet.clock.ClockDisplay()


    def move(symbol, modifiers):
        if symbol == key.UP:
            drone.move_up()
        elif symbol == key.DOWN:
            drone.move_down()
        elif symbol == key.LEFT:
            drone.turn_left()
        elif symbol == key.RIGHT:
            drone.turn_right()
        elif symbol == key.W:
            drone.move_forward()
        elif symbol == key.S:
            drone.move_backward()
        elif symbol == key.A:
            drone.move_left()
        elif symbol == key.D:
            drone.move_right()
        elif symbol == key.RETURN:
            drone.takeoff()
        elif symbol == key.SPACE:
            drone.land()
        elif symbol == key.BACKSPACE:
            drone.reset()
        else:
            return pyglet.event.EVENT_UNHANDLED
        return pyglet.event.EVENT_HANDLED
    window.push_handlers(on_key_press=move)

    def change_speed(symbol, modifiers):
        speeds = {
                key._1 : 0.1,
                key._2 : 0.2,
                key._3 : 0.3,
                key._4 : 0.4,
                key._5 : 0.5,
                key._6 : 0.6,
                key._7 : 0.7,
                key._8 : 0.8,
                key._9 : 0.9,
                key:_0 : 1.0
                }
        try:
            drone.speed = speeds[symbol]
        except KeyError:
            return pyglet.event.EVENT_UNHANDLED
        return pyglet.event.EVENT_HANDLED
    window.push_handlers(on_key_press=change_speed)

    def hover(symbol, modifiers):
        drone.hover()
    window.push_handlers(on_key_release=hover)

    @window.event
    def on_draw():
        # Draw the image
        window.clear()
        image_data = drone.image
        image = pyglet.image.ImageData(width=image_data['width'],
                                       height=image_data['height'],
                                       format='RGB',
                                       data=image['data'])
        image.blit(0.0, 0.0)
        # Draw a simple HUD
        in_emergency = drone.navdata.get('drone_state', dict()).get('emergency_mask', 1)
        hud_color = (255, 0, 0, 220) if in_emergency else (10, 10, 255, 204)
        battery_level = drone.navdata.get(0, dict()).get('battery', 0)
        label.color = hud_color
        label.text = "Battery {}%".format(battery_level)
        label.draw()
        # Draw FPS
        fps_display.draw()

    @window.event
    def close():
        drone.reset()
        drone.halt()

    print "Shutting down...",
    drone.halt()
    print "Ok."

if __name__ == '__main__':
    main()

