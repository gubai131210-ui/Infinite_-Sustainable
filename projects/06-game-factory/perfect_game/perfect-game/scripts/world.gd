extends Node2D
## Wave0 world: TileMapLayer ground + zone base paint + collision for water/cliff.

const W := 192
const H := 128
const TS := 16

# Atlas tile ids (see gen_tileset_master.py)
const T_GRASS := 0
const T_DIRT := 1
const T_PATH := 2
const T_PLAZA := 3
const T_WATER := 4
const T_CLIFF := 5
const T_HILL := 6
const T_STAIRS := 7
const T_FARM := 8
const T_RAIL := 9
const T_SAND := 10
const T_BRIDGE := 11
const T_GRASS2 := 12
const T_DEEP := 13
const T_WE_E := 14
const T_WE_W := 15
const T_WE_N := 16
const T_WE_S := 17
const T_GRASS3 := 18
const T_GRASS4 := 19
const T_PATH2 := 20  # organic path variant (atlas extras)
const T_DIRT2 := 21
const T_GD_N := 22   # grass↔dirt north edge of dirt
const T_PLAZA2 := 23
const T_GD_S := 24
const T_GD_SE := 25  # outer corner (was sand dup)
const T_GD_SW := 26  # outer corner (was farmland dup)
const T_GD_E := 28
const T_GD_W := 29
const T_GD_NE := 30
const T_GD_NW := 31

# Zone rects from R5_WORLD_BLUEPRINT
const ZONES := {
	"Z1_FARM": Rect2i(8, 72, 65, 47),
	"Z2_RIVER": Rect2i(4, 16, 53, 73),
	"Z3_TOWN": Rect2i(64, 28, 57, 45),
	"Z4_STATION": Rect2i(120, 8, 65, 33),
	"Z5_TERRACE": Rect2i(120, 40, 49, 41),
	"Z6_LAKE": Rect2i(112, 80, 77, 45),
}

var _ground: TileMapLayer
var _water: TileMapLayer
var _colliders: Node2D

func _ready() -> void:
	_ground = $Ground
	_water = $Water
	_colliders = $Colliders
	_setup_tileset()
	_paint_base()
	_build_water_collisions()
	_cache_water_cells()
	_spawn_zone_labels()
	# wood placards in decor.gd remain as physical props; Labels are poster-scale overlays

var _water_t: float = 0.0
var _water_cells: Array[Vector2i] = []

func _process(delta: float) -> void:
	if _water == null:
		return
	_water_t += delta
	# Soft shimmer only — avoid checkerboard tile swap (reads as broken water)
	var pulse := 0.90 + 0.10 * sin(_water_t * 2.1)
	var cool := 0.95 + 0.05 * sin(_water_t * 1.3 + 1.0)
	_water.modulate = Color(pulse * cool, pulse, 1.05, 1.0)

func _cache_water_cells() -> void:
	_water_cells.clear()
	for cell in _water.get_used_cells():
		_water_cells.append(cell)
func _spawn_zone_labels() -> void:
	## Poster placards — hidden in normal play; golden overview toggles visible
	var markers := $ZoneMarkers
	markers.visible = false
	var labels := {
		"米勒农庄": Vector2(28, 90),
		"橡木河": Vector2(16, 46),
		"橡木火车站": Vector2(140, 6),
		"回声湖": Vector2(148, 100),
	}
	for label_text in labels.keys():
		var lab := Label.new()
		lab.text = str(label_text)
		lab.position = labels[label_text] * TS
		lab.z_index = 40
		lab.add_theme_font_size_override("font_size", 22)
		lab.add_theme_color_override("font_color", Color(1, 1, 1))
		lab.add_theme_color_override("font_outline_color", Color(0.04, 0.05, 0.08))
		lab.add_theme_constant_override("outline_size", 10)
		lab.scale = Vector2(2.8, 2.8)
		markers.add_child(lab)

func _fill_dirt_blob(cx: int, cy: int, hw: int, hh: int, till: bool = false) -> void:
	## Stardew-like irregular dirt patch (noisy ellipse), optional tilled core
	for y in range(cy - hh - 3, cy + hh + 4):
		for x in range(cx - hw - 3, cx + hw + 4):
			var dx: float = absf(float(x - cx)) / float(maxi(hw, 1))
			var dy: float = absf(float(y - cy)) / float(maxi(hh, 1))
			var edge: float = sqrt(dx * dx * 0.85 + dy * dy)
			var n: float = float(absi(x * 17 + y * 31) % 11) / 11.0
			var n2: float = float(absi(x * 13 + y * 19) % 7) / 7.0
			var wave: float = 0.14 * sin(float(x) * 0.55 + float(y) * 0.31) + 0.1 * (n - 0.5)
			var rim: float = 1.0 + wave
			if edge < rim * 0.72:
				if till and edge < rim * 0.55 and ((y + cy) % 2) == 0 and x > cx - hw + 1 and x < cx + hw - 1:
					_set_cell(_ground, x, y, T_FARM)
				elif n2 > 0.78:
					_set_cell(_ground, x, y, T_DIRT2)
				else:
					_set_cell(_ground, x, y, T_DIRT)
			elif edge < rim * 0.92:
				## Soft grass↔dirt fringe band
				var pick: int = absi(x * 7 + y * 11) % 5
				if pick == 0:
					_set_cell(_ground, x, y, T_GD_N if dy > dx else T_GD_E)
				elif pick == 1:
					_set_cell(_ground, x, y, T_GD_S if dy > dx else T_GD_W)
				elif pick == 2:
					_set_cell(_ground, x, y, T_DIRT2)
				elif pick == 3:
					_set_cell(_ground, x, y, T_GRASS3)
				else:
					_set_cell(_ground, x, y, T_GRASS4)
			elif edge < rim * 1.05 and n > 0.55:
				## Occasional dirt spit / grass pocket outside
				if n2 > 0.7:
					_set_cell(_ground, x, y, T_DIRT2)
				else:
					_set_cell(_ground, x, y, T_GRASS2)

