extends CharacterBody2D
## Paper Isle player — static papercraft sprite, top-down move.

@export var speed: float = 140.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var camera: Camera2D = $Camera2D

func _ready() -> void:
	add_to_group("player")
	var tex := load("res://assets/processed/player.png") as Texture2D
	if tex:
		sprite.texture = tex
		sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	camera.make_current()

func _physics_process(_delta: float) -> void:
	var dir := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	velocity = dir * speed
	move_and_slide()
	if absf(dir.x) > 0.01:
		sprite.flip_h = dir.x < 0.0
