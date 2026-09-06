extends Node
## Simple stack inventory. Tools are always available via hotbar, not consumed.

signal changed

var stacks: Dictionary = {}  # id -> count
var selected_seed: String = "seed_radish"
var selected_gift: String = ""
var selected_inv_index: int = 0

func _ready() -> void:
	reset_start()

func reset_start() -> void:
	stacks = {
		"seed_radish": 8,
		"seed_greens": 6,
		"seed_wheat": 6,
		"seed_tomato": 4,
		"seed_pumpkin": 3,
		"feed": 10,
	}
	selected_seed = "seed_radish"
	changed.emit()

func count(id: String) -> int:
	return int(stacks.get(id, 0))

func has(id: String, n: int = 1) -> bool:
	return count(id) >= n

func add(id: String, n: int = 1) -> void:
	if n <= 0:
		return
	stacks[id] = count(id) + n
	changed.emit()

func remove(id: String, n: int = 1) -> bool:
	if not has(id, n):
		return false
	var left := count(id) - n
	if left <= 0:
		stacks.erase(id)
	else:
		stacks[id] = left
	changed.emit()
	return true

func list_entries() -> Array:
	var out: Array = []
	for k in stacks.keys():
		out.append({"id": str(k), "count": int(stacks[k])})
	out.sort_custom(func(a, b): return str(a["id"]) < str(b["id"]))
	return out

func grant_chest_bonus() -> Dictionary:
	## One-shot chest refill amounts.
	var bonus := {
		"seed_radish": 4,
		"seed_greens": 3,
		"seed_wheat": 3,
		"feed": 5,
	}
	for k in bonus.keys():
		add(str(k), int(bonus[k]))
	return bonus
