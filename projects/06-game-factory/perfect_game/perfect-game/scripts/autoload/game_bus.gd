extends Node
## Oakhaven global bus — toast, dialogue, multi-interior teleport.

signal toast(text: String)
signal dialogue(speaker: String, text: String)
signal dialogue_closed
signal quest_hint(text: String)

var chest_claimed: bool = false
var inventory_open: bool = false
var dialogue_open: bool = false

var outdoor_return_pos: Vector2 = Vector2(40 * 16, 90 * 16)
var pending_spawn: Vector2 = Vector2.ZERO
var has_pending_spawn: bool = false
var current_interior_id: String = "farmhouse"
var current_interior_title: String = "农舍"

const INTERIORS := {
	"farmhouse": {"scene": "res://scenes/interiors/interior.tscn", "title": "米勒农舍"},
	"barn": {"scene": "res://scenes/interiors/interior.tscn", "title": "谷仓工坊"},
	"shop": {"scene": "res://scenes/interiors/interior.tscn", "title": "杂货店"},
	"cafe": {"scene": "res://scenes/interiors/interior.tscn", "title": "橡木咖啡馆"},
	"station": {"scene": "res://scenes/interiors/interior.tscn", "title": "火车站厅"},
	"lighthouse": {"scene": "res://scenes/interiors/interior.tscn", "title": "灯塔底层"},
}

func show_toast(text: String) -> void:
	toast.emit(text)

func show_dialogue(speaker: String, text: String) -> void:
	dialogue_open = true
	dialogue.emit(speaker, text)

func close_dialogue() -> void:
	dialogue_open = false
	dialogue_closed.emit()

func set_quest_hint(text: String) -> void:
	quest_hint.emit(text)

func enter_house(from_pos: Vector2) -> void:
	enter_interior(from_pos, "farmhouse")

func enter_interior(from_pos: Vector2, interior_id: String) -> void:
	outdoor_return_pos = from_pos
	current_interior_id = interior_id
	var info: Dictionary = INTERIORS.get(interior_id, INTERIORS["farmhouse"])
	current_interior_title = str(info["title"])
	get_tree().change_scene_to_file(str(info["scene"]))

func exit_house() -> void:
	pending_spawn = outdoor_return_pos
	has_pending_spawn = true
	get_tree().change_scene_to_file("res://scenes/main.tscn")

func consume_spawn() -> Vector2:
	if has_pending_spawn:
		has_pending_spawn = false
		return pending_spawn
	return Vector2.ZERO
