@echo off
cd /d "%~dp0"
echo ===================================================
echo   LAUNCHING AUTOMATED RE-VERSION AND GIT DEPLOY
echo ===================================================

echo Incrementing VSIX manifest version number...
powershell -NonInteractive -Command "& { [xml]$m = Get-Content source.extension.vsixmanifest; $v = [version]$m.PackageManifest.Metadata.Identity.Version; $n = '{0}.{1}.{2}' -f $v.Major, $v.Minor, ($v.Build + 1); $m.PackageManifest.Metadata.Identity.Version = $n; $m.Save('source.extension.vsixmanifest'); Write-Host 'Successfully bumped manifest to:' $n -ForegroundColor Green }"

echo Staging updated version and VSIX bundle...
git add source.extension.vsixmanifest bin/Release/MatrixUltrA12.vsix MatrixUltrAFishEdition.vstheme MatrixUltrA12.csproj

echo Committing deployment package to repository...
git commit -m "release: post-build automated version bump and binary sync [skip ci]"

echo Pushing updates to GitHub...
git push origin main

echo ===================================================
echo   SUCCESS: Pipeline Complete! Marketplace upload triggered.
echo ===================================================