extends Node
## Soft looping BGM + rain bed (P24). Procedural WAV placeholders.

var _bgm: AudioStreamPlayer
var _rain: AudioStreamPlayer

func _ready() -> void:
	_bgm = AudioStreamPlayer.new()
	_bgm.name = "BGM"
	_bgm.volume_db = -18.0
	_bgm.bus = "Master"
	add_child(_bgm)
	_rain = AudioStreamPlayer.new()
	_rain.name = "RainLoop"
	_rain.volume_db = -22.0
	add_child(_rain)
	_bgm.stream = _load_wav("res://assets/sfx/bgm_soft.wav")
	_rain.stream = _load_wav("res://assets/sfx/rain_loop.wav")
	if _bgm.stream != null:
		_bgm.play()
	call_deferred("_bind_weather")
	_bgm.finished.connect(func():
		if _bgm.stream != null:
			_bgm.play()
	)
	_rain.finished.connect(func():
		var w := get_node_or_null("/root/Weather")
		if w != null and bool(w.call("is_raining")) and _rain.stream != null:
			_rain.play()
	)

func _bind_weather() -> void:
	var w := get_node_or_null("/root/Weather")
	if w == null:
		return
	if not w.weather_changed.is_connected(_on_weather):
		w.weather_changed.connect(_on_weather)
	_on_weather(str(w.get("weather")))

func _on_weather(weather_id: String) -> void:
	if weather_id == "rain":
		if _rain.stream != null and not _rain.playing:
			_rain.play()
	else:
		_rain.stop()

func _load_wav(path: String) -> AudioStreamWAV:
	var abs_path := ProjectSettings.globalize_path(path)
	if not FileAccess.file_exists(abs_path):
		return null
	var f := FileAccess.open(abs_path, FileAccess.READ)
	if f == null:
		return null
	var bytes := f.get_buffer(f.get_length())
	f.close()
	if bytes.size() < 44:
		return null
	var pcm := bytes.slice(44)
	var stream := AudioStreamWAV.new()
	stream.format = AudioStreamWAV.FORMAT_16_BITS
	stream.mix_rate = 22050
	stream.stereo = false
	stream.data = pcm
	stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
	stream.loop_begin = 0
	stream.loop_end = int(pcm.size() / 2.0)
	return stream
