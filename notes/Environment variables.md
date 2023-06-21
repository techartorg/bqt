
## Purpose
The env variables are mostly used as feature toggles, letting you turn off certain features of bqt if they are undesired or causing problems.

## Overview

|   |   |
|---|---|
|BQT_DISABLE_STARTUP|if set to `1`, completely disable bqt|
|BQT_DISABLE_WRAP|if set to `1`, disable wrapping blender in a QWindow|
|BQT_DISABLE_CLOSE_DIALOGUE|if set to `1`, use the standard blender close dialogue|
|BQT_MANAGE_FOREGROUND|defaults to `1`, if `0`, widgets registered with `bqt.add(my_widget)` won't stay in the foreground when using Blender.|
|BQT_AUTO_ADD|defaults to `1`, if `0` top level widgets won't automatically be added to bqt.|
|BQT_UNIQUE_OBJECTNAME|defaults to `1`, 1 or 0, automatically delete widgets with same objectName, preventing you from opening multiple versions of the same widget window. Great if you want to ensure that clicking "my window" activates "mywindow" if already open, instead of making a new one|

### Legacy
Outdated env vars go here, currently no outdated env vars

# FAQ
### How to edit env variables?
It's quite a common thing, a google search for `set environment variable` should help you.
- a [tutorial](https://www.howtogeek.com/787217/how-to-edit-environment-variables-on-windows-10-or-11/) for windows users with images

### Restart after edit env vars.
Don't forget to click the OK button on Windows. (I've done it 😅)

After editing env variables, you have to restart Blender, or the launcher that launches Blender. e.g. `steam` or `blender launcher`. Closing these launchers often just hides them in the background, and doesn't really restarts them. Which means edits to the env vars wont show. If you don't know how to restart it, just restart your computer.

### dynamically set env vars
You can also do this with a startup script.  
If you modify env vars in code, ensure they're strings!
