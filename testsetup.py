from cx_Freeze import setup, Executable

base = None

executables = [Executable("pygametest.py", base=base)]
packages = ["idna"]
options = {
	'build_exe': {
		'packages':packages,
			"include_files":["circle.png", "circle2.png", "diamond.png", "diamond2.png", "square.png", "square2.png", "triangle.png", "triangle2.png", "augustus.ttf"]
	},    
}
setup(
    name = "The Trial",
    options = options,
    version = "1.0",
    description = '7th Guest',
    executables = executables
)