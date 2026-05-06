# Testa README: Parte 3 (gerenciamento de produtos) e Parte 4 (vendas).
# Faz cadastro -> ativacao -> login para obter o token, e depois exercita
# todos os endpoints de produtos e vendas.
# Pre-requisito: API a correr, ex.:  python run.py  (por defeito http://127.0.0.1:5000)
param(
    [string]$BaseUrl = "http://127.0.0.1:5000"
)

$ErrorActionPreference = "Stop"
$suffix = Get-Random -Minimum 10000 -Maximum 99999
$email = "mercado$suffix@test.local"
$cnpj = "00.000.000/0001-$suffix"
$celular = "+55999$suffix"

Write-Host "=== Setup: cadastro + ativacao + login ===" -ForegroundColor Cyan

$createBody = @{
    nome    = "Mini Mercado Teste $suffix"
    cnpj    = $cnpj
    email   = $email
    celular = $celular
    senha   = "123456"
} | ConvertTo-Json
$created = Invoke-RestMethod -Uri "$BaseUrl/api/sellers" -Method Post -Body $createBody -ContentType "application/json"
$codigo = [string]$created.codigo_ativacao

$activateBody = @{ celular = $celular; codigo = $codigo } | ConvertTo-Json
Invoke-RestMethod -Uri "$BaseUrl/api/sellers/activate" -Method Post -Body $activateBody -ContentType "application/json" | Out-Null

$loginBody = @{ email = $email; senha = "123456" } | ConvertTo-Json
$auth = Invoke-RestMethod -Uri "$BaseUrl/api/sellers/login" -Method Post -Body $loginBody -ContentType "application/json"
$token = $auth.access_token
$headers = @{ Authorization = "Bearer $token" }

Write-Host "`n=== 1) POST /api/products (criar produto) ===" -ForegroundColor Cyan
$prodBody = @{
    nome       = "Arroz"
    preco      = 10.50
    quantidade = 100
    status     = "Ativo"
    img        = "https://exemplo.com/arroz.png"
} | ConvertTo-Json
$prod = Invoke-RestMethod -Uri "$BaseUrl/api/products" -Method Post -Headers $headers -Body $prodBody -ContentType "application/json"
$prod | ConvertTo-Json -Depth 5
$prodId = $prod.produto.id

Write-Host "`n=== 2) GET /api/products (listar produtos) ===" -ForegroundColor Cyan
Invoke-RestMethod -Uri "$BaseUrl/api/products" -Method Get -Headers $headers | ConvertTo-Json -Depth 5

Write-Host "`n=== 3) GET /api/products/$prodId (detalhe) ===" -ForegroundColor Cyan
Invoke-RestMethod -Uri "$BaseUrl/api/products/$prodId" -Method Get -Headers $headers | ConvertTo-Json -Depth 5

Write-Host "`n=== 4) PUT /api/products/$prodId (editar) ===" -ForegroundColor Cyan
$updateBody = @{
    nome       = "Arroz Integral"
    preco      = 12.00
    quantidade = 50
    status     = "Ativo"
} | ConvertTo-Json
Invoke-RestMethod -Uri "$BaseUrl/api/products/$prodId" -Method Put -Headers $headers -Body $updateBody -ContentType "application/json" | ConvertTo-Json -Depth 5

Write-Host "`n=== 5) POST /api/sales (vender 2 unidades) ===" -ForegroundColor Cyan
$saleBody = @{ produtoId = $prodId; quantidade = 2 } | ConvertTo-Json
Invoke-RestMethod -Uri "$BaseUrl/api/sales" -Method Post -Headers $headers -Body $saleBody -ContentType "application/json" | ConvertTo-Json -Depth 5

Write-Host "`n=== 6) GET /api/sales (listar vendas) ===" -ForegroundColor Cyan
Invoke-RestMethod -Uri "$BaseUrl/api/sales" -Method Get -Headers $headers | ConvertTo-Json -Depth 5

Write-Host "`n=== 7) PATCH /api/products/$prodId/inactivate ===" -ForegroundColor Cyan
Invoke-RestMethod -Uri "$BaseUrl/api/products/$prodId/inactivate" -Method Patch -Headers $headers | ConvertTo-Json -Depth 5

Write-Host "`n=== 8) Tentar vender produto inativo (deve falhar 400) ===" -ForegroundColor Cyan
try {
    Invoke-RestMethod -Uri "$BaseUrl/api/sales" -Method Post -Headers $headers -Body $saleBody -ContentType "application/json"
    Write-Host "ERRO: deveria ter falhado." -ForegroundColor Red
} catch {
    Write-Host "OK - venda bloqueada como esperado:" -ForegroundColor Green
    Write-Host $_.ErrorDetails.Message
}

Write-Host "`nConcluido." -ForegroundColor Green
