extends Node2D
## Farm plots + ground tile rendering + crop sprites.

const W := 96
const H := 64
const TS := 16

enum T { GRASS, DIRT, FARMLAND, TILLED, WATERED, WATER, PATH, HILL }

var grid: Array = []  # row-major int
var plots: Dictionary = {}  # Vector2i -> {crop, stage, waters_done, watered_now}
var stump_cells: Dictionary = {}  # Vector2i -> true (chop once)
var textures: Dictionary = {}
var edge_tex: Dictionary = {}  # "gw_n" etc.
var crop_tex: Dictionary = {}
var _ground: Node2D
var _crops_layer: Node2D
var _player: Node = null

func _ready() -> void:
	_load_textures()
	_ground = Node2D.new()
	_ground.name = "Ground"
	add_child(_ground)
	_crops_layer = Node2D.new()
	_crops_layer.name = "Crops"
	_crops_layer.z_index = 2
	add_child(_crops_layer)
	_build_grid()
	_paint_ground()
	_spawn_stumps()

func set_player(p: Node) -> void:
	_player = p
	if p != null and p.has_method("set_farm"):
		p.set_farm(self)

func _load_textures() -> void:
	textures = {
		T.GRASS: load("res://assets/processed/tile_grass.png"),
		T.DIRT: load("res://assets/processed/tile_dirt.png"),
		T.FARMLAND: load("res://assets/processed/tile_farmland.png"),
		T.TILLED: load("res://assets/processed/tile_tilled.png"),
		T.WATERED: load("res://assets/processed/tile_watered.png"),
		T.WATER: load("res://assets/processed/tile_water.png"),
		T.PATH: load("res://assets/processed/tile_path.png"),
		T.HILL: load("res://assets/processed/tile_hill.png"),
	}
	edge_tex = {
		"gd_n": load("res://assets/processed/tile_gd_n.png"),
		"gd_e": load("res://assets/processed/tile_gd_e.png"),
		"gd_s": load("res://assets/processed/tile_gd_s.png"),
		"gd_w": load("res://assets/processed/tile_gd_w.png"),
		"gw_n": load("res://assets/processed/tile_gw_n.png"),
		"gw_e": load("res://assets/processed/tile_gw_e.png"),
		"gw_s": load("res://assets/processed/tile_gw_s.png"),
		"gw_w": load("res://assets/processed/tile_gw_w.png"),
		"gw_ne": load("res://assets/processed/tile_gw_ne.png"),
		"gw_nw": load("res://assets/processed/tile_gw_nw.png"),
		"gw_se": load("res://assets/processed/tile_gw_se.png"),
		"gw_sw": load("res://assets/processed/tile_gw_sw.png"),
	}
	for crop in ItemDB.CROPS.keys():
		crop_tex[crop] = []
		for s in range(4):
			crop_tex[crop].append(load("res://assets/processed/crop_%s_%d.png" % [crop, s]))

func _idx(x: int, y: int) -> int:
	return y * W + x

func get_tile(x: int, y: int) -> int:
	if x < 0 or y < 0 or x >= W or y >= H:
		return T.HILL
	return int(grid[_idx(x, y)])

func set_tile(x: int, y: int, t: int) -> void:
	if x < 0 or y < 0 or x >= W or y >= H:
		return
	grid[_idx(x, y)] = t

