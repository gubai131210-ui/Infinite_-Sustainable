extends CharacterBody2D
## Player — Stardew-like frame anims: walk legs + hoe/water/plant actions.

@export var speed: float = 130.0
@export var tile_size: int = 16
@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var camera: Camera2D = $Camera2D

enum Tool { HOE, CAN, AXE, ROD }

const CELL := 48
## Sheet rows: walk D/L/R/U, hoe D/L/R/U, water D/L/R/U, plant D/L/R/U
const DIRS := ["down", "left", "right", "up"]

var tool: Tool = Tool.HOE
var facing: Vector2 = Vector2.DOWN
var _facing_name: String = "down"
var _prompt: String = ""
var _interact_cb: Callable = Callable()
var _farm: Node = null
var _busy: float = 0.0
var _action_lock: bool = false
var _action_anim: String = ""
var _bob_t: float = 0.0
var _anim_base_y: float = -8.0
var _foot_cd: float = 0.0
var _foot_dust: CPUParticles2D
var _shadow: Polygon2D

func _ready() -> void:
	add_to_group("player")
	y_sort_enabled = true
	_anim_base_y = anim.position.y
	_setup_shadow()
	_setup_frames()
	_setup_foot_dust()
	camera.make_current()
	camera.zoom = Vector2(2, 2)
	camera.position_smoothing_enabled = false
	anim.animation_finished.connect(_on_anim_finished)
	anim.play("idle_down")

func _setup_shadow() -> void:
	## Grounding oval — Stardew props/characters sit on soft shadows
	_shadow = Polygon2D.new()
	_shadow.name = "GroundShadow"
	_shadow.z_index = -2
	_shadow.color = Color(0.08, 0.08, 0.12, 0.35)
	var pts := PackedVector2Array()
	for i in range(12):
		var a := TAU * float(i) / 12.0
		pts.append(Vector2(cos(a) * 9.0, sin(a) * 3.5 + 6.0))
	_shadow.polygon = pts
	add_child(_shadow)

func _setup_foot_dust() -> void:
	_foot_dust = CPUParticles2D.new()
	_foot_dust.name = "FootDust"
	_foot_dust.emitting = false
	_foot_dust.one_shot = true
	_foot_dust.explosiveness = 0.85
	_foot_dust.amount = 6
	_foot_dust.lifetime = 0.35
	_foot_dust.emission_shape = CPUParticles2D.EMISSION_SHAPE_SPHERE
	_foot_dust.emission_sphere_radius = 3.0
	_foot_dust.direction = Vector2(0, -1)
	_foot_dust.spread = 60.0
	_foot_dust.gravity = Vector2(0, 40)
	_foot_dust.initial_velocity_min = 8.0
	_foot_dust.initial_velocity_max = 18.0
	_foot_dust.scale_amount_min = 0.4
	_foot_dust.scale_amount_max = 1.0
	_foot_dust.color = Color(0.72, 0.62, 0.45, 0.45)
	_foot_dust.z_index = -1
	_foot_dust.position = Vector2(0, 6)
	add_child(_foot_dust)

func _load_tex(path: String) -> Texture2D:
	if ResourceLoader.exists(path):
		var res := load(path)
		if res is Texture2D:
			return res
	var abs_path := ProjectSettings.globalize_path(path)
	var img := Image.new()
	if img.load(abs_path) != OK:
		return null
	return ImageTexture.create_from_image(img)

func _add_row_anim(frames: SpriteFrames, name: String, row: int, tex: Texture2D, cols: int, speed: float, loop: bool) -> void:
	frames.add_animation(name)
	frames.set_animation_speed(name, speed)
	frames.set_animation_loop(name, loop)
	for ci in range(cols):
		var at := AtlasTexture.new()
		at.atlas = tex
		at.region = Rect2(ci * CELL, row * CELL, CELL, CELL)
		frames.add_frame(name, at, 1.0)

func _setup_frames() -> void:
	var path := "res://assets/processed/player.png"
	var tex := _load_tex(path)
	if tex == null:
		push_error("missing player.png")
		return
	var frames := SpriteFrames.new()
	for di in range(DIRS.size()):
		var d: String = DIRS[di]
		## Walk: 6 clear stride frames @ 10 fps (legs visibly alternate)
		_add_row_anim(frames, "walk_%s" % d, di, tex, 6, 10.0, true)
		## Idle: plant frames 0 + 3
		frames.add_animation("idle_%s" % d)
		frames.set_animation_speed("idle_%s" % d, 2.0)
		frames.set_animation_loop("idle_%s" % d, true)
		for ci in [0, 3]:
			var at := AtlasTexture.new()
			at.atlas = tex
			at.region = Rect2(ci * CELL, di * CELL, CELL, CELL)
			frames.add_frame("idle_%s" % d, at, 1.0)
		## Tool actions: 4 frames, play once
		_add_row_anim(frames, "hoe_%s" % d, 4 + di, tex, 4, 12.0, false)
		_add_row_anim(frames, "water_%s" % d, 8 + di, tex, 4, 10.0, false)
		_add_row_anim(frames, "plant_%s" % d, 12 + di, tex, 4, 10.0, false)
	anim.sprite_frames = frames
	anim.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	anim.speed_scale = 1.0
	anim.centered = true
	anim.offset = Vector2(0, -16)

