extends Node
## Oakhaven global bus — toast, dialogue, gold, save, interiors.

signal toast(text: String)
signal dialogue(speaker: String, text: String)
signal dialogue_closed
signal quest_hint(text: String)
signal gold_changed(amount: int)

var chest_claimed: bool = false
var inventory_open: bool = false
var dialogue_open: bool = false

var outdoor_return_pos: Vector2 = Vector2(40 * 16, 90 * 16)
var pending_spawn: Vector2 = Vector2.ZERO
var has_pending_spawn: bool = false
var current_interior_id: String = "farmhouse"
var current_interior_title: String = "农舍"
var farm_plots_data: Dictionary = {}

## Integer coins (no float money).
var gold: int = 120

const SAVE_PATH := "user://oakhaven_save.json"

const INTERIORS := {
	"farmhouse": {"scene": "res://scenes/interiors/interior.tscn", "title": "米勒农舍"},
	"barn": {"scene": "res://scenes/interiors/interior.tscn", "title": "谷仓工坊"},
	"shop": {"scene": "res://scenes/interiors/interior.tscn", "title": "杂货店"},
	"cafe": {"scene": "res://scenes/interiors/interior.tscn", "title": "橡木咖啡馆"},
	"station": {"scene": "res://scenes/interiors/interior.tscn", "title": "火车站厅"},
	"lighthouse": {"scene": "res://scenes/interiors/interior.tscn", "title": "灯塔底层"},
}

func _ready() -> void:
	# Defer load until other autoloads exist
	call_deferred("_deferred_load")

func _deferred_load() -> void:
	load_game()

func show_toast(text: String) -> void:
	toast.emit(text)

func show_dialogue(speaker: String, text: String) -> void:
	dialogue_open = true
	dialogue.emit(speaker, text)
	QuestLog.mark("talk_npc")

func close_dialogue() -> void:
	dialogue_open = false
	dialogue_closed.emit()

func set_quest_hint(text: String) -> void:
	quest_hint.emit(text)

func add_gold(n: int) -> void:
	gold = maxi(gold + n, 0)
	gold_changed.emit(gold)

func enter_house(from_pos: Vector2) -> void:
	enter_interior(from_pos, "farmhouse")

func enter_interior(from_pos: Vector2, interior_id: String) -> void:
	outdoor_return_pos = from_pos
	current_interior_id = interior_id
	var info: Dictionary = INTERIORS.get(interior_id, INTERIORS["farmhouse"])
	current_interior_title = str(info["title"])
	save_game()
	get_tree().change_scene_to_file(str(info["scene"]))

func exit_house() -> void:
	pending_spawn = outdoor_return_pos
	has_pending_spawn = true
	save_game()
	get_tree().change_scene_to_file("res://scenes/main.tscn")

func consume_spawn() -> Vector2:
	if has_pending_spawn:
		has_pending_spawn = false
		return pending_spawn
	return Vector2.ZERO

func save_game() -> void:
	var plots_out: Dictionary = {}
	for k in farm_plots_data.keys():
		var cell: Vector2i
		if k is Vector2i:
			cell = k
		else:
			cell = _parse_cell_key(str(k))
		plots_out["%d,%d" % [cell.x, cell.y]] = farm_plots_data[k]
	var data := {
		"gold": gold,
		"day": TimeClock.day,
		"hour": TimeClock.hour,
		"chest_claimed": chest_claimed,
		"farm_plots": plots_out,
		"inventory": Inventory.stacks.duplicate(true),
		"quest_done": QuestLog.done.duplicate(true),
		"quest_idx": QuestLog._idx,
		"energy": Stamina.energy,
		"save_version": 2,
	}
	var f := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if f == null:
		push_warning("save failed")
		return
	f.store_string(JSON.stringify(data))
	f.close()

func _parse_cell_key(s: String) -> Vector2i:
	## Accept "x,y" or Godot-ish "(x, y)" from older saves.
	var t := s.strip_edges().replace("(", "").replace(")", "").replace(" ", "")
	var parts := t.split(",")
	if parts.size() >= 2:
		return Vector2i(int(parts[0]), int(parts[1]))
	return Vector2i.ZERO

func load_game() -> void:
	if not FileAccess.file_exists(SAVE_PATH):
		return
	var f := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if f == null:
		return
	var parsed: Variant = JSON.parse_string(f.get_as_text())
	f.close()
	if typeof(parsed) != TYPE_DICTIONARY:
		return
	var data: Dictionary = parsed
	gold = int(data.get("gold", gold))
	chest_claimed = bool(data.get("chest_claimed", false))
	if data.has("farm_plots") and typeof(data["farm_plots"]) == TYPE_DICTIONARY:
		var raw: Dictionary = data["farm_plots"]
		var normalized: Dictionary = {}
		for k in raw.keys():
			normalized[_parse_cell_key(str(k))] = raw[k]
		farm_plots_data = normalized
	if data.has("inventory") and typeof(data["inventory"]) == TYPE_DICTIONARY:
		Inventory.stacks = data["inventory"]
		Inventory.changed.emit()
	if data.has("day"):
		TimeClock.day = int(data["day"])
	if data.has("hour"):
		TimeClock.hour = int(data["hour"])
		TimeClock._refresh_period()
	if data.has("quest_done") and typeof(data["quest_done"]) == TYPE_DICTIONARY:
		QuestLog.done = data["quest_done"]
	if data.has("quest_idx"):
		QuestLog._idx = int(data["quest_idx"])
	if data.has("energy"):
		Stamina.energy = clampi(int(data["energy"]), 0, Stamina.MAX_ENERGY)
		Stamina.energy_changed.emit(Stamina.energy, Stamina.MAX_ENERGY)
	gold_changed.emit(gold)
