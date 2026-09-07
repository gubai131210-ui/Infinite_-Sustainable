extends Node2D
## Dense decor: trees, flowers, animals, NPCs, farmhouse door, ambient smoke/ripples.
## Animal/NPC sheets are horizontal atlases — always crop one frame.

const TS := 16

func _ready() -> void:
	_trees()
	_forest_rim()
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

func _entity_host() -> Node:
	## Flatten onto Entities so Player/trees/NPCs share one y_sort sibling list
	var p := get_parent()
	return p if p != null else self

func _spr(path: String, tile: Vector2, z: int = 0, choppable: bool = false, scale_mul: float = 1.0) -> Sprite2D:
	var tex := _load_tex(path)
	if tex == null:
		return null
	var s := Sprite2D.new()
	s.texture = tex
	s.centered = true
	var th := float(tex.get_height()) * scale_mul
	s.offset = Vector2(0, -th * 0.5)
	s.scale = Vector2(scale_mul, scale_mul)
	s.position = tile * TS
	## z ignored for world props — Entities y_sort requires shared z_index
	s.z_index = 0
	s.y_sort_enabled = true
	s.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	if "tree" in path:
		s.set_meta("sway", true)
	elif "flower" in path or "bush" in path:
		s.set_meta("sway", true)
		s.set_meta("sway_soft", true)
	if choppable:
		s.add_to_group("choppable")
		s.set_meta("chop_hp", 2)
	_entity_host().add_child(s)
	return s

func _spr_atlas(path: String, tile: Vector2, z: int = 0, frame: int = 0, flip: bool = false) -> Sprite2D:
	var tex := _atlas_frame(path, frame)
	if tex == null:
		return null
	var s := Sprite2D.new()
	s.texture = tex
	s.centered = true
	var th := float(tex.get_height())
	s.offset = Vector2(0, -th * 0.5)
	s.position = tile * TS
	s.z_index = 0
	s.flip_h = flip
	s.y_sort_enabled = true
	s.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	_entity_host().add_child(s)
	return s