func _build_grid() -> void:
	grid.resize(W * H)
	for y in range(H):
		for x in range(W):
			grid[_idx(x, y)] = T.GRASS

	# North hills
	for y in range(0, 11):
		for x in range(W):
			if y < 7 or (y < 11 and (x + y) % 4 != 0):
				set_tile(x, y, T.HILL)

	# Winding river around x≈28
	for y in range(H):
		var cx := 28 + int(4.0 * sin(y * 0.28))
		for dx in range(-2, 3):
			set_tile(cx + dx, y, T.WATER)
		set_tile(cx - 3, y, T.DIRT)
		set_tile(cx + 3, y, T.DIRT)

	# West farmland
	for y in range(14, 34):
		for x in range(4, 18):
			set_tile(x, y, T.FARMLAND)

	# Farmhouse yard
	for y in range(18, 30):
		for x in range(32, 44):
			if get_tile(x, y) != T.WATER:
				set_tile(x, y, T.DIRT)

	# Paths: farm → village → south pasture
	for x in range(18, 80):
		set_tile(x, 26, T.PATH)
		set_tile(x, 27, T.PATH)
	for y in range(20, 50):
		set_tile(76, y, T.PATH)
		set_tile(77, y, T.PATH)
	for y in range(28, 52):
		set_tile(36, y, T.PATH)
		set_tile(37, y, T.PATH)

	# Village plaza east
	for y in range(20, 36):
		for x in range(70, 90):
			if get_tile(x, y) != T.WATER:
				set_tile(x, y, T.PATH)

	# South pasture (new zone) — keep grass, light dirt patches
	for y in range(46, 58):
		for x in range(22, 48):
			if (x + y) % 7 == 0:
				set_tile(x, y, T.DIRT)

	# East forest floor soft dirt spots
	for y in range(42, 58):
		for x in range(78, 92):
			if (x * 3 + y) % 11 == 0:
				set_tile(x, y, T.DIRT)

func _paint_ground() -> void:
	for c in _ground.get_children():
		c.queue_free()
	for y in range(H):
		for x in range(W):
			var t: int = get_tile(x, y)
			var key := Vector2i(x, y)
			if plots.has(key):
				var p: Dictionary = plots[key]
				t = T.WATERED if bool(p.get("watered_now", false)) else T.TILLED
			var spr := Sprite2D.new()
			spr.texture = _display_tex(x, y, t)
			spr.centered = false
			spr.position = Vector2(x * TS, y * TS)
			spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
			_ground.add_child(spr)
	_refresh_crop_sprites()

func _display_tex(x: int, y: int, t: int) -> Texture2D:
	## Only grass↔water edges (skip grass↔dirt to avoid red-line artifacts).
	if t == T.GRASS:
		var n_water := get_tile(x, y - 1) == T.WATER
		var s_water := get_tile(x, y + 1) == T.WATER
		var e_water := get_tile(x + 1, y) == T.WATER
		var w_water := get_tile(x - 1, y) == T.WATER
		if n_water and e_water and edge_tex.has("gw_ne"):
			return edge_tex["gw_ne"]
		if n_water and w_water and edge_tex.has("gw_nw"):
			return edge_tex["gw_nw"]
		if s_water and e_water and edge_tex.has("gw_se"):
			return edge_tex["gw_se"]
		if s_water and w_water and edge_tex.has("gw_sw"):
			return edge_tex["gw_sw"]
		if n_water and edge_tex.has("gw_n"):
			return edge_tex["gw_n"]
		if s_water and edge_tex.has("gw_s"):
			return edge_tex["gw_s"]
		if e_water and edge_tex.has("gw_e"):
			return edge_tex["gw_e"]
		if w_water and edge_tex.has("gw_w"):
			return edge_tex["gw_w"]
	return textures[t]

func _refresh_crop_sprites() -> void:
	for c in _crops_layer.get_children():
		c.queue_free()
	for key in plots.keys():
		var p: Dictionary = plots[key]
		var crop: String = str(p.get("crop", ""))
		if crop == "":
			continue
		var stage: int = int(p.get("stage", 0))
		stage = clampi(stage, 0, 3)
		var spr := Sprite2D.new()
		spr.texture = crop_tex[crop][stage]
		spr.centered = false
		spr.position = Vector2(key.x * TS, key.y * TS)
		spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		_crops_layer.add_child(spr)

