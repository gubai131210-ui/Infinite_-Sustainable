extends Node2D
## Builds decor, NPCs, animals, collision, interactables on top of FarmField.

const TS := 16

@onready var field: Node2D = $FarmField
@onready var ysort: Node2D = $YSort
@onready var colliders: Node2D = $Colliders

func _ready() -> void:
	var player := get_parent().get_node("Player")
	if field.has_method("set_player"):
		field.set_player(player)
	if field.has_method("build_collisions"):
		field.build_collisions(colliders)
	_spawn_decor()
	_spawn_npcs()
	_spawn_animals()
	_spawn_props()

func _spr(path: String, pos: Vector2, z: int = 1) -> Sprite2D:
	var s := Sprite2D.new()
	s.texture = load(path)
	s.position = pos
	s.centered = true
	s.z_index = z
	s.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	ysort.add_child(s)
	return s

func _spawn_decor() -> void:
	var trees := [
		Vector2(8, 12), Vector2(14, 10), Vector2(40, 10), Vector2(50, 12),
		Vector2(70, 14), Vector2(10, 36), Vector2(48, 50), Vector2(30, 52),
		# east forest
		Vector2(80, 44), Vector2(84, 46), Vector2(88, 48), Vector2(82, 52), Vector2(90, 50),
	]
	for i in range(trees.size()):
		var p: Vector2 = trees[i] * TS
		_spr("res://assets/processed/tree_%d.png" % (i % 3), p + Vector2(24, 32), 5)

	for i in range(24):
		var p := Vector2(6 + (i * 4) % 50, 16 + (i * 3) % 30) * TS
		_spr("res://assets/processed/flower_%d.png" % (i % 4), p + Vector2(8, 8), 3)

	for i in range(8):
		var p := Vector2(24 + i * 3, 50) * TS
		_spr("res://assets/processed/bush.png", p + Vector2(16, 12), 4)

func _spawn_npcs() -> void:
	var defs := [
		{"id": "ahe", "name": "阿禾", "line": "地要勤锄，苗才肯长。浇水别偷懒。", "tex": "res://assets/processed/npc_ahe.png", "pos": Vector2(10, 22)},
		{"id": "xiaoman", "name": "小满", "line": "村口风软，来坐坐呗。", "tex": "res://assets/processed/npc_xiaoman.png", "pos": Vector2(78, 24)},
		{"id": "qingyu", "name": "青渔", "line": "河弯深处有鱼，记得带钓竿。", "tex": "res://assets/processed/npc_qingyu.png", "pos": Vector2(32, 30)},
		{"id": "linshen", "name": "林婶", "line": "花开满坡，心情也跟着亮。", "tex": "res://assets/processed/npc_linshen.png", "pos": Vector2(82, 28)},
		{"id": "zhou", "name": "石匠周", "line": "北山石头硬，脚步稳着点。东边林子也能砍柴。", "tex": "res://assets/processed/npc_zhou.png", "pos": Vector2(48, 12)},
	]
	var scene := preload("res://scenes/npc.tscn")
	for d in defs:
		var n: Node = scene.instantiate()
		n.display_name = str(d["name"])
		n.line = str(d["line"])
		n.sprite_path = str(d["tex"])
		n.npc_id = str(d["id"])
		n.position = d["pos"] * TS
		ysort.add_child(n)

func _spawn_animals() -> void:
	var scene := preload("res://scenes/animal.tscn")
	var defs := [
		{"kind": "chicken", "name": "鸡", "tex": "res://assets/processed/chicken.png", "pos": Vector2(34, 22)},
		{"kind": "chicken", "name": "鸡", "tex": "res://assets/processed/chicken.png", "pos": Vector2(36, 23)},
		{"kind": "chicken", "name": "鸡", "tex": "res://assets/processed/chicken.png", "pos": Vector2(38, 24)},
		# south pasture
		{"kind": "cow", "name": "牛", "tex": "res://assets/processed/cow.png", "pos": Vector2(30, 50)},
		{"kind": "sheep", "name": "羊", "tex": "res://assets/processed/sheep.png", "pos": Vector2(34, 52)},
		{"kind": "sheep", "name": "羊", "tex": "res://assets/processed/sheep.png", "pos": Vector2(40, 50)},
		{"kind": "cow", "name": "牛", "tex": "res://assets/processed/cow.png", "pos": Vector2(44, 54)},
	]
	for d in defs:
		var a: Node = scene.instantiate()
		a.animal_kind = str(d["kind"])
		a.display_name = str(d["name"])
		a.sprite_path = str(d["tex"])
		a.position = d["pos"] * TS
		ysort.add_child(a)

func _spawn_props() -> void:
	# Enterable farmhouse
	_spr("res://assets/processed/house.png", Vector2(36, 20) * TS + Vector2(32, 32), 6)
	# Village deco houses
	_spr("res://assets/processed/house.png", Vector2(74, 22) * TS + Vector2(32, 32), 6)
	_spr("res://assets/processed/house.png", Vector2(82, 26) * TS + Vector2(32, 32), 6)
	_spr("res://assets/processed/chest.png", Vector2(34, 24) * TS + Vector2(12, 10), 4)

	var door := preload("res://scenes/interact_zone.tscn").instantiate()
	door.name = "FarmHouseDoor"
	door.prompt_text = "按 E 进入农舍"
	door.mode = "house"
	door.position = Vector2(36, 24) * TS + Vector2(16, 8)
	ysort.add_child(door)

	var chest := preload("res://scenes/interact_zone.tscn").instantiate()
	chest.prompt_text = "按 E 打开箱子"
	chest.mode = "chest"
	chest.position = Vector2(34, 24) * TS + Vector2(12, 10)
	ysort.add_child(chest)

	for y in [22, 34, 48]:
		var fish := preload("res://scenes/interact_zone.tscn").instantiate()
		fish.prompt_text = "按 E 钓鱼"
		fish.mode = "fish"
		fish.position = Vector2(28, y) * TS + Vector2(8, 8)
		ysort.add_child(fish)
