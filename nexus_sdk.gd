// NEXUS Game SDK - Godot (GDScript)
// Production-grade client for GD4
extends Node

const BACKEND_URL = "http://127.0.0.1:7000"
var player_id: String
var initialized: bool = false
var session_meta: Dictionary = {}
var http_client: HTTPClient

func _ready():
	add_to_group("nexus_sdk")

func initialize(pid: String, url: String = BACKEND_URL):
	if initialized:
		return
	player_id = pid
	initialized = true
	http_client = HTTPClient.new()
	
	session_meta = {
		"device_model": OS.get_model_info(),
		"os": OS.get_name(),
		"screen_size": get_viewport().get_visible_rect().size,
		"ram_mb": OS.get_static_memory_usage() / 1024 / 1024
	}
	
	print("[NEXUS] Initialized GDScript SDK for %s" % player_id)
	get_tree().create_timer(30.0).timeout.connect(_on_heartbeat)

func _on_heartbeat():
	if initialized:
		send_telemetry("heartbeat", {
			"fps": Engine.get_frames_per_second(),
			"memory_mb": int(OS.get_static_memory_usage() / 1024 / 1024)
		})
		get_tree().create_timer(30.0).timeout.connect(_on_heartbeat)

func submit_score(score: int, meta: Dictionary = {}) -> void:
	var data = {
		"player_id": player_id,
		"score": score,
		"meta": meta
	}
	post_request("/leaderboard/submit", data)

func send_telemetry(event: String, payload: Dictionary = {}) -> void:
	var data = {
		"player_id": player_id,
		"event": event,
		"payload": payload
	}
	post_request("/telemetry", data)

func report_crash(stacktrace: String, device_info: Dictionary = {}) -> void:
	var data = {
		"player_id": player_id,
		"stacktrace": stacktrace,
		"device_info": device_info if device_info else session_meta
	}
	post_request("/crash", data)

func get_leaderboard(limit: int = 50, callback: Callable = Callable()) -> void:
	get_request("/leaderboard/top?limit=%d" % limit, callback)

func get_feature_flags(callback: Callable = Callable()) -> void:
	get_request("/feature-flags", callback)

func get_ab_variant(callback: Callable = Callable()) -> void:
	get_request("/ab-variant?player_id=%s" % player_id, callback)

func post_request(endpoint: String, data: Dictionary) -> void:
	var request = HTTPRequest.new()
	add_child(request)
	var url = BACKEND_URL + endpoint
	request.request(url, ["Content-Type: application/json"], HTTPClient.METHOD_POST, JSON.stringify(data))
	await request.request_completed
	request.queue_free()

func get_request(endpoint: String, callback: Callable) -> void:
	var request = HTTPRequest.new()
	add_child(request)
	var url = BACKEND_URL + endpoint
	var result = await request.request(url)
	if result == OK:
		var response_code = request.get_response_code()
		var response_body = request.get_response_body_as_text()
		if callback.is_valid():
			callback.call(JSON.parse_string(response_body))
	request.queue_free()

func _exit_tree():
	initialized = false
