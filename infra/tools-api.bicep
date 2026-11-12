targetScope = 'resourceGroup'

@secure()
param functionKey string
param toolsEndpoint string
param apimName string = 'apim-volt-citadel-261111'
param vaultName string = 'kv-2b36dghmyp5qg'

resource vault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: vaultName
}
resource secret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: vault
  name: 'volt-tools-function-key'
  properties: {
    value: functionKey
    contentType: 'application/x-functions-key'
  }
}
resource apim 'Microsoft.ApiManagement/service@2024-05-01' existing = {
  name: apimName
}
resource backendKey 'Microsoft.ApiManagement/service/namedValues@2024-05-01' = {
  parent: apim
  name: 'volt-tools-function-key'
  properties: {
    displayName: 'volt-tools-function-key'
    secret: true
    keyVault: {
      secretIdentifier: '${vault.properties.vaultUri}secrets/${secret.name}'
    }
  }
}
resource api 'Microsoft.ApiManagement/service/apis@2024-05-01' = {
  parent: apim
  name: 'volt-business-api'
  properties: {
    displayName: 'Volt synthetic business API'
    description: 'Read-only synthetic product, order, recall and replacement operations.'
    path: 'volt-business'
    serviceUrl: toolsEndpoint
    protocols: ['https']
    subscriptionRequired: true
    subscriptionKeyParameterNames: {
      header: 'x-mcp-sub-key'
      query: 'source-key'
    }
    format: 'openapi+json'
    value: loadTextContent('../tools/openapi.json')
  }
}
resource policy 'Microsoft.ApiManagement/service/apis/policies@2024-05-01' = {
  parent: api
  name: 'policy'
  properties: {
    format: 'rawxml'
    value: '''
<policies>
  <inbound>
    <base />
    <set-header name="x-functions-key" exists-action="override">
      <value>{{volt-tools-function-key}}</value>
    </set-header>
  </inbound>
  <backend><base /></backend>
  <outbound><base /></outbound>
  <on-error><base /></on-error>
</policies>
'''
  }
  dependsOn: [backendKey]
}

module mcp '../.runtime/ai-hub-gateway-solution-accelerator-81599b31dfbaee20ebd3a6d2ba9b07dde3c31814/bicep/infra/citadel-publish-contracts/modules/publishMcpFromApi.bicep' = {
  name: 'volt-business-mcp'
  params: {
    apimServiceName: apim.name
    sourceApiName: api.name
    operationNames: [
      'searchProductCatalog'
      'checkCompatibility'
      'getRecallNotices'
      'getOrderStatus'
      'getReturnWarrantyEligibility'
    ]
    mcpName: 'volt-business-mcp'
    mcpDisplayName: 'Volt governed business tools'
    mcpDescription: 'Synthetic read-only business tools, published through Citadel.'
    mcpPath: 'volt-tools'
    mcpSubscriptionRequired: true
    subscriptionKeyHeaderName: 'api-key'
    forwardSubscriptionKeyToSource: true
    sourceSubscriptionKeyHeaderName: 'x-mcp-sub-key'
  }
  dependsOn: [policy]
}

output mcpEndpoint string = mcp.outputs.endpoint
