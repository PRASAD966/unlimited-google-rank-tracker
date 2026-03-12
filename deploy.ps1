$dest = "root@72.61.171.138"
$destPath = "/home/rankplex/htdocs/rank1"
$zipFile = "deploy.zip"

# Clean up previous zip
if (Test-Path $zipFile) { Remove-Item $zipFile }

# Gather files excluding .venv, __pycache__, and local data files
$files = Get-ChildItem -Path . -Exclude ".venv", "__pycache__", "rankplex.db", "rankplex_tasks.json", "users.json", "tokens.json", "deploy.zip", "deploy.ps1", ".git", ".env" -Recurse

# Create archive
Write-Host "Creating archive..."
Compress-Archive -Path $files -DestinationPath $zipFile

Write-Host "Transferring $zipFile to $dest..."
scp $zipFile "$($dest):$destPath"

Write-Host "Executing deployment commands on server..."
ssh $dest "cd $destPath && unzip -o $zipFile && rm $zipFile && docker-compose down && docker-compose up -d --build"

Write-Host "Deployment complete!"
