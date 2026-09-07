<#
.SYNOPSIS
  Stage 1 over a whole PDF library. Zero model tokens.

.DESCRIPTION
  Runs pdf2md.py on every PDF under -Root, then prints a triage table so you can
  see which papers are worth spending stage-2 tokens on before spending any.

  Idempotent: papers already extracted are skipped by sha256 unless -Force.

.EXAMPLE
  .\batch_scan.ps1
  .\batch_scan.ps1 -Root .\01_classified_pdfs -Python "D:\2\software\python.exe"
#>
param(
  [string]$Root   = ".\01_classified_pdfs",
  [string]$Out    = ".\output\extracted",
  [string]$Python = "D:\2\software\python.exe",
  [string]$Csv    = ".\output\triage.csv",
  [switch]$Force
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $Python)) { throw "Interpreter not found: $Python" }
if (-not (Test-Path $Root))   { throw "PDF folder not found: $Root" }

# Fail fast on the dependency rather than 221 times in a row.
& $Python -c "import pdf_inspector" 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
  Write-Host "pdf-inspector is not installed for $Python" -ForegroundColor Red
  Write-Host "  fix:  & `"$Python`" -m pip install pdf-inspector"
  exit 1
}

$pdfs = Get-ChildItem -Path $Root -Recurse -Filter *.pdf | Sort-Object FullName
Write-Host "$($pdfs.Count) PDFs under $Root`n" -ForegroundColor Cyan

$i = 0
$failed = @()
foreach ($p in $pdfs) {
  $i++
  Write-Progress -Activity "Stage 1" -Status "$i/$($pdfs.Count)  $($p.Name)" `
                 -PercentComplete ($i * 100 / $pdfs.Count)
  $argv = @("pdf2md.py", $p.FullName, "--out", $Out)
  if ($Force) { $argv += "--force" }
  $output = & $Python @argv 2>&1
  if ($LASTEXITCODE -ne 0) {
    $failed += [pscustomobject]@{ File = $p.Name; Error = ($output | Select-Object -Last 1) }
  }
}
Write-Progress -Activity "Stage 1" -Completed

# ---- triage ----------------------------------------------------------------
# 2.47 bytes per token, measured on extracted paper prose. Not the generic ~4.
$BYTES_PER_TOKEN = 2.47

$rows = Get-ChildItem -Path $Out -Directory | ForEach-Object {
  $metaPath = Join-Path $_.FullName "meta.json"
  if (-not (Test-Path $metaPath)) { return }
  $m = Get-Content $metaPath -Raw -Encoding UTF8 | ConvertFrom-Json
  $bodyPath = Join-Path $_.FullName "body.md"
  $bodyBytes = if (Test-Path $bodyPath) { (Get-Item $bodyPath).Length } else { 0 }

  $w = @()
  foreach ($x in $m.warnings) {
    if     ($x -like "references were not split*") { $w += "REFS" }
    elseif ($x -like "no figures*")                { $w += "NOFIG" }
    elseif ($x -like "*branch*")                   { $w += "BRANCH?" }
    elseif ($x -like "*shredded*")                 { $w += "SHRED" }
  }
  if ($m.pdf_kind -ne "text_based") { $w += "SCANNED" }

  [pscustomobject]@{
    Slug     = $_.Name
    Topic    = (Split-Path (Split-Path $m.pdf_path -Parent) -Leaf)
    Pages    = $m.n_pages
    Branch   = if ($m.has_primary_data) { "primary" } else { "synthesis" }
    Figs     = $m.figures
    BodyKB   = [math]::Round($bodyBytes / 1KB)
    Est2kTok = [math]::Round($bodyBytes / $BYTES_PER_TOKEN / 1000, 1)
    Flags    = ($w -join ",")
  }
}

$rows = $rows | Sort-Object Est2kTok
New-Item -ItemType Directory -Force -Path (Split-Path $Csv) | Out-Null
$rows | Export-Csv -Path $Csv -NoTypeInformation -Encoding UTF8

# ---- summary ---------------------------------------------------------------
# NOFIG / BRANCH? are informational: a review really can have no figures.
# Only SCANNED blocks, and only REFS costs extra money.
$ready   = $rows | Where-Object { $_.Flags -notlike "*SCANNED*" -and $_.Flags -notlike "*REFS*" }
$scanned = $rows | Where-Object { $_.Flags -like "*SCANNED*" }
$refs    = $rows | Where-Object { $_.Flags -like "*REFS*" }
$shred   = $rows | Where-Object { $_.Flags -like "*SHRED*" }
$usable  = $rows | Where-Object { $_.Flags -notlike "*SCANNED*" }

""
Write-Host "extracted        $($rows.Count)" -ForegroundColor Cyan
if ($rows.Count -lt $pdfs.Count) {
  # Caught a real bug: 10 of 221 papers had been silently overwritten because their
  # slugs collided. Every per-file call had exited 0, so nothing else would have noticed.
  Write-Host ("  !! $($pdfs.Count - $rows.Count) PDFs produced no folder of their own. " +
              "Delete $Out and re-run; if the gap persists, it is not slug collision.") -ForegroundColor Red
}
Write-Host "  ready to run   $($ready.Count)   no blocker, no wasted references"
Write-Host "  scanned        $($scanned.Count)   cannot process, no OCR path"
Write-Host "  refs not split $($refs.Count)   each costs ~35% more in stage 2"
Write-Host "  shredded heads $($shred.Count)   branch flag unreliable, check by hand"
Write-Host "  primary/synth  $(($rows | Where-Object Branch -eq 'primary').Count) / $(($rows | Where-Object Branch -eq 'synthesis').Count)"
""
$totalM = [math]::Round((($usable | Measure-Object Est2kTok -Sum).Sum) / 1000, 2)
$wasteK = [math]::Round((($refs   | Measure-Object Est2kTok -Sum).Sum) * 0.35, 0)
Write-Host "stage 2 for ALL usable papers:  ~$totalM M tokens" -ForegroundColor Yellow
Write-Host "  of which wasted on unsplit references: ~$wasteK k" -ForegroundColor Yellow
""
Write-Host "cheapest 15 ready papers to try first:" -ForegroundColor Green
$ready | Select-Object -First 15 Slug, Topic, Pages, Branch, Est2kTok | Format-Table -AutoSize

if ($failed.Count) {
  Write-Host "$($failed.Count) failed:" -ForegroundColor Red
  $failed | Format-Table -AutoSize
}
Write-Host "full table: $Csv"
