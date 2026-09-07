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

func _spr(path: String, tile: Vector2, z: int = 0, scale_mul: float = 1.0, coll: Vector2 = Vector2.ZERO, tint: Color = Color(1, 1, 1, 1), y_sort: bool = true) -> Node2D:
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
		## Bias collision upward so south door approach stays clear
		cs.position = Vector2(0, -coll.y * 0.55)
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
	s.modulate = tint
	s.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	s.y_sort_enabled = y_sort
	## Soft grounding shadow (small oval at feet — large props use smaller relative shadow)
	var shadow := Polygon2D.new()
	shadow.z_index = -1
	shadow.color = Color(0.08, 0.08, 0.12, 0.22)
	var sw := clampf(float(tex.get_width()) * scale_mul * 0.18, 5.0, 14.0)
	var sh := clampf(sw * 0.32, 2.0, 5.0)
	var pts := PackedVector2Array()
	for i in range(10):
		var a := TAU * float(i) / 10.0
		pts.append(Vector2(cos(a) * sw, sin(a) * sh + 1.0))
	shadow.polygon = pts
	root.add_child(shadow)
	root.add_child(s)
	root.position = tile * TS
	## Entities y_sort requires shared z_index with Player (non-sorting skyline keeps z)
	root.z_index = 0 if y_sort else z
	root.y_sort_enabled = y_sort
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
	## Tall seamless skyline + batched pine canopy strip (perf: not 2k tree sprites).
	_spr("res://assets/processed/prop_skyline_wide.png", Vector2(96, 0), 1, 1.0, Vector2.ZERO, Color(1, 1, 1, 1), false)
	# Overlapping canopy masses under skyline (waterfall window baked transparent)
	_spr("res://assets/processed/prop_pine_canopy.png", Vector2(96, 14), 3, 1.0, Vector2.ZERO, Color(1, 1, 1, 1), false)
	_spr("res://assets/processed/prop_pine_canopy.png", Vector2(96, 19), 4, 1.0, Vector2.ZERO, Color(0.88, 0.96, 0.9, 1), false)
	_spr("res://assets/processed/prop_pine_canopy.png", Vector2(96, 22), 4, 1.0, Vector2.ZERO, Color(0.75, 0.9, 0.82, 0.85), false)
	## Mid-valley deciduous oil — staggered (break rigid horizontal bands / corridor windows)
	_spr("res://assets/processed/prop_meadow_canopy.png", Vector2(88, 38), 2, 1.0, Vector2.ZERO, Color(1, 1, 1, 0.72), false)
	_spr("res://assets/processed/prop_meadow_canopy.png", Vector2(104, 44), 2, 1.0, Vector2.ZERO, Color(0.92, 0.98, 0.9, 0.48), false)
	_spr("res://assets/processed/prop_meadow_canopy.png", Vector2(78, 52), 2, 0.95, Vector2.ZERO, Color(0.88, 0.96, 0.86, 0.38), false)
	# Sparse landmark accent pines only
	for p in [Vector2(6, 14), Vector2(48, 13), Vector2(120, 14), Vector2(186, 13)]:
		_spr("res://assets/processed/tree_pine.png", p, 5, 0.95)

