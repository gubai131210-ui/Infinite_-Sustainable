extends Node2D
## Main entry: wire camera limits after world ready.

func _ready() -> void:
	var field := $World/FarmField
	var player := $Player
	if field.has_method("world_size"):
		var sz: Vector2 = field.world_size()
		var cam := player.get_node("Camera2D") as Camera2D
		cam.limit_left = 0
		cam.limit_top = 0
		cam.limit_right = int(sz.x)
		cam.limit_bottom = int(sz.y)
		cam.zoom = Vector2(2.0, 2.0)
	player.global_position = Vector2(8 * 16, 18 * 16)
	GameBus.show_toast("欢迎来到农场 Demo！Tab 开背包，1 锄地，2 浇水")
