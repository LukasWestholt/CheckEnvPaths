import os
import winreg

r"""
TASK

Look for duplicate and nonexistent environment paths

User Variables
HKEY_CURRENT_USER\Environment

System Variables
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment

"""


def path_exists(path):
    return os.path.exists(path)


def get(key, path, name):
    with winreg.OpenKey(key, path, 0, winreg.KEY_READ) as registry_key:
        value = str(winreg.QueryValueEx(registry_key, name)[0])
        winreg.CloseKey(registry_key)
        return value


def edit(key, path, name, value):
    if demo:
        print("DEMO MODE - NO CHANGES")
        return False
    with winreg.OpenKey(key, path, 0, winreg.KEY_WRITE) as registry_key:
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
    return True


def clear(key, path, name, value_list):
    print("SOURCE: " + ';'.join(value_list))

    seen = set()
    uniq_paths = []
    not_uniq_paths = []
    for x in value_list:
        x = os.path.expandvars(os.path.normpath(x.strip()))
        if x not in seen:
            uniq_paths.append(x)
            seen.add(x)
        else:
            not_uniq_paths.append(x)
    print("Duplicate paths that will be deleted: " + str(not_uniq_paths))

    valid_paths = []
    non_valid_paths = []
    for x in uniq_paths:
        if path_exists(x):
            valid_paths.append(x)
        else:
            non_valid_paths.append(x)
    print("Invalid paths that will be deleted: " + str(non_valid_paths))

    if valid_paths == value_list:
        print("EVERYTHING FINE - NO CHANGES")
        return True
    success = edit(key, path, name, ';'.join(valid_paths))
    if not success:
        return False
    result_value = get(key, path, name)
    print("Successfully changed registry" if result_value == ';'.join(valid_paths) else "Failing on changing registry")
    print("RESULT: " + result_value)
    return result_value.split(";")


def run():
    # User Variables
    value_list = get(winreg.HKEY_CURRENT_USER, "Environment", "Path").split(";")
    clear(winreg.HKEY_CURRENT_USER, "Environment", "Path", value_list)

    # System Variables
    value = get(winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", "Path").split(";")
    clear(winreg.HKEY_LOCAL_MACHINE,
          r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", "Path", value)


if __name__ == '__main__':
    demo = True
    run()
