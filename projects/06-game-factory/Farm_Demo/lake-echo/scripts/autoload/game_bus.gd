extends Node
## Global game helpers / toast bridge / house teleport.

signal toast(text: String)
signal dialogue(speaker: String, text: String)
signal dialogue_closed

var chest_claimed: bool = false
var inventory_open: bool = false
var dialogue_open: bool = false

var outdoor_return_pos: Vector2 = Vector2(40 * 16, 90 * 16)
var pending_spawn: Vector2 = Vector2.ZERO
var has_pending_spawn: bool = false

func show_toast(text: String) -> void:
	toast.emit(text)

func show_dialogue(speaker: String, text: String) -> void:
	dialogue_open = true
	dialogue.emit(speaker, text)

func close_dialogue() -> void:
	dialogue_open = false
	dialogue_closed.emit()

func enter_house(from_pos: Vector2) -> void:
	outdoor_return_pos = from_pos
	get_tree().change_scene_to_file("res://scenes/house_interior.tscn")

func exit_house() -> void:
	pending_spawn = outdoor_return_pos
	has_pending_spawn = true
	get_tree().change_scene_to_file("res://scenes/main.tscn")

func consume_spawn() -> Vector2:
	if has_pending_spawn:
		has_pending_spawn = false
		return pending_spawn
	return Vector2.ZERO
