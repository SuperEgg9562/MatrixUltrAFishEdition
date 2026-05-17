@echo off
cd /d "%~dp0"
echo ===================================================
echo   LAUNCHING AUTOMATED RE-VERSION AND GIT DEPLOY
echo ===================================================

echo Incrementing VSIX manifest version number...
powershell -NonInteractive -Command "& { [xml]$m = Get-Content source.extension.vsixmanifest; $ns = New-Object System.Xml.XmlNamespaceManager $m.NameTable; $ns.AddNamespace('main', 'http://schemas.microsoft.com/developer/vsx-schema/2011'); $node = $m.SelectSingleNode('//main:Identity', $ns); $v = [version]$node.Version; $n = '{0}.{1}.{2}' -f $v.Major, $v.Minor, ($v.Build + 1); $node.Version = $n; $m.Save('source.extension.vsixmanifest'); Write-Host 'Successfully bumped manifest to:' $n -ForegroundColor Green }"

for /f "usebackq tokens=*" %%i in (`"C:\Program Files\Microsoft Visual Studio\Installer\vswhere.exe" -latest -requires Microsoft.Component.MSBuild -property installationPath`) do (
    set "VS_PATH=%%i"
)
set "MSBUILD_PATH=%VS_PATH%\MSBuild\Current\Bin\MSBuild.exe"

echo Compiling fresh Release VSIX container...
"%MSBUILD_PATH%" MatrixUltrA12.csproj /p:Configuration=Release /p:Platform="Any CPU"

echo Staging updated version and VSIX bundle...
git add source.extension.vsixmanifest MatrixUltrAFishEdition.vstheme MatrixUltrA12.csproj
git add -f bin/Release/MatrixUltrA12.vsix

echo Committing deployment package to repository...
git commit -m "release: automated post-build version bump and binary sync [skip ci]"

echo Pushing updates to GitHub...
git push origin main

echo ===================================================
echo   SUCCESS: Pipeline Complete! Marketplace upload triggered.
echo ===================================================