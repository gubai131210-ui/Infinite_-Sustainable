extends Node2D
## Paper Isle world: terrain, props, stars, decor pads, fox.

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

var _fox: Node = null
var _pads_visible: bool = false

func _ready() -> void:
	_build_tileset()
	_paint_island()
	_spawn_props()
	_spawn_stars()
	_spawn_pads()
	_spawn_fox_slot()
	GameState.phase_changed.connect(_on_phase)
	GameState.reset()

func bind_hud(_hud: Node) -> void:
	pass  # HUD listens to GameState directly

func _on_phase(phase: int) -> void:
	if phase == GameState.Phase.DECORATE:
		_show_pads(true)
	elif phase == GameState.Phase.FOX:
		_show_pads(false)
		if _fox and _fox.has_method("activate"):
			_fox.call("activate", Vector2(16 * TS, 10 * TS))
	elif phase == GameState.Phase.DONE:
		_show_pads(false)

func _show_pads(on: bool) -> void:
	_pads_visible = on
	for n in get_tree().get_nodes_in_group("decor_pad"):
		n.visible = on
		n.monitoring = on

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
				var path_h: bool = absi(y - int(MAP_H * 0.55)) <= 1 and x > 6 and x < MAP_W - 6
				var path_v: bool = absi(x - int(MAP_W * 0.45)) <= 1 and y > 5 and y < MAP_H - 6
				if path_h or path_v:
					id = ID_PATH
			ground.set_cell(Vector2i(x, y), 0, Vector2i(id, 0))

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

func _load_tex(path: String) -> Texture2D:
	if ResourceLoader.exists(path):
		var cached := load(path) as Texture2D
		if cached:
			return cached
	var img := Image.new()
	if img.load(path) != OK:
		push_warning("Missing texture: %s" % path)
		return null
	return ImageTexture.create_from_image(img)

func _spawn_sprite(path: String, pos: Vector2, coll_size: Vector2 = Vector2.ZERO) -> Node2D:
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
	spr.texture = _load_tex(path)
	spr.centered = true
	spr.position = Vector2(0, -8)
	spr.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	root.add_child(spr)
	root.position = pos
	entities.add_child(root)
	return root

func _spawn_props() -> void:
	entities.y_sort_enabled = true
	_spawn_sprite("res://assets/processed/cottage.png", Vector2(14 * TS, 9 * TS), Vector2(70, 40))
	_spawn_sprite("res://assets/processed/tree.png", Vector2(10 * TS, 7 * TS), Vector2(28, 20))
	_spawn_sprite("res://assets/processed/tree.png", Vector2(18 * TS, 8 * TS), Vector2(28, 20))
	_spawn_sprite("res://assets/processed/tree.png", Vector2(12 * TS, 13 * TS), Vector2(28, 20))
	_spawn_sprite("res://assets/processed/flowers.png", Vector2(16 * TS, 12 * TS))
	_spawn_sprite("res://assets/processed/sign.png", Vector2(13 * TS, 11 * TS), Vector2(20, 16))

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
		star.collected.connect(_on_star_collected)

func _on_star_collected() -> void:
	GameState.add_star()

func _spawn_pads() -> void:
	var pad_scene := load("res://scenes/decor_pad.tscn") as PackedScene
	var spots := [
		Vector2(12.5 * TS, 10.5 * TS),
		Vector2(15.5 * TS, 10.2 * TS),
		Vector2(14.0 * TS, 11.8 * TS),
	]
	for p in spots:
		var pad := pad_scene.instantiate()
		pad.position = p
		pad.visible = false
		pad.monitoring = false
		pad.placed.connect(_on_pad_placed)
		entities.add_child(pad)

func _on_pad_placed(pad: Area2D, prop: String) -> void:
	var path := "res://assets/processed/lantern.png" if prop == "lantern" else "res://assets/processed/flowers.png"
	var item := _spawn_sprite(path, pad.position + Vector2(0, -6))
	item.scale = Vector2(0.2, 0.2)
	var tw := create_tween()
	tw.tween_property(item, "scale", Vector2.ONE, 0.35).set_trans(Tween.TRANS_BACK)

func _spawn_fox_slot() -> void:
	var fox_scene := load("res://scenes/fox.tscn") as PackedScene
	_fox = fox_scene.instantiate()
	entities.add_child(_fox)
