extends Node2D
## Place Wave1–6 landmark props on Entities (Y-sorted). Dense, recognizable landmarks.

const TS := 16

func _ready() -> void:
	_place()

func _spr(path: String, tile: Vector2, z: int = 6) -> void:
	if not ResourceLoader.exists(path):
		push_warning("missing landmark: %s" % path)
		return
	var s := Sprite2D.new()
	s.texture = load(path)
	s.centered = true
	s.position = tile * TS + Vector2(0, -8)
	s.z_index = z
	s.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	s.y_sort_enabled = true
	add_child(s)

func _place() -> void:
	_farm()
	_river()
	_town()
	_station()
	_terrace()
	_lake()

func _farm() -> void:
	# Z1 — barns east of river, silos, farmhouse, fence pen
	_spr("res://assets/processed/prop_barn.png", Vector2(38, 100), 8)
	_spr("res://assets/processed/prop_barn2.png", Vector2(50, 102), 8)
	_spr("res://assets/processed/prop_silo.png", Vector2(34, 96), 8)
	_spr("res://assets/processed/prop_silo.png", Vector2(54, 96), 8)
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(40, 88), 8)
	# Pen fence — spaced posts, not every tile (avoids “crowd” noise)
	for x in range(20, 54, 2):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 78), 4)
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 110), 4)
	for y in range(80, 110, 3):
		_spr("res://assets/processed/prop_fence.png", Vector2(20, y), 4)
		_spr("res://assets/processed/prop_fence.png", Vector2(52, y), 4)

func _river() -> void:
	# Z2 — waterfall + bridges
	_spr("res://assets/processed/prop_waterfall.png", Vector2(24, 20), 9)
	_spr("res://assets/processed/prop_bridge.png", Vector2(29, 40), 5)
	_spr("res://assets/processed/prop_bridge.png", Vector2(29, 62), 5)

func _town() -> void:
	# Z3 — plaza statue, stalls, half-timber houses (≥6)
	_spr("res://assets/processed/prop_statue.png", Vector2(90, 48), 7)
	_spr("res://assets/processed/prop_stall.png", Vector2(80, 42), 6)
	_spr("res://assets/processed/prop_stall_blue.png", Vector2(100, 42), 6)
	_spr("res://assets/processed/prop_stall.png", Vector2(80, 56), 6)
	_spr("res://assets/processed/prop_stall_blue.png", Vector2(100, 56), 6)
	_spr("res://assets/processed/prop_stall.png", Vector2(90, 40), 6)
	_spr("res://assets/processed/prop_stall_blue.png", Vector2(90, 58), 6)
	_spr("res://assets/processed/prop_townhouse_blue.png", Vector2(72, 34), 8)
	_spr("res://assets/processed/prop_townhouse_brown.png", Vector2(108, 34), 8)
	_spr("res://assets/processed/prop_townhouse_brown.png", Vector2(72, 62), 8)
	_spr("res://assets/processed/prop_townhouse_blue.png", Vector2(108, 62), 8)
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(84, 32), 8)
	_spr("res://assets/processed/prop_townhouse_brown.png", Vector2(98, 64), 8)
	_spr("res://assets/processed/prop_townhouse_blue.png", Vector2(68, 48), 8)
	_spr("res://assets/processed/prop_townhouse_brown.png", Vector2(112, 48), 8)

func _station() -> void:
	# Z4 — train + station house + platform props
	_spr("res://assets/processed/prop_train.png", Vector2(150, 20), 7)
	_spr("res://assets/processed/prop_townhouse_brown.png", Vector2(142, 14), 8)
	_spr("res://assets/processed/prop_stall.png", Vector2(158, 16), 6)
	_spr("res://assets/processed/prop_fence.png", Vector2(138, 18), 4)
	_spr("res://assets/processed/prop_fence.png", Vector2(162, 18), 4)

func _terrace() -> void:
	# Z5 — small shed markers on terrace bands
	_spr("res://assets/processed/prop_stall.png", Vector2(148, 48), 5)
	_spr("res://assets/processed/prop_fence.png", Vector2(128, 52), 4)
	_spr("res://assets/processed/prop_fence.png", Vector2(158, 52), 4)

func _lake() -> void:
	# Z6 — lighthouse, pier boat
	_spr("res://assets/processed/prop_lighthouse.png", Vector2(173, 103), 10)
	_spr("res://assets/processed/prop_boat.png", Vector2(160, 110), 6)
	_spr("res://assets/processed/prop_bridge.png", Vector2(162, 110), 5)