func _spawn_stumps() -> void:
	var spots := [
		Vector2i(8, 12), Vector2i(14, 12), Vector2i(40, 12),
		Vector2i(80, 44), Vector2i(84, 48), Vector2i(88, 50), Vector2i(82, 54),
	]
	for c in spots:
		if get_tile(c.x, c.y) != T.WATER:
			stump_cells[c] = true
			var spr := Sprite2D.new()
			spr.name = "Stump_%d_%d" % [c.x, c.y]
			spr.texture = load("res://assets/processed/item_wood.png")
			spr.centered = false
			spr.position = Vector2(c.x * TS, c.y * TS)
			spr.z_index = 2
			spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
			spr.scale = Vector2(1.5, 1.5)
			add_child(spr)

func is_blocked(cell: Vector2i) -> bool:
	var t := get_tile(cell.x, cell.y)
	return t == T.WATER or t == T.HILL

func world_size() -> Vector2:
	return Vector2(W * TS, H * TS)

func hoe(cell: Vector2i) -> bool:
	var t := get_tile(cell.x, cell.y)
	if t != T.FARMLAND and t != T.DIRT and t != T.TILLED and t != T.WATERED:
		return false
	if plots.has(cell) and str(plots[cell].get("crop", "")) != "":
		return false
	plots[cell] = {"crop": "", "stage": 0, "waters_done": 0, "watered_now": false}
	set_tile(cell.x, cell.y, T.TILLED)
	_paint_ground()
	return true

func plant(cell: Vector2i, seed_id: String) -> bool:
	if not plots.has(cell):
		return false
	var p: Dictionary = plots[cell]
	if str(p.get("crop", "")) != "":
		return false
	if not ItemDB.ITEMS.has(seed_id):
		return false
	var meta: Dictionary = ItemDB.ITEMS[seed_id]
	if str(meta.get("kind", "")) != "seed":
		return false
	var crop: String = str(meta.get("crop", ""))
	p["crop"] = crop
	p["stage"] = 0
	p["waters_done"] = 0
	p["watered_now"] = false
	plots[cell] = p
	_paint_ground()
	return true

func water(cell: Vector2i) -> bool:
	if not plots.has(cell):
		return false
	var p: Dictionary = plots[cell]
	var crop: String = str(p.get("crop", ""))
	if crop == "":
		p["watered_now"] = true
		plots[cell] = p
		_paint_ground()
		return true
	if int(p.get("stage", 0)) >= 3:
		return false
	var need: int = int(ItemDB.CROPS[crop]["waters"])
	var done: int = int(p.get("waters_done", 0)) + 1
	p["waters_done"] = done
	p["watered_now"] = true
	if done >= need:
		p["stage"] = 3
	else:
		p["stage"] = clampi(int(float(done) / float(need) * 3.0), 0, 2)
	plots[cell] = p
	_paint_ground()
	return true

func harvest(cell: Vector2i) -> String:
	if not plots.has(cell):
		return ""
	var p: Dictionary = plots[cell]
	var crop: String = str(p.get("crop", ""))
	if crop == "":
		return ""
	if int(p.get("stage", 0)) < 3:
		return ""
	var item: String = str(ItemDB.CROPS[crop]["item"])
	plots.erase(cell)
	set_tile(cell.x, cell.y, T.FARMLAND)
	_paint_ground()
	return item

func chop(cell: Vector2i) -> bool:
	if not stump_cells.has(cell):
		return false
	stump_cells.erase(cell)
	var node := get_node_or_null("Stump_%d_%d" % [cell.x, cell.y])
	if node != null:
		node.queue_free()
	Inventory.add("wood", 1)
	return true

func build_collisions(parent: Node) -> void:
	for y in range(H):
		for x in range(W):
			var t := get_tile(x, y)
			if t != T.WATER and t != T.HILL:
				continue
			var body := StaticBody2D.new()
			body.position = Vector2(x * TS + TS * 0.5, y * TS + TS * 0.5)
			var cs := CollisionShape2D.new()
			var rect := RectangleShape2D.new()
			rect.size = Vector2(TS, TS)
			cs.shape = rect
			body.add_child(cs)
			parent.add_child(body)
