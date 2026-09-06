extends Node
## Item catalog + crop definitions + integer buy/sell prices.

const CROPS := {
	"radish": {"name": "萝卜", "waters": 2, "seed": "seed_radish", "item": "radish", "sell": 15},
	"greens": {"name": "青菜", "waters": 3, "seed": "seed_greens", "item": "greens", "sell": 20},
	"wheat": {"name": "小麦", "waters": 4, "seed": "seed_wheat", "item": "wheat", "sell": 25},
	"tomato": {"name": "番茄", "waters": 5, "seed": "seed_tomato", "item": "tomato", "sell": 35},
	"pumpkin": {"name": "南瓜", "waters": 6, "seed": "seed_pumpkin", "item": "pumpkin", "sell": 50},
}

const ITEMS := {
	"hoe": {"name": "锄头", "icon": "res://assets/processed/tool_hoe.png", "kind": "tool"},
	"can": {"name": "水壶", "icon": "res://assets/processed/tool_can.png", "kind": "tool"},
	"axe": {"name": "斧头", "icon": "res://assets/processed/tool_axe.png", "kind": "tool"},
	"rod": {"name": "钓竿", "icon": "res://assets/processed/tool_rod.png", "kind": "tool"},
	"seed_radish": {"name": "萝卜种子", "icon": "res://assets/processed/item_seed_radish.png", "kind": "seed", "crop": "radish", "buy": 8},
	"seed_greens": {"name": "青菜种子", "icon": "res://assets/processed/item_seed_greens.png", "kind": "seed", "crop": "greens", "buy": 10},
	"seed_wheat": {"name": "小麦种子", "icon": "res://assets/processed/item_seed_wheat.png", "kind": "seed", "crop": "wheat", "buy": 12},
	"seed_tomato": {"name": "番茄种子", "icon": "res://assets/processed/item_seed_tomato.png", "kind": "seed", "crop": "tomato", "buy": 16},
	"seed_pumpkin": {"name": "南瓜种子", "icon": "res://assets/processed/item_seed_pumpkin.png", "kind": "seed", "crop": "pumpkin", "buy": 22},
	"radish": {"name": "萝卜", "icon": "res://assets/processed/item_radish.png", "kind": "crop", "sell": 15},
	"greens": {"name": "青菜", "icon": "res://assets/processed/item_greens.png", "kind": "crop", "sell": 20},
	"wheat": {"name": "小麦", "icon": "res://assets/processed/item_wheat.png", "kind": "crop", "sell": 25},
	"tomato": {"name": "番茄", "icon": "res://assets/processed/item_tomato.png", "kind": "crop", "sell": 35},
	"pumpkin": {"name": "南瓜", "icon": "res://assets/processed/item_pumpkin.png", "kind": "crop", "sell": 50},
	"feed": {"name": "饲料", "icon": "res://assets/processed/item_feed.png", "kind": "feed", "buy": 5},
	"fish": {"name": "鱼", "icon": "res://assets/processed/item_fish.png", "kind": "loot", "sell": 18},
	"wood": {"name": "木头", "icon": "res://assets/processed/item_wood.png", "kind": "loot", "sell": 8},
	"egg": {"name": "鸡蛋", "icon": "res://assets/processed/item_egg.png", "kind": "loot", "sell": 12},
	"wool": {"name": "羊毛", "icon": "res://assets/processed/item_wool.png", "kind": "loot", "sell": 20},
	"milk": {"name": "牛奶", "icon": "res://assets/processed/item_milk.png", "kind": "loot", "sell": 25},
	"salad": {"name": "田园沙拉", "icon": "res://assets/processed/item_salad.png", "kind": "food", "sell": 45, "stamina": 25},
	"omelette": {"name": "农家蛋饼", "icon": "res://assets/processed/item_omelette.png", "kind": "food", "sell": 55, "stamina": 35},
	"fish_soup": {"name": "回声湖鱼汤", "icon": "res://assets/processed/item_fish_soup.png", "kind": "food", "sell": 48, "stamina": 30},
	"pumpkin_pie": {"name": "南瓜派", "icon": "res://assets/processed/item_pumpkin_pie.png", "kind": "food", "sell": 70, "stamina": 40},
}

func get_item(id: String) -> Dictionary:
	if ITEMS.has(id):
		return ITEMS[id]
	return {}


func display_name(id: String) -> String:
	if ITEMS.has(id):
		return str(ITEMS[id]["name"])
	return id

func icon_path(id: String) -> String:
	if ITEMS.has(id):
		return str(ITEMS[id]["icon"])
	return ""

func sell_price(id: String) -> int:
	if ITEMS.has(id) and ITEMS[id].has("sell"):
		return int(ITEMS[id]["sell"])
	return 0

func buy_price(id: String) -> int:
	if ITEMS.has(id) and ITEMS[id].has("buy"):
		return int(ITEMS[id]["buy"])
	return 0
