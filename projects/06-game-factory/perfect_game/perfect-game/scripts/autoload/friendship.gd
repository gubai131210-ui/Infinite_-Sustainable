extends Node
## Cozy friendship hearts + gift reactions (P16).

signal friendship_changed(npc_id: String, hearts: int)

## npc_id -> hearts 0..5
var hearts: Dictionary = {}

const GIFTABLE_KINDS := ["crop", "loot", "feed"]
const MAX_HEARTS := 5

func hearts_of(npc_id: String) -> int:
	return clampi(int(hearts.get(npc_id, 0)), 0, MAX_HEARTS)

func can_gift(item_id: String) -> bool:
	if not ItemDB.ITEMS.has(item_id):
		return false
	var kind := str(ItemDB.ITEMS[item_id].get("kind", ""))
	return kind in GIFTABLE_KINDS

func try_gift(npc_id: String, item_id: String) -> bool:
	if not can_gift(item_id):
		return false
	if not Inventory.has(item_id, 1):
		return false
	Inventory.remove(item_id, 1)
	var h := hearts_of(npc_id) + 1
	hearts[npc_id] = mini(h, MAX_HEARTS)
	friendship_changed.emit(npc_id, hearts[npc_id])
	QuestLog.mark("mkt_gift")
	GameBus.save_game()
	return true

func gift_line(npc_id: String, item_id: String) -> String:
	var h := hearts_of(npc_id)
	var item_name := ItemDB.display_name(item_id)
	match h:
		0, 1:
			return "谢谢你的%s，我收下啦。" % item_name
		2, 3:
			return "又给我%s？真贴心，我们更熟了。" % item_name
		_:
			return "有你这份%s，今天都亮堂了。友谊心满满！" % item_name

func warm_line_suffix(npc_id: String) -> String:
	var h := hearts_of(npc_id)
	if h >= 4:
		return "（你俩很熟了）"
	if h >= 2:
		return "（有点熟络）"
	return ""
