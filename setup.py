from cx_Freeze import setup, Executable

base = None    

executables = [Executable("PDFInserter.py", base = "Win32GUI")]

packages = ["idna", "PyPDF2", "reportlab"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

bdist_msi_options={'add_to_path':True, 'target_name':"PDF Inserter"}

setup(
    name = "PDF Inserter",
    options = options,
    version = "1",
    description = '',
    executables = executables
)

#python3 setup.py bdist_msi for MSI Installer
#python3 setup.py build for executable