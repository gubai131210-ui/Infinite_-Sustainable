extends CharacterBody2D
## Wandering farm animal; feed with E. Scale by kind (chicken < sheep < cow < human).

@export var animal_kind: String = "chicken"
@export var display_name: String = "鸡"
@export var sprite_path: String = "res://assets/processed/chicken.png"

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var area: Area2D = $InteractArea

var _dir: Vector2 = Vector2.RIGHT
var _timer: float = 0.0
var _player_inside: Node = null
var _speed: float = 28.0

func _ready() -> void:
	add_to_group("animal")
	_setup_sprite()
	area.body_entered.connect(_on_enter)
	area.body_exited.connect(_on_exit)
	_timer = randf_range(0.5, 2.0)
	match animal_kind:
		"chicken":
			_speed = 36.0
		"sheep":
			_speed = 24.0
		"cow":
			_speed = 18.0
	anim.play("walk")

func _cell_size() -> int:
	match animal_kind:
		"chicken":
			return 20
		"sheep":
			return 28
		"cow":
			return 36
	return 20

func _setup_sprite() -> void:
	var tex := load(sprite_path) as Texture2D
	var frames := SpriteFrames.new()
	frames.add_animation("idle")
	frames.add_animation("walk")
	frames.set_animation_speed("idle", 4.0)
	frames.set_animation_loop("idle", true)
	frames.set_animation_speed("walk", 8.0)
	frames.set_animation_loop("walk", true)
	var cell := _cell_size()
	var n := int(tex.get_width() / float(cell))
	n = maxi(n, 1)
	for i in range(n):
		var at := AtlasTexture.new()
		at.atlas = tex
		at.region = Rect2(i * cell, 0, cell, cell)
		frames.add_frame("walk", at)
		if i == 0 or i == 1:
			frames.add_frame("idle", at)
	anim.sprite_frames = frames
	anim.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST

func _physics_process(delta: float) -> void:
	_timer -= delta
	if _timer <= 0.0:
		_timer = randf_range(1.0, 3.0)
		var opts := [Vector2.LEFT, Vector2.RIGHT, Vector2.UP, Vector2.DOWN, Vector2.ZERO]
		_dir = opts[randi() % opts.size()]
	velocity = _dir * _speed
	anim.flip_h = _dir.x < 0.0
	if _dir.length() > 0.1:
		if anim.animation != "walk":
			anim.play("walk")
	else:
		if anim.animation != "idle":
			anim.play("idle")
	move_and_slide()

func _on_enter(body: Node2D) -> void:
	if body.is_in_group("player") and body.has_method("set_interact_prompt"):
		_player_inside = body
		body.set_interact_prompt("按 E 喂%s" % display_name, Callable(self, "_feed"))

func _on_exit(body: Node2D) -> void:
	if body == _player_inside and body.has_method("clear_interact_prompt"):
		body.clear_interact_prompt()
		_player_inside = null

func _feed() -> void:
	if Inventory.remove("feed", 1):
		GameBus.show_toast("%s吃得很开心！" % display_name)
	else:
		GameBus.show_toast("没有饲料了")
