extends CanvasLayer
## Dialogue box with optional friendship heart row.

@onready var box: PanelContainer = $Box
@onready var speaker: Label = $Box/Margin/VBox/Speaker
@onready var body: Label = $Box/Margin/VBox/Body
@onready var tip: Label = $Box/Margin/VBox/Tip

var _hearts: Label
var _opened_frame: int = -1

func _ready() -> void:
	visible = false
	_hearts = Label.new()
	_hearts.name = "Hearts"
	_hearts.visible = false
	_hearts.add_theme_color_override("font_color", Color(1.0, 0.45, 0.55, 1.0))
	$Box/Margin/VBox.add_child(_hearts)
	$Box/Margin/VBox.move_child(_hearts, 1)
	GameBus.dialogue.connect(_on_dialogue)
	GameBus.dialogue_closed.connect(func(): visible = false)
	tip.text = "按 E 或 空格 关闭"

func _on_dialogue(who: String, text: String) -> void:
	speaker.text = who
	body.text = text
	var h: int = int(GameBus.get("dialogue_hearts"))
	if h >= 0:
		var filled := "♥".repeat(clampi(h, 0, 5))
		var empty := "♡".repeat(clampi(5 - h, 0, 5))
		_hearts.text = "友谊  %s%s" % [filled, empty]
		_hearts.visible = true
	else:
		_hearts.visible = false
	visible = true
	_opened_frame = Engine.get_process_frames()

func _process(_delta: float) -> void:
	if not visible:
		return
	if Engine.get_process_frames() <= _opened_frame:
		return
	if Input.is_action_just_pressed("interact") or Input.is_action_just_pressed("use_tool"):
		visible = false
		GameBus.close_dialogue()
