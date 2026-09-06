extends Node
## Z1 farm plots — hoe/plant/water/harvest on farmland tiles.

const TS := 16
const T_FARM_ATLAS := Vector2i(0, 1)  # tile id 8 -> (0,1) in 8-col atlas

var plots: Dictionary = {}  # Vector2i -> dict
var _crops: Node2D
var _ground: TileMapLayer

func _ready() -> void:
	await get_tree().process_frame
	var world := get_parent()
	_ground = world.get_node("Ground")
	_crops = Node2D.new()
	_crops.name = "Crops"
	_crops.z_index = 3
	world.add_child(_crops)
	var player := get_tree().get_first_node_in_group("player")
	if player != null and player.has_method("set_farm"):
		player.set_farm(self)

func is_farmland(cell: Vector2i) -> bool:
	if _ground == null:
		return false
	return _ground.get_cell_atlas_coords(cell) == Vector2i(0, 1)  # farmland

func hoe(cell: Vector2i) -> bool:
	if not is_farmland(cell) and _ground.get_cell_atlas_coords(cell) != Vector2i(1, 0):
		# also allow dirt (1,0)
		if _ground.get_cell_atlas_coords(cell) != Vector2i(1, 0):
			return false
	if plots.has(cell) and str(plots[cell].get("crop", "")) != "":
		return false
	plots[cell] = {"crop": "", "stage": 0, "waters_done": 0}
	_ground.set_cell(cell, 0, Vector2i(0, 1))  # keep farmland look; tilled = id 8 still
	GameBus.show_toast("锄地完成")
	return true

func plant(cell: Vector2i, seed_id: String) -> bool:
	if not plots.has(cell):
		return false
	if str(plots[cell].get("crop", "")) != "":
		return false
	if not ItemDB.ITEMS.has(seed_id):
		return false
	var crop := str(ItemDB.ITEMS[seed_id].get("crop", ""))
	plots[cell]["crop"] = crop
	plots[cell]["stage"] = 0
	plots[cell]["waters_done"] = 0
	_refresh()
	return true

func water(cell: Vector2i) -> bool:
	if not plots.has(cell):
		return false
	var p: Dictionary = plots[cell]
	var crop := str(p.get("crop", ""))
	if crop == "":
		return true
	if int(p.get("stage", 0)) >= 3:
		return false
	var need := int(ItemDB.CROPS[crop]["waters"])
	p["waters_done"] = int(p.get("waters_done", 0)) + 1
	if int(p["waters_done"]) >= need:
		p["stage"] = 3
	else:
		p["stage"] = clampi(int(float(p["waters_done"]) / float(need) * 3.0), 0, 2)
	plots[cell] = p
	_refresh()
	return true

func harvest(cell: Vector2i) -> String:
	if not plots.has(cell):
		return ""
	var p: Dictionary = plots[cell]
	var crop := str(p.get("crop", ""))
	if crop == "" or int(p.get("stage", 0)) < 3:
		return ""
	var item := str(ItemDB.CROPS[crop]["item"])
	plots.erase(cell)
	_refresh()
	return item

func _refresh() -> void:
	for c in _crops.get_children():
		c.queue_free()
	for key in plots.keys():
		var p: Dictionary = plots[key]
		var crop := str(p.get("crop", ""))
		if crop == "":
			continue
		var stage := clampi(int(p.get("stage", 0)), 0, 3)
		var path := "res://assets/processed/crop_%s_%d.png" % [crop, stage]
		if not ResourceLoader.exists(path):
			continue
		var spr := Sprite2D.new()
		spr.texture = load(path)
		spr.centered = false
		spr.position = Vector2(key.x * TS, key.y * TS)
		spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		_crops.add_child(spr)
