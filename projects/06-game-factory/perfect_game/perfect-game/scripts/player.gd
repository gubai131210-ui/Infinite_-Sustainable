extends CharacterBody2D
## Paper Isle player — move, select prop, interact.

@export var speed: float = 150.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var camera: Camera2D = $Camera2D

var _bob_t: float = 0.0

func _ready() -> void:
	add_to_group("player")
	var tex := load("res://assets/processed/player.png") as Texture2D
	if tex:
		sprite.texture = tex
		sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	camera.make_current()

func _physics_process(delta: float) -> void:
	var dir := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	velocity = dir * speed
	move_and_slide()
	if absf(dir.x) > 0.01:
		sprite.flip_h = dir.x < 0.0
	if dir.length() > 0.1:
		_bob_t += delta * 10.0
		sprite.position.y = -20.0 + sin(_bob_t) * 2.5
	else:
		sprite.position.y = -20.0

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("select_lantern"):
		GameState.set_selected("lantern")
	elif event.is_action_pressed("select_flowers"):
		GameState.set_selected("flowers")
	elif event.is_action_pressed("interact"):
		_try_interact()

func _try_interact() -> void:
	# Prefer fox greet, then nearest pad
	for n in get_tree().get_nodes_in_group("fox"):
		if n.has_method("try_greet") and n.call("try_greet"):
			_cam_punch()
			return
	for n in get_tree().get_nodes_in_group("decor_pad"):
		if n.has_method("try_place") and n.call("try_place"):
			_cam_punch()
			return

func _cam_punch() -> void:
	var tw := create_tween()
	tw.tween_property(camera, "zoom", Vector2(1.32, 1.32), 0.08)
	tw.tween_property(camera, "zoom", Vector2(1.25, 1.25), 0.12)
