$filePath = 'D:\Projects\CalibraFit\app\src\app\dashboard\page.js'
$lines = Get-Content $filePath -TotalCount 555
$lines | Set-Content $filePath
