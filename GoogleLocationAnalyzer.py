import json
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Path to the json file
file_path = "Standortverlauf.json"
# Path to the map image
map_path = "Map.png"

# Coordinate boundaries of measurements that should be used for the time calculation
# Integers here because the json file uses integers for coordinates
lat_min = 519636100
lat_max = 519683500

lon_min = 75948700
lon_max = 76056100

# Only measurements between these two timestamps should be used for the time calculation
# 2015_10_01 00:00:00:000
time_start = 1443650400000
# 2016_04_01 00:00:00:000
time_end = 1459461600000

# Map corners
# Necessary to plot the used measurements to the map image
# lower left corner
lat_llc = 51.96361
lon_llc = 7.59487
# upper right corner
lat_urc = 51.96835
lon_urc = 7.60561

# Hold the used coordinates
x = []  # longitudes
y = []  # latitudes

# Holds the time in milliseconds
sum_time = 0

with open(file_path) as data_file:
    json_data = json.load(data_file)
    location_data = json_data["locations"]
    location_data_len = len(location_data)
    if location_data_len >= 2:
        i = 0
        # skip all entries that are at or after time_end

        while (i < location_data_len) and (int(location_data[i]["timestampMs"]) >= time_end):
            i += 1

        # skip the first entry that is before time_end
        if i < location_data_len:
            i += 1

        # look at all entries between time_start and time_end
        while (i < location_data_len) and (int(location_data[i]["timestampMs"]) >= time_start):
            lat1 = location_data[i - 1]["latitudeE7"]
            lat2 = location_data[i]["latitudeE7"]
            lon1 = location_data[i - 1]["longitudeE7"]
            lon2 = location_data[i]["longitudeE7"]

            # if both entries are in the specified area, increase sum_time by the time difference between the entries.
            if lat_min <= lat1 <= lat_max and lon_min <= lon1 <= lon_max \
                    and lat_min <= lat2 <= lat_max and lon_min <= lon2 <= lon_max:
                sum_time += (int(location_data[i - 1]["timestampMs"]) - int(location_data[i]["timestampMs"]))

                # save the used measurement points
                # only add lon1 and lat1 coordinates to the list of used measurements if they were not added already.
                if (len(x) == 0 and len(y) == 0) or not (x[-1] == (lon1 / 10000000) and y[-1] == (lat1 / 10000000)):
                    x.append(lon1 / 10000000)
                    y.append(lat1 / 10000000)

                x.append(lon2 / 10000000)
                y.append(lat2 / 10000000)

            i += 1

    sum_time_hours = sum_time / (1000 * 60 * 60)

    print("Hours: " + str(sum_time_hours))
    print("Days: " + str(sum_time_hours / 24))

    # Plot the used measurements onto a map
    m = Basemap(llcrnrlon=lon_llc, llcrnrlat=lat_llc, urcrnrlon=lon_urc,
                urcrnrlat=lat_urc, lat_ts=20, resolution='h', projection='merc')

    x1, y1 = m(x, y)
    m.drawmapboundary(fill_color='white')  # fill to edge
    m.scatter(x1, y1, s=5, c='r', marker="o", alpha=1.0)
    img = mpimg.imread(map_path)
    plt.imshow(img, zorder=0, extent=[m.xmin, m.xmax, m.ymin, m.ymax])
    plt.title("Measure Points")
    plt.show()
