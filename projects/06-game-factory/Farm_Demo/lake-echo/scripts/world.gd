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
	for name in labels.keys():
		var lab := Label.new()
		lab.text = str(name)
		lab.position = labels[name] * TS
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
	for i in range(16):
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

func _paint_base() -> void:
	# Full grass
	_fill_rect(_ground, Rect2i(0, 0, W, H), T_GRASS)
	# North hills
	_fill_rect(_ground, Rect2i(0, 0, W, 14), T_HILL)
	_fill_rect(_ground, Rect2i(0, 14, W, 4), T_CLIFF)

	# Z1 farm soil
	_fill_rect(_ground, ZONES["Z1_FARM"], T_DIRT)
	_fill_rect(_ground, Rect2i(16, 80, 40, 24), T_FARM)

	# Z2 river winding
	for y in range(16, 100):
		var cx := 28 + int(6.0 * sin(y * 0.18))
		for dx in range(-2, 3):
			_set_cell(_water, cx + dx, y, T_WATER)
			_set_cell(_ground, cx + dx, y, T_WATER)
		_set_cell(_ground, cx - 3, y, T_DIRT)
		_set_cell(_ground, cx + 3, y, T_DIRT)
	# Waterfall head
	_fill_rect(_ground, Rect2i(18, 16, 8, 6), T_CLIFF)
	for x in range(20, 26):
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

	# Z3 plaza
	_fill_rect(_ground, Rect2i(72, 36, 40, 28), T_PLAZA)
	# paths into plaza
	for x in range(40, 72):
		_set_cell(_ground, x, 50, T_PATH)
		_set_cell(_ground, x, 51, T_PATH)
	for y in range(50, 90):
		_set_cell(_ground, 48, y, T_PATH)
		_set_cell(_ground, 49, y, T_PATH)

	# Z4 rails
	for x in range(120, 184):
		_set_cell(_ground, x, 20, T_RAIL)
		_set_cell(_ground, x, 21, T_RAIL)
	_fill_rect(_ground, Rect2i(140, 16, 20, 12), T_PLAZA)

	# Z5 terrace bands
	for band in range(3):
		var y0 := 44 + band * 10
		_fill_rect(_ground, Rect2i(124, y0, 36, 4), T_FARM)
		_fill_rect(_ground, Rect2i(124, y0 + 4, 36, 2), T_CLIFF)
		for x in range(130, 136):
			_set_cell(_ground, x, y0 + 4, T_STAIRS)
			_set_cell(_ground, x, y0 + 5, T_STAIRS)

	# Z6 lake
	for y in range(88, 120):
		for x in range(130, 180):
			var dx := x - 155
			var dy := y - 104
			if dx * dx + dy * dy * 2 < 900:
				_set_cell(_water, x, y, T_DEEP if dx * dx + dy * dy * 2 < 400 else T_WATER)
				_set_cell(_ground, x, y, T_DEEP if dx * dx + dy * dy * 2 < 400 else T_WATER)
			elif dx * dx + dy * dy * 2 < 1100:
				_set_cell(_ground, x, y, T_SAND)
	# Lighthouse pad
	_fill_rect(_ground, Rect2i(168, 100, 6, 8), T_CLIFF)

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
