# Testa README: Parte 1 (cadastro + ativação) e Parte 2 (login JWT + refresh).
# Pré-requisito: API a correr, ex.:  python run.py  (por defeito http://127.0.0.1:5000)
param(
    [string]$BaseUrl = "http://127.0.0.1:5000"
)

$ErrorActionPreference = "Stop"
$suffix = Get-Random -Minimum 10000 -Maximum 99999
$email = "mercado$suffix@test.local"
$cnpj = "00.000.000/0001-$suffix"
$celular = "+55999$suffix"

Write-Host "=== GET /api (health) ===" -ForegroundColor Cyan
try {
    Invoke-RestMethod -Uri "$BaseUrl/api" -Method Get
} catch {
    Write-Host "Falhou. A API está a correr em $BaseUrl ?" -ForegroundColor Red
    throw
}

Write-Host "`n=== 1) POST /api/sellers (cadastro, status Inativo) ===" -ForegroundColor Cyan
$createBody = @{
    nome     = "Mini Mercado Teste $suffix"
    cnpj     = $cnpj
    email    = $email
    celular  = $celular
    senha    = "123456"
} | ConvertTo-Json

$created = Invoke-RestMethod -Uri "$BaseUrl/api/sellers" -Method Post -Body $createBody -ContentType "application/json"
$created | ConvertTo-Json -Depth 5
$codigo = [string]$created.codigo_ativacao
if ($codigo.Length -ne 4) {
    throw "Resposta sem codigo_ativacao de 4 digitos (recebido: '$codigo')."
}

Write-Host "`n=== 2) POST /api/sellers/activate (mesmo celular + codigo da resposta) ===" -ForegroundColor Cyan
$activateBody = @{
    celular = $celular
    codigo  = $codigo
} | ConvertTo-Json

Invoke-RestMethod -Uri "$BaseUrl/api/sellers/activate" -Method Post -Body $activateBody -ContentType "application/json" | ConvertTo-Json -Depth 5

Write-Host "`n=== 3) POST /api/sellers/login (README menciona /api/auth/login; na API real e este) ===" -ForegroundColor Cyan
$loginBody = @{
    email = $email
    senha = "123456"
} | ConvertTo-Json

$auth = Invoke-RestMethod -Uri "$BaseUrl/api/sellers/login" -Method Post -Body $loginBody -ContentType "application/json"
$auth | ConvertTo-Json -Depth 5

Write-Host "`n=== 4) POST /api/sellers/refresh (novo access_token) ===" -ForegroundColor Cyan
$headers = @{ Authorization = "Bearer $($auth.refresh_token)" }
$refreshed = Invoke-RestMethod -Uri "$BaseUrl/api/sellers/refresh" -Method Post -Headers $headers
$refreshed | ConvertTo-Json

Write-Host "`nConcluido." -ForegroundColor Green
