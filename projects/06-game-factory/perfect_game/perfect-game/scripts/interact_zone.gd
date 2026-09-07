extends Area2D
## Reusable interact prompt zone.

@export var prompt_text: String = "按 E 交互"
@export var mode: String = "toast"  # toast|chest|fish|dialogue|house|bed|exit_house|shop_sell|shop_buy|quest_zone|stamina_sip|cook|eat|bulletin|mail|ruin_loot
@export var message: String = ""
@export var speaker: String = ""
@export var interior_id: String = "farmhouse"
@export var quest_step_id: String = ""
@export var stamina_restore: int = 0
@export var recipe_id: String = ""
@export var food_id: String = ""
@export var gold_cost: int = 0

signal interacted(message: String)

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)
	add_to_group("interact_zone")

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("player") and body.has_method("set_interact_prompt"):
		body.set_interact_prompt(prompt_text, Callable(self, "_do_interact"))
		if mode == "quest_zone" and quest_step_id != "":
			var ql := get_node_or_null("/root/QuestLog")
			if ql != null and ql.has_method("mark"):
				ql.call("mark", quest_step_id)

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
			if message != "" and message.length() > 12:
				GameBus.show_dialogue(speaker if speaker != "" else "提示", message)
			else:
				GameBus.show_toast(message if message != "" else "到访打卡")
			interacted.emit(quest_step_id)
		"stamina_sip":
			var cost := gold_cost
			if cost > 0:
				if GameBus.gold < cost:
					GameBus.show_toast("金币不够（需要 %d）" % cost)
					return
				GameBus.add_gold(-cost)
			var amt := stamina_restore if stamina_restore > 0 else 10
			Stamina.restore(amt)
			var tip := message if message != "" else ("恢复精力 +%d" % amt)
			if cost > 0:
				tip = "%s（-%d金）" % [tip, cost]
			GameBus.show_toast(tip)
			QuestLog.mark("mkt_cafe")
			interacted.emit("sip")
			GameBus.save_game()
		"cook":
			_do_cook()
		"eat":
			_do_eat()
		"bulletin":
			_show_bulletin()
		"mail":
			_show_mail()
		"ruin_loot":
			_ruin_loot()
		_:
			GameBus.show_toast(message)
			interacted.emit(message)

func _do_cook() -> void:
	var cooking := get_node_or_null("/root/Cooking")
	if cooking == null:
		GameBus.show_toast("厨房还没准备好")
		return
	var r: Dictionary
	if recipe_id != "":
		r = cooking.call("try_cook", recipe_id)
	else:
		r = cooking.call("try_cook_any")
	if bool(r.get("ok", false)):
		GameBus.save_game()
		GameBus.show_toast(str(r.get("msg", "烹饪完成")))
		SFX.play("ui")
		interacted.emit("cook")
	else:
		GameBus.show_toast(str(r.get("msg", "做不了")))

func _do_eat() -> void:
	var cooking := get_node_or_null("/root/Cooking")
	var fid := food_id
	if fid == "":
		for cand in ["salad", "omelette", "fish_soup", "pumpkin_pie"]:
			if Inventory.count(cand) > 0:
				fid = cand
				break
	if fid == "" or Inventory.count(fid) <= 0:
		GameBus.show_toast("没有可吃的料理（先在灶台烹饪）")
		return
	if cooking != null and bool(cooking.call("eat", fid)):
		GameBus.save_game()
		SFX.play("ui")
		interacted.emit("eat_" + fid)

func _show_bulletin() -> void:
	var weather := "晴"
	var season := "春"
	var w := get_node_or_null("/root/Weather")
	if w != null and w.has_method("weather_cn"):
		weather = str(w.call("weather_cn"))
	var sc := get_node_or_null("/root/SeasonClock")
	if sc != null and sc.has_method("season_cn"):
		season = str(sc.call("season_cn"))
	var hint := QuestLog.current_hint()
	var lines: PackedStringArray = PackedStringArray([
		"【镇告示栏】",
		"· 春季市集筹备中：买种子、卖货、送小礼物。",
		"· 码头渔获不错，可去海边试竿。",
		"· 北缘瀑布回声清亮；遗迹旧箱里或许有纸条。",
		"· 今日：" + season + " · " + weather,
		"· 你的当前事项：" + hint,
	])
	GameBus.show_dialogue("告示栏", "\n".join(lines))
	QuestLog.mark("mkt_board")
	interacted.emit("bulletin")

func _show_mail() -> void:
	var day := TimeClock.day
	var body := "亲爱的农场主：\n\n欢迎来到橡木湾。\n先在米勒农庄锄地播种，\n再去广场看看告示栏吧。\n\n—— 镇长"
	if bool(QuestLog.done.get("explore_farm", false)):
		body = "亲爱的农场主：\n\n听说你已经下田了！\n浇水过夜后作物会长大。\n记得睡在农舍床上。\n\n—— 玛贝尔"
	if bool(QuestLog.done.get("harvest_one", false)):
		body = "亲爱的农场主：\n\n第一批收获真棒。\n去杂货店卖掉，顺便买点种子礼包。\n\n—— 店主"
	if day >= 2 or bool(QuestLog.done.get("done", false)):
		body = "亲爱的农场主：\n\n市集日开始啦！\n买种子、卖货、找花贩小菊聊聊，\n再去咖啡馆暖暖手。\n\n—— 玛贝尔"
	if day >= 3 or bool(QuestLog.done.get("visit_ruins", false)):
		body = "亲爱的农场主：\n\n遗迹那边有人看见闪光。\n若你已路过瀑布，去旧木箱看看纸条，\n再去灯塔看一眼灯火吧。\n\n—— 伊莱"
	if bool(QuestLog.done.get("visit_waterfall", false)):
		body = "亲爱的农场主：\n\n你听见瀑布的回声了。\n纸条说得对——灯塔灯火还亮着，\n去回声湖边看看吧。\n\n—— 伊莱"
	if bool(QuestLog.done.get("visit_lighthouse", false)):
		body = "亲爱的农场主：\n\n灯塔的灯火还亮着。\n橡木湾的日常会一直继续——\n种地、交友、赶集、听雨。\n\n—— 镇长"
	GameBus.show_dialogue("信箱", body)
	interacted.emit("mail")

func _ruin_loot() -> void:
	if bool(QuestLog.done.get("ruin_loot", false)):
		GameBus.show_toast("旧木箱已经空了")
		return
	QuestLog.mark("ruin_loot")
	QuestLog.mark("visit_ruins")
	GameBus.add_gold(15)
	GameBus.save_game()
	GameBus.show_dialogue("旧木箱", "箱子里只有一张发黄的纸条：\n「若你听见瀑布的回声，就去灯塔看一眼灯火。」\n\n（获得 15 金币的旧铜币）")
	SFX.play("chest")
	interacted.emit("ruin_loot")

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
