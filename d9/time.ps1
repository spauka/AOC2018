$sw = [Diagnostics.Stopwatch]::StartNew()
python .\d9_opt.py
$sw.Stop()
$sw.Elapsed