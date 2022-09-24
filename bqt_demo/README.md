bqt_demo is an optional module, with several qt samples you can use as a guide.
To install, add the bqt_demo folder to your python path.

## hello_world
To verify installation was successful, launch Blender and in the python console enter
the following:
```python
from bqt_demo import hello_world
hello_world.demo()
```

## Blender controlling qt - anim_bar
Demo showing how qt can listen to blender
![sample_blender_2way](https://user-images.githubusercontent.com/3758308/192096952-e9ed73be-26e4-4ad8-a85f-be4175cebbda.gif)

```python
from bqt_demo import anim_bar
anim_bar.main()
```

## timer
a Qt-timer demo
```python
from bqt_demo import timer
timer.main()
```
