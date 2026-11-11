targetScope = 'resourceGroup'

param accountName string = 'fdy-volt-citadel-261111'
param projectName string = 'volt-dev'
param apimName string = 'apim-volt-citadel-261111'

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: accountName
}
resource project 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' existing = {
  parent: account
  name: projectName
}
resource apim 'Microsoft.ApiManagement/service@2024-05-01' existing = {
  name: apimName
}
resource subscription 'Microsoft.ApiManagement/service/subscriptions@2024-05-01' existing = {
  parent: apim
  name: 'TOOL-Volt-Support-DEV-SUB-01'
}
resource connection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-10-01-preview' = {
  parent: project
  name: 'volt-business-tools'
  properties: {
    category: 'RemoteTool'
    authType: 'CustomKeys'
    target: '${apim.properties.gatewayUrl}/volt-tools/mcp'
    isSharedToAll: false
    credentials: {
      keys: {
        'api-key': subscription.listSecrets().primaryKey
      }
    }
    metadata: {
      ApiType: 'Azure'
    }
  }
}
output connectionName string = connection.name
