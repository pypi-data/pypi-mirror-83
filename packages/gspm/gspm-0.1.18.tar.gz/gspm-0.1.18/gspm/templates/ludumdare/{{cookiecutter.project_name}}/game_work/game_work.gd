extends Node2D

export var settings_config : String = "res://game.cfg"
export var dreamlo_config : String = "res://dreamlo.cfg"


func _ready():
	
	Ludum.start(settings_config, LudumSettingsResource.new())
	DreamLo.load_settings(dreamlo_config)

	Core.change_state(Ludum.GAME_STATE_INIT)
