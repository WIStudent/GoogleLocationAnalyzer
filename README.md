# GoogleLocationAnalyzer

I wrote this small Python script because I wanted to know how much time I spend inside university buildings last semester. It uses the Google's Location History that was created by my Android phone. It visualizes the used measurement points on a map.

## Dependencies
- [matplotlib](http://matplotlib.org/)
- [basemap](https://github.com/matplotlib/basemap)

## Usage
1. Download your location history from the [Google Takeout](https://takeout.google.com/settings/takeout) page as a json file.
2. Go to Google Maps and make a screenshot of the area you are interested in. You need the latitude/longitude coordinates of the lower left and upper right corner of the image (Use right click and "What's here?" on Google Maps). 
3. Set the parameters in the script as you wish.

## Example Result
![Example Result](https://raw.githubusercontent.com/WIStudent/GoogleLocationAnalyzer/master/map_result.png "Example Result")