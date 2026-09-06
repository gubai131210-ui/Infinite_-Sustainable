extends Node2D
## Main: World + Player + HUD.

@onready var world: Node2D = $World
@onready var hud: CanvasLayer = $HUD

func _ready() -> void:
	if world.has_method("bind_hud"):
		world.call("bind_hud", hud)
	var player := $World/Entities/Player as Node2D
	if player:
		player.position = Vector2(14 * 64, 12 * 64)
