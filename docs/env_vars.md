# Environment Variables

You can configure how BQt is running through feature toggles exposed as Environment variables.

These toggles are used by setting them to either "0" or "1".


## `BQT_DISABLE_STARTUP`
_added in `1.0.0`_

Disable BQt. Setting this to `"1"` will ensure that BQt is not managing Blender windows.
No Qt application should be expected to work.


## `BQT_DISABLE_WRAP`
_added in `1.3.1`_

Set this to `"1"` to disable wrapping any Blender window in a QWindow.

If this is set to `"1"` BQt will use and internal system (`bqt.manager`)
to handle windows always being on top. 


## `BQT_DISABLE_CLOSE_DIALOGUE`
_added in `1.0.0`_

Do not use BQt close dialog. 

Qt Windows are always above Blender, this means that if this is enabled
the close dialog might appear behind Blender.


## `BQT_MANAGE_FOREGROUND`
_added in `1.2.2`_

If [`BQT_DISABLE_WRAP`](#bqt_disable_wrap) is enabled BQt still tries to display any
widget or window above the Blender window. 
Set this to `"0"` to stop BQt from trying to display Windows above the Blender window.


## `BQT_AUTO_ADD`
_added in `1.2.0`_

By default, BQt handles parenting of any orphaned window. 
This means that you don't have to explicitly set the parent of a tool.
BQt will pick it up as an orphan and set itself as the parent.

If disabled, set to `"0"`, any top level window won't automatically be added to BQt,
any orphaned will be garbage collected. You need to set the parent
explicitly to keep the tool around.


## `BQT_UNIQUE_OBJECTNAME`
_added in `1.3.0`_

By default, BQt will ensure only one of each object name is available.
This will ensure that opening your tool a second time will not open a new window,
but instead it will surface the old instance.

Set this to `"0"` to disable this behavior.


## `BQT_DOCKABLE_WRAP`
_added in `1.3.1`_

Set to `"0"` to disable wrapping of widgets in a dockable widget.

By default, BQt grabs all orphaned widgets, wraps them in a window,
and parents them to the main window.
This means that you don't have to manually fetch the main window and
parent your tool to it. However, this also means that if you unparent
a widget by setting `parent(None)` on it
(like you would if removing dynamically spawned widgets) 
the widget will be grabbed by BQt and parented to the main window again.


## `BQT_LOG_LEVEL`
_added in `1.4.1`_

By default, BQt does not surface any logs.

Set to `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`
to surface logs of the set level and higher.
