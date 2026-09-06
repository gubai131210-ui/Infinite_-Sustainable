extends Node2D
## Oakhaven main — camera, spawn, day/night modulate, rain FX, quest boot.

var _modulate: CanvasModulate
var _rain: CPUParticles2D

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
	_modulate = CanvasModulate.new()
	_modulate.color = TimeClock.modulate_for_period() * SeasonClock.world_tint()
	add_child(_modulate)
	_setup_rain(player)
	TimeClock.period_changed.connect(_on_period)
	TimeClock.hour_changed.connect(func(_d, _h): _refresh_modulate())
	SeasonClock.season_changed.connect(func(_s): _refresh_modulate())
	Weather.weather_changed.connect(_on_weather)
	_on_weather(Weather.weather)
	GameBus.show_toast("橡木湾：WASD 移动 · 1-4 工具 · E 交互 · Tab 背包 · 床睡觉")
	GameBus.set_quest_hint(QuestLog.current_hint())
	if "--capture_golden" in OS.get_cmdline_user_args():
		await _capture_goldens(player)

func _setup_rain(player: Node2D) -> void:
	_rain = CPUParticles2D.new()
	_rain.name = "RainFX"
	_rain.z_index = 80
	_rain.amount = 140
	_rain.lifetime = 0.85
	_rain.preprocess = 0.4
	_rain.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	_rain.emission_rect_extents = Vector2(220, 140)
	_rain.direction = Vector2(0.15, 1)
	_rain.spread = 8.0
	_rain.gravity = Vector2(0, 420)
	_rain.initial_velocity_min = 90.0
	_rain.initial_velocity_max = 160.0
	_rain.scale_amount_min = 1.0
	_rain.scale_amount_max = 2.2
	_rain.color = Color(0.75, 0.85, 1.0, 0.55)
	_rain.emitting = false
	player.add_child(_rain)
	_rain.position = Vector2(0, -40)

func _on_weather(w: String) -> void:
	if _rain != null:
		_rain.emitting = (w == "rain")
	_refresh_modulate()

func _refresh_modulate() -> void:
	if _modulate != null:
		var c := TimeClock.modulate_for_period() * SeasonClock.world_tint()
		if Weather.is_raining():
			c *= Color(0.78, 0.82, 0.92, 1.0)
		_modulate.color = c

func _on_period(_p: String) -> void:
	if _modulate != null:
		var tw := create_tween()
		var target := TimeClock.modulate_for_period() * SeasonClock.world_tint()
		if Weather.is_raining():
			target *= Color(0.78, 0.82, 0.92, 1.0)
		tw.tween_property(_modulate, "color", target, 1.2)

func _capture_goldens(player: Node2D) -> void:
	await get_tree().process_frame
	await get_tree().process_frame
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://assets/qa/golden"))
	var shots := [
		["01_farm", Vector2(40 * 16, 98 * 16)],
		["02_river", Vector2(28 * 16, 28 * 16)],
		["03_town", Vector2(90 * 16, 48 * 16)],
		["04_station", Vector2(155 * 16, 18 * 16)],
		["05_terrace", Vector2(142 * 16, 44 * 16)],
		["06_lake", Vector2(168 * 16, 105 * 16)],
		["00_overview", Vector2(100 * 16, 64 * 16)],
	]
	var cam := player.get_node("Camera2D") as Camera2D
	for s in shots:
		player.global_position = s[1]
		if str(s[0]) == "00_overview":
			cam.zoom = Vector2(0.38, 0.38)
		else:
			cam.zoom = Vector2(2, 2)
		await get_tree().process_frame
		await get_tree().create_timer(0.2).timeout
		var img: Image = get_viewport().get_texture().get_image()
		var path := "res://assets/qa/golden/%s.png" % str(s[0])
		img.save_png(path)
		print("GOLDEN_SAVED ", path)
	print("GOLDEN_CAPTURE_DONE")
	await get_tree().create_timer(0.3).timeout
	get_tree().quit()