func _ruins() -> void:
	## Irregular mossy arches woven with canopy (break flat grid rows)
	var arches := [
		Vector2(68, 14), Vector2(76, 12), Vector2(84, 15), Vector2(92, 13), Vector2(100, 16),
		Vector2(72, 19), Vector2(80, 21), Vector2(88, 18), Vector2(96, 20),
		Vector2(74, 24), Vector2(86, 25), Vector2(94, 23),
	]
	# Keep grove below ridge so skyline stays open
	var grove := [
		Vector2(70, 20), Vector2(82, 22), Vector2(94, 21), Vector2(78, 26), Vector2(90, 27),
	]
	for i in range(grove.size()):
		var gp: Vector2 = grove[i]
		var tpath := "res://assets/processed/tree_pine.png" if (i % 3) == 0 else ("res://assets/processed/tree_%d.png" % (i % 3))
		_spr(tpath, gp, 5 if (i % 2) == 0 else 8, 0.95 + float(i % 3) * 0.08)
	for i in range(arches.size()):
		var p: Vector2 = arches[i]
		var path := "res://assets/processed/prop_ruin_arch.png" if (i % 2) == 0 else "res://assets/processed/prop_ruins.png"
		var z := 6 if (i % 3) == 0 else 7
		_spr(path, p, z, 0.8 + float(i % 4) * 0.1, Vector2(32, 16))
	for x in range(60, 108, 4):
		_spr("res://assets/processed/prop_stonewall.png", Vector2(x, 29), 6, 1.0)
	for p in [
		Vector2(66, 22), Vector2(80, 28), Vector2(94, 22), Vector2(72, 28), Vector2(88, 26),
		Vector2(76, 12), Vector2(90, 14), Vector2(100, 24), Vector2(64, 26), Vector2(84, 28),
	]:
		_spr("res://assets/processed/prop_rocks.png", p, 5, 1.0)
	_spr("res://assets/processed/chest.png", Vector2(82, 18), 6, 0.9)

func _river() -> void:
	## Amphitheater bowl above canopy/skyline (non-y-sort) so hero shot reads falls
	for p in [Vector2(9, 15), Vector2(13, 18), Vector2(35, 15), Vector2(39, 18), Vector2(11, 21), Vector2(37, 21)]:
		_spr("res://assets/processed/tree_pine.png", p, 5, 1.2)
	_spr("res://assets/processed/prop_waterfall_bowl.png", Vector2(24, 18), 8, 1.2, Vector2(56, 48), Color(1, 1, 1, 1), false)
	_spr("res://assets/processed/prop_rocks.png", Vector2(14, 24), 8, 1.3)
	_spr("res://assets/processed/prop_rocks.png", Vector2(34, 24), 8, 1.25)
	_spr("res://assets/processed/prop_rocks.png", Vector2(20, 26), 8, 1.1)
	_spr("res://assets/processed/prop_rocks.png", Vector2(28, 26), 8, 1.1)
	_spr("res://assets/processed/prop_rocks.png", Vector2(18, 22), 8, 1.0)
	_spr("res://assets/processed/prop_rocks.png", Vector2(30, 22), 8, 1.0)
	_spr("res://assets/processed/bush.png", Vector2(16, 23), 9, 0.95)
	_spr("res://assets/processed/bush.png", Vector2(32, 23), 9, 0.95)
	for p in [Vector2(8, 16), Vector2(12, 20), Vector2(36, 16), Vector2(40, 20), Vector2(10, 24), Vector2(38, 24)]:
		var pine := "res://assets/processed/tree_pine_b.png" if int(p.x) % 2 == 0 else "res://assets/processed/tree_pine_c.png"
		_spr(pine, p, 5, 1.15)
	for p in [Vector2(14, 26), Vector2(34, 26)]:
		_spr("res://assets/processed/tree_%d.png" % (int(p.x) % 3), p, 10, 1.05)
	_spr("res://assets/processed/bush.png", Vector2(19, 26), 9, 1.0)
	_spr("res://assets/processed/bush.png", Vector2(29, 26), 9, 1.0)
	_spr("res://assets/processed/prop_bridge.png", Vector2(29, 40), 5, 1.2)
	_spr("res://assets/processed/prop_bridge.png", Vector2(29, 62), 5, 1.2)
	_spr("res://assets/processed/prop_bridge.png", Vector2(28, 78), 5, 1.1)

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
	_spr("res://assets/processed/prop_townhouse_brown.png", Vector2(168, 48), 8, 1.0, Vector2(40, 30), Color(1.05, 0.92, 0.88))
	_spr("res://assets/processed/prop_townhouse_green.png", Vector2(176, 56), 8, 0.95, Vector2(36, 28), Color(0.92, 1.05, 0.95))
	_spr("res://assets/processed/prop_farmhouse.png", Vector2(166, 62), 8, 0.95, Vector2(40, 26))
	_spr("res://assets/processed/prop_flowerbed.png", Vector2(170, 52), 4)
	_spr("res://assets/processed/prop_fence.png", Vector2(164, 44), 4)
	_spr("res://assets/processed/prop_fence.png", Vector2(172, 44), 4)