func _fringe_soft(bed: Rect2i) -> void:
	## Stardew blob rim: nibble dirt→grass, protrude dirt into grass, GD seam tiles
	var x0 := bed.position.x
	var y0 := bed.position.y
	var x1 := x0 + bed.size.x - 1
	var y1 := y0 + bed.size.y - 1
	## Cut hard corners into grass pockets
	for c in [
		Vector2i(x0, y0), Vector2i(x1, y0), Vector2i(x0, y1), Vector2i(x1, y1),
		Vector2i(x0 + 1, y0), Vector2i(x1 - 1, y0), Vector2i(x0, y0 + 1), Vector2i(x1, y0 + 1),
		Vector2i(x0 + 1, y1), Vector2i(x1 - 1, y1), Vector2i(x0, y1 - 1), Vector2i(x1, y1 - 1),
	]:
		if (absi(c.x * 19 + c.y * 23) % 3) != 0:
			_set_cell(_ground, c.x, c.y, T_GRASS3 if ((c.x + c.y) % 2) == 0 else T_GRASS2)
	for x in range(x0, x1 + 1):
		var n: int = absi(x * 13 + y0 * 7) % 6
		if n == 0:
			_set_cell(_ground, x, y0, T_GRASS4)
		elif n == 1:
			_set_cell(_ground, x, y0, T_GD_N)
		elif n >= 4:
			_set_cell(_ground, x, y0 - 1, T_DIRT2 if (n == 5) else T_GD_S)
		var s: int = absi(x * 11 + y1 * 9) % 6
		if s == 0:
			_set_cell(_ground, x, y1, T_GRASS2)
		elif s == 1:
			_set_cell(_ground, x, y1, T_GD_S)
		elif s >= 4:
			_set_cell(_ground, x, y1 + 1, T_DIRT if (s == 5) else T_GD_N)
	for y in range(y0, y1 + 1):
		var w: int = absi(y * 11 + x0 * 5) % 6
		if w == 0:
			_set_cell(_ground, x0, y, T_GRASS4)
		elif w == 1:
			_set_cell(_ground, x0, y, T_GD_W)
		elif w >= 4:
			_set_cell(_ground, x0 - 1, y, T_DIRT2 if (w == 5) else T_GD_E)
		var e: int = absi(y * 17 + x1 * 3) % 6
		if e == 0:
			_set_cell(_ground, x1, y, T_GRASS3)
		elif e == 1:
			_set_cell(_ground, x1, y, T_GD_E)
		elif e >= 4:
			_set_cell(_ground, x1 + 1, y, T_DIRT if (e == 5) else T_GD_W)

func world_size() -> Vector2:
	return Vector2(W * TS, H * TS)

func _setup_tileset() -> void:
	var path := "res://assets/tiles/tileset_master.png"
	var abs_path := ProjectSettings.globalize_path(path)
	var img := Image.new()
	if img.load(abs_path) != OK:
		push_error("Missing tileset_master.png")
		return
	var tex := ImageTexture.create_from_image(img)
	var ts := TileSet.new()
	ts.tile_size = Vector2i(TS, TS)
	var src := TileSetAtlasSource.new()
	src.texture = tex
	src.texture_region_size = Vector2i(TS, TS)
	for i in range(32):
		var atlas_coords := Vector2i(i % 8, i >> 3)
		if not src.has_tile(atlas_coords):
			src.create_tile(atlas_coords)
	ts.add_source(src, 0)
	_ground.tile_set = ts
	_water.tile_set = ts
	_ground.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	_water.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST

func _set_cell(layer: TileMapLayer, x: int, y: int, tid: int) -> void:
	if x < 0 or y < 0 or x >= W or y >= H:
		return
	var atlas := Vector2i(tid % 8, tid >> 3)
	layer.set_cell(Vector2i(x, y), 0, atlas)

func _fill_rect(layer: TileMapLayer, r: Rect2i, tid: int) -> void:
	for y in range(r.position.y, r.position.y + r.size.y):
		for x in range(r.position.x, r.position.x + r.size.x):
			_set_cell(layer, x, y, tid)

func _paint_plaza_soft(cx: int, cy: int, hw: int, hh: int) -> void:
	## Soft oval plaza — heavy dither fringe + interior grass pockets
	for y in range(cy - hh - 3, cy + hh + 4):
		for x in range(cx - hw - 3, cx + hw + 4):
			var dx: float = absf(float(x - cx)) / float(maxi(hw, 1))
			var dy: float = absf(float(y - cy)) / float(maxi(hh, 1))
			var edge: float = maxf(dx, dy)
			var n: float = float((x * 17 + y * 31) % 11) / 11.0
			var n2: float = float((x * 13 + y * 19) % 7) / 7.0
			if edge < 0.55:
				if n2 > 0.82:
					_set_cell(_ground, x, y, T_DIRT2)
				elif n > 0.7:
					_set_cell(_ground, x, y, T_PLAZA2)
				else:
					_set_cell(_ground, x, y, T_PLAZA)
			elif edge < 0.72:
				if n > 0.35:
					_set_cell(_ground, x, y, T_PLAZA if ((x + y) % 2 == 0) else T_PLAZA2)
				elif n > 0.15:
					_set_cell(_ground, x, y, T_DIRT)
				elif n2 > 0.5:
					_set_cell(_ground, x, y, T_GRASS3)
			elif edge < 0.88:
				if n > 0.55:
					_set_cell(_ground, x, y, T_DIRT)
				elif n > 0.28:
					_set_cell(_ground, x, y, T_GRASS3 if ((x + y) % 2 == 0) else T_GRASS2)
				elif n2 > 0.6:
					_set_cell(_ground, x, y, T_GRASS4)
			elif edge < 1.05:
				if n > 0.45:
					_set_cell(_ground, x, y, T_GRASS4 if (x % 2 == 0) else T_DIRT)
				elif n2 > 0.55:
					_set_cell(_ground, x, y, T_GRASS2)

