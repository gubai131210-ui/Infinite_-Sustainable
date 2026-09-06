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
	# zone names shown via wood placards in decor.gd

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
	var markers := $ZoneMarkers
	var labels := {
		"米勒农庄": Vector2(40, 90),
		"橡木河": Vector2(28, 50),
		"镇中心广场": Vector2(90, 48),
		"橡木火车站": Vector2(150, 22),
		"梯田": Vector2(140, 55),
		"回声湖·灯塔": Vector2(170, 108),
	}
	for label_text in labels.keys():
		var lab := Label.new()
		lab.text = str(label_text)
		lab.position = labels[label_text] * TS
		lab.z_index = 30
		lab.add_theme_color_override("font_color", Color(1, 1, 1))
		lab.add_theme_color_override("font_outline_color", Color(0, 0, 0))
		lab.add_theme_constant_override("outline_size", 4)
		markers.add_child(lab)

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

func _paint_path_winding(a: Vector2i, b: Vector2i, steps: int) -> void:
	## Soft organic dirt — stronger multi-frequency wobble + feathered edges
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
		_set_cell(_ground, x, y, T_PATH)
		_set_cell(_ground, x + 1, y, T_PATH)
		if i % 3 != 1:
			_set_cell(_ground, x, y + 1, T_PATH)
		if i % 4 == 0:
			_set_cell(_ground, x + 1, y + 1, T_DIRT)
		# Feathered soft edge (dirt / grass mix — less grid brick)
		if i % 2 == 0:
			_set_cell(_ground, x - 1, y, T_DIRT)
			_set_cell(_ground, x + 2, y, T_DIRT)
		if i % 3 == 0:
			_set_cell(_ground, x, y - 1, T_DIRT)
		if i % 5 == 0:
			_set_cell(_ground, x + 1, y - 1, T_GRASS3)
			_set_cell(_ground, x - 1, y + 1, T_GRASS2)