func _process(delta: float) -> void:
	if _train != null:
		_train_t += delta
		_train.position.x = _train_home.x + sin(_train_t * 0.35) * 10.0
		_train.position.y = _train_home.y + sin(_train_t * 2.2) * 0.6
	if _lighthouse_sprite != null:
		_lh_t += delta
		var pulse := 0.85 + 0.15 * sin(_lh_t * 3.0)
		_lighthouse_sprite.modulate = Color(pulse, pulse, 0.95 + 0.05 * sin(_lh_t * 2.0), 1.0)

func _farm() -> void:
	_spr("res://assets/processed/prop_farmhouse_darkroof.png", Vector2(40, 88), 0, 1.05, Vector2(48, 28))
	## Deck/porch strip — Stardew farmhouse sits on raised wood, not floating
	_spr("res://assets/processed/prop_doormat.png", Vector2(40, 91), 0, 1.2)
	_spr("res://assets/processed/prop_doormat.png", Vector2(42, 91), 0, 1.15)
	_spr("res://assets/processed/prop_doormat.png", Vector2(41, 92), 0, 1.0)
	_spr("res://assets/processed/prop_bench.png", Vector2(36, 91), 0, 0.9)
	_spr("res://assets/processed/prop_crate.png", Vector2(44, 91), 0, 0.95)
	_spr("res://assets/processed/prop_barrel.png", Vector2(45, 92), 0, 0.9)
	_spr("res://assets/processed/prop_hay.png", Vector2(33, 93), 0, 1.0)
	_spr("res://assets/processed/prop_hay.png", Vector2(47, 94), 0, 0.95)
	## Stardew clearing debris — rocks/logs/weeds dense on dirt apron
	for p in [
		Vector2(34, 92), Vector2(46, 93), Vector2(38, 94), Vector2(42, 95),
		Vector2(30, 96), Vector2(50, 97), Vector2(36, 98), Vector2(44, 99),
		Vector2(32, 100), Vector2(48, 101), Vector2(40, 102), Vector2(28, 98),
	]:
		_spr("res://assets/processed/prop_rocks.png", p, 4, 0.75 + float(int(p.x) % 3) * 0.08)
	for p2 in [
		Vector2(35, 95), Vector2(43, 96), Vector2(39, 100), Vector2(51, 99),
		Vector2(29, 94), Vector2(47, 98),
	]:
		_spr("res://assets/processed/prop_path_tuft.png", p2, 3, 1.0)
	_spr("res://assets/processed/prop_barn.png", Vector2(28, 102), 0, 1.25, Vector2(56, 32))
	_spr("res://assets/processed/prop_doormat.png", Vector2(28, 105), 0, 1.1)
	_spr("res://assets/processed/prop_barn2.png", Vector2(48, 104), 0, 1.2, Vector2(52, 30))
	## Silos south of farmhouse so dome caps stay in farm golden frame
	_spr("res://assets/processed/prop_silo.png", Vector2(34, 100), 0, 1.15, Vector2(16, 36))
	_spr("res://assets/processed/prop_silo.png", Vector2(50, 100), 0, 1.15, Vector2(16, 36))
	_spr("res://assets/processed/prop_chimney.png", Vector2(41, 86), 0, 1.1)
	_spr("res://assets/processed/prop_signboard.png", Vector2(34, 86), 0, 1.05)
	_spr("res://assets/processed/prop_flowerbed.png", Vector2(36, 90), 4, 1.0)
	_spr("res://assets/processed/prop_flowerbed.png", Vector2(44, 90), 4, 1.0)
	_spr("res://assets/processed/prop_planter.png", Vector2(38, 91), 5, 0.95)
	_spr("res://assets/processed/prop_planter.png", Vector2(46, 91), 5, 0.95)
	## Decorative mature beds OUTSIDE playable hoe rows
	## Hoe beds ~ (14-29/34-49, y78-86) and (14-29/34-49, y92-99) — keep clear
	## Place on barn apron south of beds (y>=106)
	var farm_crops: Array[String] = ["greens", "wheat", "tomato", "radish", "pumpkin"]
	for row in range(2):
		for col in range(6):
			var cx := 20 + col * 2
			var cy := 106 + row * 2
			var kind: String = farm_crops[(row + col) % farm_crops.size()]
			var stage: int = 2 + ((row + col) % 2)
			var crop_path: String = "res://assets/processed/crop_%s_%d.png" % [kind, stage]
			_spr(crop_path, Vector2(cx, cy), 4, 1.05)
	for col in range(5):
		var kind2: String = farm_crops[col % farm_crops.size()]
		var edge_path: String = "res://assets/processed/crop_%s_3.png" % kind2
		_spr(edge_path, Vector2(58 + col * 2, 86), 4, 1.0)
	_spr("res://assets/processed/prop_crate.png", Vector2(22, 100), 5, 1.1)
	_spr("res://assets/processed/prop_barrel.png", Vector2(56, 100), 5, 1.05)
	## Live chickens/cows come from decor._animals — no static doubles
	## Dense rail fence (1-tile step so rails connect edge-to-edge)
	## South side leaves a 3-tile gate so player/animals can enter the pen
	for x in range(24, 46, 1):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 112), 0, 1.0, Vector2(14, 10))
		if x < 32 or x > 35:
			_spr("res://assets/processed/prop_fence.png", Vector2(x, 122), 0, 1.0, Vector2(14, 10))
	for y in range(112, 123, 1):
		_spr("res://assets/processed/prop_fence.png", Vector2(24, y), 0, 1.0, Vector2(10, 14))
		_spr("res://assets/processed/prop_fence.png", Vector2(44, y), 0, 1.0, Vector2(10, 14))
	for x in range(14, 60, 1):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 74), 0, 1.0, Vector2(14, 10))

