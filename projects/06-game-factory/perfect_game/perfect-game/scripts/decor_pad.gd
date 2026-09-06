extends Area2D
## Glowing pad — press E while overlapping to place selected prop.

signal placed(pad: Area2D, prop: String)

@onready var ring: Polygon2D = $Ring
@onready var hint: Label = $Hint

var filled: bool = false
var _player_in: bool = false

func _ready() -> void:
	body_entered.connect(_on_enter)
	body_exited.connect(_on_exit)
	hint.visible = false
	_pulse()

func _pulse() -> void:
	var tw := create_tween().set_loops()
	tw.tween_property(ring, "modulate:a", 0.35, 0.9).set_trans(Tween.TRANS_SINE)
	tw.tween_property(ring, "modulate:a", 0.75, 0.9).set_trans(Tween.TRANS_SINE)

func _on_enter(body: Node2D) -> void:
	if body.is_in_group("player"):
		_player_in = true
		if not filled and GameState.phase == GameState.Phase.DECORATE:
			hint.visible = true
			hint.text = "E 摆放"

func _on_exit(body: Node2D) -> void:
	if body.is_in_group("player"):
		_player_in = false
		hint.visible = false

func try_place() -> bool:
	if filled or not _player_in:
		return false
	if GameState.phase != GameState.Phase.DECORATE:
		return false
	filled = true
	hint.visible = false
	ring.modulate = Color(1.0, 0.85, 0.45, 0.9)
	var prop: String = GameState.selected_prop
	placed.emit(self, prop)
	GameState.fill_pad()
	return true
