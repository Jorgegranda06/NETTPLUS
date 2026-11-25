$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
Set-Location backend
if (!(Test-Path .venv)) { py -3 -m venv .venv }
$python = '.\.venv\Scripts\python.exe'
& $python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Error instalando Python' }
if (!(Test-Path .env)) { $u=Read-Host 'Usuario MySQL'; $p=Read-Host 'Password MySQL' -AsSecureString; $plain=[System.Net.NetworkCredential]::new('', $p).Password; $secret=[guid]::NewGuid().ToString()+[guid]::NewGuid().ToString(); @("DB_NAME=nettplus_db","DB_USER=$u",("DB_PASSWORD=" + ($plain | ConvertTo-Json -Compress)),"SECRET_KEY=$secret") | Set-Content .env -Encoding UTF8 }
& $python manage.py makemigrations negocio
if ($LASTEXITCODE -ne 0) { throw 'Error migraciones' }
& $python manage.py migrate
if ($LASTEXITCODE -ne 0) { throw 'Error MySQL' }
& $python manage.py createsuperuser
Set-Location ../frontend
npm install
if ($LASTEXITCODE -ne 0) { throw 'Error npm' }
npm run build
if ($LASTEXITCODE -ne 0) { throw 'Error build' }
if (!(Test-Path android)) { npx cap add android }
npx cap sync android
