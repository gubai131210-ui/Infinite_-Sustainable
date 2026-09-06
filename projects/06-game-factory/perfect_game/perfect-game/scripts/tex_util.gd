extends Node
## Autoload texture loader â€?editor + exported PCK safe.

func load_tex(path: String) -> Texture2D:
	if ResourceLoader.exists(path):
		var cached := load(path) as Texture2D
		if cached != null:
			return cached
	var abs_path := ProjectSettings.globalize_path(path)
	if FileAccess.file_exists(abs_path):
		var img := Image.new()
		if img.load(abs_path) == OK:
			return ImageTexture.create_from_image(img)
	return null
