$sw = [Diagnostics.Stopwatch]::StartNew()
python .\d9.py
$sw.Stop()
$sw.Elapsed