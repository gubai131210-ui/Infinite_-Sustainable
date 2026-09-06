extends CharacterBody2D
## Ambient NPC with real side-view walk strip (flip_h for left).

@export var npc_id: String = "ahe"
@export var display_name: String = "阿禾"
@export var line: String = "地要勤锄，苗才肯长。"
@export var sprite_path: String = "res://assets/processed/npc_ahe.png"

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var area: Area2D = $InteractArea

const CELL := 48

var _dir: Vector2 = Vector2.RIGHT
var _timer: float = 0.0
var _player_inside: Node = null
var _home: Vector2 = Vector2.ZERO

func _ready() -> void:
	add_to_group("npc")
	_home = global_position
	_setup_sprite()
	area.body_entered.connect(_on_enter)
	area.body_exited.connect(_on_exit)
	_timer = randf_range(0.8, 2.2)
	anim.play("idle")

func _setup_sprite() -> void:
	var abs_path := ProjectSettings.globalize_path(sprite_path)
	var img := Image.new()
	if img.load(abs_path) != OK:
		push_warning("NPC missing sprite: %s" % sprite_path)
		return
	var tex := ImageTexture.create_from_image(img)
	var frames := SpriteFrames.new()
	frames.add_animation("idle")
	frames.add_animation("walk")
	frames.set_animation_speed("idle", 1.0)
	frames.set_animation_loop("idle", true)
	frames.set_animation_speed("walk", 8.0)
	frames.set_animation_loop("walk", true)
	var cell_w := CELL
	if tex.get_height() > 0 and tex.get_height() < CELL:
		cell_w = tex.get_height()
	var n := maxi(int(tex.get_width() / float(cell_w)), 1)
	for i in range(n):
		var at := AtlasTexture.new()
		at.atlas = tex
		at.region = Rect2(i * cell_w, 0, cell_w, tex.get_height())
		frames.add_frame("walk", at)
		if i == 0:
			frames.add_frame("idle", at)
	anim.sprite_frames = frames
	anim.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST

func _physics_process(delta: float) -> void:
	_timer -= delta
	if _timer <= 0.0:
		_timer = randf_range(1.2, 3.0)
		var opts := [Vector2.LEFT, Vector2.RIGHT, Vector2.ZERO, Vector2.ZERO]
		_dir = opts[randi() % opts.size()]
	velocity = _dir * 22.0
	# leash near home
	if global_position.distance_to(_home) > 48.0 and _dir != Vector2.ZERO:
		_dir = (_home - global_position).normalized()
		_dir.x = signf(_dir.x)
		_dir.y = 0.0
		velocity = _dir * 22.0
	if absf(_dir.x) > 0.1:
		anim.flip_h = _dir.x < 0.0
		if anim.animation != "walk":
			anim.play("walk")
	else:
		if anim.animation != "idle":
			anim.play("idle")
	move_and_slide()

func _on_enter(body: Node2D) -> void:
	if body.is_in_group("player") and body.has_method("set_interact_prompt"):
		_player_inside = body
		body.set_interact_prompt("按 E 与%s交谈" % display_name, Callable(self, "_talk"))

func _on_exit(body: Node2D) -> void:
	if body == _player_inside and body.has_method("clear_interact_prompt"):
		body.clear_interact_prompt()
		_player_inside = null

func _talk() -> void:
	GameBus.show_dialogue(display_name, line)
