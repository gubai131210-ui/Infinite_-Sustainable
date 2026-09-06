extends Node
## Loads cozy character lines + schedule from content/characters.json

var _data: Dictionary = {}

func _ready() -> void:
	_load()

func _load() -> void:
	var path := "res://docs/content/characters.json"
	if not FileAccess.file_exists(path):
		push_warning("characters.json missing")
		return
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return
	var parsed: Variant = JSON.parse_string(f.get_as_text())
	f.close()
	if typeof(parsed) == TYPE_DICTIONARY:
		_data = parsed

func has_id(id: String) -> bool:
	return _data.has(id)

func display_name(id: String) -> String:
	if not _data.has(id):
		return id
	return str(_data[id].get("name", id))

func line_for(id: String, period: String = "") -> String:
	if not _data.has(id):
		return "……"
	var entry: Dictionary = _data[id]
	var lines: Dictionary = entry.get("lines", {})
	var p := period
	if p == "":
		var tc := get_node_or_null("/root/TimeClock")
		p = str(tc.get("period")) if tc != null else "day"
	if lines.has(p):
		return str(lines[p])
	if lines.has("day"):
		return str(lines["day"])
	return str(entry.get("fallback", "……"))

func schedule_tile(id: String, period: String = "") -> Vector2:
	if not _data.has(id):
		return Vector2.ZERO
	var sched: Dictionary = _data[id].get("schedule", {})
	var p := period
	if p == "":
		var tc := get_node_or_null("/root/TimeClock")
		p = str(tc.get("period")) if tc != null else "day"
	var key := p
	if not sched.has(key):
		key = "day"
	if not sched.has(key):
		return Vector2.ZERO
	var arr: Array = sched[key]
	if arr.size() < 2:
		return Vector2.ZERO
	return Vector2(float(arr[0]), float(arr[1]))