func _trees() -> void:
	var spots: Array[Vector2] = []
	# North belt: sparse accents only — skyline/mountains/clouds must read through
	for x in range(2, 68, 5):
		for y in range(22, 30, 4):
			if ((x * 3 + y * 5) % 7) < 4:
				continue
			if x >= 12 and x <= 38:
				continue  # wide waterfall sky corridor
			spots.append(Vector2(x + (y % 2) * 0.5, y + (x % 2) * 0.5))
	for x in range(72, 128, 5):
		for y in range(22, 28, 4):
			if ((x + y * 2) % 5) == 0:
				continue
			spots.append(Vector2(x + (y % 2), y))
	# Ruins grove — sparse weave below skyline
	for x in range(64, 100, 5):
		for y in range(20, 28, 4):
			if ((x + y) % 3) == 0:
				continue
			spots.append(Vector2(x + (y % 2), y + (x % 2)))
	# Farm edges + river corridor (choppable for axe wood)
	var farm_chop: Array[Vector2] = [
		Vector2(10, 70), Vector2(14, 74), Vector2(8, 88), Vector2(12, 100),
		Vector2(8, 110), Vector2(58, 70), Vector2(62, 78), Vector2(60, 90),
		Vector2(64, 100), Vector2(58, 110), Vector2(20, 66), Vector2(30, 68),
		Vector2(42, 66), Vector2(52, 68), Vector2(16, 62), Vector2(56, 62),
		Vector2(6, 80), Vector2(18, 86), Vector2(54, 86), Vector2(66, 94),
	]
	for p in farm_chop:
		spots.append(p)
	# River west bank denser (start lower so north skyline stays open)
	for y in range(36, 100, 2):
		spots.append(Vector2(8 + (y % 3), y))
		spots.append(Vector2(14 + (y % 2), y + 1))
		spots.append(Vector2(44 + (y % 4), y))
	# Town fringe dense
	for p in [
		Vector2(66, 28), Vector2(66, 34), Vector2(66, 40), Vector2(66, 48), Vector2(66, 55), Vector2(66, 68),
		Vector2(116, 28), Vector2(116, 34), Vector2(116, 40), Vector2(116, 48), Vector2(116, 55), Vector2(116, 68),
		Vector2(78, 44), Vector2(102, 44), Vector2(78, 72), Vector2(102, 72),
		Vector2(70, 48), Vector2(112, 48), Vector2(70, 68), Vector2(112, 68),
		Vector2(64, 52), Vector2(118, 52), Vector2(64, 64), Vector2(118, 64),
	]:
		spots.append(p)
	# Station ridge: NO tree wall — leave sky/mountain/cliff readable
	for x in range(118, 188, 2):
		for y in [86, 90, 94, 98, 112, 116, 120]:
			if ((x + y) % 3) != 0:
				spots.append(Vector2(x + (y % 2), y))
	for p in [
		Vector2(125, 18), Vector2(135, 20), Vector2(165, 18), Vector2(175, 20),
		Vector2(180, 28), Vector2(120, 40), Vector2(168, 45), Vector2(175, 55),
		Vector2(120, 88), Vector2(125, 100), Vector2(128, 115), Vector2(180, 90),
		Vector2(185, 105), Vector2(180, 118), Vector2(140, 120), Vector2(155, 122),
		Vector2(130, 85), Vector2(175, 85), Vector2(185, 95), Vector2(122, 105),
		Vector2(148, 88), Vector2(158, 92), Vector2(170, 118), Vector2(188, 110),
	]:
		spots.append(p)
	for i in range(spots.size()):
		var p: Vector2 = spots[i]
		var pine := "res://assets/processed/tree_pine.png"
		var path := "res://assets/processed/tree_%d.png" % (i % 3)
		var can_chop := p in farm_chop
		# Prefer mixed canopy; pines only as sparse accents (not a wall)
		if p.y < 16 and (i % 5) == 0 and _load_tex(pine) != null:
			_spr(pine, p, 6, can_chop)
		else:
			_spr(path, p, 6, can_chop)

