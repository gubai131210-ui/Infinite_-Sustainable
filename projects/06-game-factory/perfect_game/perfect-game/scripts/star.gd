extends Area2D
## Collectible paper star with bob + pop juice.

signal collected

@onready var sprite: Sprite2D = $Sprite2D

var _taken: bool = false
var _base_y: float = 0.0

func _ready() -> void:
	var tex := load("res://assets/processed/star.png") as Texture2D
	if tex:
		sprite.texture = tex
	_base_y = sprite.position.y
	body_entered.connect(_on_body_entered)
	set_process(true)

func _process(_delta: float) -> void:
	if _taken:
		return
	sprite.position.y = _base_y + sin(Time.get_ticks_msec() * 0.005 + global_position.x * 0.01) * 4.0
	sprite.rotation_degrees = sin(Time.get_ticks_msec() * 0.004) * 6.0

func _on_body_entered(body: Node2D) -> void:
	if _taken:
		return
	if body.is_in_group("player"):
		_taken = true
		set_process(false)
		collected.emit()
		var tw := create_tween()
		tw.tween_property(sprite, "scale", Vector2(1.6, 1.6), 0.12)
		tw.parallel().tween_property(sprite, "modulate:a", 0.0, 0.18)
		tw.tween_callback(queue_free)
