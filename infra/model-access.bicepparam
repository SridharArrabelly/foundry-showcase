using '../.runtime/ai-hub-gateway-solution-accelerator-81599b31dfbaee20ebd3a6d2ba9b07dde3c31814/bicep/infra/citadel-access-contracts/main.bicep'

param apim = {
  subscriptionId: '40b687ca-31b5-4374-bea2-4c178369b9c0'
  resourceGroupName: 'rg-volt-citadel'
  name: 'apim-volt-citadel-261111'
}
param keyVault = {
  subscriptionId: '40b687ca-31b5-4374-bea2-4c178369b9c0'
  resourceGroupName: 'rg-volt-citadel'
  name: 'kv-2b36dghmyp5qg'
}
param useTargetAzureKeyVault = true
param useTargetFoundry = true
param foundry = {
  subscriptionId: '40b687ca-31b5-4374-bea2-4c178369b9c0'
  resourceGroupName: 'rg-volt-citadel'
  accountName: 'fdy-volt-citadel-261111'
  projectName: 'volt-dev'
}
param foundryConfig = {
  connectionNamePrefix: 'volt-models'
  connectionCategory: 'ApiManagement'
  authType: 'ProjectManagedIdentity'
  managedIdentityAudience: 'https://cognitiveservices.azure.com'
  deploymentInPath: 'false'
  isSharedToAll: false
  deploymentProvider: 'AzureOpenAI'
}
param useCase = {
  businessUnit: 'Volt'
  useCaseName: 'Support'
  environment: 'DEV'
}
param apiNameMapping = {
  LLM: ['universal-llm-api']
}
param services = [
  {
    code: 'LLM'
    endpointSecretName: 'volt-dev-model-endpoint'
    apiKeySecretName: 'volt-dev-model-key'
    policyXml: loadTextContent('model-access-policy.xml')
  }
]
param productTerms = 'Synthetic internal enablement only. Entra token plus use-case subscription required. Not a monetary spending cap.'
