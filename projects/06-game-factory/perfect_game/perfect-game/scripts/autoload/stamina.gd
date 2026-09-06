extends Node
## Player stamina — integer points, tool spend, sleep restore.

signal energy_changed(current: int, maximum: int)

const MAX_ENERGY := 100

var energy: int = MAX_ENERGY

func _ready() -> void:
	energy_changed.emit(energy, MAX_ENERGY)

func spend(amount: int, reason: String = "") -> bool:
	if amount <= 0:
		return true
	if energy < amount:
		GameBus.show_toast("太累了，回农舍睡一觉吧")
		return false
	energy = maxi(energy - amount, 0)
	energy_changed.emit(energy, MAX_ENERGY)
	if energy <= 15 and reason != "":
		GameBus.show_toast("精力不足，注意休息")
	return true

func restore_full() -> void:
	energy = MAX_ENERGY
	energy_changed.emit(energy, MAX_ENERGY)

func restore(amount: int) -> void:
	energy = mini(energy + amount, MAX_ENERGY)
	energy_changed.emit(energy, MAX_ENERGY)
