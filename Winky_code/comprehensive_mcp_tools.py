"""
Comprehensive MCP Tools - Multi-purpose tools server
Includes: System info, file ops, image analysis, web fetch, text processing, etc.
"""

import os
import json
import subprocess
import platform
import psutil
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
import requests
from pathlib import Path

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ComprehensiveMCPTools:
    """Comprehensive suite of tools - 20+ utilities"""

    # ============ SYSTEM INFORMATION TOOLS ============

    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get comprehensive system information"""
        try:
            return {
                "os": platform.system(),
                "os_version": platform.release(),
                "processor": platform.processor(),
                "cpu_cores": psutil.cpu_count(logical=True),
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "memory_used_gb": psutil.virtual_memory().used / (1024**3),
                "memory_total_gb": psutil.virtual_memory().total / (1024**3),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage("/").percent,
                "hostname": platform.node(),
                "python_version": platform.python_version(),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        """Get detailed CPU metrics"""
        try:
            return {
                "physical_cores": psutil.cpu_count(logical=False),
                "total_cores": psutil.cpu_count(logical=True),
                "usage_percent": psutil.cpu_percent(interval=1),
                "frequency_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else None,
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_memory_info() -> Dict[str, Any]:
        """Get detailed memory statistics"""
        try:
            mem = psutil.virtual_memory()
            return {
                "total_gb": round(mem.total / (1024**3), 2),
                "used_gb": round(mem.used / (1024**3), 2),
                "available_gb": round(mem.available / (1024**3), 2),
                "percent_used": mem.percent
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_processes() -> Dict[str, Any]:
        """Get running processes information"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])[:10]:
                processes.append({
                    "name": proc.info['name'],
                    "pid": proc.info['pid'],
                    "cpu_percent": proc.info['cpu_percent'],
                    "memory_mb": proc.info['memory_percent']
                })
            return {"processes": processes, "count": len(psutil.pids())}
        except Exception as e:
            return {"error": str(e)}

    # ============ FILE OPERATIONS ============

    @staticmethod
    def read_file(file_path: str) -> Dict[str, Any]:
        """Read file contents safely"""
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            return {
                "success": True,
                "file": file_path,
                "size_bytes": os.path.getsize(file_path),
                "content": content[:2000]
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def list_directory(path: str = ".") -> Dict[str, Any]:
        """List directory contents"""
        try:
            if not os.path.isdir(path):
                return {"error": f"Directory not found: {path}"}

            items = []
            for item in os.listdir(path)[:50]:
                item_path = os.path.join(path, item)
                items.append({
                    "name": item,
                    "type": "dir" if os.path.isdir(item_path) else "file",
                    "size_mb": round(os.path.getsize(item_path) / (1024**2), 2) if os.path.isfile(item_path) else None
                })

            return {"path": path, "items": items}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """Get detailed file metadata"""
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}

            stat = os.stat(file_path)
            return {
                "path": file_path,
                "size_mb": round(stat.st_size / (1024**2), 2),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "is_file": os.path.isfile(file_path),
                "is_dir": os.path.isdir(file_path)
            }
        except Exception as e:
            return {"error": str(e)}

    # ============ IMAGE TOOLS ============

    @staticmethod
    def analyze_image(image_path: str) -> Dict[str, Any]:
        """Analyze image properties"""
        if not HAS_PIL:
            return {"error": "PIL/Pillow not installed"}

        try:
            if not os.path.exists(image_path):
                return {"error": f"Image not found: {image_path}"}

            img = Image.open(image_path)
            return {
                "format": img.format,
                "width": img.width,
                "height": img.height,
                "mode": img.mode,
                "size_mb": round(os.path.getsize(image_path) / (1024**2), 2)
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def list_images(directory: str = ".") -> Dict[str, Any]:
        """Find all images in directory"""
        try:
            image_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
            images = []

            if os.path.isdir(directory):
                for file in os.listdir(directory)[:50]:
                    if os.path.splitext(file)[1].lower() in image_exts:
                        images.append({
                            "name": file,
                            "path": os.path.join(directory, file)
                        })

            return {"directory": directory, "count": len(images), "images": images}
        except Exception as e:
            return {"error": str(e)}

    # ============ WEB TOOLS ============

    @staticmethod
    def fetch_url(url: str, max_chars: int = 2000) -> Dict[str, Any]:
        """Fetch and preview URL content"""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=8)

            return {
                "url": url,
                "status": response.status_code,
                "content_length": len(response.text),
                "content": response.text[:max_chars],
                "success": response.status_code < 400
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def check_url(url: str) -> Dict[str, Any]:
        """Check if URL is accessible"""
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            return {
                "url": url,
                "accessible": response.status_code < 400,
                "status": response.status_code,
                "reason": response.reason
            }
        except Exception as e:
            return {"error": str(e), "url": url, "accessible": False}

    # ============ TEXT TOOLS ============

    @staticmethod
    def count_words(text: str) -> Dict[str, Any]:
        """Analyze text statistics"""
        lines = text.split("\n")
        words = text.split()

        return {
            "characters": len(text),
            "words": len(words),
            "lines": len(lines),
            "paragraphs": len([l for l in lines if l.strip()]),
            "avg_word_length": round(len(text) / len(words), 2) if words else 0
        }

    @staticmethod
    def reverse_text(text: str) -> Dict[str, Any]:
        """Reverse text"""
        return {"original": text[:50], "reversed": text[::-1], "length": len(text)}

    # ============ JSON TOOLS ============

    @staticmethod
    def parse_json(json_string: str) -> Dict[str, Any]:
        """Parse JSON safely"""
        try:
            data = json.loads(json_string)
            return {"success": True, "data": data, "type": type(data).__name__}
        except Exception as e:
            return {"error": f"JSON parse error: {str(e)}"}

    @staticmethod
    def format_json(data_dict: Dict) -> Dict[str, Any]:
        """Format JSON beautifully"""
        try:
            formatted = json.dumps(data_dict, indent=2)
            return {"success": True, "formatted": formatted[:1000]}
        except Exception as e:
            return {"error": str(e)}

    # ============ CODE ANALYSIS ============

    @staticmethod
    def analyze_python_file(file_path: str) -> Dict[str, Any]:
        """Analyze Python file structure"""
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found"}

            with open(file_path, 'r') as f:
                lines = f.readlines()

            functions = [l.strip() for l in lines if l.strip().startswith("def ")]
            classes = [l.strip() for l in lines if l.strip().startswith("class ")]

            return {
                "lines": len(lines),
                "functions_count": len(functions),
                "classes_count": len(classes),
                "functions": functions[:5],
                "classes": classes[:5]
            }
        except Exception as e:
            return {"error": str(e)}

    # ============ UTILITY TOOLS ============

    @staticmethod
    def get_datetime() -> Dict[str, Any]:
        """Get current date and time in multiple formats"""
        now = datetime.now()
        return {
            "iso": now.isoformat(),
            "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "day": now.strftime("%A"),
            "unix": int(now.timestamp())
        }

    @staticmethod
    def calculate(expression: str) -> Dict[str, Any]:
        """Safe calculator"""
        try:
            # Only allow safe operations
            result = eval(expression, {"__builtins__": {}}, {"pi": 3.14159, "e": 2.71828})
            return {"expression": expression, "result": result}
        except Exception as e:
            return {"error": f"Calculation error: {str(e)}"}

    @staticmethod
    def uuid_generator() -> Dict[str, Any]:
        """Generate random UUIDs"""
        import uuid
        return {
            "uuid4": str(uuid.uuid4()),
            "uuid1": str(uuid.uuid1()),
            "timestamp": datetime.now().isoformat()
        }


# Tool registry for easy access
COMPREHENSIVE_TOOLS = {
    # System
    "system_info": ComprehensiveMCPTools.get_system_info,
    "cpu_info": ComprehensiveMCPTools.get_cpu_info,
    "memory_info": ComprehensiveMCPTools.get_memory_info,
    "processes": ComprehensiveMCPTools.get_processes,

    # Files
    "read_file": ComprehensiveMCPTools.read_file,
    "list_directory": ComprehensiveMCPTools.list_directory,
    "file_info": ComprehensiveMCPTools.get_file_info,

    # Images
    "analyze_image": ComprehensiveMCPTools.analyze_image,
    "list_images": ComprehensiveMCPTools.list_images,

    # Web
    "fetch_url": ComprehensiveMCPTools.fetch_url,
    "check_url": ComprehensiveMCPTools.check_url,

    # Text
    "count_words": ComprehensiveMCPTools.count_words,
    "reverse_text": ComprehensiveMCPTools.reverse_text,

    # JSON
    "parse_json": ComprehensiveMCPTools.parse_json,
    "format_json": ComprehensiveMCPTools.format_json,

    # Code
    "analyze_python": ComprehensiveMCPTools.analyze_python_file,

    # Utility
    "datetime": ComprehensiveMCPTools.get_datetime,
    "calculate": ComprehensiveMCPTools.calculate,
    "uuid": ComprehensiveMCPTools.uuid_generator,
}

if __name__ == "__main__":
    print("System Info:", ComprehensiveMCPTools.get_system_info())
    print("\nMemory Info:", ComprehensiveMCPTools.get_memory_info())
    print("\nDate/Time:", ComprehensiveMCPTools.get_datetime())