func _paint_path_winding(a: Vector2i, b: Vector2i, steps: int) -> void:
	## Continuous 2–3 tile dirt spine (readable at overview) + soft organic shoulders
	for i in range(steps + 1):
		var t: float = float(i) / float(maxi(steps, 1))
		var wobble_x: float = 7.2 * sin(t * PI * 4.2 + float(a.x) * 0.13)
		wobble_x += 3.1 * sin(t * PI * 9.0 + float(a.y) * 0.07)
		var wobble_y: float = 5.0 * sin(t * PI * 3.1 + float(a.y) * 0.11)
		wobble_y += 2.4 * cos(t * PI * 7.5 + float(a.x) * 0.05)
		var x: int = int(lerpf(float(a.x), float(b.x), t) + wobble_x)
		var y: int = int(lerpf(float(a.y), float(b.y), t) + wobble_y)
		x = clampi(x, 2, W - 4)
		y = clampi(y, 2, H - 4)
		## Never punch PATH through water bowl (ground/water desync)
		if _water_blocks_path(x, y) or _water_blocks_path(x + 1, y):
			continue
		## Solid spine — avoid spray-dot corridors at overview zoom
		_set_path_cell(x, y, T_PATH if (i % 3 != 0) else T_PATH2)
		_set_path_cell(x + 1, y, T_PATH2 if (i % 2 == 0) else T_PATH)
		_set_path_cell(x, y + 1, T_PATH if (i % 5 != 0) else T_DIRT2)
		_set_path_cell(x + 1, y + 1, T_PATH2 if (i % 4 == 0) else T_DIRT)
		if i % 2 == 0:
			_set_path_cell(x + 2, y, T_DIRT2 if (i % 6 == 0) else T_PATH)
			_set_path_cell(x - 1, y + 1, T_DIRT if (i % 5 == 0) else T_PATH2)
		# Organic fringe: dirt nubs + grass dither (less brick corridor)
		var ox := (i % 5) - 2
		var oy := ((i * 3) % 5) - 2
		if i % 2 == 0:
			_set_path_cell(x - 1 + ox, y + oy, T_DIRT)
			_set_path_cell(x + 2 - ox, y, T_DIRT)
		if i % 3 == 0:
			_set_path_cell(x + ox, y - 1, T_DIRT)
			_set_path_cell(x + 1 + ox, y + 2, T_DIRT)
		if i % 4 == 0:
			_set_path_cell(x - 1, y + 1 + oy, T_GRASS2)
			_set_path_cell(x + 2, y - 1, T_GRASS3)
		if i % 5 == 0:
			_set_path_cell(x + 1, y - 1 + oy, T_GRASS3)
			_set_path_cell(x - 1, y + 1, T_GRASS2)
			_set_path_cell(x + 3, y + oy, T_GRASS4)
		if i % 6 == 0:
			_set_path_cell(x + ox, y + 2, T_GRASS)
			_set_path_cell(x + 2 + ox, y + 1, T_DIRT)
		if i % 7 == 0:
			_set_path_cell(x + 2, y + 1, T_GRASS4)
			_set_path_cell(x - 1, y - 1, T_DIRT)
			_set_path_cell(x - 2, y + oy, T_GRASS3)
		if i % 2 == 1:
			_set_path_cell(x - 2 + ox, y + oy, T_GRASS3 if (i % 4 == 1) else T_DIRT)
			_set_path_cell(x + 3 - ox, y + 1, T_GRASS2 if (i % 3 == 0) else T_DIRT)
		if i % 8 == 0:
			_set_path_cell(x + ox, y - 2, T_GRASS4)
			_set_path_cell(x + 1 + ox, y + 3, T_GRASS)

func _water_blocks_path(x: int, y: int) -> bool:
	if _water.get_cell_source_id(Vector2i(x, y)) != -1:
		return true
	return _is_waterish(_cell_tid(x, y))

func _set_path_cell(x: int, y: int, tid: int) -> void:
	if _water_blocks_path(x, y):
		return
	_set_cell(_ground, x, y, tid)

