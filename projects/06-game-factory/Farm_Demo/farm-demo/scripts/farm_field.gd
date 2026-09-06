extends Node2D
## Farm plots + ground tile rendering + crop sprites (R4 layout).

const W := 96
const H := 64
const TS := 16

enum T { GRASS, DIRT, FARMLAND, TILLED, WATERED, WATER, PATH, HILL, PLAZA, CLIFF, STAIRS }

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
		T.PLAZA: load("res://assets/processed/tile_plaza.png"),
		T.CLIFF: load("res://assets/processed/tile_cliff.png"),
		T.STAIRS: load("res://assets/processed/tile_stairs.png"),
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

	# North hills + cliff face + stair notch toward farm
	for y in range(0, 10):
		for x in range(W):
			if y < 6:
				set_tile(x, y, T.HILL)
			elif y < 8:
				set_tile(x, y, T.CLIFF)
			else:
				if (x + y) % 5 == 0:
					set_tile(x, y, T.CLIFF)
	# Stairs corridor from hills into farm (x 10-13)
	for y in range(6, 12):
		for x in range(10, 14):
			set_tile(x, y, T.STAIRS)

	# Winding river (video-like soft curve)
	for y in range(H):
		var cx := 30 + int(5.0 * sin(y * 0.22) + 2.0 * sin(y * 0.07))
		for dx in range(-2, 3):
			set_tile(cx + dx, y, T.WATER)
		# dirt banks
		set_tile(cx - 3, y, T.DIRT)
		set_tile(cx + 3, y, T.DIRT)

	# West farmland rows
	for y in range(14, 34):
		for x in range(4, 18):
			set_tile(x, y, T.FARMLAND)

	# Farmhouse yard (west of river bend)
	for y in range(18, 28):
		for x in range(34, 44):
			if get_tile(x, y) != T.WATER:
				set_tile(x, y, T.DIRT)

	# Winding dirt path farm → bridge → village
	for t in range(0, 70):
		var px := 18 + t
		var py := 26 + int(2.0 * sin(t * 0.18))
		set_tile(px, py, T.PATH)
		set_tile(px, py + 1, T.PATH)
	# Bridge strip over river around y~26
	for x in range(26, 36):
		set_tile(x, 25, T.PATH)
		set_tile(x, 26, T.PATH)
		set_tile(x, 27, T.PATH)
	# South spur to pasture
	for y in range(28, 52):
		var ox := 36 + int(1.5 * sin(y * 0.3))
		set_tile(ox, y, T.PATH)
		set_tile(ox + 1, y, T.PATH)
	# East spur to village / forest
	for y in range(20, 50):
		set_tile(76, y, T.PATH)
		set_tile(77, y, T.PATH)

	# Village stone plaza
	for y in range(18, 34):
		for x in range(68, 90):
			if get_tile(x, y) == T.WATER:
				continue
			if x >= 72 and x <= 86 and y >= 20 and y <= 30:
				set_tile(x, y, T.PLAZA)
			else:
				set_tile(x, y, T.PATH)

	# South pasture soft dirt patches
	for y in range(46, 58):
		for x in range(22, 48):
			if (x + y) % 7 == 0 and get_tile(x, y) == T.GRASS:
				set_tile(x, y, T.DIRT)

	# East forest floor soft dirt spots
	for y in range(42, 58):
		for x in range(78, 92):
			if (x * 3 + y) % 11 == 0 and get_tile(x, y) == T.GRASS:
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

func _is_water(t: int) -> bool:
	return t == T.WATER

func _is_soft_ground(t: int) -> bool:
	return t == T.DIRT or t == T.PATH or t == T.FARMLAND or t == T.PLAZA

func _display_tex(x: int, y: int, t: int) -> Texture2D:
	if t == T.GRASS:
		var n_water := _is_water(get_tile(x, y - 1))
		var s_water := _is_water(get_tile(x, y + 1))
		var e_water := _is_water(get_tile(x + 1, y))
		var w_water := _is_water(get_tile(x - 1, y))
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
		# soft grass↔dirt edges (clean procedural tiles, no red-line AI edges)
		var n_d := _is_soft_ground(get_tile(x, y - 1))
		var s_d := _is_soft_ground(get_tile(x, y + 1))
		var e_d := _is_soft_ground(get_tile(x + 1, y))
		var w_d := _is_soft_ground(get_tile(x - 1, y))
		if n_d and edge_tex.has("gd_n"):
			return edge_tex["gd_n"]
		if s_d and edge_tex.has("gd_s"):
			return edge_tex["gd_s"]
		if e_d and edge_tex.has("gd_e"):
			return edge_tex["gd_e"]
		if w_d and edge_tex.has("gd_w"):
			return edge_tex["gd_w"]
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
		Vector2i(8, 12), Vector2i(14, 12), Vector2i(42, 12),
		Vector2i(80, 44), Vector2i(84, 48), Vector2i(88, 50), Vector2i(82, 54),
	]
	for c in spots:
		if get_tile(c.x, c.y) != T.WATER and get_tile(c.x, c.y) != T.CLIFF:
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
	return t == T.WATER or t == T.HILL or t == T.CLIFF

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
			if t != T.WATER and t != T.HILL and t != T.CLIFF:
				continue
			# stairs stay walkable
			var body := StaticBody2D.new()
			body.position = Vector2(x * TS + TS * 0.5, y * TS + TS * 0.5)
			var cs := CollisionShape2D.new()
			var rect := RectangleShape2D.new()
			rect.size = Vector2(TS, TS)
			cs.shape = rect
			body.add_child(cs)
			parent.add_child(body)
