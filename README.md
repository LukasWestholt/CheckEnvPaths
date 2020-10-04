# CheckEnvPaths
 Windows: Look for duplicate and nonexistent environment paths

User Variables\
HKEY_CURRENT_USER\Environment

System Variables\
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment

if you want to edit the environment paths then you have to set `demo = True` to `demo = False` in [main.py](main.py#L88)