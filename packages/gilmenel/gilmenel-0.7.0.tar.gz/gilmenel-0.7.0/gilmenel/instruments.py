import abc

from typing import List

import numpy as np

from astropy import units as u
from astropy.coordinates import SkyCoord

from matplotlib.artist import Artist
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from matplotlib.transforms import Affine2D, CompositeGenericTransform


from gilmenel.sources import Star


EQUINOX = SkyCoord(0, 0, unit=u.deg)


class BaseInstrument(metaclass=abc.ABCMeta):
    def __init__(
        self,
        name: str,
        instr_fov: u.arcmin,
        inner_excl_distance: u.arcmin,
        nearby_limit: u.arcsec,
        bright_limit: float,
        faint_limit: float,
        instr_offset: SkyCoord = None,
    ):
        global EQUINOX

        self.name = name
        self.instr_fov = instr_fov  # arcminutes radius
        self.inner_excl_distance = inner_excl_distance  # arcminutes radius
        self.nearby_limit = nearby_limit  # arcseconds diameter
        self.bright_limit = bright_limit
        self.faint_limit = faint_limit
        self.inner_excl_shape = 'circle'
        self.instr_offset = instr_offset if instr_offset is not None else EQUINOX

        # these are set by instr.point_to()
        self.origin = None
        self.target = None
        self._position_angle = 0 * u.deg

        # for simple fiducial drawing
        self.one_arcmin = 1 / 60

    def __getattribute__(self, name):
        if name == 'target':
            return self.origin
        elif name == 'position_angle':
            return self._position_angle
        else:
            return object.__getattribute__(self, name)

    # args and kwargs allow easier overloading of this function
    def point_to(self, target, position_angle, *args, instr_offset=None, **kwargs):
        global EQUINOX

        self._position_angle = position_angle
        self.target = target

        # update instr_offset if a new one is provided
        if instr_offset is not None:
            self.instr_offset = instr_offset

        # Instrument frame PA=0
        #  _________
        # |    N    |
        # |         |
        # |    0    |
        # |      X  |
        # |_________|
        #
        # Instrument frame PA=+90
        #  _________       _________       _________
        # |         |     |    N    |     |         |
        # |         |     |         |     |         |
        # |    0   N| <-- |    0    | <-- |    0    |
        # |  X      |     |      X  |     |      X  |
        # |_________|     |_________|     |_________|
        #
        # N = North
        # X = target
        # 0 = instr origin

        # target = known
        # target = origin + instr_offset
        # origin = target - instr_offset

        if self.instr_offset != EQUINOX:
            # perform target offset
            offset_sep = EQUINOX.separation(self.instr_offset)
            offset_pa = EQUINOX.position_angle(self.instr_offset)

            self.origin = target.directional_offset_by(
                offset_pa + position_angle, offset_sep
            )
        else:
            # set origin to target
            # prevents cpu rounding errors from interferring with tests
            self.origin = target

        # set instrument frame from cenre of field
        # position angle is already included
        self.instr_frame = self.origin.skyoffset_frame(rotation=position_angle)

    def star_available(self, star: Star) -> bool:
        '''Check if star location falls within allowable geometry'''

        # set star coordinates relative to instrument frame
        star.instr_coord = star.sky_coord.copy()
        star.instr_coord = star.instr_coord.transform_to(self.instr_frame)

        # Check if star falls within FOV
        if star.radius > self.instr_fov:
            return False

        # Check if star falls within exclusion zone
        if self.inner_excl_shape == 'circle':
            if star.radius <= self.inner_excl_distance:
                return False
        elif self.inner_excl_shape == 'square':
            if (
                star.instr_coord.lon <= self.inner_excl_distance
                and star.instr_coord.lon >= -self.inner_excl_distance
                and star.instr_coord.lat <= self.inner_excl_distance
                and star.instr_coord.lat >= -self.inner_excl_distance
            ):
                return False
        else:
            raise NotImplementedError

        return True

    def filter_geometry(self, stars: List[Star]) -> List[Star]:
        for s in stars:
            if self.star_available(s):
                s.merit = 1
            else:
                s.merit = 0  # mark that star has been checked

        return stars

    def filter_nearby_pairs(self, stars: List[Star]) -> List[Star]:
        for s in stars:

            def s_is_close_to(t):
                return (
                    t.g_mag < s.g_mag + 2
                    and abs(t.ra - s.ra)  # t mag brighter than s mag -2
                    <= self.nearby_limit
                    and abs(t.dec - s.dec) <= self.nearby_limit
                )

            nearby_stars = any(  # any returns True at first test star found
                True for t in stars if s_is_close_to(t) and s is not t
            )  # t -> test star

            if nearby_stars is False:
                s.merit = 2

        return stars

    def filter_magnitudes(self, stars: List[Star]) -> List[Star]:
        for s in stars:
            # remove faint stars
            if s.g_mag > self.faint_limit:
                pass  # leave faint stars at their current merit value

            # remove bright stars
            elif s.g_mag < self.bright_limit:
                s.merit = 3

            # just right
            else:
                s.merit = 4

        return stars

    def criteria(self, stars: List[Star]) -> bool:
        '''
        Criteria for filtering stars. Alter the original list of stars in-place by
        setting 'star.merit' to a user-defined value for later optimisation.

        Return True for a new selection that includes fainter stars to prevent visual
        over-crowding in dense fields.

        This method should be duplicated and overriden by the user.
        '''
        self.filter_geometry(stars)
        self.filter_nearby_pairs([s for s in stars if s.merit == 1])
        self.filter_magnitudes([s for s in stars if s.merit == 2])

        max_suitable_stars = 10

        # check if enough stars have been found
        if len([s for s in stars if s.merit >= 4]) >= max_suitable_stars:
            return True

        return False

    def filter(self, stars: List[Star]) -> List[Star]:
        '''
        Filter stars in layers of magnitude, each call to criteria will be
        given an additional subset of fainter stars.

        Two magnitudes of additional stars are included to make sure that
        dim, yet visible, stars that are too close are rejected later.
        '''
        brightest = min(s.g_mag for s in stars)
        faintest = max(s.g_mag for s in stars)

        # make sure to include at least one magnitude if brightest == faintest
        test_magnitudes = np.arange(brightest, max(brightest + 1, faintest - 2))

        star_subset = []
        for mag in test_magnitudes:
            star_subset = [s for s in stars if s.g_mag <= mag + 2]

            if self.criteria(star_subset) is True:
                # if sufficient stars for later selection have been found
                # do not request any more
                break

        return star_subset

    @abc.abstractmethod
    def best_stars(self, stars: List[Star]) -> List[Star]:
        '''Return the best guide stars from the given selection'''

    def get_fiducials(self, ax_transData: CompositeGenericTransform) -> List[Artist]:
        '''Return a list of Artists (lines, circles, patches, etc) to draw
        on Matplotlib diagrams'''
        global EQUINOX

        # Data field of view
        instr_fov = Circle(
            (0, 0), self.instr_fov.to_value(u.deg), color='#444', fill=False
        )

        # Target Exclusion Zone
        exclusion_size = self.inner_excl_distance.to_value(u.deg)
        exclusion = Circle((0, 0), exclusion_size, color='#990000', fill=False)

        # Target
        target_colour = '#ff00ff'
        t_ra, t_dec = self.instr_offset.spherical_offsets_to(EQUINOX)
        target_pos = (t_ra.to_value(u.deg), t_dec.to_value(u.deg))

        target_points = [
            [(0, 1), (0, 2)],
            [(0, -1), (0, -2)],
            [(1, 0), (2, 0)],
            [(-1, 0), (-2, 0)],
        ]

        target_points = [
            [np.array(point) / 60 / 10 + np.array(target_pos) for point in line]
            for line in target_points
        ]

        target_lines = [
            Line2D(*np.transpose(line), color=target_colour, lw=0.5,)
            for line in target_points
        ]

        target = Circle(
            target_pos,
            0.1 * self.one_arcmin,
            color=target_colour,
            lw=0.5,
            fill=False,
            # transform=ax_transData,
        )

        return [instr_fov] + [exclusion] + target_lines + [target]


