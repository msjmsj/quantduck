import re
from pathlib import Path

def update_version_in_file(file_path: str, new_version: str, pattern: str, replacement: str) -> None:
    """更新指定文件中的版本号"""
    path = Path(file_path)
    content = path.read_text()
    new_content = re.sub(pattern, replacement.format(new_version), content)
    path.write_text(new_content)

def increment_version():
    """增加版本号的补丁号并更新所有相关文件"""
    # 从 __init__.py 读取当前版本
    init_file = Path("quantduck/__init__.py")
    content = init_file.read_text()
    
    # 查找版本号
    version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not version_match:
        raise ValueError("Version not found in __init__.py")
    
    # 解析版本号
    current_version = version_match.group(1)
    major, minor, patch = map(int, current_version.split('.'))
    
    # 增加补丁号
    new_version = f"{major}.{minor}.{patch + 1}"
    
    # 更新 __init__.py
    update_version_in_file(
        "quantduck/__init__.py",
        new_version,
        r'__version__\s*=\s*["\']([^"\']+)["\']',
        '__version__ = "{}"'
    )
    
    # 更新 setup.py
    update_version_in_file(
        "setup.py",
        new_version,
        r'version\s*=\s*["\']([^"\']+)["\']',
        'version="{}"'
    )
    
    # 更新 pyproject.toml
    update_version_in_file(
        "pyproject.toml",
        new_version,
        r'version\s*=\s*["\']([^"\']+)["\']',
        'version = "{}"'
    )
    
    return new_version

if __name__ == "__main__":
    new_version = increment_version()
    print(f"Version updated to {new_version}") 