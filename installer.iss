#define MyAppName "Extreme Message Animator"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Extreme Message Animator"
#define MyAppExeName "ExtremeMessageAnimator.exe"

[Setup]
AppId={{F6D4D9D2-5E8B-4C67-A5B9-3C6A7D9E2148}}

AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\Extreme Message Animator
DefaultGroupName=Extreme Message Animator

OutputDir=installer
OutputBaseFilename=ExtremeMessageAnimator-Setup

Compression=lzma2
SolidCompression=yes

WizardStyle=modern

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

DisableProgramGroupPage=yes

UninstallDisplayIcon={app}\{#MyAppExeName}

PrivilegesRequired=admin

[Files]
Source: "dist\ExtremeMessageAnimator.exe"; \
    DestDir: "{app}"; \
    Flags: ignoreversion

[Icons]
Name: "{autodesktop}\Extreme Message Animator"; \
    Filename: "{app}\{#MyAppExeName}"

Name: "{group}\Extreme Message Animator"; \
    Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; \
    Description: "Launch Extreme Message Animator"; \
    Flags: nowait postinstall skipifsilent
