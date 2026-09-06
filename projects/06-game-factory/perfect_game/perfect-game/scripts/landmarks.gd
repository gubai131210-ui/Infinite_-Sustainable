extends Node2D
## Landmark props denser / better scaled toward oakhaven_overview reference.

const TS := 16

func _ready() -> void:
	_place()

func _spr(path: String, tile: Vector2, z: int = 6, scale_mul: float = 1.0, coll: Vector2 = Vector2.ZERO) -> void:
	var abs_path := ProjectSettings.globalize_path(path)
	var img := Image.new()
	if img.load(abs_path) != OK:
		push_warning("missing landmark: %s" % path)
		return
	var tex := ImageTexture.create_from_image(img)
	var root: Node2D
	if coll != Vector2.ZERO:
		var body := StaticBody2D.new()
		var cs := CollisionShape2D.new()
		var shape := RectangleShape2D.new()
		shape.size = coll
		cs.shape = shape
		cs.position = Vector2(0, -coll.y * 0.25)
		body.add_child(cs)
		root = body
	else:
		root = Node2D.new()
	var s := Sprite2D.new()
	s.texture = tex
	s.centered = true
	var th := float(tex.get_height()) * scale_mul
	s.offset = Vector2(0, -th * 0.5)
	s.scale = Vector2(scale_mul, scale_mul)
	s.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	s.y_sort_enabled = true
	root.add_child(s)
	root.position = tile * TS
	root.z_index = z
	root.y_sort_enabled = true
	add_child(root)

func _place() -> void:
	_farm()
	_river()
	_ruins()
	_town()
	_station()
	_terrace()
	_lake()

func _farm() -> void:
	# Scales closer to reference (avoid giant barns)
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(40, 88), 8, 1.05, Vector2(48, 28))
	_spr("res://assets/processed/prop_barn.png", Vector2(28, 102), 8, 1.05, Vector2(70, 36))
	_spr("res://assets/processed/prop_barn2.png", Vector2(48, 104), 8, 1.0, Vector2(64, 34))
	_spr("res://assets/processed/prop_silo.png", Vector2(36, 98), 8, 1.1, Vector2(22, 48))
	_spr("res://assets/processed/prop_silo.png", Vector2(52, 98), 8, 1.1, Vector2(22, 48))
	# Animal pen (south of barns) — matches reference fenced sheep yard
	for x in range(24, 46, 2):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 112), 4, 1.0, Vector2(14, 10))
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 122), 4, 1.0, Vector2(14, 10))
	for y in range(112, 122, 2):
		_spr("res://assets/processed/prop_fence.png", Vector2(24, y), 4, 1.0, Vector2(10, 14))
		_spr("res://assets/processed/prop_fence.png", Vector2(44, y), 4, 1.0, Vector2(10, 14))
	# Outer farm rails
	for x in range(14, 60, 3):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 74), 4, 1.0, Vector2(14, 10))

func _river() -> void:
	_spr("res://assets/processed/prop_waterfall.png", Vector2(24, 20), 9, 1.35, Vector2(40, 36))
	_spr("res://assets/processed/prop_bridge.png", Vector2(29, 40), 5, 1.2)
	_spr("res://assets/processed/prop_bridge.png", Vector2(29, 62), 5, 1.2)
	_spr("res://assets/processed/prop_bridge.png", Vector2(28, 78), 5, 1.1)

func _ruins() -> void:
	# Forest ruins between waterfall and station (reference top-center)
	_spr("res://assets/processed/prop_ruins.png", Vector2(70, 18), 7, 1.15, Vector2(48, 24))
	_spr("res://assets/processed/prop_ruins.png", Vector2(88, 16), 7, 0.95, Vector2(40, 20))
	_spr("res://assets/processed/prop_stonewall.png", Vector2(78, 22), 6, 1.2)

func _town() -> void:
	_spr("res://assets/processed/prop_statue.png", Vector2(90, 48), 7, 1.15, Vector2(16, 20))
	# Market stalls — 4 awnings like reference
	_spr("res://assets/processed/prop_stall.png", Vector2(82, 42), 6, 1.1, Vector2(28, 18))
	_spr("res://assets/processed/prop_stall_blue.png", Vector2(98, 42), 6, 1.1, Vector2(28, 18))
	_spr("res://assets/processed/prop_stall.png", Vector2(82, 54), 6, 1.1, Vector2(28, 18))
	_spr("res://assets/processed/prop_stall_blue.png", Vector2(98, 54), 6, 1.1, Vector2(28, 18))
	# Dense ring of houses around plaza
	var houses := [
		[Vector2(72, 32), "blue"], [Vector2(84, 30), "brown"], [Vector2(96, 30), "blue"],
		[Vector2(108, 32), "brown"], [Vector2(68, 44), "brown"], [Vector2(112, 44), "blue"],
		[Vector2(70, 58), "blue"], [Vector2(110, 58), "brown"], [Vector2(82, 64), "brown"],
		[Vector2(98, 64), "blue"], [Vector2(76, 36), "brown"], [Vector2(104, 36), "blue"],
	]
	for h in houses:
		var path := "res://assets/processed/prop_townhouse_blue.png" if h[1] == "blue" else "res://assets/processed/prop_townhouse_brown.png"
		_spr(path, h[0], 8, 1.05, Vector2(36, 28))

func _station() -> void:
	_spr("res://assets/processed/prop_station.png", Vector2(150, 14), 8, 1.2, Vector2(90, 36))
	_spr("res://assets/processed/prop_canopy.png", Vector2(154, 18), 7, 1.25)
	_spr("res://assets/processed/prop_train.png", Vector2(158, 20), 7, 1.35, Vector2(80, 24))
	_spr("res://assets/processed/prop_tunnel.png", Vector2(182, 16), 9, 1.25, Vector2(36, 32))
	_spr("res://assets/processed/prop_crate.png", Vector2(140, 18), 5)
	_spr("res://assets/processed/prop_barrel.png", Vector2(142, 20), 5)
	for x in range(130, 170, 4):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 24), 4)

func _terrace() -> void:
	for band in range(5):
		var y := 42 + band * 10
		for x in range(126, 164, 6):
			_spr("res://assets/processed/prop_stonewall.png", Vector2(x, y + 3), 5, 1.15)
	_spr("res://assets/processed/prop_townhouse_brown.png", Vector2(168, 48), 8, 1.0, Vector2(36, 28))
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(166, 62), 8, 0.95, Vector2(40, 26))

func _lake() -> void:
	_spr("res://assets/processed/prop_lighthouse.png", Vector2(173, 102), 10, 1.35, Vector2(28, 64))
	_spr("res://assets/processed/prop_boat.png", Vector2(160, 110), 6, 1.25)
	_spr("res://assets/processed/prop_bridge.png", Vector2(162, 110), 5, 1.15)
	_spr("res://assets/processed/prop_townhouse_blue.png", Vector2(178, 92), 8, 1.0, Vector2(36, 28))
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(148, 96), 8, 1.0, Vector2(40, 26))
	_spr("res://assets/processed/prop_townhouse_brown.png", Vector2(140, 112), 8, 0.95, Vector2(36, 28))
	for x in range(146, 156, 2):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 100), 4)
