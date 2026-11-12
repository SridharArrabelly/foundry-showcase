$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$pptx = Join-Path $root 'Volt & Co - Governed and improving agents.pptx'
$pdf = Join-Path $root 'Volt & Co - Audience.pdf'
$render = Join-Path $root '..\.runtime\presentation-renders'
New-Item -ItemType Directory -Force -Path $render | Out-Null
$app = New-Object -ComObject PowerPoint.Application
$deck = $null
try {
    $deck = $app.Presentations.Open($pptx, -1, 0, 0)
    foreach ($slide in $deck.Slides) {
        $name = 'slide-{0:D2}.png' -f $slide.SlideIndex
        $slide.Export((Join-Path $render $name), 'PNG', 1920, 1080)
    }
    $deck.SaveAs($pdf, 32)
    Write-Output ("Rendered {0} slides with native PowerPoint." -f $deck.Slides.Count)
    Write-Output $pdf
}
finally {
    if ($null -ne $deck) {
        $deck.Close()
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($deck) | Out-Null
    }
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
