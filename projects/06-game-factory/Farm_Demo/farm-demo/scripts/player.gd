extends CharacterBody2D
## Top-down player with 4-direction walk cycles (atlas rows: down/left/right/up).

@export var speed: float = 120.0
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

func _ready() -> void:
	add_to_group("player")
	_setup_frames()
	for a in ["move_left", "move_right", "move_up", "move_down", "interact", "use_tool", "inventory", "tool_1", "tool_2", "tool_3", "tool_4"]:
		if InputMap.has_action(a):
			Input.action_release(a)
	camera.make_current()
	anim.play("idle_down")

func _setup_frames() -> void:
	var tex := load("res://assets/processed/player.png") as Texture2D
	var frames := SpriteFrames.new()
	var cols := maxi(int(tex.get_width() / float(CELL)), 1)
	var rows := maxi(int(tex.get_height() / float(CELL)), 1)
	for ri in range(mini(rows, DIRS.size())):
		var d: String = DIRS[ri]
		var walk_name := "walk_%s" % d
		var idle_name := "idle_%s" % d
		frames.add_animation(walk_name)
		frames.add_animation(idle_name)
		frames.set_animation_speed(walk_name, 10.0)
		frames.set_animation_loop(walk_name, true)
		frames.set_animation_speed(idle_name, 1.0)
		frames.set_animation_loop(idle_name, true)
		for ci in range(cols):
			var at := AtlasTexture.new()
			at.atlas = tex
			at.region = Rect2(ci * CELL, ri * CELL, CELL, CELL)
			frames.add_frame(walk_name, at)
			if ci == 0:
				frames.add_frame(idle_name, at)
	anim.sprite_frames = frames
	anim.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST

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

func try_interact() -> bool:
	if _interact_cb.is_valid():
		_interact_cb.call()
		return true
	return false

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

func target_cell() -> Vector2i:
	var world := global_position + facing * float(tile_size)
	return Vector2i(floori(world.x / tile_size), floori(world.y / tile_size))

func _physics_process(delta: float) -> void:
	if Input.is_action_just_pressed("inventory"):
		GameBus.inventory_open = not GameBus.inventory_open

	if GameBus.inventory_open or GameBus.dialogue_open:
		velocity = Vector2.ZERO
		move_and_slide()
		return
	_busy = maxf(_busy - delta, 0.0)
	var dir := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	if dir.length() > 0.1:
		facing = dir.normalized()
		_facing_name = _dir_name_from_vec(facing)
		velocity = facing * speed
		var walk_anim := "walk_%s" % _facing_name
		if anim.animation != walk_anim:
			anim.play(walk_anim)
		anim.flip_h = false
	else:
		velocity = Vector2.ZERO
		var idle_anim := "idle_%s" % _facing_name
		if anim.animation != idle_anim:
			anim.play(idle_anim)
	move_and_slide()
	global_position.x = clampf(global_position.x, 8.0, 56.0 * 16.0 - 8.0)
	global_position.y = clampf(global_position.y, 8.0, 40.0 * 16.0 - 8.0)

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

func _use_tool() -> void:
	_busy = 0.18
	if _farm == null:
		return
	var cell := target_cell()
	match tool:
		Tool.HOE:
			if _farm.call("hoe", cell):
				GameBus.show_toast("锄地完成")
			else:
				GameBus.show_toast("这里不能锄")
		Tool.CAN:
			if _farm.call("water", cell):
				GameBus.show_toast("浇水了")
			else:
				GameBus.show_toast("这里不用浇")
		Tool.AXE:
			if _farm.call("chop", cell):
				GameBus.show_toast("获得木头")
			else:
				GameBus.show_toast("没有可砍的枯枝")
		Tool.ROD:
			GameBus.show_toast("去河边按 E 钓鱼")

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
		return
