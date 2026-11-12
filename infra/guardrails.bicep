targetScope = 'resourceGroup'

param accountName string = 'fdy-volt-citadel-261111'

resource account 'Microsoft.CognitiveServices/accounts@2024-10-01' existing = {
  name: accountName
}

resource blocklist 'Microsoft.CognitiveServices/accounts/raiBlocklists@2024-10-01' = {
  parent: account
  name: 'volt-demo-markers'
  properties: {
    description: 'Harmless synthetic marker for a repeatable platform-block demonstration.'
  }
}

resource marker 'Microsoft.CognitiveServices/accounts/raiBlocklists/raiBlocklistItems@2024-10-01' = {
  parent: blocklist
  name: 'synthetic-block-test'
  properties: {
    pattern: 'VOLT_DEMO_BLOCK_MARKER_261111'
    isRegex: false
  }
}

var categories = ['Hate', 'Sexual', 'Selfharm', 'Violence']
var promptControls = [for category in categories: {
    name: category
    enabled: true
    blocking: true
    severityThreshold: 'Medium'
    source: 'Prompt'
}]
var completionControls = [for category in categories: {
    name: category
    enabled: true
    blocking: true
    severityThreshold: 'Medium'
    source: 'Completion'
}]

resource policy 'Microsoft.CognitiveServices/accounts/raiPolicies@2024-10-01' = {
  parent: account
  name: 'volt-support-guardrails'
  properties: {
    basePolicyName: 'Microsoft.DefaultV2'
    mode: 'Default'
    contentFilters: concat(promptControls, completionControls, [
      {
        name: 'Jailbreak'
        enabled: true
        blocking: true
        source: 'Prompt'
      }
    ])
    customBlocklists: [
      {
        blocklistName: blocklist.name
        blocking: true
        source: 'Prompt'
      }
    ]
  }
  dependsOn: [
    marker
  ]
}

output guardrailResourceId string = policy.id
