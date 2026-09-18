#define MyAppName "Extreme Message Animator"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Extreme Message Animator"
#define MyAppExeName "ExtremeMessageAnimator.exe"

[Setup]
AppId={{A4E2B9F8-8D9A-4A3C-9F0C-EXTREMEANIMATOR}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\Extreme Message Animator
DefaultGroupName=Extreme Message Animator

OutputDir=installer
OutputBaseFilename=ExtremeMessageAnimator-Setup

Compression=lzma
SolidCompression=yes

WizardStyle=modern

ArchitecturesInstallIn64BitMode=x64

DisableProgramGroupPage=yes

UninstallDisplayIcon={app}\{#MyAppExeName}

[Files]
Source: "dist\ExtremeMessageAnimator.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autodesktop}\Extreme Message Animator"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Extreme Message Animator"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"
Description: "Launch Extreme Message Animator"
Flags: nowait postinstall skipifsilent
