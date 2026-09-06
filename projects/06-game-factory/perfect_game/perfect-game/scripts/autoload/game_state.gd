extends Node
## Paper Isle quest state — stars → decorate pads → fox friend.

signal stars_changed(got: int, total: int)
signal cozy_changed(score: int)
signal quest_changed(text: String)
signal toast(text: String)
signal phase_changed(phase: int)

enum Phase { STARS, DECORATE, FOX, DONE }

var phase: int = Phase.STARS
var stars_got: int = 0
var stars_total: int = 5
var pads_filled: int = 0
var pads_total: int = 3
var cozy: int = 0
var selected_prop: String = "lantern"  # lantern | flowers

func quest_text() -> String:
	return _quest_text()

func reset() -> void:
	phase = Phase.STARS
	stars_got = 0
	pads_filled = 0
	cozy = 0
	selected_prop = "lantern"
	quest_changed.emit(_quest_text())
	stars_changed.emit(stars_got, stars_total)
	cozy_changed.emit(cozy)
	phase_changed.emit(phase)

func _quest_text() -> String:
	match phase:
		Phase.STARS:
			return "任务：收集纸星点亮沙盘  %d/%d" % [stars_got, stars_total]
		Phase.DECORATE:
			return "任务：站在光圈上按 E 摆灯笼/花  %d/%d（1灯笼 2花丛）" % [pads_filled, pads_total]
		Phase.FOX:
			return "任务：找纸狐按 E 打招呼"
		Phase.DONE:
			return "今晚的沙盘亮起来了 — 自由漫步吧"
	return ""

func add_star() -> void:
	if phase != Phase.STARS:
		return
	stars_got += 1
	cozy += 8
	stars_changed.emit(stars_got, stars_total)
	cozy_changed.emit(cozy)
	quest_changed.emit(_quest_text())
	toast.emit("纸星 +1")
	if stars_got >= stars_total:
		phase = Phase.DECORATE
		phase_changed.emit(phase)
		quest_changed.emit(_quest_text())
		toast.emit("纸星齐了！去小屋旁的光圈摆摆件")

func fill_pad() -> void:
	if phase != Phase.DECORATE:
		return
	pads_filled += 1
	cozy += 15
	cozy_changed.emit(cozy)
	quest_changed.emit(_quest_text())
	toast.emit("沙盘更温馨了")
	if pads_filled >= pads_total:
		phase = Phase.FOX
		phase_changed.emit(phase)
		quest_changed.emit(_quest_text())
		toast.emit("有谁被灯光吸引过来了…")

func greet_fox() -> void:
	if phase != Phase.FOX:
		return
	phase = Phase.DONE
	cozy += 25
	cozy_changed.emit(cozy)
	phase_changed.emit(phase)
	quest_changed.emit(_quest_text())
	toast.emit("纸狐决定留下陪你看守沙盘")

func set_selected(prop: String) -> void:
	if prop != "lantern" and prop != "flowers":
		return
	selected_prop = prop
	toast.emit("手持：%s" % ("纸灯笼" if prop == "lantern" else "花丛"))
