targetScope = 'resourceGroup'

param accountName string = 'fdy-volt-citadel-261111'
param projectName string
param searchName string = 'srch-volt-citadel-261111'
param existingRetrievalRoleName string = ''
param connectionName string = 'volt-policy-knowledge'

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: accountName
}
resource project 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' existing = {
  parent: account
  name: projectName
}
resource search 'Microsoft.Search/searchServices@2025-05-01' existing = {
  name: searchName
}
resource retrievalAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: empty(existingRetrievalRoleName) ? guid(search.id, project.id, 'knowledge-reader') : existingRetrievalRoleName
  scope: search
  properties: {
    principalId: project.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '1407120a-92aa-4202-b7e9-c0e197c71c8f')
  }
}
resource connection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-10-01-preview' = {
  parent: project
  name: connectionName
  properties: {
    category: 'RemoteTool'
    authType: 'ProjectManagedIdentity'
    audience: 'https://search.azure.com/'
    target: 'https://${search.name}.search.windows.net/knowledgebases/volt-support-knowledge/mcp?api-version=2026-08-01-preview'
    isSharedToAll: false
  }
}
output connectionName string = connection.name
