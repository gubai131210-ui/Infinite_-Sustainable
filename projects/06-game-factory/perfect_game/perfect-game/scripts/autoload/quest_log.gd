extends Node
## Lightweight quest flags toward Stardew-like demo loop.

signal progress_changed(hint: String)

const STEPS := [
	{"id": "explore_farm", "hint": "任务：在米勒农庄锄地并播种"},
	{"id": "harvest_one", "hint": "任务：浇水至成熟并收获一次"},
	{"id": "talk_npc", "hint": "任务：与任意村民交谈"},
	{"id": "visit_town", "hint": "任务：走到镇中心广场（雕像附近）"},
	{"id": "visit_station", "hint": "任务：参观橡木火车站"},
	{"id": "visit_lighthouse", "hint": "任务：参观回声湖灯塔"},
	{"id": "done", "hint": "任务完成：橡木湾一日游达成！去杂货店卖掉作物吧"},
]

var done: Dictionary = {}
var _idx: int = 0

func _ready() -> void:
	_emit_hint()

func current_hint() -> String:
	return str(STEPS[mini(_idx, STEPS.size() - 1)]["hint"])

func mark(step_id: String) -> void:
	if done.get(step_id, false):
		return
	var before := _idx
	done[step_id] = true
	while _idx < STEPS.size() - 1 and done.get(str(STEPS[_idx]["id"]), false):
		_idx += 1
	_emit_hint()
	if _idx != before:
		GameBus.show_toast("任务进度更新")

func _emit_hint() -> void:
	var h := current_hint()
	progress_changed.emit(h)
	GameBus.set_quest_hint(h)
