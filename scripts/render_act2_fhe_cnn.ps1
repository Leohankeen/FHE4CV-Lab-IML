param(
    [string]$Quality = "-ql"
)

$ErrorActionPreference = "Stop"
$aggregateDir = "media/videos/02_fhe_cnn"
New-Item -ItemType Directory -Force -Path $aggregateDir | Out-Null

Write-Host "Checking Python and Manim prerequisites"
$pythonVersion = python -c "import sys; print(sys.version.split()[0])"
if ($LASTEXITCODE -ne 0) {
    throw "Python is not available from this terminal."
}
Write-Host "Using Python $pythonVersion"

python -c "import pydub; import manim; print('Manim import OK')"
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Manim import failed before rendering any scene."
    Write-Host "If the traceback mentions audioop or pyaudioop, your venv is likely Python 3.13."
    Write-Host "Fix option 1: python -m pip install audioop-lts"
    Write-Host "Fix option 2: recreate .venv with Python 3.11 or 3.12, then pip install -r requirements.txt"
    exit 1
}

$scenes = @(
    @{ File = "scenes/02_fhe_cnn/scene_01_relu_barrier.py"; Class = "ReLuBarrier" },
    @{ File = "scenes/02_fhe_cnn/scene_02_polynomial_approx.py"; Class = "PolynomialApproximation" },
    @{ File = "scenes/02_fhe_cnn/scene_03_naive_cnn_bottleneck.py"; Class = "NaiveCNNBottleneck" },
    @{ File = "scenes/02_fhe_cnn/scene_04_multiplexed_conv.py"; Class = "MultiplexedPacking" }
)

foreach ($scene in $scenes) {
    Write-Host "Rendering full storyboard: $($scene.Class) from $($scene.File)"
    python -m manim -c configs/manim.cfg $Quality $scene.File $scene.Class
    if ($LASTEXITCODE -ne 0) {
        throw "Render failed for $($scene.Class)."
    }

    $sceneStem = [System.IO.Path]::GetFileNameWithoutExtension($scene.File)
    $renderedFile = Get-ChildItem -Path "media/videos/$sceneStem" -Recurse -Filter "$($scene.Class).mp4" |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    if ($renderedFile) {
        Copy-Item -LiteralPath $renderedFile.FullName -Destination "$aggregateDir/$($scene.Class).mp4" -Force
        Write-Host "Copied to $aggregateDir/$($scene.Class).mp4"
    }
}

Write-Host "Act 2 render complete. Collected videos are under $aggregateDir/."