func _forest_rim() -> void:
	## Valley enclosure for overview — dense rim canopy, keep sky/waterfall/station open.
	# West outer wall (left of river)
	for y in range(18, 124, 2):
		for x in range(0, 7, 2):
			if ((x + y) % 3) == 0:
				continue
			var pine_w := (y % 4) == 0
			_spr("res://assets/processed/tree_pine.png" if pine_w else "res://assets/processed/tree_%d.png" % ((x + y) % 3), Vector2(x + (y % 2) * 0.4, y), 6)
	# East outer wall (right of terraces / lake)
	for y in range(20, 124, 2):
		for x in range(184, 192, 2):
			if ((x * 2 + y) % 5) == 0:
				continue
			_spr("res://assets/processed/tree_%d.png" % ((x + y) % 3), Vector2(x, y + (x % 2) * 0.3), 6)
	# South canopy belt
	for x in range(4, 188, 2):
		for y in range(120, 128, 2):
			if ((x + y * 3) % 4) == 0:
				continue
			_spr("res://assets/processed/tree_%d.png" % (x % 3), Vector2(x + (y % 2), y), 5)
	# N canopy: batched strip lives in landmarks — only sparse accent pines here (variants)
	for x in range(4, 188, 5):
		if x >= 18 and x <= 32:
			continue
		if x >= 132 and x <= 178 and (x % 3) != 0:
			continue
		var y := 22 + (x % 5)
		var path := "res://assets/processed/tree_pine.png"
		match (x + y) % 3:
			1:
				path = "res://assets/processed/tree_pine_b.png"
			2:
				path = "res://assets/processed/tree_pine_c.png"
		_spr(path, Vector2(x + 0.3, y), 5, false, 1.2 + float(x % 3) * 0.08)
	# Soft mid-map irregular groves — density along spines, clear plaza (P160 World-driven)
	for gx in range(38, 128, 3):
		for gy in range(24, 76, 3):
			# keep town plaza / storefronts clear of grove trees
			if gx >= 66 and gx <= 118 and gy >= 38 and gy <= 76:
				continue
			# leave waterfall approach open
			if gx <= 42 and gy <= 30:
				continue
			var h := (gx * 7 + gy * 11) % 11
			## denser along farm↔town corridor (y 55–88), thinner elsewhere
			var near_spine: bool = gy >= 55 and gy <= 88 and gx >= 42 and gx <= 100
			var thresh := 4 if near_spine else 6
			if h < thresh:
				continue
			_spr("res://assets/processed/tree_%d.png" % ((gx + gy) % 3), Vector2(gx + (gy % 3) * 0.25, gy + (gx % 2) * 0.25), 5, false, 0.95 + float(h % 3) * 0.06)
			if h >= 9:
				_spr("res://assets/processed/tree_pine.png", Vector2(gx + 1.1, gy + 0.7), 5, false, 1.05)
			if near_spine and h >= 8:
				_spr("res://assets/processed/bush.png", Vector2(gx + 0.6, gy + 1.1), 3, false)
	# Soft inner belts (east of river / west of town) to break empty mid-grass
	for y in range(26, 74, 3):
		_spr("res://assets/processed/tree_%d.png" % (y % 3), Vector2(46 + (y % 3), y), 5)
		_spr("res://assets/processed/tree_%d.png" % ((y + 1) % 3), Vector2(54 + (y % 2), y + 1), 5)
		_spr("res://assets/processed/bush.png", Vector2(50 + (y % 2) * 0.4, y + 0.5), 3, false)
	# Town→lake / town→station corridors (accent trees only — canopy strip fills mass)
	for x in range(110, 170, 3):
		for y in range(28, 50, 3):
			if x >= 130 and x <= 178 and y <= 28:
				continue  # station platform
			var hh := (x * 13 + y * 17) % 9
			if hh < 4:
				continue
			if hh <= 6:
				_spr("res://assets/processed/tree_%d.png" % ((x + y) % 3), Vector2(x + 0.2, y + 0.2), 5, false, 1.0)
			elif hh == 7:
				_spr("res://assets/processed/bush.png", Vector2(x, y), 3, false)
			else:
				_spr("res://assets/processed/flower_%d.png" % ((x + y) % 4), Vector2(x, y), 2, false)
	for x in range(118, 170, 3):
		for y in range(70, 100, 3):
			## west of lake / south of terraces
			if x >= 150 and y >= 86:
				continue  # lake water
			var hh2 := (x * 19 + y * 23) % 10
			if hh2 < 5:
				continue
			if hh2 <= 7:
				_spr("res://assets/processed/tree_%d.png" % ((x + y) % 3), Vector2(x + 0.15, y), 5, false, 0.98)
			elif hh2 == 8:
				_spr("res://assets/processed/bush.png", Vector2(x, y + 0.2), 3, false)
			else:
				_spr("res://assets/processed/flower_%d.png" % ((x) % 4), Vector2(x + 0.3, y), 2, false)
	# Mid-map ground clutter (flowers/tufts — trees alone don't kill grass sea)
	for x in range(38, 130, 2):
		for y in range(28, 76, 2):
			if x >= 70 and x <= 114 and y >= 36 and y <= 64:
				continue  # plaza
			var h := (x * 17 + y * 31) % 9
			if h == 0:
				_spr("res://assets/processed/prop_path_tuft.png", Vector2(x + 0.3, y), 2, false)
			elif h == 1 or h == 2:
				_spr("res://assets/processed/flower_%d.png" % ((x + y) % 4), Vector2(x, y), 2, false)
			elif h == 3:
				_spr("res://assets/processed/bush.png", Vector2(x + 0.2, y + 0.2), 3, false)
			elif h == 4:
				_spr("res://assets/processed/prop_path_pebble.png", Vector2(x + 0.1, y + 0.1), 2, false)

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
		Vector2(76, 52), Vector2(104, 52), Vector2(76, 64), Vector2(104, 64),
		Vector2(90, 48), Vector2(148, 14), Vector2(168, 100),
	]:
		_spr("res://assets/processed/prop_lamp.png", p, 5)
	## Farm bed / path seam tufts — Stardew grass overhang on dirt edges
	for x in range(13, 66, 2):
		_spr("res://assets/processed/prop_path_tuft.png", Vector2(x + 0.2, 77), 3, false)
		_spr("res://assets/processed/prop_path_tuft.png", Vector2(x, 88.2), 3, false)
		_spr("res://assets/processed/prop_path_tuft.png", Vector2(x + 0.4, 99.5), 3, false)
	for y in range(78, 100, 2):
		_spr("res://assets/processed/prop_path_tuft.png", Vector2(13.2, y), 3, false)
		_spr("res://assets/processed/prop_path_tuft.png", Vector2(50.5, y + 0.3), 3, false)
		_spr("res://assets/processed/prop_path_pebble.png", Vector2(30.5, y), 2, false)

