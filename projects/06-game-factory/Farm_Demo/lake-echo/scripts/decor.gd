extends Node2D
## Dense decor: trees, flowers, animals, NPCs, farmhouse door, ambient smoke/ripples.
## Animal/NPC sheets are horizontal atlases — always crop one frame.

const TS := 16

func _ready() -> void:
	_trees()
	_bushes()
	_flowers()
	_crops_on_fields()
	_props_fill()
	_animals()
	_npcs()
	_door_and_chest()
	_ambient()

func _atlas_frame(path: String, frame: int = 0, fw: int = -1, fh: int = -1) -> Texture2D:
	if not ResourceLoader.exists(path):
		return null
	var tex := load(path) as Texture2D
	if tex == null:
		return null
	var h := tex.get_height()
	var w := tex.get_width()
	if fw <= 0:
		fw = h  # square-ish frames for npc/player-like sheets
	if fh <= 0:
		fh = h
	# animal sheets: frame width = height (chicken 20, sheep 28, cow 36)
	if w > h * 2:
		fw = h
		fh = h
	var cols := maxi(int(w / float(fw)), 1)
	frame = clampi(frame, 0, cols - 1)
	var at := AtlasTexture.new()
	at.atlas = tex
	at.region = Rect2(frame * fw, 0, fw, fh)
	return at

func _spr(path: String, tile: Vector2, z: int = 5) -> Sprite2D:
	if not ResourceLoader.exists(path):
		return null
	var s := Sprite2D.new()
	s.texture = load(path)
	s.centered = true
	var th := float(s.texture.get_height())
	s.offset = Vector2(0, -th * 0.5)
	s.position = tile * TS
	s.z_index = z
	s.y_sort_enabled = true
	s.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	add_child(s)
	return s

func _spr_atlas(path: String, tile: Vector2, z: int = 5, frame: int = 0, flip: bool = false) -> Sprite2D:
	var tex := _atlas_frame(path, frame)
	if tex == null:
		return null
	var s := Sprite2D.new()
	s.texture = tex
	s.centered = true
	var th := float(tex.get_height())
	s.offset = Vector2(0, -th * 0.5)
	s.position = tile * TS
	s.z_index = z
	s.flip_h = flip
	s.y_sort_enabled = true
	s.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	add_child(s)
	return s

func _trees() -> void:
	var spots: Array[Vector2] = []
	# Dense NW pine belt above waterfall
	for x in range(2, 55, 2):
		for y in range(6, 20, 2):
			spots.append(Vector2(x + (y % 2), y + (x % 2)))
	for x in range(55, 110, 3):
		spots.append(Vector2(x, 10 + (x % 4)))
	# Farm edges + river corridor
	for p in [
		Vector2(10, 70), Vector2(14, 74), Vector2(8, 88), Vector2(12, 100),
		Vector2(8, 110), Vector2(58, 70), Vector2(62, 78), Vector2(60, 90),
		Vector2(64, 100), Vector2(58, 110), Vector2(20, 66), Vector2(30, 68),
		Vector2(42, 66), Vector2(52, 68), Vector2(16, 62), Vector2(56, 62),
	]:
		spots.append(p)
	for y in range(26, 95, 4):
		spots.append(Vector2(12 + (y % 4), y))
		spots.append(Vector2(42 + (y % 3), y + 1))
	# Town fringe dense
	for p in [
		Vector2(66, 28), Vector2(66, 34), Vector2(66, 40), Vector2(66, 48), Vector2(66, 55), Vector2(66, 68),
		Vector2(116, 28), Vector2(116, 34), Vector2(116, 40), Vector2(116, 48), Vector2(116, 55), Vector2(116, 68),
		Vector2(78, 26), Vector2(102, 26), Vector2(78, 70), Vector2(102, 70),
		Vector2(70, 30), Vector2(112, 30), Vector2(70, 66), Vector2(112, 66),
	]:
		spots.append(p)
	# Station / terrace / lake rings
	for p in [
		Vector2(125, 12), Vector2(135, 10), Vector2(165, 12), Vector2(175, 14),
		Vector2(180, 28), Vector2(120, 40), Vector2(168, 45), Vector2(175, 55),
		Vector2(120, 88), Vector2(125, 100), Vector2(128, 115), Vector2(180, 90),
		Vector2(185, 105), Vector2(180, 118), Vector2(140, 120), Vector2(155, 122),
		Vector2(130, 85), Vector2(175, 85), Vector2(185, 95), Vector2(122, 105),
	]:
		spots.append(p)
	for i in range(spots.size()):
		var p: Vector2 = spots[i]
		if p.y < 22 and ResourceLoader.exists("res://assets/processed/tree_pine.png"):
			_spr("res://assets/processed/tree_pine.png", p, 6)
		else:
			_spr("res://assets/processed/tree_%d.png" % (i % 3), p, 6)

