extends CanvasLayer
## Oakhaven HUD — coords, tool, clock, gold, quest, toast.

@onready var info: Label = $Margin/VBox/InfoLabel
@onready var quest: Label = $Margin/VBox/QuestLabel
@onready var toast_label: Label = $Margin/VBox/ToastLabel

var _toast_left: float = 0.0
var _clock_line: String = ""

func _ready() -> void:
	GameBus.toast.connect(_on_toast)
	GameBus.quest_hint.connect(_on_quest)
	GameBus.gold_changed.connect(_on_gold)
	TimeClock.hour_changed.connect(_on_hour)
	Stamina.energy_changed.connect(func(_c, _m): pass)
	toast_label.text = ""
	quest.text = QuestLog.current_hint()
	_clock_line = TimeClock.clock_text()
	_on_gold(GameBus.gold)
	call_deferred("_bind_weather")

func _bind_weather() -> void:
	var w := get_node_or_null("/root/Weather")
	if w != null and not w.weather_changed.is_connected(_on_weather):
		w.weather_changed.connect(_on_weather)

func _on_weather(_weather_id: String) -> void:
	_clock_line = TimeClock.clock_text()

func _on_toast(text: String) -> void:
	toast_label.text = text
	_toast_left = 2.5

func _on_quest(text: String) -> void:
	quest.text = text

func _on_gold(_g: int) -> void:
	pass

func _on_hour(_d: int, _h: int) -> void:
	_clock_line = TimeClock.clock_text()

func _process(delta: float) -> void:
	var player := get_tree().get_first_node_in_group("player") as Node2D
	if player != null:
		var tool_name := "?"
		if player.has_method("get_tool_name"):
			tool_name = str(player.call("get_tool_name"))
		var prompt := ""
		if player.has_method("get_interact_prompt"):
			prompt = str(player.call("get_interact_prompt"))
		info.text = "%s  金:%d  精力:%d/%d  (%.0f,%.0f)  工具:%s  %s" % [
			_clock_line, GameBus.gold, Stamina.energy, Stamina.MAX_ENERGY,
			player.global_position.x, player.global_position.y, tool_name, prompt
		]
	if _toast_left > 0.0:
		_toast_left = maxf(_toast_left - delta, 0.0)
		if _toast_left == 0.0:
			toast_label.text = ""
