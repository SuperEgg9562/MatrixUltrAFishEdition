@echo off
cd /d "%~dp0"
echo ===================================================
echo   LAUNCHING AUTOMATED GIT DEPLOY ASSET SYNC
echo ===================================================

echo Staging all repository adjustments...
git add .
git add -f bin/Release/MatrixUltrA12.vsix

echo Committing deployment package to repository...
git commit -m "release: post-build automated binary sync v1.0.98" || echo No local changes to commit.

echo Pulling latest changes from GitHub to synchronize histories...
git pull origin main --rebase

echo Pushing updates to GitHub...
git push origin main

echo ===================================================
echo   SUCCESS: Pipeline Complete! Marketplace upload triggered.
echo ===================================================