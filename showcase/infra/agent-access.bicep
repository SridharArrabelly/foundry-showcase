targetScope = 'resourceGroup'

@description('The deployed hosted agent instance_identity.principal_id, read from Foundry.')
param agentPrincipalId string
param accountName string = 'fdy-volt-citadel-261111'
param projectName string = 'volt-dev'

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: accountName
}
resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' existing = {
  parent: account
  name: projectName
}
resource runtimeAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(project.id, agentPrincipalId, '53ca6127-db72-4b80-b1b0-d745d6d5456d')
  scope: project
  properties: {
    principalId: agentPrincipalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '53ca6127-db72-4b80-b1b0-d745d6d5456d')
  }
}
