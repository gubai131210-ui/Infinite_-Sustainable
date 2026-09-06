extends Node2D
## Differentiated interiors (P10) — layout/palette/props per GameBus.current_interior_id.

const TS := 16
const IW := 18
const IH := 12

const ROOM_PALETTE := {
	"farmhouse": {"floor": Color(0.72, 0.58, 0.42), "wall": Color(0.55, 0.42, 0.32), "tint": Color(1.05, 0.98, 0.92)},
	"barn": {"floor": Color(0.55, 0.42, 0.28), "wall": Color(0.4, 0.3, 0.2), "tint": Color(1.0, 0.95, 0.85)},
	"shop": {"floor": Color(0.62, 0.55, 0.48), "wall": Color(0.45, 0.5, 0.55), "tint": Color(1.0, 1.0, 1.05)},
	"cafe": {"floor": Color(0.5, 0.38, 0.32), "wall": Color(0.42, 0.28, 0.25), "tint": Color(1.08, 0.95, 0.9)},
	"station": {"floor": Color(0.45, 0.48, 0.52), "wall": Color(0.35, 0.38, 0.45), "tint": Color(0.95, 0.98, 1.05)},
	"lighthouse": {"floor": Color(0.4, 0.42, 0.5), "wall": Color(0.3, 0.32, 0.42), "tint": Color(0.9, 0.95, 1.1)},
}

func _ready() -> void:
	_build_room()
	var player := $Player
	player.global_position = Vector2(9 * TS, 9 * TS)
	var cam := player.get_node("Camera2D") as Camera2D
	cam.limit_left = 0
	cam.limit_top = 0
	cam.limit_right = IW * TS
	cam.limit_bottom = IH * TS
	cam.zoom = Vector2(2, 2)
	cam.make_current()
	if player.has_method("set_farm"):
		player.set_farm(null)
	$ExitZone.prompt_text = "按 E 离开%s" % GameBus.current_interior_title
	_configure_zones()
	_modulate_room()
	GameBus.show_toast("%s：按 E 交互，门口可离开" % GameBus.current_interior_title)

func _configure_zones() -> void:
	var id := GameBus.current_interior_id
	var show_bed := id == "farmhouse"
	$BedZone.visible = show_bed
	$BedZone.monitoring = show_bed
	match id:
		"farmhouse":
			$ChestZone.position = Vector2(12 * TS, 4 * TS)
			$ChestZone.visible = true
		"barn":
			$ChestZone.position = Vector2(4 * TS, 4 * TS)
			$ChestZone.visible = true
		"shop":
			$ChestZone.position = Vector2(15 * TS, 8 * TS)
			$ChestZone.visible = true
		"lighthouse":
			$ChestZone.position = Vector2(13 * TS, 8 * TS)
			$ChestZone.visible = true
		_:
			$ChestZone.visible = false
	$ChestZone.monitoring = $ChestZone.visible
	if id == "shop":
		_zone("shop_sell", "按 E 卖出作物", Vector2(8 * TS, 6 * TS))
		_zone("shop_buy", "按 E 买种子礼包(30金)", Vector2(11 * TS, 6 * TS))
	elif id == "cafe":
		var z := preload("res://scenes/interact_zone.tscn").instantiate()
		z.prompt_text = "按 E 点一杯热可可（+10 精力）"
		z.mode = "stamina_sip"
		z.stamina_restore = 10
		z.message = "热可可暖手，精力 +10"
		z.position = Vector2(9 * TS, 5 * TS)
		add_child(z)

func _zone(mode: String, prompt: String, pos: Vector2) -> void:
	var z := preload("res://scenes/interact_zone.tscn").instantiate()
	z.prompt_text = prompt
	z.mode = mode
	z.position = pos
	add_child(z)

func _modulate_room() -> void:
	var pal: Dictionary = ROOM_PALETTE.get(GameBus.current_interior_id, ROOM_PALETTE["farmhouse"])
	modulate = pal["tint"]

