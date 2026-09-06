extends Node2D
## Farmhouse interior: bed, chest, exit door.

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
	GameBus.show_toast("农舍内：床可休息，箱子可拿物资，门口离开")

func _build_room() -> void:
	var floor_tex: Texture2D = load("res://assets/processed/tile_indoor_floor.png")
	var wall_tex: Texture2D = load("res://assets/processed/tile_indoor_wall.png")
	var ground := $Ground
	for y in range(IH):
		for x in range(IW):
			var spr := Sprite2D.new()
			spr.texture = wall_tex if y == 0 or y == IH - 1 or x == 0 or x == IW - 1 else floor_tex
			spr.centered = false
			spr.position = Vector2(x * TS, y * TS)
			spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
			ground.add_child(spr)
	# walls collision
	_add_wall_body(Rect2(0, 0, IW * TS, TS))
	_add_wall_body(Rect2(0, (IH - 1) * TS, IW * TS, TS))
	_add_wall_body(Rect2(0, 0, TS, IH * TS))
	_add_wall_body(Rect2((IW - 1) * TS, 0, TS, IH * TS))

	var bed_spr := Sprite2D.new()
	bed_spr.texture = load("res://assets/processed/prop_bed.png")
	bed_spr.position = Vector2(5 * TS, 4 * TS)
	bed_spr.centered = true
	bed_spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	$Props.add_child(bed_spr)

	var chest_spr := Sprite2D.new()
	chest_spr.texture = load("res://assets/processed/chest.png")
	chest_spr.position = Vector2(12 * TS, 4 * TS)
	chest_spr.centered = true
	chest_spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	$Props.add_child(chest_spr)

	var mat := Sprite2D.new()
	mat.texture = load("res://assets/processed/prop_doormat.png")
	mat.position = Vector2(9 * TS, 10 * TS)
	mat.centered = true
	mat.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	$Props.add_child(mat)

func _add_wall_body(r: Rect2) -> void:
	var body := StaticBody2D.new()
	body.position = r.position + r.size * 0.5
	var cs := CollisionShape2D.new()
	var shape := RectangleShape2D.new()
	shape.size = r.size
	cs.shape = shape
	body.add_child(cs)
	$Colliders.add_child(body)
