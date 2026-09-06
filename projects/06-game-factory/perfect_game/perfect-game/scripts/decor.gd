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

func _load_tex(path: String) -> Texture2D:
	var abs_path := ProjectSettings.globalize_path(path)
	var img := Image.new()
	if img.load(abs_path) != OK:
		return null
	return ImageTexture.create_from_image(img)

func _atlas_frame(path: String, frame: int = 0, fw: int = -1, fh: int = -1) -> Texture2D:
	var tex := _load_tex(path)
	if tex == null:
		return null
	var h := tex.get_height()
	var w := tex.get_width()
	if fw <= 0:
		fw = h
	if fh <= 0:
		fh = h
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
	var tex := _load_tex(path)
	if tex == null:
		return null
	var s := Sprite2D.new()
	s.texture = tex
	s.centered = true
	var th := float(tex.get_height())
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
	# Dense NW pine belt (video forest above waterfall)
	for x in range(2, 60, 2):
		for y in range(2, 24, 2):
			spots.append(Vector2(x + (y % 2), y + (x % 2)))
	for x in range(60, 120, 2):
		for y in range(4, 18, 2):
			spots.append(Vector2(x + (y % 2), y))
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
		var pine := "res://assets/processed/tree_pine.png"
		var path := "res://assets/processed/tree_%d.png" % (i % 3)
		if p.y < 22 and _load_tex(pine) != null:
			_spr(pine, p, 6)
		else:
			_spr(path, p, 6)

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
		# Town plaza ring
		Vector2(78, 38), Vector2(102, 38), Vector2(78, 60), Vector2(102, 60),
		Vector2(88, 34), Vector2(92, 34), Vector2(88, 64), Vector2(92, 64),
		# Lake shore
		Vector2(148, 98), Vector2(154, 102), Vector2(166, 96), Vector2(176, 98),
		Vector2(182, 92), Vector2(170, 110),
	]
	for i in range(spots.size()):
		_spr("res://assets/processed/flower_%d.png" % (i % 4), spots[i], 3)

func _crops_on_fields() -> void:
	# Decorative crops only on bed edges + terraces — leave playable hoe rows clear
	var crops := [
		"res://assets/processed/crop_wheat_3.png",
		"res://assets/processed/crop_tomato_3.png",
		"res://assets/processed/crop_greens_3.png",
		"res://assets/processed/crop_radish_3.png",
		"res://assets/processed/crop_pumpkin_3.png",
	]
	var i := 0
	# Sparse showcase rows on farm beds (not every tile)
	for x in range(16, 28, 3):
		_spr(crops[i % crops.size()], Vector2(x, 80), 4)
		i += 1
	for x in range(36, 48, 3):
		_spr(crops[i % crops.size()], Vector2(x, 82), 4)
		i += 1
	for x in range(16, 28, 3):
		_spr(crops[i % crops.size()], Vector2(x, 94), 4)
		i += 1
	# Z5 terraces — denser showcase
	for band in range(5):
		var y0 := 39 + band * 10
		for x in range(128, 158, 3):
			_spr(crops[i % crops.size()], Vector2(x, y0), 4)
			i += 1

func _npcs() -> void:
	# 12 named interactive NPCs across zones (CharacterBody2D + dialogue)
	var roster := [
		{"id": "he", "name": "阿禾", "line": "米勒农庄的地，锄透了才肯长苗。", "pos": Vector2(44, 94), "spr": "npc_01.png"},
		{"id": "man", "name": "小满", "line": "镇上市集今天来了新鲜番茄苗！", "pos": Vector2(86, 48), "spr": "npc_02.png"},
		{"id": "yu", "name": "青渔", "line": "回声湖的鱼最肥，记得带钓竿。", "pos": Vector2(158, 108), "spr": "npc_03.png"},
		{"id": "lin", "name": "林婶", "line": "杂货店进了新饲料，别忘了喂鸡。", "pos": Vector2(74, 46), "spr": "npc_04.png"},
		{"id": "zhou", "name": "石匠周", "line": "梯田挡墙要常修，雨季最怕塌。", "pos": Vector2(140, 52), "spr": "npc_05.png"},
		{"id": "tie", "name": "铁轨老张", "line": "橡木火车站正点到站，别站得太近。", "pos": Vector2(148, 20), "spr": "npc_06.png"},
		{"id": "ka", "name": "咖啡豆豆", "line": "咖啡馆的热可可能暖一天。", "pos": Vector2(100, 52), "spr": "npc_07.png"},
		{"id": "ta", "name": "灯塔阿白", "line": "夜里灯塔亮着，渔船才找得到岸。", "pos": Vector2(170, 100), "spr": "npc_08.png"},
		{"id": "qiao", "name": "桥边阿桥", "line": "橡木河涨水时，记得走木桥。", "pos": Vector2(30, 42), "spr": "npc_09.png"},
		{"id": "hua", "name": "花贩小菊", "line": "广场花坛要是没花，镇子就少了颜色。", "pos": Vector2(92, 44), "spr": "npc_10.png"},
		{"id": "mu", "name": "木匠老木", "line": "谷仓里工具齐全，缺什么跟我说。", "pos": Vector2(48, 100), "spr": "npc_11.png"},
		{"id": "shan", "name": "山风", "line": "北崖瀑布旁风大，帽子戴牢。", "pos": Vector2(26, 26), "spr": "npc_12.png"},
	]
	var npc_scene := preload("res://scenes/npc.tscn")
	for info in roster:
		var n := npc_scene.instantiate()
		n.npc_id = str(info["id"])
		n.display_name = str(info["name"])
		n.line = str(info["line"])
		n.sprite_path = "res://assets/processed/%s" % str(info["spr"])
		n.position = info["pos"] * TS
		n.z_index = 7
		add_child(n)

