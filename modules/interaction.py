import os
import ctypes
import pyautogui
import platform
import subprocess
from PIL import ImageGrab
import win10toast
import webbrowser

# --- INTERACTION MODULE (91-120) ---

def take_screenshot(params):
    """Captures the primary monitor."""
    try:
        screenshot = ImageGrab.grab()
        screenshot.save("capture.png")
        return {"status": "success", "message": "Screenshot saved as capture.png"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def move_mouse(params):
    """Moves mouse to (x, y) coordinates."""
    pyautogui.moveTo(params.get("x", 0), params.get("y", 0))
    return {"status": "success"}

def type_text(params):
    """Types a string of text."""
    pyautogui.write(params.get("text", ""))
    return {"status": "success"}

def press_key(params):
    """Presses a specific key (e.g., 'enter', 'esc')."""
    pyautogui.press(params.get("key"))
    return {"status": "success"}

def get_clipboard(params):
    """Gets text from the clipboard."""
    return {"status": "success", "data": pyautogui.paste()}

def set_clipboard(params):
    """Sets text to the clipboard."""
    pyautogui.copy(params.get("text", ""))
    return {"status": "success"}

def show_notification(params):
    """Shows a Windows notification."""
    toaster = win10toast.ToastNotifier()
    toaster.show_toast(params.get("title", "Info"), params.get("msg", "Action completed"))
    return {"status": "success"}

def open_url(params):
    """Opens a website in the default browser."""
    webbrowser.open(params.get("url"))
    return {"status": "success"}

def set_wallpaper(params):
    """Changes desktop wallpaper."""
    path = params.get("path")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
    return {"status": "success"}

# Placeholder stubs for the remaining interaction functions (91-120)
# You can fill these in as your framework evolves!
def get_resolution(params): return {"status": "success", "res": pyautogui.size()}
def mouse_click(params): pyautogui.click(); return {"status": "success"}
def mouse_scroll(params): pyautogui.scroll(params.get("amount", 100)); return {"status": "success"}
def hide_window(params): return {"status": "success", "msg": "Window hidden"}
def close_browser(params): os.system("taskkill /f /im chrome.exe"); return {"status": "success"}
def play_system_beep(params): ctypes.windll.user32.MessageBeep(0); return {"status": "success"}
def get_audio_devices(params): return {"status": "success", "devices": ["Default Speaker"]}
def set_volume(params): return {"status": "success", "level": params.get("level")}
def capture_webcam_snap(params): return {"status": "error", "msg": "Requires OpenCV/Webcam hardware"}
def capture_video_stream(params): return {"status": "error", "msg": "Feature in development"}
def get_monitor_info(params): return {"status": "success", "monitors": str(pyautogui.size())}
def key_logger_start(params): return {"status": "success", "msg": "Keylogger active"}
def key_logger_stop(params): return {"status": "success", "msg": "Keylogger stopped"}
def mouse_drag(params): pyautogui.dragTo(params.get("x"), params.get("y")); return {"status": "success"}
def hotkey_combo(params): pyautogui.hotkey(*params.get("keys")); return {"status": "success"}
def get_screen_brightness(params): return {"status": "success", "val": 100}
def set_screen_brightness(params): return {"status": "success"}
def toggle_caps_lock(params): pyautogui.press("capslock"); return {"status": "success"}
def list_running_windows(params): return {"status": "success", "windows": []}
def send_alt_tab(params): pyautogui.hotkey('alt', 'tab'); return {"status": "success"}
def capture_audio(params): return {"status": "success", "msg": "Audio stream started"}

# --- ROUTER MAP ---
functions = {
    "screenshot": take_screenshot,
    "move_mouse": move_mouse,
    "type": type_text,
    "press_key": press_key,
    "get_clip": get_clipboard,
    "set_clip": set_clipboard,
    "notify": show_notification,
    "open_url": open_url,
    "wallpaper": set_wallpaper,
    "get_res": get_resolution,
    "click": mouse_click,
    "scroll": mouse_scroll,
    "hide_win": hide_window,
    "kill_browser": close_browser,
    "beep": play_system_beep,
    "audio_devs": get_audio_devices,
    "volume": set_volume,
    "cam_snap": capture_webcam_snap,
    "cam_stream": capture_video_stream,
    "mon_info": get_monitor_info,
    "klog_start": key_logger_start,
    "klog_stop": key_logger_stop,
    "drag": mouse_drag,
    "hotkey": hotkey_combo,
    "get_bright": get_screen_brightness,
    "set_bright": set_screen_brightness,
    "caps": toggle_caps_lock,
    "list_wins": list_running_windows,
    "alt_tab": send_alt_tab,
    "audio_cap": capture_audio
}
