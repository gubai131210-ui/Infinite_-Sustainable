extends CanvasLayer
## Quest + stars + cozy + toast.

@onready var quest: Label = $Top/Quest
@onready var stats: Label = $Top/Stats
@onready var toast_label: Label = $Toast
@onready var toast_timer: Timer = $ToastTimer

func _ready() -> void:
	toast_label.visible = false
	toast_timer.timeout.connect(func() -> void: toast_label.visible = false)
	GameState.stars_changed.connect(_on_stars)
	GameState.cozy_changed.connect(_on_cozy)
	GameState.quest_changed.connect(_on_quest)
	GameState.toast.connect(show_toast)
	_on_quest(GameState.quest_text())
	_refresh_stats()

func _on_stars(_g: int, _t: int) -> void:
	_refresh_stats()

func _on_cozy(_s: int) -> void:
	_refresh_stats()

func _on_quest(text: String) -> void:
	quest.text = text

func _refresh_stats() -> void:
	stats.text = "纸星 %d/%d   温馨 %d   手持：%s" % [
		GameState.stars_got,
		GameState.stars_total,
		GameState.cozy,
		"灯笼" if GameState.selected_prop == "lantern" else "花丛",
	]

func show_toast(text: String) -> void:
	_refresh_stats()
	toast_label.text = text
	toast_label.visible = true
	toast_label.modulate.a = 1.0
	toast_timer.start(2.0)
	var tw := create_tween()
	tw.tween_property(toast_label, "modulate:a", 1.0, 0.05)
	tw.tween_interval(1.4)
	tw.tween_property(toast_label, "modulate:a", 0.0, 0.4)
