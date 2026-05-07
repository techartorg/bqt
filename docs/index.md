# Home

BQt adds Qt Support to Blender, 
letting you create custom UIs for your addons with PySide6.

![custom ui sample](https://user-images.githubusercontent.com/3758308/192096952-e9ed73be-26e4-4ad8-a85f-be4175cebbda.gif)

BQt is created with games and VFX in mind, 
it's there to help you integrate already existing tools and widgets into your Blender workflow.

BQt takes care of the heavy lifting, so you can focus on your qt tools.

* Manage focus of widgets, letting you parent widgets to Blender.
* Manage QApplication setup for you (the qt eventloop).
* Prevent widgets from being garbage collected.
* Automatically applies a style to your widgets to match Blender's UI.
