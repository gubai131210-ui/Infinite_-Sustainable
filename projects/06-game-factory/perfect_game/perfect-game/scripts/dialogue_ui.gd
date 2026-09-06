extends CanvasLayer
## Simple dialogue box. Ignores close on the same frame it opened.

@onready var box: PanelContainer = $Box
@onready var speaker: Label = $Box/Margin/VBox/Speaker
@onready var body: Label = $Box/Margin/VBox/Body
@onready var tip: Label = $Box/Margin/VBox/Tip

var _opened_frame: int = -1

func _ready() -> void:
	visible = false
	GameBus.dialogue.connect(_on_dialogue)
	GameBus.dialogue_closed.connect(func(): visible = false)
	tip.text = "按 E 或 空格 关闭"

func _on_dialogue(who: String, text: String) -> void:
	speaker.text = who
	body.text = text
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
