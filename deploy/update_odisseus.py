from  pyinfra.operations import files

files.sync(src="rorobt", dest="robot", delete=True, exclude("*.pyc","__pycache__",".vscode",".idea"))
