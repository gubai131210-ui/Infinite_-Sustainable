extends Node2D
## Dense decor: trees, flowers, animals, farmhouse door interact.

const TS := 16

func _ready() -> void:
	_trees()
	_flowers()
	_animals()
	_door_and_chest()

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
	var spots := [
		Vector2(12, 70), Vector2(20, 68), Vector2(55, 70), Vector2(60, 85),
		Vector2(8, 100), Vector2(50, 110), Vector2(65, 100),
		Vector2(100, 70), Vector2(110, 65), Vector2(115, 75),
		Vector2(125, 45), Vector2(160, 35), Vector2(175, 30),
		Vector2(120, 95), Vector2(125, 115), Vector2(180, 115),
		Vector2(70, 25), Vector2(50, 30), Vector2(35, 20),
	]
	for i in range(spots.size()):
		_spr("res://assets/processed/tree_%d.png" % (i % 3), spots[i], 6)

func _flowers() -> void:
	var spots := [
		Vector2(22, 84), Vector2(28, 86), Vector2(45, 82), Vector2(88, 42),
		Vector2(92, 56), Vector2(135, 50), Vector2(145, 70), Vector2(160, 90),
	]
	for i in range(spots.size()):
		_spr("res://assets/processed/flower_%d.png" % (i % 4), spots[i], 3)

func _animals() -> void:
	_spr("res://assets/processed/chicken.png", Vector2(30, 92), 5)
	_spr("res://assets/processed/chicken.png", Vector2(33, 94), 5)
	_spr("res://assets/processed/cow.png", Vector2(28, 105), 5)
	_spr("res://assets/processed/sheep.png", Vector2(36, 108), 5)

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
	# station toast
	var station := preload("res://scenes/interact_zone.tscn").instantiate()
	station.prompt_text = "按 E 看站台"
	station.mode = "toast"
	station.message = "列车停靠中（不可上车）"
	station.position = Vector2(150, 22) * TS
	add_child(station)
	# pier
	var pier := preload("res://scenes/interact_zone.tscn").instantiate()
	pier.prompt_text = "按 E 看码头"
	pier.mode = "toast"
	pier.message = "Lake Echo 湖面波光粼粼"
	pier.position = Vector2(155, 110) * TS
	add_child(pier)