func _paint_base() -> void:
	# Coherent meadow patches (8×8 cells) — large soft fields kill overview checkerboard
	for y in range(H):
		for x in range(W):
			var px8: int = x >> 3
			var py8: int = y >> 3
			var patch: int = absi((px8 * 73856093) ^ (py8 * 19349663) ^ (px8 * py8 * 83492791))
			var local: int = absi((x * 374761393 + y * 668265263) ^ (x * y * 127))
			var g: int = T_GRASS
			var m: int = patch % 5
			if m == 0:
				g = T_GRASS2
			elif m == 1:
				g = T_GRASS3
			elif m == 2:
				g = T_GRASS4
			# Soft fringe inside patch — rare neighbor variant (not every other tile)
			if (local % 23) == 0:
				g = T_GRASS if g != T_GRASS else T_GRASS3
			elif (local % 41) == 0:
				g = T_DIRT if (local % 5) == 0 else T_GRASS2
			_set_cell(_ground, x, y, g)
	# North hills — irregular shelf (not solid wall); leave waterfall corridor open
	for x in range(W):
		var hmax := 5 + ((x * 7) % 4)
		if x >= 14 and x <= 38:
			hmax = 2
		elif x >= 66 and x <= 105:
			hmax = 3 + (x % 3)
		for y in range(hmax):
			if ((x + y * 3) % 4) == 0 and y < 2:
				continue
			_set_cell(_ground, x, y, T_HILL)
	# Soft mid-north hills only in patches (not full-width shelf)
	for x in range(0, W, 3):
		if x >= 14 and x <= 38:
			continue
		if ((x * 5) % 7) < 3:
			_set_cell(_ground, x, 8 + (x % 3), T_HILL)
			_set_cell(_ground, x + 1, 9 + (x % 2), T_HILL)
	# Rocky accents sparse
	for x in range(0, W, 13):
		if x >= 14 and x <= 38:
			continue
		_fill_rect(_ground, Rect2i(x, 3, 2, 3), T_CLIFF)

	# Z1 farm — Stardew hybrid: irregular dirt CLEARINGS + rectangular tilled beds
	# Animal pen = dirt yard (overview ref), not plain grass
	## Farmhouse / barn dirt aprons (blob, not crop grid)
	_fill_dirt_blob(40, 93, 15, 7, false)
	_fill_dirt_blob(38, 104, 17, 6, false)
	_fill_dirt_blob(28, 100, 8, 4, false)
	## Soft path ribbons (noisy)
	for y in range(76, 108):
		var wob: int = int(1.6 * sin(float(y) * 0.33))
		_set_cell(_ground, 30 + wob, y, T_PATH if (y % 3 != 0) else T_PATH2)
		_set_cell(_ground, 31 + wob, y, T_PATH2 if (y % 4 == 0) else T_DIRT2)
	for x in range(14, 60):
		var wobx: int = int(1.3 * sin(float(x) * 0.38))
		_set_cell(_ground, x, 88 + wobx, T_PATH if (x % 3 != 0) else T_DIRT2)
	## Playable tilled beds (keep FarmPlots cells like 16,78 hoeable)
	var farm_beds := [
		Rect2i(14, 78, 16, 10), Rect2i(34, 78, 16, 10), Rect2i(52, 78, 12, 10),
		Rect2i(14, 92, 16, 8), Rect2i(34, 92, 16, 8),
	]
	for bed in farm_beds:
		_fill_rect(_ground, bed, T_DIRT)
		for row in range(0, bed.size.y - 1, 2):
			_fill_rect(_ground, Rect2i(bed.position.x + 1, bed.position.y + row, bed.size.x - 2, 1), T_FARM)
		_fringe_soft(bed)
		for row in range(0, bed.size.y - 1, 2):
			_fill_rect(_ground, Rect2i(bed.position.x + 1, bed.position.y + row, bed.size.x - 2, 1), T_FARM)
	# Animal pen — dirt yard like overview ref (not plain grass)
	_fill_dirt_blob(34, 116, 11, 5, false)
	for yy in range(113, 121):
		for xx in range(25, 43):
			var h: int = absi(xx * 11 + yy * 7) % 5
			if h <= 2:
				_set_cell(_ground, xx, yy, T_DIRT)
			elif h == 3:
				_set_cell(_ground, xx, yy, T_DIRT2)
			else:
				_set_cell(_ground, xx, yy, T_PATH2)
	_fringe_soft(Rect2i(25, 113, 18, 8))

	# Z2 river winding + soft banks + edges
	for y in range(16, 100):
		var cx := 28 + int(6.0 * sin(y * 0.18))
		for dx in range(-2, 3):
			_set_cell(_water, cx + dx, y, T_WATER)
			_set_cell(_ground, cx + dx, y, T_WATER)
		# Soft irregular banks — wider sand/dirt shoulder (ref-like river edge)
		var wob := (y * 3) % 3 - 1
		_set_cell(_ground, cx - 3 + wob, y, T_SAND if (y % 5 == 0) else (T_WE_E if (y % 2) == 0 else T_GRASS3))
		_set_cell(_ground, cx + 3 - wob, y, T_SAND if (y % 5 == 2) else (T_WE_W if (y % 2) == 0 else T_GRASS2))
		if y % 2 == 0:
			_set_cell(_ground, cx - 4 + wob, y, T_DIRT if (y % 3 == 0) else T_SAND)
			_set_cell(_ground, cx + 4 - wob, y, T_DIRT if (y % 4 == 0) else T_GRASS3)
		if y % 3 == 0:
			_set_cell(_ground, cx - 5, y, T_GRASS4)
			_set_cell(_ground, cx + 5, y, T_DIRT)
			_set_cell(_ground, cx - 2, y, T_SAND)
			_set_cell(_ground, cx + 2, y, T_SAND)
		elif y % 4 == 1:
			_set_cell(_ground, cx - 4 + wob, y, T_DIRT)
			_set_cell(_ground, cx + 4 - wob, y, T_GRASS3)
			_set_cell(_ground, cx - 5 + wob, y, T_GRASS2)
		else:
			_set_cell(_ground, cx - 4, y, T_GRASS2)
			_set_cell(_ground, cx + 4, y, T_GRASS)
			if y % 5 == 3:
				_set_cell(_ground, cx - 5, y, T_SAND)
				_set_cell(_ground, cx + 5, y, T_DIRT)
	# Waterfall amphitheater — rock rim only; interior = water (kill farm/hill banding)
	for x in range(14, 34):
		for y in range(10, 24):
			var dx := x - 24
			var dy := y - 15
			var bowl := float(dx * dx) * 0.4 + float(dy * dy) * 1.05
			if bowl < 22.0:
				_set_cell(_water, x, y, T_WATER)
				_set_cell(_ground, x, y, T_WATER)
			elif bowl < 40.0:
				_set_cell(_ground, x, y, T_CLIFF)
			elif bowl < 52.0 and ((x * 3 + y) % 5) != 0:
				_set_cell(_ground, x, y, T_CLIFF)
	# Extend pool mouth into river + soft irregular banks (no hard dirt ladder)
	for x in range(19, 29):
		for y in range(20, 28):
			_set_cell(_water, x, y, T_WATER)
			_set_cell(_ground, x, y, T_WATER)
	# Soft bank fringe — sand / WE / grass (avoid hard cliff ladder at pool mouth)
	for x in range(15, 33):
		for ey in range(26, 30):
			var n: int = absi(x * 13 + ey * 17) % 6
			if n <= 1:
				_set_cell(_ground, x, ey, T_SAND)
			elif n == 2:
				_set_cell(_ground, x, ey, T_WE_N)
			elif n == 3:
				_set_cell(_ground, x, ey, T_DIRT2)
			else:
				_set_cell(_ground, x, ey, T_GRASS3 if (x % 2) == 0 else T_GRASS2)
	# Convert outer amphitheater cliff ring → sand/WE speckles (soft land↔water)
	for x in range(14, 34):
		for y in range(10, 26):
			var dx := x - 24
			var dy := y - 15
			var bowl := float(dx * dx) * 0.4 + float(dy * dy) * 1.05
			if bowl < 40.0 or bowl > 58.0:
				continue
			if _is_waterish(_cell_tid(x, y)):
				continue
			var h: int = absi(x * 19 + y * 23) % 5
			if h <= 1:
				_set_cell(_ground, x, y, T_SAND)
			elif h == 2:
				_set_cell(_ground, x, y, T_WE_S if dy < 0 else T_WE_N)
			elif h == 3:
				_set_cell(_ground, x, y, T_GRASS3)
	for p in [Vector2i(16, 24), Vector2i(17, 25), Vector2i(30, 24), Vector2i(31, 25), Vector2i(18, 26), Vector2i(29, 26)]:
		_set_cell(_ground, p.x, p.y, T_CLIFF)
	# Bridges
	for x in range(24, 34):
		_set_cell(_ground, x, 40, T_BRIDGE)
		_set_cell(_ground, x, 41, T_BRIDGE)
		_water.erase_cell(Vector2i(x, 40))
		_water.erase_cell(Vector2i(x, 41))
	for x in range(24, 34):
		_set_cell(_ground, x, 62, T_BRIDGE)
		_set_cell(_ground, x, 63, T_BRIDGE)
		_water.erase_cell(Vector2i(x, 62))
		_water.erase_cell(Vector2i(x, 63))

	# Z3 plaza — soft oval core + dither fringe (less brick rectangle)
	_paint_plaza_soft(90, 50, 20, 14)
	for x in range(70, 114):
		if (x * 3 + 5) % 7 != 0:
			_set_cell(_ground, x, 35 + ((x * 2) % 2), T_DIRT if (x % 3 == 0) else T_PLAZA)
		if (x * 5 + 1) % 6 != 0:
			_set_cell(_ground, x, 64 + ((x) % 2), T_DIRT if (x % 4 == 0) else T_PLAZA)
		if (x + 2) % 4 == 0:
			_set_cell(_ground, x, 36, T_GRASS3)
			_set_cell(_ground, x, 63, T_GRASS2)
		if (x + 4) % 5 == 0:
			_set_cell(_ground, x, 37, T_DIRT)
			_set_cell(_ground, x, 62, T_GRASS4)
	for y in range(36, 66):
		if (y * 2 + 3) % 5 != 0:
			_set_cell(_ground, 70 + (y % 2), y, T_DIRT if (y % 3 == 0) else T_PLAZA)
			_set_cell(_ground, 113 - (y % 2), y, T_GRASS3 if (y % 4 == 0) else T_PLAZA)
		if y % 3 == 0:
			_set_cell(_ground, 69, y, T_DIRT)
			_set_cell(_ground, 114, y, T_GRASS2)
		if y % 4 == 1:
			_set_cell(_ground, 71, y, T_GRASS4)
			_set_cell(_ground, 112, y, T_DIRT)
		if y % 5 == 2:
			_set_cell(_ground, 72, y, T_GRASS3)
			_set_cell(_ground, 111, y, T_GRASS2)
	# Organic winding dirt paths (stronger wobble + more links)
	_paint_path_winding(Vector2i(42, 92), Vector2i(90, 50), 95)
	_paint_path_winding(Vector2i(90, 50), Vector2i(148, 22), 80)
	_paint_path_winding(Vector2i(90, 55), Vector2i(155, 105), 85)
	_paint_path_winding(Vector2i(48, 88), Vector2i(48, 30), 55)
	_paint_path_winding(Vector2i(40, 90), Vector2i(82, 20), 65)  # farm → ruins
	_paint_path_winding(Vector2i(110, 48), Vector2i(168, 100), 75)  # town → lake
	_paint_path_winding(Vector2i(70, 70), Vector2i(130, 70), 48)  # mid crosslink
	_paint_path_winding(Vector2i(90, 48), Vector2i(28, 24), 70)  # town → waterfall
	## Mid-valley composition — dirt meadows along spines (World-driven, not micro clutter)
	_paint_mid_valley_meadows()

	# Z4 rails + organic station yard (not a solid plaza slab)
	_paint_station_yard()
	# Tunnel cliff mouth on east end of rails
	_fill_rect(_ground, Rect2i(178, 10, 10, 16), T_CLIFF)
	_fill_rect(_ground, Rect2i(180, 14, 6, 8), T_HILL)

	# Z5 terraces — tall dark cliff faces with soft farmable ledges (not brick strips)
	for band in range(5):
		var y0 := 38 + band * 10
		var inset := (band % 3) - 1
		var x0 := 122 + inset
		var w := 42
		# farmable ledge as soft dirt + tilled rows
		var ledge := Rect2i(x0 + 2, y0, w - 2, 3)
		_fill_rect(_ground, ledge, T_DIRT)
		_fill_rect(_ground, Rect2i(x0 + 3, y0 + 1, w - 4, 1), T_FARM)
		_fringe_soft(ledge)
		_fill_rect(_ground, Rect2i(x0 + 3, y0 + 1, w - 4, 1), T_FARM)
		# thick rocky retaining wall / cliff face (must read as elevation)
		_fill_rect(_ground, Rect2i(x0, y0 + 3, w, 5), T_CLIFF)
		for x in range(x0, x0 + w):
			if ((x + band * 3) % 4) == 0:
				_set_cell(_ground, x, y0 + 3, T_HILL)
			if ((x + band) % 5) == 0:
				_set_cell(_ground, x, y0 + 7, T_HILL)
		# grass strip under cliff so next ledge reads lower
		_fill_rect(_ground, Rect2i(x0, y0 + 8, w, 2), T_GRASS2)
		# narrow stair cuts only
		for x in range(134, 138):
			for yy in range(y0 + 3, y0 + 10):
				_set_cell(_ground, x, yy, T_STAIRS)
		if band % 2 == 1:
			for x in range(152, 156):
				for yy in range(y0 + 3, y0 + 10):
					_set_cell(_ground, x, yy, T_STAIRS)

	# Z6 lake — irregular organic bowl (break perfect circle) + soft shore ring
	for y in range(86, 122):
		for x in range(126, 184):
			var dx := float(x - 155)
			var dy := float(y - 104)
			## Multi-frequency shoreline wobble (World-driven lake shape)
			var wob: float = 0.12 * sin(dx * 0.31 + dy * 0.19) + 0.08 * cos(dx * 0.17 - dy * 0.27)
			wob += 0.05 * sin((dx + dy) * 0.41)
			var r2 := (dx * dx) * (1.0 + wob) + (dy * dy) * (1.65 + wob * 0.5)
			if r2 < 820.0:
				var tid := T_DEEP if r2 < 380.0 else T_WATER
				_set_cell(_water, x, y, tid)
				_set_cell(_ground, x, y, tid)
			elif r2 < 1080.0:
				_set_cell(_ground, x, y, T_SAND)
			elif r2 < 1380.0:
				# wider shore fringe — pick edge tile by direction to center
				if absf(dx) > absf(dy) * 1.2:
					_set_cell(_ground, x, y, T_WE_W if dx > 0.0 else T_WE_E)
				elif absf(dy) > absf(dx) * 0.7:
					_set_cell(_ground, x, y, T_WE_N if dy > 0.0 else T_WE_S)
				else:
					_set_cell(_ground, x, y, T_SAND if ((x + y) % 3) == 0 else T_GRASS3)
	# Lighthouse peninsula
	_fill_rect(_ground, Rect2i(168, 98, 10, 12), T_CLIFF)
	_fill_rect(_ground, Rect2i(170, 100, 6, 8), T_SAND)
	for x in range(168, 178):
		for yy in range(100, 108):
			_water.erase_cell(Vector2i(x, yy))
	# Wooden pier
	for x in range(158, 166):
		_set_cell(_ground, x, 110, T_BRIDGE)
		_water.erase_cell(Vector2i(x, 110))
	## Lake-side crop fields (must sit OUTSIDE water ellipse center 155,104)
	## West shore grass (overview: fields beside Echo Lake)
	_fill_dirt_blob(118, 108, 10, 5, false)
	var lake_beds := [
		Rect2i(112, 104, 14, 8),
		Rect2i(112, 114, 12, 6),
	]
	for bed in lake_beds:
		_fill_rect(_ground, bed, T_DIRT)
		for row in range(0, bed.size.y - 1, 2):
			_fill_rect(_ground, Rect2i(bed.position.x + 1, bed.position.y + row, bed.size.x - 2, 1), T_FARM)
		_fringe_soft(bed)
		for row in range(0, bed.size.y - 1, 2):
			_fill_rect(_ground, Rect2i(bed.position.x + 1, bed.position.y + row, bed.size.x - 2, 1), T_FARM)
		## Erase any water cells that leaked under beds
		for yy in range(bed.position.y, bed.position.y + bed.size.y):
			for xx in range(bed.position.x, bed.position.x + bed.size.x):
				_water.erase_cell(Vector2i(xx, yy))
	## Thin south-sand strip crops (y high enough to exit deep water)
	_fill_dirt_blob(150, 126, 12, 2, false)
	for xx in range(140, 168):
		_set_cell(_ground, xx, 125, T_DIRT if (xx % 2) == 0 else T_FARM)
		_set_cell(_ground, xx, 126, T_FARM if (xx % 2) == 0 else T_DIRT2)
		_water.erase_cell(Vector2i(xx, 125))
		_water.erase_cell(Vector2i(xx, 126))
	_fringe_soft(Rect2i(140, 125, 28, 2))

	# Stairs from north hills into farm corridor
	for y in range(14, 24):
		for x in range(44, 48):
			_set_cell(_ground, x, y, T_STAIRS)
	## Stardew-like grass↔dirt seam autotile pass
	_stitch_dirt_seams()
	## Water↔land shore autotile (river + lake hard edges)
	_stitch_water_shores()
	## Extra path/plaza fringe soften (overview hard edges)
	_soften_path_edges()
	## Re-assert corridor spines after lake/terrace/yard stomps (stop at shores — no PATH through water)
	_paint_path_winding(Vector2i(42, 92), Vector2i(90, 50), 95)
	_paint_path_winding(Vector2i(90, 50), Vector2i(148, 22), 80)  # town → station (after yard)
	_paint_path_winding(Vector2i(90, 55), Vector2i(145, 98), 75)  # toward lake west shore (not bowl center)
	_paint_path_winding(Vector2i(110, 48), Vector2i(148, 98), 70)  # town → lake approach
	_paint_path_winding(Vector2i(55, 80), Vector2i(90, 62), 40)
	_paint_path_winding(Vector2i(100, 72), Vector2i(128, 92), 40)
	## Light soften on final spines only
	_soften_path_edges()
	## Building footings — dirt pads so facades sit on ground (not float)
	_paint_building_footings()