class GapInstrument(BaseInstrument):
    def __init__(
        self,
        name: str,
        instr_fov: u.arcmin,
        inner_excl_distance: u.arcmin,
        nearby_limit: u.arcsec,
        bright_limit: float,
        faint_limit: float,
        slit_gap_radius: u.arcmin,
        slit_gap_angle: u.deg,
        instr_offset: SkyCoord = None,
    ):
        super().__init__(
            name,
            instr_fov,
            inner_excl_distance,
            nearby_limit,
            bright_limit,
            faint_limit,
            instr_offset=instr_offset,
        )
        self.slit_gap_radius = slit_gap_radius  # arcmin
        self.slit_gap_angle = slit_gap_angle  # degrees, relative to PA = 0

    def point_to(self, target, position_angle, instr_offset=None):
        # set target
        super().point_to(target, position_angle, instr_offset=instr_offset)

        # set position angle if available
        if position_angle is not None:
            self.slit_gap_angle = position_angle

    def star_available(self, star: Star) -> bool:
        '''Check if star location falls within allowable geometry'''

        # first call parent method
        result = super().star_available(star)
        if result is False:
            return result

        # Check if star falls within a vertical gap of distance slit_gap_radius
        ra = (star.instr_coord.lon.to_value(u.deg) + 180) % 360 - 180

        if abs(ra) <= self.slit_gap_radius.to_value(u.deg):
            return False

        return True

    def best_stars(self, stars: List[Star]) -> List[Star]:
        '''Return the best guide stars from the given selection'''
        raise NotImplementedError

    def get_fiducials(self, ax_transData: CompositeGenericTransform) -> List[Artist]:
        '''Return a list of Artists (lines, circles, patches, etc) to draw
        on Matplotlib diagrams'''

        # Slit exclusion
        # add slit lines that rotate with PA
        points = [
            (0, -4.96 * self.one_arcmin),
            (0, 4.96 * self.one_arcmin),
        ]

        fiducials = [
            Line2D(
                *np.transpose(points),
                lw=1,
                color='#990000',
                transform=Affine2D().translate(
                    +self.slit_gap_radius.to_value(u.deg), 0,
                )
                + ax_transData,
            ),
            Line2D(
                *np.transpose(points),
                lw=1,
                color='#990000',
                transform=Affine2D().translate(
                    -self.slit_gap_radius.to_value(u.deg), 0,
                )
                + ax_transData,
            ),
        ]

        return super().get_fiducials(ax_transData) + fiducials
