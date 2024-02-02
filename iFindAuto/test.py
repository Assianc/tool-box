import win32gui
import win32api
import win32con

def click_covered_window(window_name):
    """
    Clicks the specified window, even if it is covered by other windows.

    Args:
        window_name (str): The name of the window to click.
    """

    # Get the handle of the window
    hwnd = win32gui.FindWindow(None, window_name)

    # Check if the window is active
    if not win32gui.IsWindowEnabled(hwnd):
        # The window is not active. Bring it to the front.
        win32gui.SetForegroundWindow(hwnd)

    # Check if the window is visible
    if not win32gui.IsWindowVisible(hwnd):
        # The window is not visible. Show it.
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

    # Get the window's position and size
    rect = win32gui.GetWindowRect(hwnd)

    # Calculate the coordinates of the center of the window
    x = int((rect[0] + rect[2]) / 2)
    y = int((rect[1] + rect[3]) / 2)

    # Click the window at the center
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

# Example usage
click_covered_window("同花顺iFinD - [可转债研究]")
