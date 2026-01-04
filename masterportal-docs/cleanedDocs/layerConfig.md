## layerConfig {data-toc-label='Layer Config'}
The `layerConfig` entry defines the contents and their order in the topic selection. The following properties can be configured:

1. Layers containing background maps (*baselayer*)
2. Layers containing subject data (*subjectlayer*)

| Name         | Required | Type                                         | Default | Description                        | Expert |
| ------------ | -------- | -------------------------------------------- | ------- | ---------------------------------- | ------ |
| baselayer    | no       | **[baselayer](#layerconfigbaselayer)**       |         | Layers containing background maps. | false  |
| subjectlayer | no       | **[subjectlayer](#layerconfigsubjectlayer)** |         | Layers containing subject data.    | false  |

**Example**

```json
{
    "layerConfig": {
        "baselayer": {
            "elements": []
        },
        "subjectlayer": {
            "elements": []
        }
    }
}
```

***

### layerConfig.baseLayer.elements or layerConfig.subjectLayer.elements {data-toc-label='Elements'}

[type:elements]: # (layerConfig.elements)

Layers or folders are defined here. Folders can in turn contain **[elements](#layerconfigelements)** with folders or layers.
Elements can be used both in baseLayer and subjectLayers.

| Name                      | Required | Type                                   | Default | Description                                                                                         | Expert |
| ------------------------- | -------- | -------------------------------------- | ------- | --------------------------------------------------------------------------------------------------- | ------ |
| elements                  | no       | **[elements](#layerconfigelements)**[] |         | Next layer with layers or folders under the type `folder`.                                          | false  |
| name                      | no       | String                                 | ""      | Layer or folder name. Can contain HTML tags that will only be rendered in layer tree.               | false  |
| shortname                 | no       | String                                 | ""      | shortened layer or folder name. If configured it will be displayed in layer tree instead of `name`. | false  |
| type                      | no       | String                                 | "layer" | Type of the element: "layer" or "folder"                                                            | false  |
| deactivateShowAllCheckbox | no       | Boolean                                | false   | Deactivates the "Show All" Checkbox, when the type is a folder                                      | false  |

**Example baselayer**

```json
{
    "layerConfig": {
        "baselayer": {
            "elements": [
                {
                    "id": "123"
                }
            ]
        }
    }
}
```

**Example subjectlayer**

```json
{
    "layerConfig": {
        "subjectlayer": {
            "elements": [
                {
                    "id": "123",
                    "type": "layer"
                }
            ]
        }
    }
}
```

**Example with folders and layers**

```json
{
"elements": [
        {
        "name": "Folder level 1",
        "type": "folder",
        "elements": [
                {
                "name": "Folder level 2",
                "type": "folder",
                "deactivateShowAllCheckbox": true,
                "elements": [
                        {
                            "id": "2431"
                        },
                        {
                            "id": "2430"
                        },
                        {
                            "id": "2429"
                        },
                        {
                            "name": "Folder level 3",
                            "type": "folder",
                            "elements": [
                                {
                                    "id": "1103"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}
```

***

#### layerConfig.elements.layers {data-toc-label='Layers'}

[inherits]: # (layerConfig.elements)

Here layers of different types are configured. Layers can be configured in many different ways. Most of the attributes are defined in **[services.json](../Global-Config/services.json.md)**, but can be overridden here at the layer.
Besides these attributes, there are also type-specific attributes for the different layer types.

| Name                  | Required | Type                                             | Default   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Expert |
| --------------------- | -------- | ------------------------------------------------ | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| autoRefresh           | no       | Integer                                          |           | Automatically reload layer every `autoRefresh` ms. Minimum value is 500.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | false  |
| capabilitiesUrl       | no       | String                                           |           | **[services.json](../Global-Config/services.json.md)** value. Service's capabilities URL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | false  |
| filterRefId           | no       | Integer                                          |           | Referencing to a configured filter. It is the order (index) of Layer in filter. Starting with 0.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | false  |
| fitCapabilitiesExtent | no       | Boolean                                          | false     | **[services.json](../Global-Config/services.json.md)** value. When set to `true` and a `capabilitiesUrl` is specified in the configuration, the application will fit the map extent based on the bounding box information retrieved from the GetCapabilities document.                                                                                                                                                                                                                                                                                                                                                                                                                                              | false  |
| id                    | yes      | String/String[]                                  |           | Id of the layer. The ids are resolved in **[services.json](../Global-Config/services.json.md)** and the necessary information is used. When configuring an array of Ids, a layer is created that contains the LAYERS parameter in the request with a comma-separated list of the contents of the `layers` attribute of the individual layers. Setting `minScale` and `maxScale` of each layer is required to be in the `services.json`. It is important here that the specified ids address the same URL, i.e. use the same service and are of same typ. With the special character `.` as suffix, a LayerId can be used multiple times. Each LayerId marked with a suffix creates its own entry in the topic tree. | false  |
| isPointLayer          | no       | Boolean                                          | false     | Whether the (vector) layer only consists of point features (only relevant for WebGL rendering)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | false  |
| name                  | no       | String                                           |           | Layer name.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | false  |
| preview               | no       | **[preview](#layerconfigelementslayerspreview)** |           | Preview for baselayers of type WMS, WMTS and VectorTile. WMS and WMTS: if not specified, a centered map section is loaded.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | false  |
| renderer              | no       | String                                           | "default" | Which render pipeline to use ("default" or "webgl") (only for vector data of type "GeoJSON", "WFS", "OAF"). "webgl" is currently classified as experimental and can lead to errors in some modules                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | false  |
| showInLayerTree       | no       | Boolean                                          | false     | If true, then the layer is initially displayed in the topic tree. If portalConfig.tree.addLayerButton is not configured, then this attribute has no effect.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | false  |
| transparency          | no       | Integer                                          | 0         | Layer transparency.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | false  |
| type                  | no       | String                                           | "layer"   | Type of the lement: "layer" or "folder"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | false  |
| urlIsVisible          | no       | Boolean                                          | true      | Whether the service URL should be shown in the layer information window.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | false  |
| visibility            | no       | Boolean                                          | false     | Layer visibility.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | false  |

**Example**

```json
{
    "elements": [
        {
            "id": "2",
            "name": "Example Layer",
            "typ": "WMS",
            "visibility": false,
            "styleId": "3",
            "filterRefId": 0
        }
    ]
}
```

**Example with an array of IDs**

```json
{
"elements": [
        {
            "id": ["123", "456", "789"],
            "name": "My test layer"
        }
    ]
}
```

**Example layerId 8712 with suffix**

```json
{
"elements": [
        {
          "id": "8712.1",
          "styleId": "8712.1",
          "name": "Grundschulen",
          "wfsFilter": "resources/xml/schulstandort.staatlich.5.grundschulen.xml"
        },
        {
          "id": "8712.2",
          "styleId": "8712.2",
          "name": "Stadtteilschulen",
          "wfsFilter": "resources/xml/schulstandort.staatlich.5.stadtteilschulen.xml",
        },
        {
          "id": "8712.3",
          "styleId": "8712.3",
          "name": "Gymnasien",
          "wfsFilter": "resources/xml/schulstandort.staatlich.5.gymnasien.xml"
        },
        {
          "id": "8712.4",
          "styleId": "8712.4",
          "name": "Sonderschulen",
          "wfsFilter": "resources/xml/schulstandort.staatlich.5.sonderschulen.xml"
        }
    ]
}
```

***

#### layerConfig.elements.layers.preview {data-toc-label='Preview'}

[inherits]: # (layerConfig.elements.layers)

Preview for baselayer in theme tree, also used in **[baselayerSwitcher](#portalconfigmapbaselayerswitcher)**.
For the **[VectorTile](#layerconfigelementslayersvectortile)**, **[WMS](#layerconfigelementslayersrasterwms)** and WMTS layer types.
With the VectorTile layer a dropped preview image is displayed, with WMS and WMTS layers a map section is loaded. WMS and WMTS: if not specified, a centered map section is loaded. A detailed description is available in the documentation **[LayerPreview](../../Dev/vueComponents/LayerPreview.md)**

| Name        | Required | Type              | Default | Description                                                                                                                                       | Expert |
| ----------- | -------- | ----------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| center      | no       | Number[]/String[] |         | Center coordinates for the preview image loading parameters. Default is the center of the map extent.                                             | false  |
| checkable   | no       | Boolean           | false   | If `true`, then the preview image is usable as checkbox.                                                                                          | false  |
| customClass | no       | String            |         | Custom css class to override the style, NOTE: may need to use '!important'.                                                                       | false  |
| radius      | no       | Number            | 1000    | Radius of the extent in meters.                                                                                                                   | false  |
| src         | no       | String            |         | Only for type 'VectorTile'. Path to the image to be previewed.                                                                                    | false  |
| zoomLevel   | no       | Number            |         | Zoom level from which the resolution for the loading parameters of the preview image are determined. Default is the initial zoomLevel of the map. | false  |

**Example VectorTile**

```json
"preview":{
    "src": "./resources/vectorTile.png"
    }
```

**Example WMS**

```json
 "preview": {
    "zoomLevel": 6,
    "center": "566245.97,5938894.79",
    "radius": 500
    }
```

***

#### layerConfig.elements.layers.Group {data-toc-label='Group'}

[inherits]: # (layerConfig.elements.layers)
[type:children]: # (layerConfig.elements.layers)

A group layer is created that contains all layers of the specified ids.

| Name     | Required | Type                                         | Default | Description                                                                                                                                                                       | Expert |
| -------- | -------- | -------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| id       | yes      | String[]                                     |         | Ids of the layers to be grouped, these must be contained in the **[services.json](../Global-Config/services.json.md)**. They can have different types (field `typ`).              | false  |
| typ      | yes      | String                                       | "GROUP" | Sets the layer typ to GROUP, which can group layers.                                                                                                                              | false  |
| children | no       | **[children](#layerconfigelementslayers)**[] |         | Attributes on the grouped layers can be overwritten in `children`. Exception: `visibility` is not overwritten. All ids in the id array must have an equivalent in the `children`. | false  |


**Example without children**
```json
 {
    "id": [ "20501", "20502", "20503", "20504" ],
    "typ": "GROUP",
    "name": "Leisure routes and long-distance cycle routes group",
    "styleId": "4515"
}
```
**Example with children**

```json
{
    "id": [ "27926", "1711", "18104"],
    "typ": "GROUP",
    "name": "Group OAF, WFS, SensorThings",
    "visibility": false,
    "children" :[
        {
            "id": "27926",
            "styleId": "8712",
            "typ": "OAF",
            "gfiTheme": "schulinfo"
        },
        {
            "id": "1711",
            "styleId": "1711",
            "typ": "WFS"
        },
        {
            "id": "18104",
            "styleId": "18104",
            "typ": "SensorThings"
        }
    ]
}
```

***

#### layerConfig.elements.layers.Raster {data-toc-label='Raster'}

[inherits]: # (layerConfig.elements.layers)

Raster layer typical attributes are listed here. Raster layers are of type **[StaticImage](#layerconfigelementslayersrasterstaticimage)**, **[WMS](#layerconfigelementslayersrasterwms)**, WMSTime and WMTS.

***

##### layerConfig.elements.layers.Raster.StaticImage {data-toc-label='Static Image'}

[inherits]: # (layerConfig.elements.layers.Raster)

StaticImage can be used to load images as layers and display them georeferenced on the map. The formats jpeg and png are supported.

| Name   | Required | Type                           | Default                            | Description                                                                                                                                                           | Expert |
| ------ | -------- | ------------------------------ | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| extent | yes      | **[Extent](#datatypesextent)** | [560.00, 5950.00, 560.00, 5945.00] | Specifies the georeferencing of the image. The coordinate pair expected in EPSG:25832 format is the coordinate for the top left and bottom right corner of the image. | false  |
| id     | yes      | String                         |                                    | A unique ID must be assigned among all layers.                                                                                                                        | false  |
| typ    | yes      | String                         | "StaticImage"                      | Sets the layer type to StaticImage, which can display static images as layers.                                                                                        | false  |
| url    | yes      | String                         | "https://meinedomain.de/bild.png"  | Link to the image to be displayed.                                                                                                                                    | false  |


**Example**
```json
{
    "id": "4811",
    "typ": "StaticImage",
    "url": "https://www.w3.org/Graphics/PNG/alphatest.png",
    "name": "Testing PNG file",
    "visibility": true,
    "extent": [560296.72, 5932154.22, 562496.72, 5933454.22]
}
```

***

##### layerConfig.elements.layers.Raster.WMS {data-toc-label='WMS'}

[inherits]: # (layerConfig.elements.layers.Raster)

WMS typical attributes are listed here.

| Name           | Required | Type                                                                    | Default                            | Description                                                                                                                  | Expert |
| -------------- | -------- | ----------------------------------------------------------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------ |
| name           | no       | String/String[]                                                         |                                    | Name of the layer. If the **styles** attribute is configured, this attribute must be configured as Tpy String[].             | false  |
| extent         | no       | **[Extent](#datatypesextent)**                                          | [454591, 5809000, 700000, 6075769] | Extent of the layer. If not specified, it will be used extent of the map view.                                               | false  |
| featureCount   | no       | Number                                                                  | 1                                  | Number of features to return on a GetFeatureInfo query.                                                                      | false  |
| gfiAsNewWindow | no       | **[gfiAsNewWindow](#layerconfigelementslayersrasterwmsgfiasnewwindow)** | null                               | Considered only if infoFormat is text/html.                                                                                  | true   |
| styles         | no       | String[]                                                                |                                    | If styles are specified, they are also sent to the WMS. The server interprets these styles and returns the data accordingly. | true   |

**Example**

```json
{
    "id": "4711",
    "name": ["MyFirstWMSLayerName", "MySecondWMSLayerName"],
    "transparency": 0,
    "visibility": true,
    "featureCount": 2,
    "gfiAsNewWindow": {
        "name": "_blank",
        "specs": "width=800,height=700"
    },
    "styles": ["firstStyle", "secondStyle"]
}
```

***

###### layerConfig.elements.layers.Raster.WMS.gfiAsNewWindow {data-toc-label='gfiAsNewWindow'}

[inherits]: # (layerConfig.elements.layers.Raster)

The parameter `gfiAsNewWindow` is only in use when `infoFormat` is set to `"text/html"`.

This feature allows opening WMS HTML responses in their own window or tab rather than in an iFrame or GFI. To open HTML contents in a standard browser window, set the empty object `{}` instead of `null`.

You may change the opening behaviour by setting the parameter `name`:

**Note on SSL encryption**

If `gfiAsNewWindow` is not defined, it's applied with default values when the called URL is not SSL-encrypted (HTTPS).

Due to the *No Mixed Content* policy of all modern browsers, unencrypted content may not be displayed in an iFrame. Please mind that automatic forwarding (e.g. in Javascript) in iFrames to an insecure HTTP connection (without SSL) is not automatically recognized and may be prevented by the browser.

For such cases, define `gfiAsNewWindow` manually as described above.

| Name  | Required | Type                     | Default  | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Expert |
| ----- | -------- | ------------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| name  | yes      | enum["_blank_","_self_"] | "_blank" | `"_blank"` opens a new browser tab or window (depending on browser) with the specified HTML content. The window appearance can be changed with the `specs` parameter. `"_self"` opens the specified HTML content within the current browser window.                                                                                                                                                                                                                    | true   |
| specs | no       | String                   |          | You may add an arbitrary amount of comma-separated properties like `{"specs": "width=800,height=700"}`. For more options, please read the documentation regarding `javascript` and `window.open`: [W3 Schools: Met win open](https://www.w3schools.com/jsref/met_win_open.asp) (German), [JavaScript Info: Popup windows](https://javascript.info/popup-windows) (English), [MDN: Window open](https://developer.mozilla.org/en-US/docs/Web/API/Window/open) (English) | true   |

**Example**

```json
{
    "id": "4711",
    "gfiAsNewWindow": {
        "name": "_blank",
        "specs": "toolbar=yes,scrollbars=yes,resizable=yes,top=0,left=500,width=800,height=700"
    }
}
```

***

#### layerConfig.elements.layers.Vector {data-toc-label='Vector'}

[inherits]: # (layerConfig.elements.layers)

Vector typical attributes are listed here. Vector layers are of type **[WFS](#layerconfigelementslayersvectorwfs)**, GeoJSON (only in EPSG:4326), **[SensorLayer](../../Dev/sensorThings.md)** and OAF.

| Name                 | Required | Type            | Default | Description                                                                                                                                                                                   | Expert |
| -------------------- | -------- | --------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| additionalInfoField  | no       | String          | "name"  | Attribute name of the feature for the hitlist in the searchbar. If the attribute does not exist, the layer name is specified.                                                                 | false  |
| clusterDistance      | no       | Integer         |         | Pixel radius. Within this radius all features are "clustered" to one feature. ⚠️ clusterDistance for WFS layers with polygon or line geometry will result in the features not being displayed. | false  |
| hitTolerance         | no       | String          |         | Click tolerance at which a hit is triggered for the GetFeatureInfo query.                                                                                                                     | false  |
| loadingStrategy      | no       | String          | "bbox"  | LLoading strategy for loading the features. Possible values are "bbox" or "all". **[see](https://openlayers.org/en/latest/apidoc/module-ol_loadingstrategy.html)**.                           | false  |
| mouseHoverField      | no       | String/String[] |         | Attribute name or array of attribute names to be displayed when the user hovers over a feature.                                                                                               | false  |
| nearbyTitle          | no       | String/String[] |         | Attribute name or array of attribute names to be displayed as title in the result list during the proximity search.                                                                           | false  |
| searchField          | no       | String          |         | Attribute name for which the searchbar searches this layer.                                                                                                                                   | false  |
| styleGeometryType    | no       | String/String[] |         | Geometry types for a WFS style, if only certain geometries of a layer are to be displayed **[see](../Global-Config/style.json.md#display-rules)**.                                            | false  |
| styleId              | yes      | String          |         | Id that defines the style. Id is resolved in the **[style.json](../Global-Config/style.json.md)**.                                                                                            | false  |
| isNeverVisibleInTree | no       | Boolean         |         | A parameter for layer config to supply an option to hide the layer in tree. If true, the layer will not be visible in tree.                                                                   | false  |

**Example**

```json
{
"elements": [
          {
            "id": "22078",
            "name": "Bewohnerparkgebiete Hamburg",
            "typ": "WFS",
            "visibility": false,
            "styleId": "22078",
            "styleField": "bewirtschaftungsart",
            "searchField": "bwp_name",
            "mouseHoverField": [
                "bwp_name",
                "bewirtschaftungsart"
            ],
            "isNeverVisibleInTree": false
        },
        {
            "id" : "11111",
            "name" : "lokale GeoJSON",
            "url" : "portal/master/test.json",
            "typ" : "GeoJSON",
            "gfiAttributes" : "showAll",
            "layerAttribution" : "nicht vorhanden",
            "legend" : true
        }
    ]
}
```

***

##### layerConfig.elements.layers.Vector.WFS {data-toc-label='WFS'}

[inherits]: # (layerConfig.elements.layers.Vector)

Attributes for the WFS search at highlightFeaturesByAttribute. For the call parameters see **[urlParameter](../Misc/urlParameter.md)**.
```
Example calls:
?api/highlightFeaturesByAttribute=1&wfsId=1&attributeName=DK5&attributeValue=valueToSearchFor&attributeQuery=isequal
?api/highlightFeaturesByAttribute=123&wfsId=1711&attributeName=name&attributeValue=Helios%20ENDO-Klinik%20Hamburg&attributeQuery=IsLike
?api/highlightFeaturesByAttribute=123&wfsId=2003&attributeName=gebietsname&attributeValue=NSG%20Zollenspieker&attributeQuery=isequal
?api/highlightFeaturesByAttribute=123&wfsId=2928&attributeName=biotop_nr&attributeValue=111&attributeQuery=isLike
```

| Name           | Required | Type   | Default | Description                                          | Expert |
| -------------- | -------- | ------ | ------- | ---------------------------------------------------- | ------ |
| escapeChar     | yes      | String |         | The escape character for the WFS query - e.g. \|     | true   |
| featurePrefix  | yes      | String |         | Search prefix for the WFS query - e.g. app:.         | true   |
| singleChar     | yes      | String |         | The single character for the WFS query - e.g. #      | true   |
| valueDelimiter | no       | String | ";"     | The value delimiter for isIn queries attributeValue. | true   |
| wildCard       | yes      | String |         | The wildcard character for the WFS query -e.g. %     | true   |

**Example**

```json
{
    "id": "1",
    "visibility": false,
    "name": "Animal species invasive",
    "featurePrefix": "app:",
    "wildCard": "%",
    "singleChar": "#",
    "escapeChar": "!"
}
```

***

#### layerConfig.elements.layers.VectorTile {data-toc-label='VectorTile'}

[inherits]: # (layerConfig.elements.layers)

VectorTile typical attributes are listed here.

| Name       | Required | Type                                                         | Default | Description                                                                                                                                                                                                                                             | Expert |
| ---------- | -------- | ------------------------------------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| useMpFonts | no       | Boolean                                                      | true    | Only available in a *Vector Tile Layer*. Switch to overwrite Fontstacks of external style definitions, to assure needed fonts are available. If set to false, used fonts need to be added separately e.g. via '<link rel=stylesheet ...>' in index.html | false  |
| vtStyles   | no       | **[vtStyle](#layerconfigelementslayersvectortilevtstyle)**[] |         | Choosable external style definitions.                                                                                                                                                                                                                   | false  |

**Example**

```json
{
  "id": "123",
  "name": "Vectortile layer name",
  "epsg": "EPSG:3857",
  "url": "https://example.com/3857/tile/{z}/{y}/{x}.pbf",
  "typ": "VectorTile",
  "vtStyles": [
    {
      "id": "STYLE_1",
      "name": "Day view",
      "url": "https://example.com/3857/resources/styles/day.json",
      "defaultStyle": true
    },
    {
      "id": "STYLE_2",
      "name": "Night view",
      "url": "https://example.com/3857/resources/styles/night.json"
    }
  ],
  "preview":{
    "src": "./resources/vectorTile.png"
    }
}
```

***

##### layerConfig.elements.layers.VectorTile.vtStyle {data-toc-label='vtStyle'}

[inherits]: # (layerConfig.elements.layers.VectorTile)

Style definitions. Available for *Vector Tile Layers* only.

| Name         | Required | Type     | Default | Description                                                                                                                                | Expert |
| ------------ | -------- | -------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| defaultStyle | no       | String   |         | If set `true`, this style is used initially; if no field is set `true`, the first style is used.                                           | false  |
| id           | yes      | String   |         | Cross-service unique id.                                                                                                                   | false  |
| name         | yes      | String   |         | Display name, e.g. used in the selection tool.                                                                                             | false  |
| resolutions  | no       | Number[] |         | Resolutions for zoom levels defined in style. If not set default resolutions from ol-mapbox-style project are used.                        | false  |
| url          | yes      | String   |         | URL to load a style from. The linked JSON *must* match the [Mapbox style specification](https://docs.mapbox.com/mapbox-gl-js/style-spec/). | false  |

**Example**

```json
{
    "id": "Style_1",
    "name": "Red lines",
    "url": "https://example.com/asdf/styles/root.json",
    "defaultStyle": true,
    "resolutions": [
        661.4579761460263,
        264.58319045841048,
        66.14579761460263,
        26.458319045841044,
        15.874991427504629,
        10.583327618336419
    ]
}
```

***

#### layerConfig.elements.layers.Tileset {data-toc-label='Tileset'}

[inherits]: # (layerConfig.elements.layers)

List of attributes typically used for tilesets.

| Name                                                                                              | Required | Type                                                                                | Default | Description                                                                                                                                | Expert |
| ------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| hiddenFeatures                                                                                    | no       | String[]                                                                            | []      | List of IDs to be hidden in the plane.                                                                                                     | true   |
| **[cesium3DTilesetOption](https://cesiumjs.org/Cesium/Build/Documentation/Cesium3DTileset.html)** | no       | **[cesium3DTilesetOption](#layerconfigelementslayerstilesetcesium3dtilesetoption)** |         | Cesium 3D tileset options directly forwarded to the *Cesium tileset object*. E.g. `maximumScreenSpaceError` is relevant to the visibility. | true   |

**Example**

```json
{
    "id": "123456",
    "name": "TilesetLayerName",
    "visibility": true,
    "hiddenFeatures": ["id1", "id2"],
    "cesium3DTilesetOptions" : {
        "maximumScreenSpaceError" : 6
    },
}
```

***

##### layerConfig.elements.layers.Tileset.cesium3DTilesetOption {data-toc-label='cesium3DTilesetOption'}

[inherits]: # (layerConfig.elements.layers.Tileset)

Cesium 3D tileset options directly forwarded to the *Cesium tileset object*.

| Name                    | Required | Type   | Default | Description                                                                                                                                                                                                                   | Expert |
| ----------------------- | -------- | ------ | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| maximumScreenSpaceError | no       | Number |         | The maximum screen space error used for refining the level of detail. This value helps determine when a tile is refined to its successors, and therefore plays an important role in balancing performance and visual quality. | true   |

**Example**

```json
"cesium3DTilesetOptions" : {
    "maximumScreenSpaceError" : 6
}
```

***

#### layerConfig.elements.layers.Terrain {data-toc-label='Terrain'}

[inherits]: # (layerConfig.elements.layers)

List of attributes typically used for Terrain.

| Name                                                                                                          | Required | Type                                                                                              | Default | Description                                                                                                                                       | Expert |
| ------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| **[cesiumTerrainProviderOption](https://cesiumjs.org/Cesium/Build/Documentation/CesiumTerrainProvider.html)** | no       | **[cesiumTerrainProviderOption](#layerconfigelementslayersterraincesiumterrainprovideroption)**[] |         | Cesium TerrainProvider options directly forwarded to the *Cesium TerrainProvider* E.g. `requestVertexNormals` is used for object surface shading. | true   |

**Example**

```json
{
    "id": "123456",
    "name": "TerrainLayerName",
    "visibility": true,
    "cesiumTerrainProviderOptions": {
        "requestVertexNormals" : true
    },
}
```

***

##### layerConfig.elements.layers.Terrain.cesiumTerrainProviderOption {data-toc-label='Cesium TerrainProviderOption'}

[inherits]: # (layerConfig.elements.layers.Terrain)

Initialization options for the CesiumTerrainProvider constructor.
[cesiumTerrainProviderOptions]: https://cesium.com/learn/cesiumjs/ref-doc/CesiumTerrainProvider.html

| Name                 | Required | Type    | Default | Description                                                                                                                                             | Expert |
| -------------------- | -------- | ------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| requestVertexNormals | no       | Boolean |         | Flag indicating whether the client should request additional illumination information from the server, in the form of normals per vertex, if available. | true   |

**Example**

```json
"cesiumTerrainProviderOptions": {
    "requestVertexNormals" : true
}
```

***

#### layerConfig.elements.layers.Entity3D {data-toc-label='Entity3D'}

[inherits]: # (layerConfig.elements.layers)
[type:Attribute]: # (layerConfig.elements.layers.Entity3D.entities)

List of attributes typically used for Entities 3D.

| Name     | Required | Type                                                  | Default | Description                                    | Expert |
| -------- | -------- | ----------------------------------------------------- | ------- | ---------------------------------------------- | ------ |
| entities | yes      | **[Attribute](#layerconfigelementslayersentity3d)**[] |         | List of entities of the layer to be displayed. | false  |

***

##### layerConfig.elements.layers.Entity3D.entities {data-toc-label='Entities'}

[inherits]: # (layerConfig.elements.layers.Entity3D)
[type:Attribute]: # (layerConfig.elements.layers.Entity3D.entities)

Entities3D entities typical attributes are listed here.

| Name         | Required | Type                                                                 | Default | Description                                                                            | Expert |
| ------------ | -------- | -------------------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------- | ------ |
| allowPicking | no       | Boolean                                                              | true    | Whether the model may be clicked for GFI. Example: `true`                              | false  |
| attributes   | no       | **[Attribute](#layerconfigelementslayersentity3dentitiesattribute)** |         | Model attributes, e.g. `{"name": "test"}`                                              | false  |
| latitude     | yes      | Number                                                               |         | Model origin latitude in degrees. Example: `53.541831`                                 | false  |
| longitude    | yes      | Number                                                               |         | Model origin longitude in degrees. Example: `9.917963`                                 | false  |
| height       | no       | Number                                                               | 0       | Model origin height. Example: `10`                                                     | false  |
| heading      | no       | Number                                                               | 0       | Model rotation in degrees. Example: `0`                                                | false  |
| pitch        | no       | Number                                                               | 0       | Model pitch in degrees. Example: `0`                                                   | false  |
| roll         | no       | Number                                                               | 0       | Model roll in degrees. Example: `0`                                                    | false  |
| scale        | no       | Number                                                               | 1       | Model scale. Example: `1`                                                              | false  |
| show         | no       | Boolean                                                              | true    | Whether the model should be shown. Should be `true`. Example: `true`                   | false  |
| url          | yes      | String                                                               | ""      | Model url, e.g. `"https://daten-hamburg.de/gdi3d/datasource-data/Simple_Building.glb"` | false  |


**Example**

```json
{
      "id": "123456",
      "name": "EntitiesLayerName",
      "visibility": true,
      "typ": "Entities3D",
      "entities": [
         {
            "url": "https://daten-hamburg.de/gdi3d/datasource-data/Simple_Building.glb",
           "attributes": {
             "name": "einfaches Haus in Planten und Blomen"
           },
           "latitude": 53.5631,
           "longitude": 9.9800,
           "height": 12,
           "heading": 0,
           "pitch": 0,
           "roll": 0,
           "scale": 5,
           "allowPicking": true,
           "show": true
         }
       ],
       "gfiAttributes" : {
         "name": "Name"
      }
  },
```

***

###### layerConfig.elements.layers.Entity3D.entities.Attribute {data-toc-label='Attribute'}

[inherits]: # (layerConfig.elements.layers.Entity3D)


| Name | Required | Type   | Default | Description                             | Expert |
| ---- | -------- | ------ | ------- | --------------------------------------- | ------ |
| name | no       | String | ""      | Field that can be displayed in the GFI. | false  |

**Example**

```json
{
   "name": "Fernsehturm.kmz"
}
```
***
