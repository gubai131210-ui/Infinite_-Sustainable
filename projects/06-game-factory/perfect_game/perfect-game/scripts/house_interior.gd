extends Node2D
## Interior room — title from GameBus.current_interior_*.

const TS := 16
const IW := 18
const IH := 12

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
	var show_bed := GameBus.current_interior_id == "farmhouse"
	$BedZone.visible = show_bed
	$BedZone.monitoring = show_bed
	$ChestZone.visible = GameBus.current_interior_id in ["farmhouse", "barn", "shop"]
	$ChestZone.monitoring = $ChestZone.visible
	GameBus.show_toast("%s：按 E 交互，门口可离开" % GameBus.current_interior_title)

func _build_room() -> void:
	var floor_tex: Texture2D = _load_tex("res://assets/processed/tile_indoor_floor.png")
	var wall_tex: Texture2D = _load_tex("res://assets/processed/tile_indoor_wall.png")
	var ground := $Ground
	for y in range(IH):
		for x in range(IW):
			var spr := Sprite2D.new()
			spr.texture = wall_tex if y == 0 or y == IH - 1 or x == 0 or x == IW - 1 else floor_tex
			spr.centered = false
			spr.position = Vector2(x * TS, y * TS)
			spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
			ground.add_child(spr)
	_add_wall_body(Rect2(0, 0, IW * TS, TS))
	_add_wall_body(Rect2(0, (IH - 1) * TS, IW * TS, TS))
	_add_wall_body(Rect2(0, 0, TS, IH * TS))
	_add_wall_body(Rect2((IW - 1) * TS, 0, TS, IH * TS))

	_prop("res://assets/processed/prop_bed.png", Vector2(5 * TS, 4 * TS))
	_prop("res://assets/processed/chest.png", Vector2(12 * TS, 4 * TS))
	_prop("res://assets/processed/prop_doormat.png", Vector2(9 * TS, 10 * TS))
	match GameBus.current_interior_id:
		"shop":
			_prop("res://assets/processed/prop_crate.png", Vector2(7 * TS, 5 * TS))
			_prop("res://assets/processed/prop_barrel.png", Vector2(10 * TS, 5 * TS))
		"cafe":
			_prop("res://assets/processed/prop_stall.png", Vector2(8 * TS, 5 * TS))
		"station":
			_prop("res://assets/processed/prop_crate.png", Vector2(6 * TS, 6 * TS))
		"lighthouse":
			_prop("res://assets/processed/prop_lamp.png", Vector2(9 * TS, 5 * TS))
		"barn":
			_prop("res://assets/processed/prop_barrel.png", Vector2(7 * TS, 6 * TS))
			_prop("res://assets/processed/prop_crate.png", Vector2(11 * TS, 6 * TS))

func _load_tex(path: String) -> Texture2D:
	if ResourceLoader.exists(path):
		return load(path) as Texture2D
	var img := Image.create(TS, TS, false, Image.FORMAT_RGBA8)
	img.fill(Color(0.55, 0.4, 0.28))
	return ImageTexture.create_from_image(img)

func _prop(path: String, pos: Vector2) -> void:
	if not ResourceLoader.exists(path):
		return
	var spr := Sprite2D.new()
	spr.texture = load(path)
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