func _props_fill() -> void:
	for p in [
		Vector2(78, 44), Vector2(102, 44), Vector2(86, 58), Vector2(94, 40),
		Vector2(146, 18), Vector2(154, 24), Vector2(38, 94), Vector2(46, 96),
		Vector2(160, 100), Vector2(172, 96),
	]:
		_spr("res://assets/processed/prop_crate.png", p, 4)
	for p in [
		Vector2(82, 52), Vector2(98, 52), Vector2(150, 16), Vector2(44, 100),
		Vector2(164, 108),
	]:
		_spr("res://assets/processed/prop_barrel.png", p, 4)
	for p in [
		Vector2(76, 38), Vector2(104, 38), Vector2(76, 60), Vector2(104, 60),
		Vector2(90, 36), Vector2(148, 14), Vector2(168, 100),
	]:
		_spr("res://assets/processed/prop_lamp.png", p, 5)

func _bushes() -> void:
	if not ResourceLoader.exists("res://assets/processed/bush.png"):
		return
	for p in [
		Vector2(24, 82), Vector2(44, 84), Vector2(86, 46), Vector2(94, 52),
		Vector2(132, 55), Vector2(150, 60), Vector2(168, 95), Vector2(155, 100),
		Vector2(80, 48), Vector2(100, 48), Vector2(140, 48), Vector2(148, 72),
	]:
		_spr("res://assets/processed/bush.png", p, 4)

func _flowers() -> void:
	var spots := [
		Vector2(22, 84), Vector2(28, 86), Vector2(32, 84), Vector2(45, 82),
		Vector2(48, 86), Vector2(88, 42), Vector2(92, 46), Vector2(96, 42),
		Vector2(86, 54), Vector2(94, 56), Vector2(135, 50), Vector2(140, 58),
		Vector2(145, 70), Vector2(150, 68), Vector2(160, 90), Vector2(165, 92),
		Vector2(170, 88), Vector2(72, 50), Vector2(108, 50), Vector2(36, 80),
	]
	for i in range(spots.size()):
		_spr("res://assets/processed/flower_%d.png" % (i % 4), spots[i], 3)

func _crops_on_fields() -> void:
	# Visible crop rows on Z1 farm + Z5 terraces (mature stage sprites)
	var crops := [
		"res://assets/processed/crop_wheat_3.png",
		"res://assets/processed/crop_tomato_3.png",
		"res://assets/processed/crop_greens_3.png",
		"res://assets/processed/crop_radish_3.png",
		"res://assets/processed/crop_pumpkin_3.png",
	]
	var i := 0
	for row in range(8):
		for x in range(18, 52, 2):
			var y := 81 + row * 3
			_spr(crops[i % crops.size()], Vector2(x, y), 4)
			i += 1
	for band in range(5):
		var y0 := 42 + band * 8
		for x in range(128, 158, 2):
			_spr(crops[i % crops.size()], Vector2(x, y0 + 1), 4)
			i += 1

func _animals() -> void:
	_spr_atlas("res://assets/processed/chicken.png", Vector2(30, 92), 5, 0, false)
	_spr_atlas("res://assets/processed/chicken.png", Vector2(33, 94), 5, 2, true)
	_spr_atlas("res://assets/processed/chicken.png", Vector2(36, 93), 5, 4, false)
	_spr_atlas("res://assets/processed/cow.png", Vector2(28, 105), 5, 0, false)
	_spr_atlas("res://assets/processed/cow.png", Vector2(42, 108), 5, 1, true)
	_spr_atlas("res://assets/processed/sheep.png", Vector2(36, 108), 5, 0, false)
	_spr_atlas("res://assets/processed/sheep.png", Vector2(45, 104), 5, 3, true)

