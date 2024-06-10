Write-Output "Starting server..."
Start-Sleep -Seconds 2

.\nssm.exe install mechademy-server "$ProjectPath\start_server.bat"
.\nssm.exe set mechademy-server AppDirectory "$ProjectPath"
.\nssm.exe set mechademy-server AppStdout "$ProjectPath\server.log"
.\nssm.exe set mechademy-server AppStderr "$ProjectPath\server_error.log"
.\nssm.exe start mechademy-server

Write-Output "Server started successfully :)"