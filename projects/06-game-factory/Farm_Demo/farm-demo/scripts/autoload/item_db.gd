extends Node
## Item catalog + crop definitions.

const CROPS := {
	"radish": {"name": "萝卜", "waters": 2, "seed": "seed_radish", "item": "radish"},
	"greens": {"name": "青菜", "waters": 3, "seed": "seed_greens", "item": "greens"},
	"wheat": {"name": "小麦", "waters": 4, "seed": "seed_wheat", "item": "wheat"},
	"tomato": {"name": "番茄", "waters": 5, "seed": "seed_tomato", "item": "tomato"},
	"pumpkin": {"name": "南瓜", "waters": 6, "seed": "seed_pumpkin", "item": "pumpkin"},
}

const ITEMS := {
	"hoe": {"name": "锄头", "icon": "res://assets/processed/tool_hoe.png", "kind": "tool"},
	"can": {"name": "水壶", "icon": "res://assets/processed/tool_can.png", "kind": "tool"},
	"axe": {"name": "斧头", "icon": "res://assets/processed/tool_axe.png", "kind": "tool"},
	"rod": {"name": "钓竿", "icon": "res://assets/processed/tool_rod.png", "kind": "tool"},
	"seed_radish": {"name": "萝卜种子", "icon": "res://assets/processed/item_seed_radish.png", "kind": "seed", "crop": "radish"},
	"seed_greens": {"name": "青菜种子", "icon": "res://assets/processed/item_seed_greens.png", "kind": "seed", "crop": "greens"},
	"seed_wheat": {"name": "小麦种子", "icon": "res://assets/processed/item_seed_wheat.png", "kind": "seed", "crop": "wheat"},
	"seed_tomato": {"name": "番茄种子", "icon": "res://assets/processed/item_seed_tomato.png", "kind": "seed", "crop": "tomato"},
	"seed_pumpkin": {"name": "南瓜种子", "icon": "res://assets/processed/item_seed_pumpkin.png", "kind": "seed", "crop": "pumpkin"},
	"radish": {"name": "萝卜", "icon": "res://assets/processed/item_radish.png", "kind": "crop"},
	"greens": {"name": "青菜", "icon": "res://assets/processed/item_greens.png", "kind": "crop"},
	"wheat": {"name": "小麦", "icon": "res://assets/processed/item_wheat.png", "kind": "crop"},
	"tomato": {"name": "番茄", "icon": "res://assets/processed/item_tomato.png", "kind": "crop"},
	"pumpkin": {"name": "南瓜", "icon": "res://assets/processed/item_pumpkin.png", "kind": "crop"},
	"feed": {"name": "饲料", "icon": "res://assets/processed/item_feed.png", "kind": "feed"},
	"fish": {"name": "鱼", "icon": "res://assets/processed/item_fish.png", "kind": "loot"},
	"wood": {"name": "木头", "icon": "res://assets/processed/item_wood.png", "kind": "loot"},
}

func display_name(id: String) -> String:
	if ITEMS.has(id):
		return str(ITEMS[id]["name"])
	return id

func icon_path(id: String) -> String:
	if ITEMS.has(id):
		return str(ITEMS[id]["icon"])
	return ""
