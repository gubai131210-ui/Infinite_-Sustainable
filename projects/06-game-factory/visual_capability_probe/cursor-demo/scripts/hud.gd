extends CanvasLayer

@onready var label: Label = $Margin/Label
var _player: Node2D

func _ready() -> void:
	_player = get_tree().get_first_node_in_group("player") as Node2D

func _process(_delta: float) -> void:
	if _player == null:
		_player = get_tree().get_first_node_in_group("player") as Node2D
		return
	label.text = "pos: (%.0f, %.0f)" % [_player.global_position.x, _player.global_position.y]
