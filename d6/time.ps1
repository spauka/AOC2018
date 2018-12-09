$sw = [Diagnostics.Stopwatch]::StartNew()
python .\d6.py
$sw.Stop()
$sw.Elapsed