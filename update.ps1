$nssmPath = "C:\Program Files\Mechademy\nssm-2.24\win64"
$ProjectPath = "C:\Program Files\Mechademy\data-connector"


Write-Output "Updating project..."

cd $nssmPath
.\nssm.exe stop mechademy-celery-worker > $null
Start-Sleep -Seconds 2
.\nssm.exe stop mechademy-celery-beat > $null

cd $ProjectPath
# Run git stash and capture the output
$stashOutput = git stash

# Run git pull
git pull

# Check if any files were stashed
if ($stashOutput -notmatch "No local changes to save") {
    # If files were stashed, run git pop
    git stash pop *>$null
}

Write-Output "Restarting services..."

cd $nssmPath
.\nssm.exe start mechademy-celery-worker > $null
Start-Sleep -Seconds 2
.\nssm.exe start mechademy-celery-beat > $null

cd $ProjectPath
Write-Output "Project updated successfully..."