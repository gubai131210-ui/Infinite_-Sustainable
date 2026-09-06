extends Node
## Lightweight season spine (P17) — visual leaf/crop tint by season.

signal season_changed(season: String)

const SEASONS := ["spring", "summer", "autumn", "winter"]
const DAYS_PER_SEASON := 7

var season: String = "spring"
var season_day: int = 1

func _ready() -> void:
	if not TimeClock.day_changed.is_connected(_on_day):
		TimeClock.day_changed.connect(_on_day)
	_sync_from_day(TimeClock.day)

func _on_day(day: int) -> void:
	_sync_from_day(day)

func _sync_from_day(day: int) -> void:
	var idx := int(floori(float(maxi(day - 1, 0)) / float(DAYS_PER_SEASON))) % SEASONS.size()
	var next: String = SEASONS[idx]
	season_day = ((day - 1) % DAYS_PER_SEASON) + 1
	if next != season:
		season = next
		season_changed.emit(season)

func season_cn() -> String:
	match season:
		"spring":
			return "春"
		"summer":
			return "夏"
		"autumn":
			return "秋"
		"winter":
			return "冬"
	return season

func world_tint() -> Color:
	match season:
		"spring":
			return Color(1.02, 1.05, 1.0, 1.0)
		"summer":
			return Color(1.06, 1.02, 0.95, 1.0)
		"autumn":
			return Color(1.08, 0.92, 0.78, 1.0)
		"winter":
			return Color(0.88, 0.92, 1.05, 1.0)
	return Color.WHITE

func crop_modulate() -> Color:
	match season:
		"autumn":
			return Color(1.1, 0.95, 0.75, 1.0)
		"winter":
			return Color(0.85, 0.9, 1.0, 1.0)
		_:
			return Color.WHITE
