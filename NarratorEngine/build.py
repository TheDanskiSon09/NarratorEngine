from subprocess import run


def generate_version_file():
    version = '1.0'
    version_tuple = tuple(map(int, version.split("."))) + (0,)

    content = f"""
# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={version_tuple},
    prodvers={version_tuple},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo([
      StringTable(
        '040904B0',
        [
        StringStruct('CompanyName', 'SVT-Games'),
        StringStruct('FileDescription', 'Mygame'),
        StringStruct('FileVersion', '1.0'),
        StringStruct('InternalName', 'mygame'),
        StringStruct('LegalCopyright', '2026'),
        StringStruct('OriginalFilename', 'mygame.exe'),
        StringStruct('ProductName', 'MyGameEngine'),
        StringStruct('ProductVersion', '1.0')
        ])
      ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""
    with open('version.txt', 'w', encoding='utf-8') as version_file:
        version_file.write(content)


def build():
    generate_version_file()

    command = [
        "pyinstaller",
        "main.py",
        "--onefile",
        "--windowed",
        f"--name=mygame.exe",
        f"--icon={GAME_METADATA['APP_ICON']}",
        "--version-file=version.txt"
    ]

    run(command)


if __name__ == "__main__":
    build()
