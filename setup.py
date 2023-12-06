from cx_Freeze import setup, Executable

executables = [
  Executable(
    'main.py',
    base='Win32GUI',
    icon='icon.ico',
    shortcut_name='AutomacaoEptc'
  )
]

packages = [
  'selenium',
  'json',
  'configparser',
  'oracledb',
  'bs4'
]


includes = [
  'os',
  'shutil',
  'datetime'
]

files = [
  'browser.py',
  'dboracle.py',
  'directories.py',
  'excel.py',
  'logs.py',
  'dboracle.ini'
]
files += [
  ('temp/' + f) for f in ['dados.json', 'reclamations.json']
]

setup(
    name='AutomacaoEptc',
    version='1.0',
    description='Aplicativo para automatizar reclamações',
    executables=executables,
    options={
      'build_exe': {
        'packages': packages,
        'includes': includes,
        'include_files': files
      }
    }
)
