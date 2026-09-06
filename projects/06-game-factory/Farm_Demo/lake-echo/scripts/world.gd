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
	_spawn_zone_labels()

func _spawn_zone_labels() -> void:
	var markers := $ZoneMarkers
	var labels := {
		"农场 Z1": Vector2(40, 90),
		"河流 Z2": Vector2(28, 50),
		"镇广场 Z3": Vector2(90, 48),
		"车站 Z4": Vector2(150, 22),
		"梯田 Z5": Vector2(140, 55),
		"湖·灯塔 Z6": Vector2(170, 108),
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
	var tex: Texture2D = load("res://assets/tiles/tileset_master.png")
	var ts := TileSet.new()
	ts.tile_size = Vector2i(TS, TS)
	var src := TileSetAtlasSource.new()
	src.texture = tex
	src.texture_region_size = Vector2i(TS, TS)
	for i in range(32):
		var atlas_coords := Vector2i(i % 8, int(i / 8))
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
	var atlas := Vector2i(tid % 8, int(tid / 8))
	layer.set_cell(Vector2i(x, y), 0, atlas)

func _fill_rect(layer: TileMapLayer, r: Rect2i, tid: int) -> void:
	for y in range(r.position.y, r.position.y + r.size.y):
		for x in range(r.position.x, r.position.x + r.size.x):
			_set_cell(layer, x, y, tid)

func _paint_path_winding(a: Vector2i, b: Vector2i, steps: int) -> void:
	for i in range(steps + 1):
		var t: float = float(i) / float(maxi(steps, 1))
		var wobble_x: float = 2.5 * sin(t * PI * 4.0 + float(a.x) * 0.1)
		var wobble_y: float = 1.8 * sin(t * PI * 3.0 + float(a.y) * 0.07)
		var x: int = int(lerpf(float(a.x), float(b.x), t) + wobble_x)
		var y: int = int(lerpf(float(a.y), float(b.y), t) + wobble_y)
		_set_cell(_ground, x, y, T_PATH)
		_set_cell(_ground, x + 1, y, T_PATH)
		_set_cell(_ground, x, y + 1, T_PATH)
		if i % 3 == 0:
			_set_cell(_ground, x - 1, y, T_DIRT)
			_set_cell(_ground, x + 2, y, T_DIRT)

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
	# North hills
	_fill_rect(_ground, Rect2i(0, 0, W, 14), T_HILL)
	_fill_rect(_ground, Rect2i(0, 14, W, 4), T_CLIFF)

	# Z1 farm soil — irregular blob (not hard rectangle)
	for y in range(72, 118):
		for x in range(10, 68):
			var dx := x - 38
			var dy := y - 94
			if dx * dx + int(dy * dy * 0.7) < 780 + ((x * 13 + y) % 40):
				_set_cell(_ground, x, y, T_DIRT)
	for row in range(8):
		_fill_rect(_ground, Rect2i(16, 80 + row * 3, 40, 2), T_FARM)

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
	# Organic winding dirt paths (sine wobble, 2-wide)
	_paint_path_winding(Vector2i(42, 92), Vector2i(90, 50), 70)
	_paint_path_winding(Vector2i(90, 50), Vector2i(148, 22), 55)
	_paint_path_winding(Vector2i(90, 55), Vector2i(155, 105), 60)
	_paint_path_winding(Vector2i(48, 88), Vector2i(48, 30), 40)

	# Z4 rails + wider platform
	for x in range(118, 186):
		_set_cell(_ground, x, 18, T_RAIL)
		_set_cell(_ground, x, 19, T_RAIL)
		_set_cell(_ground, x, 20, T_RAIL)
	_fill_rect(_ground, Rect2i(136, 12, 36, 16), T_PLAZA)
	# Tunnel cliff mouth on east end of rails
	_fill_rect(_ground, Rect2i(178, 10, 10, 16), T_CLIFF)
	_fill_rect(_ground, Rect2i(180, 14, 6, 8), T_HILL)

	# Z5 terraces — tall cliff faces (not thin gray stair strips)
	# Pattern per band: farm ledge (3) + stone cliff drop (5) + stairs only in 4-wide columns
	for band in range(5):
		var y0 := 38 + band * 10
		var inset := (band % 3) - 1
		var x0 := 122 + inset
		var w := 42
		# farmable ledge
		_fill_rect(_ground, Rect2i(x0 + 2, y0, w - 2, 3), T_FARM)
		for x in range(x0 + 4, x0 + w - 2, 2):
			_set_cell(_ground, x, y0 + 1, T_DIRT)
		# thick rocky retaining wall / cliff face
		_fill_rect(_ground, Rect2i(x0, y0 + 3, w, 5), T_CLIFF)
		for x in range(x0, x0 + w):
			if ((x + band * 3) % 4) == 0:
				_set_cell(_ground, x, y0 + 3, T_HILL)
			if ((x + band) % 5) == 0:
				_set_cell(_ground, x, y0 + 7, T_HILL)
		# narrow stair cuts only (do not paint stairs across whole band)
		for x in range(134, 138):
			for yy in range(y0 + 3, y0 + 8):
				_set_cell(_ground, x, yy, T_STAIRS)
		if band % 2 == 1:
			for x in range(152, 156):
				for yy in range(y0 + 3, y0 + 8):
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
