from geopy.geocoders import Nominatim


def get_location_name(latitude, longitude):
    geolocator = Nominatim(user_agent="your_app_name")
    location = geolocator.reverse((latitude, longitude), language="en")

    if location:
        return location.address
    else:
        return "None"
