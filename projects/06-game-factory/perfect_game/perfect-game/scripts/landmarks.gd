extends Node2D
## Landmark props denser / better scaled toward oakhaven_overview reference.

const TS := 16

var _train: Node2D = null
var _train_home: Vector2 = Vector2.ZERO
var _train_t: float = 0.0
var _lighthouse_sprite: Sprite2D = null
var _lh_t: float = 0.0

func _ready() -> void:
	_place()

func _spr(path: String, tile: Vector2, z: int = 6, scale_mul: float = 1.0, coll: Vector2 = Vector2.ZERO) -> Node2D:
	var abs_path := ProjectSettings.globalize_path(path)
	var img := Image.new()
	if img.load(abs_path) != OK:
		push_warning("missing landmark: %s" % path)
		return null
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
	root.set_meta("sprite", s)
	add_child(root)
	return root

func _place() -> void:
	_mountains()
	_farm()
	_river()
	_ruins()
	_town()
	_station()
	_terrace()
	_lake()

func _mountains() -> void:
	## Distant skyline + cliff shelf (readable at overview zoom)
	for x in range(-4, 200, 5):
		_spr("res://assets/processed/prop_mountains.png", Vector2(x, 0), 0, 2.1)
	for x in range(0, 192, 3):
		_spr("res://assets/processed/prop_cliff.png", Vector2(x, 6), 1, 1.35)
	for x in range(1, 191, 4):
		_spr("res://assets/processed/prop_hills.png", Vector2(x, 10), 1, 1.5)
	for x in range(2, 190, 5):
		_spr("res://assets/processed/prop_hills.png", Vector2(x, 14), 2, 1.15)

func _ruins() -> void:
	## Nested mossy arches in forest north of plaza
	var arches := [
		Vector2(68, 14), Vector2(76, 12), Vector2(84, 14), Vector2(92, 12),
		Vector2(72, 18), Vector2(88, 18), Vector2(80, 16), Vector2(96, 16),
		Vector2(64, 20), Vector2(100, 20), Vector2(78, 20), Vector2(86, 22),
	]
	for i in range(arches.size()):
		var p: Vector2 = arches[i]
		var path := "res://assets/processed/prop_ruin_arch.png" if (i % 2) == 0 else "res://assets/processed/prop_ruins.png"
		_spr(path, p, 7, 0.85 + float(i % 3) * 0.12, Vector2(36, 18))
	for x in range(66, 102, 4):
		_spr("res://assets/processed/prop_stonewall.png", Vector2(x, 24), 6, 1.05)
	for p in [Vector2(70, 22), Vector2(82, 26), Vector2(94, 22), Vector2(76, 26), Vector2(90, 24)]:
		_spr("res://assets/processed/prop_rocks.png", p, 5, 1.0)

func _terrace() -> void:
	## Layered ledges with crops (not only retaining walls)
	for band in range(5):
		var y := 42 + band * 10
		for x in range(126, 164, 5):
			_spr("res://assets/processed/prop_stonewall.png", Vector2(x, y + 4), 5, 1.1)
		for x in range(128, 162, 3):
			var crop := "res://assets/processed/crop_%s_2.png" % ["wheat", "greens", "tomato", "radish"][band % 4]
			_spr(crop, Vector2(x, y + 1), 4, 1.0)
		_spr("res://assets/processed/prop_planter.png", Vector2(130 + band * 6, y + 2), 5, 0.9)
	_spr("res://assets/processed/prop_townhouse_brown.png", Vector2(168, 48), 8, 1.0, Vector2(40, 30))
	_spr("res://assets/processed/prop_townhouse_green.png", Vector2(176, 56), 8, 0.95, Vector2(36, 28))
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(166, 62), 8, 0.95, Vector2(40, 26))
	_spr("res://assets/processed/prop_flowerbed.png", Vector2(170, 52), 4)
	_spr("res://assets/processed/prop_fence.png", Vector2(164, 44), 4)
	_spr("res://assets/processed/prop_fence.png", Vector2(172, 44), 4)

func _process(delta: float) -> void:
	# Idle train rock + slow crawl along platform
	if _train != null:
		_train_t += delta
		_train.position.x = _train_home.x + sin(_train_t * 0.35) * 10.0
		_train.position.y = _train_home.y + sin(_train_t * 2.2) * 0.6
	# Lighthouse lantern pulse
	if _lighthouse_sprite != null:
		_lh_t += delta
		var pulse := 0.85 + 0.15 * sin(_lh_t * 3.0)
		_lighthouse_sprite.modulate = Color(pulse, pulse, 0.95 + 0.05 * sin(_lh_t * 2.0), 1.0)

