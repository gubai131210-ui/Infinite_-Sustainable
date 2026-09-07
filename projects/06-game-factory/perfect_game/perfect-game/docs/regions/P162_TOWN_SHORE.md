# REGION — P162 soft seams + town residential density

## SHORE_SOFT

```text
REGION: WATER_LAND
PURPOSE: Land fringe sand/grass only; WE only on water layer (no stitch re-harden)
```

## FARM_DIRT_SEAM

```text
REGION: FARM_BEDS
PURPOSE: GD stitch only on DIRT/FARM — PATH excluded to kill checkerboard spam
```

## TOWN_RESIDENTIAL

```text
REGION: TOWN_RING
PURPOSE: Denser house clusters + yard aprons toward ref overview
PRIMARY LANDMARK: shop/cafe/bakery remain heroes
BUILDING DENSITY: +6 houses west/east/south of plaza
TRANSITION AREAS: dirt footings under each house
EMPTY SPACE: plaza core stays walkable
```
