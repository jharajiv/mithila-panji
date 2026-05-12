# =============================================================================
# Mithila-Panji — one-time file population script (PowerShell, Windows)
# =============================================================================
# Copies the seed data files, the extraction scripts, and the parsed
# persons.json into their right places under the repo. Run this ONCE,
# after cloning / downloading the repo.
#
# How to run:
#   1. Open File Explorer, navigate to the mithila-panji folder.
#   2. Right-click on this file (_setup-copy-files.ps1) → "Run with PowerShell".
#   3. If Windows blocks it, hold Shift, right-click → "Run as Administrator",
#      or run from PowerShell:
#         powershell -ExecutionPolicy Bypass -File .\_setup-copy-files.ps1
#
# This script assumes the original Genome folder layout, with this repo
# sitting at: C:\Users\HP\OneDrive - Vyoma\Documents\Genome\mithila-panji\
# If you've moved things, edit $sourceRoot below before running.
# =============================================================================

$ErrorActionPreference = "Stop"

# ---- Locate source files ---------------------------------------------------
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceRoot = Split-Path -Parent $scriptRoot   # parent = Genome\
Write-Host "Mithila-Panji setup: copying files from $sourceRoot" -ForegroundColor Cyan

$copies = @(
  @{ Src = "$sourceRoot\exports\panji_seed_gotras_mools.cypher"
     Dst = "$scriptRoot\data\seed\panji_seed_gotras_mools.cypher" },
  @{ Src = "$sourceRoot\exports\panji_seed_gotras_mools.jsonl"
     Dst = "$scriptRoot\data\seed\panji_seed_gotras_mools.jsonl" },
  @{ Src = "$sourceRoot\exports\panji_founding_history.cypher"
     Dst = "$scriptRoot\data\seed\panji_founding_history.cypher" },

  @{ Src = "$sourceRoot\genome_db\extract.py"
     Dst = "$scriptRoot\scripts\extract.py" },
  @{ Src = "$sourceRoot\genome_db\load_neo4j.py"
     Dst = "$scriptRoot\scripts\load_neo4j.py" },
  @{ Src = "$sourceRoot\genome_db\build_lineage_exports.py"
     Dst = "$scriptRoot\scripts\build_lineage_exports.py" },

  @{ Src = "$sourceRoot\genome_db\persons.json"
     Dst = "$scriptRoot\data\extracted\persons.json" }
)

# ---- Make sure target directories exist ------------------------------------
$null = New-Item -ItemType Directory -Force -Path "$scriptRoot\data\seed"
$null = New-Item -ItemType Directory -Force -Path "$scriptRoot\data\extracted"
$null = New-Item -ItemType Directory -Force -Path "$scriptRoot\scripts"

# ---- Do the copies ---------------------------------------------------------
$copied = 0
$skipped = 0

foreach ($pair in $copies) {
  if (Test-Path $pair.Src) {
    Copy-Item -Path $pair.Src -Destination $pair.Dst -Force
    $rel = $pair.Dst.Substring($scriptRoot.Length + 1)
    Write-Host "  ✓ $rel" -ForegroundColor Green
    $copied++
  } else {
    $rel = $pair.Src.Substring($sourceRoot.Length + 1)
    Write-Host "  ✗ NOT FOUND: $rel" -ForegroundColor Yellow
    $skipped++
  }
}

Write-Host ""
Write-Host "Done. Copied $copied file(s); $skipped not found." -ForegroundColor Cyan
if ($skipped -gt 0) {
  Write-Host "The 'not found' files are usually because you haven't run extract.py yet," -ForegroundColor Yellow
  Write-Host "or because the original Genome folder layout has changed."                -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next step: open docs\MVP_SETUP.md and follow Step 1 onwards." -ForegroundColor Cyan
