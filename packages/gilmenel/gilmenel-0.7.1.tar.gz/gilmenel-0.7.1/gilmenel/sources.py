import re

from typing import Optional


from astropy import units as u
from astropy.coordinates import SkyCoord


class Star(object):
    def __init__(
        self,
        source_id: str,
        ra: u.deg,
        dec: u.deg,
        radius: u.arcmin,
        g_mag: float,
        rp_mag: Optional[float] = None,
        merit: Optional[int] = None,
    ):
        # unique identifier for a source, generally a GUID, comprising of a
        # first-part string and second part number
        self.source_id = str(source_id)

        self.sky_coord = SkyCoord(ra, dec, frame='icrs')
        self.ra = self.sky_coord.ra
        self.dec = self.sky_coord.dec

        self.radius = radius  # arcmin
        self.g_mag = g_mag
        self.rp_mag = rp_mag

        # the source coordinates in the instrument's reference frame
        self.instr_coord = None

        # at first, all sources have a merit of -1
        # as they pass each filter, the merit value increases
        # this will allow for operations in marginal conditions
        if merit is None:
            self.merit = -1
        else:
            self.merit = merit

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Star):
            return (
                self.source_id == other.source_id
                and u.isclose(self.ra, other.ra, rtol=1e-6)
                and u.isclose(self.dec, other.dec, rtol=1e-6)
                and u.isclose(self.radius, other.radius, rtol=1e-2)
                and self.g_mag == other.g_mag
                and self.rp_mag == other.rp_mag
                and u.isclose(self.merit, other.merit, rtol=1e-6)
            )
        return False  # pragma: no cover

    def __hash__(self):
        return hash((self.ra, self.dec, self.g_mag, self.rp_mag))  # pragma: no cover

    def __str__(self):
        return (
            f"source_id='{self.source_id}', "
            f"ra={self.ra:.6f}, "
            f"dec={self.dec:.6f}, "
            f"radius={self.radius:.3f}, "
            f"g_mag={self.g_mag:.2f}, "
            f"{f'rp_mag={self.rp_mag:.2f}, ' if self.rp_mag else ''}"
            f"merit={self.merit:.6f}"
        )  # pragma: no cover

    def __repr__(self):
        return re.sub(
            r'0+ ',
            '0 ',
            f"\nStar("
            f"'{self.source_id}',"
            f" {self.ra.to_value(u.deg):.6f} * d,"
            f" {self.dec.to_value(u.deg):.6f} * d,"
            f" {self.radius.to_value(u.arcmin):.3f} * m,"
            f" {self.g_mag},"
            f"{f' rp_mag={self.rp_mag:.2f},' if self.rp_mag else ''}"
            f" merit={self.merit:.6f})",
        )  # pragma: no cover
