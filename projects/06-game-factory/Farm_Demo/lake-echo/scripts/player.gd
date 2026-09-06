extends CharacterBody2D
## Player — atlas rows: down, left, right, up (48px).

@export var speed: float = 130.0
@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var camera: Camera2D = $Camera2D

const CELL := 48
const DIRS := ["down", "left", "right", "up"]

var facing: Vector2 = Vector2.DOWN
var _facing_name: String = "down"
var _prompt: String = ""
var _interact_cb: Callable = Callable()

func _ready() -> void:
	add_to_group("player")
	_setup_frames()
	camera.make_current()
	camera.zoom = Vector2(2, 2)
	camera.position_smoothing_enabled = false
	anim.play("idle_down")

func _setup_frames() -> void:
	var tex := load("res://assets/processed/player.png") as Texture2D
	var frames := SpriteFrames.new()
	var cols := maxi(int(tex.get_width() / float(CELL)), 1)
	var rows := maxi(int(tex.get_height() / float(CELL)), 1)
	for ri in range(mini(rows, DIRS.size())):
		var d: String = DIRS[ri]
		var walk_name := "walk_%s" % d
		var idle_name := "idle_%s" % d
		frames.add_animation(walk_name)
		frames.add_animation(idle_name)
		frames.set_animation_speed(walk_name, 10.0)
		frames.set_animation_loop(walk_name, true)
		frames.set_animation_speed(idle_name, 1.0)
		frames.set_animation_loop(idle_name, true)
		for ci in range(cols):
			var at := AtlasTexture.new()
			at.atlas = tex
			at.region = Rect2(ci * CELL, ri * CELL, CELL, CELL)
			frames.add_frame(walk_name, at)
			if ci == 0:
				frames.add_frame(idle_name, at)
	anim.sprite_frames = frames
	anim.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST

func _dir_name_from_vec(v: Vector2) -> String:
	if absf(v.x) > absf(v.y):
		return "left" if v.x < 0.0 else "right"
	return "up" if v.y < 0.0 else "down"

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

func _physics_process(_delta: float) -> void:
	if GameBus.inventory_open or GameBus.dialogue_open:
		velocity = Vector2.ZERO
		move_and_slide()
		return
	var dir := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	if dir.length() > 0.1:
		facing = dir.normalized()
		_facing_name = _dir_name_from_vec(facing)
		velocity = facing * speed
		var walk_anim := "walk_%s" % _facing_name
		if anim.animation != walk_anim:
			anim.play(walk_anim)
	else:
		velocity = Vector2.ZERO
		var idle_anim := "idle_%s" % _facing_name
		if anim.animation != idle_anim:
			anim.play(idle_anim)
	move_and_slide()
	global_position.x = clampf(global_position.x, 8.0, float(192 * 16) - 8.0)
	global_position.y = clampf(global_position.y, 8.0, float(128 * 16) - 8.0)
	if Input.is_action_just_pressed("interact"):
		try_interact()
	if Input.is_action_just_pressed("inventory"):
		GameBus.inventory_open = not GameBus.inventory_open
		GameBus.show_toast("背包暂未接入 UI（Wave1+）" if GameBus.inventory_open else "关闭背包")
