param([string]$EnvironmentName = 'showcase')
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
$target = Get-Content config\demo-target.json | ConvertFrom-Json
function Invoke-Azd {
    & azd @args
    if ($LASTEXITCODE -ne 0) { throw "azd failed: $($args[0..1] -join ' ')" }
}
$environments = (& azd env list --output json | ConvertFrom-Json)
if ($LASTEXITCODE -ne 0) { throw 'Cannot list local azd environments' }
if ($environments | Where-Object name -eq $EnvironmentName) {
    Invoke-Azd env select $EnvironmentName
} else {
    Invoke-Azd env new $EnvironmentName --no-prompt
}
$values = @{
    AZURE_SUBSCRIPTION_ID = $target.subscription_id
    AZURE_TENANT_ID = $target.tenant_id
    AZURE_LOCATION = $target.location
    AZURE_RESOURCE_GROUP = $target.resource_group
    AZURE_AI_PROJECT_ID = $target.project_id
    FOUNDRY_PROJECT_ENDPOINT = $target.project_endpoint
    AZURE_AI_PROJECT_ENDPOINT = $target.project_endpoint
    AZURE_AI_MODEL_DEPLOYMENT_NAME = $target.model_deployment
    VOLT_VARIANT = 'improved'
}
foreach ($key in $values.Keys) { Invoke-Azd env set $key $values[$key] }
$connection = & az resource show --subscription $target.subscription_id `
    --resource-group $target.resource_group --name $target.app_insights_name `
    --resource-type Microsoft.Insights/components --api-version 2020-02-02 `
    --query properties.ConnectionString -o tsv
if ($LASTEXITCODE -ne 0 -or -not $connection) { throw 'Cannot read the authorized telemetry configuration' }
Invoke-Azd env set APPLICATIONINSIGHTS_CONNECTION_STRING $connection
Write-Host 'Local configuration now points to the existing demo. No cloud resources were created.'
