extends Node
## Lightweight SFX bus — placeholder WAVs loaded as PCM (P12).

var _players: Dictionary = {}

func _ready() -> void:
	for id in ["footstep", "water", "chest", "sell", "hoe"]:
		var p := AudioStreamPlayer.new()
		p.name = "SFX_%s" % id
		p.volume_db = -6.0
		p.stream = _load_wav("res://assets/sfx/%s.wav" % id)
		add_child(p)
		_players[id] = p

func play(id: String) -> void:
	if not _players.has(id):
		return
	var p: AudioStreamPlayer = _players[id]
	if p.stream == null:
		p.stream = _load_wav("res://assets/sfx/%s.wav" % id)
	if p.stream != null:
		p.play()

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
	# Minimal PCM WAV: assume 16-bit mono from our generator
	var data_offset := 44
	var pcm := bytes.slice(data_offset)
	var stream := AudioStreamWAV.new()
	stream.format = AudioStreamWAV.FORMAT_16_BITS
	stream.mix_rate = 22050
	stream.stereo = false
	stream.data = pcm
	return stream
