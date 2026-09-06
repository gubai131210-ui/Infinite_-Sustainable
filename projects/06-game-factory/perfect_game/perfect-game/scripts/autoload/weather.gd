extends Node
## Simple weather spine — clear / rain (P21).

signal weather_changed(weather: String)

var weather: String = "clear"  # clear | rain
var _hours_left: int = 0

func _ready() -> void:
	call_deferred("_bind_clock")

func _bind_clock() -> void:
	var tc := get_node_or_null("/root/TimeClock")
	if tc == null:
		return
	if not tc.hour_changed.is_connected(_on_hour):
		tc.hour_changed.connect(_on_hour)
	_roll_maybe(true)

func _on_hour(_d: int, h: int) -> void:
	if _hours_left > 0:
		_hours_left -= 1
		if _hours_left <= 0:
			_set_weather("clear")
	elif h == 6 or h == 12 or h == 18:
		_roll_maybe(false)

func _roll_maybe(force: bool) -> void:
	if not force and randf() > 0.28:
		return
	if randf() < 0.45:
		_set_weather("rain")
		_hours_left = randi_range(3, 8)
	else:
		_set_weather("clear")
		_hours_left = 0

func _set_weather(w: String) -> void:
	if w == weather:
		return
	weather = w
	weather_changed.emit(weather)
	call_deferred("_announce_weather")

func _announce_weather() -> void:
	var bus := get_node_or_null("/root/GameBus")
	var sfx := get_node_or_null("/root/SFX")
	if weather == "rain":
		if bus:
			bus.show_toast("下雨了…作物会喝饱水")
		if sfx:
			sfx.play("rain")
	else:
		if bus:
			bus.show_toast("天晴了")

func is_raining() -> bool:
	return weather == "rain"

func weather_cn() -> String:
	return "雨" if weather == "rain" else "晴"

func force_rain_for_test(hours: int = 4) -> void:
	_hours_left = hours
	_set_weather("rain")

func force_clear_for_test() -> void:
	_hours_left = 99
	_set_weather("clear")