func _paint_station_yard() -> void:
	## Gravel/dirt blob + rails under train (replaces solid plaza rectangle)
	for yy in range(14, 29):
		for xx in range(136, 178):
			var dx := xx - 156
			var dy := yy - 21
			var r2 := float(dx * dx) + float(dy * dy) * 1.85
			if r2 > 268.0 and (absi(xx * 7 + yy * 11) % 4) != 0:
				continue
			## 2D value-noise-ish hash — avoid diagonal stripe from xx*17+yy*13
			var h: int = absi((xx * 73856093) ^ (yy * 19349663) ^ (xx * yy * 83492791)) % 8
			if h <= 1:
				_set_cell(_ground, xx, yy, T_PLAZA2)
			elif h <= 3:
				_set_cell(_ground, xx, yy, T_PATH2)
			elif h <= 5:
				_set_cell(_ground, xx, yy, T_DIRT)
			elif h == 6:
				_set_cell(_ground, xx, yy, T_DIRT2)
			else:
				_set_cell(_ground, xx, yy, T_SAND)
	_fringe_soft(Rect2i(138, 15, 36, 13))
	## Dual rail bands: approach north of hall + track under train
	for x in range(118, 186):
		_set_cell(_ground, x, 18, T_RAIL)
		_set_cell(_ground, x, 19, T_RAIL)
		if x >= 140 and x <= 176:
			_set_cell(_ground, x, 25, T_RAIL)
			_set_cell(_ground, x, 26, T_RAIL)
	## Wood sleeper accents beside platform edge
	for x in range(142, 172, 3):
		_set_cell(_ground, x, 24, T_BRIDGE)
		_set_cell(_ground, x, 27, T_BRIDGE)

