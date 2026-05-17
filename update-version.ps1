$path = "$PSScriptRoot\source.extension.vsixmanifest"
[xml]$m = Get-Content $path

$currentVersion = $m.PackageManifest.Metadata.Identity.Version
$versionObj = [version]$currentVersion

$newVersion = "{0}.{1}.{2}" -f $versionObj.Major, $versionObj.Minor, ($versionObj.Build + 1)

$m.PackageManifest.Metadata.Identity.Version = $newVersion
$m.Save($path)

Write-Output "Successfully bumped manifest file version directly to: $newVersion"
