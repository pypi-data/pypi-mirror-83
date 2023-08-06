
from collections import Iterable

import cadquery as cq

from paramak import Shape


class RotateSplineShape(Shape):
    """Rotates a 3d CadQuery solid from points connected with splines.

    Args:
        rotation_angle (float, optional): The rotation_angle to use when
            revolving the solid (degrees). Defaults to 360.0.
        stp_filename (str, optional): Defaults to "RotateSplineShape.stp".
        stl_filename (str, optional): Defaults to "RotateSplineShape.stl".
    """

    def __init__(
        self,
        rotation_angle=360,
        stp_filename="RotateSplineShape.stp",
        stl_filename="RotateSplineShape.stl",
        **kwargs
    ):

        super().__init__(
            stp_filename=stp_filename,
            stl_filename=stl_filename,
            **kwargs
        )

        self.rotation_angle = rotation_angle

    @property
    def rotation_angle(self):
        return self._rotation_angle

    @rotation_angle.setter
    def rotation_angle(self, value):
        self._rotation_angle = value

    def create_solid(self):
        """Creates a rotated 3d solid using points with spline edges.

           Returns:
              A CadQuery solid: A 3D solid volume
        """

        # Creates a cadquery solid from points and revolves
        solid = (
            cq.Workplane(self.workplane)
            .spline(self.points)
            .close()
            .revolve(self.rotation_angle)
        )

        # Checks if the azimuth_placement_angle is a list of angles
        if isinstance(self.azimuth_placement_angle, Iterable):
            rotated_solids = []
            # Perform seperate rotations for each angle
            for angle in self.azimuth_placement_angle:
                rotated_solids.append(
                    solid.rotate(
                        (0, 0, -1), (0, 0, 1), angle))
            solid = cq.Workplane(self.workplane)

            # Joins the seperate solids together
            for i in rotated_solids:
                solid = solid.union(i)
        else:
            # Peform rotations for a single azimuth_placement_angle angle
            solid = solid.rotate(
                (0, 0, -1), (0, 0, 1), self.azimuth_placement_angle)

        self.perform_boolean_operations(solid)

        return solid
