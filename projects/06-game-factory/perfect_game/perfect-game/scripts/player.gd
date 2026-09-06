extends CharacterBody2D
## Player — atlas rows: down, left, right, up (48px). Walk cycle always plays while moving.

@export var speed: float = 130.0
@export var tile_size: int = 16
@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var camera: Camera2D = $Camera2D

enum Tool { HOE, CAN, AXE, ROD }

const CELL := 48
const DIRS := ["down", "left", "right", "up"]

var tool: Tool = Tool.HOE
var facing: Vector2 = Vector2.DOWN
var _facing_name: String = "down"
var _prompt: String = ""
var _interact_cb: Callable = Callable()
var _farm: Node = null
var _busy: float = 0.0
var _bob_t: float = 0.0
var _anim_base_y: float = -8.0

func _ready() -> void:
	add_to_group("player")
	_anim_base_y = anim.position.y
	_setup_frames()
	camera.make_current()
	camera.zoom = Vector2(2, 2)
	camera.position_smoothing_enabled = false
	anim.play("idle_down")

func _load_tex(path: String) -> Texture2D:
	# Prefer imported resource; fall back to Image.load for Chinese-path / broken .import
	if ResourceLoader.exists(path):
		var res := load(path)
		if res is Texture2D:
			return res
	var abs_path := ProjectSettings.globalize_path(path)
	var img := Image.new()
	if img.load(abs_path) != OK:
		return null
	return ImageTexture.create_from_image(img)

func _setup_frames() -> void:
	var path := "res://assets/processed/player.png"
	var tex := _load_tex(path)
	if tex == null:
		push_error("missing player.png")
		return
	var frames := SpriteFrames.new()
	var cols := maxi(int(tex.get_width() / float(CELL)), 1)
	var rows := maxi(int(tex.get_height() / float(CELL)), 1)
	for ri in range(mini(rows, DIRS.size())):
		var d: String = DIRS[ri]
		var walk_name := "walk_%s" % d
		var idle_name := "idle_%s" % d
		frames.add_animation(walk_name)
		frames.add_animation(idle_name)
		frames.set_animation_speed(walk_name, 12.0)
		frames.set_animation_loop(walk_name, true)
		frames.set_animation_speed(idle_name, 2.0)
		frames.set_animation_loop(idle_name, true)
		for ci in range(cols):
			var at := AtlasTexture.new()
			at.atlas = tex
			at.region = Rect2(ci * CELL, ri * CELL, CELL, CELL)
			frames.add_frame(walk_name, at, 1.0)
			if ci == 0:
				frames.add_frame(idle_name, at, 1.0)
			# soft idle breathe: reuse mid stride as second idle frame
			if ci == 2:
				frames.add_frame(idle_name, at, 1.0)
	anim.sprite_frames = frames
	anim.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	anim.speed_scale = 1.0

func _dir_name_from_vec(v: Vector2) -> String:
	if absf(v.x) > absf(v.y):
		return "left" if v.x < 0.0 else "right"
	return "up" if v.y < 0.0 else "down"

func set_farm(farm: Node) -> void:
	_farm = farm

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

func _physics_process(delta: float) -> void:
	if GameBus.inventory_open or GameBus.dialogue_open:
		velocity = Vector2.ZERO
		var idle_lock := "idle_%s" % _facing_name
		if anim.animation != idle_lock or not anim.is_playing():
			anim.play(idle_lock)
		_set_bob(delta, false)
		move_and_slide()
		return
	_busy = maxf(_busy - delta, 0.0)
	var dir := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	var moving := dir.length() > 0.1
	if moving:
		facing = dir.normalized()
		_facing_name = _dir_name_from_vec(facing)
		velocity = facing * speed
		var walk_anim := "walk_%s" % _facing_name
		# Always play so walk cycle never freezes after first frame
		if anim.animation != walk_anim or not anim.is_playing():
			anim.play(walk_anim)
		anim.speed_scale = 1.15
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

	if Input.is_action_just_pressed("interact"):
		if not try_interact():
			_try_farm_interact()

	if Input.is_action_just_pressed("use_tool") and _busy <= 0.0:
		_use_tool()

	if Input.is_action_just_pressed("inventory"):
		GameBus.inventory_open = not GameBus.inventory_open
		GameBus.show_toast("背包开" if GameBus.inventory_open else "背包关")

func _set_bob(delta: float, moving: bool) -> void:
	# Light bob only — walk sheet already has stride motion
	if moving:
		_bob_t += delta * 10.0
		anim.position.y = _anim_base_y + sin(_bob_t) * 0.8
	else:
		_bob_t += delta * 2.5
		anim.position.y = _anim_base_y + sin(_bob_t) * 0.4

func _use_tool() -> void:
	_busy = 0.18
	if _farm == null:
		return
	var cell := target_cell()
	match tool:
		Tool.HOE:
			_farm.call("hoe", cell)
		Tool.CAN:
			if _farm.call("water", cell):
				GameBus.show_toast("浇水了")
		Tool.AXE:
			GameBus.show_toast("暂无枯枝")
		Tool.ROD:
			GameBus.show_toast("去河边按 E 钓鱼（Wave2）")

func _try_farm_interact() -> void:
	if _farm == null:
		return
	var cell := target_cell()
	var got: Variant = _farm.call("harvest", cell)
	if got != null and str(got) != "":
		Inventory.add(str(got), 1)
		GameBus.show_toast("收获：" + ItemDB.display_name(str(got)))
		return
	var seed_id := Inventory.selected_seed
	if Inventory.has(seed_id) and _farm.call("plant", cell, seed_id):
		Inventory.remove(seed_id, 1)
		GameBus.show_toast("播种：" + ItemDB.display_name(seed_id))
