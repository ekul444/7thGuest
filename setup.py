import cx_Freeze

executables = [cx_Freeze.Executable("pygametest.py")]

cx_Freeze.setup(
    name="The Trial",
    options={"build_exe": {"packages":["pygame", "idna"],
                           "include_files":["circle.png", "circle2.png", "diamond.png", "diamond2.png", "square.py", "square2.py", "triangle.py", "triangle2.py", "augustus.ttf"]}},
    executables = executables

    )