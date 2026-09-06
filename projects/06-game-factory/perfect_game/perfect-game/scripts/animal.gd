extends CharacterBody2D
## Wandering farm animal with walk cycle + bob. Feed with E.

@export var animal_kind: String = "chicken"
@export var display_name: String = "鸡"
@export var sprite_path: String = "res://assets/processed/chicken.png"

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var area: Area2D = $InteractArea

var _dir: Vector2 = Vector2.RIGHT
var _timer: float = 0.0
var _player_inside: Node = null
var _speed: float = 28.0
var _home: Vector2 = Vector2.ZERO
var _bob_t: float = 0.0
var _anim_base_y: float = -6.0

func _ready() -> void:
	add_to_group("animal")
	_home = global_position
	_anim_base_y = anim.position.y
	_bob_t = randf() * TAU
	_setup_sprite()
	area.body_entered.connect(_on_enter)
	area.body_exited.connect(_on_exit)
	_timer = randf_range(0.5, 2.0)
	match animal_kind:
		"chicken":
			_speed = 40.0
			display_name = "鸡"
		"sheep":
			_speed = 26.0
			display_name = "羊"
		"cow":
			_speed = 18.0
			display_name = "牛"
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
	var tex: Texture2D = null
	if ResourceLoader.exists(sprite_path):
		var res := load(sprite_path)
		if res is Texture2D:
			tex = res
	if tex == null:
		var abs_path := ProjectSettings.globalize_path(sprite_path)
		var img := Image.new()
		if img.load(abs_path) != OK:
			push_warning("animal missing: %s" % sprite_path)
			return
		tex = ImageTexture.create_from_image(img)
	var frames := SpriteFrames.new()
	frames.add_animation("idle")
	frames.add_animation("walk")
	frames.set_animation_speed("idle", 3.0)
	frames.set_animation_loop("idle", true)
	frames.set_animation_speed("walk", 9.0)
	frames.set_animation_loop("walk", true)
	var cell := _cell_size()
	# Horizontal strip: frame height = sheet height if not square
	var fh := tex.get_height()
	var fw := cell
	if fh > 0 and fh < cell:
		fw = fh
	var n := maxi(int(tex.get_width() / float(fw)), 1)
	for i in range(n):
		var at := AtlasTexture.new()
		at.atlas = tex
		at.region = Rect2(i * fw, 0, fw, fh)
		frames.add_frame("walk", at)
		if i == 0 or i == mini(1, n - 1):
			frames.add_frame("idle", at)
	anim.sprite_frames = frames
	anim.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST

func _physics_process(delta: float) -> void:
	_timer -= delta
	if _timer <= 0.0:
		_timer = randf_range(0.8, 2.4)
		var opts := [Vector2.LEFT, Vector2.RIGHT, Vector2.UP, Vector2.DOWN, Vector2.ZERO, Vector2.LEFT, Vector2.RIGHT]
		_dir = opts[randi() % opts.size()]
	if global_position.distance_to(_home) > 40.0:
		_dir = (_home - global_position).normalized()
	velocity = _dir * _speed
	var moving := _dir.length() > 0.1
	if absf(_dir.x) > 0.05:
		anim.flip_h = _dir.x < 0.0
	if moving:
		if anim.animation != "walk" or not anim.is_playing():
			anim.play("walk")
		_bob_t += delta * 14.0
		anim.position.y = _anim_base_y + sin(_bob_t) * 1.2
	else:
		if anim.animation != "idle" or not anim.is_playing():
			anim.play("idle")
		_bob_t += delta * 2.0
		anim.position.y = _anim_base_y + sin(_bob_t) * 0.4
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
