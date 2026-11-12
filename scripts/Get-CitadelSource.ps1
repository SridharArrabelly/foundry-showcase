$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$source = Get-Content (Join-Path $PSScriptRoot '..\infra\citadel-source.json') -Raw | ConvertFrom-Json
$runtime = Join-Path $repoRoot '.runtime'
$folder = Join-Path $runtime "ai-hub-gateway-solution-accelerator-$($source.commit)"
if (-not (Test-Path (Join-Path $folder $source.template))) {
    New-Item -ItemType Directory -Force -Path $runtime | Out-Null
    $archive = Join-Path $runtime "citadel-$($source.commit).zip"
    Invoke-WebRequest -Uri $source.archive -OutFile $archive
    Expand-Archive -LiteralPath $archive -DestinationPath $runtime
}
if (-not (Test-Path (Join-Path $folder $source.template))) {
    throw "Pinned Citadel template is missing from $folder."
}
$relative = ".runtime/ai-hub-gateway-solution-accelerator-$($source.commit)"
$patches = Get-ChildItem (Join-Path $PSScriptRoot '..\infra\patches') -Filter '*.patch' | Sort-Object Name
foreach ($patch in $patches) {
    & git -C $repoRoot apply --check --ignore-space-change --directory $relative $patch.FullName 2>$null
    if ($LASTEXITCODE -eq 0) {
        & git -C $repoRoot apply --ignore-space-change --directory $relative $patch.FullName
        if ($LASTEXITCODE -ne 0) { throw "Failed to apply reviewed patch $($patch.Name)." }
    } else {
        & git -C $repoRoot apply --reverse --check --ignore-space-change --directory $relative $patch.FullName 2>$null
        if ($LASTEXITCODE -ne 0) { throw "Citadel source differs from both versions of $($patch.Name)." }
    }
}
Write-Output $folder
