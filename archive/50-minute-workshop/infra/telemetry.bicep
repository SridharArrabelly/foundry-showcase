param location string = resourceGroup().location
param accountName string
param projectName string

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: accountName
}
resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' existing = {
  parent: account
  name: projectName
}
resource workspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-foundry-showcase'
  location: location
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
    workspaceCapping: { dailyQuotaGb: 1 }
  }
}
resource insights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-foundry-showcase'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: workspace.id
    RetentionInDays: 30
  }
}
resource connection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-06-01' = {
  parent: project
  name: 'showcase-appinsights'
  properties: {
    authType: 'ApiKey'
    category: 'AppInsights'
    target: insights.id
    credentials: { key: insights.properties.ConnectionString }
    metadata: {
      ApiType: 'Azure'
      ResourceId: insights.id
    }
  }
}
resource reader 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(insights.id, project.id, 'monitoring-reader')
  scope: insights
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '43d0d8ad-25c7-4714-9337-8ba259a9fe05')
    principalId: project.identity.principalId
    principalType: 'ServicePrincipal'
  }
}
output applicationInsightsId string = insights.id
output workspaceId string = workspace.id
