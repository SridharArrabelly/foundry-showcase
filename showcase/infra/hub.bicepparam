using '../../.runtime/ai-hub-gateway-solution-accelerator-81599b31dfbaee20ebd3a6d2ba9b07dde3c31814/bicep/infra/main.bicep'

param environmentName = 'volt-citadel'
param location = 'swedencentral'
param apicLocation = 'swedencentral'
param resourceGroupName = 'rg-volt-citadel'
param tags = {
  Environment: 'InternalEnablement'
  Workload: 'VoltShowcase'
  DataClassification: 'SyntheticOnly'
  'azd-env-name': 'volt-citadel'
}

param apimServiceName = 'apim-volt-citadel-261111'
param apimSku = 'Developer'
param apimSkuUnits = 1
param eventHubCapacityUnits = 1
param cosmosDbRUs = 400
param logicAppsSkuCapacityUnits = 1
param apicSku = 'Free'
param enableAPICenter = true
param enableManagedRedis = false
param enableDocumentIntelligence = false
param enableAzureAISearch = false
param enableOpenAIRealtime = false
param enableAIModelInference = true
param enableUnifiedAiApi = true
param enableAIGatewayPiiRedaction = false
param createAppInsightsDashboards = false

// New demo endpoints use authenticated public access; this is not a private-network showcase.
param apimNetworkType = 'External'
param apimV2UsePrivateEndpoint = false
param foundryNetworkInjectionEnabled = false
param aiFoundryExternalNetworkAccess = 'Enabled'
param keyVaultExternalNetworkAccess = 'Enabled'
param cosmosDbPublicAccess = 'Disabled'
param useAzureMonitorPrivateLinkScope = false

// Subscription authentication is enforced initially; use-case JWT contracts are added separately.
param entraAuth = false
param aiSearchInstances = []
param aiFoundryInstances = [
  {
    name: 'fdy-volt-citadel-261111'
    location: 'swedencentral'
    customSubDomainName: 'fdy-volt-citadel-261111'
    defaultProjectName: 'volt-dev'
    networkInjectionEnabled: false
  }
]
param aiFoundryModelsConfig = [
  {
    name: 'gpt-5.4-mini'
    publisher: 'OpenAI'
    version: '2026-03-17'
    sku: 'DataZoneStandard'
    capacity: 10
    aiserviceIndex: 0
    apiVersion: '2025-04-01-preview'
  }
  {
    name: 'gpt-5.4'
    publisher: 'OpenAI'
    version: '2026-03-05'
    sku: 'DataZoneStandard'
    capacity: 5
    aiserviceIndex: 0
    apiVersion: '2025-04-01-preview'
  }
  {
    name: 'text-embedding-3-small'
    publisher: 'OpenAI'
    version: '1'
    sku: 'DataZoneStandard'
    capacity: 10
    aiserviceIndex: 0
  }
]
param primaryFoundryEmbeddingModelName = 'text-embedding-3-small'

param azureMonitorLogSettings = {
  frontend: {
    request: { headers: [], body: { bytes: 0 } }
    response: { headers: [], body: { bytes: 0 } }
  }
  backend: {
    request: { headers: [], body: { bytes: 0 } }
    response: { headers: [], body: { bytes: 0 } }
  }
  largeLanguageModel: {
    logs: 'disabled'
  }
}
param appInsightsLogSettings = {
  headers: ['Content-type', 'x-ms-region']
  body: { bytes: 0 }
}
