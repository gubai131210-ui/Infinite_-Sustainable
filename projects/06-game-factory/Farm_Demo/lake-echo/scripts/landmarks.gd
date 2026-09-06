extends Node2D
## Place Wave1–6 landmark props on Entities (Y-sorted).

const TS := 16

func _ready() -> void:
	_place()

func _spr(path: String, tile: Vector2, z: int = 6) -> void:
	var s := Sprite2D.new()
	s.texture = load(path)
	s.centered = true
	s.position = tile * TS + Vector2(0, -8)
	s.z_index = z
	s.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	s.y_sort_enabled = true
	add_child(s)

func _place() -> void:
	# Z1 Farm — keep barns east of river (~x>=34)
	_spr("res://assets/processed/prop_barn.png", Vector2(38, 100), 8)
	_spr("res://assets/processed/prop_barn.png", Vector2(48, 102), 8)
	_spr("res://assets/processed/prop_silo.png", Vector2(34, 96), 8)
	_spr("res://assets/processed/prop_silo.png", Vector2(54, 96), 8)
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(40, 88), 8)
	for x in range(20, 52, 2):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 78), 4)
	# Z3 Town
	_spr("res://assets/processed/prop_statue.png", Vector2(90, 48), 7)
	_spr("res://assets/processed/prop_stall.png", Vector2(82, 44), 6)
	_spr("res://assets/processed/prop_stall.png", Vector2(98, 44), 6)
	_spr("res://assets/processed/prop_stall.png", Vector2(82, 54), 6)
	_spr("res://assets/processed/prop_stall.png", Vector2(98, 54), 6)
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(74, 38), 8)
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(104, 38), 8)
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(74, 60), 8)
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(104, 60), 8)
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(86, 36), 8)
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(96, 62), 8)
	# Z4 Station
	_spr("res://assets/processed/prop_train.png", Vector2(150, 20), 7)
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(145, 16), 8)
	# Z6 Lake — lighthouse on shore cliff pad (not in water)
	_spr("res://assets/processed/prop_lighthouse.png", Vector2(173, 103), 10)
	# Bridges visual
	_spr("res://assets/processed/prop_bridge.png", Vector2(29, 40), 5)
	_spr("res://assets/processed/prop_bridge.png", Vector2(29, 62), 5)
