import os
import subprocess
import logging
import shutil
from livekit.agents import function_tool

logger = logging.getLogger(__name__)

# Registry of common apps mapping to executable names / commands
APP_COMMANDS = {
    # Browsers & Text Editors
    "chrome": "chrome",
    "google chrome": "chrome",
    "browser": "chrome",
    "notepad": "notepad",
    "text editor": "notepad",
    "notepad++": "notepad++",
    
    # Development
    "code": "code",
    "vscode": "code",
    "vs code": "code",
    "cmd": "cmd",
    "command prompt": "cmd",
    "powershell": "powershell",
    
    # Utilities & Built-ins
    "calculator": "calc",
    "calc": "calc",
    "paint": "mspaint",
    "mspaint": "mspaint",
    "explorer": "explorer",
    "file explorer": "explorer",
    "task manager": "taskmgr",
    "control panel": "control",
    "settings": "ms-settings:",
    
    # Entertainment & Social
    "spotify": "spotify",
    "discord": "discord",
    "steam": "steam",
    "vlc": "vlc",
    "obs": "obs",
    "slack": "slack",
    "zoom": "zoom",
    "whatsapp": "whatsapp",
    
    # MS Office
    "word": "winword",
    "msword": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "outlook": "outlook"
}

# Apps that are UWP/Store apps and should NOT use os.startfile (it causes error dialogs)
UWP_APPS = {"spotify", "discord", "slack", "zoom", "settings", "calculator", "calc", "ms-settings:"}

@function_tool
async def launch_app(app_name: str, argument: str = None) -> str:
    """
    Launches a local application on the PC.
    You can optionally pass an argument (such as a URL for chrome/browser, or a file path for notepad).
    Common apps include: chrome, notepad, calculator, paint, vscode.
    
    Examples:
    - launch_app("chrome", "youtube.com") -> Opens YouTube in Chrome
    - launch_app("notepad") -> Opens Notepad
    """
    app_key = app_name.lower().strip()
    executable = APP_COMMANDS.get(app_key, app_key)
    
    logger.info(f"Launching application: {app_name} (mapped to '{executable}') with argument: {argument}...")
    
    try:
        if os.name == 'nt':
            # Smarter handling for Chrome to prevent profile picker and open in default profile
            if executable == "chrome":
                if argument:
                    cmd = f'start chrome --profile-directory="Default" "{argument}"'
                else:
                    cmd = 'start chrome --profile-directory="Default"'
                logger.info(f"Executing Chrome command: {cmd}")
                subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"Successfully launched Chrome (Default profile) with URL: {argument}"
                
            # For other apps with arguments
            if argument:
                cmd = f'start "" "{executable}" "{argument}"'
                logger.info(f"Executing command: {cmd}")
                subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"Successfully launched {app_name} with argument: {argument}"
            
            # For UWP/Store apps or unknown apps, use 'start' command via shell
            # This avoids the Windows error dialog that os.startfile triggers for UWP apps
            if app_key in UWP_APPS or executable in UWP_APPS:
                # Try shell 'start' command first (handles UWP apps like Spotify, Discord, etc.)
                cmd = f'start "" "{executable}"'
                logger.info(f"Launching UWP/Store app with: {cmd}")
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                _, stderr = proc.communicate(timeout=3)
                if proc.returncode == 0:
                    return f"Successfully launched {app_name}"
                else:
                    logger.warning(f"Shell start failed for {app_name}, stderr: {stderr}")
                    return f"Failed to launch {app_name}. It may not be installed."
            
            # Standard launch for traditional .exe apps
            # First check if the executable is on PATH
            exe_path = shutil.which(executable) or shutil.which(executable + ".exe")
            if exe_path:
                subprocess.Popen([exe_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"Successfully launched {app_name}"
            
            # Try os.startfile (works for system apps like notepad, calc, mspaint)
            try:
                os.startfile(executable)
                return f"Successfully launched {app_name}"
            except FileNotFoundError:
                # Last resort: shell start
                subprocess.Popen(f'start "" "{executable}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"Successfully launched {app_name} using fallback shell"
        else:
            # Fallback for non-Windows
            if argument:
                subprocess.Popen([executable, argument])
            else:
                subprocess.Popen([executable])
            return f"Successfully launched {app_name}"
            
    except Exception as e:
        logger.error(f"Error launching app '{app_name}': {e}")
        return f"Failed to launch {app_name}. Error: {str(e)}"

