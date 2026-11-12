param accountName string
param projectName string
param repository string
@description('Exact subject emitted by the GitHub OIDC token. New repositories can include immutable owner/repository IDs.')
param oidcSubject string = 'repo:${repository}:ref:refs/heads/main'
param location string = resourceGroup().location

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = { name: accountName }
resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' existing = {
  parent: account
  name: projectName
}
resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-foundry-showcase-ci'
  location: location
}
resource federation 'Microsoft.ManagedIdentity/userAssignedIdentities/federatedIdentityCredentials@2023-01-31' = {
  parent: identity
  name: 'github-main'
  properties: {
    issuer: 'https://token.actions.githubusercontent.com'
    subject: oidcSubject
    audiences: ['api://AzureADTokenExchange']
  }
}
resource contributor 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(project.id, identity.id, 'contributor')
  scope: project
  properties: {
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'b24988ac-6180-42a0-ab88-20f7382dd24c')
  }
}
resource user 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(account.id, identity.id, 'foundry-user')
  scope: account
  properties: {
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '53ca6127-db72-4b80-b1b0-d745d6d5456d')
  }
}
output clientId string = identity.properties.clientId
