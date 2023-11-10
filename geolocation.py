import geocoder
import time


def get_location():
    while True:
        location = geocoder.ip("me")

        if location.latlng:
            latitude, longitude = location.latlng

            # Determine the cardinal direction
            if latitude > 0:
                latitude_direction = "North"
            elif latitude < 0:
                latitude_direction = "South"
            else:
                latitude_direction = ""

            if longitude > 0:
                longitude_direction = "East"
            elif longitude < 0:
                longitude_direction = "West"
            else:
                longitude_direction = ""
            print("Your current location details:")
            print("Latitude:", latitude, latitude_direction)
            print("Longitude:", longitude, longitude_direction)
            print("City:", location.city)

            # Wait for 5 minutes before checking again
            time.sleep(90)
        else:
            print("Unable to retrieve location information.")
            # If unsuccessful, wait for 1 minute before trying again
            time.sleep(60)


if __name__ == "__main__":
    get_location()
