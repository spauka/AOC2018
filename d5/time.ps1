$sw = [Diagnostics.Stopwatch]::StartNew()
python .\d5_opt.py
$sw.Stop()
$sw.Elapsed