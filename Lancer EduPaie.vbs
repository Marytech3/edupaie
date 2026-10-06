Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

projectDir = fso.GetParentFolderName(WScript.ScriptFullName)
pythonw = projectDir & "\.venv\Scripts\pythonw.exe"
mainScript = projectDir & "\main.py"

If Not fso.FileExists(pythonw) Then
    MsgBox "Le lanceur Python est introuvable :" & vbCrLf & pythonw, vbCritical, "EduPaie"
    WScript.Quit 1
End If

If Not fso.FileExists(mainScript) Then
    MsgBox "Le fichier principal d'EduPaie est introuvable :" & vbCrLf & mainScript, vbCritical, "EduPaie"
    WScript.Quit 1
End If

shell.CurrentDirectory = projectDir
command = Chr(34) & pythonw & Chr(34) & " " & Chr(34) & mainScript & Chr(34)
shell.Run command, 0, False