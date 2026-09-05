extends CanvasLayer
## Inventory panel (Tab). Select seed with number row hints / click buttons.

@onready var panel: PanelContainer = $Panel
@onready var list: VBoxContainer = $Panel/Margin/VBox/List
@onready var hint: Label = $Panel/Margin/VBox/Hint

func _ready() -> void:
	visible = false
	panel.visible = true
	Inventory.changed.connect(_rebuild)
	_rebuild()

func _process(_delta: float) -> void:
	var want := GameBus.inventory_open
	if visible != want:
		visible = want
		if want:
			_rebuild()

func _rebuild() -> void:
	for c in list.get_children():
		c.queue_free()
	hint.text = "点击种子以选中播种；再按 Tab 关闭"
	for e in Inventory.list_entries():
		var id: String = str(e["id"])
		var n: int = int(e["count"])
		var btn := Button.new()
		btn.text = "%s  x%d%s" % [ItemDB.display_name(id), n, "  ←选中" if id == Inventory.selected_seed else ""]
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		btn.pressed.connect(_on_pick.bind(id))
		list.add_child(btn)

func _on_pick(id: String) -> void:
	if ItemDB.ITEMS.has(id) and str(ItemDB.ITEMS[id].get("kind", "")) == "seed":
		Inventory.selected_seed = id
		GameBus.show_toast("选中种子：" + ItemDB.display_name(id))
		_rebuild()
	else:
		GameBus.show_toast(ItemDB.display_name(id) + " x" + str(Inventory.count(id)))
