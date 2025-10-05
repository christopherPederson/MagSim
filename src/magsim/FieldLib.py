try:
    import geomag
    from datetime import datetime

    def get_B_field(lat, lon, h_km):
        # Get current date in YYYY-MM-DD format
        real_time = datetime.now()
        real_time_str = real_time.strftime('%Y-%m-%d')

        m = geomag.GeoMag()
        b = m.GeoMag(lat, lon, h_km, time=real_time_str)

        return (b.bx, b.by, b.bz)
    # not all of these functions require precision so im using this as an easy way to get feild strength
    def get_B_field():
        return 45e-6
except Exception:
    # Fallback constant ~45 µT if geomag unavailable
    EARTH_FIELD_STRENGTH = 45e-6  # Tesla
    def get_B_field(lat, lon, h_km):
        # simple fallback: total field only
        return (EARTH_FIELD_STRENGTH, 0.0, 0.0)