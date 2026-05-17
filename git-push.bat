@echo off
cd /d "%~dp0"
echo ===================================================
echo   LAUNCHING AUTOMATED RE-VERSION AND GIT DEPLOY
echo ===================================================

echo Staging updated version and VSIX bundle...
git add source.extension.vsixmanifest MatrixUltrAFishEdition.vstheme MatrixUltrA12.csproj
git add -f bin/Release/MatrixUltrA12.vsix

echo Committing deployment package to repository...
git commit -m "release: post-build automated version bump and binary sync [skip ci]"

echo Pushing updates to GitHub...
git push origin main

echo ===================================================
echo   SUCCESS: Pipeline Complete! Marketplace upload triggered.
echo ===================================================