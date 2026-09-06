extends Area2D
## Reusable interact prompt zone.

@export var prompt_text: String = "按 E 交互"
@export var mode: String = "toast"  # toast|chest|fish|dialogue|house|bed|exit_house|shop_sell|shop_buy|quest_zone|stamina_sip|cook|eat|bulletin|mail
@export var message: String = ""
@export var speaker: String = ""
@export var interior_id: String = "farmhouse"
@export var quest_step_id: String = ""
@export var stamina_restore: int = 0
@export var recipe_id: String = ""
@export var food_id: String = ""

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
				SFX.play("chest")
				GameBus.save_game()
				interacted.emit(str(bonus))
		"fish":
			var player := get_tree().get_first_node_in_group("player")
			if player != null and int(player.get("tool")) != 3:
				GameBus.show_toast("装备钓竿（按 4）后再钓")
				return
			if not Stamina.spend(3, "fish"):
				return
			# Mini bite roll — cozy daily, not arcade timing yet
			var roll := randi() % 100
			if roll < 18:
				GameBus.show_toast("跑掉了…再试一次")
			elif roll < 85:
				Inventory.add("fish", 1)
				GameBus.show_toast("钓到一条鱼！")
				interacted.emit("fish")
			else:
				Inventory.add("fish", 2)
				GameBus.show_toast("大鱼！鱼 x2")
				interacted.emit("fish_big")
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
			Stamina.restore_full()
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
		"stamina_sip":
			var amt := stamina_restore if stamina_restore > 0 else 10
			Stamina.restore(amt)
			GameBus.show_toast(message if message != "" else ("恢复精力 +%d" % amt))
			QuestLog.mark("mkt_cafe")
			interacted.emit("sip")
		"cook":
			_do_cook()
		"eat":
			_do_eat()
		"bulletin":
			_show_bulletin()
		"mail":
			_show_mail()
		_:
			GameBus.show_toast(message)
			interacted.emit(message)

func _do_cook() -> void:
	var r: Dictionary
	if recipe_id != "":
		r = Cooking.try_cook(recipe_id)
	else:
		r = Cooking.try_cook_any()
	if bool(r.get("ok", false)):
		GameBus.save_game()
		GameBus.show_toast(str(r.get("msg", "烹饪完成")))
		SFX.play("ui")
		interacted.emit("cook")
	else:
		GameBus.show_toast(str(r.get("msg", "做不了")))

func _do_eat() -> void:
	var fid := food_id
	if fid == "":
		for cand in ["salad", "omelette", "fish_soup", "pumpkin_pie"]:
			if Inventory.count(cand) > 0:
				fid = cand
				break
	if fid == "" or Inventory.count(fid) <= 0:
		GameBus.show_toast("没有可吃的料理（先在灶台烹饪）")
		return
	if Cooking.eat(fid):
		GameBus.save_game()
		SFX.play("ui")
		interacted.emit("eat_" + fid)

func _show_bulletin() -> void:
	var lines: PackedStringArray = PackedStringArray([
		"【镇告示栏】",
		"· 春季市集即将举办，欢迎上交新鲜作物。",
		"· 码头渔获不错，可去海边试竿。",
		"· 遗迹区请注意安全，结伴而行。",
		"· 今日天气：" + Weather.weather_cn() + " · " + SeasonClock.season_cn(),
	])
	GameBus.show_dialogue("告示栏", "\n".join(lines))
	QuestLog.mark("mkt_board")
	interacted.emit("bulletin")

func _show_mail() -> void:
	var day := TimeClock.day
	var body := "亲爱的农场主：\n\n欢迎来到橡木湾。\n种点作物，去市集卖出第一笔，\n再去码头吹吹风吧。\n\n—— 镇长"
	if day >= 2:
		body = "亲爱的农场主：\n\n市集筹备顺利！\n若你已卖出货物，记得去咖啡馆坐坐。\n\n—— 玛贝尔"
	if day >= 3:
		body = "亲爱的农场主：\n\n遗迹那边有人看见闪光。\n有空可以去看看，也许藏着小秘密。\n\n—— 伊莱"
	GameBus.show_dialogue("信箱", body)
	interacted.emit("mail")

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
	SFX.play("sell")
	QuestLog.mark("done")
	QuestLog.mark("mkt_sell")
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
	QuestLog.mark("mkt_buy")
	interacted.emit("bought")
