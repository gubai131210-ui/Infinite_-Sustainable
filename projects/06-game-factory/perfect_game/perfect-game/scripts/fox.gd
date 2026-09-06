extends CharacterBody2D
## Papercraft fox — appears after decorate, follows player, E to greet.

signal greeted

@onready var sprite: Sprite2D = $Sprite2D

var active: bool = false
var _greeted: bool = false
var _player: Node2D = null
var _near: bool = false

func _ready() -> void:
	visible = false
	set_physics_process(false)
	var tex_path := "res://assets/processed/fox.png"
	var tex: Texture2D = null
	if ResourceLoader.exists(tex_path):
		tex = load(tex_path) as Texture2D
	if tex == null:
		var img := Image.new()
		if img.load(tex_path) == OK:
			tex = ImageTexture.create_from_image(img)
	if tex:
		sprite.texture = tex
	$Area2D.body_entered.connect(_on_enter)
	$Area2D.body_exited.connect(_on_exit)

func activate(at: Vector2) -> void:
	global_position = at
	visible = true
	active = true
	set_physics_process(true)
	var tw := create_tween()
	sprite.scale = Vector2(0.2, 0.2)
	tw.tween_property(sprite, "scale", Vector2.ONE, 0.45).set_trans(Tween.TRANS_BACK)

func _physics_process(delta: float) -> void:
	if not active:
		return
	if _player == null:
		_player = get_tree().get_first_node_in_group("player") as Node2D
		return
	var to: Vector2 = _player.global_position - global_position
	var dist := to.length()
	if dist > 28.0:
		global_position += to.normalized() * 90.0 * delta
		sprite.flip_h = to.x < 0.0
	# soft bob
	sprite.position.y = -12.0 + sin(Time.get_ticks_msec() * 0.006) * 3.0

func _on_enter(body: Node2D) -> void:
	if body.is_in_group("player"):
		_near = true

func _on_exit(body: Node2D) -> void:
	if body.is_in_group("player"):
		_near = false

func try_greet() -> bool:
	if not active or _greeted or not _near:
		return false
	_greeted = true
	greeted.emit()
	GameState.greet_fox()
	var tw := create_tween()
	tw.tween_property(sprite, "rotation_degrees", -12.0, 0.12)
	tw.tween_property(sprite, "rotation_degrees", 12.0, 0.12)
	tw.tween_property(sprite, "rotation_degrees", 0.0, 0.12)
	return true
