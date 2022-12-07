import sys
from cx_Freeze import setup, Executable


base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
        Executable("main.py", base=base)
]

buildOptions = dict(
        packages = ["tkinter", "pygame", "os", "random"],
        includes = [],
        include_files = ["Assets"],
        excludes = []
)




setup(
    name = "Space Invaders 2022",
    version = "1.0",
    description = "Remake do jogo Space Invaders",
    options = dict(build_exe = buildOptions),
    executables = executables
 )
