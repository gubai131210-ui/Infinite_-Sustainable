extends CanvasLayer
## Minimal HUD toast + coords.

@onready var info: Label = $Margin/VBox/InfoLabel
@onready var toast_label: Label = $Margin/VBox/ToastLabel

var _toast_left: float = 0.0

func _ready() -> void:
	GameBus.toast.connect(_on_toast)
	toast_label.text = ""

func _on_toast(text: String) -> void:
	toast_label.text = text
	_toast_left = 2.5

func _process(delta: float) -> void:
	var player := get_tree().get_first_node_in_group("player") as Node2D
	if player != null:
		info.text = "坐标 (%.0f, %.0f)  |  WASD移动 E交互  |  Lake Echo R5" % [player.global_position.x, player.global_position.y]
	if _toast_left > 0.0:
		_toast_left = maxf(_toast_left - delta, 0.0)
		if _toast_left == 0.0:
			toast_label.text = ""
