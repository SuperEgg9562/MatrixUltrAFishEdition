param(
    [string]$RepoRoot = (Get-Location).Path
)

$ErrorActionPreference = 'Stop'

$Palette = @{
    Background = '#FF000000'
    Foreground = '#FF00FF41'
    Accent     = '#FF39FF14'
    Selection  = '#FF003300'
    Border     = '#FF004400'
    Error      = '#FFFF0033'
    Warning    = '#FFCCFF00'
    Info       = '#FF00FF99'
}

function Write-Info([string]$Message) {
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Backup-File([string]$Path, [string]$BackupDir) {
    if (Test-Path $Path) {
        Copy-Item $Path (Join-Path $BackupDir (Split-Path $Path -Leaf)) -Force
    }
}

function Get-MatrixColor([string]$Context) {
    $c = ''
    if ($null -ne $Context) { $c = $Context.ToLower() }

    if ($c -match 'error')   { return $Palette.Error }
    if ($c -match 'warning') { return $Palette.Warning }
    if ($c -match 'select|selection|highlight|match') { return $Palette.Selection }
    if ($c -match 'border|separator|grid|rule') { return $Palette.Border }
    if ($c -match 'accent|active|hover|pressed|hot|focus|keyword') { return $Palette.Accent }
    if ($c -match 'class|function|number|string|link|identifier') { return $Palette.Info }

    return $Palette.Foreground
}

function Convert-AllColorsToMatrixTheme([string]$XmlPath) {
    Write-Info "Converting all colors in $XmlPath"

    $text = Get-Content $XmlPath -Raw
    $lines = $text -split "`r?`n"

    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})') {
            $replacement = Get-MatrixColor $lines[$i]
            $lines[$i] = [regex]::Replace(
                $lines[$i],
                '#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})',
                $replacement
            )
        }
    }

    Set-Content -Path $XmlPath -Value ($lines -join [Environment]::NewLine) -Encoding UTF8
}

function Update-VsixManifest([string]$ManifestPath, [string]$ThemeFileName) {
    [xml]$xml = Get-Content $ManifestPath
    $nsUri = $xml.DocumentElement.NamespaceURI
    $ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
    if ($nsUri) { $ns.AddNamespace('x', $nsUri) }

    $assets = $xml.SelectSingleNode('//x:Assets', $ns)
    if (-not $assets) {
        $assets = $xml.CreateElement('Assets', $nsUri)
        $xml.DocumentElement.AppendChild($assets) | Out-Null
    }

    $asset = $xml.SelectSingleNode("//x:Asset[contains(@Path,'.vsTheme')]", $ns)
    if (-not $asset) {
        $asset = $xml.CreateElement('Asset', $nsUri)
        $asset.SetAttribute('Type', 'Microsoft.VisualStudio.ColorTheme')
        $asset.SetAttribute('Path', $ThemeFileName)
        $assets.AppendChild($asset) | Out-Null
    } else {
        $asset.SetAttribute('Type', 'Microsoft.VisualStudio.ColorTheme')
        $asset.SetAttribute('Path', $ThemeFileName)
    }

    $xml.Save($ManifestPath)
}

function Update-Csproj([string]$ProjectPath, [string]$ThemeFileName) {
    [xml]$xml = Get-Content $ProjectPath
    $nsUri = $xml.DocumentElement.NamespaceURI

    $itemGroup = $xml.Project.ItemGroup | Select-Object -First 1
    if (-not $itemGroup) {
        $itemGroup = $xml.CreateElement('ItemGroup', $nsUri)
        $xml.Project.AppendChild($itemGroup) | Out-Null
    }

    $existing = $null
    foreach ($node in $xml.SelectNodes('//*[local-name()="None" or local-name()="Content"]')) {
        if ($node.GetAttribute('Include') -eq $ThemeFileName) {
            $existing = $node
            break
        }
    }

    if (-not $existing) {
        $existing = $xml.CreateElement('Content', $nsUri)
        $existing.SetAttribute('Include', $ThemeFileName)
        $itemGroup.AppendChild($existing) | Out-Null
    }

    $include = $existing.SelectSingleNode('*[local-name()="IncludeInVSIX"]')
    if (-not $include) {
        $include = $xml.CreateElement('IncludeInVSIX', $nsUri)
        $existing.AppendChild($include) | Out-Null
    }
    $include.InnerText = 'true'

    $xml.Save($ProjectPath)
}

Set-Location $RepoRoot

$theme = Get-ChildItem -Recurse -Filter *.vsTheme | Select-Object -First 1
$project = Get-ChildItem -Recurse -Filter *.csproj | Select-Object -First 1
$manifest = Get-ChildItem -Recurse -Filter source.extension.vsixmanifest | Select-Object -First 1

if (-not $theme)    { throw 'No .vsTheme file found.' }
if (-not $project)  { throw 'No .csproj file found.' }
if (-not $manifest) { throw 'No source.extension.vsixmanifest file found.' }

$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupDir = Join-Path $RepoRoot "backup\$timestamp"
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

Backup-File $theme.FullName $backupDir
Backup-File $project.FullName $backupDir
Backup-File $manifest.FullName $backupDir

Convert-AllColorsToMatrixTheme $theme.FullName
Update-VsixManifest $manifest.FullName $theme.Name
Update-Csproj $project.FullName $theme.Name

Write-Host ''
Write-Host '========================================' -ForegroundColor Cyan
Write-Host ' FULL MATRIX THEME CONVERSION COMPLETE' -ForegroundColor Cyan
Write-Host " Backup folder: $backupDir" -ForegroundColor Cyan
Write-Host '========================================' -ForegroundColor Cyan
