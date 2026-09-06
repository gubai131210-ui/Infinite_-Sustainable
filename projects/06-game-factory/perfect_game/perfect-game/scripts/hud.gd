extends CanvasLayer
## HUD: paper star count.

@onready var label: Label = $Margin/Label

var total: int = 5
var got: int = 0

func _ready() -> void:
	_refresh()

func set_total(n: int) -> void:
	total = n
	_refresh()

func add_one() -> void:
	got += 1
	_refresh()
	if got >= total:
		label.text = "纸星 %d/%d  — 沙盘收集完成！" % [got, total]

func _refresh() -> void:
	label.text = "纸星 %d/%d" % [got, total]
