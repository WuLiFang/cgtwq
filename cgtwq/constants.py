# server defined os string.

OS_WINDOWS = "win"
OS_LINUX = "linux"
OS_MAC = "mac"
OS_UNKNOWN = ""

OS = {
    "windows": OS_WINDOWS,
    "linux": OS_LINUX,
    "darwin": OS_MAC,
}.get(__import__("platform").system().lower(), OS_UNKNOWN)
