extends Node
## Kitchen recipes — cozy cooking (P22).

const RECIPES := {
	"salad": {
		"name": "田园沙拉",
		"need": {"greens": 1, "radish": 1, "tomato": 1},
		"stamina": 25,
		"sell": 45,
	},
	"omelette": {
		"name": "农家蛋饼",
		"need": {"egg": 1, "milk": 1, "wheat": 1},
		"stamina": 35,
		"sell": 55,
	},
	"fish_soup": {
		"name": "回声湖鱼汤",
		"need": {"fish": 1, "greens": 1},
		"stamina": 30,
		"sell": 48,
	},
	"pumpkin_pie": {
		"name": "南瓜派",
		"need": {"pumpkin": 1, "wheat": 1, "egg": 1},
		"stamina": 40,
		"sell": 70,
	},
}

func recipe_ids() -> Array:
	return RECIPES.keys()

func display_name(id: String) -> String:
	if RECIPES.has(id):
		return str(RECIPES[id]["name"])
	return id

func can_cook(id: String) -> bool:
	if not RECIPES.has(id):
		return false
	var need: Dictionary = RECIPES[id]["need"]
	for k in need.keys():
		if Inventory.count(str(k)) < int(need[k]):
			return false
	return true

func try_cook(id: String) -> Dictionary:
	if not RECIPES.has(id):
		return {"ok": false, "msg": "未知菜谱"}
	if not can_cook(id):
		var need: Dictionary = RECIPES[id]["need"]
		var parts: PackedStringArray = PackedStringArray()
		for k in need.keys():
			parts.append("%s×%d" % [ItemDB.display_name(str(k)), int(need[k])])
		return {"ok": false, "msg": "材料不够（需要 %s）" % "、".join(parts)}
	var need2: Dictionary = RECIPES[id]["need"]
	for k in need2.keys():
		Inventory.remove(str(k), int(need2[k]))
	Inventory.add(id, 1)
	return {"ok": true, "msg": "做好了%s" % display_name(id)}

func try_cook_any() -> Dictionary:
	for id in RECIPES.keys():
		if can_cook(str(id)):
			return try_cook(str(id))
	return {"ok": false, "msg": "材料不够：沙拉/蛋饼/鱼汤/南瓜派"}

func cook(id: String) -> bool:
	return bool(try_cook(id).get("ok", false))

func eat(id: String) -> bool:
	if Inventory.count(id) <= 0:
		return false
	var restore := 20
	if RECIPES.has(id):
		restore = int(RECIPES[id]["stamina"])
	elif ItemDB.get_item(id).has("stamina"):
		restore = int(ItemDB.get_item(id)["stamina"])
	Inventory.remove(id, 1)
	Stamina.restore(restore)
	GameBus.show_toast("吃了%s，精力 +%d" % [ItemDB.display_name(id), restore])
	return true