func _town() -> void:
	## Overview silhouette: lived-in residential ring + hero facades
	_spr("res://assets/processed/prop_statue.png", Vector2(90, 70), 7, 1.2, Vector2(18, 22))
	_spr("res://assets/processed/prop_flowerbed.png", Vector2(84, 66), 4, 1.0)
	_spr("res://assets/processed/prop_flowerbed.png", Vector2(96, 66), 4, 1.0)
	_spr("res://assets/processed/prop_bench.png", Vector2(86, 72), 4, 1.05)
	_spr("res://assets/processed/prop_bench.png", Vector2(94, 72), 4, 1.05)
	_spr("res://assets/processed/prop_lamp.png", Vector2(80, 64), 5, 1.1)
	_spr("res://assets/processed/prop_lamp.png", Vector2(100, 64), 5, 1.1)
	_spr("res://assets/processed/prop_lamp.png", Vector2(72, 52), 5, 1.05)
	_spr("res://assets/processed/prop_lamp.png", Vector2(108, 52), 5, 1.05)
	# Hero shop / cafe / bakery — short coll so south door tiles stay walkable
	_spr("res://assets/processed/prop_shop_awning.png", Vector2(78, 50), 10, 1.55, Vector2(52, 28))
	_spr("res://assets/processed/prop_cafe_awning.png", Vector2(102, 50), 10, 1.55, Vector2(52, 28))
	_spr("res://assets/processed/prop_bakery.png", Vector2(90, 62), 10, 1.45, Vector2(40, 22))
	# Door mats + crates at storefront feet (overview lived-in clutter)
	_spr("res://assets/processed/prop_doormat.png", Vector2(78, 54), 3, 1.0)
	_spr("res://assets/processed/prop_doormat.png", Vector2(102, 54), 3, 1.0)
	_spr("res://assets/processed/prop_crate.png", Vector2(72, 54), 4, 0.95)
	_spr("res://assets/processed/prop_barrel.png", Vector2(108, 54), 4, 0.95)
	_spr("res://assets/processed/prop_crate.png", Vector2(86, 58), 4, 0.9)
	_spr("res://assets/processed/prop_barrel.png", Vector2(94, 58), 4, 0.9)
	# Stalls south/side — never covering facade signs
	_spr("res://assets/processed/prop_stall.png", Vector2(76, 70), 6, 1.1, Vector2(28, 16))
	_spr("res://assets/processed/prop_stall_blue.png", Vector2(104, 70), 6, 1.1, Vector2(28, 16))
	_spr("res://assets/processed/prop_stall_yellow.png", Vector2(70, 58), 6, 1.0, Vector2(26, 16))
	_spr("res://assets/processed/prop_stall.png", Vector2(110, 58), 6, 1.0, Vector2(26, 16))
	_spr("res://assets/processed/prop_stall_blue.png", Vector2(82, 74), 6, 0.95, Vector2(24, 14))
	_spr("res://assets/processed/prop_stall_yellow.png", Vector2(98, 74), 6, 0.95, Vector2(24, 14))
	for p in [Vector2(84, 54), Vector2(96, 54), Vector2(84, 66), Vector2(96, 66), Vector2(88, 68), Vector2(92, 68)]:
		_spr("res://assets/processed/prop_planter.png", p, 5, 1.0)
	# Shade trees in residential yards (overview density — not plaza center)
	for tp in [Vector2(58, 44), Vector2(122, 44), Vector2(50, 62), Vector2(130, 62), Vector2(70, 82), Vector2(110, 82)]:
		_spr("res://assets/processed/tree_%d.png" % (int(tp.x + tp.y) % 3), tp, 6, 1.15)
	# Houses ring — keep clear of hero facade footprints
	var houses := [
		[Vector2(54, 40), "red"],
		[Vector2(54, 58), "thatch"],
		[Vector2(126, 40), "slate"],
		[Vector2(126, 58), "green"],
		[Vector2(74, 76), "slate"],
		[Vector2(106, 76), "thatch"],
		[Vector2(48, 50), "green"],
		[Vector2(132, 50), "red"],
		[Vector2(62, 34), "slate"],
		[Vector2(118, 34), "thatch"],
		[Vector2(66, 88), "green"],
		[Vector2(114, 88), "red"],
	]
	for h in houses:
		var path := "res://assets/processed/prop_house_redroof.png"
		match str(h[1]):
			"red":
				path = "res://assets/processed/prop_house_redroof.png"
			"slate":
				path = "res://assets/processed/prop_house_slateroof.png"
			"thatch":
				path = "res://assets/processed/prop_house_thatch.png"
			"green":
				path = "res://assets/processed/prop_house_greenroof.png"
		var hp := h[0] as Vector2
		_spr(path, hp, 8, 1.2, Vector2(42, 34))
		## Yard props (fence + flower + crate) — ref residential density
		_spr("res://assets/processed/prop_fence.png", hp + Vector2(-2, 4), 4, 0.9, Vector2(12, 8))
		_spr("res://assets/processed/prop_flowerbed.png", hp + Vector2(2, 5), 4, 0.95)
		_spr("res://assets/processed/prop_chair.png", hp + Vector2(1, 4), 4, 0.85)
		if int(hp.x + hp.y) % 2 == 0:
			_spr("res://assets/processed/prop_crate.png", hp + Vector2(-3, 3), 5, 0.85)
		else:
			_spr("res://assets/processed/prop_barrel.png", hp + Vector2(3, 3), 5, 0.85)
	for x in range(68, 114, 3):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 80), 4, 1.0, Vector2(12, 8))
	## Plaza pebble accents (break empty grass between stalls)
	for p2 in [Vector2(88, 66), Vector2(92, 68), Vector2(86, 70), Vector2(94, 70), Vector2(90, 74)]:
		_spr("res://assets/processed/prop_path_pebble.png", p2, 2, 0.9)
		_spr("res://assets/processed/prop_path_tuft.png", p2 + Vector2(1, 0), 2, 0.85)

