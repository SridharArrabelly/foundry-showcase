using '../../.runtime/ai-hub-gateway-solution-accelerator-81599b31dfbaee20ebd3a6d2ba9b07dde3c31814/bicep/infra/citadel-access-contracts/main.bicep'

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
param useTargetFoundry = false
param useCase = {
  businessUnit: 'Volt'
  useCaseName: 'Support'
  environment: 'DEV'
}
param apiNameMapping = {
  TOOL: ['volt-business-mcp', 'volt-business-api']
}
param services = [{
  code: 'TOOL'
  apiKeySecretName: 'volt-dev-tool-key'
  endpointSecretName: 'volt-dev-tool-endpoint'
  policyXml: '''
<policies>
  <inbound>
    <base />
    <rate-limit-by-key calls="60" renewal-period="60" counter-key="@(context.Subscription.Id)" />
  </inbound>
  <backend><base /></backend>
  <outbound><base /></outbound>
  <on-error><base /></on-error>
</policies>
'''
}]
param productTerms = 'Synthetic read-only tools. Foundry-to-toolbox uses Entra; toolbox-to-APIM uses this managed per-use-case credential.'