func _paint_mid_valley_meadows() -> void:
	## Density gradients along farm↔town↔lake spines — fills overview "dead green"
	## without uniform decoration spam (GAME_VISION / WORLD_DESIGN MID_VALLEY)
	var blobs: Array = [
		Vector2i(55, 78), Vector2i(68, 72), Vector2i(78, 68),
		Vector2i(100, 70), Vector2i(112, 78), Vector2i(120, 88),
		Vector2i(52, 60), Vector2i(64, 55), Vector2i(108, 58),
		Vector2i(130, 70), Vector2i(140, 82), Vector2i(85, 82),
	]
	for b in blobs:
		var cx: int = int(b.x)
		var cy: int = int(b.y)
		var hw: int = 4 + absi(cx * 3 + cy) % 3
		var hh: int = 3 + absi(cx + cy * 2) % 3
		_fill_dirt_blob(cx, cy, hw, hh, false)
	## Continuous mid-ridge shoulders (overview-readable brown mass, not spray)
	for i in range(90):
		var t: float = float(i) / 89.0
		var x: int = int(lerpf(48.0, 88.0, t) + 2.5 * sin(t * PI * 3.2))
		var y: int = int(lerpf(88.0, 58.0, t) + 2.0 * cos(t * PI * 2.4))
		for ox in range(-1, 3):
			for oy in range(-1, 2):
				_set_path_cell(x + ox, y + oy, T_DIRT if ((x + ox + y + oy) % 3) != 0 else T_DIRT2)
	for i in range(70):
		var t2: float = float(i) / 69.0
		var x2: int = int(lerpf(90.0, 140.0, t2) + 3.0 * sin(t2 * PI * 2.8))
		var y2: int = int(lerpf(62.0, 98.0, t2) + 2.2 * sin(t2 * PI * 4.1))
		for ox in range(-1, 3):
			for oy in range(-1, 2):
				_set_path_cell(x2 + ox, y2 + oy, T_PATH if ((i + ox) % 4) == 0 else T_DIRT)
	## Sparse secondary path links (composition, not noise)
	_paint_path_winding(Vector2i(55, 80), Vector2i(90, 62), 40)
	_paint_path_winding(Vector2i(100, 72), Vector2i(130, 95), 45)
	_paint_path_winding(Vector2i(70, 55), Vector2i(110, 55), 35)

