'''
Copyright (C) 2018 Jean Da Costa Machado.

Created by Jean Da Costa Machado

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from mathutils import Vector, Matrix, Quaternion
from math import sin, cos, pi
import bpy

def circle_point(angle):
    return Vector((sin(angle * 2 * pi), cos(angle * 2 * pi), 0))


class StrokeCurve:
    def __init__(self, stroke):
        self.stroke = stroke
        self.points = []
        self._location = Vector()
        self._rotation = Matrix.Identity(4)
        self._scale = Vector((1, 1, 1))

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value
        self.update()

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        self.update()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()

    def update(self):
        for point, stroke_point in zip(self.points, self.stroke.points):
            stroke_point.co = Vector((point[0] * self.scale[0],
                                      point[1] * self.scale[1],
                                      point[2] * self.scale[2]))
            stroke_point.co.rotate(self._rotation)
            stroke_point.co += self.location

    def set_points(self, points):
        while not len(self.stroke.points) == len(points):
            if len(self.stroke.points) > len(points):
                self.stroke.points.pop()
            elif len(self.stroke.points) < len(points):
                self.stroke.points.add()
        self.points = points
        self.update()


class StrokeLayer:
    def __init__(self, context, name="Grease"):
        if context.scene.grease_pencil:
            gp = context.scene.grease_pencil

        else:
            gp = bpy.data.grease_pencil.new("Grease Pencil")
            context.scene.grease_pencil = gp

        if not gp.palettes:
            self.palette = gp.palettes.new(name)
        else:
            self.palette = gp.palettes.active

        self.palette_colors = self.palette.colors.new()
        self.palette.name = name

        self.layer = gp.layers.new(name)
        self.layer.line_change = 2
        self.frame = self.layer.frames.new(context.scene.frame_current)
        self.gp = gp

    def remove_layer(self):
        self.gp.layers.remove(self.layer)
        self.palette.colors.remove(self.palette_colors)

    def create_stroke(self):
        stroke = self.frame.strokes.new(self.palette.name)
        stroke.draw_mode = "3DSPACE"
        return StrokeCurve(stroke)

    def delete_stroke(self, stroke_curve):
        self.frame.strokes.remove(stroke_curve.stroke)
