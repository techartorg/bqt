Blender's integrated Python interpreter lives in the Blender install folder:  
`../Blender Foundation/<version>/Python/bin`

Any time you see a command that says `python`, you should instead use Blender's python interpreter.

so instead of 
```bash
python -m pip install bqt
```
use
```bash
"C:\Program Files\Blender Foundation\Blender 3.2\3.2\python\bin\python.exe" -m pip install bqt
```
which is the same as
```bash
cd "C:\Program Files\Blender Foundation\Blender 3.2\3.2\python\bin"
python -m pip install bqt
```

(⚠️ note that Blender modifies it's paths on startup, so pip won't be aware of all installed modules)