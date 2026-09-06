extends Node2D
## Place Wave1–6 landmark props on Entities (Y-sorted). Dense, recognizable landmarks.

const TS := 16

func _ready() -> void:
	_place()

func _spr(path: String, tile: Vector2, z: int = 6, scale_mul: float = 1.0) -> void:
	var abs_path := ProjectSettings.globalize_path(path)
	var img := Image.new()
	if img.load(abs_path) != OK:
		push_warning("missing landmark: %s" % path)
		return
	var tex := ImageTexture.create_from_image(img)
	var s := Sprite2D.new()
	s.texture = tex
	s.centered = true
	var th := float(tex.get_height()) * scale_mul
	s.offset = Vector2(0, -th * 0.5)
	s.position = tile * TS
	s.z_index = z
	s.scale = Vector2(scale_mul, scale_mul)
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
	_spr("res://assets/processed/prop_barn.png", Vector2(38, 100), 8, 1.25)
	_spr("res://assets/processed/prop_barn2.png", Vector2(50, 102), 8, 1.2)
	_spr("res://assets/processed/prop_silo.png", Vector2(34, 96), 8, 1.35)
	_spr("res://assets/processed/prop_silo.png", Vector2(54, 96), 8, 1.35)
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(40, 88), 8, 1.3)
	# Pen fence — spaced posts, not every tile (avoids “crowd” noise)
	for x in range(20, 54, 2):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 78), 4)
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 110), 4)
	for y in range(80, 110, 3):
		_spr("res://assets/processed/prop_fence.png", Vector2(20, y), 4)
		_spr("res://assets/processed/prop_fence.png", Vector2(52, y), 4)

func _river() -> void:
	_spr("res://assets/processed/prop_waterfall.png", Vector2(24, 20), 9, 1.4)
	_spr("res://assets/processed/prop_bridge.png", Vector2(29, 40), 5, 1.15)
	_spr("res://assets/processed/prop_bridge.png", Vector2(29, 62), 5, 1.15)

func _town() -> void:
	_spr("res://assets/processed/prop_statue.png", Vector2(90, 48), 7, 1.2)
	_spr("res://assets/processed/prop_stall.png", Vector2(80, 42), 6, 1.15)
	_spr("res://assets/processed/prop_stall_blue.png", Vector2(100, 42), 6, 1.15)
	_spr("res://assets/processed/prop_stall.png", Vector2(80, 56), 6, 1.15)
	_spr("res://assets/processed/prop_stall_blue.png", Vector2(100, 56), 6, 1.15)
	_spr("res://assets/processed/prop_stall.png", Vector2(90, 40), 6, 1.1)
	_spr("res://assets/processed/prop_stall_blue.png", Vector2(90, 58), 6, 1.1)
	_spr("res://assets/processed/prop_townhouse_blue.png", Vector2(72, 34), 8, 1.2)
	_spr("res://assets/processed/prop_townhouse_brown.png", Vector2(108, 34), 8, 1.2)
	_spr("res://assets/processed/prop_townhouse_brown.png", Vector2(72, 62), 8, 1.2)
	_spr("res://assets/processed/prop_townhouse_blue.png", Vector2(108, 62), 8, 1.2)
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(84, 32), 8, 1.15)
	_spr("res://assets/processed/prop_townhouse_brown.png", Vector2(98, 64), 8, 1.15)
	_spr("res://assets/processed/prop_townhouse_blue.png", Vector2(68, 48), 8, 1.15)
	_spr("res://assets/processed/prop_townhouse_brown.png", Vector2(112, 48), 8, 1.15)

func _station() -> void:
	_spr("res://assets/processed/prop_station.png", Vector2(148, 14), 8, 1.15)
	_spr("res://assets/processed/prop_canopy.png", Vector2(152, 18), 7, 1.2)
	_spr("res://assets/processed/prop_train.png", Vector2(155, 20), 7, 1.4)
	_spr("res://assets/processed/prop_tunnel.png", Vector2(182, 16), 9, 1.3)
	_spr("res://assets/processed/prop_stall.png", Vector2(138, 16), 6, 1.1)
	_spr("res://assets/processed/prop_fence.png", Vector2(130, 18), 4)
	_spr("res://assets/processed/prop_fence.png", Vector2(168, 18), 4)

func _terrace() -> void:
	_spr("res://assets/processed/prop_stall.png", Vector2(148, 42), 5, 1.1)
	for band in range(5):
		var y := 42 + band * 10
		_spr("res://assets/processed/prop_stonewall.png", Vector2(130, y), 5, 1.2)
		_spr("res://assets/processed/prop_stonewall.png", Vector2(145, y), 5, 1.2)
		_spr("res://assets/processed/prop_stonewall.png", Vector2(160, y), 5, 1.2)

func _lake() -> void:
	_spr("res://assets/processed/prop_lighthouse.png", Vector2(173, 103), 10, 1.45)
	_spr("res://assets/processed/prop_boat.png", Vector2(160, 110), 6, 1.3)
	_spr("res://assets/processed/prop_bridge.png", Vector2(162, 110), 5, 1.1)
	_spr("res://assets/processed/prop_townhouse_blue.png", Vector2(178, 92), 8, 1.1)
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(150, 98), 8, 1.1)