func _build_room() -> void:
	var id := GameBus.current_interior_id
	var pal: Dictionary = ROOM_PALETTE.get(id, ROOM_PALETTE["farmhouse"])
	var floor_tex := _solid_tile(pal["floor"])
	var wall_tex := _solid_tile(pal["wall"])
	# Prefer baked tiles if present, then tint
	var baked_floor := _load_tex("res://assets/processed/tile_indoor_floor.png")
	var baked_wall := _load_tex("res://assets/processed/tile_indoor_wall.png")
	var ground := $Ground
	for y in range(IH):
		for x in range(IW):
			var is_wall := y == 0 or y == IH - 1 or x == 0 or x == IW - 1
			var spr := Sprite2D.new()
			spr.texture = (baked_wall if baked_wall else wall_tex) if is_wall else (baked_floor if baked_floor else floor_tex)
			spr.modulate = pal["wall"] if is_wall else pal["floor"]
			if not is_wall and baked_floor:
				spr.modulate = pal["floor"]
			spr.centered = false
			spr.position = Vector2(x * TS, y * TS)
			spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
			ground.add_child(spr)
	_add_wall_body(Rect2(0, 0, IW * TS, TS))
	_add_wall_body(Rect2(0, (IH - 1) * TS, IW * TS, TS))
	_add_wall_body(Rect2(0, 0, TS, IH * TS))
	_add_wall_body(Rect2((IW - 1) * TS, 0, TS, IH * TS))
	_prop("res://assets/processed/prop_doormat.png", Vector2(9 * TS, 10 * TS))
	_title_label(GameBus.current_interior_title)
	match id:
		"farmhouse":
			_prop("res://assets/processed/prop_bed.png", Vector2(5 * TS, 4 * TS))
			_prop("res://assets/processed/chest.png", Vector2(12 * TS, 4 * TS))
			_prop("res://assets/processed/prop_lamp.png", Vector2(14 * TS, 3 * TS))
			_prop("res://assets/processed/prop_crate.png", Vector2(3 * TS, 7 * TS))
		"barn":
			_prop("res://assets/processed/prop_hay.png", Vector2(5 * TS, 5 * TS))
			_prop("res://assets/processed/prop_hay.png", Vector2(7 * TS, 6 * TS))
			_prop("res://assets/processed/prop_barrel.png", Vector2(11 * TS, 5 * TS))
			_prop("res://assets/processed/prop_crate.png", Vector2(13 * TS, 6 * TS))
			_prop("res://assets/processed/chest.png", Vector2(4 * TS, 4 * TS))
			_prop("res://assets/processed/tool_axe.png", Vector2(14 * TS, 4 * TS))
		"shop":
			_prop("res://assets/processed/prop_counter.png", Vector2(9 * TS, 5 * TS))
			_prop("res://assets/processed/prop_shelf.png", Vector2(4 * TS, 4 * TS))
			_prop("res://assets/processed/prop_shelf.png", Vector2(14 * TS, 4 * TS))
			_prop("res://assets/processed/prop_crate.png", Vector2(6 * TS, 7 * TS))
			_prop("res://assets/processed/prop_barrel.png", Vector2(12 * TS, 7 * TS))
			_prop("res://assets/processed/chest.png", Vector2(15 * TS, 8 * TS))
		"cafe":
			_prop("res://assets/processed/prop_counter.png", Vector2(9 * TS, 3 * TS))
			_prop("res://assets/processed/prop_table.png", Vector2(5 * TS, 6 * TS))
			_prop("res://assets/processed/prop_chair.png", Vector2(4 * TS, 7 * TS))
			_prop("res://assets/processed/prop_chair.png", Vector2(6 * TS, 7 * TS))
			_prop("res://assets/processed/prop_table.png", Vector2(13 * TS, 6 * TS))
			_prop("res://assets/processed/prop_chair.png", Vector2(12 * TS, 7 * TS))
			_prop("res://assets/processed/prop_chair.png", Vector2(14 * TS, 7 * TS))
			_prop("res://assets/processed/prop_lamp.png", Vector2(9 * TS, 8 * TS))
		"station":
			_prop("res://assets/processed/prop_bench.png", Vector2(5 * TS, 5 * TS))
			_prop("res://assets/processed/prop_bench.png", Vector2(9 * TS, 5 * TS))
			_prop("res://assets/processed/prop_bench.png", Vector2(13 * TS, 5 * TS))
			_prop("res://assets/processed/prop_crate.png", Vector2(4 * TS, 7 * TS))
			_prop("res://assets/processed/prop_barrel.png", Vector2(14 * TS, 7 * TS))
			_prop("res://assets/processed/prop_signboard.png", Vector2(9 * TS, 3 * TS))
		"lighthouse":
			_prop("res://assets/processed/prop_lamp.png", Vector2(9 * TS, 4 * TS))
			_prop("res://assets/processed/prop_lamp.png", Vector2(7 * TS, 6 * TS))
			_prop("res://assets/processed/prop_lamp.png", Vector2(11 * TS, 6 * TS))
			_prop("res://assets/processed/prop_barrel.png", Vector2(5 * TS, 8 * TS))
			_prop("res://assets/processed/chest.png", Vector2(13 * TS, 8 * TS))
			_prop("res://assets/processed/prop_rocks.png", Vector2(9 * TS, 7 * TS))
		_:
			_prop("res://assets/processed/prop_bed.png", Vector2(5 * TS, 4 * TS))
			_prop("res://assets/processed/chest.png", Vector2(12 * TS, 4 * TS))

func _title_label(text: String) -> void:
	var lab := Label.new()
	lab.text = text
	lab.position = Vector2(4 * TS, 1 * TS + 2)
	lab.z_index = 20
	lab.add_theme_font_size_override("font_size", 14)
	lab.add_theme_color_override("font_color", Color(0.95, 0.92, 0.85))
	lab.add_theme_color_override("font_outline_color", Color(0.1, 0.08, 0.05))
	lab.add_theme_constant_override("outline_size", 4)
	$Props.add_child(lab)

func _solid_tile(c: Color) -> Texture2D:
	var img := Image.create(TS, TS, false, Image.FORMAT_RGBA8)
	img.fill(c)
	return ImageTexture.create_from_image(img)

func _load_tex(path: String) -> Texture2D:
	if ResourceLoader.exists(path):
		var res := load(path)
		if res is Texture2D:
			return res
	var abs_path := ProjectSettings.globalize_path(path)
	var img := Image.new()
	if img.load(abs_path) == OK:
		return ImageTexture.create_from_image(img)
	return null

func _prop(path: String, pos: Vector2) -> void:
	var tex := _load_tex(path)
	if tex == null:
		return
	var spr := Sprite2D.new()
	spr.texture = tex
	spr.position = pos
	spr.centered = true
	spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	$Props.add_child(spr)

func _add_wall_body(r: Rect2) -> void:
	var body := StaticBody2D.new()
	body.position = r.position + r.size * 0.5
	var cs := CollisionShape2D.new()
	var shape := RectangleShape2D.new()
	shape.size = r.size
	cs.shape = shape
	body.add_child(cs)
	$Colliders.add_child(body)