func _on_anim_finished() -> void:
	if not _action_lock:
		return
	var cur := String(anim.animation)
	if _action_anim != "" and cur != _action_anim:
		return
	_action_lock = false
	_action_anim = ""
	anim.play("idle_%s" % _facing_name)

func _dir_name_from_vec(v: Vector2) -> String:
	if absf(v.x) > absf(v.y):
		return "left" if v.x < 0.0 else "right"
	return "up" if v.y < 0.0 else "down"

func set_farm(farm: Node) -> void:
	_farm = farm

func debug_list_anims() -> PackedStringArray:
	if anim == null or anim.sprite_frames == null:
		return PackedStringArray()
	return anim.sprite_frames.get_animation_names()

func debug_play_hoe() -> String:
	_play_action("hoe")
	return "%s|lock=%s|busy=%.2f" % [String(anim.animation), str(_action_lock), _busy]

func debug_freeze_action(kind: String, frame: int = 2) -> String:
	## Hold a mid-action pose for MCP smoke (tool anims finish before remote round-trips)
	_action_anim = "%s_%s" % [kind, _facing_name]
	_action_lock = true
	_busy = 30.0
	if anim.sprite_frames != null and anim.sprite_frames.has_animation(_action_anim):
		anim.play(_action_anim)
		anim.pause()
		var fc: int = anim.sprite_frames.get_frame_count(_action_anim)
		anim.frame = clampi(frame, 0, maxi(fc - 1, 0))
	return "%s frame=%d lock=%s" % [String(anim.animation), anim.frame, str(_action_lock)]

func set_interact_prompt(text: String, cb: Callable = Callable()) -> void:
	_prompt = text
	_interact_cb = cb

func clear_interact_prompt() -> void:
	_prompt = ""
	_interact_cb = Callable()

func get_interact_prompt() -> String:
	return _prompt

func get_tool_name() -> String:
	match tool:
		Tool.HOE:
			return "锄头"
		Tool.CAN:
			return "水壶"
		Tool.AXE:
			return "斧头"
		Tool.ROD:
			return "钓竿"
	return "?"

func try_interact() -> bool:
	if _interact_cb.is_valid():
		_interact_cb.call()
		return true
	return false

func target_cell() -> Vector2i:
	var world := global_position + facing * float(tile_size)
	return Vector2i(floori(world.x / tile_size), floori(world.y / tile_size))

func _play_action(kind: String) -> void:
	_action_anim = "%s_%s" % [kind, _facing_name]
	_action_lock = true
	_busy = 0.42
	if anim.sprite_frames != null and anim.sprite_frames.has_animation(_action_anim):
		anim.speed_scale = 1.0
		anim.play(_action_anim)
		anim.set_frame_and_progress(0, 0.0)
	else:
		push_warning("Oakhaven: missing player anim %s" % _action_anim)
		_action_lock = false
		_action_anim = ""

func _physics_process(delta: float) -> void:
	if GameBus.inventory_open or GameBus.dialogue_open:
		velocity = Vector2.ZERO
		if not _action_lock:
			var idle_lock := "idle_%s" % _facing_name
			if anim.animation != idle_lock or not anim.is_playing():
				anim.play(idle_lock)
		_set_bob(delta, false)
		move_and_slide()
		return
	_busy = maxf(_busy - delta, 0.0)
	_foot_cd = maxf(_foot_cd - delta, 0.0)

	## During tool anim: freeze locomotion + re-assert action frames
	if _action_lock or _busy > 0.0:
		velocity = Vector2.ZERO
		if _action_lock and _action_anim != "" and String(anim.animation) != _action_anim:
			anim.play(_action_anim)
		if _action_lock and _busy <= 0.0 and not anim.is_playing():
			_action_lock = false
			_action_anim = ""
		_set_bob(delta, false)
		move_and_slide()
		_handle_hotkeys()
		return

	var dir := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	var moving := dir.length() > 0.1
	if moving:
		facing = dir.normalized()
		_facing_name = _dir_name_from_vec(facing)
		velocity = facing * speed
		var walk_anim := "walk_%s" % _facing_name
		if anim.animation != walk_anim or not anim.is_playing():
			anim.play(walk_anim)
		anim.speed_scale = 1.0
		if _foot_cd <= 0.0:
			SFX.play("footstep")
			_foot_cd = 0.22
			if _foot_dust != null:
				_foot_dust.restart()
				_foot_dust.emitting = true
	else:
		velocity = Vector2.ZERO
		var idle_anim := "idle_%s" % _facing_name
		if anim.animation != idle_anim or not anim.is_playing():
			anim.play(idle_anim)
		anim.speed_scale = 1.0
	_set_bob(delta, moving)
	move_and_slide()
	global_position.x = clampf(global_position.x, 8.0, float(192 * 16) - 8.0)
	global_position.y = clampf(global_position.y, 8.0, float(128 * 16) - 8.0)
	_handle_hotkeys()

