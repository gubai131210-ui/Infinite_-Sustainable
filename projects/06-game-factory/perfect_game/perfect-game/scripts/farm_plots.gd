extends Node
## Z1 farm plots — hoe/plant/water/harvest + wet soil + day growth + crop sway.

const TS := 16

var plots: Dictionary = {}  # Vector2i -> dict
var _crops: Node2D
var _ground: TileMapLayer
var _wet_overlay: Node2D

func _ready() -> void:
	await get_tree().process_frame
	var world := get_parent()
	_ground = world.get_node("Ground")
	_crops = Node2D.new()
	_crops.name = "Crops"
	_crops.z_index = 3
	world.add_child(_crops)
	_wet_overlay = Node2D.new()
	_wet_overlay.name = "WetSoil"
	_wet_overlay.z_index = 2
	world.add_child(_wet_overlay)
	plots = GameBus.farm_plots_data.duplicate(true)
	_refresh()
	var player := get_tree().get_first_node_in_group("player")
	if player != null and player.has_method("set_farm"):
		player.set_farm(self)
	if not TimeClock.day_changed.is_connected(_on_new_day):
		TimeClock.day_changed.connect(_on_new_day)

func _persist() -> void:
	GameBus.farm_plots_data = plots.duplicate(true)

func is_farmland(cell: Vector2i) -> bool:
	if _ground == null:
		return false
	var atlas := _ground.get_cell_atlas_coords(cell)
	return atlas == Vector2i(0, 1) or atlas == Vector2i(1, 0)

func hoe(cell: Vector2i) -> bool:
	if not is_farmland(cell):
		return false
	if plots.has(cell) and str(plots[cell].get("crop", "")) != "":
		return false
	plots[cell] = {"crop": "", "stage": 0, "waters_done": 0, "wet": false}
	_ground.set_cell(cell, 0, Vector2i(0, 1))
	_persist()
	_refresh()
	QuestLog.mark("explore_farm")
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
	_persist()
	_refresh()
	QuestLog.mark("explore_farm")
	return true

func water(cell: Vector2i) -> bool:
	if not plots.has(cell):
		return false
	var p: Dictionary = plots[cell]
	p["wet"] = true
	var crop := str(p.get("crop", ""))
	if crop == "":
		plots[cell] = p
		_persist()
		_refresh()
		return true
	if int(p.get("stage", 0)) >= 3:
		plots[cell] = p
		_persist()
		_refresh()
		return false
	var need := int(ItemDB.CROPS[crop]["waters"])
	p["waters_done"] = int(p.get("waters_done", 0)) + 1
	var prev_stage := int(p.get("stage", 0))
	if int(p["waters_done"]) >= need:
		p["stage"] = 3
	else:
		p["stage"] = clampi(int(float(p["waters_done"]) / float(need) * 3.0), 0, 2)
	plots[cell] = p
	_persist()
	_refresh()
	if int(p["stage"]) > prev_stage:
		_pop_crop_at(cell)
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
	_persist()
	_refresh()
	QuestLog.mark("harvest_one")
	return item

func _on_new_day(_day: int) -> void:
	## Overnight: wet planted crops advance one stage (Stardew-like).
	for key in plots.keys():
		var p: Dictionary = plots[key]
		var crop := str(p.get("crop", ""))
		if crop == "":
			p["wet"] = false
			plots[key] = p
			continue
		var stage := int(p.get("stage", 0))
		if bool(p.get("wet", false)) and stage < 3:
			p["stage"] = mini(stage + 1, 3)
			p["waters_done"] = int(p.get("waters_done", 0)) + 1
		p["wet"] = false
		plots[key] = p
	_persist()
	_refresh()
	GameBus.show_toast("新的一天，作物又长高了些")

func _pop_crop_at(cell: Vector2i) -> void:
	for c in _crops.get_children():
		if c is Node2D and c.has_meta("cell") and c.get_meta("cell") == cell:
			var tw := create_tween()
			tw.tween_property(c, "scale", Vector2(1.25, 1.25), 0.12)
			tw.tween_property(c, "scale", Vector2.ONE, 0.12)
			return

func _refresh() -> void:
	for c in _crops.get_children():
		c.queue_free()
	for c in _wet_overlay.get_children():
		c.queue_free()
	for key in plots.keys():
		var p: Dictionary = plots[key]
		if bool(p.get("wet", false)):
			_add_wet_tile(key)
		var crop := str(p.get("crop", ""))
		if crop == "":
			continue
		var stage := clampi(int(p.get("stage", 0)), 0, 3)
		var path := "res://assets/processed/crop_%s_%d.png" % [crop, stage]
		var abs_path := ProjectSettings.globalize_path(path)
		var img := Image.new()
		if img.load(abs_path) != OK:
			continue
		var tex := ImageTexture.create_from_image(img)
		var root := Node2D.new()
		root.position = Vector2(key.x * TS + TS * 0.5, key.y * TS + TS * 0.5)
		root.set_meta("cell", key)
		root.z_index = 3
		var spr := Sprite2D.new()
		spr.texture = tex
		spr.centered = true
		spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		root.add_child(spr)
		_crops.add_child(root)
		_start_sway(root, stage)

func _add_wet_tile(cell: Vector2i) -> void:
	var img := Image.create(TS, TS, false, Image.FORMAT_RGBA8)
	img.fill(Color(0.22, 0.42, 0.72, 0.38))
	var spr := Sprite2D.new()
	spr.texture = ImageTexture.create_from_image(img)
	spr.centered = false
	spr.position = Vector2(cell.x * TS, cell.y * TS)
	spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	_wet_overlay.add_child(spr)

func _start_sway(root: Node2D, stage: int) -> void:
	if stage <= 0:
		return
	var tw := create_tween().set_loops()
	var amp := 2.0 + float(stage) * 0.8
	var dur := randf_range(0.9, 1.4)
	tw.tween_property(root, "rotation_degrees", amp, dur).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tw.tween_property(root, "rotation_degrees", -amp, dur).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
