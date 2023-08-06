# -*- coding: utf-8 -*-

from ....Classes.Arc1 import Arc1
from ....Classes.Arc3 import Arc3
from ....Classes.Segment import Segment


def build_geometry(self):
    """Compute the curve (Line) needed to plot the object.
    The ending point of a curve is the starting point of the next curve
    in the list

    Parameters
    ----------
    self : SlotUD
        A SlotUD object

    Returns
    -------
    curve_list: list
        A list of Segments

    """

    # Apply symmetry if needed
    point_list = self.point_list.copy()
    if self.is_sym:
        for point in self.point_list[::-1]:
            point_list.append(point.conjugate())

    # Creation of curve
    curve_list = list()
    for ii in range(len(point_list) - 1):
        curve_list.append(Segment(point_list[ii], point_list[ii + 1]))

    return curve_list
