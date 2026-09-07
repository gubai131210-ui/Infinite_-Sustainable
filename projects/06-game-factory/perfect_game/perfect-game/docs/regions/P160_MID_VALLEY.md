# REGION templates — P160 World-driven pass（2026-09-07）

## MID_VALLEY（镇↔农庄↔湖之间的空洞带）

```text
REGION: MID_VALLEY
PURPOSE: Connect farm/town/lake so overview reads as one place, not POI islands
PRIMARY LANDMARK: winding dirt spine farm→plaza→lake + secondary to station
TERRAIN: soft grass variants + dirt blobs along road shoulders (not square beds)
ROAD STRUCTURE: continuous 2-tile-wide winding paths; forks at plaza
VEGETATION DENSITY: medium clusters along road, sparse open meadow pockets, denser near forest rim
BUILDING DENSITY: none new — reinforce existing house yards with path links
PALETTE: warm grass + dirt path
TRANSITION AREAS: path→grass GD seams; avoid empty pure-green slabs
DECORATION: pebble/tuft only ON road shoulders after composition
EMPTY SPACE: keep 2–3 breathing pockets south of plaza, NOT half the map
PLAYER FLOW: farm → plaza → lake / station
```

## TOWN_PLAZA

```text
REGION: TOWN_PLAZA
PURPOSE: Dense readable hub with stone core + dirt fringe
PRIMARY LANDMARK: storefronts + stalls
TERRAIN: plaza oval + dirt approach rings
ROAD STRUCTURE: four-way dirt spokes already exist — thicken + soft edges
VEGETATION DENSITY: yard trees / planters only; no solid canopy over plaza
BUILDING DENSITY: keep; ensure path to each door apron
PALETTE: plaza grey + dirt
TRANSITION AREAS: plaza→dirt→grass
DECORATION: existing stalls; no new micro spam
EMPTY SPACE: small plaza breathing room only
PLAYER FLOW: crossroads
```

## LAKE_ECHO

```text
REGION: LAKE_ECHO
PURPOSE: Break perfect circle; organic shore + connected west fields
PRIMARY LANDMARK: lighthouse + pier
TERRAIN: irregular lake ellipse + sand/WE fringe
ROAD STRUCTURE: path from town to pier/lighthouse
VEGETATION DENSITY: shore reeds/rocks clusters; west fields stay farm
BUILDING DENSITY: cottage/pier only
PALETTE: water blue + sand
TRANSITION AREAS: WE/sand multi-ring
DECORATION: boats already; rocks at shore
EMPTY SPACE: open water is intentional
PLAYER FLOW: town path → pier / lighthouse
```
