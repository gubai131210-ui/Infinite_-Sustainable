extends Node
## Global game helpers / toast bridge.

signal toast(text: String)
signal dialogue(speaker: String, text: String)
signal dialogue_closed

var chest_claimed: bool = false
var inventory_open: bool = false
var dialogue_open: bool = false

func show_toast(text: String) -> void:
	toast.emit(text)

func show_dialogue(speaker: String, text: String) -> void:
	dialogue_open = true
	dialogue.emit(speaker, text)

func close_dialogue() -> void:
	dialogue_open = false
	dialogue_closed.emit()