func _animals() -> void:
	# Chickens near barns; sheep/cows inside south pen (matches reference)
	var animal_spots := [
		["chicken", Vector2(30, 100), "咯咯！想来点饲料吗？"],
		["chicken", Vector2(34, 102), "啄啄地面……"],
		["chicken", Vector2(38, 100), "母鸡今天心情不错。"],
		["cow", Vector2(28, 116), "哞——牧场草很甜。"],
		["cow", Vector2(40, 118), "慢悠悠地反刍着。"],
		["sheep", Vector2(32, 114), "咩～羊毛蓬松。"],
		["sheep", Vector2(38, 116), "咩咩，别拉我的毛。"],
	]
	for item in animal_spots:
		_spr_atlas("res://assets/processed/%s.png" % item[0], item[1], 5, 0, false)
		var z := preload("res://scenes/interact_zone.tscn").instantiate()
		z.prompt_text = "按 E 摸摸"
		z.mode = "dialogue"
		z.speaker = item[0]
		z.message = item[2]
		z.position = item[1] * TS
		add_child(z)

func _door_and_chest() -> void:
	_spr("res://assets/processed/chest.png", Vector2(36, 90), 4)
	var doors := [
		{"id": "farmhouse", "prompt": "按 E 进入农舍", "pos": Vector2(40, 88)},
		{"id": "barn", "prompt": "按 E 进入谷仓", "pos": Vector2(28, 102)},
		{"id": "shop", "prompt": "按 E 进入杂货店", "pos": Vector2(72, 32)},
		{"id": "cafe", "prompt": "按 E 进入咖啡馆", "pos": Vector2(108, 32)},
		{"id": "station", "prompt": "按 E 进入火车站厅", "pos": Vector2(150, 14)},
		{"id": "lighthouse", "prompt": "按 E 进入灯塔", "pos": Vector2(174, 100)},
	]
	for d in doors:
		var door := preload("res://scenes/interact_zone.tscn").instantiate()
		door.prompt_text = str(d["prompt"])
		door.mode = "house"
		door.interior_id = str(d["id"])
		door.position = d["pos"] * TS + Vector2(0, 12)
		add_child(door)
	var chest := preload("res://scenes/interact_zone.tscn").instantiate()
	chest.prompt_text = "按 E 打开箱子"
	chest.mode = "chest"
	chest.position = Vector2(36, 90) * TS
	add_child(chest)
	# Chinese wood placards (layout labels)
	var signs := [
		{"t": "米勒农庄", "pos": Vector2(42, 76)},
		{"t": "橡木河", "pos": Vector2(34, 48)},
		{"t": "橡木火车站", "pos": Vector2(150, 10)},
		{"t": "回声湖", "pos": Vector2(162, 96)},
	]
	for s in signs:
		_spr("res://assets/processed/prop_signboard.png", s["pos"], 8)
		var lab := Label.new()
		lab.text = str(s["t"])
		lab.position = s["pos"] * TS + Vector2(-28, -36)
		lab.z_index = 25
		lab.add_theme_font_size_override("font_size", 12)
		lab.add_theme_color_override("font_color", Color(0.15, 0.1, 0.05))
		lab.add_theme_color_override("font_outline_color", Color(1, 1, 1))
		lab.add_theme_constant_override("outline_size", 3)
		add_child(lab)
	var pier := preload("res://scenes/interact_zone.tscn").instantiate()
	pier.prompt_text = "按 E 看码头"
	pier.mode = "toast"
	pier.message = "回声湖波光粼粼，远处灯塔守着夜航。"
	pier.position = Vector2(155, 110) * TS
	add_child(pier)
	var fall := preload("res://scenes/interact_zone.tscn").instantiate()
	fall.prompt_text = "按 E 看瀑布"
	fall.mode = "toast"
	fall.message = "橡木河源头瀑布轰鸣，水雾扑面。"
	fall.position = Vector2(24, 22) * TS
	add_child(fall)
	var stall := preload("res://scenes/interact_zone.tscn").instantiate()
	stall.prompt_text = "按 E 看看摊位"
	stall.mode = "dialogue"
	stall.speaker = "摊主"
	stall.message = "今日番茄与萝卜新鲜，先去农庄种点种子吧！"
	stall.position = Vector2(80, 44) * TS
	add_child(stall)
	var fish := preload("res://scenes/interact_zone.tscn").instantiate()
	fish.prompt_text = "按 E 钓鱼"
	fish.mode = "fish"
	fish.position = Vector2(160, 112) * TS
	add_child(fish)

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