func _bushes() -> void:
	# Plaza fringe tufts denser (around current storefront ring)
	for p in [
		Vector2(70, 48), Vector2(72, 46), Vector2(110, 46), Vector2(112, 48),
		Vector2(72, 66), Vector2(74, 68), Vector2(110, 66), Vector2(112, 68),
		Vector2(68, 52), Vector2(68, 58), Vector2(68, 64), Vector2(116, 52), Vector2(116, 58), Vector2(116, 64),
		Vector2(84, 48), Vector2(96, 48), Vector2(84, 70), Vector2(96, 70),
		Vector2(76, 54), Vector2(108, 54), Vector2(76, 64), Vector2(108, 64),
	]:
		_spr("res://assets/processed/prop_path_tuft.png", p, 3, false)
	for p in [
		Vector2(73, 50), Vector2(111, 52), Vector2(73, 62), Vector2(111, 60),
		Vector2(86, 49), Vector2(94, 49), Vector2(86, 67), Vector2(94, 67),
	]:
		_spr("res://assets/processed/prop_path_pebble.png", p, 2, false)
	# Path fringe tufts + pebbles (soften dirt edge brick-read)
	for p in [
		Vector2(50, 88), Vector2(58, 80), Vector2(66, 70), Vector2(74, 60), Vector2(82, 54),
		Vector2(88, 52), Vector2(96, 48), Vector2(104, 46), Vector2(112, 40), Vector2(120, 34),
		Vector2(70, 68), Vector2(100, 58), Vector2(48, 50), Vector2(52, 40), Vector2(60, 34),
		Vector2(108, 70), Vector2(118, 78), Vector2(130, 88), Vector2(140, 96), Vector2(150, 102),
		Vector2(80, 42), Vector2(70, 36), Vector2(55, 30), Vector2(42, 26), Vector2(34, 24),
		Vector2(62, 76), Vector2(84, 62), Vector2(94, 50), Vector2(116, 44), Vector2(128, 36),
		Vector2(76, 72), Vector2(102, 64), Vector2(54, 56), Vector2(46, 44), Vector2(38, 32),
	]:
		_spr("res://assets/processed/prop_path_tuft.png", p, 3, false)
	for p in [
		Vector2(52, 86), Vector2(64, 72), Vector2(78, 58), Vector2(90, 50), Vector2(106, 44),
		Vector2(72, 66), Vector2(98, 56), Vector2(56, 48), Vector2(44, 36), Vector2(122, 80),
		Vector2(136, 92), Vector2(148, 100), Vector2(68, 82), Vector2(86, 48), Vector2(110, 52),
	]:
		_spr("res://assets/processed/prop_path_pebble.png", p, 2, false)
	# Fill mid-map grass voids (overview "lived-in" density)
	for x in range(48, 120, 4):
		for y in range(70, 86, 4):
			if ((x + y) % 3) != 0:
				_spr("res://assets/processed/bush.png", Vector2(x + (y % 2), y), 4)
	# Farm ↔ town corridor fill
	for x in range(42, 86, 3):
		for y in range(62, 74, 3):
			if ((x * 3 + y) % 5) != 0:
				_spr("res://assets/processed/bush.png", Vector2(x + (y % 2), y), 4)
	# Mid-map void fill (Critic: empty grass between zones)
	for x in range(48, 118, 2):
		for y in range(48, 64, 2):
			if ((x * 2 + y * 3) % 7) == 0:
				continue
			if ((x + y) % 2) == 0:
				_spr("res://assets/processed/bush.png", Vector2(x + (y % 2), y), 4)
			else:
				_spr("res://assets/processed/flower_%d.png" % ((x + y) % 4), Vector2(x, y), 3)
	for p in [
		Vector2(24, 82), Vector2(44, 84), Vector2(86, 46), Vector2(94, 52),
		Vector2(132, 55), Vector2(150, 60), Vector2(168, 95), Vector2(155, 100),
		Vector2(80, 48), Vector2(100, 48), Vector2(140, 48), Vector2(148, 72),
		Vector2(56, 72), Vector2(64, 78), Vector2(110, 76), Vector2(118, 80),
		Vector2(100, 88), Vector2(72, 84), Vector2(128, 70), Vector2(136, 78),
		Vector2(58, 64), Vector2(66, 66), Vector2(74, 68), Vector2(52, 68),
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
		# Miller farmstead yard
		Vector2(34, 88), Vector2(42, 88), Vector2(38, 92), Vector2(48, 92),
		Vector2(20, 96), Vector2(54, 96), Vector2(26, 108), Vector2(42, 110),
	]
	for i in range(spots.size()):
		_spr("res://assets/processed/flower_%d.png" % (i % 4), spots[i], 3)
	# Dense meadow bands along farm ↔ town path (Critic)
	for x in range(46, 88, 2):
		for y in range(64, 74, 2):
			if ((x + y * 3) % 5) != 0:
				_spr("res://assets/processed/flower_%d.png" % ((x + y) % 4), Vector2(x + (y % 2), y), 3)
	for x in range(70, 112, 2):
		for y in range(34, 38, 2):
			_spr("res://assets/processed/flower_%d.png" % ((x + y) % 4), Vector2(x, y), 3)
	for x in range(120, 150, 2):
		for y in range(70, 78, 2):
			if ((x * 2 + y) % 3) != 0:
				_spr("res://assets/processed/flower_%d.png" % ((x + y) % 4), Vector2(x, y), 3)

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
	# 12 NPCs — lines/schedule from CharacterDB (docs/content/characters.json)
	var roster := [
		{"id": "he", "spr": "npc_01.png"},
		{"id": "man", "spr": "npc_02.png"},
		{"id": "yu", "spr": "npc_03.png"},
		{"id": "lin", "spr": "npc_04.png"},
		{"id": "zhou", "spr": "npc_05.png"},
		{"id": "tie", "spr": "npc_06.png"},
		{"id": "ka", "spr": "npc_07.png"},
		{"id": "ta", "spr": "npc_08.png"},
		{"id": "qiao", "spr": "npc_09.png"},
		{"id": "hua", "spr": "npc_10.png"},
		{"id": "mu", "spr": "npc_11.png"},
		{"id": "shan", "spr": "npc_12.png"},
	]
	var npc_scene := preload("res://scenes/npc.tscn")
	var cdb := get_node_or_null("/root/CharacterDB")
	var tc := get_node_or_null("/root/TimeClock")
	var period := str(tc.get("period")) if tc != null else "day"
	for info in roster:
		var nid := str(info["id"])
		var n := npc_scene.instantiate()
		n.npc_id = nid
		if cdb != null:
			n.display_name = str(cdb.call("display_name", nid))
			n.line = str(cdb.call("line_for", nid))
			var tile: Vector2 = cdb.call("schedule_tile", nid, period)
			if tile != Vector2.ZERO:
				n.position = tile * TS
			else:
				n.position = Vector2(90, 48) * TS
		else:
			n.display_name = nid
			n.line = "……"
			n.position = Vector2(90, 48) * TS
		n.sprite_path = "res://assets/processed/%s" % str(info["spr"])
		n.z_index = 0
		_entity_host().add_child(n)