func _soften_path_edges() -> void:
	## Nibble path/plaza borders into grass + GD tiles (breaks overview brick-read)
	var extras: Array = []
	for y in range(H):
		for x in range(W):
			var tid: int = _cell_tid(x, y)
			if tid != T_PATH and tid != T_PATH2 and tid != T_PLAZA and tid != T_PLAZA2:
				continue
			for d in [Vector2i(0, -1), Vector2i(0, 1), Vector2i(-1, 0), Vector2i(1, 0)]:
				var nx: int = x + d.x
				var ny: int = y + d.y
				if not _is_grassish(_cell_tid(nx, ny)):
					continue
				var n: int = absi(nx * 13 + ny * 17) % 6
				if n == 0:
					extras.append([nx, ny, T_GD_S if d.y < 0 else (T_GD_N if d.y > 0 else (T_GD_E if d.x < 0 else T_GD_W))])
				elif n == 1:
					extras.append([nx, ny, T_GRASS3])
				elif n == 2:
					extras.append([nx, ny, T_DIRT2])
	for item in extras:
		_set_cell(_ground, int(item[0]), int(item[1]), int(item[2]))

func _is_dirtish(tid: int) -> bool:
	return tid == T_DIRT or tid == T_DIRT2 or tid == T_FARM or tid == T_PATH or tid == T_PATH2 or tid == T_SAND

func _is_grassish(tid: int) -> bool:
	return tid == T_GRASS or tid == T_GRASS2 or tid == T_GRASS3 or tid == T_GRASS4

func _is_waterish(tid: int) -> bool:
	return tid == T_WATER or tid == T_DEEP

func _is_shoreable(tid: int) -> bool:
	## Land tiles that can host a water-edge fringe (not structures / beds)
	if tid < 0:
		return false
	if _is_waterish(tid):
		return false
	if tid == T_CLIFF or tid == T_HILL or tid == T_BRIDGE or tid == T_RAIL or tid == T_STAIRS:
		return false
	if tid == T_FARM or tid == T_PLAZA or tid == T_PLAZA2:
		return false
	return true

func _cell_tid(x: int, y: int) -> int:
	if x < 0 or y < 0 or x >= W or y >= H:
		return -1
	var data: Variant = _ground.get_cell_atlas_coords(Vector2i(x, y))
	if typeof(data) != TYPE_VECTOR2I:
		return -1
	var ac: Vector2i = data
	if ac.x < 0:
		return -1
	return ac.x + ac.y * 8

func _stitch_water_shores() -> void:
	## 1) Soften OUTER water cells themselves (replace solid blue with WE facing land)
	## 2) Place WE_* on adjacent land for a second fringe ring
	var edge_water: Array = []
	var land_fringe: Array = []
	for y in range(H):
		for x in range(W):
			if not _is_waterish(_cell_tid(x, y)):
				continue
			var n_land := _is_shoreable(_cell_tid(x, y - 1))
			var s_land := _is_shoreable(_cell_tid(x, y + 1))
			var w_land := _is_shoreable(_cell_tid(x - 1, y))
			var e_land := _is_shoreable(_cell_tid(x + 1, y))
			if n_land or s_land or w_land or e_land:
				## Prefer cardinal with strongest land contact; WE side = water bite toward land
				var we: int = T_WE_S if n_land else (T_WE_N if s_land else (T_WE_E if w_land else T_WE_W))
				if n_land and (e_land or w_land):
					we = T_WE_S
				elif s_land and (e_land or w_land):
					we = T_WE_N
				edge_water.append([x, y, we])
			if n_land:
				land_fringe.append([x, y - 1, T_SAND if (absi(x + y) % 3) == 0 else T_WE_S])
			if s_land:
				land_fringe.append([x, y + 1, T_SAND if (absi(x * 2 + y) % 3) == 0 else T_WE_N])
			if w_land:
				land_fringe.append([x - 1, y, T_DIRT2 if (absi(x + y * 2) % 3) == 0 else T_WE_E])
			if e_land:
				land_fringe.append([x + 1, y, T_DIRT2 if (absi(x * 3 + y) % 3) == 0 else T_WE_W])
			for d in [Vector2i(-1, -1), Vector2i(1, -1), Vector2i(-1, 1), Vector2i(1, 1)]:
				var nx: int = x + d.x
				var ny: int = y + d.y
				if not _is_shoreable(_cell_tid(nx, ny)):
					continue
				var n: int = absi(nx * 19 + ny * 23) % 5
				## Prefer sand/grass speckles over WE on land (less jagged hero shores)
				if n <= 1:
					land_fringe.append([nx, ny, T_SAND])
				elif n == 2:
					land_fringe.append([nx, ny, T_GRASS3])
				elif n == 3:
					land_fringe.append([nx, ny, T_DIRT2])
				else:
					land_fringe.append([nx, ny, T_WE_S if d.y < 0 else T_WE_N])
	for item in edge_water:
		var ex: int = int(item[0])
		var ey: int = int(item[1])
		var et: int = int(item[2])
		## Soft edge on Water layer only — keep ground as water for collision
		_set_cell(_water, ex, ey, et)
	for item in land_fringe:
		_set_cell(_ground, int(item[0]), int(item[1]), int(item[2]))

