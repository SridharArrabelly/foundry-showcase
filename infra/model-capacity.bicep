targetScope = 'resourceGroup'

@minValue(1)
param capacity int

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: 'fdy-volt-citadel-261111'
}
resource model 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: account
  name: 'gpt-5.4-mini'
  sku: {
    name: 'DataZoneStandard'
    capacity: capacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-5.4-mini'
      version: '2026-03-17'
    }
    raiPolicyName: 'Microsoft.DefaultV2'
    versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
  }
}