func _station() -> void:
	# Hall + canopy + train on south rails; dense lived-in clutter
	_spr("res://assets/processed/prop_station.png", Vector2(152, 20), 0, 1.05, Vector2(96, 26))
	_spr("res://assets/processed/prop_canopy.png", Vector2(158, 24), 0, 1.15)
	_train = _spr("res://assets/processed/prop_train.png", Vector2(162, 26), 0, 1.2, Vector2.ZERO)
	if _train != null:
		_train_home = _train.position
		_attach_train_steam(_train)
	_spr("res://assets/processed/prop_tunnel.png", Vector2(186, 18), 0, 1.25, Vector2(32, 28))
	# Luggage / crates / barrels (platform left + right)
	for p in [Vector2(140, 22), Vector2(143, 23), Vector2(146, 22), Vector2(168, 22), Vector2(171, 24)]:
		_spr("res://assets/processed/prop_crate.png", p, 0, 0.95)
	for p in [Vector2(145, 24), Vector2(170, 23), Vector2(148, 25)]:
		_spr("res://assets/processed/prop_barrel.png", p, 0, 0.9)
	_spr("res://assets/processed/prop_bench.png", Vector2(150, 23), 0, 1.0)
	_spr("res://assets/processed/prop_bench.png", Vector2(166, 23), 0, 1.0)
	_spr("res://assets/processed/prop_lamp.png", Vector2(148, 18), 0)
	_spr("res://assets/processed/prop_lamp.png", Vector2(168, 18), 0)
	_spr("res://assets/processed/prop_lamp.png", Vector2(156, 28), 0)
	_spr("res://assets/processed/prop_signboard.png", Vector2(154, 14), 0)
	_spr("res://assets/processed/prop_doormat.png", Vector2(152, 22), 0, 0.9)
	_spr("res://assets/processed/prop_flowerbed.png", Vector2(149, 16), 0, 0.85)
	_spr("res://assets/processed/prop_flowerbed.png", Vector2(161, 16), 0, 0.85)
	for p2 in [Vector2(144, 27), Vector2(150, 28), Vector2(158, 28), Vector2(164, 27), Vector2(170, 28)]:
		_spr("res://assets/processed/prop_path_pebble.png", p2, 0, 0.9)
		_spr("res://assets/processed/prop_path_tuft.png", p2 + Vector2(1, 0), 0, 0.85)
	for x in range(132, 180, 2):
		_spr("res://assets/processed/prop_fence.png", Vector2(x, 30), 0)

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
	var lh := _spr("res://assets/processed/prop_lighthouse.png", Vector2(174, 100), 11, 1.55, Vector2(24, 48))
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
	## Mature rows on lake-west fields (outside water ellipse)
	var lake_crops: Array[String] = ["wheat", "tomato", "greens", "pumpkin", "radish"]
	for col in range(6):
		var k: String = lake_crops[col % lake_crops.size()]
		_spr("res://assets/processed/crop_%s_3.png" % k, Vector2(114 + col * 2, 106), 4, 1.0)
		_spr("res://assets/processed/crop_%s_2.png" % k, Vector2(114 + col * 2, 108), 4, 1.0)
	for col2 in range(5):
		var k2: String = lake_crops[(col2 + 2) % lake_crops.size()]
		_spr("res://assets/processed/crop_%s_3.png" % k2, Vector2(114 + col2 * 2, 116), 4, 1.0)
	for col3 in range(8):
		var k3: String = lake_crops[col3 % lake_crops.size()]
		_spr("res://assets/processed/crop_%s_2.png" % k3, Vector2(142 + col3 * 2, 125), 4, 0.95)
	for p in [Vector2(116, 112), Vector2(122, 118), Vector2(148, 126)]:
		_spr("res://assets/processed/prop_path_tuft.png", p, 3, 1.0)
