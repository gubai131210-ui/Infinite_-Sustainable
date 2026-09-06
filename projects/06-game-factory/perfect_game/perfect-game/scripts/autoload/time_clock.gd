extends Node
## Day/hour clock — physics tick, not framerate. Stardew-like spine.

signal hour_changed(day: int, hour: int)
signal day_changed(day: int)
signal period_changed(period: String)

## Real seconds per in-game hour (outdoor pace).
const SEC_PER_HOUR := 7.5

var day: int = 1
var hour: int = 8
var period: String = "day"
var paused: bool = false

var _acc: float = 0.0

func _physics_process(delta: float) -> void:
	if paused:
		return
	if GameBus.dialogue_open or GameBus.inventory_open:
		return
	_acc += delta
	while _acc >= SEC_PER_HOUR:
		_acc -= SEC_PER_HOUR
		advance_hour()

func clock_text() -> String:
	return "第%d天 %02d:00 · %s" % [day, hour, _period_cn()]

func _period_cn() -> String:
	match period:
		"dawn":
			return "黎明"
		"day":
			return "白天"
		"dusk":
			return "黄昏"
		"night":
			return "夜晚"
	return period

func advance_hour() -> void:
	hour += 1
	if hour >= 24:
		hour = 0
		_roll_day()
	_refresh_period()
	hour_changed.emit(day, hour)

func sleep_to_morning() -> void:
	## Bed rest: jump to next day 06:00 and notify farm growth.
	_acc = 0.0
	_roll_day()
	hour = 6
	_refresh_period()
	hour_changed.emit(day, hour)
	GameBus.show_toast("睡到了第%d天清晨" % day)

func _roll_day() -> void:
	day += 1
	day_changed.emit(day)

func _refresh_period() -> void:
	var next := "day"
	if hour >= 5 and hour < 8:
		next = "dawn"
	elif hour >= 8 and hour < 17:
		next = "day"
	elif hour >= 17 and hour < 20:
		next = "dusk"
	else:
		next = "night"
	if next != period:
		period = next
		period_changed.emit(period)

func modulate_for_period() -> Color:
	match period:
		"dawn":
			return Color(1.05, 0.95, 0.9, 1.0)
		"day":
			return Color(1.0, 1.0, 1.0, 1.0)
		"dusk":
			return Color(1.08, 0.85, 0.72, 1.0)
		"night":
			return Color(0.45, 0.5, 0.75, 1.0)
	return Color.WHITE
