extends Area2D
## Reusable interact prompt zone.

@export var prompt_text: String = "按 E 交互"
@export var mode: String = "toast"  # toast | chest | fish | dialogue | house | bed | exit_house
@export var message: String = ""
@export var speaker: String = ""
@export var interior_id: String = "farmhouse"

signal interacted(message: String)

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)
	add_to_group("interact_zone")

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("player") and body.has_method("set_interact_prompt"):
		body.set_interact_prompt(prompt_text, Callable(self, "_do_interact"))

func _on_body_exited(body: Node2D) -> void:
	if body.is_in_group("player") and body.has_method("clear_interact_prompt"):
		body.clear_interact_prompt()

func _do_interact() -> void:
	match mode:
		"chest":
			if GameBus.chest_claimed:
				GameBus.show_toast("箱子是空的")
			else:
				GameBus.chest_claimed = true
				var bonus: Dictionary = Inventory.grant_chest_bonus()
				GameBus.show_toast("从箱子里拿了备用种子和饲料")
				interacted.emit(str(bonus))
		"fish":
			var player := get_tree().get_first_node_in_group("player")
			if player != null and int(player.get("tool")) != 3:
				GameBus.show_toast("装备钓竿（按 4）后再钓")
				return
			Inventory.add("fish", 1)
			GameBus.show_toast("钓到一条鱼！")
			interacted.emit("fish")
		"dialogue":
			GameBus.show_dialogue(speaker, message)
			interacted.emit(message)
		"house":
			var p := get_tree().get_first_node_in_group("player") as Node2D
			var from := p.global_position if p != null else global_position
			GameBus.show_toast("进入%s…" % GameBus.INTERIORS.get(interior_id, {}).get("title", "室内"))
			GameBus.enter_interior(from, interior_id)
			interacted.emit(interior_id)
		"bed":
			GameBus.show_toast("休息了一会儿，精神满满。")
			interacted.emit("bed")
		"exit_house":
			GameBus.show_toast("离开%s" % GameBus.current_interior_title)
			GameBus.exit_house()
			interacted.emit("exit")
		_:
			GameBus.show_toast(message)
			interacted.emit(message)
