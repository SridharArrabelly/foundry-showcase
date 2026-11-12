$ErrorActionPreference = 'Stop'
$account = (& az cognitiveservices account show `
    --subscription '40b687ca-31b5-4374-bea2-4c178369b9c0' `
    --resource-group 'rg-volt-citadel' `
    --name 'fdy-volt-citadel-261111' --output json) | ConvertFrom-Json
if ($LASTEXITCODE -ne 0 -or $account.name -ne 'fdy-volt-citadel-261111') {
    throw 'The separate Volt demo account could not be resolved.'
}
if ($account.properties.provisioningState -ne 'Succeeded') {
    throw 'Wait for the Foundry account deployment before applying its approved network configuration.'
}
# The pinned Citadel template hard-codes Deny. This approved demo-only overlay also disables API keys.
& az resource update --ids $account.id `
    --set properties.publicNetworkAccess=Enabled properties.networkAcls.defaultAction=Allow properties.disableLocalAuth=true `
    --query 'properties.{publicNetworkAccess:publicNetworkAccess,defaultAction:networkAcls.defaultAction,disableLocalAuth:disableLocalAuth}' `
    --output json
if ($LASTEXITCODE -ne 0) {
    throw 'Failed to apply the approved demo network overlay.'
}