func _paint_base() -> void:
	# Full grass with noisy variants (avoid diagonal stripe modulo)
	for y in range(H):
		for x in range(W):
			var h := (x * 374761393 + y * 668265263) ^ (x * y * 127)
			h = abs(h)
			var g := T_GRASS
			var m := h % 11
			if m <= 2:
				g = T_GRASS2
			elif m <= 5:
				g = T_GRASS3
			elif m <= 7:
				g = T_GRASS4
			elif m == 8:
				g = T_DIRT if (h % 17) == 0 else T_GRASS
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

	# Z1 farm — rectangular crop beds + grass corridors (like reference), not one brown slab
	# Animal pen stays grass (south of barns)
	var farm_beds := [
		Rect2i(14, 78, 16, 10), Rect2i(34, 78, 16, 10), Rect2i(52, 78, 12, 10),
		Rect2i(14, 92, 16, 8), Rect2i(34, 92, 16, 8),
	]
	for bed in farm_beds:
		_fill_rect(_ground, bed, T_DIRT)
		# inner tilled rows
		for row in range(0, bed.size.y - 1, 2):
			_fill_rect(_ground, Rect2i(bed.position.x + 1, bed.position.y + row, bed.size.x - 2, 1), T_FARM)
	# Path strips between beds
	_fill_rect(_ground, Rect2i(30, 78, 4, 22), T_PATH)
	_fill_rect(_ground, Rect2i(14, 88, 50, 3), T_PATH)
	# Yard around farmhouse / barns — light dirt patches, not wall-to-wall soil
	for y in range(96, 110):
		for x in range(22, 56):
			if ((x + y * 3) % 5) != 0:
				_set_cell(_ground, x, y, T_DIRT)
	# Animal pen floor stays mostly grass (south of barns)
	_fill_rect(_ground, Rect2i(24, 112, 20, 10), T_GRASS2)

	# Z2 river winding + banks + edges
	for y in range(16, 100):
		var cx := 28 + int(6.0 * sin(y * 0.18))
		for dx in range(-2, 3):
			_set_cell(_water, cx + dx, y, T_WATER)
			_set_cell(_ground, cx + dx, y, T_WATER)
		_set_cell(_ground, cx - 3, y, T_WE_E)
		_set_cell(_ground, cx + 3, y, T_WE_W)
		_set_cell(_ground, cx - 4, y, T_DIRT)
		_set_cell(_ground, cx + 4, y, T_DIRT)
	# Waterfall head
	_fill_rect(_ground, Rect2i(16, 14, 14, 8), T_CLIFF)
	for x in range(20, 28):
		_set_cell(_water, x, 22, T_WATER)
		_set_cell(_ground, x, 22, T_WATER)
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

	# Z3 plaza (slightly irregular edge)
	_fill_rect(_ground, Rect2i(72, 36, 40, 28), T_PLAZA)
	for x in range(72, 112):
		if (x + 3) % 7 == 0:
			_set_cell(_ground, x, 35, T_PLAZA)
		if (x + 5) % 6 == 0:
			_set_cell(_ground, x, 64, T_PLAZA)
	# Organic winding dirt paths (stronger wobble + more links)
	_paint_path_winding(Vector2i(42, 92), Vector2i(90, 50), 95)
	_paint_path_winding(Vector2i(90, 50), Vector2i(148, 22), 80)
	_paint_path_winding(Vector2i(90, 55), Vector2i(155, 105), 85)
	_paint_path_winding(Vector2i(48, 88), Vector2i(48, 30), 55)
	_paint_path_winding(Vector2i(40, 90), Vector2i(82, 20), 65)  # farm → ruins
	_paint_path_winding(Vector2i(110, 48), Vector2i(168, 100), 75)  # town → lake
	_paint_path_winding(Vector2i(70, 70), Vector2i(130, 70), 48)  # mid crosslink
	_paint_path_winding(Vector2i(90, 48), Vector2i(28, 24), 70)  # town → waterfall

	# Z4 rails + wider platform
	for x in range(118, 186):
		_set_cell(_ground, x, 18, T_RAIL)
		_set_cell(_ground, x, 19, T_RAIL)
		_set_cell(_ground, x, 20, T_RAIL)
	_fill_rect(_ground, Rect2i(136, 12, 36, 16), T_PLAZA)
	# Tunnel cliff mouth on east end of rails
	_fill_rect(_ground, Rect2i(178, 10, 10, 16), T_CLIFF)
	_fill_rect(_ground, Rect2i(180, 14, 6, 8), T_HILL)

	# Z5 terraces — tall dark cliff faces with grass gap between bands
	for band in range(5):
		var y0 := 38 + band * 10
		var inset := (band % 3) - 1
		var x0 := 122 + inset
		var w := 42
		# farmable ledge
		_fill_rect(_ground, Rect2i(x0 + 2, y0, w - 2, 3), T_FARM)
		for x in range(x0 + 4, x0 + w - 2, 2):
			_set_cell(_ground, x, y0 + 1, T_DIRT)
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

	# Z6 lake + soft shore ring (sand + water-edge tiles)
	for y in range(86, 122):
		for x in range(126, 184):
			var dx := float(x - 155)
			var dy := float(y - 104)
			# slight ellipse wobble
			var r2 := dx * dx + dy * dy * 1.85
			if r2 < 780.0:
				var tid := T_DEEP if r2 < 360.0 else T_WATER
				_set_cell(_water, x, y, tid)
				_set_cell(_ground, x, y, tid)
			elif r2 < 980.0:
				_set_cell(_ground, x, y, T_SAND)
			elif r2 < 1120.0:
				# shore fringe — pick edge tile by direction to center
				if absf(dx) > absf(dy):
					_set_cell(_ground, x, y, T_WE_W if dx > 0.0 else T_WE_E)
				else:
					_set_cell(_ground, x, y, T_WE_N if dy > 0.0 else T_WE_S)
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

	# Stairs from north hills into farm corridor
	for y in range(14, 24):
		for x in range(44, 48):
			_set_cell(_ground, x, y, T_STAIRS)

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
