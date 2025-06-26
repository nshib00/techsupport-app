$venvPath = poetry env info -p

$activatePath = Join-Path $venvPath "Scripts\Activate.ps1"

& $activatePath