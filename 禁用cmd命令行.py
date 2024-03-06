import winreg as reg

def disable_cmd():
    key_path = r"Software\Policies\Microsoft\Windows\System"
    try:
        key = reg.CreateKey(reg.HKEY_CURRENT_USER, key_path)
        reg.SetValueEx(key, "DisableCMD", 0, reg.REG_DWORD, 1)
        print("命令提示符已被禁用。")
    except PermissionError:
        print("权限错误：需要管理员权限来执行此操作。")
    finally:
        if 'key' in locals():
            reg.CloseKey(key)

if __name__ == "__main__":
    disable_cmd()


# 启用cmd命令行
'''
import winreg as reg

def enable_cmd():
    key_path = r"Software\Policies\Microsoft\Windows\System"
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_WRITE)
        reg.DeleteValue(key, "DisableCMD")
        print("命令提示符已被启用。")
    except FileNotFoundError:
        print("找不到设置，命令提示符可能已经是启用状态。")
    except PermissionError:
        print("权限错误：需要管理员权限来执行此操作。")
    except OSError:
        print("可能已经删除了值，命令提示符没有被禁用。")
    finally:
        if 'key' in locals():
            reg.CloseKey(key)

if __name__ == "__main__":
    enable_cmd()

'''