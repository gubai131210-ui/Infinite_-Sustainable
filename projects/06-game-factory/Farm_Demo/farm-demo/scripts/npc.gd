extends CharacterBody2D
## Ambient NPC with short Chinese dialogue.

@export var npc_id: String = "ahe"
@export var display_name: String = "阿禾"
@export var line: String = "地要勤锄，苗才肯长。"
@export var sprite_path: String = "res://assets/processed/npc_ahe.png"

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var area: Area2D = $InteractArea

var _player_inside: Node = null

func _ready() -> void:
	add_to_group("npc")
	_setup_sprite()
	area.body_entered.connect(_on_enter)
	area.body_exited.connect(_on_exit)
	anim.play("idle")

func _setup_sprite() -> void:
	var tex := load(sprite_path) as Texture2D
	var frames := SpriteFrames.new()
	frames.add_animation("idle")
	frames.add_animation("walk")
	frames.set_animation_speed("idle", 4.0)
	frames.set_animation_loop("idle", true)
	frames.set_animation_speed("walk", 8.0)
	frames.set_animation_loop("walk", true)
	var cell := 48
	var n := int(tex.get_width() / float(cell))
	n = maxi(n, 1)
	for i in range(n):
		var at := AtlasTexture.new()
		at.atlas = tex
		at.region = Rect2(i * cell, 0, cell, cell)
		frames.add_frame("walk", at)
		frames.add_frame("idle", at)
	anim.sprite_frames = frames
	anim.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST

func _on_enter(body: Node2D) -> void:
	if body.is_in_group("player") and body.has_method("set_interact_prompt"):
		_player_inside = body
		body.set_interact_prompt("按 E 与%s交谈" % display_name, Callable(self, "_talk"))

func _on_exit(body: Node2D) -> void:
	if body == _player_inside and body.has_method("clear_interact_prompt"):
		body.clear_interact_prompt()
		_player_inside = null

func _talk() -> void:
	GameBus.show_dialogue(display_name, line)
