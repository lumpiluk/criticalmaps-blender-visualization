# CriticalMaps Blender Visualization

Visualize [CriticalMaps](https://www.criticalmaps.net/) traces in Blender.

![Screenshot of Blender showing a map of Berlin, active bicycles, and the side panel for CriticalMaps visualization.](screenshots/screenshot_blender_overview.png)

## Installation

Requirements:
- Python 3.14 or [UV](https://docs.astral.sh/uv/)
- [Blender](https://blender.org) (5.1.2 or newer)
- The [BlenderGIS](https://github.com/domlysz/BlenderGIS) add-on


## Workflow

1. Run `./record_criticalmaps.py` during the bicycling event that you want to visualize.
   Alternatively, you may experiment with [the dataset](https://github.com/lumpiluk/criticalmaps-blender-visualization/releases/download/2026-06-09/criticalmaps-data_2026-06-07-adfc-berlin-sternfahrt.zip) from ADFC Berlin Sternfahrt on 2026-06-07.
1. Create a copy of `visualization.blend` and open it in Blender. Allow the included script to run.
1. Use BlenderGIS to download map tiles for the background. Be mindful of the map providers' licenses and attribution requirements.
1. In Blender's Properties Editor, select the Scene tab and find the CriticalMaps section. This will only be visible if you ran the script included in the .blend file.
1. Align your CriticalMaps traces with the map:
   Find a recognizable location on the map. Move your 3D cursor there and note its X and Y position as the anchor point. Set the latitude and longitude accordingly.
1. Set the CSV folder to the output folder of your recorded CriticalMaps traces from step 1. Adjust the keyframe animation of the Time field as you like.
   Now when you scrub through the timeline, you should be able to see points of the CriticalMaps scene object moving around.