func _handle_hotkeys() -> void:
	if Input.is_action_just_pressed("tool_1"):
		tool = Tool.HOE
		GameBus.show_toast("工具：锄头")
	elif Input.is_action_just_pressed("tool_2"):
		tool = Tool.CAN
		GameBus.show_toast("工具：水壶")
	elif Input.is_action_just_pressed("tool_3"):
		tool = Tool.AXE
		GameBus.show_toast("工具：斧头")
	elif Input.is_action_just_pressed("tool_4"):
		tool = Tool.ROD
		GameBus.show_toast("工具：钓竿")

	if _action_lock:
		return

	if Input.is_action_just_pressed("interact"):
		if not try_interact():
			_try_farm_interact()

	if Input.is_action_just_pressed("use_tool") and _busy <= 0.0:
		_use_tool()

	if Input.is_action_just_pressed("inventory"):
		GameBus.inventory_open = not GameBus.inventory_open
		GameBus.show_toast("背包开" if GameBus.inventory_open else "背包关")

func _set_bob(delta: float, moving: bool) -> void:
	## Keep bob tiny — walk sheet already carries stride bob
	if moving:
		_bob_t += delta * 8.0
		anim.position.y = _anim_base_y + sin(_bob_t) * 0.4
	else:
		anim.position.y = _anim_base_y

func _use_tool() -> void:
	var cell := target_cell()
	match tool:
		Tool.HOE:
			if _farm == null:
				return
			if not Stamina.spend(4, "hoe"):
				return
			_play_action("hoe")
			if not _farm.call("hoe", cell):
				Stamina.restore(4)
			else:
				SFX.play("hoe")
		Tool.CAN:
			if _farm == null:
				return
			if not Stamina.spend(2, "water"):
				return
			_play_action("water")
			if _farm.call("water", cell):
				GameBus.show_toast("浇水了")
				SFX.play("water")
			else:
				Stamina.restore(2)
		Tool.AXE:
			_play_action("hoe")  # reuse swing until axe sheet exists
			_try_chop_tree()
		Tool.ROD:
			GameBus.show_toast("去湖边/河边钓鱼点按 E（需装备钓竿）")

func _try_chop_tree() -> void:
	if not Stamina.spend(5, "axe"):
		return
	var best: Node2D = null
	var best_d := 36.0
	for n in get_tree().get_nodes_in_group("choppable"):
		if not (n is Node2D):
			continue
		var d := global_position.distance_to((n as Node2D).global_position)
		if d < best_d:
			best_d = d
			best = n as Node2D
	if best == null:
		Stamina.restore(5)
		GameBus.show_toast("附近没有可砍的树（农庄边的树可砍）")
		return
	var hp := int(best.get_meta("chop_hp", 2)) - 1
	best.set_meta("chop_hp", hp)
	var tw := create_tween()
	tw.tween_property(best, "rotation_degrees", randf_range(-8.0, 8.0), 0.08)
	tw.tween_property(best, "rotation_degrees", 0.0, 0.08)
	if hp > 0:
		GameBus.show_toast("咔嚓…再砍一下")
		return
	Inventory.add("wood", 2)
	GameBus.show_toast("获得木头 x2")
	best.remove_from_group("choppable")
	var fall := create_tween()
	fall.tween_property(best, "modulate:a", 0.0, 0.25)
	fall.tween_callback(best.queue_free)

func _try_farm_interact() -> void:
	if _farm == null:
		return
	var cell := target_cell()
	var got: Variant = _farm.call("harvest", cell)
	if got != null and str(got) != "":
		Inventory.add(str(got), 1)
		GameBus.show_toast("收获：" + ItemDB.display_name(str(got)))
		_play_action("plant")
		return
	var seed_id := Inventory.selected_seed
	if Inventory.has(seed_id):
		if not Stamina.spend(1, "plant"):
			return
		if _farm.call("plant", cell, seed_id):
			Inventory.remove(seed_id, 1)
			GameBus.show_toast("播种：" + ItemDB.display_name(seed_id))
			_play_action("plant")
		else:
			Stamina.restore(1)