func _farm() -> void:
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(40, 88), 8, 1.05, Vector2(48, 28))
	_spr("res://assets/processed/prop_barn.png", Vector2(28, 102), 8, 1.05, Vector2(70, 36))
	_spr("res://assets/processed/prop_barn2.png", Vector2(48, 104), 8, 1.0, Vector2(64, 34))
	_spr("res://assets/processed/prop_silo.png", Vector2(36, 98), 8, 1.1, Vector2(22, 48))
	_spr("res://assets/processed/prop_silo.png", Vector2(52, 98), 8, 1.1, Vector2(22, 48))
	for x in range(24, 46, 2):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 112), 4, 1.0, Vector2(14, 10))
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 122), 4, 1.0, Vector2(14, 10))
	for y in range(112, 122, 2):
		_spr("res://assets/processed/prop_fence.png", Vector2(24, y), 4, 1.0, Vector2(10, 14))
		_spr("res://assets/processed/prop_fence.png", Vector2(44, y), 4, 1.0, Vector2(10, 14))
	for x in range(14, 60, 3):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 74), 4, 1.0, Vector2(14, 10))

func _river() -> void:
	_spr("res://assets/processed/prop_waterfall.png", Vector2(24, 20), 9, 1.35, Vector2(40, 36))
	_spr("res://assets/processed/prop_bridge.png", Vector2(29, 40), 5, 1.2)
	_spr("res://assets/processed/prop_bridge.png", Vector2(29, 62), 5, 1.2)
	_spr("res://assets/processed/prop_bridge.png", Vector2(28, 78), 5, 1.1)

func _town() -> void:
	_spr("res://assets/processed/prop_statue.png", Vector2(90, 48), 7, 1.2, Vector2(18, 22))
	_spr("res://assets/processed/prop_flowerbed.png", Vector2(90, 42), 4, 1.0)
	_spr("res://assets/processed/prop_flowerbed.png", Vector2(90, 54), 4, 1.0)
	_spr("res://assets/processed/prop_stall.png", Vector2(78, 38), 6, 1.15, Vector2(30, 18))
	_spr("res://assets/processed/prop_stall_blue.png", Vector2(102, 38), 6, 1.15, Vector2(30, 18))
	_spr("res://assets/processed/prop_stall_yellow.png", Vector2(78, 58), 6, 1.1, Vector2(30, 18))
	_spr("res://assets/processed/prop_stall.png", Vector2(102, 58), 6, 1.15, Vector2(30, 18))
	_spr("res://assets/processed/prop_stall_blue.png", Vector2(70, 48), 6, 1.05, Vector2(28, 16))
	_spr("res://assets/processed/prop_stall_yellow.png", Vector2(110, 48), 6, 1.05, Vector2(28, 16))
	for p in [Vector2(82, 44), Vector2(98, 44), Vector2(82, 52), Vector2(98, 52)]:
		_spr("res://assets/processed/prop_planter.png", p, 5, 1.0)
	_spr("res://assets/processed/prop_shop.png", Vector2(72, 32), 8, 1.05, Vector2(48, 28))
	_spr("res://assets/processed/prop_cafe.png", Vector2(108, 32), 8, 1.05, Vector2(48, 28))
	var houses := [
		[Vector2(66, 38), "brown"], [Vector2(66, 54), "green"],
		[Vector2(114, 38), "blue"], [Vector2(114, 54), "brown"],
		[Vector2(74, 64), "blue"], [Vector2(90, 66), "brown"], [Vector2(106, 64), "green"],
		[Vector2(82, 28), "green"], [Vector2(98, 28), "brown"],
		[Vector2(70, 70), "brown"], [Vector2(110, 70), "blue"],
	]
	for h in houses:
		var path := "res://assets/processed/prop_townhouse_blue.png"
		match str(h[1]):
			"brown":
				path = "res://assets/processed/prop_townhouse_brown.png"
			"green":
				path = "res://assets/processed/prop_townhouse_green.png"
		_spr(path, h[0], 8, 1.0, Vector2(40, 30))
	for x in range(68, 114, 3):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 74), 4, 1.0, Vector2(12, 8))

