param([string]$Presentation = (Join-Path $PSScriptRoot '..\presentation\Foundry - From prototype to operated service.pptx'))
$ErrorActionPreference = 'Stop'
$file = (Resolve-Path -LiteralPath $Presentation).Path
$directory = Split-Path $file
$renders = Join-Path $directory 'renders'
New-Item -ItemType Directory -Force -Path $renders | Out-Null
$powerpoint = New-Object -ComObject PowerPoint.Application
$deck = $null
try {
    $deck = $powerpoint.Presentations.Open($file, $true, $false, $false)
    for ($i = 1; $i -le $deck.Slides.Count; $i++) {
        $deck.Slides.Item($i).Export((Join-Path $renders ('slide-{0:00}.png' -f $i)), 'PNG', 1600, 900)
    }
    $deck.SaveAs([IO.Path]::ChangeExtension($file, '.pdf'), 32)
} finally {
    if ($null -ne $deck) { $deck.Close() }
    # Do not quit PowerPoint: an existing user session may share the COM server.
    [Runtime.InteropServices.Marshal]::ReleaseComObject($powerpoint) | Out-Null
}
Write-Host "Rendered slides and audience PDF to $directory"
