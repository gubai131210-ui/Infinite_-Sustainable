extends CharacterBody2D
## Wandering farm animal — feed then collect egg/wool/milk.

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
var _product_ready: bool = false
var _fed_today: bool = false

func _ready() -> void:
	add_to_group("animal")
	y_sort_enabled = true
	z_as_relative = true
	_home = global_position
	_anim_base_y = anim.position.y
	_bob_t = randf() * TAU
	_setup_sprite()
	_setup_shadow()
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
	if not TimeClock.day_changed.is_connected(_on_new_day):
		TimeClock.day_changed.connect(_on_new_day)

func _on_new_day(_day: int) -> void:
	_fed_today = false
	# Uncollected product stays; new day can still feed again after collect

func _product_id() -> String:
	match animal_kind:
		"chicken":
			return "egg"
		"sheep":
			return "wool"
		"cow":
			return "milk"
	return "egg"

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

func _setup_shadow() -> void:
	var shadow := Polygon2D.new()
	shadow.name = "GroundShadow"
	shadow.z_index = -1
	shadow.color = Color(0.08, 0.08, 0.12, 0.28)
	var sw := 6.0 if animal_kind == "chicken" else (9.0 if animal_kind == "sheep" else 11.0)
	var pts := PackedVector2Array()
	for i in range(10):
		var a := TAU * float(i) / 10.0
		pts.append(Vector2(cos(a) * sw, sin(a) * (sw * 0.35) + 4.0))
	shadow.polygon = pts
	add_child(shadow)

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

func _prompt_text() -> String:
	if _product_ready:
		return "按 E 收取%s产出" % display_name
	return "按 E 喂%s" % display_name

func _refresh_prompt() -> void:
	if _player_inside != null and _player_inside.has_method("set_interact_prompt"):
		_player_inside.set_interact_prompt(_prompt_text(), Callable(self, "_interact"))

func _on_enter(body: Node2D) -> void:
	if body.is_in_group("player") and body.has_method("set_interact_prompt"):
		_player_inside = body
		_refresh_prompt()

func _on_exit(body: Node2D) -> void:
	if body == _player_inside and body.has_method("clear_interact_prompt"):
		body.clear_interact_prompt()
		_player_inside = null

func _interact() -> void:
	if _product_ready:
		var pid := _product_id()
		Inventory.add(pid, 1)
		_product_ready = false
		GameBus.show_toast("获得%s！" % ItemDB.display_name(pid))
		_refresh_prompt()
		return
	if _fed_today:
		GameBus.show_toast("%s今天已经喂过了" % display_name)
		return
	if Inventory.remove("feed", 1):
		_fed_today = true
		_product_ready = true
		GameBus.show_toast("%s吃得很开心，可以收取了！" % display_name)
		_refresh_prompt()
	else:
		GameBus.show_toast("没有饲料了")