func _station() -> void:
	# Upgraded hall + canopy + crawling train; collision shorter so door is approachable
	_spr("res://assets/processed/prop_station.png", Vector2(148, 16), 8, 1.1, Vector2(100, 28))
	_spr("res://assets/processed/prop_canopy.png", Vector2(156, 20), 7, 1.2)
	_train = _spr("res://assets/processed/prop_train.png", Vector2(160, 22), 7, 1.25, Vector2.ZERO)
	if _train != null:
		_train_home = _train.position
		_attach_train_steam(_train)
	_spr("res://assets/processed/prop_tunnel.png", Vector2(184, 16), 9, 1.3, Vector2(36, 32))
	_spr("res://assets/processed/prop_crate.png", Vector2(136, 18), 5)
	_spr("res://assets/processed/prop_crate.png", Vector2(140, 20), 5)
	_spr("res://assets/processed/prop_barrel.png", Vector2(142, 18), 5)
	_spr("res://assets/processed/prop_lamp.png", Vector2(146, 14), 5)
	_spr("res://assets/processed/prop_lamp.png", Vector2(166, 14), 5)
	_spr("res://assets/processed/prop_signboard.png", Vector2(150, 10), 8)
	for x in range(128, 178, 3):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 26), 4)

func _attach_train_steam(train: Node2D) -> void:
	var p := CPUParticles2D.new()
	p.position = Vector2(-36, -28)
	p.amount = 18
	p.lifetime = 2.0
	p.emission_shape = CPUParticles2D.EMISSION_SHAPE_SPHERE
	p.emission_sphere_radius = 4.0
	p.direction = Vector2(0.2, -1)
	p.spread = 25.0
	p.gravity = Vector2(0, -12)
	p.initial_velocity_min = 12.0
	p.initial_velocity_max = 28.0
	p.scale_amount_min = 0.6
	p.scale_amount_max = 1.6
	p.color = Color(0.9, 0.9, 0.92, 0.5)
	p.z_index = 12
	train.add_child(p)

func _lake() -> void:
	var lh := _spr("res://assets/processed/prop_lighthouse.png", Vector2(174, 100), 11, 1.25, Vector2(30, 72))
	if lh != null and lh.has_meta("sprite"):
		_lighthouse_sprite = lh.get_meta("sprite")
	_spr("res://assets/processed/prop_rocks.png", Vector2(168, 106), 5, 1.2)
	_spr("res://assets/processed/prop_rocks.png", Vector2(180, 104), 5, 1.1)
	_spr("res://assets/processed/prop_rocks.png", Vector2(176, 110), 5, 1.0)
	_spr("res://assets/processed/prop_pier.png", Vector2(160, 110), 6, 1.15)
	_spr("res://assets/processed/prop_boat.png", Vector2(154, 112), 7, 1.15)
	_spr("res://assets/processed/prop_boat.png", Vector2(166, 114), 7, 0.95)
	_spr("res://assets/processed/prop_townhouse_blue.png", Vector2(180, 88), 8, 1.0, Vector2(40, 30))
	_spr("res://assets/processed/prop_townhouse_green.png", Vector2(186, 94), 8, 0.95, Vector2(36, 28))
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(134, 88), 8, 1.0, Vector2(40, 28))
	_spr("res://assets/processed/prop_townhouse_brown.png", Vector2(128, 108), 8, 0.95, Vector2(36, 28))
	_spr("res://assets/processed/prop_townhouse_blue.png", Vector2(124, 96), 8, 0.9, Vector2(34, 26))
	for x in range(130, 142, 2):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 92), 4, 1.0, Vector2(12, 8))
	for p in [Vector2(136, 94), Vector2(178, 92), Vector2(130, 104), Vector2(168, 96)]:
		_spr("res://assets/processed/prop_flowerbed.png", p, 4)
	for p in [Vector2(138, 96), Vector2(182, 90), Vector2(170, 102)]:
		_spr("res://assets/processed/prop_planter.png", p, 5)
	_spr("res://assets/processed/prop_lamp.png", Vector2(158, 108), 5)
	_spr("res://assets/processed/prop_lamp.png", Vector2(170, 100), 5)
	_spr("res://assets/processed/prop_crate.png", Vector2(156, 106), 4)
	_spr("res://assets/processed/prop_barrel.png", Vector2(162, 108), 4)
