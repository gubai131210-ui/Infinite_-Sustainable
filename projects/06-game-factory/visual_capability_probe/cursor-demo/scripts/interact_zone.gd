extends Area2D

@export var prompt_text: String = "按 E 敲门"
@export var message: String = "木门关着。夜里再来吧。"

signal interacted(message: String)

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("player") and body.has_method("set_interact_prompt"):
		body.set_interact_prompt(prompt_text, Callable(self, "_do_interact"))

func _on_body_exited(body: Node2D) -> void:
	if body.is_in_group("player") and body.has_method("clear_interact_prompt"):
		body.clear_interact_prompt()

func _do_interact() -> void:
	var toast := get_node_or_null("/root/Main/HUD/Margin/VBox/ToastLabel") as Label
	if toast != null:
		toast.text = message
	var hud := get_node_or_null("/root/Main/HUD")
	if hud != null and hud.has_method("show_toast"):
		hud.show_toast(message, 3.0)
	interacted.emit(message)
