from simplepush import send, send_encrypted

key = "bmKBdH"

send(key, "This is a test", "Hello", "event")

send_encrypted(key, "password", "salt", "title", "message", "event")