#define MyAppName "Extreme Message Animator"
#define MyAppVersion "3.0.0"
#define MyAppPublisher "Extreme Message Animator"
#define MyAppExeName "ExtremeMessageAnimator.exe"

[Setup]
AppId={{A8C2F6B7-9A51-4E45-B8D4-2F3E7C9A61D2}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\Extreme Message Animator

DefaultGroupName=Extreme Message Animator

DisableProgramGroupPage=yes

OutputDir=Output
OutputBaseFilename=ExtremeMessageAnimator-Windows7-10-Setup

Compression=lzma
SolidCompression=yes

WizardStyle=modern

PrivilegesRequired=admin

ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

UninstallDisplayIcon={app}\{#MyAppExeName}

SetupIconFile=

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; \
    Description: "Create a desktop shortcut"; \
    GroupDescription: "Additional shortcuts:"; \
    Flags: unchecked

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

Name: "{group}\Extreme Message Animator"; \
    Filename: "{app}\{#MyAppExeName}"

Name: "{autodesktop}\Extreme Message Animator"; \
    Filename: "{app}\{#MyAppExeName}"; \
    Tasks: desktopicon

[Run]

Filename: "{app}\{#MyAppExeName}"; \
    Description: "Launch Extreme Message Animator"; \
    Flags: nowait postinstall skipifsilent
