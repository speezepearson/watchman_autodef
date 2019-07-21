import json
import re
import subprocess
from pathlib import Path
from typing import Any, Set

CONFIG_FILENAME = '.watchman-autodef.json'
AUTODEF_PREFIX = 'autodef.'
RELOADER_NAME = 'autodef-reload'

def get_autodefd_names(dir: Path) -> Set[str]:
    j = json.loads(subprocess.check_output(['watchman', 'trigger-list', str(dir)]))
    if 'error' in j:
        raise RuntimeError(f'watchman trigger-list failed: {j["error"]}')
    assert 'triggers' in j
    return {
        trigger['name']
        for trigger in j['triggers']
        if trigger['name'].startswith(AUTODEF_PREFIX)
    }

def update(dir: Path) -> None:
    current_triggers = json.load((dir/CONFIG_FILENAME).open())['triggers']
    for trigger in current_triggers:
        trigger['name'] = AUTODEF_PREFIX + trigger['name']
    current_triggers.append({
        'name': RELOADER_NAME,
        'expression': ['pcre', f'^{re.escape(CONFIG_FILENAME)}$', 'wholename'],
        'command': ['watchman-autodef'],
        'append_files': False,
    })

    for name in get_autodefd_names(dir) - {trigger['name'] for trigger in current_triggers}:
        subprocess.check_call(['watchman', 'trigger-del', str(dir), name])
    for trigger in current_triggers:
        subprocess.run(
            ['watchman', '-j'],
            input=json.dumps(['trigger', str(dir), trigger]).encode('utf8'),
            cwd=dir,
        )

def unload(dir: Path) -> None:
    subprocess.check_call(['watchman', 'trigger-del', str(dir), RELOADER_NAME])
    for name in get_autodefd_names(dir):
        subprocess.check_call(['watchman', 'trigger-del', str(dir), name])
