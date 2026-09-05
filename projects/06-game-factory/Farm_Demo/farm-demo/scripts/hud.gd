extends CanvasLayer
## HUD: position, prompt, toast, tool, seed.

func _ready() -> void:
	add_to_group("hud")
	GameBus.toast.connect(_on_toast)
	$Margin/VBox/PromptLabel.text = ""
	$Margin/VBox/ToastLabel.text = ""

var _toast_left: float = 0.0
var _player: Node

func _on_toast(text: String) -> void:
	show_toast(text, 2.5)

func show_toast(text: String, seconds: float = 2.5) -> void:
	$Margin/VBox/ToastLabel.text = text
	_toast_left = maxf(seconds, 2.0)

func _process(delta: float) -> void:
	if _player == null:
		_player = get_tree().get_first_node_in_group("player")
	if _player != null:
		var p := _player as Node2D
		$Margin/VBox/PosLabel.text = "坐标 (%.0f, %.0f)" % [p.global_position.x, p.global_position.y]
		if _player.has_method("get_interact_prompt"):
			$Margin/VBox/PromptLabel.text = str(_player.get_interact_prompt())
		if _player.has_method("get_tool_name"):
			$Margin/VBox/ToolLabel.text = "工具[%d]: %s | 种子: %s x%d" % [
				int(_player.get("tool")) + 1,
				_player.get_tool_name(),
				ItemDB.display_name(Inventory.selected_seed),
				Inventory.count(Inventory.selected_seed),
			]
	$Margin/VBox/HelpLabel.text = "WASD移动 空格工具 E交互 Tab背包 1-4切工具"
	if _toast_left > 0.0:
		_toast_left = maxf(_toast_left - delta, 0.0)
		if _toast_left == 0.0:
			$Margin/VBox/ToastLabel.text = ""
