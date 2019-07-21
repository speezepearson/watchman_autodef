A wrapper around [Watchman](https://facebook.github.io/watchman/) to help make hooks persistent.

Tldr: define all your Watchman triggers in a special file (`.watchman-autodef.json`), and run `python -m watchman_autodef` in order to load them all.


Config format
-------------

The contents of `.watchman-autodef.json` should be a JSON object with the following keys:

- `triggers`: an array of "trigger objects" as specified in [Watchman's extended trigger syntax](https://facebook.github.io/watchman/docs/cmd/trigger.html#extended-syntax).
- (...maybe more someday?)

For example:
```json
{
    "triggers": [
        {
            "name": "pytest",
            "expression": [
                "allof",
                ["pcre", ".*\\.py$", "wholename"],
                ["not", ["pcre", "(^|.*/)\\..*", "wholename"]],
                ["not", ["pcre", "(^|.*/)__pycache__/.*", "wholename"]]
            ],
            "append_files": false,
            "command": [
                "bash",
                "-c",
                "pytest --color=yes >.pytest.log 2>&1"
            ]
        }
    ]
}
```
Then you could `tail -f .pytest.log` in one window, edit Python files in another, and watch the tests run every time you save.
