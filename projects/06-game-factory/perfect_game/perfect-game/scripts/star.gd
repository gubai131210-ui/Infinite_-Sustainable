extends Area2D
## Collectible paper star.

signal collected

@onready var sprite: Sprite2D = $Sprite2D

var _taken: bool = false

func _ready() -> void:
	var tex := load("res://assets/processed/star.png") as Texture2D
	if tex:
		sprite.texture = tex
	body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node2D) -> void:
	if _taken:
		return
	if body.is_in_group("player"):
		_taken = true
		collected.emit()
		queue_free()
