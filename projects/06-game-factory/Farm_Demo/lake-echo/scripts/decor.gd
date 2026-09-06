extends Node2D
## Dense decor: trees, flowers, animals, NPCs, farmhouse door, ambient smoke/ripples.

const TS := 16

func _ready() -> void:
	_trees()
	_bushes()
	_flowers()
	_animals()
	_npcs()
	_door_and_chest()
	_ambient()

func _spr(path: String, tile: Vector2, z: int = 5) -> Sprite2D:
	if not ResourceLoader.exists(path):
		return null
	var s := Sprite2D.new()
	s.texture = load(path)
	s.centered = true
	s.position = tile * TS
	s.z_index = z
	s.y_sort_enabled = true
	s.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	add_child(s)
	return s

func _trees() -> void:
	# Dense belts matching video: NW forest, river banks, lake shore, station fringe
	var spots: Array[Vector2] = []
	# Dense NW pine belt (video: forest above waterfall)
	for x in range(2, 55, 2):
		for y in range(8, 20, 3):
			spots.append(Vector2(x + (y % 2), y + (x % 2)))
	for x in range(55, 100, 3):
		spots.append(Vector2(x, 12 + (x % 4)))
	# Farm west of river + pasture edges
	for p in [
		Vector2(10, 70), Vector2(14, 74), Vector2(8, 88), Vector2(12, 100),
		Vector2(8, 110), Vector2(58, 70), Vector2(62, 78), Vector2(60, 90),
		Vector2(64, 100), Vector2(58, 110), Vector2(20, 66), Vector2(30, 68),
		Vector2(42, 66), Vector2(52, 68),
	]:
		spots.append(p)
	# River corridor trees
	for y in range(28, 95, 6):
		spots.append(Vector2(14 + (y % 4), y))
		spots.append(Vector2(40 + (y % 3), y + 2))
	# Town fringe
	for p in [
		Vector2(66, 28), Vector2(66, 40), Vector2(66, 55), Vector2(66, 68),
		Vector2(116, 28), Vector2(116, 40), Vector2(116, 55), Vector2(116, 68),
		Vector2(78, 26), Vector2(102, 26), Vector2(78, 70), Vector2(102, 70),
	]:
		spots.append(p)
	# Station / terrace / lake
	for p in [
		Vector2(125, 12), Vector2(135, 10), Vector2(165, 12), Vector2(175, 14),
		Vector2(180, 28), Vector2(120, 40), Vector2(168, 45), Vector2(175, 55),
		Vector2(120, 88), Vector2(125, 100), Vector2(128, 115), Vector2(180, 90),
		Vector2(185, 105), Vector2(180, 118), Vector2(140, 120), Vector2(155, 122),
	]:
		spots.append(p)
	for i in range(spots.size()):
		_spr("res://assets/processed/tree_%d.png" % (i % 3), spots[i], 6)

func _bushes() -> void:
	if not ResourceLoader.exists("res://assets/processed/bush.png"):
		return
	for p in [
		Vector2(24, 82), Vector2(44, 84), Vector2(86, 46), Vector2(94, 52),
		Vector2(132, 55), Vector2(150, 60), Vector2(168, 95), Vector2(155, 100),
	]:
		_spr("res://assets/processed/bush.png", p, 4)

func _flowers() -> void:
	var spots := [
		Vector2(22, 84), Vector2(28, 86), Vector2(32, 84), Vector2(45, 82),
		Vector2(48, 86), Vector2(88, 42), Vector2(92, 46), Vector2(96, 42),
		Vector2(86, 54), Vector2(94, 56), Vector2(135, 50), Vector2(140, 58),
		Vector2(145, 70), Vector2(150, 68), Vector2(160, 90), Vector2(165, 92),
		Vector2(170, 88), Vector2(72, 50), Vector2(108, 50),
	]
	for i in range(spots.size()):
		_spr("res://assets/processed/flower_%d.png" % (i % 4), spots[i], 3)

func _animals() -> void:
	_spr("res://assets/processed/chicken.png", Vector2(30, 92), 5)
	_spr("res://assets/processed/chicken.png", Vector2(33, 94), 5)
	_spr("res://assets/processed/chicken.png", Vector2(36, 93), 5)
	_spr("res://assets/processed/cow.png", Vector2(28, 105), 5)
	_spr("res://assets/processed/cow.png", Vector2(42, 108), 5)
	_spr("res://assets/processed/sheep.png", Vector2(36, 108), 5)
	_spr("res://assets/processed/sheep.png", Vector2(45, 104), 5)

func _npcs() -> void:
	# Sparse recognizable NPCs (not a clone army)
	var spots := [
		[Vector2(84, 46), false], [Vector2(96, 50), true],
		[Vector2(88, 54), false], [Vector2(92, 44), true],
		[Vector2(148, 18), false], [Vector2(42, 92), true],
	]
	for item in spots:
		var s := _spr("res://assets/processed/npc_ahe.png", item[0], 7)
		if s != null:
			s.flip_h = bool(item[1])

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
	# Chimney smoke puffs (farmhouse + town)
	for origin in [Vector2(40, 86), Vector2(74, 32), Vector2(108, 32), Vector2(142, 12)]:
		_spawn_smoke(origin * TS)
	# Lake ripples near pier
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