func _stitch_dirt_seams() -> void:
	## For each dirtish cell, if neighbor is grass, place transition on the GRASS side
	## (keeps farmland interior intact; seams read as soft like Stardew)
	var to_set: Array = []
	for y in range(H):
		for x in range(W):
			var tid: int = _cell_tid(x, y)
			if not _is_dirtish(tid):
				continue
			# north neighbor grass → put GD_S on that grass cell (dirt below jag)
			if _is_grassish(_cell_tid(x, y - 1)):
				to_set.append([x, y - 1, T_GD_S])
			if _is_grassish(_cell_tid(x, y + 1)):
				to_set.append([x, y + 1, T_GD_N])
			if _is_grassish(_cell_tid(x - 1, y)):
				to_set.append([x - 1, y, T_GD_E])
			if _is_grassish(_cell_tid(x + 1, y)):
				to_set.append([x + 1, y, T_GD_W])
			# outer corners on grass diagonal
			if _is_grassish(_cell_tid(x - 1, y - 1)):
				to_set.append([x - 1, y - 1, T_GD_NE])
			if _is_grassish(_cell_tid(x + 1, y - 1)):
				to_set.append([x + 1, y - 1, T_GD_NW])
			if _is_grassish(_cell_tid(x - 1, y + 1)):
				to_set.append([x - 1, y + 1, T_GD_SE])
			if _is_grassish(_cell_tid(x + 1, y + 1)):
				to_set.append([x + 1, y + 1, T_GD_SW])
	for item in to_set:
		_set_cell(_ground, int(item[0]), int(item[1]), int(item[2]))

func _paint_building_footings() -> void:
	## Soft dirt/deck pads under key buildings (embed facades)
	var pads := [
		Rect2i(36, 90, 10, 4),   # farmhouse
		Rect2i(24, 104, 12, 4),  # barn
		Rect2i(44, 106, 12, 3),  # barn2
		Rect2i(74, 52, 10, 3),   # shop
		Rect2i(98, 52, 10, 3),   # cafe
		Rect2i(86, 64, 10, 3),   # bakery
		Rect2i(148, 19, 12, 4),  # station hall apron only (do not remash full yard/rails)
		Rect2i(170, 102, 8, 4),  # lighthouse
	]
	for pad in pads:
		for yy in range(pad.position.y, pad.position.y + pad.size.y):
			for xx in range(pad.position.x, pad.position.x + pad.size.x):
				var cur: int = _cell_tid(xx, yy)
				## Preserve rails / sleepers / cliffs painted by station yard
				if cur == T_RAIL or cur == T_BRIDGE or cur == T_CLIFF or cur == T_STAIRS:
					continue
				var h: int = absi(xx * 17 + yy * 13) % 5
				if h <= 2:
					_set_cell(_ground, xx, yy, T_DIRT)
				elif h == 3:
					_set_cell(_ground, xx, yy, T_PATH2)
				else:
					_set_cell(_ground, xx, yy, T_DIRT2)
		_fringe_soft(pad)
	## Re-assert station dual rails after any fringe nibble
	for x in range(118, 186):
		_set_cell(_ground, x, 18, T_RAIL)
		_set_cell(_ground, x, 19, T_RAIL)
		if x >= 140 and x <= 176:
			_set_cell(_ground, x, 25, T_RAIL)
			_set_cell(_ground, x, 26, T_RAIL)
	for x in range(142, 172, 3):
		_set_cell(_ground, x, 24, T_BRIDGE)
		_set_cell(_ground, x, 27, T_BRIDGE)
	## Farmhouse raised wood porch (bridge tiles as deck planks + step)
	for xx in range(37, 46):
		_set_cell(_ground, xx, 90, T_BRIDGE)
		_set_cell(_ground, xx, 91, T_BRIDGE)
		if (xx % 2) == 0:
			_set_cell(_ground, xx, 92, T_PATH)
		else:
			_set_cell(_ground, xx, 92, T_DIRT2)
	_set_cell(_ground, 40, 92, T_STAIRS)
	_set_cell(_ground, 41, 92, T_STAIRS)
	_set_cell(_ground, 42, 92, T_STAIRS)

func _build_water_collisions() -> void:
	for c in _colliders.get_children():
		c.queue_free()
	for y in range(H):
		for x in range(W):
			var data := _ground.get_cell_tile_data(Vector2i(x, y))
			if data == null:
				continue
			var atlas: Vector2i = _ground.get_cell_atlas_coords(Vector2i(x, y))
			var tid := atlas.x + atlas.y * 8
			if tid != T_WATER and tid != T_DEEP and tid != T_CLIFF and tid != T_HILL:
				continue
			# stairs override: skip if stairs painted on cliff band
			if tid == T_HILL and x >= 44 and x <= 47 and y >= 14 and y <= 23:
				continue
			var body := StaticBody2D.new()
			body.position = Vector2(x * TS + TS * 0.5, y * TS + TS * 0.5)
			var cs := CollisionShape2D.new()
			var rect := RectangleShape2D.new()
			rect.size = Vector2(TS, TS)
			cs.shape = rect
			body.add_child(cs)
			_colliders.add_child(body)
