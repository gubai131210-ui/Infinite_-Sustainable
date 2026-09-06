extends Area2D
## Reusable interact prompt zone.

@export var prompt_text: String = "按 E 交互"
@export var mode: String = "toast"  # toast|chest|fish|dialogue|house|bed|exit_house|shop_sell|shop_buy|quest_zone
@export var message: String = ""
@export var speaker: String = ""
@export var interior_id: String = "farmhouse"
@export var quest_step_id: String = ""

signal interacted(message: String)

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)
	add_to_group("interact_zone")

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("player") and body.has_method("set_interact_prompt"):
		body.set_interact_prompt(prompt_text, Callable(self, "_do_interact"))
		if mode == "quest_zone" and quest_step_id != "":
			QuestLog.mark(quest_step_id)

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
				GameBus.save_game()
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
			TimeClock.sleep_to_morning()
			GameBus.save_game()
			interacted.emit("bed")
		"exit_house":
			GameBus.show_toast("离开%s" % GameBus.current_interior_title)
			GameBus.exit_house()
			interacted.emit("exit")
		"shop_sell":
			_sell_all_crops()
		"shop_buy":
			_buy_seed_bundle()
		"quest_zone":
			if quest_step_id != "":
				QuestLog.mark(quest_step_id)
			GameBus.show_toast(message if message != "" else "到访打卡")
			interacted.emit(quest_step_id)
		_:
			GameBus.show_toast(message)
			interacted.emit(message)

func _sell_all_crops() -> void:
	var earned := 0
	var ids: Array = Inventory.stacks.keys()
	for id in ids:
		var sid := str(id)
		var price := ItemDB.sell_price(sid)
		if price <= 0:
			continue
		var n := Inventory.count(sid)
		if n <= 0:
			continue
		Inventory.remove(sid, n)
		earned += price * n
	if earned <= 0:
		GameBus.show_toast("没有可卖的作物或鱼")
		return
	GameBus.add_gold(earned)
	GameBus.save_game()
	GameBus.show_toast("卖出货物，获得 %d 金币" % earned)
	QuestLog.mark("done")
	interacted.emit("sold")

func _buy_seed_bundle() -> void:
	var cost := 30
	if GameBus.gold < cost:
		GameBus.show_toast("金币不足（需要 %d）" % cost)
		return
	GameBus.add_gold(-cost)
	Inventory.add("seed_radish", 3)
	Inventory.add("seed_greens", 2)
	Inventory.add("feed", 2)
	GameBus.save_game()
	GameBus.show_toast("买下种子礼包（-%d 金）" % cost)
	interacted.emit("bought")
