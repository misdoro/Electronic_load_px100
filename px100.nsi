/*
Basic installer for battery tester
*/

!define NAME "Battery tester PX100"
!define REGPATH_UNINSTSUBKEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${NAME}"
Name "${NAME}"
OutFile "Install ${NAME}.exe"
Unicode True
RequestExecutionLevel User ; We don't need UAC elevation
InstallDir "" ; Don't set a default $InstDir so we can detect /D= and InstallDirRegKey
InstallDirRegKey HKCU "${REGPATH_UNINSTSUBKEY}" "UninstallString"

!include LogicLib.nsh
!include WinCore.nsh
!include Integration.nsh

Page Directory
Page InstFiles

Uninstpage UninstConfirm
Uninstpage InstFiles


Function .onInit
  SetShellVarContext Current

  ${If} $InstDir == "" ; No /D= nor InstallDirRegKey?
    GetKnownFolderPath $InstDir ${FOLDERID_UserProgramFiles} ; This folder only exists on Win7+
    StrCmp $InstDir "" 0 +2 
    StrCpy $InstDir "$LocalAppData\Programs" ; Fallback directory

    StrCpy $InstDir "$InstDir\$(^Name)"
  ${EndIf}
FunctionEnd

Function un.onInit
  SetShellVarContext Current
FunctionEnd

Section "Program files (Required)"
  SectionIn Ro

  SetOutPath $InstDir
  WriteUninstaller "$InstDir\Uninst.exe"
  WriteRegStr HKCU "${REGPATH_UNINSTSUBKEY}" "DisplayName" "${NAME}"
  WriteRegStr HKCU "${REGPATH_UNINSTSUBKEY}" "DisplayIcon" "$InstDir\MyApp.exe,0"
  WriteRegStr HKCU "${REGPATH_UNINSTSUBKEY}" "UninstallString" '"$InstDir\Uninst.exe"'
  WriteRegDWORD HKCU "${REGPATH_UNINSTSUBKEY}" "NoModify" 1
  WriteRegDWORD HKCU "${REGPATH_UNINSTSUBKEY}" "NoRepair" 1

  File /r dist\px100\*
SectionEnd

Section "Start Menu shortcut"
  CreateShortcut "$SMPrograms\${NAME}.lnk" "$InstDir\px100.exe"
SectionEnd

Section -Uninstall
  ${UnpinShortcut} "$SMPrograms\${NAME}.lnk"
  Delete "$SMPrograms\${NAME}.lnk"

  Delete "$InstDir\MyApp.exe"
  Delete "$InstDir\Uninst.exe"
  RMDir "$InstDir"
  DeleteRegKey HKCU "${REGPATH_UNINSTSUBKEY}"
SectionEnd
