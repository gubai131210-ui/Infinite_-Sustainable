extends CharacterBody2D
## Top-down player: move, tools 1-4, plant seed, interact E, inventory Tab.

@export var speed: float = 120.0
@export var tile_size: int = 16

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var camera: Camera2D = $Camera2D

enum Tool { HOE, CAN, AXE, ROD }

var tool: Tool = Tool.HOE
var facing: Vector2 = Vector2.DOWN
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
	anim.play("idle")

func _setup_frames() -> void:
	var tex := load("res://assets/processed/player.png") as Texture2D
	var frames := SpriteFrames.new()
	frames.add_animation("idle")
	frames.add_animation("walk")
	frames.set_animation_speed("walk", 8.0)
	frames.set_animation_loop("walk", true)
	frames.set_animation_speed("idle", 1.0)
	frames.set_animation_loop("idle", true)
	for i in range(4):
		var at := AtlasTexture.new()
		at.atlas = tex
		at.region = Rect2(i * 32, 0, 32, 32)
		frames.add_frame("walk", at)
		if i == 0:
			frames.add_frame("idle", at)
	anim.sprite_frames = frames
	anim.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST

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
	# Inventory toggle must work even while panel is open.
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
		velocity = dir.normalized() * speed
		if anim.animation != "walk":
			anim.play("walk")
		anim.flip_h = facing.x < -0.2
	else:
		velocity = Vector2.ZERO
		if anim.animation != "idle":
			anim.play("idle")
	move_and_slide()
	# clamp inside map (56x40 tiles)
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
			# Fishing handled by FishingSpot interact; tip player
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
