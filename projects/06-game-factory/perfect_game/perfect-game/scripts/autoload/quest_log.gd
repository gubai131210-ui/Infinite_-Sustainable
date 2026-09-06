extends Node
## Dual cozy quest lines: main day-trip + market festival (P13).

signal progress_changed(hint: String)

const MAIN := [
	{"id": "explore_farm", "hint": "任务：在米勒农庄锄地并播种"},
	{"id": "harvest_one", "hint": "任务：浇水至成熟并收获一次"},
	{"id": "talk_npc", "hint": "任务：与任意村民交谈"},
	{"id": "visit_town", "hint": "任务：走到镇中心广场（雕像附近）"},
	{"id": "visit_station", "hint": "任务：参观橡木火车站"},
	{"id": "visit_waterfall", "hint": "任务：去北缘瀑布倾听回声"},
	{"id": "visit_lighthouse", "hint": "任务：按纸条提示参观回声湖灯塔"},
	{"id": "done", "hint": "一日游完成！可去卖作物，或开始「小镇集市日」"},
]

const MARKET := [
	{"id": "mkt_buy", "hint": "集市：去杂货店买一份种子礼包"},
	{"id": "mkt_sell", "hint": "集市：在摊位或店里卖出一次货物"},
	{"id": "mkt_talk_hua", "hint": "集市：与花贩小菊交谈"},
	{"id": "mkt_gift", "hint": "集市：送礼给任意村民（背包点选礼物后对话）"},
	{"id": "mkt_cafe", "hint": "集市：去咖啡馆点一杯热可可"},
	{"id": "mkt_done", "hint": "集市日完成：镇子更热闹了！继续过日子吧"},
]

var done: Dictionary = {}
var _main_idx: int = 0
var _mkt_idx: int = 0
var active_line: String = "main"

func _ready() -> void:
	_emit_hint()

func current_hint() -> String:
	if active_line == "market" or _main_complete():
		return str(MARKET[mini(_mkt_idx, MARKET.size() - 1)]["hint"])
	return str(MAIN[mini(_main_idx, MAIN.size() - 1)]["hint"])

func _main_complete() -> bool:
	return bool(done.get("done", false))

func _market_complete() -> bool:
	return bool(done.get("mkt_done", false))

func mark(step_id: String) -> void:
	if done.get(step_id, false):
		return
	var before_hint := current_hint()
	done[step_id] = true
	_advance_main()
	_maybe_auto_market_done()
	_advance_market()
	if _main_complete() and not _market_complete():
		active_line = "market"
	_emit_hint()
	if current_hint() != before_hint:
		var bus := get_node_or_null("/root/GameBus")
		if bus != null and bus.has_method("show_toast"):
			bus.call("show_toast", "任务进度更新")

func _advance_main() -> void:
	while _main_idx < MAIN.size() - 1 and done.get(str(MAIN[_main_idx]["id"]), false):
		_main_idx += 1

func _advance_market() -> void:
	while _mkt_idx < MARKET.size() - 1 and done.get(str(MARKET[_mkt_idx]["id"]), false):
		_mkt_idx += 1

func _maybe_auto_market_done() -> void:
	for i in range(MARKET.size() - 1):
		if not done.get(str(MARKET[i]["id"]), false):
			return
	done["mkt_done"] = true

func _emit_hint() -> void:
	var h := current_hint()
	progress_changed.emit(h)
	var bus := get_node_or_null("/root/GameBus")
	if bus != null and bus.has_method("set_quest_hint"):
		bus.call("set_quest_hint", h)

func restore_state(done_map: Dictionary, main_idx: int, mkt_idx: int, line: String) -> void:
	done = done_map.duplicate(true)
	_main_idx = main_idx
	_mkt_idx = mkt_idx
	active_line = line if line in ["main", "market"] else "main"
	_maybe_auto_market_done()
	_advance_main()
	_advance_market()
	if _main_complete() and not _market_complete():
		active_line = "market"
	_emit_hint()