func _animals() -> void:
	## All livestock inside south pen only (avoid tree canopy z-fight)
	var animal_spots := [
		["chicken", "鸡", Vector2(28, 114)],
		["chicken", "鸡", Vector2(32, 116)],
		["chicken", "鸡", Vector2(36, 114)],
		["cow", "牛", Vector2(30, 118)],
		["cow", "牛", Vector2(38, 118)],
		["sheep", "羊", Vector2(34, 116)],
		["sheep", "羊", Vector2(40, 116)],
	]
	var animal_scene := preload("res://scenes/animal.tscn")
	for item in animal_spots:
		var a := animal_scene.instantiate()
		a.animal_kind = str(item[0])
		a.display_name = str(item[1])
		a.sprite_path = "res://assets/processed/%s.png" % str(item[0])
		a.position = item[2] * TS
		a.z_index = 0
		## Pen clamp in animal script via meta
		a.set_meta("pen_min", Vector2(25, 113) * TS)
		a.set_meta("pen_max", Vector2(43, 121) * TS)
		a.set_meta("wander_radius", 28.0)
		_entity_host().add_child(a)

func _door_and_chest() -> void:
	_spr("res://assets/processed/chest.png", Vector2(36, 90), 4)
	# Door tiles match landmarks._town facade footprints (P103)
	var doors := [
		{"id": "farmhouse", "prompt": "按 E 进入农舍", "pos": Vector2(40, 88)},
		{"id": "barn", "prompt": "按 E 进入谷仓", "pos": Vector2(28, 102)},
		{"id": "shop", "prompt": "按 E 进入杂货店", "pos": Vector2(78, 51)},
		{"id": "cafe", "prompt": "按 E 进入咖啡馆", "pos": Vector2(102, 51)},
		{"id": "bakery", "prompt": "按 E 进入面包房", "pos": Vector2(90, 63)},
		{"id": "station", "prompt": "按 E 进入火车站厅", "pos": Vector2(152, 22)},
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
	var mail := preload("res://scenes/interact_zone.tscn").instantiate()
	mail.prompt_text = "按 E 查看信箱"
	mail.mode = "mail"
	mail.position = Vector2(44, 88) * TS
	add_child(mail)
	var ruin_chest := preload("res://scenes/interact_zone.tscn").instantiate()
	ruin_chest.prompt_text = "按 E 查看遗迹旧箱"
	ruin_chest.mode = "ruin_loot"
	ruin_chest.position = Vector2(82, 18) * TS
	add_child(ruin_chest)
	# Chinese wood placards (layout labels)
	var signs := [
		{"t": "米勒农庄", "pos": Vector2(42, 76)},
		{"t": "橡木河", "pos": Vector2(34, 48)},
		{"t": "橡木火车站", "pos": Vector2(154, 14)},
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
	fall.prompt_text = "按 E 倾听瀑布"
	fall.mode = "quest_zone"
	fall.quest_step_id = "visit_waterfall"
	fall.speaker = "瀑布回声"
	fall.message = "水雾扑面。耳边有人低语：\n「若你听见瀑布的回声，就去灯塔看一眼灯火。」"
	fall.position = Vector2(24, 18) * TS
	add_child(fall)
	var stall := preload("res://scenes/interact_zone.tscn").instantiate()
	stall.prompt_text = "按 E 看看摊位"
	stall.mode = "dialogue"
	stall.speaker = "摊主"
	stall.message = "今日番茄与萝卜新鲜，先去农庄种点种子吧！"
	stall.position = Vector2(90, 72) * TS
	add_child(stall)
	var sell := preload("res://scenes/interact_zone.tscn").instantiate()
	sell.prompt_text = "按 E 卖出作物"
	sell.mode = "shop_sell"
	sell.position = Vector2(74, 52) * TS
	add_child(sell)
	var buy := preload("res://scenes/interact_zone.tscn").instantiate()
	buy.prompt_text = "按 E 买种子礼包(30金)"
	buy.mode = "shop_buy"
	buy.position = Vector2(82, 52) * TS
	add_child(buy)
	# Quest visit triggers (轻松日常打卡)
	_quest_zone("visit_town", "镇中心", Vector2(90, 56))
	_quest_zone("visit_station", "火车站", Vector2(154, 22))
	_quest_zone("visit_lighthouse", "灯塔", Vector2(174, 102))
	var fish := preload("res://scenes/interact_zone.tscn").instantiate()
	fish.prompt_text = "按 E 钓鱼"
	fish.mode = "fish"
	fish.position = Vector2(160, 112) * TS
	add_child(fish)
	var fish_river := preload("res://scenes/interact_zone.tscn").instantiate()
	fish_river.prompt_text = "按 E 在河边钓鱼"
	fish_river.mode = "fish"
	fish_river.position = Vector2(34, 50) * TS
	add_child(fish_river)
	_market_festival()

func _market_festival() -> void:
	## Market day south of hero storefronts (do not cover GENERAL STORE / CAFE)
	for p in [Vector2(78, 70), Vector2(90, 72), Vector2(102, 70), Vector2(84, 76)]:
		_spr("res://assets/processed/prop_stall_yellow.png", p, 5)
	_spr("res://assets/processed/prop_stall_blue.png", Vector2(96, 76), 5)
	_spr("res://assets/processed/prop_canopy.png", Vector2(90, 74), 5)
	var lab := Label.new()
	lab.text = "今日集市"
	lab.position = Vector2(86, 72) * TS + Vector2(-20, -28)
	lab.z_index = 25
	lab.add_theme_font_size_override("font_size", 13)
	lab.add_theme_color_override("font_color", Color(0.55, 0.2, 0.15))
	lab.add_theme_color_override("font_outline_color", Color(1, 0.95, 0.8))
	lab.add_theme_constant_override("outline_size", 3)
	add_child(lab)
	var board := preload("res://scenes/interact_zone.tscn").instantiate()
	board.prompt_text = "按 E 看镇告示栏"
	board.mode = "bulletin"
	board.position = Vector2(90, 74) * TS
	add_child(board)
	# Soft mid-map path flowers between farm ↔ town
	for x in range(50, 78, 3):
		_spr("res://assets/processed/flower_%d.png" % (x % 4), Vector2(x, 68 + (x % 5)), 3)

		_spr("res://assets/processed/bush.png", Vector2(x + 1, 72), 4)

func _quest_zone(step_id: String, label: String, tile: Vector2) -> void:
	var z := preload("res://scenes/interact_zone.tscn").instantiate()
	z.prompt_text = "按 E 打卡·%s" % label
	z.mode = "quest_zone"
	z.quest_step_id = step_id
	z.message = "打卡：%s" % label
	z.position = tile * TS
	add_child(z)

func _ambient() -> void:
	for origin in [Vector2(40, 86), Vector2(78, 48), Vector2(102, 48), Vector2(90, 60), Vector2(142, 12), Vector2(174, 100)]:
		_spawn_smoke(origin * TS)
	_spawn_ripples(Vector2(155, 108) * TS)
	_spawn_ripples(Vector2(28, 50) * TS)
	_spawn_waterfall_mist(Vector2(24, 16) * TS)
	_spawn_waterfall_mist(Vector2(24, 20) * TS)
	_spawn_waterfall_mist(Vector2(22, 18) * TS)
	_sway_trees()

func _spawn_smoke(at: Vector2) -> void:
	var p := CPUParticles2D.new()
	p.position = at + Vector2(8, -28)
	p.amount = 16
	p.lifetime = 2.4
	p.emission_shape = CPUParticles2D.EMISSION_SHAPE_SPHERE
	p.emission_sphere_radius = 3.0
	p.direction = Vector2(0, -1)
	p.spread = 22.0
	p.gravity = Vector2(0, -10)
	p.initial_velocity_min = 10.0
	p.initial_velocity_max = 22.0
	p.scale_amount_min = 0.5
	p.scale_amount_max = 1.4
	p.color = Color(0.85, 0.85, 0.88, 0.55)
	p.z_index = 12
	add_child(p)

func _spawn_ripples(at: Vector2) -> void:
	var p := CPUParticles2D.new()
	p.position = at
	p.amount = 14
	p.lifetime = 2.8
	p.emission_shape = CPUParticles2D.EMISSION_SHAPE_SPHERE
	p.emission_sphere_radius = 18.0
	p.direction = Vector2(0, 0)
	p.spread = 180.0
	p.gravity = Vector2.ZERO
	p.initial_velocity_min = 3.0
	p.initial_velocity_max = 8.0
	p.scale_amount_min = 0.4
	p.scale_amount_max = 1.3
	p.color = Color(0.7, 0.85, 1.0, 0.4)
	p.z_index = 2
	add_child(p)

func _spawn_waterfall_mist(at: Vector2) -> void:
	for i in range(3):
		var p := CPUParticles2D.new()
		p.position = at + Vector2(float(i - 1) * 10.0, 18.0 + float(i) * 8.0)
		p.amount = 36
		p.lifetime = 1.8
		p.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
		p.emission_rect_extents = Vector2(14, 6)
		p.direction = Vector2(0.05, 1)
		p.spread = 28.0
		p.gravity = Vector2(0, 28)
		p.initial_velocity_min = 28.0
		p.initial_velocity_max = 55.0
		p.scale_amount_min = 0.7
		p.scale_amount_max = 2.0
		p.color = Color(0.85, 0.93, 1.0, 0.5)
		p.z_index = 10
		add_child(p)
	# Soft spray at pool base
	var spray := CPUParticles2D.new()
	spray.position = at + Vector2(0, 48)
	spray.amount = 22
	spray.lifetime = 1.2
	spray.emission_shape = CPUParticles2D.EMISSION_SHAPE_SPHERE
	spray.emission_sphere_radius = 14.0
	spray.direction = Vector2(0, -1)
	spray.spread = 70.0
	spray.gravity = Vector2(0, 8)
	spray.initial_velocity_min = 8.0
	spray.initial_velocity_max = 22.0
	spray.scale_amount_min = 0.5
	spray.scale_amount_max = 1.4
	spray.color = Color(0.9, 0.96, 1.0, 0.4)
	spray.z_index = 9
	add_child(spray)

func _sway_trees() -> void:
	for c in get_children():
		if c is Sprite2D and c.has_meta("sway") and bool(c.get_meta("sway")):
			var tw := c.create_tween().set_loops()
			var soft := c.has_meta("sway_soft") and bool(c.get_meta("sway_soft"))
			var amp := randf_range(0.6, 1.6) if soft else randf_range(1.2, 3.2)
			var dur := randf_range(1.4, 2.4) if soft else randf_range(1.8, 3.0)
			tw.tween_property(c, "rotation_degrees", amp, dur).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
			tw.tween_property(c, "rotation_degrees", -amp, dur).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
