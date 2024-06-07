Write-Output "Setting up Initial environment ..."
$erlPath = "C:\Program Files\erl-24.0"
$RmqPath = "C:\Program Files\RabbitMQ Server\rabbitmq_server-3.9.12"
$ProjectPath = "C:\Program Files\Mechademy\data-connector-main"

Write-Output "Installing Python ..."
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe" -OutFile "$env:TEMP\python-3.10.2-amd64.exe"
Start-Process -FilePath "$env:TEMP\python-3.10.2-amd64.exe" -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1 Include_test=0' -Wait
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Output "Installing Erlang ..."
Invoke-WebRequest -Uri "https://erlang.org/download/otp_win64_24.0.exe" -OutFile "$env:TEMP\otp_win64_24.0.exe"
Start-Process -FilePath "$env:TEMP\otp_win64_24.0.exe" -ArgumentList '/S' -Wait
[System.Environment]::SetEnvironmentVariable("ERLANG_HOME", $erlPath, [System.EnvironmentVariableTarget]::Machine)
$path = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
$newPath = "$path;$erlPath\bin"
[System.Environment]::SetEnvironmentVariable("Path", $newPath, [System.EnvironmentVariableTarget]::Machine)

Write-Output "Installing RabbitMQ ..."
Invoke-WebRequest -Uri "https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.9.12/rabbitmq-server-3.9.12.exe" -OutFile "$env:TEMP\rabbitmq-installer.exe"
# Define the path to the installer
$RabbitMqInstallerPath = "$env:TEMP\rabbitmq-installer.exe"

# Check if the installer exists
if (Test-Path $RabbitMqInstallerPath) {
    try {
        # Start the installation process with silent mode and log the output and errors
        cmd /c start /wait $RabbitMqInstallerPath /S
        
        # Check the exit code of the process
        if ($LASTEXITCODE -eq 0) {
            Write-Output "RabbitMQ installation completed successfully."
	        Stop-Service -Name RabbitMQ -WarningAction Ignore
        } else {
            Write-Output "RabbitMQ installation failed with exit code $LASTEXITCODE. Check the logs for more details."
        }
    } catch {
        Write-Error "An error occurred during RabbitMQ installation: $_"
    }
} else {
    Write-Error "Rabbit MQ Installer not found at $RabbitMqInstallerPath"
}
# Setting up RabbitMQ environment variables
[System.Environment]::SetEnvironmentVariable("RMQ_HOME", $RmqPath, [System.EnvironmentVariableTarget]::Machine)
$path = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
$newPath = "$path;$RmqPath\sbin"
[System.Environment]::SetEnvironmentVariable("Path", $newPath, [System.EnvironmentVariableTarget]::Machine)

Write-Output "Installing data-connector dependencies ..."
cd $ProjectPath
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install poetry
poetry lock --no-update
poetry install --no-root

Write-Output "Installing NSSM ..."
Invoke-WebRequest -Uri "https://www.nssm.cc/release/nssm-2.24.zip" -OutFile "$ProjectPath\nssm.zip"
Expand-Archive -Path "$ProjectPath\nssm.zip" -DestinationPath "$ProjectPath"
Remove-Item "$ProjectPath\nssm.zip"

Write-Output "Starting Services ..."
cd "$ProjectPath\nssm-2.24\win64"

.\nssm.exe start RabbitMQ

Start-Sleep -Seconds 2

.\nssm.exe install mechademy-celery-worker "$ProjectPath\start_celery_worker.bat"
.\nssm.exe set mechademy-celery-worker AppDirectory $ProjectPath
.\nssm.exe set mechademy-celery-worker AppStdout $ProjectPath\celery_worker.log
.\nssm.exe set mechademy-celery-worker AppStderr $ProjectPath\celery_worker_error.log
.\nssm.exe start mechademy-celery-worker

Start-Sleep -Seconds 2

.\nssm.exe install mechademy-celery-beat "$ProjectPath\start_celery_beat.bat"
.\nssm.exe set mechademy-celery-beat AppDirectory "$ProjectPath"
.\nssm.exe set mechademy-celery-beat AppStdout "$ProjectPath\celery_beat.log"
.\nssm.exe set mechademy-celery-beat AppStderr "$ProjectPath\celery_beat_error.log"
.\nssm.exe start mechademy-celery-beat

Start-Sleep -Seconds 2

.\nssm.exe install mechademy-server "$ProjectPath\start_server.bat"
.\nssm.exe set mechademy-server AppDirectory "$ProjectPath"
.\nssm.exe set mechademy-server AppStdout "$ProjectPath\server.log"
.\nssm.exe set mechademy-server AppStderr "$ProjectPath\server_error.log"
.\nssm.exe start mechademy-server

Write-Output "Setup Completed Successfully :)"