func _npcs() -> void:
	# Keep NPCs on plaza/path clear of tree canopies
	var spots := [
		[Vector2(86, 48), false, 0], [Vector2(94, 50), true, 1],
		[Vector2(88, 52), false, 2], [Vector2(92, 46), true, 3],
		[Vector2(148, 18), false, 0], [Vector2(44, 94), true, 1],
		[Vector2(100, 50), false, 4], [Vector2(154, 22), true, 2],
	]
	for item in spots:
		_spr_atlas("res://assets/processed/npc_ahe.png", item[0], 7, int(item[2]), bool(item[1]))

func _door_and_chest() -> void:
	_spr("res://assets/processed/chest.png", Vector2(36, 90), 4)
	var door := preload("res://scenes/interact_zone.tscn").instantiate()
	door.prompt_text = "按 E 进入农舍"
	door.mode = "house"
	door.position = Vector2(40, 90) * TS + Vector2(0, 12)
	add_child(door)
	var chest := preload("res://scenes/interact_zone.tscn").instantiate()
	chest.prompt_text = "按 E 打开箱子"
	chest.mode = "chest"
	chest.position = Vector2(36, 90) * TS
	add_child(chest)
	var station := preload("res://scenes/interact_zone.tscn").instantiate()
	station.prompt_text = "按 E 看站台"
	station.mode = "toast"
	station.message = "列车停靠中（不可上车）"
	station.position = Vector2(150, 22) * TS
	add_child(station)
	var pier := preload("res://scenes/interact_zone.tscn").instantiate()
	pier.prompt_text = "按 E 看码头"
	pier.mode = "toast"
	pier.message = "Lake Echo 湖面波光粼粼"
	pier.position = Vector2(155, 110) * TS
	add_child(pier)
	var fall := preload("res://scenes/interact_zone.tscn").instantiate()
	fall.prompt_text = "按 E 看瀑布"
	fall.mode = "toast"
	fall.message = "Castlenock 瀑布轰鸣"
	fall.position = Vector2(24, 22) * TS
	add_child(fall)

func _ambient() -> void:
	for origin in [Vector2(40, 86), Vector2(74, 32), Vector2(108, 32), Vector2(142, 12)]:
		_spawn_smoke(origin * TS)
	_spawn_ripples(Vector2(155, 108) * TS)

func _spawn_smoke(at: Vector2) -> void:
	var p := CPUParticles2D.new()
	p.position = at + Vector2(8, -20)
	p.amount = 12
	p.lifetime = 2.2
	p.emission_shape = CPUParticles2D.EMISSION_SHAPE_SPHERE
	p.emission_sphere_radius = 3.0
	p.direction = Vector2(0, -1)
	p.spread = 18.0
	p.gravity = Vector2(0, -8)
	p.initial_velocity_min = 8.0
	p.initial_velocity_max = 18.0
	p.scale_amount_min = 0.4
	p.scale_amount_max = 1.2
	p.color = Color(0.85, 0.85, 0.88, 0.55)
	p.z_index = 12
	add_child(p)

func _spawn_ripples(at: Vector2) -> void:
	var p := CPUParticles2D.new()
	p.position = at
	p.amount = 8
	p.lifetime = 2.5
	p.emission_shape = CPUParticles2D.EMISSION_SHAPE_SPHERE
	p.emission_sphere_radius = 12.0
	p.direction = Vector2(0, 0)
	p.spread = 180.0
	p.gravity = Vector2.ZERO
	p.initial_velocity_min = 2.0
	p.initial_velocity_max = 6.0
	p.scale_amount_min = 0.3
	p.scale_amount_max = 1.0
	p.color = Color(0.7, 0.85, 1.0, 0.35)
	p.z_index = 2
	add_child(p)
