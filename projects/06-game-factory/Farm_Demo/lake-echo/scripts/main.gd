extends Node2D
## Main entry — camera limits + spawn at farm.

func _ready() -> void:
	var world := $World
	var player := $Player
	if world.has_method("world_size"):
		var sz: Vector2 = world.world_size()
		var cam := player.get_node("Camera2D") as Camera2D
		cam.limit_left = 0
		cam.limit_top = 0
		cam.limit_right = int(sz.x)
		cam.limit_bottom = int(sz.y)
		cam.zoom = Vector2(2, 2)
	var spawn := GameBus.consume_spawn()
	if spawn != Vector2.ZERO:
		player.global_position = spawn
	else:
		player.global_position = Vector2(40 * 16, 90 * 16)
	GameBus.show_toast("Lake Echo Wave0：六区底图已铺，可 WASD 探索")
