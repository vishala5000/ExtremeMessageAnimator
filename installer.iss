#define MyAppName "Extreme Message Animator"
#define MyAppVersion "3.0.0"
#define MyAppPublisher "Extreme Message Animator"
#define MyAppExeName "ExtremeMessageAnimator.exe"

[Setup]

AppId={{E4A7A9D4-5C8B-4A42-BB25-83E7D1F3A910}}

AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={pf}\Extreme Message Animator
DefaultGroupName=Extreme Message Animator

OutputDir=installer
OutputBaseFilename=ExtremeMessageAnimator-Windows7-10-Setup

Compression=lzma
SolidCompression=yes

WizardStyle=classic

DisableProgramGroupPage=yes

PrivilegesRequired=admin

UninstallDisplayIcon={app}\{#MyAppExeName}

[Files]

Source: "dist\ExtremeMessageAnimator.exe"; \
    DestDir: "{app}"; \
    Flags: ignoreversion

Source: "dist\ucrtbase.dll"; \
    DestDir: "{app}"; \
    Flags: ignoreversion skipifsourcedoesntexist

Source: "dist\vcruntime140.dll"; \
    DestDir: "{app}"; \
    Flags: ignoreversion skipifsourcedoesntexist

Source: "dist\vcruntime140_1.dll"; \
    DestDir: "{app}"; \
    Flags: ignoreversion skipifsourcedoesntexist

[Icons]

Name: "{desktop}\Extreme Message Animator"; \
    Filename: "{app}\{#MyAppExeName}"

Name: "{group}\Extreme Message Animator"; \
    Filename: "{app}\{#MyAppExeName}"

[Run]

Filename: "{app}\{#MyAppExeName}"; \
    Description: "Launch Extreme Message Animator"; \
    Flags: nowait postinstall skipifsilent
