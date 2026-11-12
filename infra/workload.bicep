targetScope = 'resourceGroup'

param location string = 'swedencentral'
param foundryAccountName string = 'fdy-volt-citadel-261111'
param workspaceName string
param toolsAppName string = 'func-volt-tools-261111'
param searchName string = 'srch-volt-citadel-261111'
param tags object = {
  Environment: 'InternalEnablement'
  Workload: 'VoltShowcase'
  DataClassification: 'SyntheticOnly'
}

resource foundry 'Microsoft.CognitiveServices/accounts@2026-01-15-preview' existing = {
  name: foundryAccountName
}

resource demoProject 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  parent: foundry
  name: 'volt-demo'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    displayName: 'Volt production-like DEMO'
    description: 'Synthetic internal enablement environment, separate from DEV; not customer production.'
  }
}

resource search 'Microsoft.Search/searchServices@2025-05-01' = {
  name: searchName
  location: location
  tags: tags
  sku: {
    name: 'basic'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
    disableLocalAuth: true
    semanticSearch: 'free'
  }
}

resource workspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = {
  name: workspaceName
}

resource insights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-volt-tools-261111'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: workspace.id
    DisableLocalAuth: true
  }
}

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'stvolttools261111'
  location: location
  tags: tags
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    publicNetworkAccess: 'Disabled'
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: 'Deny'
    }
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
  resource blobs 'blobServices' = {
    name: 'default'
    resource packages 'containers' = {
      name: 'function-packages'
      properties: {
        publicAccess: 'None'
      }
    }
  }
}

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-volt-tools'
  location: location
  tags: tags
}

resource toolsNetwork 'Microsoft.Network/virtualNetworks@2023-05-01' = {
  name: 'vnet-volt-tools'
  location: location
  tags: tags
  properties: {
    addressSpace: {
      addressPrefixes: ['10.172.0.0/24']
    }
    subnets: [
      {
        name: 'functions'
        properties: {
          addressPrefix: '10.172.0.0/26'
          delegations: [{
            name: 'flex-consumption'
            properties: {
              serviceName: 'Microsoft.App/environments'
            }
          }]
        }
      }
      {
        name: 'private-endpoints'
        properties: {
          addressPrefix: '10.172.0.64/26'
          privateEndpointNetworkPolicies: 'Disabled'
        }
      }
    ]
  }
  resource integration 'subnets' existing = {
    name: 'functions'
  }
  resource endpoints 'subnets' existing = {
    name: 'private-endpoints'
  }
}

var storageServices = ['blob', 'queue', 'table']
resource storageZones 'Microsoft.Network/privateDnsZones@2020-06-01' existing = [for service in storageServices: {
  name: 'privatelink.${service}.core.windows.net'
}]
resource dnsLinks 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = [for (service, i) in storageServices: {
  parent: storageZones[i]
  name: 'volt-tools-link'
  location: 'global'
  properties: {
    virtualNetwork: {
      id: toolsNetwork.id
    }
    registrationEnabled: false
  }
}]
@batchSize(1)
resource storageEndpoints 'Microsoft.Network/privateEndpoints@2023-05-01' = [for service in storageServices: {
  name: 'pe-volt-tools-${service}'
  location: location
  tags: tags
  properties: {
    subnet: {
      id: toolsNetwork::endpoints.id
    }
    privateLinkServiceConnections: [{
      name: 'volt-tools-${service}'
      properties: {
        privateLinkServiceId: storage.id
        groupIds: [service]
      }
    }]
  }
  dependsOn: [
    toolsNetwork
  ]
}]
resource endpointDns 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-05-01' = [for (service, i) in storageServices: {
  parent: storageEndpoints[i]
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [{
      name: 'storage'
      properties: {
        privateDnsZoneId: storageZones[i].id
      }
    }]
  }
}]

var storageRoles = [
  'b7e6dc6d-f1e8-4753-8033-0f276bb0955b'
  '974c5e8b-45b9-4653-ba55-5f855dd0fb88'
  '0a9a7e1f-b9d0-4cc4-a60d-0319b160aaa3'
]

resource storageAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for role in storageRoles: {
  name: guid(storage.id, identity.id, role)
  scope: storage
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', role)
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}]

resource monitoringAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(insights.id, identity.id, 'metrics')
  scope: insights
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '3913510d-42f4-4e42-8a64-420c390055eb')
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource plan 'Microsoft.Web/serverfarms@2024-04-01' = {
  name: 'plan-volt-tools'
  location: location
  tags: tags
  kind: 'functionapp'
  sku: {
    tier: 'FlexConsumption'
    name: 'FC1'
  }
  properties: {
    reserved: true
  }
}

resource tools 'Microsoft.Web/sites@2024-04-01' = {
  name: toolsAppName
  location: location
  tags: tags
  kind: 'functionapp,linux'
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identity.id}': {}
    }
  }
  properties: {
    serverFarmId: plan.id
    virtualNetworkSubnetId: toolsNetwork::integration.id
    httpsOnly: true
    siteConfig: {
      minTlsVersion: '1.2'
      appSettings: [
        { name: 'AzureWebJobsStorage__accountName', value: storage.name }
        { name: 'AzureWebJobsStorage__credential', value: 'managedidentity' }
        { name: 'AzureWebJobsStorage__clientId', value: identity.properties.clientId }
        { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: insights.properties.ConnectionString }
        { name: 'APPLICATIONINSIGHTS_AUTHENTICATION_STRING', value: 'ClientId=${identity.properties.clientId};Authorization=AAD' }
      ]
    }
    functionAppConfig: {
      deployment: {
        storage: {
          type: 'blobContainer'
          value: '${storage.properties.primaryEndpoints.blob}${storage::blobs::packages.name}'
          authentication: {
            type: 'UserAssignedIdentity'
            userAssignedIdentityResourceId: identity.id
          }
        }
      }
      scaleAndConcurrency: {
        maximumInstanceCount: 40
        instanceMemoryMB: 2048
      }
      runtime: {
        name: 'python'
        version: '3.12'
      }
    }
  }
  dependsOn: [
    storageAccess
    endpointDns
    dnsLinks
  ]
}

output functionAppName string = tools.name
output toolsEndpoint string = 'https://${tools.properties.defaultHostName}/api'
output searchResourceId string = search.id
output demoProjectId string = demoProject.id
