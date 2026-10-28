# LiDAR check: Avenue and ring (1 m bare-earth DTM)

Source: Environment Agency / DEFRA Lidar Composite DTM, 1 m, EPSG:27700 (WCS, fetched this session).
Tiles: 900 m × 900 m, centred near the monument and along the expected Avenue line (about 50°) out to about 2.5 km.

## Method
- Ring centre: circle fit to the bank/ditch relief, E 412245, N 142194 (diameter about 102 m; crest 96 m, ditch 106 m).
- Relief: DTM minus a Gaussian-smoothed copy (sigma 10 m), keeping features roughly under 20 m.
- Avenue test: for each bearing, a 50 m-wide cross-profile averaged along 150–2400 m, with each cross-section's mean removed. A real bank or ditch should give a sustained centre dip or ridge.
- Positive control: the A303 road (bearing about 96°) gives a clear 0.5 m profile with this method.

## Results
- Bearing sweep 35–65°: the strongest centre dip is at 51° (−0.067 m), confined to 500–1,300 m. It disappears beyond 1,300 m and is positive from 150–500 m. It does not persist along the line and is not the Avenue on this evidence.
- Control bearings 40°, 45°, 58° and 60° show no comparable sustained dip.
- No Avenue bank or ditch is detected along 40–60° at a relief above about 0.15 m.

## Limits
- A 1 m DTM with a 20 m filter can miss shallow or eroded earthworks below about 0.15 m.
- Bearing uncertainty of 1° moves a line about 35 m at 2 km. The ±25 m corridor could miss a slightly curved Avenue.
- The sarsen circle (about 30–33 m) is not resolvable at this resolution, so ring diameters here are for the bank and ditch only.

## Status
Not detected in this DTM. Not ruled out. Confirmation needs a survey (geophysics or a higher-resolution scan).
