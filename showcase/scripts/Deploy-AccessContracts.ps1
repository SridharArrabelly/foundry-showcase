param(
    [Parameter(Mandatory)]
    [ValidateSet('DEV', 'DEMO')]
    [string] $Environment
)

$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$infra = Join-Path $root 'showcase\infra'
$pin = Get-Content (Join-Path $infra 'citadel-source.json') -Raw | ConvertFrom-Json
$account = az account show --query '{subscription:id,tenant:tenantId}' -o json --only-show-errors | ConvertFrom-Json
if ($LASTEXITCODE -ne 0 -or $account.subscription -ne $pin.subscription -or $account.tenant -ne $pin.tenant) {
    throw 'Select the approved showcase subscription and tenant before deployment.'
}
$template = Join-Path $root ".runtime\ai-hub-gateway-solution-accelerator-$($pin.commit)\bicep\infra\citadel-access-contracts\main.bicep"
if (-not (Test-Path -LiteralPath $template)) {
    throw 'Run Get-CitadelSource.ps1 to restore the reviewed pinned templates first.'
}
$label = $Environment.ToLowerInvariant()
$project = "volt-$label"
$connectionPrefix = if ($Environment -eq 'DEV') { 'volt' } else { "volt-$label" }

foreach ($kind in @('model', 'tool')) {
    $parametersPath = Join-Path $root ".runtime\volt-$label-$kind-access.parameters.json"
    az bicep build-params --file (Join-Path $infra "$kind-access.bicepparam") --outfile $parametersPath --only-show-errors
    if ($LASTEXITCODE -ne 0) { throw "Cannot compile $kind access parameters." }
    $parameters = Get-Content $parametersPath -Raw | ConvertFrom-Json
    $parameters.parameters.useCase.value.environment = $Environment
    if ($kind -eq 'model') {
        $parameters.parameters.foundry.value.projectName = $project
        $parameters.parameters.foundryConfig.value.connectionNamePrefix = "$connectionPrefix-models"
    }
    foreach ($service in $parameters.parameters.services.value) {
        $service.apiKeySecretName = $service.apiKeySecretName.Replace('volt-dev-', "volt-$label-")
        $service.endpointSecretName = $service.endpointSecretName.Replace('volt-dev-', "volt-$label-")
    }
    $parameters | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $parametersPath -Encoding utf8
    az deployment sub create --subscription $pin.subscription --location $pin.region `
        --name "volt-$label-$kind-access" --template-file $template `
        --parameters "@$parametersPath" --query properties.provisioningState -o tsv --only-show-errors
    if ($LASTEXITCODE -ne 0) { throw "$kind access deployment failed; inspect it before retrying." }
}

az deployment group create --subscription $pin.subscription --resource-group rg-volt-citadel `
    --name "volt-$label-tool-connection" --template-file (Join-Path $infra 'tool-connection.bicep') `
    --parameters projectName=$project apimSubscriptionName="TOOL-Volt-Support-$Environment-SUB-01" connectionName="$connectionPrefix-business-tools" `
    --query properties.provisioningState -o tsv --only-show-errors
if ($LASTEXITCODE -ne 0) { throw 'Tool connection deployment failed.' }

$projectId = "/subscriptions/$($pin.subscription)/resourceGroups/rg-volt-citadel/providers/Microsoft.CognitiveServices/accounts/fdy-volt-citadel-261111/projects/$project"
$principal = az resource show --ids $projectId --api-version 2025-04-01-preview --query identity.principalId -o tsv --only-show-errors
if ($LASTEXITCODE -ne 0 -or -not $principal) { throw 'Cannot resolve the selected project identity.' }
$searchId = "/subscriptions/$($pin.subscription)/resourceGroups/rg-volt-citadel/providers/Microsoft.Search/searchServices/srch-volt-citadel-261111"
$existingRole = az role assignment list --scope $searchId --fill-principal-name false --fill-role-definition-name false `
    --query "[?principalId=='$principal' && ends_with(roleDefinitionId, '/1407120a-92aa-4202-b7e9-c0e197c71c8f')].name | [0]" `
    -o tsv --only-show-errors
if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect the existing Search role; refusing a duplicate assignment.' }
az deployment group create --subscription $pin.subscription --resource-group rg-volt-citadel `
    --name "volt-$label-knowledge-connection" --template-file (Join-Path $infra 'knowledge-connection.bicep') `
    --parameters projectName=$project "existingRetrievalRoleName=$existingRole" connectionName="$connectionPrefix-policy-knowledge" `
    --query properties.provisioningState -o tsv --only-show-errors
if ($LASTEXITCODE -ne 0) { throw 'Knowledge connection deployment failed.' }
Write-Host "Prepared $project access contracts and connections. No agent version was promoted."
