# ============================================================
# Chicago Data Portal - Taxi Trips Downloader (with resume)
# ============================================================
# Usage:
#   .\download_chicago_taxi.ps1                # default: 1 month test
#   .\download_chicago_taxi.ps1 -Mode test     # 1 month (2023-01)
#   .\download_chicago_taxi.ps1 -Mode full     # full year 2023
#
# Resume:
#   If the output CSV already exists, the script counts its rows
#   and resumes from that offset automatically. To start from
#   scratch, delete the CSV manually before running.
#
# Output:
#   ../_work/chicago_taxi_{range}.csv
#
# Optional: set -AppToken to relax rate limits.
# App Token: https://data.cityofchicago.org/profile/app_tokens
# ============================================================

param(
  [ValidateSet('test', 'full')]
  [string]$Mode = 'test',
  [string]$AppToken = '',
  [int]$Timeout = 300,
  [int]$MaxRetries = 6
)

# ---- Config ----
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkDir = Join-Path (Split-Path -Parent $ScriptRoot) '_work'
$BaseUrl = 'https://data.cityofchicago.org/resource/wrvz-psew.csv'
$Limit = 50000

switch ($Mode) {
  'test' {
    $From = '2023-01-01T00:00:00'
    $To = '2023-02-01T00:00:00'
    $Label = '2023_01'
  }
  'full' {
    $From = '2023-01-01T00:00:00'
    $To = '2024-01-01T00:00:00'
    $Label = '2023_full'
  }
}

$Out = Join-Path $WorkDir "chicago_taxi_$Label.csv"
$Where = "trip_start_timestamp >= '$From' AND trip_start_timestamp < '$To'"

# ---- Prepare ----
New-Item -Path $WorkDir -ItemType Directory -Force | Out-Null

$Headers = @{}
if ($AppToken) { $Headers['X-App-Token'] = $AppToken }

# ---- Resume detection ----
$StartOffset = 0
$First = $true

if (Test-Path $Out) {
  Write-Host "Existing CSV found. Counting rows for resume (may take 30-60s)..."
  $lineCount = 0
  $reader = [System.IO.StreamReader]::new($Out)
  try {
    while ($null -ne $reader.ReadLine()) { $lineCount++ }
  } finally {
    $reader.Close()
  }
  $StartOffset = [Math]::Max(0, $lineCount - 1)  # minus header
  if ($StartOffset -gt 0) {
    Write-Host "Existing data rows: $StartOffset. Resuming from offset $StartOffset."
    $First = $false
  } else {
    Remove-Item $Out
    Write-Host "Existing CSV had no data, starting fresh."
  }
}

Write-Host ""
Write-Host "==== Chicago Taxi Trips Downloader ===="
Write-Host "Mode    : $Mode"
Write-Host "Range   : $From  ->  $To"
Write-Host "Out     : $Out"
Write-Host "Timeout : ${Timeout}s per request"
Write-Host "Retries : $MaxRetries"
Write-Host "Start at: offset $StartOffset"
if (-not $AppToken) {
  Write-Host "AppToken: (not set, rate limit may apply)"
}
Write-Host ""

# ---- Paging fetch ----
$Offset = $StartOffset
$TotalRows = $StartOffset
$BatchIndex = 0
$StartTime = Get-Date

do {
  $BatchIndex++
  $EncodedWhere = [Uri]::EscapeDataString($Where)
  $Url = "$BaseUrl`?`$where=$EncodedWhere&`$limit=$Limit&`$offset=$Offset&`$order=trip_start_timestamp"

  Write-Host ("[{0,3}] offset={1,-10} fetching ..." -f $BatchIndex, $Offset) -NoNewline

  $Response = $null
  $Attempt = 0
  while ($null -eq $Response -and $Attempt -lt $MaxRetries) {
    $Attempt++
    try {
      $Response = Invoke-WebRequest -Uri $Url -Headers $Headers -UseBasicParsing -TimeoutSec $Timeout
    } catch {
      $sleep = [int]([Math]::Min(120, 5 * [Math]::Pow(2, $Attempt - 1)))
      Write-Host ""
      Write-Warning "Attempt $Attempt/$MaxRetries failed: $($_.Exception.Message)"
      if ($Attempt -lt $MaxRetries) {
        Write-Warning "Sleeping ${sleep}s before next retry..."
        Start-Sleep -Seconds $sleep
      }
    }
  }

  if ($null -eq $Response) {
    Write-Host ""
    Write-Error "All $MaxRetries attempts failed at offset $Offset."
    Write-Host "CSV is preserved at: $Out"
    Write-Host "Re-run the same command to resume from the same offset."
    exit 1
  }

  $Lines = $Response.Content -split "`r?`n" | Where-Object { $_ -ne '' }
  if ($Lines.Count -le 1) {
    Write-Host "  (empty response, stop)"
    break
  }

  $RowsThisBatch = $Lines.Count - 1
  if ($First) {
    $Lines | Out-File -FilePath $Out -Encoding utf8
    $First = $false
  } else {
    $Lines | Select-Object -Skip 1 | Add-Content -Path $Out -Encoding utf8
  }

  $TotalRows += $RowsThisBatch
  Write-Host ("  +{0,6} rows (total {1,9})" -f $RowsThisBatch, $TotalRows)

  $Offset += $Limit
} while ($RowsThisBatch -eq $Limit)

$Elapsed = (Get-Date) - $StartTime
$Size = (Get-Item $Out).Length

Write-Host ""
Write-Host "==== Done ===="
Write-Host ("Rows     : {0:N0}" -f $TotalRows)
Write-Host ("Size     : {0:N1} MB" -f ($Size / 1MB))
Write-Host ("Elapsed  : {0:N1} sec (this run)" -f $Elapsed.TotalSeconds)
Write-Host ("Out      : $Out")
Write-Host ""
Write-Host "Next: open the CSV in Tableau Desktop and convert to .hyper extract."
