### portalConfig.tree {data-toc-label='Tree'}
Possibility to make settings for the topic selection tree. The layers are rendered in reverse configuration order.

| Name                         | Required | Type                                                            | Default                                                      | Description                                                                                                                                                                                                                                                                                               | Expert |
| ---------------------------- | -------- | --------------------------------------------------------------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| addLayerButton               | no       | **[addLayerButton](#portalconfigtreeaddlayerbutton)**           | false                                                        | If active:true, a button for adding layers will be displayed. Initially only visible layers and layers with the property `showInLayerTree = true` are shown in the topic tree. If false, then all configured layers are shown in the topic tree. With the tree.type `auto` an add button is always shown. | false  |
| categories                   | no       | **[categories](#portalconfigtreecategories)**                   |                                                              | Configuration of the categories from the metadata. Only for the tree.type `auto`.                                                                                                                                                                                                                         | false  |
| highlightedFeatures          | no       | **[highlightedFeatures](#portalconfigtreehighlightedfeatures)** |                                                              | Configuration in addition to highlighting features.                                                                                                                                                                                                                                                       | false  |
| layerIDsToIgnore             | no       | String[]                                                        |                                                              | List of `services.json` layer ids that should not be displayed in the tree and map. Only for the tree.type `auto`.                                                                                                                                                                                        | false  |
| layerIDsToStyle              | no       | **[layerIDsToStyle](#portalconfigtreelayeridstostyle)**[]       |                                                              | Special implementation for a HVV service (Hamburger Verkehrsbetriebe). Contains objects to query different styles of a layer ID.                                                                                                                                                                          | true   |
| metaIDsToIgnore              | no       | String[]                                                        |                                                              | All layers found in `services.json` that match these meta IDs will not be displayed in the tree and map. Only for the tree.type `auto`.                                                                                                                                                                   | false  |
| metaIDsToMerge               | no       | String[]                                                        |                                                              | All layers found in `services.json` that match these meta-IDs will be merged into a single layer in the tree. Only for the tree.type `auto`.                                                                                                                                                              | true   |
| rasterLayerDefaultInfoFormat | no       | String                                                          | "`text/xml`"                                                 | InfoFormat for Raster-Layer if not specified in layer configuration.                                                                                                                                                                                                                                      | false  |
| showFolderPath               | no       | Boolean                                                         | false                                                        | Determines whether the folder structure of visible layers is displayed in 'Show more functions'.                                                                                                                                                                                                          | false  |
| singleBaselayer              | no       | Boolean                                                         | false                                                        | Specifies whether only one base layer may be active at any time.                                                                                                                                                                                                                                          | false  |
| type                         | no       | enum["auto"]                                                    |                                                              | The topic tree is built in the same structure as the **[topicconfig](#layerconfig)**. If the type `auto` is configured, all layers from the [services.json](../Global-Config/services.json.md) are offered in the tree, structured by their metadata (Geoportal-Hamburg).                                 | false  |
| validLayerTypesAutoTree      | no       | enum                                                            | ["WMS", "SENSORTHINGS", "TERRAIN3D", "TILESET3D", "OBLIQUE"] | Layer types to be used with the tree.type `auto`.                                                                                                                                                                                                                                                         | false  |
| hideBackgroundsHeader        | no       | Boolean                                                         | false                                                        | Set to true to hide the backgrounds headline.                                                                                                                                                                                                                                                             | false  |
| backgroundsHeaderText        | no       | String                                                          |                                                              | Alternativ backgrounds headline. If set, a none empty string is required. An empty string will output the default i18n string/translation.                                                                                                                                                                | false  |
| hideDatalayerHeader          | no       | Boolean                                                         | false                                                        | Set to true to hide the datalayer headline.                                                                                                                                                                                                                                                               | false  |
| datalayerHeaderText          | no       | String                                                          |                                                              | Alternativ datalayer headline. If set, a none empty string is required. An empty string will output the default i18n string/ translation.                                                                                                                                                                 | false  |
| subMenuContactButton         | no       | Boolean                                                         | true                                                         | Defines if the button to open the contact form with layer specific parameters is shown                                                                                                                                                                                                                    | false  |
| allowBaselayerDrag           | no       | Boolean                                                         | true                                                         | Determines whether base layers can be moved over data layers.                                                                                                                                                                                                                                             | false  |
| contactPublisherName         | no       | Boolean                                                         | false                                                        | If enabled and a publisher is available, the contact message will display the publisher's name instead of the layer name.                                                                                                                                                                                 | false  |

**Example type auto**

```json
{
    "tree": {
        "type": "auto",
        "validLayerTypesAutoTree": ["WMS", "WFS"],
        "layerIDsToIgnore": ["1912", "1913"],
        "metaIDsToIgnore": [
            "09DE39AB-A965-45F4-B8F9-0C339A45B154"
        ],
        "metaIDsToMerge": [
            "FE4DAF57-2AF6-434D-85E3-220A20B8C0F1"
        ],
        "layerIDsToStyle": [
            {
                "id": "1935",
                "styles": ["geofox_Faehre", "geofox-bahn", "geofox-bus", "geofox_BusName"],
                "name": ["Fährverbindungen", "Bahnlinien", "Buslinien", "Busliniennummern"],
                "legendURL": ["http://geoportal.metropolregion.hamburg.de/legende_mrh/hvv-faehre.png", "http://geoportal.metropolregion.hamburg.de/legende_mrh/hvv-bahn.png", "http://geoportal.metropolregion.hamburg.de/legende_mrh/hvv-bus.png", "http://87.106.16.168/legende_mrh/hvv-bus.png"]
            }
        ],
        "categories": [
        {
          "key": "kategorie_opendata",
          "name": "common:modules.layerTree.categoryOpendata",
          "active": true
        },
        {
          "key": "kategorie_inspire",
          "name": "common:modules.layerTree.categoryInspire"
        },
        {
          "key": "kategorie_organisation",
          "name": "common:modules.layerTree.categoryOrganisation"
        }
      ],
        "hideBackgroundsHeader": true,
        "backgroundsHeaderText": "This should not appear on output",
        "hideDatalayerHeader": false,
        "datalayerHeaderText": "Specific heading for datalayers across all languages - overwrites i18n"
    }
}
```

**Example no type**

```json
{
    "tree": {
        "addLayerButton": {
            "active": true
        },
        "highlightedFeatures": {
            "active": false
        },
    }
}
```

***

#### portalConfig.tree.addLayerButton {data-toc-label='Add Layer Button'}
Configuration of the addLayerButton to select layers.

| Name                      | Required | Type                                                              | Default | Description                                                                                                                                                                                                                                              | Expert |
| ------------------------- | -------- | ----------------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| active                    | yes      | Boolean                                                           |         | Controls if addLayerButton is shown or not.                                                                                                                                                                                                              | false  |
| searchBar                 | no       | **[searchBar](#portalconfigtreeaddlayerbuttonsearchbar)**/Boolean | false   | If active:true then a search within the configured searchInterfaces and searchCategory is possible.                                                                                                                                                      | false  |
| buttonTitle               | no       | String                                                            |         | Sets the button title with customized text.                                                                                                                                                                                                              | false  |
| searchInterfaceInstanceId | no       | String                                                            |         | Deprecated in next major release - use **[searchInterfaceInstances](#portalconfigtreeaddlayerbuttonsearchbarsearchinterfaceinstances) []** instead. Id of the search interface. Configured on the search interface at the parameter 'searchInterfaceId'. | true   |
| searchCategory            | no       | String                                                            |         | Deprecated in next major release - use **[searchInterfaceInstances](#portalconfigtreeaddlayerbuttonsearchbarsearchinterfaceinstances) []** instead. The category of the search.                                                                          | true   |

**Example**

```json
{
    "tree": {
        "addLayerButton": {
            "active": true,
            "buttonTitle": "Add Layers",
            "searchBar": {
                "active": true,
                "searchInterfaceInstances": [
                    {
                        "id":"elasticSearch_0",
                        "searchCategory": "Thema (externe Fachdaten)"
                    },
                    {
                        "id": "topicTree",
                        "searchCategory": "Thema"
                    }
                ]
            }
        }
    }
}
```
```json
{
    "tree": {
        "addLayerButton": {
            "active": true,
            "buttonTitle": "Layer hinzufügen",
            "searchBar": {
                "active": true,
                "searchInterfaceInstanceId": "elasticSearch_0",
                "searchCategory": "Thema (externe Fachdaten)"
            }
        }
    }
}
```

***
#### portalConfig.tree.addLayerButton.searchBar {data-toc-label='Searchbar in Topic Tree'}
A topic search is enabled within the configured SearchInterface and SearchCategory.

| Name                     | Required | Type                                                                                                | Default | Description                                                                                                                                                                                                                                                                            | Expert |
| ------------------------ | -------- | --------------------------------------------------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| active                   | yes      | Boolean                                                                                             |         | Specifies whether the search is displayed.                                                                                                                                                                                                                                             | false  |
| searchInterfaceInstances | ja       | **[searchInterfaceInstances](#portalconfigtreeaddlayerbuttonsearchbarsearchinterfaceinstances) []** |         | List of search interfaces from the searchbar that are to be used here.                                                                                                                                                                                                                 | true   |
| filter                   | no       | Boolean                                                                                             | false   | Enables client-side filtering of layers and folders in the tree based on the user's search input. <br>**Note:** <br>If `searchInterfaceInstances` *is* configured, `filter: true` takes **priority** and triggers local filtering **instead of** using the configured SearchInterface. | false  |

**Example with `searchInterfaceInstances`**

```json
{
  "searchBar": {
    "active": true,
    "searchInterfaceInstances": [
      {
        "id": "elasticSearch_0",
        "searchCategory": "Topic (external data)"
      },
      {
        "id": "topicTree",
        "searchCategory": "Topic"
      }
    ]
  }
}
```
**Example with `filter`**

```json
{
  "searchBar": {
    "active": true,
    "filter": true
  }
}
```

***
#### portalConfig.tree.addLayerButton.searchBar.searchInterfaceInstances {data-toc-label='Searchinterface Instances'}
List of search interfaces from the searchbar that are to be used here.
The search only works with interfaces that perform a topic search.

| Name           | Required | Type   | Default | Description                                                                                | Expert |
| -------------- | -------- | ------ | ------- | ------------------------------------------------------------------------------------------ | ------ |
| id             | yes      | String |         | Id des Suchinterfaces. Konfiguriert an dem Suchinterface am Parameter 'searchInterfaceId'. | false  |
| searchCategory | yes      | String |         | the search category.                                                                       | false  |

**Example**

```json
{
    "searchInterfaceInstances": [
        {
            "id":"elasticSearch_0",
            "searchCategory": "Thema (externe Fachdaten)"
        },
        {
            "id": "topicTree",
            "searchCategory": "Thema"
        }
    ]
}
```

***

#### portalConfig.tree.categories {data-toc-label='Categories'}
Configuration of the categories from the metadata. Only for the tree.type `auto`.

| Name   | Required | Type    | Default | Description                                                                                                  | Expert |
| ------ | -------- | ------- | ------- | ------------------------------------------------------------------------------------------------------------ | ------ |
| key    | yes      | String  |         | Key of the respective category in the metadata.                                                              | false  |
| name   | yes      | String  |         | Name of the categorie.                                                                                       | false  |
| active | no       | Boolean |         | Indicates whether this category is initially active. If not specified, the 1st category is initially active. | false  |

**Example**

```json
 "categories": [
        {
          "key": "categorie_opendata",
          "name": "common:modules.layerTree.categoryOpendata",
          "active": true
        },
        {
          "key": "categorie_inspire",
          "name": "common:modules.layerTree.categoryInspire"
        },
        {
          "key": "categorie_organisation",
          "name": "common:modules.layerTree.categoryOrganisation"
        }
      ]
```

***

#### portalConfig.tree.highlightedFeatures {data-toc-label='Highlighted Features'}
Configuration in addition to highlighting features. If features are highlighted with the "List" or "Select Features" module with "Zoom to this Feature" or via url parameter, then a layer with these features is selectable in the menu tree.

| Name      | Required | Type    | Default                                   | Description                                                                                                                          | Expert |
| --------- | -------- | ------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| active    | no       | Boolean | false                                     | Indicates whether this feature is active.                                                                                            | false  |
| layerName | no       | String  | "common:shared.js.utils.selectedFeatures" | Name of the created layer with the highlighted features. The name additionally contains the name of the module that was worked with. | true   |

**Example**

```json
"highlightedFeatures": {
    "active": false,
    "layerName": "Selected features"
},
```

***

#### portalConfig.tree.layerIDsToStyle {data-toc-label='Layer IDs To Style'}
Special implementation for a HVV service (Hamburger Verkehrsbetriebe). Contains objects to query different styles of a layer ID. Only for the tree.type `auto`.

| Name      | Required | Type            | Default | Description                                                                                                        | Expert |
| --------- | -------- | --------------- | ------- | ------------------------------------------------------------------------------------------------------------------ | ------ |
| id        | no       | String          |         | A `services.json` layer's id.                                                                                      | false  |
| styles    | no       | String/String[] |         | Style to use as a string; if multiple styles are to be used, they are listed in an array.                          | false  |
| name      | no       | String/String[] |         | Name to use as a string; if multiple names are to be used, they are listed in an array.                            | false  |
| legendUrl | no       | String/String[] |         | URL of the legend image as a string ; if multiple legend images are to be used, their URLs are listed in an array. | false  |

**Example:**

```json
{
    "layerIDsToStyle": [
        {
            "id": "1935",
            "styles": ["geofox_Faehre", "geofox-bahn", "geofox-bus", "geofox_BusName"],
            "name": ["Fährverbindungen", "Bahnlinien", "Buslinien", "Busliniennummern"],
            "legendURL": ["http://geoportal.metropolregion.hamburg.de/legende_mrh/hvv-faehre.png", "http://geoportal.metropolregion.hamburg.de/legende_mrh/hvv-bahn.png", "http://geoportal.metropolregion.hamburg.de/legende_mrh/hvv-bus.png", "http://87.106.16.168/legende_mrh/hvv-bus.png"]
        }
    ]
}
```

***
