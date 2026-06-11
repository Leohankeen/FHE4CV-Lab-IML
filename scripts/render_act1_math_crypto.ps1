param(
    [string]$Quality = "-ql"
)

$ErrorActionPreference = "Stop"
$aggregateDir = "media/videos/01_math_crypto"
New-Item -ItemType Directory -Force -Path $aggregateDir | Out-Null

Write-Host "Validating Act 1 storyboard structure"
python scripts/validate_act1_math_crypto.py
if ($LASTEXITCODE -ne 0) {
    throw "Act 1 validation failed."
}

Write-Host "Checking Python and Manim prerequisites"
$pythonVersion = python -c "import sys; print(sys.version.split()[0])"
if ($LASTEXITCODE -ne 0) {
    throw "Python is not available from this terminal."
}
Write-Host "Using Python $pythonVersion"

python -c "import manim; print('Manim import OK')"
if ($LASTEXITCODE -ne 0) {
    throw "Manim is not importable in the active Python environment."
}

$scenes = @(
    @{ File = "scenes/01_math_crypto/scene_01_he_foundations.py"; Class = "HomomorphicEncryptionFoundations" },
    @{ File = "scenes/01_math_crypto/scene_02_ckks_encoding.py"; Class = "CKKSEncodingAndParameters" },
    @{ File = "scenes/01_math_crypto/scene_03_ciphertext_operations.py"; Class = "CiphertextOperations" },
    @{ File = "scenes/01_math_crypto/scene_04_keys_and_seal_pipeline.py"; Class = "KeysAndSEALPipeline" }
)

foreach ($scene in $scenes) {
    Write-Host "Rendering full storyboard: $($scene.Class)"
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
    }
}

Write-Host "Act 1 render complete. Collected videos are under $aggregateDir/."
