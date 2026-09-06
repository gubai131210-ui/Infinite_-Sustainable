extends Node2D
## Main entry: camera limits, spawn, integer zoom.

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
		# Integer zoom for crisp pixels (Goal R3)
		cam.zoom = Vector2(2, 2)
		cam.position_smoothing_enabled = false
	var spawn := GameBus.consume_spawn()
	if spawn != Vector2.ZERO:
		player.global_position = spawn
	else:
		player.global_position = Vector2(10 * 16, 22 * 16)
	GameBus.show_toast("欢迎来到村口农场！北有山阶，东有广场，南有牧场")
