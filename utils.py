import pandas as pd
import numpy as np
import utm


def latlon_to_utm(lat, lon):
    """
    Convert latitude and longitude to UTM coordinates.

    Returns:
        pd.Series with:
        - utm_easting
        - utm_northing
        - utm_zone_number
        - utm_zone_letter
    """
    if pd.isna(lat) or pd.isna(lon):
        return pd.Series({
            "utm_easting": np.nan,
            "utm_northing": np.nan,
            "utm_zone_number": pd.NA,
            "utm_zone_letter": pd.NA,
        })

    try:
        easting, northing, zone_number, zone_letter = utm.from_latlon(lat, lon)

        return pd.Series({
            "utm_easting": easting,
            "utm_northing": northing,
            "utm_zone_number": zone_number,
            "utm_zone_letter": zone_letter,
        })

    except Exception:
        return pd.Series({
            "utm_easting": np.nan,
            "utm_northing": np.nan,
            "utm_zone_number": pd.NA,
            "utm_zone_letter": pd.NA,
        })
