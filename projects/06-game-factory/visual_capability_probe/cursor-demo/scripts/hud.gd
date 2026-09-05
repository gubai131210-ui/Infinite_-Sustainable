extends CanvasLayer

var _player: Node
var _toast_left: float = 0.0

func _ready() -> void:
	add_to_group("hud")
	_player = get_tree().get_first_node_in_group("player")
	_label("PromptLabel").text = ""
	_label("ToastLabel").text = ""

func _label(name: String) -> Label:
	return $Margin/VBox.get_node(name) as Label

func show_toast(text: String, seconds: float = 2.5) -> void:
	var toast := _label("ToastLabel")
	toast.text = text
	_toast_left = maxf(seconds, 2.5)

func _process(delta: float) -> void:
	if _player == null:
		_player = get_tree().get_first_node_in_group("player")
	if _player != null:
		var p := _player as Node2D
		_label("PosLabel").text = "pos: (%.0f, %.0f)" % [p.global_position.x, p.global_position.y]
		if _player.has_method("get_interact_prompt"):
			_label("PromptLabel").text = str(_player.get_interact_prompt())
	if _toast_left > 0.0:
		_toast_left = maxf(_toast_left - delta, 0.0)
		if _toast_left == 0.0:
			_label("ToastLabel").text = ""
