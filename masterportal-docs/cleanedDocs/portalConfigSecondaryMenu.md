### portalConfig.secondaryMenu {data-toc-label='Menu'}
Here you can configure the menu items for the `secondaryMenu` (in the desktop view on the right). The order of the modules results from the order in the *Config.json*. 

```json
{
    "portalConfig": {
        "mainMenu": {},
        "map": {},
        "portalFooter": {},
        "secondaryMenu": {
            "expanded": false,
            "sections": [
                [
                    {
                        "type": ""
                    }
                ]
            ]
        },
        "tree": {}
    }
}
```



| Name             | Required | Type                                        | Default | Description                                                                                                                                                                                                                                             | Expert |
| ---------------- | -------- | ------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| currentComponent | no       | String                                      | ""      | Defines a module that is opened initially. Please mind that modules nested in folders can not be opened this way. If a module is present multiple times, all instances will be opened in order of appearence, which may result in unexpected behaviour. | false  |
| expanded         | no       | Boolean                                     | false   | Defines whether the respective menu is expanded or collapsed when the portal is started.                                                                                                                                                                | false  |
| width            | no       | String                                      | "25%"   | Sets the initial width of the respective menu as a percentage value.                                                                                                                                                                                    | false  |
| showDescription  | no       | Boolean                                     |         | Defines whether a description of the modules should be displayed in the respective menu.                                                                                                                                                                | false  |
| showHeaderIcon   | no       | Boolean                                     | false   | Defines whether the icon of the current module is shown in the menu header                                                                                                                                                                              | false  |
| searchBar        | no       | **[searchBar](#portalconfigmenusearchbar)** |         | The search bar allows requesting information from various search services at once.                                                                                                                                                                      | false  |
| sections         | no       | **[sections](#portalconfigmenusections)**[] |         | Subdivision of modules in the menu.                                                                                                                                                                                                                     | false  |
| title            | no       | **[title](#portalconfigmenutitle)**         |         | The portal's title and further elements to be shown in the main menu bar.                                                                                                                                                                               | false  |

***

#### portalConfig.secondaryMenu.searchBar {data-toc-label='Search Bar'}
Configuration of the search bar. Different search services can be configured.

| Name                  | Required | Type                                                                         | Default                                        | Description                                                                   | Expert |
| --------------------- | -------- | ---------------------------------------------------------------------------- | ---------------------------------------------- | ----------------------------------------------------------------------------- | ------ |
| minCharacters         | no       | Integer                                                                      | 3                                              | Minimum amount of characters before sending a request to an external service. | false  |
| placeholder           | no       | String                                                                       | "common:modules.searchBar.placeholder.address" | Input text field placeholder shown when no input has been given yet.          | false  |
| coloredHighlighting3D | no       | **[coloredHighlighting3D](#portalconfigmenusearchbarcoloredhighlighting3d)** | ""                                             | Configures the color for 3D tile highlighting in a Cesium 3D scene.           | false  |
| searchInterfaces      | no       | **[searchInterfaces](#portalconfigmenusearchbarsearchinterfaces)**[]         |                                                | Interfaces to search services.                                                | false  |
| timeout               | no       | Integer                                                                      | 5000                                           | Service request timeout in milliseconds.                                      | false  |
| zoomLevel             | no       | Integer                                                                      | 7                                              | ZoomLevel to which the searchbar zooms in at maximum.                         | false  |

**Example**

```json
{
    "searchBar": {
        "minCharacters": 3,
        "placeholder": "common:modules.searchBar.placeholder.address",
        "searchInterfaces": [
            {
                "type": "gazetteer",
                "serviceId": "6",
                "searchAddress": true,
                "searchStreets": true,
                "searchHouseNumbers": true,
                "searchDistricts": true,
                "searchParcels": true,
                "searchStreetKey": true
            }
        ],
        "timeout": 5000,
        "zoomLevel": 7
    }
}
```

***

##### portalConfig.secondaryMenu.searchBar.coloredHighlighting3D {data-toc-label='Colored Highlighting 3D'}
Enables and configures the 3D highlighting feature for tiles in a Cesium 3D scene. This allows selected features to be visually emphasized by changing their color.

| Name  | Required | Type            | Default | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Expert |
| ----- | -------- | --------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| color | no       | String/String[] | "RED"   | The highlight color for the 3D tile feature. This can be set using: <br> 1. **String** (e.g., "YELLOW", "BLUE") – A predefined Cesium color.<br> (e.g., `"rgba(0, 255, 255, 1)"`) – A standard RGBA color format, where the alpha value is between `0` (fully transparent) and `1` (fully opaque). <br> (e.g., `"rgb(0, 255, 255)"`) – A standard RGB color format. <br> (e.g., `"#FF0000"`) – A standard hex color format. <br> 2. **Array (RGBA)** – An array of four values `[R, G, B, A]`. <br> 3. **Array (RGB)** – An array of three values `[R, G, B]`. <br> **Important**: For RGBA values, **alpha (A)** must be between `0` (fully transparent) and `255` (fully opaque). Example: `[255, 255, 0, 0]` for yellow with full feature transparency, `[255, 255, 0, 255]` for yellow with full feature opacity. | false  |

The Vuex action `highlight3DTileByCoordinates` will:

1. Check if the current map mode is `3D`.
2. Convert the given longitude and latitude into Cartesian coordinates.
3. Project the coordinates onto the screen.
4. Retrieve the configured highlight color from `config.json`.
5. If a feature is picked at the screen position, apply the highlight color.
6. If no feature is initially found, wait for all tiles to load before attempting to highlight again.

- If the feature at the given coordinates is found, it will be highlighted with the specified color.
- If an invalid color is provided, a warning will be displayed in the console.
- If all 3D tiles are not yet loaded, highlighting will be delayed until loading is complete.

**Example**

```json
{
    "searchBar": {
        "minCharacters": 3,
        "placeholder": "common:modules.searchBar.placeholder.address",
        "coloredHighlighting3D":{
          "color": "YELLOW"
        }
    }
}
```

***

##### portalConfig.secondaryMenu.searchBar.searchInterfaces {data-toc-label='Search Interfaces'}
Definitions of the search interfaces.

| Name           | Required | Type                                                                           | Default | Description                                       | Expert |
| -------------- | -------- | ------------------------------------------------------------------------------ | ------- | ------------------------------------------------- | ------ |
| bkg            | no       | **[bkg](#portalconfigmenusearchbarsearchinterfacesbkg)**                       |         | BKG search service configuration.                 | false  |
| elasticSearch  | no       | **[elasticSearch](#portalconfigmenusearchbarsearchinterfaceselasticsearch)**   |         | Elastic search service configuration.             | false  |
| gazetteer      | no       | **[gazetteer](#portalconfigmenusearchbarsearchinterfacesgazetteer)**           |         | Configuration of the Gazetteer search service.    | false  |
| komootPhoton   | no       | **[komootPhoton](#portalconfigmenusearchbarsearchinterfaceskomootphoton)**     |         | Komoot Photon search service configuration.       | false  |
| locationFinder | no       | **[locationFinder](#portalconfigmenusearchbarsearchinterfaceslocationfinder)** |         | LocationFinder search service configuration.      | false  |
| osmNominatim   | no       | **[osmNominatim](#portalconfigmenusearchbarsearchinterfacesosmnominatim)**     |         | OpenStreetMap (OSM) search service configuration. | false  |
| specialWFS     | no       | **[specialWFS](#portalconfigmenusearchbarsearchinterfacesspecialwfs)**         |         | specialWFS search service configuration.          | false  |
| topicTree      | no       | **[topicTree](#portalconfigmenusearchbarsearchinterfacestopictree)**           |         | Topic selection tree search configuration.        | false  |
| visibleVector  | no       | **[visibleVector](#portalconfigmenusearchbarsearchinterfacesvisiblevector)**   |         | Visible vector layer search configuration.        | false  |

**Example**

```json
"searchInterfaces": [
    {
        "type": "gazetteer",
        "serviceId": "6",
        "searchAddress": true,
        "searchStreets": true,
        "searchHouseNumbers": true,
        "searchDistricts": true,
        "searchParcels": true,
        "searchStreetKey": true
    }
]
```

***

###### portalConfig.secondaryMenu.searchBar.searchInterfaces.bkg {data-toc-label='BKG'}

[type:Extent]: # (Datatypes.Extent)
[type:resultEvents]: # (portalConfig.secondaryMenu.searchBar.searchInterfaces.resultEvents)

BKG search service configuration.

**Attention: This requires a backend!**

**To avoid openly using your BKG UUID, URLs ("bkg_geosearch" and "bkg_suggest" in this case) of the restServices should be caught and redirected in a proxy.**

**Example proxy configuration**

```
ProxyPass /bkg_geosearch http://sg.geodatenzentrum.de/gdz_geokodierung__[UUID]/geosearch
<Location /bkg_geosearch>
  ProxyPassReverse http://sg.geodatenzentrum.de/gdz_geokodierung__[UUID]/geosearch
</Location>

ProxyPass /bkg_suggest http://sg.geodatenzentrum.de/gdz_geokodierung__[UUID]/suggest
<Location /bkg_suggest>
  ProxyPassReverse http://sg.geodatenzentrum.de/gdz_geokodierung__[UUID]/suggest
</Location>
```

| Name               | Required | Type                                                                       | Default                                                                                           | Description                                                                                                                                                                                  | Expert |
| ------------------ | -------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| epsg               | no       | String                                                                     | "EPSG:25832"                                                                                      | EPSG code of the coordinate reference system to use.                                                                                                                                         | false  |
| extent             | no       | **[Extent](#datatypesextent)**                                             | [454591, 5809000, 700000, 6075769]                                                                | Coordinate extent in which search algorithms should return.                                                                                                                                  | false  |
| geoSearchServiceId | yes      | String                                                                     |                                                                                                   | Search service id. Resolved using the **[rest-services.json](../Global-Config/rest-services.json.md)** file.                                                                                 | false  |
| minScore           | no       | Number                                                                     | 0.6                                                                                               | Score defining the minimum quality of search results.                                                                                                                                        | false  |
| resultCount        | no       | Integer                                                                    | 20                                                                                                | Maximum number of search hits returned by the service.                                                                                                                                       | false  |
| resultEvents       | no       | **[resultEvents](#portalconfigmenusearchbarsearchinterfacesresultevents)** | {"onClick": ["setMarker", "zoomToResult"], "onHover": ["setMarker"], "buttons": ["startRouting"]} | Actions that are executed when an interaction, such as hover or click, is performed with a result list item. The following events are possible: "setMarker", "zoomToResult", "startRouting". | false  |
| type               | yes      | String                                                                     | "bkg"                                                                                             | Search interface type. Defines which search interface is configured.                                                                                                                         | false  |

**Example**

```json
{
    "geoSearchServiceId": "5",
    "extent": [454591, 5809000, 700000, 6075769],
    "resultCount": 10,
    "epsg": "EPSG:25832",
    "minScore": 0.6,
    "type": "bkg"
}
```

***

###### portalConfig.secondaryMenu.searchBar.searchInterfaces.elasticSearch {data-toc-label='Elastic Search'}

[type:resultEvents]: # (portalConfig.secondaryMenu.searchBar.searchInterfaces.resultEvents)

Elasticsearch service configuration.

| Name                  | Required | Type                                                                        | Default                                                                          | Description                                                                                                                                                                                                                                                                        | Expert |
| --------------------- | -------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| hitIcon               | no       | String                                                                      | "bi-signpost-2"                                                                  | CSS icon class of search results, shown before the result name.                                                                                                                                                                                                                    | false  |
| hitMap                | no       | **[hitMap](#portalconfigmenusearchbarsearchinterfaceselasticsearchhitmap)** |                                                                                  | Object mapping result object attributes to keys.                                                                                                                                                                                                                                   | true   |
| hitTemplate           | no       | String                                                                      | "default"                                                                        | Template in which the search results (`show all`) are displayed. Possible values are "default" and "layer".                                                                                                                                                                        | false  |
| hitType               | no       | String                                                                      | "common:modules.searchbar.type.subject"                                          | Search result type shown in the result list after the result name. Set to the translation key.                                                                                                                                                                                     | false  |
| resultEvents          | no       | **[resultEvents](#portalconfigmenusearchbarsearchinterfacesresultevents)**  | {"onClick": ["addLayerToTopicTree"], "buttons": ["showInTree", "showLayerInfo"]} | Actions that are executed when an interaction, such as hover or click, is performed with a result list item. The following events are possible: "addLayerToTopicTree", "setMarker", "showInTree", "showLayerInfo", "startRouting", "zoomToResult", "highlight3DTileByCoordinates". | false  |
| requestType           | no       | enum["POST", "GET"]                                                         | "POST"                                                                           | Request type                                                                                                                                                                                                                                                                       | false  |
| responseEntryPath     | no       | String                                                                      | ""                                                                               | Response JSON attribute path to found features.                                                                                                                                                                                                                                    | false  |
| searchInterfaceId     | no       | String                                                                      | "elasticSearch"                                                                  | Id, which is used to link to the searchbar in the topic search.                                                                                                                                                                                                                    | false  |
| searchStringAttribute | no       | String                                                                      | "searchString"                                                                   | Search string attribute name for `payload` object.                                                                                                                                                                                                                                 | false  |
| serviceId             | yes      | String                                                                      |                                                                                  | Search service id. Resolved using the **[rest-services.json](../Global-Config/rest-services.json.md)** file.                                                                                                                                                                       | false  |
| type                  | yes      | String                                                                      | "elasticSearch"                                                                  | Search interface type. Defines which search interface is configured.                                                                                                                                                                                                               | false  |

As an additional property, you may add `payload`. It is not required, and matches the custom object description. By default, it is set to the empty object `{}`. The object describes the payload to be sent as part of the request. It must provide the searchString attribute. For more info on usable attributes, see **[Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html)**. This object can not be handled in the Admintool, since custom objects are not yet supported.

 **Example**

```json
{
    "type": "elasticSearch",
    "searchInterfaceId":"elasticSearch_0",
    "serviceId":"elastic",
    "requestType": "GET",
    "payload": {
        "id":"query",
        "params":{
            "query_string":""
        }
    },
    "searchStringAttribute": "query_string",
    "responseEntryPath": "hits.hits",
    "hitMap": {
        "name": "_source.name",
        "id": "_source.id",
        "source": "_source"
    },
    "hitType": "common:modules.searchbar.type.subject",
    "hitIcon": "bi-list-ul"
}
```

***

###### portalConfig.secondaryMenu.searchBar.searchInterfaces.elasticSearch.hitMap {data-toc-label='Hit Map'}
Mapping Objekt. Mappt die Attribute des Ergebnis Objektes auf den entsprechenden Key.

| Name       | Required | Type            | Default  | Description                                                                            | Expert |
| ---------- | -------- | --------------- | -------- | -------------------------------------------------------------------------------------- | ------ |
| coordinate | no       | String/String[] |          | Attribute value will be mapped to the attribute key. Required to display a map marker. | false  |
| id         | yes      | String/String[] | "id"     | Attribute value will be mapped to the attribute key. Required to display results.      | false  |
| layerId    | yes      | String/String[] |          | Attribute value will be mapped to the attribute key. Required to display results.      | false  |
| name       | yes      | String/String[] | "name"   | Attribute value will be mapped to the attribute key. Required to display results.      | false  |
| source     | yes      | String/String[] | "source" | Attribute value will be mapped to the attribute key. Required to display results.      | false  |
| toolTip    | yes      | String/String[] |          | Attribute value will be mapped to the attribute key. Required to display results.      | false  |

**Example**

```json
"hitMap": {
    "name": "_source.name",
    "id": "_source.id",
    "source": "_source",
    "layerId": "_source.id",
    "toolTip": [
        "_source.name",
        "_source.datasets.md_name"
    ]
}
```

***

###### portalConfig.secondaryMenu.searchBar.searchInterfaces.gazetteer {data-toc-label='Gazetteer'}

[type:resultEvents]: # (portalConfig.secondaryMenu.searchBar.searchInterfaces.resultEvents)

Gazetteer search service configuration.

**This requires a backend!**
**A WFS's Stored Query is requested with predefined parameters.**

| Name                     | Required | Type                                                                       | Default                                                                                           | Description                                                                                                                                                                                                                 | Expert |
| ------------------------ | -------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| resultEvents             | no       | **[resultEvents](#portalconfigmenusearchbarsearchinterfacesresultevents)** | {"onClick": ["setMarker", "zoomToResult"], "onHover": ["setMarker"], "buttons": ["startRouting"]} | Actions that are executed when an interaction, such as hover or click, is performed with a result list item. The following events are possible: "setMarker", "zoomToResult","highlight3DTileByCoordinates".                 | false  |
| searchAddress            | no       | Boolean                                                                    | false                                                                                             | Defines whether address search is active. For backward compatibility, if "searchAddress" is not configured, the "searchAddress" attribute is set to "true" when "searchStreets" and "searchHouseNumbers" are set to "true". | false  |
| searchDistricts          | no       | Boolean                                                                    | false                                                                                             | Defines whether district search is active.                                                                                                                                                                                  | false  |
| searchHouseNumbers       | no       | Boolean                                                                    | false                                                                                             | Defines whether house numbers should be searched for. Requires `searchStreets` to be set to `true`, too.                                                                                                                    | false  |
| searchParcels            | no       | Boolean                                                                    | false                                                                                             | Defines whether parcels search is active.                                                                                                                                                                                   | false  |
| searchStreetKey          | no       | Boolean                                                                    | false                                                                                             | Defines whether streets should be searched for by key.                                                                                                                                                                      | false  |
| searchStreets            | no       | Boolean                                                                    | false                                                                                             | Defines whether street search is active. Precondition to set `searchHouseNumbers` to `true`.                                                                                                                                | false  |
| serviceId                | yes      | String                                                                     |                                                                                                   | Search service id. Resolved using the **[rest-services.json](../Global-Config/rest-services.json.md)** file.                                                                                                                | false  |
| showGeographicIdentifier | no       | Boolean                                                                    | false                                                                                             | Specifies whether the attribute `geographicIdentifier` should be used to display the search result.                                                                                                                         | false  |
| type                     | yes      | String                                                                     | "gazetteer"                                                                                       | Search interface type. Defines which search interface is configured.                                                                                                                                                        | false  |

**Example**

```json
{
    "type": "gazetteer",
    "serviceId": "6",
    "searchAddress": true,
    "searchStreets": true,
    "searchHouseNumbers": true,
    "searchDistricts": true,
    "searchParcels": true,
    "searchStreetKey": true
}
```

***

###### portalConfig.secondaryMenu.searchBar.searchInterfaces.komootPhoton {data-toc-label='Komoot Photon'}

[type:resultEvents]: # (portalConfig.secondaryMenu.searchBar.searchInterfaces.resultEvents)

Search by **[Komoot Photon](https://photon.komoot.io/)**.

| Name         | Required | Type                                                                       | Default                                                                                           | Description                                                                                                                                                                                                                  | Expert |
| ------------ | -------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| bbox         | no       | string                                                                     |                                                                                                   | Boundingbox of the search.                                                                                                                                                                                                   | false  |
| lang         | no       | string                                                                     | "de"                                                                                              | Language of the Komoot Search. Effects language specific locationnames (e.g. Countrynames) aus.                                                                                                                              | false  |
| lat          | no       | Number                                                                     |                                                                                                   | Latitude of the center for the search.                                                                                                                                                                                       | false  |
| limit        | no       | Number                                                                     |                                                                                                   | Maximum amount of requested unfiltered results.                                                                                                                                                                              | false  |
| lon          | no       | Number                                                                     |                                                                                                   | Longtitude of the center for the search.                                                                                                                                                                                     | false  |
| osm_tag      | no       | string                                                                     |                                                                                                   | Filtering of OSM Tags (see https://github.com/komoot/photon#filter-results-by-tags-and-values).                                                                                                                              | false  |
| resultEvents | no       | **[resultEvents](#portalconfigmenusearchbarsearchinterfacesresultevents)** | {"onClick": ["setMarker", "zoomToResult"], "onHover": ["setMarker"], "buttons": ["startRouting"]} | Actions that are executed when an interaction, such as hover or click, is performed with a result list item. The following events are possible: "setMarker", "startRouting", "zoomToResult", "highlight3DTileByCoordinates". | false  |
| serviceId    | yes      | String                                                                     |                                                                                                   | Komoot search service id. Resolved using the **[rest-services.json](../Global-Config/rest-services.json.md)** file.                                                                                                          | false  |
| type         | yes      | String                                                                     | "komootPhoton"                                                                                    | Search interface type. Defines which search interface is configured.                                                                                                                                                         | false  |

**Example**

```json
{
    "type": "komootPhoton",
    "serviceId": "10",
    "limit": 20,
    "lang": "de",
    "lat": 52.5,
    "lon": 13.4,
    "bbox": "12.5,52.05,14.05,52.75"
}
```

***

###### portalConfig.secondaryMenu.searchBar.searchInterfaces.locationFinder {data-toc-label='Location Finder'}

[type:resultEvents]: # (portalConfig.secondaryMenu.searchBar.searchInterfaces.resultEvents)

Configuration of the search by usage of an ESRI CH LocationFinder.

| Name         | Required | Type                                                                                                   | Default                                                                                           | Description                                                                                                                                                                                  | Expert |
| ------------ | -------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| classes      | no       | **[LocationFinderClass](#portalconfigmenusearchbarsearchinterfaceslocationfinderlocationfinderclass)** |                                                                                                   | May contain classes (with properties) to use in searches. If nothing is specified, all classes are considered valid.                                                                         | false  |
| epsg         | no       | String                                                                                                 |                                                                                                   | Coordinate reference system (EPSG-Code) to use for requests. By default, the value in `portalConfig.mapView.epsg` is used.                                                                   | false  |
| resultEvents | no       | **[resultEvents](#portalconfigmenusearchbarsearchinterfacesresultevents)**                             | {"onClick": ["setMarker", "zoomToResult"], "onHover": ["setMarker"], "buttons": ["startRouting"]} | Actions that are executed when an interaction, such as hover or click, is performed with a result list item. The following events are possible: "setMarker", "startRouting", "zoomToResult". | false  |
| serviceId    | yes      | String                                                                                                 |                                                                                                   | Service id. Resolved using the **[rest-services.json](../Global-Config/rest-services.json.md)** file.                                                                                        | false  |
| type         | yes      | String                                                                                                 | "locationFinder"                                                                                  | Search interface type. Defines which search interface is configured.                                                                                                                         | false  |

**Example**

```json
{
    "type": "locationFinder",
    "serviceId": "locationFinder",
    "classes": [
        {
            "name": "Haltestelle",
            "icon": "bi-record-circle"
        },
        {
            "name": "Straßenname"
        }
    ]
}
```

***

###### portalConfig.secondaryMenu.searchBar.searchInterfaces.locationFinder.LocationFinderClass {data-toc-label='Location Finder Class'}
Definition of classes that should be considered with the results.

| Name | Required | Type   | Default         | Description                                                                                                                                                                                                                                                                  | Expert |
| ---- | -------- | ------ | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| icon | no       | String | "bi-signpost-2" | Class visualization by a icon                                                                                                                                                                                                                                                | false  |
| name | yes      | String |                 | Class name                                                                                                                                                                                                                                                                   | false  |
| zoom | no       | String | "center"        | Defines how to zoom to a hit on selection. If `center` is chosen, the center coordinate (`cx`, `cy`) is zoomed to and a marker is placed. If `bbox` is chosen, the LocationFinder's given BoundingBox (`xmin`, `ymin`, `xmax`, `ymax`) is zoomed to, and no marker is shown. | false  |

**Example**

```json
{
    "type": "locationFinder",
    "serviceId": "10",
    "classes": [
        {
            "name": "Haltestelle",
            "icon": "bi-record-circle"
        },
        {
            "name": "Adresse",
            "icon": "bi-house-door-fill"
        },
        {
            "name": "Straßenname",
            "zoom": "bbox"
        }
    ]
}
```

***

###### portalConfig.secondaryMenu.searchBar.searchInterfaces.osmNominatim {data-toc-label='OSM Nominatim'}

[type:resultEvents]: # (portalConfig.secondaryMenu.searchBar.searchInterfaces.resultEvents)

OpenStreetMap search for city, street, and house number. Only executed on clicking the search icon or pressing enter since the amount of requests to the OSM search service is limited.

| Name         | Required | Type                                                                       | Default                                                                                           | Description                                                                                                                                                                                                                   | Expert |
| ------------ | -------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| classes      | no       | String                                                                     | []                                                                                                | May contain the classes to search for.                                                                                                                                                                                        | false  |
| limit        | no       | Number                                                                     | 50                                                                                                | Maximum amount of requested unfiltered results.                                                                                                                                                                               | false  |
| resultEvents | no       | **[resultEvents](#portalconfigmenusearchbarsearchinterfacesresultevents)** | {"onClick": ["setMarker", "zoomToResult"], "onHover": ["setMarker"], "buttons": ["startRouting"]} | Actions that are executed when an interaction, such as hover or click, is performed with a result list item. The following events are possible: "setMarker", "startRouting", "zoomToResult", "highlight3DTileByCoordinates".  | false  |
| serviceId    | yes      | String                                                                     |                                                                                                   | OSM search service id. Resolved using the **[rest-services.json](../Global-Config/rest-services.json.md)** file.                                                                                                              | false  |
| states       | no       | string                                                                     | ""                                                                                                | May contain federal state names with arbitrary separators. Names may also be used in English depending on whether the data has been added to the free open source project **[OpenStreetMap](https://www.openstreetmap.org)**. | false  |
| type         | yes      | String                                                                     | "osmNominatim"                                                                                    | Search interface type. Defines which search interface is configured.                                                                                                                                                          | false  |

**Example**

```json
{
    "type": "osmNominatim",
    "serviceId": "10",
    "limit": 60,
    "states": "Hamburg, Nordrhein-Westfalen, Niedersachsen, Rhineland-Palatinate Rheinland-Pfalz",
    "classes": "place,highway,building,shop,historic,leisure,city,county"
}
```

***

###### portalConfig.secondaryMenu.searchBar.searchInterfaces.specialWFS {data-toc-label='Special WFS'}

[type:resultEvents]: # (portalConfig.secondaryMenu.searchBar.searchInterfaces.resultEvents)

WFS search function configuration. Requests features from a WFS. The service must be configured to allow WFS 2.0 requests.

For example, on entering "Kronenmatten" the service
https://geoportal.freiburg.de/geoportal_freiburg_de/wfs/stpla_bplan/wfs_mapfile/geltungsbereiche
will be requested with the following XML attached as payload, and the service will answer with an XML FeatureCollection. The collection features will then be offered as search results.

```xml
<?xml version='1.0' encoding='UTF-8'?>
<wfs:GetFeature service='WFS' xmlns:wfs='http://www.opengis.net/wfs' xmlns:ogc='http://www.opengis.net/ogc' xmlns:gml='http://www.opengis.net/gml' traverseXlinkDepth='*' version='1.1.0'>
    <wfs:Query typeName='ms:geltungsbereiche'>
        <wfs:PropertyName>ms:planbez</wfs:PropertyName>
        <wfs:PropertyName>ms:msGeometry</wfs:PropertyName>
        <wfs:maxFeatures>20</wfs:maxFeatures>
        <ogc:Filter>
            <ogc:PropertyIsLike matchCase='false' wildCard='*' singleChar='#' escapeChar='!'>
                <ogc:PropertyName>ms:planbez</ogc:PropertyName>
                <ogc:Literal>*Kronenmatten*</ogc:Literal>
            </ogc:PropertyIsLike>
        </ogc:Filter>
    </wfs:Query>
</wfs:GetFeature>
```

The WFS 2.0 query is dynamically created by the Masterportal. No stored query configuration is required in the service.

| Name         | Required | Type                                                                                 | Default                                                                                                                | Description                                                                                                                                                                                                                    | Expert |
| ------------ | -------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| definitions  | no       | **[definition](#portalconfigmenusearchbarsearchinterfacesspecialwfsdefinition)** *[] |                                                                                                                        | Special WFS search definitions.                                                                                                                                                                                                | false  |
| geometryName | no       | String                                                                               | "app:geom"                                                                                                             | Geometry attribute name required for zoom functionality. Overwritable by a **[definition](#portalconfigmenusearchbarsearchinterfacesspecialwfsdefinition)**.                                                                   | false  |
| icon         | no       | String                                                                               | "bi-house-fill"                                                                                                        | Default icon used in the suggestion list. Overwritable by a **[definition](#portalconfigmenusearchbarsearchinterfacesspecialwfsdefinition)**.                                                                                  | false  |
| maxFeatures  | no       | Integer                                                                              | 20                                                                                                                     | Maximum amount of features to be returned. Overwritable by a **[definition](#portalconfigmenusearchbarsearchinterfacesspecialwfsdefinition)**.                                                                                 | false  |
| namespaces   | no       | String                                                                               | "xmlns:wfs='http://www.opengis.net/wfs' xmlns:ogc='http://www.opengis.net/ogc' xmlns:gml='http://www.opengis.net/gml'" | XML name spaces to request `propertyNames` or `geometryName`. (`xmlns:wfs`, `xmlns:ogc`, and `xmlns:gml` are always used.) Overwritable by a **[definition](#portalconfigmenusearchbarsearchinterfacesspecialwfsdefinition)**. | false  |
| resultEvents | no       | **[resultEvents](#portalconfigmenusearchbarsearchinterfacesresultevents)**           | {"onClick": ["highlightFeature", "setMarker", "zoomToResult"], "onHover": ["highlightFeature", "setMarker"]}           | Actions that are executed when an interaction, such as hover or click, is performed with a result list item. The following events are possible: "highlightFeature", "setMarker", "zoomToResult".                               | false  |
| type         | yes      | String                                                                               | "specialWFS"                                                                                                           | Search interface type. Defines which search interface is configured.                                                                                                                                                           | false  |

**Example**

```json
{
    "type": "specialWfs",
    "definitions": [
        {
            "url": "https://geodienste.hamburg.de/MRH_WFS_Rotenburg",
            "typeName": "app:mrh_row_bplan",
            "propertyNames": ["app:name"],
            "name": "B-Plan",
            "namespaces": "xmlns:app='http://www.deegree.org/app'"
        },
        {
            "url": "/geodienste.hamburg.de/HH_WFS_Bebauungsplaene",
            "typeName": "app:prosin_imverfahren",
            "propertyNames": ["app:plan"],
            "geometryName": "app:the_geom",
            "name": "im Verfahren",
            "namespaces": "xmlns:app='http://www.deegree.org/app'"
        }
    ]
}
```

***

###### portalConfig.secondaryMenu.searchBar.searchInterfaces.specialWFS.definition {data-toc-label='Definition'}
Configuration of definition of the SpecialWFS search.

| Name          | Required | Type     | Default         | Description                                                                                                                | Expert |
| ------------- | -------- | -------- | --------------- | -------------------------------------------------------------------------------------------------------------------------- | ------ |
| geometryName  | no       | String   | "app:geom"      | Geometry attribute name required for zoom functionality.                                                                   | false  |
| icon          | no       | String   | "bi-house-fill" | CSS icon class of search results, shown before the result name.                                                            | false  |
| maxFeatures   | no       | Integer  | 20              | Maximum amount of features to be returned.                                                                                 | false  |
| name          | no       | String   |                 | Category name displayed in the suggestion list.                                                                            | false  |
| namespaces    | no       | String   |                 | XML name spaces to request `propertyNames` or `geometryName`. (`xmlns:wfs`, `xmlns:ogc`, and `xmlns:gml` are always used.) | false  |
| propertyNames | no       | String[] |                 | Array of attribute names to be searched.                                                                                   | false  |
| typeName      | no       | String   |                 | The name of the WFS layer to be requested.                                                                                 | false  |
| url           | no       | String   |                 | WFS URL. Depending on your proxy configuration, the relative URL from the portal server must be given.                     | false  |

**Example**

```json
{
    "url": "https://geodienste.hamburg.de/HH_WFS_Bebauungsplaene",
    "typeName": "app:prosin_imverfahren",
    "propertyNames": ["app:plan"],
    "geometryName": "app:the_geom",
    "name": "im Verfahren"
}
```

***

###### portalConfig.secondaryMenu.searchBar.searchInterfaces.topicTree {data-toc-label='Topic Tree'}

[type:resultEvents]: # (portalConfig.secondaryMenu.searchBar.searchInterfaces.resultEvents)

Searching all topic selection tree layers.

| Name              | Required | Type                                                                       | Default                                                                               | Description                                                                                                                                                                                                | Expert |
| ----------------- | -------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| hitTemplate       | no       | String                                                                     | "default"                                                                             | Template in which the search results (`show all`) are displayed. Possible values are "default" and "layer".                                                                                                | false  |
| resultEvents      | no       | **[resultEvents](#portalconfigmenusearchbarsearchinterfacesresultevents)** | {"onClick": ["activateLayerInTopicTree"], "buttons": ["showInTree", "showLayerInfo"]} | Actions that are executed when an interaction, such as hover or click, is performed with a result list item. The following events are possible: "activateLayerInTopicTree", "showInTree", "showLayerInfo". | false  |
| searchInterfaceId | no       | String                                                                     | "topicTree"                                                                           | Id, which is used to link to the searchbar in the topic search.                                                                                                                                            | false  |
| searchType        | no       | String                                                                     | ""                                                                                    | Decides whether the metadata or the name of a layer should be searched. Possible value: "metadata". The default value is unset so the name will be searched.                                               | false  |
| toolTip           | no       | String                                                                     | ""                                                                                    | If `path` is specified here, the path to the topic/folder found is displayed in the tooltip of the search hit. The name is displayed by default.                                                           | false  |
| type              | yes      | String                                                                     | "topicTree"                                                                           | Search interface type. Defines which search interface is configured.                                                                                                                                       | false  |

**Example**

```json
{
    "type": "topicTree",
    "searchInterfaceId": "topicTree"
}
```

***

###### portalConfig.secondaryMenu.searchBar.searchInterfaces.visibleVector {data-toc-label='Visible Vector'}

[type:resultEvents]: # (portalConfig.secondaryMenu.searchBar.searchInterfaces.resultEvents)

Visible vector layer search configuration. For all vector layers supposed to be searchable, set the **[searchField](#layerconfigelementslayersvector)** attribute in the layer definition object "Fachdaten".

| Name         | Required | Type                                                                       | Default                                                                                    | Description                                                                                                                                                                                        | Expert |
| ------------ | -------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| resultEvents | no       | **[resultEvents](#portalconfigmenusearchbarsearchinterfacesresultevents)** | {"onClick": ["openGetFeatureInfo", "setMarker", "zoomToResult"], "onHover": ["setMarker"]} | Actions that are executed when an interaction, such as hover or click, is performed with a result list item. The following events are possible: "openGetFeatureInfo", "setMarker", "zoomToResult". | false  |
| type         | yes      | String                                                                     | "visibleVector"                                                                            | Search interface type. Defines which search interface is configured.                                                                                                                               | false  |

**Example**

```json
{
    "type": "visibleVector"
}
```

***

###### portalConfig.secondaryMenu.searchBar.searchInterfaces.resultEvents {data-toc-label='Result Events'}
Actions that are executed when an interaction, such as hover or click, is performed with a result list item.

The following events exist. Which events can be configured can be found in the descriptions of the respective search interface:

- activateLayerInTopicTree: Activates the found layer in the topic tree and map.
- addLayerToTopicTree: Adds the found layer to the topic tree and map.
- highligtFeature: Highlights the search result on the map.
- openGetFeatureInfo: Opens the GetFeatureInfo for the search hit in the menu.
- showInTree: Opens the topic selection and shows the selected layer.
- showLayerInfo: Opens the layer information.
- startRouting: Starts the Routing module with the selected address as destination.
- setMarker: Places a marker on the map.
- zoomToResult: Zooms to the search hit.

| Name    | Required | Type     | Default | Description                                                                                             | Expert |
| ------- | -------- | -------- | ------- | ------------------------------------------------------------------------------------------------------- | ------ |
| buttons | no       | String[] |         | Buttons that are displayed in the result list for each search result and perform an action when clicked | false  |
| onClick | no       | String[] |         | Actions that are fired when clicking on a result list item.                                             | false  |
| onHover | no       | String[] |         | Actions that are fired when hovering on a result list item.                                             | false  |

**Example 1**

```json
"resultEvents": {
    "onClick": ["setMarker", "zoomToResult"],
    "onHover": ["setMarker"]
}
```

**Example 2**

```json
"resultEvents": {
    "onClick": ["activateLayerInTopicTree"],
    "buttons": ["showInTree", "showLayerInfo"]
}
```

***

#### portalConfig.secondaryMenu.sections {data-toc-label='Sections'}

[type:about]: # (portalConfig.secondaryMenu.sections.modules.about)
[type:addWMS]: # (portalConfig.secondaryMenu.sections.modules.addWMS)
[type:bufferAnalysis]: # (portalConfig.secondaryMenu.sections.modules.bufferAnalysis)
[type:contact]: # (portalConfig.secondaryMenu.sections.modules.contact)
[type:compareFeatures]: # (portalConfig.secondaryMenu.sections.modules.compareFeatures)
[type:compareMaps]: # (portalConfig.secondaryMenu.sections.modules.compareMaps)
[type:coordToolkit]: # (portalConfig.secondaryMenu.sections.modules.coordToolkit)
[type:copyrightConstraints]: # (portalConfig.secondaryMenu.sections.modules.copyrightConstraints)
[type:customMenuElement]: # (portalConfig.secondaryMenu.sections.modules.customMenuElement)
[type:draw]: # (portalConfig.secondaryMenu.sections.modules.draw)
[type:featureLister]: # (portalConfig.secondaryMenu.sections.modules.featureLister)
[type:fileImport]: # (portalConfig.secondaryMenu.sections.modules.fileImport)
[type:filter]: # (portalConfig.secondaryMenu.sections.modules.filter)
[type:language]: # (portalConfig.secondaryMenu.sections.modules.language)
[type:layerClusterToggler]: # (portalConfig.secondaryMenu.sections.modules.layerClusterToggler)
[type:layerSlider]: # (portalConfig.secondaryMenu.sections.modules.layerSlider)
[type:login]: # (portalConfig.secondaryMenu.sections.modules.login)
[type:measure]: # (portalConfig.secondaryMenu.sections.modules.measure)
[type:modeler3D]: # (portalConfig.secondaryMenu.sections.modules.modeler3D)
[type:news]: # (portalConfig.secondaryMenu.sections.modules.news)
[type:openConfig]: # (portalConfig.secondaryMenu.sections.modules.openConfig)
[type:print]: # (portalConfig.secondaryMenu.sections.modules.print)
[type:routing]: # (portalConfig.secondaryMenu.sections.modules.routing)
[type:scaleSwitcher]: # (portalConfig.secondaryMenu.sections.modules.scaleSwitcher)
[type:selectFeatures]: # (portalConfig.secondaryMenu.sections.modules.selectFeatures)
[type:shadow]: # (portalConfig.secondaryMenu.sections.modules.shadow)
[type:statisticDashboard]: # (portalConfig.secondaryMenu.sections.modules.statisticDashboard)
[type:shareView]: # (portalConfig.secondaryMenu.sections.modules.shareView)
[type:statisticDashboard]: # (portalConfig.secondaryMenu.sections.modules.statisticDashboard)
[type:styleVT]: # (portalConfig.secondaryMenu.sections.modules.styleVT)
[type:wfsSearch]: # (portalConfig.secondaryMenu.sections.modules.wfsSearch)
[type:wfst]: # (portalConfig.secondaryMenu.sections.modules.wfst)

Modules can be divided into sections. In the menu, sections are divided with a horizontal line.

| Name                 | Required | Type                                                                             | Default | Description                                                                                                                                                                                                                                                                                                                                                                                                                                             | Expert |
| -------------------- | -------- | -------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| about                | no       | **[about](#portalconfigmenusectionsmodulesabout)**                               |         | This module displays specific portal information like description, Masterportal version, Metadata.                                                                                                                                                                                                                                                                                                                                                      | true   |
| addWMS               | no       | **[addWMS](#portalconfigmenusectionsmodulesaddwms)**                             |         | This module allows loading specific WMS layers. This is done by providing a URL. All the service's layers are retrieved and offered in the layer tree in section "External technical data".                                                                                                                                                                                                                                                             | true   |
| bufferAnalysis       | no       | **[bufferAnalysis](#portalconfigmenusectionsmodulesbufferanalysis)**             |         | This buffer analysis allows the selection of a source layer, a buffer radius and a target layer. The chosen buffer radius will then be shown around features of the selected source layer. At the moment a target layer is selected, only the features of this layer will be shown, if they are outside the buffer radii. It is also possible to invert the result. In this case the resulting features will only be show if they are inside the radii. | false  |
| contact              | no       | **[contact](#portalconfigmenusectionsmodulescontact)**                           |         | The contact form allows users to send messages to a configured email address. For example, this may be used to allow users to submit errors and suggestions. A file can be appended.                                                                                                                                                                                                                                                                    | false  |
| compareFeatures      | no       | **[compareFeatures](#portalconfigmenusectionsmodulescomparefeatures)**           |         | Offers a comparison option for vector features. The getFeatureInfo (GFI) window will offer a clickable star symbol to put elements on the comparison list. Works when used together with the GFI theme **Default**.                                                                                                                                                                                                                                     | false  |
| compareMaps          | no       | **[compareMaps](#portalconfigmenusectionsmodulescomparemaps)**                   |         | This tool allows users to compare two map layers side by side using a layer swiper.                                                                                                                                                                                                                                                                                                                                                                     | false  |
| coordToolkit         | no       | **[coordToolkit](#portalconfigmenusectionsmodulescoordtoolkit)**                 |         | Coordinate query: Tool to query coordinates and altitude by mouse click: When clicking in the map, the coordinates are frozen in the display and can also be copied directly to the clipboard. Coordinate search: The coordinate system and the coordinates can be entered via an input mask. The tool then zooms to the corresponding coordinate and places a marker on it. The coordinate systems are obtained from config.js.                        | false  |
| copyrightConstraints | no       | **[copyrightConstraints](#portalconfigmenusectionsmodulescopyrightconstraints)** |         | This module loads copyright constraints via the CSW API and shows it per layer. If no information is present, the configured fallback contact information is shown.                                                                                                                                                                                                                                                                                     | false  |
| customMenuElement    | no       | **[customMenuElement](#portalconfigmenusectionsmodulescustommenuelement)**       |         | This module can open a link, display HTML from config.json or an external file, or perform an action. This module can be configured several times in config.json.                                                                                                                                                                                                                                                                                       | false  |
| draw                 | no       | **[draw](#portalconfigmenusectionsmodulesdraw)**                                 |         | **!Attention: The new draw module is currently within refactoring process you can use the draw module from Masterportal Version 2 with type "draw_old")!** The draw tool allows painting points, lines, polygons, circles, double circles, and texts to the map. You may download these drawing as KML, GeoJSON, or GPX.                                                                                                                                | false  |
| featureLister        | no       | **[featureLister](#portalconfigmenusectionsmodulesfeaturelister)**               |         | Lists all features of a vector layer and highlights a feature by mouse over.                                                                                                                                                                                                                                                                                                                                                                            | false  |
| fileImport           | no       | **[fileImport](#portalconfigmenusectionsmodulesfileimport)**                     |         | Import KML, GeoJSON, and GPX files with this modules.                                                                                                                                                                                                                                                                                                                                                                                                   | false  |
| filter               | no       | **[filter](#portalconfigmenusectionsmodulesfilter)**                             |         | Configuration for an advanced filter for vector layers.                                                                                                                                                                                                                                                                                                                                                                                                 | false  |
| language             | no       | **[language](#portalconfigmenusectionsmoduleslanguage)**                         |         | In this module the language of the portal can be switched.                                                                                                                                                                                                                                                                                                                                                                                              | false  |
| layerClusterToggler  | no       | **[layerClusterToggler](#portalconfigmenusectionsmoduleslayerclustertoggler)**   |         | This module allows a cluster layers to be active and deactive together.                                                                                                                                                                                                                                                                                                                                                                                 | false  |
| layerSlider          | no       | **[layerSlider](#portalconfigmenusectionsmoduleslayerslider)**                   |         | The layerSlider module allows showing arbitrary services in order. This can e.g. be used to show aerial footage from multiple years in succession.                                                                                                                                                                                                                                                                                                      | false  |
| login                | no       | **[login](#portalconfigmenusectionsmoduleslogin)**                               |         | Configuration of login with an OIDC server.                                                                                                                                                                                                                                                                                                                                                                                                             | false  |
| measure              | no       | **[measure](#portalconfigmenusectionsmodulesmeasure)**                           |         | Allows measuring areas and distances in the units m/km/nm resp. m²/ha/km².                                                                                                                                                                                                                                                                                                                                                                              | false  |
| modeler3D            | no       | **[modeler3D](#portalconfigmenusectionsmodulesmodeler3d)**                       |         | Allows importing 3D models in .gltf, .dae, .obj formats and drawing extrudable 3D polygons.                                                                                                                                                                                                                                                                                                                                                             | false  |
| news                 | no       | **[news](#portalconfigmenusectionsmodulesnews)**                                 |         | This module shows all messages from the newsFeedPortalAlerts.json and the config.json of the current portal regardless of the "read" status.                                                                                                                                                                                                                                                                                                            | false  |
| openConfig           | no       | **[openConfig](#portalconfigmenusectionsmodulesopenconfig)**                     |         | ith this module a configuration file (config.json) can be reloaded at runtime. The modules and map are adapted to the new configuration.                                                                                                                                                                                                                                                                                                                | false  |
| print                | no       | **[print](#portalconfigmenusectionsmodulesprint)**                               |         | Printing module that can be used to export the map's current view as PDF.                                                                                                                                                                                                                                                                                                                                                                               | false  |
| routing              | no       | **[routing](#portalconfigmenusectionsmodulesrouting)**                           |         | Routing module to create routes and isochrones.                                                                                                                                                                                                                                                                                                                                                                                                         | false  |
| scaleSwitcher        | no       | **[scaleSwitcher](#portalconfigmenusectionsmodulesscaleswitcher)**               |         | Module that allows changing the map's current scale.                                                                                                                                                                                                                                                                                                                                                                                                    | false  |
| selectFeatures       | no       | **[selectFeatures](#portalconfigmenusectionsmodulesselectfeatures)**             |         | Allows selecting a set of vector features by letting the user draw a box on the map. Features in that box will be displayed with GFI information.                                                                                                                                                                                                                                                                                                       | false  |
| shadow               | no       | **[shadow](#portalconfigmenusectionsmodulesshadow)**                             |         | Configuration object for the 3D mode shadow time.                                                                                                                                                                                                                                                                                                                                                                                                       | false  |
| statisticDashboard   | no       | **[statisticDashboard](#portalconfigmenusectionsmodulesstatisticdashboard)**     |         | Displaying statistical data.                                                                                                                                                                                                                                                                                                                                                                                                                            | false  |
| shareView            | no       | **[shareView](#portalconfigmenusectionsmodulesshareview)**                       |         | Module to share a link to the current map view.                                                                                                                                                                                                                                                                                                                                                                                                         | false  |
| styleVT              | no       | **[styleVT](#portalconfigmenusectionsmodulesstylevt)**                           |         | Style selection for VT services. Allows switching between styles of a Vector Tile Layer that provides multiple stylings via the `services.json` file.                                                                                                                                                                                                                                                                                                   | false  |
| wfsSearch            | no       | **[wfsSearch](#portalconfigmenusectionsmoduleswfssearch)**                       |         | Makes it possible to create a form to query WFS layers using filters. It is possible to either use a stored query (WFS@2.0.0) or define the query using the defined parameters (WFS@1.1.0).                                                                                                                                                                                                                                                             | false  |
| wfst                 | no       | **[wfst](#portalconfigmenusectionsmoduleswfst)**                                 |         | WFS-T module to visualize, create, update and delete features.                                                                                                                                                                                                                                                                                                                                                                                          | false  |

***

##### portalConfig.secondaryMenu.sections.modules {data-toc-label='Modules'}

| Name              | Required | Type    | Default | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Expert |
| ----------------- | -------- | ------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| description       | no       | String  |         | The description that should be shown in the button in the right menu.                                                                                                                                                                                                                                                                                                                                                                                                | false  |
| icon              | no       | String  |         | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**.                                                                                                                                                                                                                                                                                                                                | false  |
| name              | no       | String  |         | Name of the module in the menu.                                                                                                                                                                                                                                                                                                                                                                                                                                      | false  |
| showDescription   | no       | String  |         | Indicates whether the description of the module should be displayed in the menu.                                                                                                                                                                                                                                                                                                                                                                                     | false  |
| supportedDevices  | no       | String  |         | Devices on which the module can be used and is displayed in the menu.                                                                                                                                                                                                                                                                                                                                                                                                | false  |
| supportedMapModes | no       | String  |         | Map modes in which the module can be used and is displayed in the menu.                                                                                                                                                                                                                                                                                                                                                                                              | false  |
| type              | no       | String  |         | The type of the module. Defines which module is configured.                                                                                                                                                                                                                                                                                                                                                                                                          | false  |
| showEntryDirectly | no       | Boolean |         | Can **only be set for modules of type `folder`**, and **only for one such folder in the entire project**. The folder opens automatically if **at least one element** in the folder uses `showOnlyByLayersVisible` (triggered when **all layers** in the array `showOnlyByLayersVisible` are visible) **and its action is `"Maps/activateViewpoint"`**. Note: The folder opens only once per unique combination of visible layers defined in showOnlyByLayersVisible. | false  |

**Example**

```json
{
    "name": "Viewpoints",
    "icon": "bi-binoculars-fill",
    "type": "folder",
    "showEntryDirectly": true,
    "elements": [
        {
            "name": "Buildings for Trade and Services",
            "icon": "bi-bullseye",
            "type": "customMenuElement",
            "supportedMapModes": [
                "3D"
            ],
            "showOnlyByLayersVisible": ["16102"],
            "execute": {
                "action": "Maps/activateViewpoint",
                "payload": {
                    "heading": -0.30858728378862876,
                    "tilt": -90,
                    "altitude": 272.3469798217454,
                    "center": [
                        564028.7954571751,
                        5934555.967867207
                    ],
                    "zoom": 7.456437968949651
                }
            }
        }
    ]
}
```
***

##### portalConfig.secondaryMenu.sections.modules.about {data-toc-label='About'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

This module displays specific portal information like description, Masterportal version, Metadata.

| Name                   | Required | Type           | Default                                                              | Description                                                                                                                                        | Expert |
| ---------------------- | -------- | -------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| icon                   | no       | String         | "bi-info-circle"                                                     | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**               | false  |
| name                   | no       | String         | "common:modules.about.name"                                          | Name of the module in the menu.                                                                                                                    | false  |
| type                   | yes      | String         | "about"                                                              | The type of the module. Defines which module is configured.                                                                                        | false  |
| abstractText           | no       | String         | ""                                                                   | Description of the portal                                                                                                                          | false  |
| contact                | no       | String         | null                                                                 | Metadata contact information                                                                                                                       | false  |
| cswUrl                 | no       | String         | ""                                                                   | Metadata URL                                                                                                                                       | false  |
| logo                   | no       | Boolean/String | "../../src/assets/img/Logo_Masterportal.svg"                         | Path to the logo. With `false` the logo is hidden.                                                                                                 | false  |
| logoLink               | no       | String         | "https://masterportal.org"                                           | Link that opens in a new tab when you click on the logo.                                                                                           | false  |
| logoText               | no       | String         | "Masterportallogo"                                                   | Alternative text that is displayed if the logo cannot be displayed.                                                                                | false  |
| metaDataCatalogueId    | no       | String         | "2"                                                                  | Id of the metadata service                                                                                                                         | false  |
| metaId                 | no       | String         | ""                                                                   | Id of the metadata object                                                                                                                          | false  |
| metaUrl                | no       | String         | ""                                                                   | URL of the metadata object                                                                                                                         | false  |
| noMetadataLoaded       | no       | String         | ""                                                                   | Text if no metadata is shown                                                                                                                       | false  |
| showAdditionalMetaData | no       | Boolean        | true                                                                 | Metadata link to show extended metadata                                                                                                            | false  |
| title                  | no       | String         | ""                                                                   | Metadata title                                                                                                                                     | false  |
| version                | no       | Boolean/String | true                                                                 | Version specification of the master portal. With `true` the master portal version is determined automatically. With `false` the version is hidden. | false  |
| versionLink            | no       | String         | "https://bitbucket.org/geowerkstatt-hamburg/masterportal/downloads/" | Link that opens in a new tab when you click on the version.                                                                                        | false  |
| ustId                  | no       | String         | ""                                                                   | Sales tax identification number in accordance with Section 27 of the Sales Tax Act                                                                 | false  |
| privacyStatementText   | no       | String         | "common:modules.about.privacyStatementText"                          | Text for data privacy section                                                                                                                      | false  |
| privacyStatementUrl    | no       | String         | ""                                                                   | URL to data privacy policy site                                                                                                                    | false  |
| accessibilityText      | no       | String         | "common:modules.about.accessibilityText"                             | Text for accessibility section                                                                                                                     | false  |
| accessibilityUrl       | no       | String         | ""                                                                   | URL to the accessibility statement site                                                                                                            | false  |
| hideImprintInFooter    | no       | Boolean        | false                                                                | If true, the imprint link to the about module is hidden in the footer, provided the about module exists.                                           | false  |

```json title="Example"
{
    "icon": "bi-cloud-circle",
    "name": "common:modules.about.name",
    "type": "about",
    "cswUrl": "https://metaver.de/csw",
    "metaUrl": "https://metaver.de/trefferanzeige?docuuid=40D48B03-AD1D-407B-B04D-B5BC6855BE15",
    "metaId": "40D48B03-AD1D-407B-B04D-B5BC6855BE15",
    "hideImprintInFooter": true
}
```

***


##### portalConfig.secondaryMenu.sections.modules.addWMS {data-toc-label='Add WMS'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

The module allows for adding additional WMS layers via a provided URL. The [GDI-DE](https://www.gdi-de.org/download/AK_Geodienste_Architektur_GDI-DE_Bereitstellung_Darstellungsdienste.pdf) recommends setting up a CORS header, see chapter 4.7.1.
Schema for a WMS layer URL: `www.diensteurl/wmsdienste`.

| Name            | Required | Type     | Default                      | Description                                                                                                                           | Expert |
| --------------- | -------- | -------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| featureCount    | no       | Number   |                              | Number of features to return on a GetFeatureInfo query.                                                                               | false  |
| icon            | no       | String   | "bi-cloud-plus"              | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**. | false  |
| name            | no       | String   | "common:modules.addWMS.name" | Name of the module in the menu.                                                                                                       | false  |
| showInLayerTree | no       | Boolean  | false                        | ShowInLayerTree setting for the imported layers.                                                                                      | false  |
| type            | no       | String   | "addWMS"                     | The type of the module. Defines which module is configured.                                                                           | false  |
| visibility      | no       | Boolean  | false                        | Visibility setting for the imported layers.                                                                                           | false  |
| exampleURLs     | no       | String[] | []                           | Example URLs displayed under the module.                                                                                              | false  |

**Example**

```json
{
    "icon": "bi-cloud-plus",
    "featureCount": 10,
    "name": "common:modules.addWMS.name",
    "showInLayerTree": false,
    "type": "addWMS",
    "visibility": false,
    "exampleURLs": [
        "https://sgx.geodatenzentrum.de/wms_sentinel2_de",
        "https://sgx.geodatenzentrum.de/wms_landschaften",
        "https://sgx.geodatenzentrum.de/wms_vg5000_0101"
    ]
}
```

***

##### portalConfig.secondaryMenu.sections.modules.bufferAnalysis {data-toc-label='Buffer Analysis'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

The module highlights features of a target layer, that are located within or outside a circle around the features of a source-Layer. The circle is defined by a buffer-radius. The module requires vector based Data from WFS(❗) services for both the source and the target layer.

| Name | Required | Type   | Default                              | Description                                                                                                                           | Expert |
| ---- | -------- | ------ | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| icon | no       | String | "bi-arrows-angle-expand"             | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**. | false  |
| name | no       | String | "common:modules.bufferAnalysis.name" | Name of the module in the menu.                                                                                                       | false  |
| type | no       | String | "bufferAnalysis"                     | The type of the module. Defines which module is configured.                                                                           | false  |

**Example**

```json
{
    "icon": "bi-arrows-angle-expand",
    "name": "common:modules.bufferAnalysis.name",
    "type": "bufferAnalysis"
}
```

***

##### portalConfig.secondaryMenu.sections.modules.contact {data-toc-label='Contact'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

The contact form allows users to send messages to a configured mail address. A file, e.g. a screenshot, can be attached.

>**This requires a backend!**
>
>**Contact uses an SMTP server and calls its sendmail.php.**

| Name                      | Required | Type                                                        | Default                                         | Description                                                                                                                      | Expert |
| ------------------------- | -------- | ----------------------------------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------ |
| closeAfterSend            | no       | Boolean                                                     | false                                           | Flag determining if the contact window should be closed after successfully sending a message.                                    | false  |
| configuredFileExtensions  | no       | String[]                                                    |                                                 | Additional file extensions to "png", "jpg" und "jpeg". The backend has to support these file types.                              | false  |
| contactInfo               | no       | String                                                      |                                                 | Additional text shown above the contact form.                                                                                    | false  |
| deleteAfterSend           | no       | Boolean                                                     | false                                           | Flag determining whether the contact form is emptied after successfully sending a message.                                       | false  |
| fileUpload                | no       | Boolean                                                     | false                                           | Flag whether the file upload should be available.                                                                                | false  |
| from                      | yes      | **[email](#portalconfigmenusectionsmodulescontactemail)**[] |                                                 | Email sender. Please mind our **hints regarding Email safety** below.                                                            | false  |
| icon                      | no       | String                                                      | "bi-envelope"                                   | Icon that is shown in front of the module in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**. | false  |
| includeSystemInfo         | no       | Boolean                                                     | false                                           | Flag determining if the senders system information should be included in the Email.                                              | false  |
| locationOfCustomerService | no       | String                                                      | "de"                                            | The country the customer service is based in. The parameter is used for the date in the ticketId.                                | false  |
| maxFileSize               | no       | Number                                                      | 1048576                                         | The maximum file size in bytes for uploadable content. Default: 1MB.                                                             | false  |
| maxLines                  | no       | Number                                                      | 5                                               | Amount of lines (height) for the textArea of the form                                                                            | false  |
| name                      | no       | String                                                      | "common:modules.contact.name"                   | Name of the module in the menu.                                                                                                  | false  |
| privacyPolicyLink         | no       | String                                                      | "https://www.masterportal.org/datenschutz.html" | Link to the full privacy policy. Should be given if `showPrivacyPolicy` is set to true.                                          | false  |
| serviceId                 | yes      | String                                                      |                                                 | Email service id. Resolved using the **[rest-services.json](../Global-Config/rest-services.json.md)** file.                      | false  |
| showPrivacyPolicy         | no       | Boolean                                                     | false                                           | Flag determining if a checkbox should be displayed for agreeing to the privacy policy.                                           | false  |
| subject                   | no       | String                                                      |                                                 | The subject to be used for the Email.                                                                                            | false  |
| to                        | yes      | **[email](#portalconfigmenusectionsmodulescontactemail)**[] |                                                 | Recipient of the Email. Please mind our **hints regarding Email safety** below.                                                  | false  |
| type                      | no       | String                                                      | "contact"                                       | The type of the module. Defines which module is configured.                                                                      | false  |
| withTicketNo              | no       | Boolean                                                     | true                                            | Whether successfully sending a email retrieves a ticket number for the user.                                                     | false  |
| infoMessage               | no       | String                                                      | "common:modules.contact.infoMessage"            | Explanatory note                                                                                                                 | false  |

***
**Example**

```json
{
    "type": "contact",
    "name": "common:menu.contact",
    "icon": "bi-envelope",
    "serviceId": "123",
    "from": [
        {
            "email": "lgvgeoportal-hilfe@gv.hamburg.de",
            "name": "LGVGeoportalHilfe"
        }
    ],
    "to": [
        {
            "email": "lgvgeoportal-hilfe@gv.hamburg.de",
            "name": "LGVGeoportalHilfe"
        }
    ],
    "fileUpload": true,
    "includeSystemInfo": true,
    "closeAfterSend": true,
    "deleteAfterSend": true,
    "withTicketNo": false
}
```

!!! danger "Hints regarding Email safety"

    The unchecked usage of *sender (FROM)*, *recipient (TO)*, *copy (CC)*, and *blind copy (BCC)* by the SMTP server is hereby **expressly discouraged** for security reasons. The unchecked usage of the customer email as a *reply to (REPLY-TO)* by the SMTP server is warned against.

    We strongly recommend setting *FROM* and *TO* manually on the SMTP server without offering an option for external configuration.

    >For security reasons, *Sender (FROM)* and *Empfänger (TO)* sent by the Masterportal to the SMTP server may not be used as an email's FROM and TO without further checks. This would create a security breach that allows sending malicious emails with manipulated FROM and TO by the SMTP server. Should you need the configuration in the Masterportal anyway (as in the example above), the parameters *from* and *to* may be used after checking them against a **whistelist** on the SMTP server, preventing sending to or from email addresses not mentioned on the list.

    We recommend not automatically setting the customer's email address in *CC* (or *BCC*).

    >For security reasons, the user may not be automatically set as *Copy (CC)* or *Blind Copy (BCC)* of an email. Such an automatism would allow sending malicious emails by entering a foreign mail address via the SMTP server.

    We strongly recommend to manually remove *CC* and *BCC* on the SMTP server.

    >There must be no option to set *Copy (CC)* or *Blind Copy (BCC)* via the Masterportal. Such a feature could be misused to send malicious emails via the SMTP server.

    We warn against automatically setting the customer email as *REPLY-TO*.

    >The unchecked copying of data to email headers is warned against depending on the security level (resp. age) of the SMTP server, since the risk of *Carriage Return* and *Line Feed* injections may lead to e.g. allowing *REPLY-TO* from the email header line to be escaped to ultimately manipulate the email header itself. (Example: "test@example.com\r\nBCC:target1@example.com,target2@example.com,(...),target(n)@example.com"). In a more abstract case, UTF attacks may be possible, where normally harmless UTF-16 or UTF-32 characters may change the email header's behavior when interpreted as ANSI or UTF-8, having a comparable effect.

***
###### portalConfig.secondaryMenu.sections.modules.contact.email {data-toc-label='Email'}
Email object containing email address, and display name.

| Name  | Required | Type   | Default | Description        | Expert |
| ----- | -------- | ------ | ------- | ------------------ | ------ |
| email | no       | String |         | The email address. | false  |
| name  | no       | String |         | The display name.  | false  |

**Example**

```json
{
    "email": "lgvgeoportal-hilfe@gv.hamburg.de",
    "name":"LGVGeoportalHilfe"
}
```

***

##### portalConfig.secondaryMenu.sections.modules.compareMaps {data-toc-label='Compare Maps'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

This tool allows users to compare two map layers side by side using a layer swiper. Users select layers from the active, visible layers, and the swiper divides the map to show each layer in separate sections. The tool supports WMS and WFS layers.

| Name | Required | Type   | Default       | Description                                                 | Expert |
| ---- | -------- | ------ | ------------- | ----------------------------------------------------------- | ------ |
| type | no       | String | "compareMaps" | The type of the module. Defines which module is configured. | false  |

**Example**

```json
{
    "type": "compareMaps",
}
```

***

##### portalConfig.secondaryMenu.sections.modules.coordToolkit {data-toc-label='Coordinate Toolkit'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

Coordinates tool: to display the height above sea level in addition to the 2 dimensional coordinates, a 'heightLayerId' of a WMS service that provides the height must be specified. The format XML is expected and the attribute for the heights is expected under the value of the parameter 'heightElementName'.

| Name                | Required | Type                                                                   | Default                            | Description                                                                                                                                                                                                                                                                                                                                                                                               | Expert |
| ------------------- | -------- | ---------------------------------------------------------------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| coordInfo           | no       | **[coordInfo](#portalconfigmenusectionsmodulescoordtoolkitcoordinfo)** |                                    | An object with explanations for the coordinate reference systems can be stored here.                                                                                                                                                                                                                                                                                                                      | false  |
| delimiter           | no       | String                                                                 | "Pipe-Symbol"                      | Delimiter of the coordinates when copying the coordinate pair                                                                                                                                                                                                                                                                                                                                             | false  |
| heightElementName   | no       | String                                                                 |                                    | Coordinate query: The element name under which the height in the XML is searched.                                                                                                                                                                                                                                                                                                                         | false  |
| heightLayerId       | no       | String                                                                 |                                    | Coordinate query: Id of the WMS layer that provides the height in XML format. If not defined, then no height is displayed.                                                                                                                                                                                                                                                                                | false  |
| heightLayerInfo     | no       | String                                                                 |                                    | An explanation for the height can be deposited here.                                                                                                                                                                                                                                                                                                                                                      | false  |
| heightValueBuilding | no       | String                                                                 |                                    | Coordinate query: the value in the element defined under "heightElementName" supplied by the WMS for a non-measured height in the building area, it will display the internationalized text "Building area, no heights available" under the key "common:modules.coordToolkit.noHeightBuilding" in the interface. If this attribute is not specified, then the text provided by the WMS will be displayed. | false  |
| heightValueWater    | no       | String                                                                 |                                    | Coordinate query: the value in the element defined under "heightElementName" supplied by the WMS for an unmeasured height in the water area, it will display the internationalized text "Water surface, no heights available" under the key "common:modules.coordToolkit.noHeightWater" in the interface. If this attribute is not specified, then the text provided by the WMS will be displayed.        | false  |
| icon                | no       | String                                                                 | "bi-globe"                         | Icon that is shown in front of the module in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**.                                                                                                                                                                                                                                                                          | false  |
| name                | no       | String                                                                 | "common:modules.coordToolkit.name" | Name of the module in the menu.                                                                                                                                                                                                                                                                                                                                                                           | false  |
| showCopyButtons     | no       | Boolean                                                                | true                               | Switch to show or hide the buttons for copying the coordinates.                                                                                                                                                                                                                                                                                                                                           | false  |
| type                | no       | String                                                                 | "coordToolkit"                     | The type of the module. Defines which module is configured.                                                                                                                                                                                                                                                                                                                                               | false  |
| zoomLevel           | no       | Number                                                                 | 7                                  | Coordinate search: Specifies the zoom level to which you want to zoom.                                                                                                                                                                                                                                                                                                                                    | false  |

**Example**

```json
{
    "type": "coordToolkit",
    "heightLayerId": "19173",
    "heightElementName": "value_0",
    "heightValueWater": "-20",
    "heightValueBuilding": "200",
    "zoomLevel": 5,
    "heightLayerInfo": "Basis of the height information is the \"Digitalge Höhenmodell Hamburg DGM 1\".",
    "showDescription": true,
    "description": "Determine coordinates from the map or search for coordinates.",
    "coordInfo": {
        "title": "Coordinate reference system for 2D position information, explanations",
        "explanations": [
        "ETRS89_UTM32, EPSG 4647 (zE-N): Reference system ETRS89, mapping rule UTM, zone 32",
        "EPSG 25832: explanations..."
        ]
    }
}
```

***

###### portalConfig.secondaryMenu.sections.modules.coordToolkit.coordInfo {data-toc-label='Coord Info'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules.coordToolkit)

| Name         | Required | Type     | Default | Description                                                       | Expert |
| ------------ | -------- | -------- | ------- | ----------------------------------------------------------------- | ------ |
| explanations | no       | String[] |         | Array of declarations from which a list is created.               | false  |
| title        | no       | string   |         | Heading for the explanations of the coordinate reference systems. | false  |

***

##### portalConfig.secondaryMenu.sections.modules.copyrightConstraints {data-toc-label='Copyright Constraints'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

Lists the copyright constraints of active layers.

| Name   | Required | Type   | Default                                     | Description                                                        | Expert |
| ------ | -------- | ------ | ------------------------------------------- | ------------------------------------------------------------------ | ------ |
| name   | nein     | String | "common:modules.copyrightConstraints.name"  | Title shown in the menu.                                           | false  |
| icon   | nein     | String | "bi-c-circle"                               | Icon displayed next to the title.                                  | false  |
| type   | nein     | String | "copyrightConstraints"                      | Defines the module type.                                           | false  |
| cswUrl | nein     | String | "https://gdk.gdi-de.org/gdi-de/srv/ger/csw" | URL of the CSW interface providing usage information and metadata. | false  |

```json title="Example"
{
    "name": "common:modules.copyrightConstraints.name",
    "icon": "bi-c-circle",
    "type": "copyrightConstraints",
    "cswUrl": "https://gdk.gdi-de.org/gdi-de/srv/ger/csw"
}
```

***

##### portalConfig.secondaryMenu.sections.modules.customMenuElement {data-toc-label='Custom Menu Element'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

This module can open a link, display HTML from config.json or an external file, or perform an action. This module can be configured multiple times in config.json. If `htmlContent` is specified, then `pathToContent` is not executed and vice versa.

| Name                    | Required | Type                                                                | Default             | Description                                                                                                                                                              | Expert |
| ----------------------- | -------- | ------------------------------------------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| execute                 | no       | [execute](#portalconfigmenusectionsmodulescustommenuelementexecute) |                     | Action to be executed by clicking on the menu item.                                                                                                                      | true   |
| htmlContent             | no       | String                                                              |                     | HTML displayed in the module. The HTML is not validated, the responsibility for the security of the HTML lies with the operator of the portal.                           | false  |
| icon                    | no       | String                                                              | "bi-asterisk"       | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**.                                    | false  |
| name                    | no       | String                                                              |                     | Name of the module in the menu.                                                                                                                                          | false  |
| openURL                 | no       | String                                                              |                     | Url that is to be opened in a new tab by clicking on the menu item.                                                                                                      | false  |
| pathToContent           | no       | String                                                              |                     | Path to a file containing HTML displayed in the module. The HTML is not validated, the responsibility for the security of the HTML lies with the operator of the portal. | false  |
| showOnlyByLayersVisible | no       | String[]                                                            |                     | List of layer IDs that must be visible for the module to appear. If not specified, the module will be visible by default.                                                | false  |
| type                    | yes      | String                                                              | "customMenuElement" | The type of the module. Defines which module is configured.                                                                                                              | false  |

**Example**

```json
 {
    "type": "customMenuElement",
    "name": "Open url",
    "openURL": "https://geoinfo.hamburg.de/"
 },
{
    "type": "customMenuElement",
    "name": "Open url and show HTML",
    "openURL": "https://geoinfo.hamburg.de/",
    "htmlContent": "<div><h1>This is a Heading</h1><p>url was opened!<p/></div>"
},
{
    "type": "customMenuElement",
    "name": "HTML from config.json und action",
    "htmlContent": "<div><p>This is a paragraph.</p></br><a href=\"https://www.w3schools.com/\" target=\"_blank\">Visit W3Schools.com!</a></div>",
    "execute":{
        "action": "Alerting/addSingleAlert",
        "payload":  {"title":"to all people", "content": "Hallo world"}
    }
},
{
    "type": "customMenuElement",
    "name": "Activate Viewpoint",
    "showOnlyByLayersVisible": ["16102", "33362"],
    "execute": {
        "action": "Maps/activateViewpoint",
        "payload": {
            "layerIds": ["4905", "4538"],
            "heading": -0.30858728378862876,
            "tilt": 0.9321791580603296,
            "altitude": 272.3469798217454,
            "center": [564028.7954571751, 5934555.967867207],
            "zoom": 7.456437968949651
        }
    }
}
```

***

###### portalConfig.secondaryMenu.sections.modules.customMenuElement.execute {data-toc-label='Execute'}

[type:Payload]: # (Datatypes.Payload)

CustomMenuElement Module `execute` options.

| Name    | Required | Type                                                                                                                                | Default | Description                                                 | Expert |
| ------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------- | ----------------------------------------------------------- | ------ |
| action  | yes      | String                                                                                                                              |         | Name and, if applicable, path of the action to be executed. | true   |
| payload | no       | **[Payload](#datatypespayload)**/[viewpointActivation](#portalconfigmenusectionsmodulescustommenuelementexecuteviewpointactivation) |         | Payload that is transferred to the action.                  | true   |

**Example**

```json
{
    "action": "Alerting/addSingleAlert",
    "payload":  {"title":"to all people", "content": "Hallo world"}
}
```

***

###### portalConfig.secondaryMenu.sections.modules.customMenuElement.execute.viewpointActivation {data-toc-label='Viewpoint Activation'}

The `Maps/activateViewpoint` action configures and activates a specific viewpoint on a map. It requires the `execute` object to include the following payload:

| Name     | Required | Type     | Default | Description                                                             | Expert |
| -------- | -------- | -------- | ------- | ----------------------------------------------------------------------- | ------ |
| layerIds | no       | String[] |         | List of IDs for the map layers to activate.                             | true   |
| heading  | no       | Number   |         | The direction the map is facing, in radians.                            | true   |
| tilt     | no       | Number   |         | Tilt angle of the map view, in radians.                                 | true   |
| altitude | no       | Number   |         | Camera altitude in meters above ground.                                 | true   |
| center   | no       | Number[] |         | [X, Y] coordinates of the center in the map's spatial reference system. | true   |
| zoom     | no       | Number   |         | Zoom level of the map view.                                             | true   |

**Example:**
```json
{
    "action": "Maps/activateViewpoint",
    "payload": {
        "layerIds": ["4905", "4538"],
        "heading": -0.30858728378862876,
        "tilt": 0.9321791580603296,
        "altitude": 272.3469798217454,
        "center": [564028.7954571751, 5934555.967867207],
        "zoom": 7.456437968949651
    }
}
```

***

##### portalConfig.secondaryMenu.sections.modules.draw {data-toc-label='Draw'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

!!! warning "Ongoing Refactoring"
    The new draw module is currently within refactoring process you can use the draw module from Masterportal Version 2 with type "draw_old"!
    Module used to draw features on the map. This includes points, which may also be represented by symbols, and (double) circles, polygons, polylines, and text.

| Name                     | Required | Type                                                                               | Default                                                                                                                                                                                                                                                                                                                                 | Description                                                                                                                                                                                     | Expert |
| ------------------------ | -------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| name                     | yes      | String                                                                             |                                                                                                                                                                                                                                                                                                                                         | Tool name in the menu.                                                                                                                                                                          | false  |
| iconList                 | no       | **[icon](#portalconfigmenusectionsmodulesdrawicon)**[]                             | [{"id": "iconPoint", "type": "simple_point", "value": "simple_point"}, {"id": "yellow pin", "type": "image", "scale": 2, "value": "geo-fill-ylw.svg"}]                                                                                                                                                                                  | List of symbols the user may choose from to draw colored symbols or dots. Images may be used, too, as shown in the example.                                                                     | false  |
| drawSymbolSettings       | no       | **[drawSymbolSet](#portalconfigmenusectionsmodulesdrawdrawsymbolset)**             | {"color": [55, 126, 184, 1], "opacity": 1}                                                                                                                                                                                                                                                                                              | Pre-configuration for symbol drawing.                                                                                                                                                           | false  |
| addIconsOfActiveLayers   | no       | Boolean                                                                            | false                                                                                                                                                                                                                                                                                                                                   | Set this flag to `true` to be able to select the icons and symbols of all WFS layers activated in the topic tree as additional symbols besides the icons configured under `drawSymbolSettings`. | false  |
| drawLineSettings         | no       | **[drawLineSet](#portalconfigmenusectionsmodulesdrawdrawlineset)**                 | {"strokeWidth": 1, "opacityContour": 1, "colorContour": [0, 0, 0, 1]}                                                                                                                                                                                                                                                                   | Pre-configuration for line drawing.                                                                                                                                                             | false  |
| drawCurveSettings        | no       | **[drawCurveSet](#portalconfigmenusectionsmodulesdrawdrawcurveset)**               | {"strokeWidth": 1, "opacityContour": 1, "colorContour": [0, 0, 0, 1]}                                                                                                                                                                                                                                                                   | Pre-configuration for freehand drawing.                                                                                                                                                         | false  |
| drawAreaSettings         | no       | **[drawAreaSet](#portalconfigmenusectionsmodulesdrawdrawareaset)**                 | {"strokeWidth": 1, "color": [55, 126, 184, 1], "opacity": 1, "colorContour": [0, 0, 0, 1], "opacityContour": 1}                                                                                                                                                                                                                         | Pre-configuration for area drawing.                                                                                                                                                             | false  |
| drawCircleSettings       | no       | **[drawCircleSet](#portalconfigmenusectionsmodulesdrawdrawcircleset)**             | {"circleMethod": "interactive", "unit": "m", "circleRadius": null, "strokeWidth": 1, "color": [55, 126, 184, 1], "opacity": 1, "colorContour": [0, 0, 0, 1], "opacityContour": 1, "tooltipStyle": {"fontSize": "16px", "paddingTop": "3px", "paddingLeft": "3px", "paddingRight": "3px", "backgroundColor": "rgba(255, 255, 255, .9)"}} | Pre-configuration for circle drawing.                                                                                                                                                           | false  |
| drawDoubleCircleSettings | no       | **[drawDoubleCircleSet](#portalconfigmenusectionsmodulesdrawdrawdoublecircleset)** | {"circleMethod": "defined", "unit": "m", "circleRadius": 0, "circleOuterRadius": 0, "strokeWidth": 1, "color": [55, 126, 184, 1], "opacity": 1, "colorContour": [0, 0, 0, 1], "outerColorContour": [0, 0, 0, 1], "opacityContour": 1}                                                                                                   | Pre-configuration for double circle drawing.                                                                                                                                                    | false  |
| writeTextSettings        | no       | **[writeTextSet](#portalconfigmenusectionsmodulesdrawwritetextset)**               | {"text": "", "fontSize": 10, "font": "Arial", "color": [55, 126, 184, 1], "opacity": 1}                                                                                                                                                                                                                                                 | Pre-configuration for text writing.                                                                                                                                                             | false  |
| download                 | no       | **[download](#portalconfigmenusectionsmodulesdrawdownload)**                       | {"preSelectedFormat": "KML"}                                                                                                                                                                                                                                                                                                            | Pre-configuration for download.                                                                                                                                                                 | false  |
| enableAttributesSelector | no       | Boolean                                                                            | false                                                                                                                                                                                                                                                                                                                                   | Enables an button which toggles an edit section for custom attributes on the selected feature.                                                                                                  | false  |
| semicolonCSVDelimiter    | no       | Boolean                                                                            | true                                                                                                                                                                                                                                                                                                                                    | To decide if the semicolon is used as the delimiter for exported CSV file.                                                                                                                      | false  |

**Example**

```json

{
    "type": "draw_old",
    "name": "Draw / Write",
    "icon": "bi-pencil-fill",
    "iconList": [
        {
            "id": "iconPoint",
            "type": "simple_point",
            "value": "simple_point"
        },
        {
            "id": "iconMeadow",
            "type": "image",
            "scale": 0.8,
            "value": "meadow.png"
        },
        {
            "id": "yellow pin",
            "type": "image",
            "scale": 2,
            "value": "geo-fill-ylw.svg"
        }
    ],
    "drawDoubleCircleSettings": {
        "circleRadius": 1500,
        "circleOuterRadius": 3000,
        "strokeWidth": 3,
        "color": [55, 126, 184, 0],
        "opacity": 0,
        "colorContour": [228, 26, 28, 1],
        "opacityContour": 1,
        "tooltipStyle": {
            "fontSize": "14px",
            "paddingTop": "3px",
            "paddingLeft": "3px",
            "paddingRight": "3px",
            "backgroundColor": "rgba(255, 255, 255, .9)"
        }
    }
    "semicolonCSVDelimiter": true
}

```

***

###### portalConfig.secondaryMenu.sections.modules.draw.icon {data-toc-label='Icon'}

Dot object consisting of text, type, and value.

| Name    | Required | Type                          | Default | Description                                                                                                                                                                                                                                                                                                                                                    | Expert |
| ------- | -------- | ----------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| id      | yes      | String                        |         | Symbol text displayed in the select menu. The id has to be defined in the locale file (usually `common`) as `modules.draw.iconList` child. The following entry should begin with `icon` and contain a representative description. If the key is not found, the `id` will appear as string on the user interface.                                               | false  |
| caption | no       | String                        |         | _Deprecated in 3.0.0._ Symbol text displayed in the select menu. Unlike `id`, not only the id itself, but the whole path (`modules.draw.iconList` + id) has to be given.                                                                                                                                                                                       | false  |
| type    | yes      | enum["image", "simple_point"] |         | Object type to be drawn. If `image` is chosen, the PNG or SVG file from the `value` path is drawn. By default, images are to be placed in the `/src/assets/img/tools/draw/` directory and should have a height and width of 96px to scale correctly. Alternatively, a working `scale` factor must be defined. The key `simple_point` will draw a simple point. | false  |
| scale   | no       | number                        |         | Scale factor for images.                                                                                                                                                                                                                                                                                                                                       | false  |
| value   | yes      | String                        |         | Value of the object to be drawn. If no path or URL is set, a file name is expected, and the *config.js* entry `wfsImgPath` is expected to be the file's location.                                                                                                                                                                                              | false  |

**Example**

```json
{
    "iconList": [
        {
            "id": "iconPoint",
            "type": "simple_point",
            "value": "simple_point"
        },
        {
            "id": "iconMeadow",
            "type": "image",
            "scale": 0.8,
            "value": "meadow.png"
        },
        {
            "id": "yellow pin",
            "type": "image",
            "scale": 2,
            "value": "geo-fill-ylw.svg"
        }
    ]
}
```

***


###### portalConfig.secondaryMenu.sections.modules.draw.drawSymbolSet {data-toc-label='Symbol Set'}

Object to change the drawing tool's configured point symbol default value.

| Name    | Required | Type     | Default           | Description                                                                                              | Expert |
| ------- | -------- | -------- | ----------------- | -------------------------------------------------------------------------------------------------------- | ------ |
| color   | yes      | Number[] | [55, 126, 184, 1] | The pre-configured color of the symbol as RGB color. The alpha channel value is used for point coloring. | false  |
| opacity | yes      | Number   | 1                 | The pre-configured transparency of symbols, given in range [0..1] for point data.                        | false  |


**Example**

```json
{
    "color": [55, 126, 184, 1],
    "opacity": 1
}
```

***

###### portalConfig.secondaryMenu.sections.modules.draw.drawLineSet {data-toc-label='Line Set'}

Object to change the drawing tool's configured line default value.

| Name           | Required | Type     | Default      | Description                                       | Expert |
| -------------- | -------- | -------- | ------------ | ------------------------------------------------- | ------ |
| strokeWidth    | yes      | Number   | 1            | Pre-configured stroke width of lines in pixels.   | false  |
| colorContour   | yes      | Number[] | [0, 0, 0, 1] | Pre-configured line color in RGBA.                | false  |
| opacityContour | yes      | Number   | 1            | Pre-configured line transparency in range [0..1]. | false  |

**Example**

```json
{
    "strokeWidth": 1,
    "opacityContour": 1,
    "colorContour": [0, 0, 0, 1]
}
```

***

###### portalConfig.secondaryMenu.sections.modules.draw.drawCurveSet {data-toc-label='Curve Set'}

Object to change the drawing tool's configured freehand drawing default value.

| Name           | Required | Type     | Default      | Description                                       | Expert |
| -------------- | -------- | -------- | ------------ | ------------------------------------------------- | ------ |
| strokeWidth    | yes      | Number   | 1            | Pre-configured stroke width of lines in pixels.   | false  |
| colorContour   | yes      | Number[] | [0, 0, 0, 1] | Pre-configured line color in RGBA.                | false  |
| opacityContour | yes      | Number   | 1            | Pre-configured line transparency in range [0..1]. | false  |

**Example**

```json
{
    "strokeWidth": 1,
    "opacityContour": 1,
    "colorContour": [0, 0, 0, 1]
}
```

***

###### portalConfig.secondaryMenu.sections.modules.draw.drawAreaSet {data-toc-label='Area Set'}

Object to change the drawing tool's configured area default value.

| Name           | Required | Type     | Default           | Description                                              | Expert |
| -------------- | -------- | -------- | ----------------- | -------------------------------------------------------- | ------ |
| strokeWidth    | yes      | Number   | 1                 | Pre-configured stroke width of area borders in pixels.   | false  |
| color          | yes      | Number[] | [55, 126, 184, 1] | Pre-configured area color in RGBA.                       | false  |
| opacity        | yes      | Number   | 1                 | Pre-configured area transparency in range [0..1].        | false  |
| colorContour   | yes      | Number[] | [0, 0, 0, 1]      | Pre-configured area border color in RGBA.                | false  |
| opacityContour | yes      | Number   | 1                 | Pre-configured area border transparency in range [0..1]. | false  |

**Example**

```json
{
    "strokeWidth": 1,
    "color": [55, 126, 184, 1],
    "opacity": 1,
    "colorContour": [0, 0, 0, 1],
    "opacityContour": 1
}
```

***

###### portalConfig.secondaryMenu.sections.modules.draw.drawCircleSet {data-toc-label='Circle Set'}

Object to change the drawing tool's configured circle default value.

| Name           | Required | Type     | Default           | Description                                                                                                    | Expert |
| -------------- | -------- | -------- | ----------------- | -------------------------------------------------------------------------------------------------------------- | ------ |
| circleMethod   | yes      | String   | "interactive"     | Pre-configured method of circle drawing. `"interactive"`: freehand, `"defined"`: by entering fixed values      | false  |
| unit           | yes      | String   | "m"               | Pre-configured unit regarding the circle's Radius `circleRadius` when `"defined"` is chosen as `circleMethod`. | false  |
| circleRadius   | yes      | Number   | 0                 | Pre-configured circle Radius when `"defined"` is chosen as `circleMethod`.                                     | false  |
| strokeWidth    | yes      | Number   | 1                 | Pre-configured stroke width of circle border in pixels.                                                        | false  |
| color          | yes      | Number[] | [55, 126, 184, 1] | Pre-configured circle color in RGBA.                                                                           | false  |
| opacity        | yes      | Number   | 1                 | Pre-configured circle transparency in range [0..1].                                                            | false  |
| colorContour   | yes      | Number[] | [0, 0, 0, 1]      | Pre-configured circle border color in RGBA.                                                                    | false  |
| opacityContour | yes      | Number   | 1                 | Pre-configured circle border transparency in range [0..1].                                                     | false  |
| tooltipStyle   | no       | String   | {}                | Pre-configured style for tooltip.                                                                              | false  |

**Example**

```json
{
    "circleMethod": "interactive",
    "unit": "m",
    "circleRadius": 0,
    "strokeWidth": 1,
    "color": [55, 126, 184, 1],
    "opacity": 1,
    "colorContour": [0, 0, 0, 1],
    "opacityContour": 1
}
```

***

###### portalConfig.secondaryMenu.sections.modules.draw.drawDoubleCircleSet {data-toc-label='Double Circle Set'}

Object to change the drawing tool's configured circle default value.

| Name              | Required | Type     | Default           | Description                                                                                                                            | Expert |
| ----------------- | -------- | -------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| circleMethod      | yes      | String   | "defined"         | Pre-configured method of circle drawing. `"interactive"`: freehand, `"defined"`: by entering fixed values                              | false  |
| unit              | yes      | String   | "m"               | Pre-configured unit regarding the circle's radius `circleRadius` and `circleOuterRadius` when `"defined"` is chosen as `circleMethod`. | false  |
| circleRadius      | yes      | Number   | 0                 | Pre-configured inner circle radius when `"defined"` is chosen as `circleMethod`.                                                       | false  |
| circleOuterRadius | yes      | Number   | 0                 | Pre-configured outer circle radius when `"defined"` is chosen as `circleMethod`.                                                       | false  |
| strokeWidth       | yes      | Number   | 1                 | Pre-configured stroke width of circle border in pixels.                                                                                | false  |
| color             | yes      | Number[] | [55, 126, 184, 1] | Pre-configured circle color in RGBA.                                                                                                   | false  |
| opacity           | yes      | Number   | 1                 | Pre-configured double circle transparency in range [0..1].                                                                             | false  |
| colorContour      | yes      | Number[] | [0, 0, 0, 1]      | Pre-configured inner circle border color in RGBA.                                                                                      | false  |
| outerColorContour | yes      | Number[] | [0, 0, 0, 1]      | Pre-configured outer circle border color in RGBA.                                                                                      | false  |
| opacityContour    | yes      | Number   | 1                 | Pre-configured circle border transparency in range [0..1].                                                                             | false  |

**Example**

```json
{
    "circleMethod": "defined",
    "unit": "m",
    "circleRadius": 0,
    "circleOuterRadius": 0,
    "strokeWidth": 1,
    "color": [55, 126, 184, 1],
    "opacity": 1,
    "colorContour": [0, 0, 0, 1],
    "opacityContour": 1
}
```

***

###### portalConfig.secondaryMenu.sections.modules.draw.writeTextSet {data-toc-label='Write Text Set'}

Object to change the drawing tool's configured text default value.

| Name     | Required | Type     | Default           | Description                                                                         | Expert |
| -------- | -------- | -------- | ----------------- | ----------------------------------------------------------------------------------- | ------ |
| text     | yes      | String   | ""                | Pre-configured text.                                                                | false  |
| fontSize | yes      | Number   | 10                | Pre-configured font size.                                                           | false  |
| font     | yes      | String   | "Arial"           | Pre-configured font. Restricted to `"Arial"`, `"Calibri"`, and `"Times New Roman"`. | false  |
| color    | yes      | Number[] | [55, 126, 184, 1] | Pre-configured font color in RGBA.                                                  | false  |
| opacity  | yes      | Number   | 1                 | Pre-configured font transparency in range [0..1].                                   | false  |

**Example**

```json
{
    "text": "",
    "fontSize": 10,
    "font": "Arial",
    "color": [55, 126, 184, 1],
    "opacity": 1
}
```

***

###### portalConfig.secondaryMenu.sections.modules.draw.download {data-toc-label='Download'}

Object to change the drawing tool's download preselected format. It should be one of "KML", "GEOJSON" and "GPX".

| Name              | Required | Type                        | Default | Description                       | Expert |
| ----------------- | -------- | --------------------------- | ------- | --------------------------------- | ------ |
| preSelectedFormat | no       | enum["KML","GEOJSON","GPX"] | "KML"   | Pre-configured pre-selected form. | false  |

**Example**

```json
{
    "preSelectedFormat": "KML"
}
```

##### portalConfig.secondaryMenu.sections.modules.featureLister {data-toc-label='Feature Lister'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

This module can display loaded vector data from WFS(❗) layers in a table. All visible vector layers from the map are displayed in the first tab. The features of the layer are listed in the second tab of the table. The number of displayed features is configurable.

As soon as you position the mouse pointer over a feature in the list, it will be highlighted in the map. By clicking on a feature, its attributes are displayed in a third tab.

| Name                          | Required | Type                                                                                                            | Default                             | Description                                                                                                                                        | Expert |
| ----------------------------- | -------- | --------------------------------------------------------------------------------------------------------------- | ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| highlightVectorRulesPointLine | no       | **[highlightVectorRulesPointLine](#portalconfigmenusectionsmodulesfeaturelisterhighlightvectorrulespointline)** |                                     | Specify outline color and stroke width for highlighting lines and fill color and scale factor for highlighting points as well as a zoom parameter. | false  |
| highlightVectorRulesPolygon   | no       | **[highlightVectorRulesPolygon](#portalconfigmenusectionsmodulesfeaturelisterhighlightvectorrulespolygon)**     |                                     | Specify the fill color and outline color and stroke width for highlighting the polygon features as well as a zoom parameter.                       | false  |
| icon                          | no       | String                                                                                                          | "bi-list"                           | Icon that is shown in front of the module in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**.                   | false  |
| maxFeatures                   | no       | Integer                                                                                                         | 20                                  | Amount of features to display initially. More features of the same amount can be revealed by clicking a button.                                    | false  |
| name                          | no       | String                                                                                                          | "common:modules.featureLister.name" | Name of the module in the menu.                                                                                                                    | false  |
| type                          | yes      | String                                                                                                          | "featureLister"                     | The type of the module. Defines which module is configured.                                                                                        | false  |

**Example**

```json
"featureLister": {
    "name": "List",
    "icon": "bi-list",
    "maxFeatures": 10,
    "highlightVectorRulesPolygon": {
        "fill": {
            "color": [255, 0, 255, 0.9]
        },
        "stroke": {
            "width": 4,
            "color": [0, 0, 204, 0.9]
        },
        "zoomLevel": 5
    },
    "highlightVectorRulesPointLine": {
        "fill": {
            "color": [255, 0, 255, 0.9]
        },
        "stroke": {
            "width": 8,
            "color": [255, 0, 255, 0.9]
        },
        "image": {
            "scale": 2
        },
        "zoomLevel": 5
    }
}
```

***

###### portalConfig.secondaryMenu.sections.modules.featureLister.highlightVectorRulesPointLine {data-toc-label='Highlight Vector Rules Point Line'}

[type:Image]: # (Datatypes.Image)
[type:Fill]: # (Datatypes.Fill)
[type:Stroke]: # (Datatypes.Stroke)

Specify outline color and stroke width for highlighting lines and fill color and scale factor for highlighting points. Also a zoom level can be configured.

| Name      | Required | Type                           | Default              | Description                       | Expert |
| --------- | -------- | ------------------------------ | -------------------- | --------------------------------- | ------ |
| fill      | no       | **[Fill](#datatypesfill)**     | [255, 255, 255, 0.5] | Possible setting: color           | false  |
| image     | no       | **[Image](#datatypesimage)**   | 1.5                  | Possible setting: scale           | false  |
| stroke    | no       | **[Stroke](#datatypesstroke)** | 1                    | Possible setting: width           | false  |
| zoomLevel | no       | Integer                        | 7                    | Zoom level, possible setting: 0-9 | false  |

***

###### portalConfig.secondaryMenu.sections.modules.featureLister.highlightVectorRulesPolygon {data-toc-label='Highlight Vector Rules Polygon'}

[type:Fill]: # (Datatypes.Fill)
[type:Stroke]: # (Datatypes.Stroke)

Specify the fill color, the outline color and stroke width for highlighting the polygon features as well as a zoom level.

| Name      | Required | Type                           | Default              | Description                       | Expert |
| --------- | -------- | ------------------------------ | -------------------- | --------------------------------- | ------ |
| fill      | no       | **[Fill](#datatypesfill)**     | [255, 255, 255, 0.5] | Possible setting: color           | false  |
| stroke    | no       | **[Stroke](#datatypesstroke)** | 1                    | Possible setting: width           | false  |
| zoomLevel | no       | Integer                        | 7                    | Zoom level, possible setting: 0-9 | false  |

***

##### portalConfig.secondaryMenu.sections.modules.fileImport {data-toc-label='File Import'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

Import "*.kml", "*.geojson" and "*.gpx" files with this module.

| Name                | Required | Type    | Default                          | Description                                                                                                                           | Expert |
| ------------------- | -------- | ------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| enableZoomToExtend  | no       | Boolean | false                            | To decide if the file name is shown as a button and it is able to zoom the imported features by clicking the file name                | false  |
| icon                | no       | String  | "bi-box-arrow-in-down"           | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**. | false  |
| name                | no       | String  | "common:modules.fileImport.name" | Name of the module in the menu.                                                                                                       | false  |
| type                | no       | String  | "fileImport"                     | The type of the module. Defines which module is configured.                                                                           | false  |
| customStylingOption | no       | Boolean | false                            | To decide if a custom styling option for a GeoJson is offered.                                                                        | false  |
| showConfirmation    | no       | Boolean | true                             | To decide if a confirmation window is shown after a successful import.                                                                | false  |

**Example**

```json
{
    "type": "fileImport",
    "enableZoomToExtend": true
}
```

***

##### portalConfig.secondaryMenu.sections.modules.filter {data-toc-label='Filter'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

The filter tool offers a range of options to filter vector data from WFS, OAF, GeoJSON, SensorThingsAPI and VectorTiles services.

| Name                       | Required | Type                                                                                     | Default                      | Description                                                                                                                                                                                                                | Expert |
| -------------------------- | -------- | ---------------------------------------------------------------------------------------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| geometrySelectorOptions    | no       | [filterGeometrySelector](#portalconfigmenusectionsmodulesfilterfiltergeometryselector)[] | false                        | Options for an additional tool for filtering within a self-drawn area. If you use this tool in conjunction with external filtering (`external`: `true`), please remember to configure your layer filter with geometryName. | false  |
| layerGroups                | no       | [filterLayerGroups](#portalconfigmenusectionsmodulesfilterfilterlayergroups)[]           | []                           | Configuration of the related layers to be filtered.                                                                                                                                                                        | false  |
| layers                     | no       | [filterLayer](#portalconfigmenusectionsmodulesfilterfilterlayer)[]                       | []                           | Configuration of layers to be filtered. Can be an array of plain layer ids also - if so the layer and all snippets are identified automatically.                                                                           | false  |
| liveZoomToFeatures         | no       | Boolean                                                                                  | true                         | Defines whether the filter immediately zooms to filter results.                                                                                                                                                            | false  |
| minScale                   | no       | Integer                                                                                  | 5000                         | Minimum zoom level the filter zooms in when displaying filter results.                                                                                                                                                     | false  |
| multiLayerSelector         | no       | Boolean                                                                                  | true                         | Controls whether all filters can be active or only one at same time.                                                                                                                                                       | false  |
| name                       | no       | String                                                                                   | "common:modules.filter.name" | Name of the module in the menu.                                                                                                                                                                                            | false  |
| saveTo                     | no       | String                                                                                   | "void"                       | If set to "url", the current filter setting is saved. The shareView module can be used to create a link containing the filter settings.                                                                                    | false  |
| showCurrentlyActiveFilters | no       | Boolean                                                                                  | true                         | Displays an area above all configured filters in which the currently active filters are shown. Here, you can also delete individual values or all filter settings that the user has made.                                  | false  |
| linkText                   | no       | String                                                                                   | ""                           | Link text at the bottom containing a url link to the current filter setting, or empty string if no such link should be displayed. Requires "saveTo": "url"                                                                 | false  |
| type                       | no       | String                                                                                   | "filter"                     | The type of the module. Defines which module is configured.                                                                                                                                                                | false  |
| closeGfi                   | no       | Boolean                                                                                  | false                        | If it is true and a gfi window is open, the gfi window could be closed after new filtering.                                                                                                                                | false  |
| questionLink               | no       | String                                                                                   | ""                           | The URL for the tool information button (questionmark)                                                                                                                                                                     | false  |
| closeDropdownOnSelect      | no       | Boolean                                                                                  | true                         | Enable/disable closing dropdown list after selecting an option.                                                                                                                                                            | false  |
| collapseButtons            | no       | Boolean                                                                                  | false                        | If collapseButtons is set to `true`, buttons are displayed instead of accordions.                                                                                                                                          | false  |
| clearAll                   | no       | Boolean                                                                                  | false                        | After clicking button Reset all, all the features will be shown. Set to `true` to clear all the features after clicking Reselt all button.                                                                                 | false  |

**Example**

The following example uses only a layer id to generate the filter automatically.

```json
{
    "type": "filter",
    "icon": "bi-funnel-fill",
    "closeDropdownOnSelect": true,
    "clearAll": false,
    "geometrySelectorOptions": {
        "visible": true
    },
    "closeGfi": false,
    "questionLink": "https://bitbucket.org/geowerkstatt-hamburg/addons/src/dev/cosi/manuals/005filter.md",
    "showCurrentlyActiveFilters": true,
    "layerGroups":
    [
        {
            "title": "GRUPPE 1",
            "layers": [
                {
                    "layerId": "47"
                }
            ]
        }
    ],
    "layers": [
        {
            "layerId": "8712"
        }
    ]
}
```

***

###### portalConfig.secondaryMenu.sections.modules.filter.filterGeometrySelector {data-toc-label='Filter Geometry Selector'}

An additional selection appears above the filter where a geometry can be selected and drawn on the map. The filter filters only in the selected area.
If you use this modul in conjunction with external filtering (`external`: `true`), please remember to configure your layer filter with geometryName.

| Name                 | Required | Type     | Default                                          | Description                                                                                                                                                                                        | Expert |
| -------------------- | -------- | -------- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| additionalGeometries | no       | Boolean  | false                                            | Geometries from a layer can additionally be added to the filter by the id. In that case, an attribute for the name of the geometry must also be specified. Currently only possible with WFS layer. | false  |
| circleSides          | no       | Number   | 256                                              | The geometry "Circle" is converted to a polygon for technical reasons. This is the number of polygon points of the resulting geometry.                                                             | false  |
| defaultBuffer        | no       | Number   | 20                                               | The geometry "LineString" is given a buffer (in meters) to make the LineString a "tube". This is the default distance from the center to the edge in meters.                                       | false  |
| fillColor            | no       | String   | "rgba(0, 0, 0, 0.33)"                            | The fill color of the outer area (or geometry if invertGeometry = `false`).                                                                                                                        | false  |
| geometries           | no       | String[] | ["Polygon", "Rectangle", "Circle", "LineString"] | The selectable geometries and their order.                                                                                                                                                         | false  |
| invertGeometry       | no       | Boolean  | true                                             | true: The geometry is transparent, the outer area is displayed as a shadow. `false`: The fill specifications apply to the geometry itself.                                                         | false  |
| strokeColor          | no       | String   | "rgba(0, 0, 0, 1)"                               | The color of the border of the geometry.                                                                                                                                                           | false  |
| strokeWidth          | no       | Number   | 1                                                | The thickness of the border of the geometry.                                                                                                                                                       | false  |
| visible              | yes      | Boolean  | true                                             | Activates the geometry selector.                                                                                                                                                                   | false  |

**Example**

Example of the minimal configuration of the `filterGeometrySelector`.

```json
{
    "visible": true
}
```

**Example**

Example of a complete configuration with the default settings of the `filterGeometrySelector`.

```json
{
    "visible": true,
    "circleSides": 256,
    "defaultBuffer": 20,
    "geometries": ["Polygon", "Rectangle", "Circle", "LineString"],
    "invertGeometry": true,
    "fillColor": "rgba(0, 0, 0, 0.33)",
    "strokeColor": "rgba(0, 0, 0, 1)",
    "strokeWidth": 1,
    "additionalGeometries": [
        {
            "layerId": "1692",
            "attrNameForTitle": "bezirk_name"
        }
    ]
}
```

**Example**

Example of a completely changed configuration of the `filterGeometrySelector`.

```json
{
    "visible": true,
    "circleSides": 32,
    "defaultBuffer": 60,
    "geometries": ["LineString", "Rectangle", "Circle", "Polygon"],
    "invertGeometry": false,
    "fillColor": "rgba(0, 0, 200, 0.1)",
    "strokeColor": "rgba(255, 0, 0, 1)",
    "strokeWidth": 2
}
```

***

###### portalConfig.secondaryMenu.sections.modules.filter.filterLayer {data-toc-label='Filter Layer'}

[type:Snippets]: # (Datatypes.Snippets)

An object to define a layer to filter with.

| Name                         | Required | Type                                 | Default                              | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Expert |
| ---------------------------- | -------- | ------------------------------------ | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| active                       | no       | Boolean                              | false                                | Set to `true` to let the layer selector be initialy opened. If multiLayerSelector is set to `false` and more than one filter layer has set active to `true`, the last filter layer with active `true` is initialy opened.                                                                                                                                                                                                                                                | false  |
| clearAll                     | no       | Boolean                              | false                                | After clicking button Reset all, all the features will be shown. Set to `true` to clear all the features after clicking Reselt all button.                                                                                                                                                                                                                                                                                                                               | false  |
| collection                   | no       | String                               |                                      | ONLY VectorTiles: The collection to filter. If it is set, the layer needs a `baseOAFUrl` to start the api requests                                                                                                                                                                                                                                                                                                                                                       | false  |
| description                  | no       | String                               | ""                                   | A description of the layer, displayed when the selector is opened. Can be a translation key also.                                                                                                                                                                                                                                                                                                                                                                        | false  |
| download                     | no       | Boolean                              | ""                                   | Enter true for a file here to activate the download of the data filtered on this layer. A download area will appear at the end of the filter. For VectorTiles, only CSV download works.                                                                                                                                                                                                                                                                                  | false  |
| extern                       | no       | Boolean                              | false                                | When set to `true`, filtering is done on the server side. Useful for big sets of data that can't be loaded into the browser at once. Remember to set the **[isNeverVisibleInTree](#layerconfigelementslayersvector)** flag of the layer to `true` to avoid loading of the whole data set by user click on its entry in the tree.                                                                                                                                         | false  |
| filterButtonDisabled         | no       | Boolean                              | false                                | Only for strategy `passive`: Disable the filter button while nothing is selected.                                                                                                                                                                                                                                                                                                                                                                                        | false  |
| filterOnMove                 | no       | Boolean                              |                                      | If it is `true`, the layer will be filtered dynamically after the map moves. Only works with `multiLayerSelector`: `false`. With this combination the filter is triggerd when the accordeon will be opened.                                                                                                                                                                                                                                                              | false  |
| filterOnOpen                 | no       | Boolean                              |                                      | If set to `true`, the filter is triggered when the accorden is clicked.                                                                                                                                                                                                                                                                                                                                                                                                  | false  |
| geometryName                 | no       | String                               | ""                                   | Only for extern `true` in connection with filtering within polygons: The geometry name of the features to be able to detect an intersection.                                                                                                                                                                                                                                                                                                                             | false  |
| icon                         | no       | String                               |                                      | Icon to show in the accordion title. Can be any of **[Bootstrap Icons](https://icons.getbootstrap.com/)**                                                                                                                                                                                                                                                                                                                                                                | false  |
| labelFilterButton            | no       | String                               | "common:modules.filter.filterButton" | If strategy is set to `passive` only: The text of the filter button. Can be a translation key.                                                                                                                                                                                                                                                                                                                                                                           | false  |
| layerId                      | no       | String                               |                                      | The layer id of the layer to filter. Must be configured in the `layerconfig`.                                                                                                                                                                                                                                                                                                                                                                                            | false  |
| maxZoom                      | no       | Number                               |                                      | The maximum zoom level for current filter, if current zoom level is bigger than the maximum zoom level, the current filter will be deactivated.                                                                                                                                                                                                                                                                                                                          | false  |
| minZoom                      | no       | Number                               |                                      | The minimum zoom level for current filter, if current zoom level is smaller than the minimum zoom level, the current filter will be deactivated.                                                                                                                                                                                                                                                                                                                         | false  |
| paging                       | no       | Number                               | 1000                                 | The filter will load features into the map in chunks. Paging is the chunk size. If the chunk size is set too low, the filtering will be slowed down. Set the chunk size too high, the loading of the chunk will slow the filtering down. Try it out to find your fastes setup.                                                                                                                                                                                           | false  |
| resetLayer                   | no       | Boolean                              | false                                | If true it will change the reset button to a button which resets the whole layer and ignores the prechecked values. Will be ignored if `clearAll` is set to `true`. Furthermore, the parameter should not be configured in conjunction with a low `paging` number, otherwise the complete layer will be displayed on the map only very slowly and delayed when resetting.                                                                                                | false  |
| searchInMapExtent            | no       | Boolean                              | false                                | Set to `true` to activate a generic checkbox, where you can set the filtering to `only filter in current browser extent`. If the extent checkbox is checked, automatic zooming is disabled. Make sure to set **[loadingStrategy](#layerconfigelementslayersvector)** to `all` to avoid weird effects when zooming out after filtering in extent. It should also be noted that with `external`:`true` the bbox is not sent with the snippet types `date` and `dateRange`. | false  |
| searchInMapExtentInfo        | no       | Boolean                              | true                                 | A little icon is shown right hand side of the checkbox. Clicking the icon, a standard description is shown. Set to `false` to disable this feature. Set to a individual text to use an own description or use a translation key.                                                                                                                                                                                                                                         | false  |
| searchInMapExtentPreselected | no       | Boolean                              | false                                | The checkbox for filtering in the browser extent is initially selected if `searchInMapExtentPreselected`: `true` is set.                                                                                                                                                                                                                                                                                                                                                 | false  |
| searchInMapExtentProactive   | no       | Boolean                              | true                                 | The checkbox for filtering in the browser extent triggers direct filtering in the current browser extent under `strategy`: `active`. This can be disabled by setting `searchInMapExtentProactive`: `false`.                                                                                                                                                                                                                                                              | false  |
| shortDescription             | no       | String                               | ""                                   | The shorter version of the description, displayed under the selector title. Can be a translation key also.                                                                                                                                                                                                                                                                                                                                                               | false  |
| showHits                     | no       | Boolean                              | true                                 | After filtering, the hits are displayed. Set to `false` to not show the hits.                                                                                                                                                                                                                                                                                                                                                                                            | false  |
| snippets                     | no       | **[Snippets](#datatypessnippets)**[] | []                                   | Configuration of snippets to adjust the filtering. Can be a minimalistic array of attribute names. Can be left empty to use the automatic identification of all snippets possible.                                                                                                                                                                                                                                                                                       | false  |
| strategy                     | no       | String                               |                                      | There are two filter strategies: `passive` - a filter button is used. And `active` - the filter will be triggered immediately by any choice made. Passive strategy is used by default.                                                                                                                                                                                                                                                                                   | false  |
| title                        | no       | String                               |                                      | The title to use for the selector. Can be a translation key also. If not set, the layerId will be used by default.                                                                                                                                                                                                                                                                                                                                                       | false  |
| wmsRefId                     | no       | String/String[]                      | ""                                   | If the layer is filtered, the WMS layer with `wmsRefId` will be invisible and deactivated from Tree. After resetting the layer, the WMS layer will be activated and visible again.                                                                                                                                                                                                                                                                                       | false  |

**Example**

In this example, one snippet is set with only an attrName. The snippet type is detected automatically. See the [snippet datatype](#datatypessnippets) for the advanced configuration of snippets.

```json
{
    "layerId": "8712",
    "title": "Schools",
    "strategy": "active",
    "searchInMapExtent": true,
    "searchInMapExtentInfo": true,
    "showHits": true,
    "clearAll": false,
    "wmsRefId": "21066",
    "shortDescription": "School master data and pupil numbers of Hamburg schools",
    "description": "School master data and pupil numbers of Hamburg schools",
    "paging": 100,
    "filterOnMove": false,
    "minZoom": 7,
    "maxZoom": 14,
    "snippets": [
        {
            "attrName": "rebbz_homepage"
        }
    ]
}
```

***

###### portalConfig.secondaryMenu.sections.modules.filter.filterLayerGroups {data-toc-label='Filter Layer Groups'}
An object to define a group layer to filter with.

| Name            | Required | Type    | Default | Description                                                                                                                                                                                                                                                               | Expert |
| --------------- | -------- | ------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| layers          | no       | String  | []      | Configuration of layers to be filtered. Can be an array of plain layer ids also - if so the layer and all snippets are identified automatically. The type of layers is filterLayer, but here it was defined as string to avoid repetitive definitions within layerGroups. | false  |
| title           | yes      | String  |         | The title to use for the group layer. Can be a translation key also.                                                                                                                                                                                                      | false  |
| collapseButtons | no       | Boolean | false   | If collapseButtons is set to `true`, buttons are displayed instead of accordions.                                                                                                                                                                                         | false  |

**Example**

LayerGroups group related layers. Each group has a title and a list of layers. These are displayed together in the filter.

```json
{
  "layerGroups": [
    {
      "title": "GROUP 1",
      "collapseButtons": true,
      "layers": [
        {
          "layerId": "47"
        },
        {
          "layerId": "7315"
        }
      ]
    },
    {
      "title": "GROUP 2",
      "layers": [
        {
          "layerId": "5105"
        }
      ]
    }
  ]
}
```

***

##### portalConfig.secondaryMenu.sections.modules.language {data-toc-label='Language'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

In this module the language of the portal can be switched.

| Name | Required | Type   | Default                        | Description                                                                                                                           | Expert |
| ---- | -------- | ------ | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| icon | no       | String | "bi-flag"                      | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**. | false  |
| name | no       | String | "common:modules.language.name" | Name of the module in the menu.                                                                                                       | false  |
| type | no       | String | "language"                     | The type of the module. Defines which module is configured.                                                                           | false  |

**Example**

```json
{
    "icon": "bi-flag",
    "name": "common:modules.language.name",
    "type": "language"
}
```

***

##### portalConfig.secondaryMenu.sections.modules.layerClusterToggler {data-toc-label='Layer Cluster Toggler'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

This module allows to activate/load and deactivate layers in clusters simultaneously.

| Name        | Required | Type     | Default                                   | Description                                                                                                                           | Expert |
| ----------- | -------- | -------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| icon        | no       | String   | "bi-list"                                 | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**. | false  |
| layerIdList | yes      | String[] | []                                        | List of layerIds, the layers that should be switched on or off together.                                                              | false  |
| name        | no       | String   | "common:modules.layerClusterToggler.name" | Name of the module in the menu.                                                                                                       | false  |
| type        | no       | String   | "layerClusterToggler"                     | The type of the module. Defines which module is configured.                                                                           | false  |

**Example**

```json
{
    "icon": "bi-list",
    "layerIdList": [
        "8712",,
        "8713.1",
        "8713.2",
        "8713.3"
    ],
    "name": "common:modules.layerClusterToggler.name",
    "type": "layerClusterToggler"
}
```

***

##### portalConfig.secondaryMenu.sections.modules.layerSlider {data-toc-label='Layer Slider'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

The layer slider module allows showing multiple layers in a row. This may e.g. be used to animate a time series of aerial imagery.

The slider can switch between two modes in the interface. Layer slider type. `"player"` shows start, pause, and stop buttons, while `"handle"` uses a switch. In the latter case, layer transparency is adjusted additionally.

| Name         | Required | Type                                                                | Default                            | Description                                                                                                                          | Expert |
| ------------ | -------- | ------------------------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| icon         | no       | String                                                              | "bi-collection-play"               | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)** | false  |
| layerIds     | yes      | **[layerId](#portalconfigmenusectionsmoduleslayersliderlayerid)**[] | []                                 | Array of layer information objects.                                                                                                  | false  |
| name         | no       | String                                                              | "common:modules.layerSlider.name"  | Name of the module in the menu.                                                                                                      | false  |
| timeInterval | no       | Integer                                                             | 2000                               | Time in ms until the next layer is shown.                                                                                            | false  |
| title        | no       | String                                                              | "common:modules.layerSlider.title" | Name displayed in the module.                                                                                                        | false  |
| type         | no       | String                                                              | "layerSlider"                      | The type of the module. Defines which module is configured.                                                                          | false  |

**Example**

```json
"layerSlider": {
    "icon": "bi-hourglass-split",
    "layerIds": [
        {
            "title": "Dienst 1",
            "layerId": "123"
        },
        {
            "title": "Dienst 2",
            "layerId": "456"
        },
        {
            "title": "Dienst 3",
            "layerId": "789"
        }
    ],
    "name": "Time series",
    "timeInterval": 2000,
    "title": "Simulation of Example-WMS"
}
```

***

###### portalConfig.secondaryMenu.sections.modules.layerSlider.layerId {data-toc-label='Layer Id'}
Defines a layer slider layer.

| Name    | Required | Type   | Default | Description                                                                                                   | Expert |
| ------- | -------- | ------ | ------- | ------------------------------------------------------------------------------------------------------------- | ------ |
| layerId | yes      | String |         | ID of the service to be shown in the portal. This layer ID *MUST* be configured as part of the *layerConfig*! | false  |
| title   | yes      | String |         | Service name to be shown in the portal.                                                                       | false  |

**Example**

```json
{
    "layerId": "123",
    "title": "Dienst 1"
}
```

***

###### portalConfig.secondaryMenu.sections.modules.legend {data-toc-label='Legend'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

Legend configuration options.

| Name       | Required | Type   | Default                      | Description                                                                                   | Expert |
| ---------- | -------- | ------ | ---------------------------- | --------------------------------------------------------------------------------------------- | ------ |
| icon       | no       | String | "bi-lightbulb"               | Legend icon.                                                                                  | false  |
| name       | yes      | String | "common:modules.legend.name" | Name of the module in the menu.                                                               | false  |
| type       | no       | String | "legend"                     | The type of the module. Defines which module is configured.                                   | false  |
| sldVersion | no       | String | ""                           | Defines the `Styled Layer Descriptor` Version for the GetLegendGraphic requests, e.g. "1.1.0" | false  |

***

###### portalConfig.secondaryMenu.sections.modules.login {data-toc-label='Login'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

| Name | Required | Type   | Default | Description                                                                                                   | Expert |
| ---- | -------- | ------ | ------- | ------------------------------------------------------------------------------------------------------------- | ------ |
| name | yes      | String |         | The name for the module in the menu. Overwritten when the user is logged in.                                  | false  |
| icon | yes      | String |         | The icon next to the login button in the menu. Will be changed when the user is logged in (see module store). | false  |

```json
{
    "type": "login",
    "name": "common:modules.login.login",
    "icon": "bi-door-open"
}
```

***

##### portalConfig.secondaryMenu.sections.modules.measure {data-toc-label='Measure'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

The measure tool allows measuring distances and areas.

| Name                | Required | Type     | Default                       | Description                                                                                                                                                                                                                                                                                              | Expert |
| ------------------- | -------- | -------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| color               | no       | Number[] | [255, 127, 0, 1.0]            | Defines the color for the measured lines and polygons.                                                                                                                                                                                                                                                   | false  |
| earthRadius         | no       | Number   | 6378137                       | Earth radius in meters. Please mind that the earth radius should be chosen in accordance with the reference ellipsoid. E.g., GRS80 should be used for ETRS89 (EPSG:25832).                                                                                                                               | false  |
| icon                | no       | String   | "bi-arrows-angle-expand"      | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**.                                                                                                                                                                    | false  |
| lineStringUnits     | no       | String[] | ["m", "km"]                   | Indicates which units for length measurements will be selectable by users. Options are "m" (metres), "km" (kilometres), "nm" (nautical miles).                                                                                                                                                           | false  |
| measurementAccuracy | no       | String   | "meter"                       | Indicates how accurately the measurement result is displayed for "m", "nm", "m²", "ha". Options are "decimeter" for one decimal place. "meter" for no decimal place. "dynamic" for one decimal place for results smaller 10 and no decimal place for results greater or equal 10 of the respective unit. | false  |
| name                | no       | String   | "common:modules.measure.name" | Name of the module in the menu.                                                                                                                                                                                                                                                                          | false  |
| polygonUnits        | no       | String[] | ["m²", "km²"]                 | Indicates which units for area measurements will be selectable by users. Options are "m²", "ha", "km²".                                                                                                                                                                                                  | false  |
| type                | no       | String   | "measure"                     | The type of the module. Defines which module is configured.                                                                                                                                                                                                                                              | false  |

**Example**

```json
{
    "earthRadius": 6378137,
    "icon": "bi-arrows-angle-expand",
    "measurementAccuracy": "dynamic",
    "name": "common:modules.measure.name",
    "type": "measure"
}
```

***

##### portalConfig.secondaryMenu.sections.modules.modeler3D {data-toc-label='3D Modeler'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

Can only be used in 3D mode!
The 3D modeler allows to import 3D models in the formats .gltf, .dae and .obj, as well as to draw lines and extrudable 3D polygons.
These drawings can be exported and loaded back georeferenced into the map.

| Name                | Required | Type                                                                          | Default                                                                                    | Description                                                                               | Expert |
| ------------------- | -------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- | ------ |
| gmlIdPath           | no       | String                                                                        | "gmlid"                                                                                    | Specify the path to the GML ID in the GFI for buildings in 3D Layers.                     | false  |
| updateAllLayers     | no       | Boolean                                                                       | true                                                                                       | Specify, if all layers should be updated, when buildings are hidden.                      | false  |
| highlightStyle      | no       | **[highlightStyle](#portalconfigmenusectionsmodulesmodeler3dhighlightstyle)** |                                                                                            | Specify the fill color, alpha, outline color and outline width for highlighting entities. | false  |
| allowedAttributes   | no       | String[]                                                                      | ["Wertbezeichnung", "Gebaeudefunktion"]                                                    | Define which attributes should be available for the filtering function.                   | false  |
| pvoColors           | no       | **[pvoColors](#portalconfigmenusectionsmodulesmodeler3dpvocolors)**           |                                                                                            | Define the colors of the PlanzeichenVerordnung.                                           | false  |
| buildingSource      | no       | String                                                                        | "ALKIS"                                                                                    | Define the source of buildings (currently only ALKIS supported)                           | false  |
| buildingFunctionURL | no       | String                                                                        | "https://repository.gdi-de.org/schemas/adv/citygml/Codelisten/BuildingFunctionTypeAdV.xml" | Define the URL where the building types should be retrieved from.                         | false  |
| type                | yes      | String                                                                        | "modeler3D"                                                                                | The type of the module. Defines which module is configured.                               | false  |

**Example**

```json
{
    "type": "modeler3D",
    "gmlIdPath": "gmlId",
    "updateAllLayers": false,
    "highlightStyle": {
        "silhouetteColor": "#E20D0F",
        "silhouetteSize": 4
    },
    "allowedAttributes": ["Gebaeudefunktion", "Wertbezeichnung"],
        "pvoColors": {
            "housing": "#ff0000",
            "commercial": "#666666",
            "public": "#44ff44"
        },
        "buildingSource": "ALKIS",
        "buildingFunctionURL": "https://repository.gdi-de.org/schemas/adv/citygml/Codelisten/BuildingFunctionTypeAdV.xml"
}
```

***

###### portalConfig.secondaryMenu.sections.modules.modeler3D.highlightStyle  {data-toc-label='highlightStyle'}

| Name            | Required | Type   | Default   | Description                                          | Expert |
| --------------- | -------- | ------ | --------- | ---------------------------------------------------- | ------ |
| silhouetteColor | no       | String | "#E20D0F" | Specify the outline color for highlighting entities. | false  |
| silhouetteSize  | no       | Number | 1         | Specify the outline width for highlighting entities. | false  |

**Example**

```json
{
    "highlightStyle": {
        "silhouetteColor": "#E20D0F",
        "silhouetteSize": 4
    }
}
```

***

###### portalConfig.secondaryMenu.sections.modules.modeler3D.pvoColors {data-toc-label='pvoColors'}

| Name       | Required | Type   | Default   | Description                                   | Expert |
| ---------- | -------- | ------ | --------- | --------------------------------------------- | ------ |
| housing    | no       | String | "#ff0000" | Define the pvo color of housing buildings.    | false  |
| commercial | no       | String | "#666666" | Define the pvo color of commercial buildings. | false  |
| public     | no       | String | "#44ff44" | Define the pvo color of public buildings.     | false  |

**Example**

```json
{
    "pvoColors": {
        "housing": "#ff0000",
        "commercial": "#666666",
        "public": "#44ff44"
    }
}
```

***

##### portalConfig.secondaryMenu.sections.modules.news {data-toc-label='News'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

This module shows all messages from the newsFeedPortalAlerts.json and the config.json of the current portal regardless of the "read" status.

| Name | Required | Type   | Default                    | Description                                                                                                                           | Expert |
| ---- | -------- | ------ | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| icon | no       | String | "bi-newspaper"             | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**. | false  |
| name | no       | String | "common:modules.news.name" | Name of the module in the menu.                                                                                                       | false  |
| type | no       | String | "news"                     | The type of the module. Defines which module is configured.                                                                           | false  |

**Example**

```json
{
    "icon": "bi-newspaper",
    "name": "common:modules.news.name",
    "type": "news"
}
```

***

##### portalConfig.secondaryMenu.sections.modules.openConfig {data-toc-label='Open Config'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

With this module a configuration file (config.json) can be reloaded at runtime. The modules and map are adapted to the new configuration.

| Name | Required | Type   | Default                          | Description                                                                                                                           | Expert |
| ---- | -------- | ------ | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| icon | no       | String | "bi-upload"                      | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**. | false  |
| name | no       | String | "common:modules.openConfig.name" | Name of the module in the menu.                                                                                                       | false  |
| type | no       | String | "openConfig"                     | The type of the module. Defines which module is configured.                                                                           | false  |

**Example**

```json
{
    "icon": "bi-upload",
    "name": "common:modules.openConfig.name",
    "type": "openConfig"
}
```

***

##### portalConfig.secondaryMenu.sections.modules.print {data-toc-label='Print'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

Print module, configurable for 2 print services: *High Resolution PlotService* and *MapfishPrint 3*.

**This requires a backend!**

**A [Mapfish-Print3](https://mapfish.github.io/mapfish-print-doc), or *HighResolutionPlotService* is required as backend.**

| Name                      | Required | Type                                                                              | Default                     | Description                                                                                                                                                                                                          | Expert |
| ------------------------- | -------- | --------------------------------------------------------------------------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| additionalLayers          | no       | **[additionalLayers](#portalconfigmenusectionsmodulesprintadditionallayers)**     |                             | Defines layers that can be added to print.                                                                                                                                                                           | false  |
| capabilitiesFilter        | no       | **[capabilitiesFilter](#portalconfigmenusectionsmodulesprintcapabilitiesfilter)** |                             | Filter for the response of the configured print service. Possible keys are layouts and outputFormats.                                                                                                                | false  |
| currentLayoutName         | no       | String                                                                            | "A4 Hochformat"             | Defines which layout is the default layout on opening the print tool, e.g. "A4 portrait format". If the given layout is not available oder none is provided, the first layout mentioned in the Capabilities is used. | false  |
| defaultCapabilitiesFilter | no       | **[capabilitiesFilter](#portalconfigmenusectionsmodulesprintcapabilitiesfilter)** |                             | If there is no key set in capabilitiesFilter, the key from this object is taken.                                                                                                                                     | false  |
| dpiForPdf                 | no       | Number                                                                            | 200                         | DPI resolution for the map in the PDF file.                                                                                                                                                                          | false  |
| filename                  | no       | String                                                                            | "report"                    | Print result file name.                                                                                                                                                                                              | false  |
| icon                      | no       | String                                                                            | "bi-printer"                | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**.                                                                                | false  |
| isLegendSelected          | no       | Boolean                                                                           | false                       | Defines whether a checkbox to print the legend is offered. Only used for print services supporting legend printing (Mapfish Print 3).                                                                                | false  |
| name                      | no       | String                                                                            | "common:modules.print.name" | Name of the module in the menu.                                                                                                                                                                                      | false  |
| overviewmapLayerId        | no       | String                                                                            |                             | Allows using a different layer for the overview map element. If no Id is specified, the first layer of the selected baselayer maps is used.                                                                          | false  |
| printAppCapabilities      | no       | String                                                                            | "capabilities.json"         | path for the configuration of the print service                                                                                                                                                                      | false  |
| printAppId                | no       | String                                                                            | "master"                    | Print service print app id. This tells the print service which template(s) to use.                                                                                                                                   | false  |
| printMapMarker            | no       | Boolean                                                                           | false                       | If set to true, map markers visible in the print image section will be printed. They may obstruct the view to interesting information.                                                                               | false  |
| printService              | no       | String                                                                            | "mapfish"                   | Flag determining which print service is in use. `plotservice` activates the *High Resolution PlotService*, if the parameter is not set, *Mapfish 3* is used.                                                         | false  |
| printServiceId            | yes      | String                                                                            |                             | Print service id. Resolved using the **[rest-services.json](../Global-Config/rest-services.json.md)** file.                                                                                                          | false  |
| showInvisibleLayerInfo    | no       | Boolean                                                                           | true                        | Defines whether an infobox is shown when layers will not be printed because they are invisible due to scale.                                                                                                         | false  |
| title                     | no       | String                                                                            | "PrintResult"               | Document title appearing as header.                                                                                                                                                                                  | false  |
| transferParameter         | no       | **[transferParameter](#portalconfigmenusectionsmodulesprinttransferparameter)**   | {}                          | Enables the transfer of any number of freely definable parameters. The layout design (JRXML) must then be customized by the user in a meaningful way.                                                                | false  |
| type                      | no       | String                                                                            | "print"                     | The type of the module. Defines which module is configured.                                                                                                                                                          | false  |

**High Resolution PlotService example configuration**

```json
"print": {
    "name": "common:modules.print.name",
    "icon": "bi-printer",
    "type": "print",
    "printServiceId": "123456",
    "filename": "Ausdruck",
    "title": "Mein Titel",
    "printService": "plotservice",
    "printAppCapabilities": "info.json",
    "layoutOrder": [
        "Default A4 hoch",
        "Default A4 quer",
        "Default A3 hoch",
        "Default A3 quer",
    ]
}
```

**MapfishPrint3 example configuration**

```json
"print": {
    "name": "Karte drucken",
    "icon": "bi-printer",
    "type": "print",
    "printServiceId": "mapfish_printservice_id",
    "printAppId": "mrh",
    "filename": "Ausdruck",
    "title": "Mein Titel"
}
```
***

###### portalConfig.secondaryMenu.sections.modules.print.transferParameter {data-toc-label='Print Transfer-Parameter'}
Object with parameters.

| Name              | Required | Type   | Default | Description        | Expert |
| ----------------- | -------- | ------ | ------- | ------------------ | ------ |
| exampleParameter1 | no       | String | ""      | Contains parameter | false  |


```json title="Example additionalLayers"
"transferParameter": {
        "exampleParameter1": "example placeholder",
        "exampleParameter2": "example placeholder 2"
    }
```

***

###### portalConfig.secondaryMenu.sections.modules.print.additionalLayers {data-toc-label='Print additionalLayers'}
List of Layers that can be added to the print document.

| Name   | Required | Type    | Default | Description                                | Expert |
| ------ | -------- | ------- | ------- | ------------------------------------------ | ------ |
| active | no       | Boolean | false   | Defines if the layer is active.            | false  |
| id     | yes      | String  |         | Service-ID of the layer.                   | false  |
| label  | yes      | String  |         | Label of the checkbox in the print dialog. | false  |


```json title="Example additionalLayers"
"additionalLayers": [{
  "id": "wms_coord_grid_25832",
  "label": "Coordinate Grid UTM32N - ETRS89"
}]
```

***

###### portalConfig.secondaryMenu.sections.modules.print.capabilitiesFilter {data-toc-label='Capabilities Filter'}
List of layouts and formats that filters the response from the print service in the respective category.

| Name          | Required | Type     | Default | Description                              | Expert |
| ------------- | -------- | -------- | ------- | ---------------------------------------- | ------ |
| layouts       | no       | String[] |         | Array of layouts should shown in the UI. | false  |
| outputFormats | no       | String[] |         | Array of formats should shown in the UI. | false  |

**Example capabilitiesFilter:**

```json
"capabilitiesFilter": {
    "layouts": ["A4 Hochformat", "A3 Hochformat"],
    "outputFormats": ["PDF"]
}
```

***
###### portalConfig.secondaryMenu.sections.modules.print.transferParameter {data-toc-label='Transfer Parameter'}
Any number of parameters that can be passed to MapFish. `exampleParameter` is just an example.
Any names can be chosen for the variables, and they can contain any values of type string.

| Name              | Required | Type   | Default | Description                | Expert |
| ----------------- | -------- | ------ | ------- | -------------------------- | ------ |
| exampleParameter1 | nein     | String |         | Beispiel für einen String. | false  |
| exampleParameter2 | nein     | String |         | Beispiel für einen String. | false  |

**Beispiel transferParameter:**
```json
"transferParameter": {
        "exampleParameter1": "example placeholder",
        "exampleParameter2": "example placeholder 2"
    }
```

***

#### portalConfig.secondaryMenu.sections.modules.compareFeatures {data-toc-label='Compare Features'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

This tool allows comparing vector features which are provided by WFS(❗) services.

| Name                     | Required | Type    | Default                               | Description                                                                                                                                                          | Expert |
| ------------------------ | -------- | ------- | ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| icon                     | no       | String  | "bi-star"                             | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**.                                | false  |
| name                     | no       | String  | "common:modules.compareFeatures.name" | Name of the module in the menu.                                                                                                                                      | false  |
| numberOfAttributesToShow | no       | Integer | 12                                    | Deprecated in next major release. Maximum amount of attributes initially shown. If more attributes are available, they can be shown and hidden by clicking a button. | false  |
| numberOfFeaturesToShow   | no       | Integer | 3                                     | Deprecated in next major release. Maximum amount of features selectable for comparison.                                                                              | false  |
| type                     | no       | String  | "compareFeatures"                     | The type of the module. Defines which module is configured.                                                                                                          | false  |


**Example**

```json
"compareFeatures": {
    "icon": "bi-star",
    "name": "common:modules.compareFeatures.title",
    "numberOfAttributesToShow": 10,
    "numberOfFeaturesToShow": 5,
    "type": "compareFeatures"
}
```

***

##### portalConfig.secondaryMenu.sections.modules.routing {data-toc-label='Routing'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

Routing module. Enables user to plan routes between multiple points with multiple options to choose from. In addition users can create isochrones. Both functions are available with mass requests for specific use cases. ❗ This tool will use the routing service provided by the BKG ❗.

| Name                    | Required | Type                                                                                | Default      | Description                                                        | Expert |
| ----------------------- | -------- | ----------------------------------------------------------------------------------- | ------------ | ------------------------------------------------------------------ | ------ |
| activeRoutingToolOption | no       | String                                                                              | "DIRECTIONS" | Which routing tool should be open.                                 | false  |
| routingToolOptions      | no       | String[]                                                                            | [ ]          | Which routing tool should be enabled. ("DIRECTIONS", "ISOCHRONES") | false  |
| download                | no       | **[download](#portalconfigmenusectionsmodulesroutingdownload)**                     |              | Downloadoptions                                                    | false  |
| geosearch               | no       | **[geosearch](#portalconfigmenusectionsmodulesroutinggeosearch)**                   |              | Geosearchoptions                                                   | false  |
| geosearchReverse        | no       | **[geosearchReverse](#portalconfigmenusectionsmodulesroutinggeosearchreverse)**     |              | Geosearchreverseoptions                                            | false  |
| directionsSettings      | no       | **[directionsSettings](#portalconfigmenusectionsmodulesroutingdirectionssettings)** |              | Directionsoptions                                                  | false  |
| isochronesSettings      | no       | **[isochronesSettings](#portalconfigmenusectionsmodulesroutingisochronessettings)** |              | Isochronesoptions                                                  | false  |
| tsrSettings             | no       | **[tsrSettings](#portalconfigmenusectionsmodulesroutingtsrsettings)**               |              | Travelling Salesman Routing options                                | false  |


**Example**

```json
{
    "type": "routing",
    "name": "common:modules.routing",
    "icon": "bi-signpost-2",
    "activeRoutingToolOption": "DIRECTIONS",
    "routingToolOptions": ["DIRECTIONS", "ISOCHRONES"],
    "download": {
        "filename": "",
        "format": "GEOJSON"
    },
    "geosearch": {
        "minChars": 3,
        "limit": 10,
        "type": "BKG",
        "serviceId": "bkg_geosearch"
    },
    "geosearchReverse": {
        "distance": 1000,
        "filter": "",
        "type": "BKG",
        "serviceId": "bkg_suggest"
    },
    "directionsSettings": {
        "type": "ORS",
        "serviceId": "bkg_ors",
        "speedProfile": "CAR",
        "preference": "RECOMMENDED",
        "styleRoute": {
            "fillColor": [255, 44, 0],
            "width": 6,
            "highlightColor": [255, 255, 255],
            "highlightWidth": 9,
            "partHighlightColor": [255, 255, 255],
            "partHighlightWidth": 3
        },
        "styleWaypoint": {
            "lineColor": [255, 127, 0],
            "lineWidth": 4,
            "fillColor": [255, 127, 0],
            "textFillColor": "#000",
            "textLineColor": "#fff",
            "textLineWidth": 3,
            "opacity": 0.3,
            "radius": 8
        },
        "styleAvoidAreas": {
            "lineColor": [0, 127, 255],
            "lineWidth": 2,
            "fillColor": [0, 127, 255],
            "opacity": 0.3,
            "pointRadius": 8,
            "pointLineWidth": 4
        },
        "batchProcessing": {
            "enabled": false,
            "active": false,
            "limit": 1000,
            "maximumConcurrentRequests": 3
        }
    },
    "isochronesSettings": {
        "type": "ORS",
        "serviceId": "bkg_ors",
        "speedProfile": "CAR",
        "isochronesMethodOption": "TIME",
        "distanceValue": 30,
        "minDistance": 1,
        "maxDistance": 400,
        "timeValue": 30,
        "minTime": 1,
        "maxTime": 180,
        "intervalValue": 15,
        "minInterval": 3,
        "maxInterval": 30,
        "styleCenter": {
            "lineColor": [255, 127, 0],
            "lineWidth": 4,
            "fillColor": [255, 127, 0],
            "opacity": 0.3,
            "radius": 8
        },
        "styleIsochrones": {
            "lineWidth": 2,
            "opacity": 0.65,
            "startColor": [66, 245, 78],
            "endColor": [245, 66, 66]
        },
        "batchProcessing": {
            "enabled": false,
            "active": false,
            "limit": 1000,
            "maximumConcurrentRequests": 3
        },
        "attributes": ["area", "total_pop"],
        "areaUnit": "km"
    },
    "tsrSettings": {
        "type": "TSR",
        "serviceId": "bkg_tsr",
        "speedProfile": "CAR",
        "elevation": true,
        "tsrPointLimit": 50,
        "styleRoute": {
        "fillColor": [50, 169, 232, 1.0]
        }
    }
}
```

***

###### portalConfig.secondaryMenu.sections.modules.routing.download {data-toc-label='Download'}
Routing-tool download options.

| Name     | Required | Type                        | Default   | Description                                 | Expert |
| -------- | -------- | --------------------------- | --------- | ------------------------------------------- | ------ |
| fileName | no       | String                      | ""        | Default filename for the download.          | false  |
| format   | no       | enum["GEOJSON","KML","GPX"] | "GEOJSON" | Which format should be selected by default. | false  |

**Example**

```json
{
    "download": {
        "filename": "",
        "format": "GEOJSON"
    }
}
```

***

###### portalConfig.secondaryMenu.sections.modules.routing.geosearch {data-toc-label='Geosearch'}

[type:Bbox]: # (Datatypes.Bbox)

Routing-tool geosearch options.

| Name          | Required | Type                                                                                 | Default | Description                                                                                                                            | Expert |
| ------------- | -------- | ------------------------------------------------------------------------------------ | ------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| minChars      | no       | Number                                                                               | 3       | Minimum amount of characters before sending a request to an external service.                                                          | false  |
| limit         | no       | Number                                                                               | 10      | Maximale amount of characters for the search.                                                                                          | false  |
| type          | yes      | enum["BKG","NOMINATIM","LOCATIONFINDER","KOMOOT","GAZETTEER","SPECIALWFS","ELASTIC"] | ""      | Which type of the geosearch should be used.                                                                                            | false  |
| serviceId     | yes      | String                                                                               |         | Which service should be used for the geosearch.                                                                                        | false  |
| typeName      | no       | String                                                                               |         | Type name for the specialWfs geosearch query.                                                                                          | false  |
| propertyNames | no       | String[]                                                                             |         | Names of properties to be included in the specialWfs geosearch.                                                                        | false  |
| geometryNames | no       | String                                                                               |         | Name of the geometry field for specialWfs geosearch.                                                                                   | false  |
| bbox          | no       | **[Bbox](#datatypesbbox)**                                                           |         | BBOX value according to the speedProfile. Coordinate system depends on the epsg parameter. Geosearch service must support bbox string. | false  |
| epsg          | no       | String                                                                               | 4326    | Which EPSG code is used by the service (e.g. 4326, 25832).                                                                             | false  |
| searchField   | no       | String                                                                               |         | The path to the field to be searched for when using Elastic Search.                                                                    | false  |
| sortField     | no       | String                                                                               |         | The path to the field that specifies the sorting of the results in ascending order when using Elastic Search.                          | false  |

**Example for BKG**

```json
{
    "geosearch": {
        "type": "BKG",
        "serviceId": "bkg_geosearch",
        "bbox": {"CYCLING": "9.6,53.40,10.4,53.84"}
    }
}
```
**Example for SPECIALWFS**

```json
{
    "geosearch": {
        "minChars": 3,
        "limit": 10,
        "type": "SPECIALWFS",
        "serviceId": "specialWfs_geosearch",
        "typeName": "ms:strasse_nr",
        "propertyNames": [
            "ms:LABEL_TEXT"
            ],
        "geometryName": "ms:msGeometry"
    }
}
```
**Example for ELASTIC**

```json
{
    "geosearch": {
        "minChars": 3,
        "limit": 10,
        "type": "ELASTIC",
        "serviceId": "elastic_geosearch",
        "epsg": "25832",
        "searchField": "properties.searchField",
        "sortField": "properties.HAUSNUMMER"
    }
}
```

***

###### portalConfig.secondaryMenu.sections.modules.routing.geosearchReverse {data-toc-label='Geosearch Reverse'}
Routing-tool geosearch reverse options.

| Name      | Required | Type                             | Default | Description                                             | Expert |
| --------- | -------- | -------------------------------- | ------- | ------------------------------------------------------- | ------ |
| distance  | no       | Number                           | 1000    | Search radius in meter for the external service.        | false  |
| filter    | no       | String                           |         | Additional filter used in the query.                    | false  |
| type      | yes      | enum["BKG","NOMINATIM","KOMOOT"] |         | Which type of geosearch reverse should be used.         | false  |
| serviceId | yes      | String                           |         | Which service should be used for the geosearch reverse. | false  |

**Example**

```json
{
    "geosearchReverse": {
        "distance": 1000,
        "filter": "",
        "type": "BKG",
        "serviceId": "bkg_suggest"
    }
}
```

***

###### portalConfig.secondaryMenu.sections.modules.routing.directionsSettings {data-toc-label='Directions Settings'}

[type:BatchProcessing]: # (Datatypes.BatchProcessing)
[type:StyleAvoidAreas]: # (Datatypes.StyleAvoidAreas)
[type:StyleWaypoint]: # (Datatypes.StyleWaypoint)
[type:StyleRoute]: # (Datatypes.StyleRoute)
[type:CustomPreferences]: # (Datatypes.CustomPreferences)
[type:CustomAvoidFeatures]: # (Datatypes.CustomAvoidFeatures)

Routing-tool directions options.

| Name                | Required | Type                                                     | Default       | Description                                                                                                                                                  | Expert |
| ------------------- | -------- | -------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| type                | yes      | enum["ORS"]                                              |               | Which type of service should be used for the request.                                                                                                        | false  |
| serviceId           | yes      | String                                                   |               | Which service should be used for the request.                                                                                                                | false  |
| speedProfile        | no       | String                                                   | "CAR"         | Which speed profile should be selected by default.                                                                                                           | false  |
| preference          | no       | String                                                   | "RECOMMENDED" | Which type of directions should be used by default.                                                                                                          | false  |
| elevation           | no       | Boolean                                                  | false         | Possibility to activate the elevation profile of the route.                                                                                                  | false  |
| customPreferences   | no       | **[CustomPreferences](#datatypescustompreferences)**     |               | Possibility to define additional preferences for the different speed profiles (additionally to the BKG service)  (requires own modified backend)             | false  |
| customAvoidFeatures | no       | **[CustomAvoidFeatures](#datatypescustomavoidfeatures)** |               | Possibility to define own options for avoid traffic routes for the different speed profiles(additionally to the BKG service) (requires own modified backend) | false  |
| styleRoute          | no       | **[StyleRoute](#datatypesstyleroute)**                   |               | Stylerouteoptions                                                                                                                                            | false  |
| styleWaypoint       | no       | **[StyleWaypoint](#datatypesstylewaypoint)**             |               | Stylewaypointoptions                                                                                                                                         | false  |
| styleAvoidAreas     | no       | **[StyleAvoidAreas](#datatypesstyleavoidareas)**         |               | Styleavoidareasoptions                                                                                                                                       | false  |
| batchProcessing     | no       | **[BatchProcessing](#datatypesbatchprocessing)**         |               | Batchprocessingoptions                                                                                                                                       | false  |

**Example**

```json
{
    "directionsSettings": {
        "type": "ORS",
        "serviceId": "bkg_ors",
        "speedProfile": "CAR",
        "preference": "RECOMMENDED",
        "elevation": true,
        "customPreferences": {
            "CYCLING": ["RECOMMENDED", "SHORTEST", "GREEN"]
        },
        "customAvoidFeatures": {
                "CYCLING": ["STEPS", "FERRIES", "UNPAVEDROADS"]
        },
        "styleRoute": {
            "fillColor": [255, 44, 0, 1],
            "width": 6,
            "highlightColor": [255, 255, 255, 1],
            "highlightWidth": 9,
            "partHighlightColor": [255, 255, 255, 1],
            "partHighlightWidth": 3
        },
        "styleWaypoint": {
            "lineColor": [255, 127, 0],
            "lineWidth": 4,
            "fillColor": [255, 127, 0],
            "textFillColor": "#000",
            "textLineColor": "#fff",
            "textLineWidth": 3,
            "opacity": 0.3,
            "radius": 8
        },
        "styleAvoidAreas": {
            "lineColor": [0, 127, 255],
            "lineWidth": 2,
            "fillColor": [0, 127, 255],
            "opacity": 0.3,
            "pointRadius": 8,
            "pointLineWidth": 4
        },
        "batchProcessing": {
            "enabled": false,
            "active": false,
            "limit": 1000,
            "maximumConcurrentRequests": 3
        }
    }
}
```

***

###### portalConfig.secondaryMenu.sections.modules.routing.isochronesSettings {data-toc-label='Isochrones Settings'}

[type:BatchProcessing]: # (Datatypes.BatchProcessing)
[type:StyleCenter]: # (Datatypes.StyleCenter)
[type:StyleIsochrones]: # (Datatypes.StyleIsochrones)

Routing-tool isochrones options.

| Name                   | Required | Type                                             | Default | Description                                                  | Expert |
| ---------------------- | -------- | ------------------------------------------------ | ------- | ------------------------------------------------------------ | ------ |
| type                   | yes      | enum["ORS"]                                      |         | Which type of service should be used for the request.        | false  |
| serviceId              | yes      | String                                           |         | Which service should be used for the request.                | false  |
| speedProfile           | no       | String                                           | "CAR"   | Which speed profile should be selected by default.           | false  |
| isochronesMethodOption | no       | String                                           | "TIME"  | Which method should be selected by default.                  | false  |
| distanceValue          | no       | Number                                           | 30      | Which distance value in km should be selected by default.    | false  |
| minDistance            | no       | Number                                           | 1       | Which minimal distance value in km should be used.           | false  |
| maxDistance            | no       | Number                                           | 400     | Which maximum distance value in km should be used.           | false  |
| timeValue              | no       | Number                                           | 30      | Which time value in min should be selected by default.       | false  |
| minTime                | no       | Number                                           | 1       | Which minimal time value in min should be used.              | false  |
| maxTime                | no       | Number                                           | 180     | Which maximum time in min should be used.                    | false  |
| intervalValue          | no       | Number                                           | 15      | Which interval value in km/min should be used by default.    | false  |
| minInterval            | no       | Number                                           | 1       | Which minimal interval value in km/min should be used.       | false  |
| maxInterval            | no       | Number                                           | 30      | Which maximum interval value in km/min should be used.       | false  |
| styleCenter            | no       | **[StyleCenter](#datatypesstylecenter)**         |         | Stylecenteroptions                                           | false  |
| styleIsochrones        | no       | **[StyleIsochrones](#datatypesstyleisochrones)** |         | Styleisochronesoptions                                       | false  |
| batchProcessing        | no       | **[BatchProcessing](#datatypesstyleisochrones)** |         | Batchprocessingoptions                                       | false  |
| attributes             | no       | String[]                                         | []      | Which additional attributes should be considered in request. | false  |
| areaUnit               | no       | enum["m","km","mi"]                              | "km"    | Which unit is used for area attribute.                       | false  |

**Example**

```json
{
    "isochronesSettings": {
        "type": "ORS",
        "serviceId": "bkg_ors",
        "speedProfile": "CAR",
        "isochronesMethodOption": "TIME",
        "distanceValue": 30,
        "minDistance": 1,
        "maxDistance": 400,
        "timeValue": 30,
        "minTime": 1,
        "maxTime": 180,
        "intervalValue": 15,
        "minInterval": 3,
        "maxInterval": 30,
        "styleCenter": {
            "lineColor": [255, 127, 0],
            "lineWidth": 4,
            "fillColor": [255, 127, 0],
            "opacity": 0.3,
            "radius": 8
        },
        "styleIsochrones": {
            "lineWidth": 2,
            "opacity": 0.65,
            "startColor": [66, 245, 78],
            "endColor": [245, 66, 66]
        },
        "batchProcessing": {
            "enabled": false,
            "active": false,
            "limit": 1000,
            "maximumConcurrentRequests": 3
        },
        "attributes": ["area", "total_pop"],
        "areaUnit": "km"
    }
}
```
***

#### portalConfig.secondaryMenu.sections.modules.routing.tsrSettings {data-toc-label='TSR Settings'}

[type:StyleRoute]: # (Datatypes.StyleRoute)

TSR-tool options.

| Name          | Required | Type                                   | Default | Description                                                 | Expert |
| ------------- | -------- | -------------------------------------- | ------- | ----------------------------------------------------------- | ------ |
| type          | yes      | enum["TSR"]                            |         | Which type of service should be used for the request.       | false  |
| serviceId     | yes      | String                                 |         | Which service should be used for the request.               | false  |
| speedProfile  | no       | String                                 | "CAR"   | Which speed profile should be selected by default.          | false  |
| elevation     | no       | Boolean                                | false   | Possibility to activate the elevation profile of the route. | false  |
| tsrPointLimit | no       | Number                                 | 50      | Limit of TSR points                                         | false  |
| styleRoute    | no       | **[StyleRoute](#datatypesstyleroute)** |         | Stylerouteoptions                                           | false  |


**Example**

```json
{
    "tsrSettings": {
        "type": "TSR",
        "serviceId": "bkg_tsr",
        "speedProfile": "CAR",
        "elevation": true,
        "tsrPointLimit": 50,
        "styleRoute": {
            "fillColor": [50, 169, 232, 1.0]
        }
    }
}
```

***

##### portalConfig.secondaryMenu.sections.modules.scaleSwitcher {data-toc-label='Scale Switcher'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

Module that allows changing the map's current scale.

| Name | Required | Type   | Default                             | Description                                                                                                                           | Expert |
| ---- | -------- | ------ | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| icon | no       | String | "bi-arrows-angle-contract"          | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**. | false  |
| name | no       | String | "common:modules.scaleSwitcher.name" | Name of the module in the menu.                                                                                                       | false  |
| type | no       | String | "scaleSwitcher"                     | The type of the module. Defines which module is configured.                                                                           | false  |

**Example**

```json
{
    "icon": "bi-arrows-angle-contract",
    "name": "common:modules.scaleSwitcher.name",
    "type": "scaleSwitcher"
}
```

***

##### portalConfig.secondaryMenu.sections.modules.selectFeatures {data-toc-label='Select Features'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

Allows selecting a set of vector features by letting the user draw a box on the map. Features in that box will be displayed with GFI information and it's possible to zoom to a feature. This tool requires WFS(❗) layers.

| Name                          | Required | Type                                                                                                             | Default                              | Description                                                                                                                                        | Expert |
| ----------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| highlightVectorRulesPointLine | no       | **[highlightVectorRulesPointLine](#portalconfigmenusectionsmodulesselectfeatureshighlightvectorrulespointline)** |                                      | Specify outline color and stroke width for highlighting lines and fill color and scale factor for highlighting points as well as a zoom parameter. | false  |
| highlightVectorRulesPolygon   | no       | **[highlightVectorRulesPolygon](#portalconfigmenusectionsmodulesselectfeatureshighlightvectorrulespolygon)**     |                                      | Specify the fill color and outline color and stroke width for highlighting the polygon features as well as a zoom parameter.                       | false  |
| icon                          | no       | String                                                                                                           | "bi-hand-index"                      | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**.              | false  |
| name                          | no       | String                                                                                                           | "common:modules.selectFeatures.name" | Name of the module in the menu.                                                                                                                    | false  |
| type                          | no       | String                                                                                                           | "selectFeatures"                     | The type of the module. Defines which module is configured.                                                                                        | false  |

**Example**

```json
{
    "type": "selectFeatures",
    "highlightVectorRulesPolygon": {
        "fill": {
            "color": [255, 0, 255, 0.9]
        },
        "stroke": {
            "width": 4,
            "color": [0, 0, 204, 0.9]
        },
        "zoomLevel": 5
    },
    "highlightVectorRulesPointLine": {
        "fill": {
            "color": [255, 0, 255, 0.9]
        },
        "stroke": {
            "width": 8,
            "color": [255, 0, 255, 0.9]
        },
        "image": {
            "scale": 2
        },
        "zoomLevel": 5
    }
}
```

***

###### portalConfig.secondaryMenu.sections.modules.selectFeatures.highlightVectorRulesPointLine {data-toc-label='Highlight Vector Rules Point Line'}

[type:Image]: # (Datatypes.Image)
[type:Fill]: # (Datatypes.Fill)
[type:Stroke]: # (Datatypes.Stroke)

Specify outline color and stroke width for highlighting lines and fill color and scale factor for highlighting points. Also a zoom level.

| Name      | Required | Type                           | Default              | Description                       | Expert |
| --------- | -------- | ------------------------------ | -------------------- | --------------------------------- | ------ |
| fill      | no       | **[Fill](#datatypesfill)**     | [255, 255, 255, 0.5] | Possible setting: color           | false  |
| stroke    | no       | **[Stroke](#datatypesstroke)** | 1.5                  | Possible setting: width and color | false  |
| image     | no       | **[Image](#datatypesimage)**   | 1                    | Possible setting: scale           | false  |
| zoomLevel | no       | Integer                        | 7                    | Zoom level, possible setting: 0-9 | false  |

***

###### portalConfig.secondaryMenu.sections.modules.selectFeatures.highlightVectorRulesPolygon {data-toc-label='Highlight Vector Rules Polygon'}

[type:Fill]: # (Datatypes.Fill)
[type:Stroke]: # (Datatypes.Stroke)

Specify the fill color and stroke width for highlighting the polygon features as well as a zoom level.

| Name      | Required | Type                           | Default              | Description                       | Expert |
| --------- | -------- | ------------------------------ | -------------------- | --------------------------------- | ------ |
| fill      | no       | **[Fill](#datatypesfill)**     | [255, 255, 255, 0.5] | Possible setting: color           | false  |
| stroke    | no       | **[Stroke](#datatypesstroke)** | 1                    | Possible setting: width           | false  |
| zoomLevel | no       | Integer                        | 7                    | Zoom level, possible setting: 0-9 | false  |

***

##### portalConfig.secondaryMenu.sections.modules.shadow {data-toc-label='Shadow'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

The shadow tool provides a UI element to define a point in time by using sliders and date pickers. The chosen time allows rendering the shadows of all 3D objects in 3D mode by simulating the sun's position. By pulling the sliders or selecting a different date, a new sun position is calculated immediately. By default, the tool starts with the current time, which can be overwritten in the parameters.

| Name            | Required | Type                                                               | Default                      | Description                                                                                                                           | Expert |
| --------------- | -------- | ------------------------------------------------------------------ | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| icon            | no       | String                                                             | "bi-lamp-fill"               | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**. | false  |
| isShadowEnabled | no       | Boolean                                                            | false                        | Default shadow value. `true` immediately renders shadows, `false` requires a manual confirmation.                                     | false  |
| name            | no       | String                                                             | "common:modules.shadow.name" | Name of the module in the menu.                                                                                                       | false  |
| shadowTime      | no       | **[shadowTime](#portalconfigmenusectionsmodulesshadowshadowtime)** |                              | Default time the mdoule is started with. Recognizes "month", "day", "hour", and "minute".                                             | false  |
| type            | no       | String                                                             | "shadow"                     | The type of the module. Defines which module is configured.                                                                           | false  |

**Example**

```json
{
    "isShadowEnabled": true,
    "shadowTime": {
        "month": "6",
        "day": "20",
        "hour": "13",
        "minute": "0"
    },
    "type": "shadow"
}
```

***

###### portalConfig.secondaryMenu.sections.modules.shadow.shadowTime {data-toc-label='Shadow Time'}

| Name   | Required | Type   | Default | Description | Expert |
| ------ | -------- | ------ | ------- | ----------- | ------ |
| month  | no       | String |         | month       | false  |
| day    | no       | String |         | day         | false  |
| hour   | no       | String |         | hour        | false  |
| minute | no       | String |         | minute      | false  |

**Example**

```json
{
    "month": "6",
    "day": "20",
    "hour": "13",
    "minute": "0"
}
```

***

##### portalConfig.secondaryMenu.sections.modules.statisticDashboard {data-toc-label='Statistic Dashboard'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

| Name                     | Required | Type                                                                                                     | Default                                                    | Description                                                                                   | Expert |
| ------------------------ | -------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------ |
| name                     | yes      | String                                                                                                   | "common:menu.statisticDashboard"                           | The Name of the Tool.                                                                         | false  |
| subtitle                 | no       | String                                                                                                   | "common:modules.statisticDashboard.headings.mrhstatistics" | The subtitle to display                                                                       | false  |
| icon                     | no       | String                                                                                                   | "bi-speedometer"                                           | The icon of the Tool                                                                          | false  |
| colorScheme              | yes      | **[colorScheme](#portalconfigmenusectionsmodulesstatisticdashboardcolorscheme)**                         | ""                                                         | Defines the colours of the features in statisticdashboard.                                    | false  |
| active                   | no       | Boolean                                                                                                  | false                                                      | If `true`, the tool is open after initializing the portal.                                    | false  |
| data                     | yes      | **[data](#portalconfigmenusectionsmodulesstatisticdashboarddata)**                                       | ""                                                         | data for statistic dashboard.                                                                 | false  |
| classificationMode       | no       | String                                                                                                   | "quantiles"                                                | Method for dividing values into classes: "quantiles", "equalIntervals" or "benutzerdefiniert" | false  |
| decimalPlaces            | no       | Number                                                                                                   | 2                                                          | Number of decimal places for statistical values.                                              | false  |
| allowPositiveNegativeMix | no       | Boolean                                                                                                  | false                                                      | If classification method is allowed to create classes like "from -1 to 1".                    | false  |
| minNumberOfClasses       | no       | Number                                                                                                   | 2                                                          | Minimum selectable number of classes for choropleth map and legend. At least 2.               | false  |
| maxNumberOfClasses       | no       | Number                                                                                                   | 5                                                          | Maximum selectable number of classes for choropleth map and legend. At least 3.               | false  |
| numberOfClasses          | no       | Number                                                                                                   | 5                                                          | Current selected number of classes.                                                           | false  |
| selectableColorPalettes  | no       | **[selectableColorPalettes](#portalconfigmenusectionsmodulesstatisticdashboardselectablecolorpalettes)** | []                                                         | Available options for color palettes                                                          | false  |
| downloadFilename         | no       | String                                                                                                   | "Statistic Dashboard Download"                             | The filename of the exported csv file.                                                        | false  |

**Example**

```json
{
    "name": "common:menu.statisticDashboard",
    "subtitle": "common:modules.statisticDashboard.headings.mrhstatistics",
    "icon": "bi-speedometer",
    "downloadFilename": "Downloaded_Data",
    "colorScheme": {
        "referenceRegion": [155, 155, 155, 0.7],
        "lineCharts": [[74, 0, 30, 1], [117, 18, 50, 1], [189, 47, 83, 1], [198, 81, 84, 1], [228, 121, 97, 1], [240, 168, 130, 1], [250, 212, 172, 1], [157, 185, 171, 1], [137, 192, 196, 1], [87, 158, 185, 1],
            [57, 122, 168, 1], [28, 87, 150, 1], [22, 55, 113, 1], [16, 25, 77, 1], [118, 199, 190, 1], [62, 168, 166, 1], [32, 130, 136, 1], [0, 73, 75, 1], [224, 110, 133, 1], [204, 65, 90, 1]]
    },
    "active": true,
    "data": {
        "layerId": "28992",
        "geometryAttribute": "geom",
        "chartDirectionValue": 10,
        "timeStepsFilter": {
            "5": "Die letzten 5 Jahre",
            "10": "Die letzten 10 Jahre",
            "all": "Alle Jahre"
        },
        "mappingFilter": {
            "timeAttribute": {
                "attrName": "zeitpunkt",
                "name": "Zeitpunkt",
                "inputFormat": "YYYY-MM-DD",
                "outputFormat": "YYYY"
            },
            "regionNameAttribute": {
                "attrName": "statistisches_gebiet",
                "name": "Statistisches Gebiet"
            },
            "statisticsAttributes": {
                "arbeitnehmer_inland_tausend": {
                    "name": "Arbeitnehmer (Inland) in 1.000",
                    "category": "Beschäftigte"
                },
                "arbeitslose_jahresdurchschnitt": {
                    "name": "Arbeitslose",
                    "category": "Beschäftigte"
                },
                "arbeitslose_15_bis_u25_jahresdurchschnitt": {
                    "name": "Arbeitslose 15 bis unter 25 Jahre",
                    "category": "Beschäftigte"
                },
                "einwohner_ab_65": {
                    "name": "Einwohner 65 Jahre und älter",
                    "category": "Bevölkerung"
                },
                "einwohner_ab_65_prozent_aller_einwohner": {
                    "name": "Einwohner 65 Jahre und älter in % aller Einwohner",
                    "category": "Bevölkerung"
                },
                "einwohner_auslaender": {
                    "name": "Einwohner Ausländer",
                    "category": "Bevölkerung"
                }
            }
        }
    }
}
```

***

###### portalConfig.secondaryMenu.sections.modules.statisticDashboard.colorScheme {data-toc-label='Color Scheme'}

| Name            | Required | Type    | Default | Description                                    | Expert |
| --------------- | -------- | ------- | ------- | ---------------------------------------------- | ------ |
| referenceRegion | yes      | Float[] | []      | The RGBA color of the Reference region.        | false  |
| lineCharts      | yes      | Float[] | []      | The list of the RGBA colors of the linecharts. | false  |

**Example**

```json
{
        "referenceRegion": [155, 155, 155, 0.7],
        "lineCharts": [[74, 0, 30, 1], [117, 18, 50, 1], [189, 47, 83, 1], [198, 81, 84, 1], [228, 121, 97, 1], [240, 168, 130, 1], [250, 212, 172, 1], [157, 185, 171, 1], [137, 192, 196, 1], [87, 158, 185, 1],
            [57, 122, 168, 1], [28, 87, 150, 1], [22, 55, 113, 1], [16, 25, 77, 1], [118, 199, 190, 1], [62, 168, 166, 1], [32, 130, 136, 1], [0, 73, 75, 1], [224, 110, 133, 1], [204, 65, 90, 1]]
}
```

***

###### portalConfig.secondaryMenu.sections.modules.statisticDashboard.selectableColorPalettes {data-toc-label='Selectable Color Palettes'}

| Name      | Required | Type     | Default | Description                              | Expert |
| --------- | -------- | -------- | ------- | ---------------------------------------- | ------ |
| label     | yes      | String   |         | The displayed name of the color palette. | false  |
| baseColor | yes      | Number[] |         | The base color as an rgb array           | false  |

**Example**

```json
[
        {
            "label": "Blau",
            "key": "Blues"
        }
]
```

***

###### portalConfig.secondaryMenu.sections.modules.statisticDashboard.data {data-toc-label='Data'}

| Name                  | Required | Type                                                                                         | Default | Description                                                                                                                                          | Expert |
| --------------------- | -------- | -------------------------------------------------------------------------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| layerId               | yes      | String                                                                                       | ""      | The id of the Layer.                                                                                                                                 | false  |
| oafRequestCRS         | no       | String                                                                                       | ""      | Only for OAF Service - The coordinate reference system of the response geometries. I.e.: 'http://www.opengis.net/def/crs/EPSG/0/25832'               | false  |
| oafDataProjectionCode | no       | String                                                                                       | ""      | Only for OAF Service - The projection code of the data. Is needed to render the features on the map. I.e.: 'EPSG:25832'                              | false  |
| geometryAttribute     | yes      | String                                                                                       | ""      | Type of the geometry attribute.                                                                                                                      | false  |
| chartDirectionValue   | no       | String                                                                                       | ""      | Specifies the number above which the bars in the chart will be switched from vertical to horizontal.                                                 | false  |
| timeStepsFilter       | yes      | **[timeStepsFilter](#portalconfigmenusectionsmodulesstatisticdashboarddatatimestepsfilter)** | ""      | An object consisting of keys and values where the key contains the number of time groupings and the value contains the description for the grouping. | false  |
| mappingFilter         | yes      | **[mappingFilter](#portalconfigmenusectionsmodulesstatisticdashboarddatamappingfilter)**     | ""      | This object contains attributes used to filter the map by its values.                                                                                | false  |

**Example**

```json
{
    "layerId": "28992",
    "oafRequestCRS": "http://www.opengis.net/def/crs/EPSG/0/25832",
    "oafDataProjectionCode": "EPSG:25832",
    "geometryAttribute": "geom",
    "chartDirectionValue": 10,
    "timeStepsFilter": {
        "5": "Die letzten 5 Jahre",
        "10": "Die letzten 10 Jahre",
        "all": "Alle Jahre"
    },
    "mappingFilter": {
        "timeAttribute": {
            "attrName": "zeitpunkt",
            "name": "Zeitpunkt",
            "inputFormat": "YYYY-MM-DD",
            "outputFormat": "YYYY"
        },
        "regionNameAttribute": {
            "attrName": "statistisches_gebiet",
            "name": "Statistisches Gebiet"
        },
        "statisticsAttributes": {
            "arbeitnehmer_inland_tausend": {
                "name": "Arbeitnehmer (Inland) in 1.000",
                "category": "Beschäftigte"
            },
            "arbeitslose_jahresdurchschnitt": {
                "name": "Arbeitslose",
                "category": "Beschäftigte"
            },
            "arbeitslose_15_bis_u25_jahresdurchschnitt": {
                "name": "Arbeitslose 15 bis unter 25 Jahre",
                "category": "Beschäftigte"
            },
            "einwohner_ab_65": {
                "name": "Einwohner 65 Jahre und älter",
                "category": "Bevölkerung"
            },
            "einwohner_ab_65_prozent_aller_einwohner": {
                "name": "Einwohner 65 Jahre und älter in % aller Einwohner",
                "category": "Bevölkerung"
            },
            "einwohner_auslaender": {
                "name": "Einwohner Ausländer",
                "category": "Bevölkerung"
            }
        }
    }
}
```

***

###### portalConfig.secondaryMenu.sections.modules.statisticDashboard.data.timeStepsFilter {data-toc-label='Time Steps Filter'}

| Name      | Required | Type   | Default | Description                                                                                                       | Expert |
| --------- | -------- | ------ | ------- | ----------------------------------------------------------------------------------------------------------------- | ------ |
| key:value | ja       | String | ""      | Key: The key is the number of the last "key" entry for dropdown options. Value: The description for the grouping. | false  |
| all:value | ja       | String | ""      | Key: The keyword for selecting all entries for dropdown options. Value: The description for the grouping.         | false  |

**Example**

```json
{
    "5": "Die letzten 5 Jahre",
    "10": "Die letzten 10 Jahre",
    "all": "Alle Jahre"
}
```

***

###### portalConfig.secondaryMenu.sections.modules.statisticDashboard.data.mappingFilter {data-toc-label='Mapping Filter'}

| Name                 | Required | Type                                                                                                                | Default | Description                                      | Expert |
| -------------------- | -------- | ------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------ | ------ |
| timeAttribute        | yes      | **[timeAttribute](#portalconfigmenusectionsmodulesstatisticdashboarddatamappingfiltertimeattribute)**               | ""      | The attribute for the time filter.               | false  |
| regionNameAttribute  | yes      | **[regionNameAttribute](#portalconfigmenusectionsmodulesstatisticdashboarddatamappingfilterregionnameattribute)**   | ""      | The attribute for the name of the region.        | false  |
| statisticsAttributes | yes      | **[statisticsAttributes](#portalconfigmenusectionsmodulesstatisticdashboarddatamappingfilterstatisticsattributes)** | ""      | Attributes used to filter the map by its values. | false  |

**Example**

```json
{
    "timeAttribute": {
        "attrName": "zeitpunkt",
        "name": "Zeitpunkt",
        "inputFormat": "YYYY-MM-DD",
        "outputFormat": "YYYY"
    },
    "regionNameAttribute": {
        "attrName": "statistisches_gebiet",
        "name": "Statistisches Gebiet"
    },
    "statisticsAttributes": {
        "arbeitnehmer_inland_tausend": {
            "name": "Arbeitnehmer (Inland) in 1.000",
            "category": "Beschäftigte"
        },
        "arbeitslose_jahresdurchschnitt": {
            "name": "Arbeitslose",
            "category": "Beschäftigte"
        },
        "arbeitslose_15_bis_u25_jahresdurchschnitt": {
            "name": "Arbeitslose 15 bis unter 25 Jahre",
            "category": "Beschäftigte"
        },
        "einwohner_ab_65": {
            "name": "Einwohner 65 Jahre und älter",
            "category": "Bevölkerung"
        },
        "einwohner_ab_65_prozent_aller_einwohner": {
            "name": "Einwohner 65 Jahre und älter in % aller Einwohner",
            "category": "Bevölkerung"
        },
        "einwohner_auslaender": {
            "name": "Einwohner Ausländer",
            "category": "Bevölkerung"
        }
    }
}
```

***

###### portalConfig.secondaryMenu.sections.modules.statisticDashboard.data.mappingFilter.timeAttribute {data-toc-label='Time Attribute'}

| Name         | Required | Type   | Default | Description                         | Expert |
| ------------ | -------- | ------ | ------- | ----------------------------------- | ------ |
| attrName     | yes      | String | ""      | The attribute for the time filters. | false  |
| name         | no       | String | ""      | The name of the attribute.          | false  |
| inputFormat  | no       | String | ""      | Input Format                        | false  |
| outputFormat | no       | String | ""      | Output Format                       | false  |

**Example**

```json
{
    "attrName": "zeitpunkt",
    "name": "Zeitpunkt",
    "inputFormat": "YYYY-MM-DD",
    "outputFormat": "YYYY"
}
```

***

###### portalConfig.secondaryMenu.sections.modules.statisticDashboard.data.mappingFilter.regionNameAttribute {data-toc-label='Region Name Attribute'}

| Name     | Required | Type   | Default | Description                       | Expert |
| -------- | -------- | ------ | ------- | --------------------------------- | ------ |
| attrName | yes      | String | ""      | The attribute of the region.      | false  |
| name     | no       | String | ""      | The name of the region attribute. | false  |

**Example**

```json
{
    "attrName": "statistisches_gebiet",
    "name": "Kreis"
}
```

***

###### portalConfig.secondaryMenu.sections.modules.statisticDashboard.data.mappingFilter.statisticsAttributes {data-toc-label='Statistics Attributes'}

| Name     | Required | Type   | Default | Description                                                                                                                         | Expert |
| -------- | -------- | ------ | ------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------ |
| key      | yes      | String | ""      | The key of the Statistic attributes.                                                                                                | false  |
| name     | yes      | String | ""      | The name of the statisticsAttributes.                                                                                               | false  |
| Category | yes      | String | ""      | The category of the statisticsAttributes. If the category is set, it will be grouped under this category in the category selection. | false  |

**Example**

```json
{
    "arbeitnehmer_inland_tausend": {
        "name": "Arbeitnehmer (Inland) in 1.000",
        "category": "Beschäftigte"
    },
    "arbeitslose_jahresdurchschnitt": {
        "name": "Arbeitslose",
        "category": "Beschäftigte"
    },
    "arbeitslose_15_bis_u25_jahresdurchschnitt": {
        "name": "Arbeitslose 15 bis unter 25 Jahre",
        "category": "Beschäftigte"
    }
}
```

***

##### portalConfig.secondaryMenu.sections.modules.shareView {data-toc-label='Share View'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

Module to share a link to the current map view. It is possible to share the current view as a link with url parameters, via QR code and as a Facebook link.

| Name          | Required | Type    | Default                         | Description                                                                                                                           | Expert |
| ------------- | -------- | ------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| copyShare     | nein     | Boolean | true                            | Shows if the button to copy the link should be in the module.                                                                         | false  |
| facebookShare | nein     | Boolean | false                           | Shows if the button to share a link via facebook should be in the module.                                                             | false  |
| icon          | no       | String  | "bi-share"                      | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**. | false  |
| name          | no       | String  | "common:modules.shareView.name" | Name of the module in the menu.                                                                                                       | false  |
| type          | no       | String  | "shareView"                     | The type of the module. Defines which module is configured.                                                                           | false  |
| qrShare       | nein     | Boolean | false                           | Shows if the button to create a qr code should be in the module.                                                                      | false  |

**Example**

```json
{
    "icon": "bi-share",
    "name": "common:modules.shareView.name",
    "type": "shareView",
    "facebookShare": true,
    "qrShare": true
}
```

***

##### portalConfig.secondaryMenu.sections.modules.styleVT {data-toc-label='Style Vector Tiles'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

The module allows for switching the style of vector tile layers(❗) which provides multiple stylings defined in the `services.json` file.

| Name | Required | Type   | Default                       | Description                                                                                                                           | Expert |
| ---- | -------- | ------ | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| icon | no       | String | "bi-paint-bucket"             | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**. | false  |
| name | no       | String | "common:modules.styleVT.name" | Name of the module in the menu.                                                                                                       | false  |
| type | no       | String | "styleVT"                     | The type of the module. Defines which module is configured.                                                                           | false  |

**Example**

```json
{
    "icon": "bi-paint-bucket",
    "name": "common:modules.styleVT.name",
    "type": "styleVT"
}
```

***

##### portalConfig.secondaryMenu.sections.modules.wfsSearch {data-toc-label='WFS Search'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

Allows to query a WFS(❗) layer decoupled from the search bar using filters and to create a form if necessary.
It is assumed that a stored query is used when using a WFS@2.0.0. When using a WFS@1.1.0, it is assumed that the way the WFS should be filtered is defined through the configuration.

Multiple **[SearchInstances](#portalconfigmenusectionsmoduleswfssearchsearchinstance)** can be defined, which will be selectable through a dropdown menu.

| Name           | Required | Type                                                                            | Default | Description                                                                                                                                                                            | Expert |
| -------------- | -------- | ------------------------------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| instances      | yes      | **[searchInstance](#portalconfigmenusectionsmoduleswfssearchsearchinstance)**[] |         | Array of `searchInstances`. A singular **[searchInstance](#portalconfigmenusectionsmoduleswfssearchsearchinstance)** corresponds to its own search form.                               | false  |
| zoomLevel      | no       | Number                                                                          | 5       | Specifies to which zoom level zooming is to be performed. If the feature does not fit into the zoom level, a suitable zoom level is automatically selected.                            | false  |
| resultsPerPage | no       | Number                                                                          | 0       | The search result list will at most show this amount of results at a time. Further results will be offered on separate result pages. 0 means display all on one page at the same time. | false  |
| multiSelect    | no       | Boolean                                                                         | false   | If `true`, a user may select multiple features from the result list by either pressing Strg/Shift or using checkboxes; when zooming, all selected features will be shown.              | false  |

**Example**

```json
{
    {
        "type": "wfsSearch",
        "instances": [
            {
                "requestConfig": {
                    "layerId": "1234"
                },
                "selectSource": "https://geoportal-hamburg.de/lgv-config/gemarkungen_hh.json",
                "literals": [
                    {
                        "clause": {
                            "type": "and",
                            "literals": [
                                {
                                    "field": {
                                        "queryType": "equal",
                                        "fieldName": "gemarkung",
                                        "inputLabel": "District",
                                        "options": ""
                                    }
                                },
                                {
                                    "field": {
                                        "queryType": "equal",
                                        "fieldName": "flur",
                                        "inputLabel": "Cadastral District",
                                        "options": "flur"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }
}
```

***

###### portalConfig.secondaryMenu.sections.modules.wfsSearch.searchInstance {data-toc-label='Search Instance'}

[type:Literal]: # (Datatypes.Literal)
[type:ResultList]: # (Datatypes.ResultList)
[type:RequestConfig]: # (Datatypes.RequestConfig)
[type:Suggestions]: # (Datatypes.Suggestions)

A singular instance of the WFS Search which is selectable through a dropdown.

| Name               | Required | Type                                         | Default | Description                                                                                                                                                                                                                                                                            | Expert |
| ------------------ | -------- | -------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| literals           | yes      | **[Literal](#datatypesliteral)**[]           |         | Array of `literals`.                                                                                                                                                                                                                                                                   | true   |
| requestConfig      | yes      | **[RequestConfig](#datatypesrequestconfig)** |         | An object, which mainly contains the id of the service (`layerId` or `restLayerId`) that is supposed to be requested. If a WFS@2.0.0 will be used, the `storedQueryId` needs to be provided as well. Additionally, further options for requests can be set.                            | false  |
| selectSource       | no       | String                                       |         | Optional Url leading to the expected options for the different inputs. See **[https://geoportal-hamburg.de/lgv-config/gemarkungen_hh.json]** for an example.                                                                                                                           | false  |
| suggestions        | no       | **[Suggestions](#datatypessuggestions)**     |         | If given, the service will be queried whenever a user inserts values into an input field to suggest a value.                                                                                                                                                                           | false  |
| title              | yes      | String                                       |         | Title of the search instance to be displayed in a dropdown inside the tool.                                                                                                                                                                                                            | false  |
| userHelp           | no       | String                                       |         | Information text regarding the search form to be displayed to the user. If not given, it will be generated from the structure of the config. May be a translation key. If the value is explicitly set to `hide`, no information regarding the structure of the form will be displayed. | false  |
| resultDialogTitle  | no       | String                                       |         | Heading of the result list. If not configured the name `WFS search` will be displayed. May be a translation key.                                                                                                                                                                       | false  |
| resultList         | no       | **[ResultList](#datatypesresultlist)**       |         | Settings for the output of the found features in the result list. If no resultList is configured, the search will zoom directly to the first feature found. Otherwise, clicking on a column in the search results will zoom to the feature.                                            | true   |
| zoomButtonInColumn | no       | Boolean                                      |         | If configured, a zoom button will be displayed in the column `geometry` or `geom`. The specified field must be present in the feature.                                                                                                                                                 | true   |

**Example**

```json
{
    "requestConfig": {
        "layerId": "1234"
    },
    "resultList": {
        "schulname": "School name",
        "abschluss": "Degree",
        "geometry": "Zoom"
    },
    "zoomButtonInColumn": true,
    "selectSource": "https://geoportal-hamburg.de/lgv-config/gemarkungen_hh.json",
    "title": "Parcel Search",
    "literals": [
        {
            "clause": {
                "type": "and",
                "literals": [
                    {
                        "field": {
                            "queryType": "equal",
                            "fieldName": "gemarkung",
                            "inputLabel": "District",
                            "options": ""
                        }
                    },
                    {
                        "field": {
                            "queryType": "equal",
                            "fieldName": "flur",
                            "inputLabel": "Cadastral District",
                            "options": "flur"
                        }
                    }
                ]
            }
        }
    ]
}
```

***

##### portalConfig.secondaryMenu.sections.modules.wfst {data-toc-label='WFS-T'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules)

WFS-T module to visualize (*getFeature*), create (*insert*), update (*update*) and delete (*delete*) features of a Web Feature Service (*WFS*) which is able to receive transactions.
To use this tool, a WFS-T layer must be provided in version 1.1.0. For more configuration information see **[services.json](../Global-Config/services.json.md)**.

When editing properties of a feature / adding properties to a new feature, the available values including its label are based on the layers configured `gfiAttributes`. For more information see **[services.json](../Global-Config/services.json.md)**.

| Name             | Required | Type                                                                                 | Default                                | Description                                                                                                                                        | Expert |
| ---------------- | -------- | ------------------------------------------------------------------------------------ | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| delete           | no       | [TransactionConfig](#portalconfigmenusectionsmoduleswfsttransactionconfig)/Boolean   | false                                  | Defines which layers of `layerIds` allow delete transactions.                                                                                      | false  |
| icon             | no       | String                                                                               | "bi-globe"                             | Icon that is shown in front of the module-name in the menu. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**.              | false  |
| layerIds         | yes      | String[]                                                                             |                                        | Array of layer-ids defined in **[services.json](../Global-Config/services.json.md)**.                                                              | false  |
| layerSelectLabel | no       | String                                                                               | "common:modules.wfst.layerSelectLabel" | Please set the value directly in the language files. If given, overrides the value set for the label of the layer select box. May be a locale key. | false  |
| lineButton       | no       | [TransactionConfig](#portalconfigmenusectionsmoduleswfsttransactionconfig)[]/Boolean | []                                     | Defines which layers of `layerIds` allow insert transactions of line geometries.                                                                   | false  |
| name             | no       | String                                                                               | "common:modules.wfst.name"             | Tool name shown in the portal.                                                                                                                     | false  |
| pointButton      | no       | [TransactionConfig](#portalconfigmenusectionsmoduleswfsttransactionconfig)[]/Boolean | []                                     | Defines which layers of `layerIds` allow insert transactions of point geometries.                                                                  | false  |
| polygonButton    | no       | [TransactionConfig](#portalconfigmenusectionsmoduleswfsttransactionconfig)[]/Boolean | []                                     | Defines which layers of `layerIds` allow insert transactions of polygon geometries.                                                                | false  |
| showConfirmModal | no       | Boolean                                                                              | false                                  | Flag if the modal dialog should be shown.                                                                                                          | false  |
| toggleLayer      | no       | Boolean                                                                              | false                                  | Whether the features of the currently selected layer should stay visible when adding a new feature.                                                | false  |
| type             | no       | String                                                                               | "wfst"                                 | The type of the module. Defines which module is configured.                                                                                        | false  |
| update           | no       | [TransactionConfig](#portalconfigmenusectionsmoduleswfsttransactionconfig)/Boolean   | false                                  | Defines which layers of `layerIds` allow update transactions.                                                                                      | false  |
| multiUpdate      | no       | [multiUpdate](#portalconfigmenusectionsmoduleswfstmultiupdate)[]                     | []                                     | Defines which layers allow multiple features to be updated at once.                                                                                | false  |

**Example**

```json
{
    "type": "wfst",
    "name": "common:modules.wfst.name",
    "icon": "bi-globe",
    "layerIds": ["1234", "5678", "4389"],
    "toggleLayer": true,
    "pointButton": [
        {
            "layerId":"1234",
            "caption": "Point test",
            "available": true
        },
        {
            "layerId": "5678",
            "available": true,
            "multi": true
        }
    ],
    "lineButton": false,
    "polygonButton": [
        {
            "layerId": "4389",
            "available": false
        }
    ],
    "update": [
        {
            "layerId": "4389",
            "available": true
        }
    ],
    "multiUpdate": [
        {
            "layerId": "4389",
            "available": true,
            "configAttributes": ["name", "description"],
            "controlAttributes": ["gemeinde"],
            "warningText": "common:modules.wfst.multiUpdate.warningText",
            "selectTypes": ["pen"],
            "selectIcons":
                {
                    "pen": "bi-pencil-fill",
                    "box": "fa-vector-square",
                    "select": "fa-mouse-pointer"
                }
        }
    ]
}
```

***

###### portalConfig.secondaryMenu.sections.modules.wfst.multiUpdate {data-toc-label='multiUpdate'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules.wfst)

Defines the configuration for updating multiple features at once.

| Name              | Required | Type                                                                      | Default | Description                                                                                                          | Expert |
| ----------------- | -------- | ------------------------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------- | ------ |
| layerId           | yes      | String                                                                    |         | The ID of the layer from services.json for which the multiupdate function is configured.                             | false  |
| available         | no       | Boolean                                                                   | false   | A flag to determine if the function is available for this layer.                                                     | false  |
| configAttributes  | no       | String[]                                                                  | []      | An array of attribute names whose values are only to be displayed and not editable in the multiupdate form.          | false  |
| controlAttributes | no       | String[]                                                                  | []      | An array of attribute names whose values are to be used for controlling the multiupdate process and can be editable. | false  |
| warningText       | no       | String                                                                    |         | An optional text that is displayed as a warning when selecting features.                                             | false  |
| selectTypes       | no       | String[]                                                                  | ["pen"] | Defines which tools are available for selecting features.                                                            | false  |
| selectIcons       | no       | [selectIcons](#portalconfigmenusectionsmoduleswfstmultiupdateselecticons) | {}      | An object that defines the icons for the selection tools specified in selectTypes.                                   | false  |


**Example**

```json
"multiUpdate": [
    {
        "layerId": "4389",
        "available": true,
        "configAttributes": ["name", "description"],
        "controlAttributes": ["gemeinde"],
        "warningText": "common:modules.wfst.multiUpdate.warningText",
        "selectTypes": ["pen"],
        "selectIcons": {
            "pen": "bi-pencil-fill",
            "box": "fa-vector-square",
            "select": "fa-mouse-pointer"
        }
    }
]
```

***

###### portalConfig.secondaryMenu.sections.modules.wfst.multiUpdate.selectIcons {data-toc-label='selectIcons'}

[inherits]: # (portalConfig.secondaryMenu.sections.modules.wfst.multiUpdate)

Defines the mapping of selection tools to their corresponding icons.

| Name   | Required | Type   | Default            | Description                                    | Expert |
| ------ | -------- | ------ | ------------------ | ---------------------------------------------- | ------ |
| pen    | no       | String | "bi-pencil-fill"   | The icon name used for the pen selection tool. | false  |
| box    | no       | String | "fa-vector-square" | The icon name used for the box selection tool. | false  |
| select | no       | String | "fa-mouse-pointer" | The icon name used for the click.              | false  |

**Example**

```json
"selectIcons": {
        "pen": "bi-pencil-fill",
        "box": "fa-vector-square",
        "select": "fa-mouse-pointer"
}
```

***


###### portalConfig.secondaryMenu.sections.modules.wfst.TransactionConfig {data-toc-label='Transaction Config'}
Specific configuration for transaction methods of given layers.

| Name      | Required | Type    | Default                                   | Description                                                                                                                                                                                                             | Expert |
| --------- | -------- | ------- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| available | yes      | Boolean | true                                      | Availability of the transaction method for the layer with the given id.                                                                                                                                                 | false  |
| icon      | no       | String  |                                           | Bootstrap icon displayed inside the button. If no value is specified, it defaults to the default value configured for the transaction method. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**. | false  |
| layerId   | yes      | String  |                                           | Layer the transaction method is being configured for.                                                                                                                                                                   | false  |
| multi     | no       | Boolean | false                                     | Whether the drawn geometries of this layer should be Multi-X.  This parameter does not have any use for `update` and `delete`.                                                                                          | false  |
| text      | no       | String  | "common:modules.wfst.interactionSelect.*" | Button text. If no value is given, `*` will be replaced with a standard value depending on the configured button. May be a locale key.                                                                                  | false  |

**Examples**

```json
{
    "layerId": "1234",
    "available": true,
    "text": "Point test"
}
```

```json
{
    "layerId": "5678",
    "available": true
}
```

```json
{
    "layerId": "5489",
    "multi": true
}
```

***

#### portalConfig.secondaryMenu.title {data-toc-label='Portal Title'}
The menu bar allows showing a portal name and portal image.

| Name    | Required | Type   | Default | Description                                                                                               | Expert |
| ------- | -------- | ------ | ------- | --------------------------------------------------------------------------------------------------------- | ------ |
| link    | no       | String |         | URL of an external website to link to.                                                                    | false  |
| logo    | no       | String |         | Path to an external image file. If no image is set, the title will be shown without an accompanying logo. | false  |
| text    | no       | String |         | Portal name, if not set only the logo will be shown with 80% width.                                       | false  |
| toolTip | no       | String |         | Shown on hovering the portal logo.                                                                        | false  |

**Example portalTitle**

```json
"title": {
    "text": "Master",
    "logo": "https://geodienste.hamburg.de/lgv-config/img/hh-logo.png",
    "link": "https://geoinfo.hamburg.de",
    "toolTip": "Landesbetrieb Geoinformation und Vermessung"
}
```

***
