extends Node2D
## Builds Paper Isle terrain TileMapLayer + props + stars at runtime.

const TS := 64
const MAP_W := 28
const MAP_H := 20

const ID_GRASS := 0
const ID_PATH := 1
const ID_WATER := 2
const ID_GW_N := 3
const ID_GW_S := 4
const ID_GW_E := 5
const ID_GW_W := 6
const ID_GP_N := 7
const ID_GP_S := 8
const ID_GP_E := 9
const ID_GP_W := 10

@onready var ground: TileMapLayer = $Ground
@onready var entities: Node2D = $Entities

var _hud: Node = null

func _ready() -> void:
	_build_tileset()
	_paint_island()
	_spawn_props()
	_spawn_stars()

func bind_hud(hud: Node) -> void:
	_hud = hud
	if _hud and _hud.has_method("set_total"):
		_hud.call("set_total", 5)

func _build_tileset() -> void:
	var atlas_tex := load("res://assets/tiles/atlas_terrain.png") as Texture2D
	var source := TileSetAtlasSource.new()
	source.texture = atlas_tex
	source.texture_region_size = Vector2i(TS, TS)
	for i in range(11):
		source.create_tile(Vector2i(i, 0))

	var ts := TileSet.new()
	ts.tile_size = Vector2i(TS, TS)
	ts.add_physics_layer()
	ts.add_source(source, 0)

	# Water collision on atlas tile (2,0)
	var water_data := source.get_tile_data(Vector2i(ID_WATER, 0), 0)
	water_data.add_collision_polygon(0)
	water_data.set_collision_polygon_points(0, 0, PackedVector2Array([
		Vector2(-TS * 0.5, -TS * 0.5),
		Vector2(TS * 0.5, -TS * 0.5),
		Vector2(TS * 0.5, TS * 0.5),
		Vector2(-TS * 0.5, TS * 0.5),
	]))

	ground.tile_set = ts
	ground.collision_enabled = true

func _in_island(x: int, y: int) -> bool:
	# Soft ellipse island
	var cx := (MAP_W - 1) * 0.5
	var cy := (MAP_H - 1) * 0.5
	var nx := (x - cx) / (MAP_W * 0.42)
	var ny := (y - cy) / (MAP_H * 0.40)
	return nx * nx + ny * ny <= 1.0

func _paint_island() -> void:
	for y in range(MAP_H):
		for x in range(MAP_W):
			var id: int = ID_WATER
			if _in_island(x, y):
				id = ID_GRASS
				# winding path (2 tiles wide)
				var path_h: bool = absi(y - int(MAP_H * 0.55)) <= 1 and x > 6 and x < MAP_W - 6
				var path_v: bool = absi(x - int(MAP_W * 0.45)) <= 1 and y > 5 and y < MAP_H - 6
				if path_h or path_v:
					id = ID_PATH
			ground.set_cell(Vector2i(x, y), 0, Vector2i(id, 0))

	# Shore / path transition tiles
	for y in range(MAP_H):
		for x in range(MAP_W):
			if not _is_id(x, y, ID_GRASS) and not _is_id(x, y, ID_PATH):
				continue
			var n: bool = _is_id(x, y - 1, ID_WATER)
			var s: bool = _is_id(x, y + 1, ID_WATER)
			var e: bool = _is_id(x + 1, y, ID_WATER)
			var w: bool = _is_id(x - 1, y, ID_WATER)
			if n:
				ground.set_cell(Vector2i(x, y), 0, Vector2i(ID_GW_N, 0))
			elif s:
				ground.set_cell(Vector2i(x, y), 0, Vector2i(ID_GW_S, 0))
			elif e:
				ground.set_cell(Vector2i(x, y), 0, Vector2i(ID_GW_E, 0))
			elif w:
				ground.set_cell(Vector2i(x, y), 0, Vector2i(ID_GW_W, 0))
			elif _is_id(x, y, ID_GRASS):
				var pn: bool = _is_id(x, y - 1, ID_PATH)
				var ps: bool = _is_id(x, y + 1, ID_PATH)
				var pe: bool = _is_id(x + 1, y, ID_PATH)
				var pw: bool = _is_id(x - 1, y, ID_PATH)
				if pn:
					ground.set_cell(Vector2i(x, y), 0, Vector2i(ID_GP_N, 0))
				elif ps:
					ground.set_cell(Vector2i(x, y), 0, Vector2i(ID_GP_S, 0))
				elif pe:
					ground.set_cell(Vector2i(x, y), 0, Vector2i(ID_GP_E, 0))
				elif pw:
					ground.set_cell(Vector2i(x, y), 0, Vector2i(ID_GP_W, 0))

func _is_id(x: int, y: int, id: int) -> bool:
	if x < 0 or y < 0 or x >= MAP_W or y >= MAP_H:
		return id == ID_WATER
	var atlas := ground.get_cell_atlas_coords(Vector2i(x, y))
	return atlas == Vector2i(id, 0)

func _spawn_sprite(path: String, pos: Vector2, z: int = 0, coll_size: Vector2 = Vector2.ZERO) -> Node2D:
	var root: Node2D
	if coll_size != Vector2.ZERO:
		var static_b := StaticBody2D.new()
		var cs := CollisionShape2D.new()
		var shape := RectangleShape2D.new()
		shape.size = coll_size
		cs.shape = shape
		cs.position = Vector2(0, -coll_size.y * 0.15)
		static_b.add_child(cs)
		root = static_b
	else:
		root = Node2D.new()
	var spr := Sprite2D.new()
	spr.texture = load(path) as Texture2D
	spr.centered = true
	spr.position = Vector2(0, -8)
	spr.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	root.add_child(spr)
	root.position = pos
	root.z_index = z
	entities.add_child(root)
	return root

func _spawn_props() -> void:
	entities.y_sort_enabled = true
	_spawn_sprite("res://assets/processed/cottage.png", Vector2(14 * TS, 9 * TS), 0, Vector2(70, 40))
	_spawn_sprite("res://assets/processed/tree.png", Vector2(10 * TS, 7 * TS), 0, Vector2(28, 20))
	_spawn_sprite("res://assets/processed/tree.png", Vector2(18 * TS, 8 * TS), 0, Vector2(28, 20))
	_spawn_sprite("res://assets/processed/tree.png", Vector2(12 * TS, 13 * TS), 0, Vector2(28, 20))
	_spawn_sprite("res://assets/processed/flowers.png", Vector2(16 * TS, 12 * TS))
	_spawn_sprite("res://assets/processed/flowers.png", Vector2(9 * TS, 11 * TS))

func _spawn_stars() -> void:
	var spots := [
		Vector2(8 * TS, 10 * TS),
		Vector2(20 * TS, 10 * TS),
		Vector2(14 * TS, 6 * TS),
		Vector2(11 * TS, 14 * TS),
		Vector2(17 * TS, 14 * TS),
	]
	var star_scene := load("res://scenes/star.tscn") as PackedScene
	for p in spots:
		var star := star_scene.instantiate()
		star.position = p
		entities.add_child(star)
		if star.has_signal("collected"):
			star.collected.connect(_on_star_collected)

func _on_star_collected() -> void:
	if _hud and _hud.has_method("add_one"):
		_hud.call("add_one")
