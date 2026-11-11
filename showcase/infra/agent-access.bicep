targetScope = 'resourceGroup'

@description('The deployed hosted agent instance_identity.principal_id, read from Foundry.')
param agentPrincipalId string
param accountName string = 'fdy-volt-citadel-261111'
param projectName string = 'volt-dev'
param enableMemory bool = true
@description('Optional signed-in user object ID for Memory embedding authorization; never a credential.')
param callerPrincipalId string = ''

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: accountName
}
resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' existing = {
  parent: account
  name: projectName
}
var runtimeRoles = concat([
  '53ca6127-db72-4b80-b1b0-d745d6d5456d'
], enableMemory ? [
  '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'
] : [])

resource runtimeAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for role in runtimeRoles: {
  name: guid(project.id, agentPrincipalId, role)
  scope: project
  properties: {
    principalId: agentPrincipalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', role)
  }
}]

resource callerEmbeddingAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (enableMemory && !empty(callerPrincipalId)) {
  name: guid(project.id, callerPrincipalId, '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd')
  scope: project
  properties: {
    principalId: callerPrincipalId
    principalType: 'User'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd')
  }
}

resource projectEmbeddingAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (enableMemory) {
  name: guid(account.id, project.id, 'memory-embedding', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd')
  scope: account
  properties: {
    principalId: project.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd')
  }
}

resource projectMemoryAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (enableMemory) {
  name: guid(account.id, project.id, 'memory-model-access', '53ca6127-db72-4b80-b1b0-d745d6d5456d')
  scope: account
  properties: {
    principalId: project.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '53ca6127-db72-4b80-b1b0-d745d6d5456d')
  }
}
