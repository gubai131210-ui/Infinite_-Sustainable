extends Node2D
## Main entry — camera limits + spawn + optional golden capture.

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
	GameBus.show_toast("Lake Echo：六区可探索，农舍可进，空格锄地")
	if "--capture_golden" in OS.get_cmdline_user_args():
		await _capture_goldens(player)

func _capture_goldens(player: Node2D) -> void:
	await get_tree().process_frame
	await get_tree().process_frame
	DirAccess.make_dir_recursive_absolute("res://assets/qa/golden_r5")
	var shots := [
		["01_farm", Vector2(40 * 16, 98 * 16)],
		["02_river", Vector2(28 * 16, 28 * 16)],
		["03_town", Vector2(90 * 16, 48 * 16)],
		["04_station", Vector2(155 * 16, 18 * 16)],
		["05_terrace", Vector2(142 * 16, 48 * 16)],
		["06_lake", Vector2(168 * 16, 105 * 16)],
		["00_overview", Vector2(100 * 16, 64 * 16)],
	]
	var cam := player.get_node("Camera2D") as Camera2D
	for s in shots:
		player.global_position = s[1]
		# Overview needs pull-back to show six-zone topology
		if str(s[0]) == "00_overview":
			cam.zoom = Vector2(0.38, 0.38)
		else:
			cam.zoom = Vector2(2, 2)
		await get_tree().process_frame
		await get_tree().create_timer(0.2).timeout
		var img: Image = get_viewport().get_texture().get_image()
		var path := "res://assets/qa/golden_r5/%s.png" % str(s[0])
		img.save_png(path)
		print("GOLDEN_SAVED ", path)
	print("GOLDEN_CAPTURE_DONE")
	await get_tree().create_timer(0.3).timeout
	get_tree().quit()
