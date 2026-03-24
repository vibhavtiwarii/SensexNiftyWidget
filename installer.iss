[Setup]
AppName=SensexNiftyWidget
AppVersion=1.0
AppVerName=SensexNiftyWidget 1.0
AppPublisher=thewitness
DefaultDirName={pf}\SensexNiftyWidget
DefaultGroupName=SensexNiftyWidget
OutputDir=C:\Users\Vibhav\Desktop
OutputBaseFilename=SensexNiftyWidgetSetup
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\main.exe

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\SensexNiftyWidget"; Filename: "{app}\main.exe"
Name: "{commondesktop}\SensexNiftyWidget"; Filename: "{app}\main.exe"

[Run]
Filename: "{app}\main.exe"; Description: "Launch SensexNiftyWidget"; Flags: nowait postinstall skipifsilent