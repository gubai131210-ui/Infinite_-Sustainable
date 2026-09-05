extends CharacterBody2D

@export var speed: float = 220.0
@export var gravity: float = 1400.0
@export var min_x: float = 120.0
@export var max_x: float = 1100.0

@onready var sprite: Sprite2D = $Sprite2D

var _prompt: String = ""
var _interact_cb: Callable = Callable()

func _ready() -> void:
	floor_snap_length = 8.0
	safe_margin = 0.08
	Input.action_release("move_left")
	Input.action_release("move_right")
	Input.action_release("interact")

func set_interact_prompt(text: String, cb: Callable = Callable()) -> void:
	_prompt = text
	_interact_cb = cb

func clear_interact_prompt() -> void:
	_prompt = ""
	_interact_cb = Callable()

func get_interact_prompt() -> String:
	return _prompt

func try_interact() -> bool:
	if _interact_cb.is_valid():
		_interact_cb.call()
		return true
	return false

func _physics_process(delta: float) -> void:
	var direction := Input.get_axis("move_left", "move_right")
	velocity.x = direction * speed
	if not is_on_floor():
		velocity.y = minf(velocity.y + gravity * delta, 1200.0)
	else:
		velocity.y = 0.0
	if absf(direction) > 0.01:
		sprite.flip_h = direction < 0.0
	move_and_slide()
	global_position.x = clampf(global_position.x, min_x, max_x)
	if Input.is_action_just_pressed("interact"):
		try_interact()
