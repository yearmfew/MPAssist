### portalConfig.map {data-toc-label='Map'}
Configuration of the map and elements placed on it.

| Name              | Required | Type                                                       | Default | Description                                                                                                                                                                                                                                                               | Expert |
| ----------------- | -------- | ---------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| baselayerSwitcher | no       | **[baselayerSwitcher](#portalconfigmapbaselayerswitcher)** |         | The baselayerSwitcher allows you to easily change or select a background map.                                                                                                                                                                                             | false  |
| controls          | no       | **[controls](#portalconfigmapcontrols)**                   |         | Allows setting which interactions are active in the map.                                                                                                                                                                                                                  | false  |
| featureViaURL     | no       | **[featureViaURL](#portalconfigmapfeatureviaurl)**         |         | Optional configuration for the URL parameter `featureViaURL`. See **[urlParameter](../Misc/urlParameter.md)** for details.                                                                                                                                                | false  |
| getFeatureInfo    | no       | **[getFeatureInfo](#portalconfigmapgetfeatureinfo)**       |         | Via  getFeatureInfo (GFI) information to arbitrary layers can be requested. For WMS, the data is fetched with a GetFeatureInfo request. Vector data (WFS, Sensor, GeoJSON, etc.) is already present in the client and will be shown from the already fetched information. | false  |
| layerPills        | no       | **[layerPills](#portalconfigmaplayerpills)**               |         | Configuration of the LayerPills.                                                                                                                                                                                                                                          | false  |
| map3dParameter    | no       | **[map3dParameter](#portalconfigmapmap3dparameter)**       |         | Cesium params.                                                                                                                                                                                                                                                            | false  |
| mapMarker         | no       | **[mapMarker](#portalconfigmapmapmarker)**                 |         | Overrides the map marker module's default values. Useful for 3D markers since OpenLayers's overlays can not be displayed in 3D mode. For this, the map marker has to be defined as vector layer.                                                                          | false  |
| mapView           | no       | **[mapView](#portalconfigmapmapview)**                     |         | Defines the initial map view and a background shown when no layer is selected.                                                                                                                                                                                            | false  |
| mouseHover        | no       | **[mouseHover](#portalconfigmapmousehover)**               |         | Activates the MouseHover feature for vector layers, both WFS and GeoJSON. For per-layer configuration, see the **[Vector](#layerconfigelementslayersvector)**.                                                                                                            | false  |
| startingMapMode   | no       | String                                                     | "2D"    | Indicates the mode in which the map starts. Possible are `2D` and `3D`                                                                                                                                                                                                    | false  |
| zoomTo            | no       | **[zoomTo](#portalconfigmapzoomto)**[]                     |         | Configuration for the URL query parameters `zoomToFeatureId` and `zoomToGeometry`.                                                                                                                                                                                        | false  |

**Example**

```json
{
    "map": {
        "baselayerSwitcher": {},
        "controls": {},
        "getFeatureInfo": {},
        "layerPills": {},
        "map3dParameter": {},
        "mapView": {},
        "mouseHover": {},
        "startingMapMode": "3D"
    }
}
```

***

#### portalConfig.map.baselayerSwitcher {data-toc-label='Base Layer Switcher'}
The baselayerSwitcher allows you to easily switch or select a baselayer.

| Name                | Required | Type    | Default | Description                                                                                                                                          | Expert |
| ------------------- | -------- | ------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| active              | no       | Boolean | false   | Defines if the baselayerSwitcher is activated.                                                                                                       | false  |
| activatedExpandable | no       | Boolean | false   | Specifies whether the baselayerSwitcher is expanded and all available baselayers are displayed or only the active one which is on the highest level. | false  |
| singleBaseLayer     | no       | Boolean | false   | Switches the previous selected Layer to invisible                                                                                                    | false  |

**Example**

```json
"baselayerSwitcher": {
      "active": true,
      "activatedExpandable": false
    }
```

***

#### portalConfig.map.controls {data-toc-label='Controls'}
Allows setting which interactions are active in the map.

Controls can be configured to be expandable so they will not initially show up in the sidebar but if you click the button with the three dots. You need to add the object "expandable" to the controls configuration.

| Name        | Required | Type                                                           | Default | Description                                                                                                                                                                                                                                                                      | Expert |
| ----------- | -------- | -------------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| backForward | no       | Boolean/**[backForward](#portalconfigmapcontrolsbackforward)** | false   | Shows buttons to jump to previous and next map views.                                                                                                                                                                                                                            | false  |
| button3d    | no       | Boolean/**[button3d](#portalconfigmapcontrolsbutton3d)**       | false   | Defines whether a 3D mode switch button is shown.                                                                                                                                                                                                                                | false  |
| expandable  | no       | Boolean                                                        |         | With expandable, controls are hidden behind a button with three dots and can be expanded when needed.                                                                                                                                                                            | false  |
| freeze      | no       | Boolean/**[freeze](#portalconfigmapcontrolsfreeze)**           | false   | Whether a "lock view" button is shown.                                                                                                                                                                                                                                           | false  |
| fullScreen  | no       | Boolean/**[fullScreen](#portalconfigmapcontrolsfreeze)**       | false   | Allows the user to view the portal in full screen mode, that is, without the browser's tabs and address bar, by clicking a button. A second click on the element returns the view back to normal.                                                                                | false  |
| orientation | no       | **[orientation](#portalconfigmapcontrolsorientation)**         |         | The orientation control uses the browser's geolocation feature to determine the user's coordinates.                                                                                                                                                                              | false  |
| rotation    | no       | **[rotation](#portalconfigmapcontrolsrotation)**               | false   | Control that shows the current rotation of the map. With a click the map rotation can be set to north again. Two additional control buttons can be configured to rotate the card clockwise and counterclockwise. See also `mapInteractions` in **[config.js.md](config.js.md)**. | false  |
| startModule | no       | **[startModule](#portalconfigmapcontrolsstartmodule)**         | false   | Displays buttons for the configured tools. These can be used to open and close the respective tools.                                                                                                                                                                             | false  |
| tiltView    | no       | Boolean/**[tiltView](#portalconfigmapcontrolstiltview)**       | false   | Displays two buttons that can be used to tilt the camera up or down in the 3D scene.                                                                                                                                                                                             | false  |
| totalView   | no       | Boolean/**[totalView](#portalconfigmapcontrolstotalview)**     | false   | Offers a button to return to the initial view.                                                                                                                                                                                                                                   | false  |
| zoom        | no       | Boolean/**[zoom](#portalconfigmapcontrolszoom)**               | false   | Defines whether zoom buttons should be displayed.                                                                                                                                                                                                                                | false  |

**Example**

```json
"controls": {
      "backForward": true,
      "fullScreen": true,
      "expandable": {
        "button3d": true
      }
    }
```

***

##### portalConfig.map.controls.backForward {data-toc-label='Back Forward'}
The attribute backForward may be of type boolean or object. If of type boolean, it shows a button using the default configuration that allows the user to switch back and forth between view states. When of type object, the following attributes may be set:

| Name              | Required | Type   | Default           | Description                                                             | Expert |
| ----------------- | -------- | ------ | ----------------- | ----------------------------------------------------------------------- | ------ |
| iconForward       | no       | String | "skip-end-fill"   | Allows changing the icon on the forward button.                         | false  |
| iconBack          | no       | String | "skip-start-fill" | Allows changing the icon on the backwards button.                       | false  |
| supportedDevices  | no       | String | ["Desktop"]       | Devices on which the module can be used and is displayed in the menu.   | false  |
| supportedMapModes | no       | String | ["2D", "3D"]      | Map modes in which the module can be used and is displayed in the menu. | false  |

**Example using type object backForward**

```json
"backForward" : {
    "iconForward": "bi-skip-forward-fill",
    "iconBack": "bi-skip-backward-fill"
}
```

**Example using type boolean backForward**

```json
"backForward": true
```

***

##### portalConfig.map.controls.button3d {data-toc-label='Button 3D'}
The button3d attribute can be of type Boolean or Object. If it is of type Boolean, it indicates the button for switching to 3D mode. If it is of type Object, the following attributes apply

| Name              | Required | Type   | Default                                                     | Description                                                                                            | Expert |
| ----------------- | -------- | ------ | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------ |
| icon2d            | no       | String | "https://geodienste.hamburg.de/lgv-config/img/badge-2d.svg" | A different icon can be used for the button3d control via the icon parameter if the map is in 3D mode. | false  |
| icon3d            | no       | String | "badge-3d"                                                  | A different icon can be used for the button3d control via the icon parameter if the map is in 2D mode. | false  |
| supportedDevices  | no       | String | ["Desktop", "Mobile"]                                       | Devices on which the module can be used and is displayed in the menu.                                  | false  |
| supportedMapModes | no       | String | ["2D", "3D"]                                                | Map modes in which the module can be used and is displayed in the menu.                                | false  |

***

##### portalConfig.map.controls.freeze {data-toc-label='Freeze'}
Screen is locked so that no more actions can be performed in the map. Whether a "lock view" button is shown.

The freeze attribute can be of type Boolean or Object. If it is of type Boolean, it shows the buttons that are set in the default settings. If it is of type Object, the following attributes apply:

| Name              | Required | Type   | Default      | Description                                                                               | Expert |
| ----------------- | -------- | ------ | ------------ | ----------------------------------------------------------------------------------------- | ------ |
| icon              | no       | String | "bi-lock"    | Using the icon parameter, a different icon can be used to switch back to the home screen. | false  |
| supportedDevices  | no       | String | ["Desktop"]  | Devices on which the module can be used and is displayed in the menu.                     | false  |
| supportedMapModes | no       | String | ["2D", "3D"] | Map modes in which the module can be used and is displayed in the menu.                   | false  |

***

##### portalConfig.map.controls.fullScreen {data-toc-label='Full Screen'}
Allows the user to view the portal in full screen mode by clicking a button without the browser's tabs and address bar, by clicking a button. A second click on the element returns the view back to default.

| Name              | Required | Type    | Default             | Description                                                                                                  | Expert |
| ----------------- | -------- | ------- | ------------------- | ------------------------------------------------------------------------------------------------------------ | ------ |
| iconArrow         | no       | String  | "arrows-fullscreen" | Using the iconArrow parameter, another icon can be used for the button to switch on fullscreen mode.         | false  |
| iconExit          | no       | String  | "fullscreen-exit"   | Using the iconExit parameter, another icon can be used for the button to exit fullscreen mode.               | false  |
| newTabFromFrame   | no       | Boolean | true                | If set to false gesetzt, using the control in an iFrame switch to full screen mode and don't open a new tab. | false  |
| supportedDevices  | no       | String  | ["Desktop"]         | Devices on which the module can be used and is displayed in the menu.                                        | false  |
| supportedMapModes | no       | String  | ["2D", "3D"]        | Map modes in which the module can be used and is displayed in the menu.                                      | false  |

**Example fullScreen as Object**

```json
"fullScreen" : {
    "iconArrow": "arrows-fullscreen",
    "iconExit": "fullscreen-exit",
    "newTabFromFrame": true
},
```

**Example fullScreen as Boolean**

```json
"fullScreen": true
```

***

##### portalConfig.map.controls.orientation {data-toc-label='Orientation'}
Orientation uses the browser's geolocation to determine the user's location. A list of features in the vicinity of the location is displayed.

| Name                     | Required | Type                   | Default                                                       | Description                                                                                                                                                                                                                                                                                | Expert |
| ------------------------ | -------- | ---------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| customPosition           | no       | String                 | "common:modules.controls.orientation.poiChoiceCustomPosition" | This can be used to control which text is displayed for `customPosition` in the poiChoice. The path specified here must correspond to the path for the parameter in the translation file.                                                                                                  | false  |
| iconGeolocate            | no       | String                 | "bi-geo-alt"                                                  | Icon that is displayed in the Controls menu for the control location. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**                                                                                                                                             | false  |
| iconGeolocatePOI         | no       | String                 | "bi-record-circle"                                            | Icon that is displayed in the Controls menu for the "Close to me" control. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**                                                                                                                                        | false  |
| iconGeolocationMarker    | no       | String                 | "bi-circle-fill"                                              | Icon that is displayed in the map to mark the current position. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**                                                                                                                                                   | false  |
| iFrameGeolocationEnabled | no       | Boolean                | false                                                         | If 'iFrameGeolocationEnabled' is true, orientation will try to fetch geolocation within an iFrame. This only works if the iFrame-Tag of the containing page has the attribute allow="geolocation".                                                                                         | false  |
| onlyFilteredFeatures     | no       | boolean                | false                                                         | If 'onlyFilteredFeatures' is true, only features filtered via the filter are taken into account in the poi results display.                                                                                                                                                                | false  |
| poiDistances             | no       | Boolean/Integer[]      | true                                                          | Defines whether the feature "Close to me", which shows a list of nearby points of interest, is provided. If an array is configured, multiple such lists with the given distance in meters are offered. When simply setting `poiDistances: true`, the used distances are `[500,1000,2000]`. | false  |
| supportedDevices         | no       | String                 | ["Desktop", "Mobile"]                                         | Devices on which the module can be used and is displayed in the menu.                                                                                                                                                                                                                      | false  |
| supportedMapModes        | no       | String                 | ["2D", "3D"]                                                  | Map modes in which the module can be used and is displayed in the menu.                                                                                                                                                                                                                    | false  |
| zoomMode                 | no       | enum["once", "always"] | "once"                                                        | The user's location is determined and a marker turned on or off. This requires providing the portal via **https**. Modes: *once* zooms to the user's location once, *always* zooms to the user position on each activation.                                                                | false  |

**Example using type boolean for poiDistances**

```json
"orientation": {
    "iconGeolocate": "bi-geo-alt",
    "iconGeolocatePOI": "bi-record-circle",
    "iconGeolocationMarker": "bi-circle-fill",
    "zoomMode": "once",
    "poiDistances": true
}
```

**Example using type number[] for poiDistances**

```json
"orientation": {
    "zoomMode": "once",
    "poiDistances": [500, 1000, 2000, 5000]
}
```

***

##### portalConfig.map.controls.rotation {data-toc-label='Rotation'}
Controls the display of 3 control buttons: "Reset rotation", "Rotate clockwise" and "Rotate counterclockwise" as well as the display of a compass rose for navigation in 2D and/or 3D. The compass rose is not displayed on mobile devices.
The rotation attribute can be of type Boolean or Object. If it is of the Boolean type and set to true, it only displays the "Reset rotation" button if the map rotation is not equal to north/0. The other two buttons are always displayed. The compass rose is then only displayed in 3D.
If it is of type Object, the following attributes apply:

| Name                       | Required | Type    | Default                     | Description                                                                                                                              | Expert |
| -------------------------- | -------- | ------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| compass2d                  | no       | Boolean | false                       | Controls the display of the compass rose in 2D.                                                                                          | false  |
| compass3d                  | no       | Boolean | true                        | Controls the display of the compass rose in 3D.                                                                                          | false  |
| moveDistance               | no       | Number  | 1000                        | Distance in meters, which is used when clicking on the movement arrows of the compass rose.                                              | false  |
| resetRotationIcon          | no       | String  | "bi-cursor"                 | Icon for the "Reset rotation" button. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**                           | false  |
| rotateCounterClockwiseIcon | no       | String  | "bi-arrow-counterclockwise" | Icon for the "Rotate counterclockwise" button. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**                  | false  |
| rotateClockwiseIcon        | no       | String  | "bi-arrow-clockwise"        | Icon for the "Rotate clockwise" button. For selection see **[Bootstrap Icons](https://icons.getbootstrap.com/)**                         | false  |
| rotationIcons              | no       | Boolean | true                        | The "Rotate clockwise" and "Rotate anticlockwise" buttons are displayed.                                                                 | false  |
| rotationAngle              | no       | Number  | 22.5                        | Angle by which the map is rotated when clicking on one of the rotate buttons.                                                            | false  |
| showResetRotation          | no       | Boolean | true                        | The "Reset rotation" button is displayed.                                                                                                | false  |
| showResetRotationAlways    | no       | Boolean | false                       | If the attribute is set to true, the control is shown permanently. Via default it appears only if the map rotation is not equal north/0. | false  |
| supportedDevices           | no       | String  | ["Desktop", "Mobile"]       | Devices on which the module can be used and is displayed in the menu.                                                                    | false  |
| supportedMapModes          | no       | String  | ["2D", "3D"]                | Map modes in which the module can be used and is displayed in the menu.                                                                  | false  |

**Example using type object rotation**

```json
"rotation": {
    "compass2d": true,
    "moveDistance": 2500,
    "showResetRotation": true,
    "showResetRotationAlways": false,
    "rotationIcons": false
}
```

**Example using type boolean rotation**

```json
"rotation": true
```

***

##### portalConfig.map.controls.startModule {data-toc-label='Start Module'}
The startModule attribute must be of type Object. A button is displayed for each configured module, which can be used to open and close the respective module.

| Name              | Required | Type                                                                    | Default                        | Description                                                                                                                            | Expert |
| ----------------- | -------- | ----------------------------------------------------------------------- | ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| mainMenu          | no       | **[mainMenu](#portalconfigmapcontrolsstartmodulemainmenu)**[]           |                                | Here you can configure the modules for which a button should be displayed. These will be displayed in the `mainMenu` when opened.      | false  |
| secondaryMenu     | no       | **[secondaryMenu](#portalconfigmapcontrolsstartmodulesecondarymenu)**[] |                                | Here you can configure the modules for which a button should be displayed. These will be displayed in the `secondaryMenu` when opened. | false  |
| supportedDevices  | no       | String                                                                  | ["Desktop", "Mobile", "Table"] | Devices on which the module can be used and is displayed in the menu.                                                                  | false  |
| supportedMapModes | no       | String                                                                  | ["2D", "3D"]                   | Map modes in which the module can be used and is displayed in the menu.                                                                | false  |

**Example**

```json
"startModule": {
    "mainMenu": [
        {
            "type": "scaleSwitcher"
        }
    ],
    "secondaryMenu": [
        {
            "type": "myModule"
        }
    ]
}
```

***

###### portalConfig.map.controls.startModule.mainMenu {data-toc-label='Main Menu'}
Here you can configure the modules for which a button is to be displayed. These are displayed in the `mainMenu` when opened.

| Name | Required | Type   | Default | Description                                                                                      | Expert |
| ---- | -------- | ------ | ------- | ------------------------------------------------------------------------------------------------ | ------ |
| type | no       | String |         | Type of the module that is to be displayed as a control and opened in the mainMenu when clicked. | false  |

**Example**

```json
"mainMenu": [
    {
        "type": "scaleSwitcher"
    }
]
```

***

###### portalConfig.map.controls.startModule.secondaryMenu {data-toc-label='Secondary Menu'}
Here you can configure the modules for which a button is to be displayed. These are displayed in the `secondaryMenu` when opened.

| Name | Required | Type   | Default | Description                                                                                           | Expert |
| ---- | -------- | ------ | ------- | ----------------------------------------------------------------------------------------------------- | ------ |
| type | no       | String |         | Type of the module that is to be displayed as a control and opened in the secondaryMenu when clicked. | false  |

**Example**

```json
"secondaryMenu": [
    {
        "type": "scaleSwitcher"
    }
]
```

***

##### portalConfig.map.controls.tiltView {data-toc-label='Tilt View'}
Displays two buttons that can be used to tilt the camera up or down in the 3D scene.

The tiltView attribute can be of type Boolean or Object. If it is of type Boolean, it shows the buttons that are set in the default settings. If it is of type Object, the following attributes apply:

| Name              | Required | Type   | Default                | Description                                                                        | Expert |
| ----------------- | -------- | ------ | ---------------------- | ---------------------------------------------------------------------------------- | ------ |
| tiltDownIcon      | no       | String | "bi-caret-down-square" | The tiltDownIcon parameter can be used to specify a different icon for tilt down.  | false  |
| tiltUpIcon        | no       | String | "bi-caret-up-square"   | Using the parameter tiltUpIcon another icon can be used for tilting up the camera. | false  |
| supportedDevices  | no       | String | ["Desktop"]            | Devices on which the module can be used and is displayed in the menu.              | false  |
| supportedMapModes | no       | String | ["3D"]                 | Map modes in which the module can be used and is displayed in the menu.            | false  |

**Example tiltView as Object**

```json
"tiltView" : {
    "tiltDownIcon": "bi-caret-down-square",
    "tiltUpIcon": "bi-caret-up-square",
},
```

**Example tiltView as boolean**

```json
"tiltView": true
```

***

##### portalConfig.map.controls.totalView {data-toc-label='Total View'}
Offers a button to return to the initial view.

The attribute totalView may be of type boolean or object. If of type boolean, it shows a button using the default configuration that allows the user to switch back to the initial view. When of type object, the following attributes may be set:

| Name              | Required | Type   | Default                 | Description                                                                               | Expert |
| ----------------- | -------- | ------ | ----------------------- | ----------------------------------------------------------------------------------------- | ------ |
| icon              | no       | String | "bi-skip-backward-fill" | Using the icon parameter, a different icon can be used to switch back to the home screen. | false  |
| supportedDevices  | no       | String | ["Desktop"]             | Devices on which the module can be used and is displayed in the menu.                     | false  |
| supportedMapModes | no       | String | ["2D", "3D"]            | Map modes in which the module can be used and is displayed in the menu.                   | false  |

**Example totalView as Object**

```json
"totalView" : {
    "icon": "bi-skip-forward-fill"
},
```

**Example totalView as Boolean**

```json
"totalView": true
```

***

##### portalConfig.map.controls.zoom {data-toc-label='Zoom'}
Defines whether zoom buttons should be displayed.

The attribute zoom may be of type boolean or object. If of type boolean, it shows two buttons using the default configuration that allows the user to zoom in the map. When of type object, the following attributes may be set:

| Name              | Required | Type   | Default      | Description                                                             | Expert |
| ----------------- | -------- | ------ | ------------ | ----------------------------------------------------------------------- | ------ |
| iconIn            | no       | String | "bi-plus-lg" | Using the icon parameter, another icon can be used for zooming in.      | false  |
| iconOut           | no       | String | "bi-dash-lg" | Using the icon parameter, another icon can be used for zooming out.     | false  |
| supportedDevices  | no       | String | ["Desktop"]  | Devices on which the module can be used and is displayed in the menu.   | false  |
| supportedMapModes | no       | String | ["2D", "3D"] | Map modes in which the module can be used and is displayed in the menu. | false  |

**Example zoom as Object**

```json
"zom" : {
    "iconIn": "bi-plus-lg",
    "iconOut": "bi-dash-lg"
},
```

**Example zoom as Boolean**

```json
"zoom": true
```

***

#### portalConfig.map.featureViaURL {data-toc-label='Feature Via URL'}
Optional configuration for the URL parameter `featureViaURL`. See **[urlParameter](../Misc/urlParameter.md)** for details.

| Name   | Required | Type                                                | Default | Description                                                                                                                                                                          | Expert |
| ------ | -------- | --------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| epsg   | no       | Integer                                             | 4326    | EPSG code for coordinate reference system to translate coordinates to.                                                                                                               | false  |
| layers | yes      | **[layers](#portalconfigmapfeatureviaurllayers)**[] |         | Layer configuration array for given features.                                                                                                                                        | false  |
| zoomTo | no       | String/String[]                                     |         | Id of **[layers](#portalconfigmapfeatureviaurllayers)** or array thereof, to which the Masterportal initially zooms. If none are given, the usual initial center coordinate is used. | false  |

**Example:**

```json
{
    "featureViaURL": {
        "epsg": 25832,
        "zoomTo": "urlPointFeatures",
        "layers": [
            {
                "id": "urlPointFeatures",
                "geometryType": "Point",
                "name": "URL Point Features",
                "styleId": "url_points"
            },
            {
                "id": "urlLineFeatures",
                "geometryType": "LineString",
                "name": "URL Line Features",
                "styleId": "url_lines"
            },
            {
                "id": "urlPolygonFeatures",
                "geometryType": "Polygon",
                "name": "URL Polygon Features",
                "styleId": "url_polygons"
            },
            {
                "id": "urlMultiPointFeatures",
                "geometryType": "MultiPoint",
                "name": "URL MultiPoint Features",
                "styleId": "url_mulitpoints"
            },
            {
                "id": "urlMultiLineStringFeatures",
                "geometryType": "MultiLineString",
                "name": "URL MultiLineString Features",
                "styleId": "url_multilinestring"
            },
            {
                "id": "urlMultiPolygonFeatures",
                "geometryType": "MultiPolygon",
                "name": "URL MultiPolygon Features",
                "styleId": "url_multipolygons"
            }
        ]
    }
}
```

***

##### portalConfig.map.featureViaURL.layers {data-toc-label='Layers'}
The parameters described apply for each entry of the **[layers](#portalconfigmapfeatureviaurllayers)** array.

| Name         | Required | Type                                                                                    | Default | Description                                                                                             | Expert |
| ------------ | -------- | --------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------- | ------ |
| id           | yes      | String                                                                                  |         | unique ID for the layer to be created                                                                   | false  |
| geometryType | yes      | enum["LineString", "Point", "Polygon", "MultiPoint", "MultiLineString", "MultiPolygon"] |         | Geometry type of the feature to be shown.                                                               | false  |
| name         | yes      | String                                                                                  |         | Layer name displayed in the layer tree, the legend, and the GFI pop-up.                                 | false  |
| styleId      | no       | String                                                                                  |         | Style id to be used for the feature, referring to the **[style.json](../Global-Config/style.json.md)**. | false  |

**Example:**

```json
{
    "layers": [{
        "id": "urlPolygonFeatures",
        "geometryType": "Polygon",
        "name": "URL Polygon Features",
        "styleId": "url_polygons"
    }]
}
```

***

#### portalConfig.map.getFeatureInfo {data-toc-label='Get Feature Info'}
Displays information to a clicked feature by firing a *GetFeatureInfo* or *GetFeature* request, respectively using the loaded data on vector layers.

On all GFI request types except directly fetching HTML, which is done by using `"text/html"` as `"infoFormat"` on a WMS, the "|" character is interpreted as linebreak. You may also use `"\r\n"` or `"\n"`.

| Name                           | Required | Type                                                                             | Default                              | Description                                                                                                | Expert |
| ------------------------------ | -------- | -------------------------------------------------------------------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------- | ------ |
| centerMapToClickPoint          | no       | Boolean                                                                          | false                                | If true, centers any clicked feature on the map.                                                           | false  |
| coloredHighlighting3D          | no       | **[coloredHighlighting3D](#portalconfigmapgetfeatureinfocoloredhighlighting3d)** |                                      | Rule definition to override the highlighting of clicked 3D tiles.                                          | false  |
| hideMapMarkerOnVectorHighlight | no       | Boolean                                                                          | false                                | If set to true, the mapmarker won't be shown on vector highlighting. Only applies for the DetachedTemplate | false  |
| highlightVectorRules           | no       | **[highlightVectorRules](#portalconfigmapgetfeatureinfohighlightvectorrules)**   |                                      | Rule definition to override the styling of clicked vector data.                                            | false  |
| icon                           | no       | String                                                                           | "bi-info-circle-fill"                | CSS icon class. Icon is shown before the tool name.                                                        | false  |
| menuSide                       | no       | String                                                                           | "secondaryMenu"                      | Specifies in which menu the information should be displayed.                                               | false  |
| name                           | yes      | String                                                                           | "common:modules.getFeatureInfo.name" | Name displayed in the menu.                                                                                | false  |
| showPolygonMarkerForWMS        | no       | Boolean                                                                          | false                                | If set to true, Polygonmarker will be shown for WMS features with geometry.                                | false  |

**Example of a GetFeatureInfo configuration**.

```json
"getFeatureInfo": {
    "name": "Request information",
    "icon": "bi-info-circle-fill",
    "coloredHighlighting3D": {
        "enabled": true,
        "color": "GREEN"
    },
    "highlightVectorRules": {
        "fill": {
            "color": [215, 102, 41, 0.9]
        },
        "image": {
            "scale": 1.5
        },
        "stroke": {
            "width": 4
        },
        "text": {
            "scale": 2
        }
    },
    "showPolygonMarkerForWMS": true,
    "hideMapMarkerOnVectorHighlight": true
}
```

**Example of a GetFeatureInfo configuration to retrieve information from features**.

```json
"getFeatureInfo": {
    "name": "Request information"
}
```

***

##### portalConfig.map.getFeatureInfo.coloredHighlighting3D {data-toc-label='Colored Highlighting 3D'}
Highlight Setting of 3D Tiles.
If e.g. a building is selected by left mouse click, it will be highlighted in the given color.
For color configuration see **[Color-documentation](https://cesium.com/learn/cesiumjs/ref-doc/Color.html)**

| Name  | Required | Type            | Default | Description                                                                                      | Expert |
| ----- | -------- | --------------- | ------- | ------------------------------------------------------------------------------------------------ | ------ |
| color | no       | String/String[] | "RED"   | Color can be configured as Array or Cesium.Color (definition e.g "GREEN" for Cesium.Color.GREEN) | false  |

**Example**

```json
"coloredHighlighting3D": {
    "enabled": true,
    "color": "GREEN"
}
```

***

##### portalConfig.map.getFeatureInfo.highlightVectorRules {data-toc-label='Highlight Vector Rules'}

[type:Image]: # (Datatypes.Image)
[type:Fill]: # (Datatypes.Fill)
[type:Stroke]: # (Datatypes.Stroke)

Configuration list to overwrite vector styles on gfi requests.

Hint: highlighting only works if there is a styleId in config.json configured for the layer.

| Name   | Required | Type                                                               | Default              | Description             | Expert |
| ------ | -------- | ------------------------------------------------------------------ | -------------------- | ----------------------- | ------ |
| fill   | no       | **[fill](#datatypesfill)**                                         | [255, 255, 255, 0.5] | Settable field: `color` | false  |
| image  | no       | **[image](#datatypesimage)**                                       | 1                    | Settable field: `scale` | false  |
| stroke | no       | **[stroke](#datatypesstroke)**                                     | 1                    | Settable field: `width` | false  |
| text   | no       | **[text](#portalconfigmapgetfeatureinfohighlightvectorrulestext)** |                      | Settable field: `scale` | false  |

***

###### portalConfig.map.getFeatureInfo.highlightVectorRules.text {data-toc-label='Text'}
| Name  | Required | Type  | Default | Description       | Expert |
| ----- | -------- | ----- | ------- | ----------------- | ------ |
| scale | no       | Float | 1       | Text scale number | false  |

**Example**

```json
"text": {
    "scale": 2
}
```

***

#### portalConfig.map.layerPills {data-toc-label='Layer Pills'}
Configuration to make settings for LayerPills.

Layerpills are buttons on top of the map that show the selected layers. When clicking on a LayerPill, the corresponding layer information is displayed in the menu. The close button deselects the layer. The LayerPills attribute is specified as an object and contains the following attributes:

| Name       | Required | Type    | Default | Description                                                             | Expert |
| ---------- | -------- | ------- | ------- | ----------------------------------------------------------------------- | ------ |
| active     | no       | Boolean | false   | Indicates whether LayerPills are active.                                | false  |
| mobileOnly | no       | Boolean | false   | Defines whether LayerPills should only be active in the mobile version. | false  |

**Example**

```json
"layerPills": {
    "active": true,
    "mobileOnly": true
}
```

***

#### portalConfig.map.map3dParameter {data-toc-label='Map 3D Parameter'}
Cesium Scene settings in 3D mode.
For more attributes see **[Scene](https://cesium.com/learn/cesiumjs/ref-doc/Scene.html?classFilter=scene)**

| Name                    | Required | Type                                               | Default        | Description                                                                                                                                                                                                                                                      | Expert |
| ----------------------- | -------- | -------------------------------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| camera                  | no       | **[camera](#portalconfigmapmap3dparametercamera)** |                | Cesium Scene camera settings in 3D mode.                                                                                                                                                                                                                         | false  |
| fog                     | no       | **[fog](#portalconfigmapmap3dparameterfog)**       |                | Cesium Scene fog settings in 3D mode.                                                                                                                                                                                                                            | false  |
| fxaa                    | no       | Boolean                                            | true           | activates *fast approximate anti-aliasing*                                                                                                                                                                                                                       | false  |
| globe                   | no       | **[globe](#portalconfigmapmap3dparameterglobe)**   |                | Cesium Scene globe settings in 3D mode.                                                                                                                                                                                                                          | false  |
| maximumScreenSpaceError | no       | Number                                             | 2.0            | Detail level in which terrain/raster tiles are fetched. 4/3 is the highest quality level.                                                                                                                                                                        | false  |
| tileCacheSize           | no       | Number                                             | 100            | terrain/raster tile cache size                                                                                                                                                                                                                                   | false  |
| shadowTime              | no       | String                                             | "current time" | Sets the time used to calculate shadows in 3D mode. Use the ISO-8601 string format. If not provided, shadows are calculated based on the current system time. Useful for freezing shadows for presentations or consistent visualization at a specific date/time. | false  |

**Example**

```json
{
    "camera": {
        "altitude": 127,
        "heading": -1.2502079000000208,
        "tilt": 45
    },
    "fog": {
        "enabled": true
    },
    "fxaa": true,
    "globe": {
        "enableLighting": true
    },
    "maximumScreenSpaceError": 2,
    "tileCacheSize": 20,
    "shadowTime": "2025-07-01T12:00:00Z"
}
```

***

##### portalConfig.map.map3dParameter.camera {data-toc-label='Camera'}
Cesium Scene camera settings in 3D mode.
The camera is defined by a position, orientation, and view frustum.
For more attributes see **[Scene](https://cesium.com/learn/cesiumjs/ref-doc/Camera.html)**

| Name           | Required | Type   | Default | Description                                                                                                                                                                                             | Expert |
| -------------- | -------- | ------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| altitude       | no       | Number | 0       | Camera's initial height in meters. Not used if `cameraPosition` is set.                                                                                                                                 | false  |
| cameraPosition | no       | enum   |         | Camera position containing longitude, latitude and height in meters, above the ellipsoid. If this is set, `pitch` and `roll` are used to create the direction. `Altitude` and `tilt` are not used then. | false  |
| heading        | no       | Number | 0       | Camera's initial heading in radians. Is always used.                                                                                                                                                    | false  |
| pitch          | no       | Number | 0       | Camera's initial pitch value. Only used if `cameraPosition` is set.                                                                                                                                     | false  |
| roll           | no       | Number | 0       | Camera's initial roll value. Only used if `cameraPosition` is set.                                                                                                                                      | false  |
| tilt           | no       | Number | 0       | Camera's initial tile in radians. Not used if `cameraPosition` is set.                                                                                                                                  | false  |

**Example**

```json
{
    "camera": {
        "altitude": 127,
        "heading": -1.2502079000000208,
        "tilt": 45
    }
}
```

**Example with cameraPosition**

```json
{
    "camera": {
        "heading": 0.5094404418943017,
        "pitch": -40.0515352133474,
        "cameraPosition": [9.9914497197391, 53.545716220545344, 421.1102528528311]
    }
}
```

***

##### portalConfig.map.map3dParameter.fog {data-toc-label='Fog'}
Cesium Scene fog settings in 3D mode.
Blends the atmosphere to geometry far from the camera for horizon views.
For more attributes see **[Scene](https://cesium.com/learn/cesiumjs/ref-doc/Fog.html)**

| Name    | Required | Type    | Default | Description             | Expert |
| ------- | -------- | ------- | ------- | ----------------------- | ------ |
| enabled | no       | Boolean | false   | True if fog is enabled. | false  |

**Example**

```json
{
    "fog": {
        "enabled": true
    }
}
```

***

##### portalConfig.map.map3dParameter.globe {data-toc-label='Globe'}
Cesium Scene globe settings in 3D mode.
The globe rendered in the scene, including its terrain and imagery layers.
For more attributes see **[Scene](https://cesium.com/learn/cesiumjs/ref-doc/Globe.html)**

| Name           | Required | Type    | Default | Description                                                     | Expert |
| -------------- | -------- | ------- | ------- | --------------------------------------------------------------- | ------ |
| enableLighting | no       | Boolean | false   | Activates light effects on the map based on the sun's position. | false  |

**Example**

```json
{
    "globe": {
        "enableLighting": true
    }
}
```

***

#### portalConfig.map.mapMarker {data-toc-label='Map Marker'}
Overrides the map marker module's default values. Useful for 3D markers since OpenLayers's overlays can not be displayed in 3D mode. For this, the map marker has to be defined as vector layer.

| Name                     | Required | Type   | Default                             | Description                                                                                  | Expert |
| ------------------------ | -------- | ------ | ----------------------------------- | -------------------------------------------------------------------------------------------- | ------ |
| pointStyleId             | no       | String | "defaultMapMarkerPoint"             | StyleId to refer to a `style.json` point style. If not set, the `img/mapMarker.svg` is used. | false  |
| polygonStyleId           | no       | String | "defaultMapMarkerPolygon"           | StyleId to refer to a `style.json` polygon style.                                            | false  |
| additionalPolygonStyleId | no       | String | "defaultAdditionalMapMarkerPolygon" | StyleId to refer to an additional `style.json` polygon style.                                | false  |

**Example:**

```json
{
    "mapMarker": {
        "pointStyleId": "customMapMarkerPoint",
        "polygonStyleId": "customMapMarkerPolygon",
        "additionalPolygonStyleId": "customAdditionalMapMarkerPolygon"
    }
}
```

***

#### portalConfig.map.mapView {data-toc-label='Map View'}

[type:Coordinate]: # (Datatypes.Coordinate)

Defines the initial map view and a background shown when no layer or map is selected.

| Name            | Required | Type                                                          | Default                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Description                                                                                                                    | Expert |
| --------------- | -------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------ |
| backgroundImage | no       | String                                                        | "https://bitbucket.org/geowerkstatt-hamburg/masterportal/src/dev/doc/config.json.md#portalconfigmapview"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Path to an alternative background image.                                                                                       | false  |
| epsg            | no       | String                                                        | "EPSG:25832"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Coordinate reference system EPSG code. The code must be defined as a `namedProjection`.                                        | false  |
| extent          | no       | **[Extent](#datatypesextent)**                                | [510000.0, 5850000.0, 625000.4, 6000000.0]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Map extent - map may not be moved outside these boundaries.                                                                    | false  |
| mapInteractions | nein     | **[mapInteractions](#portalconfigmapmapviewmapinteractions)** |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Overrides the ol map interactions. Provides further configuration possibilities for control behaviour and keyboardEventTarget. | false  |
| options         | no       | **[option](#portalconfigmapmapviewoption)**[]                 | [{"resolution":66.14579761460263,"scale":250000,"zoomLevel":0}, {"resolution":26.458319045841044,"scale":100000,"zoomLevel":1}, {"resolution":15.874991427504629,"scale":60000,"zoomLevel":2}, {"resolution": 10.583327618336419,"scale":40000,"zoomLevel":3}, {"resolution":5.2916638091682096,"scale":20000,"zoomLevel":4}, {"resolution":2.6458319045841048,"scale":10000,"zoomLevel":5}, {"resolution":1.3229159522920524,"scale":5000,"zoomLevel":6}, {"resolution":0.6614579761460262,"scale":2500,"zoomLevel":7}, {"resolution":0.2645831904584105,"scale": 1000,"zoomLevel":8}, {"resolution":0.13229159522920521,"scale":500,"zoomLevel":9}] | Available scale levels and their resolutions.                                                                                  | false  |
| startCenter     | no       | **[Coordinate](#datatypescoordinate)**                        | [565874, 5934140]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | The initial center coordinate.                                                                                                 | false  |
| startResolution | no       | Float                                                         | 15.874991427504629                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | The initial map resolution from the `options` element. Used in preference to `startZoomLevel`.                                 | false  |
| startZoomLevel  | no       | Integer                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | The initial map zoom level from the `options` element. If `resolutions` is set, this is ignored.                               | false  |

**Example**

```json
{
    "mapView": {
        "backgroundImage": "https://geodienste.hamburg.de/lgv-config/img/backgroundCanvas.jpeg",
        "startCenter": [561210, 5932600],
        "options": [
            {
                "resolution": 611.4974492763076,
                "scale": 2311167,
                "zoomLevel": 0
            },
            {
                "resolution": 305.7487246381551,
                "scale": 1155583,
                "zoomLevel": 1
            },
            {
                "resolution": 152.87436231907702,
                "scale": 577791,
                "zoomLevel": 2
            },
            {
                "resolution": 76.43718115953851,
                "scale": 288896,
                "zoomLevel": 3
            },
            {
                "resolution": 38.21859057976939,
                "scale": 144448,
                "zoomLevel": 4
            },
            {
                "resolution": 19.109295289884642,
                "scale": 72223,
                "zoomLevel": 5
            },
            {
                "resolution": 9.554647644942321,
                "scale": 36112,
                "zoomLevel": 6
            },
            {
                "resolution": 4.7773238224711605,
                "scale": 18056,
                "zoomLevel": 7
            },
            {
                "resolution": 2.3886619112355802,
                "scale": 9028,
                "zoomLevel": 8
            },
            {
                "resolution": 1.1943309556178034,
                "scale": 4514,
                "zoomLevel": 9
            },
            {
                "resolution": 0.5971654778089017,
                "scale": 2257,
                "zoomLevel": 10
            }
        ],
        "extent": [510000.0, 5850000.0, 625000.4, 6000000.0],
        "StartResolution": 15.874991427504629,
        "StartZoomLevel": 1,
        "epsg": "EPSG:25832"
    }
}
```

***

##### portalConfig.map.mapView.mapInteractions {data-toc-label='Map Interactions'}
Overrides the ol map interactions. Provides further configuration possibilities for control behaviour and keyboardEventTarget.

| Name                | Required | Type                                                                           | Default                                                               | Description                                                                                    | Expert |
| ------------------- | -------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------ |
| interactionModes    | no       | **[interactionModes](#portalconfigmapmapviewmapinteractionsinteractionmodes)** | {"dragPan": false, "altShiftDragRotate": false, "pinchRotate": false} | Interaction settings for the ol default interactions. If not set, the default setting is used. | false  |
| keyboardEventTarget | no       | Boolean                                                                        | false                                                                 | Possibility to set the keyboard event target for the ol map e.g keyboardEventTarget: document  | false  |

**Example:**

```json
{
    "mapInteractions": {
        "interactionModes": {
            "dragPan": false,
            "altShiftDragRotate": true,
            "pinchRotate": false,
            "dragZoom": true
        },
        "keyboardEventTarget": false
    }
}
```

***

##### portalConfig.map.mapView.mapInteractions.interactionModes {data-toc-label='Interaction Modes'}
Interaction settings for the ol default interactions. If not set, the default setting is used.

| Name               | Required | Type    | Default | Description                                                                       | Expert |
| ------------------ | -------- | ------- | ------- | --------------------------------------------------------------------------------- | ------ |
| altShiftDragRotate | no       | Boolean | true    | Rotate the map with alt + shift + drag.                                           | false  |
| dragPan            | no       | Boolean | false   | Allows the user to move the map by dragging it.                                   | false  |
| dragZoom           | no       | Boolean | false   | Allows the user to zoom the map by clicking and dragging on the map.              | false  |
| pinchRotate        | no       | Boolean | false   | Allows the user to rotate the map by twisting with two fingers on a touch screen. | false  |
| twoFingerPan       | no       | Boolean | false   | Should a 2-Finger-Pan be set on mobile devices instead of a 1-Finger-Pan?         | false  |

**Example**

```json
"interactionModes": {
    "dragPan": false,
    "altShiftDragRotate": true,
    "pinchRotate": false,
    "dragZoom": true,
    "twoFingerPan": true
}
```

***

##### portalConfig.map.mapView.option {data-toc-label='Option'}
An option defines a zoom level. Each zoom level is defined by resolution, scale number, and a unique zoom level. The higher the zoom level, the smaller the scale and the closer you have zoomed.

| Name       | Required | Type    | Default | Description                         | Expert |
| ---------- | -------- | ------- | ------- | ----------------------------------- | ------ |
| resolution | yes      | Number  |         | Zoom level definition's resolution. | false  |
| scale      | yes      | Integer |         | Zoom level definition's scale.      | false  |
| zoomLevel  | yes      | Integer |         | Zoom level definition's zoom level. | false  |

**mapView option example**

```json
{
    "resolution": 611.4974492763076,
    "scale": 2311167,
    "zoomLevel": 0
}
```

***

#### portalConfig.map.mouseHover {data-toc-label='Mouse Hover'}
Enables the MouseHover function for vector layers, e.g. WFS or GeoJSON. For per-layer configuration see **[Vector](#layerconfigelementslayersvector)**.

| Name                          | Required | Type                                                                                         | Default                                      | Description                                                                                                                                        | Expert |
| ----------------------------- | -------- | -------------------------------------------------------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| infoText                      | no       | String                                                                                       | "common:modules.mouseHover.infoText"         | Text that will be displayed if the features exceed the number of `numFeaturesToShow`.                                                              | false  |
| numFeaturesToShow             | no       | Integer                                                                                      | 2                                            | Maximum amount of element information per tooltip; when exceeded, an information text informs the user of cut content.                             | false  |
| fontFamily                    | no       | String                                                                                       | "common:modules.mouseHover.fontFamily"       | Font family for the description                                                                                                                    | false  |
| fontStyle                     | no       | String                                                                                       | "common:modules.mouseHover.fontStyle"        | Font style for the description                                                                                                                     | false  |
| fontWeight                    | no       | String                                                                                       | "common:modules.mouseHover.fontWeight"       | Font weight for the description                                                                                                                    | false  |
| fontSize                      | no       | String                                                                                       | "common:modules.mouseHover.fontSize"         | Font size for the description                                                                                                                      | false  |
| fontColor                     | no       | String                                                                                       | "common:modules.mouseHover.fontColor"        | Font color for the description                                                                                                                     | false  |
| titleFontFamily               | no       | String                                                                                       | "common:modules.mouseHover.titleFontFamily"  | Font family for the title                                                                                                                          | false  |
| titleFontStyle                | no       | String                                                                                       | "common:modules.mouseHover.titleFontStyle"   | Font style for the title                                                                                                                           | false  |
| titleFontWeight               | no       | String                                                                                       | "common:modules.mouseHover.titleFontWeight"  | Font weight for the title                                                                                                                          | false  |
| titleFontSize                 | no       | String                                                                                       | "common:modules.mouseHover.titleFontSize"    | Font size for the title                                                                                                                            | false  |
| titleFontColor                | no       | String                                                                                       | "common:modules.mouseHover.titleFontColor"   | Font color for the title                                                                                                                           | false  |
| infoBorderRadius              | no       | Integer                                                                                      | "common:modules.mouseHover.infoBorderRadius" | Border radius of the tooltip                                                                                                                       | false  |
| lineHeight                    | no       | Float                                                                                        | "common:modules.mouseHover.lineHeight"       | Line spacing for the tooltip                                                                                                                       | false  |
| highlightOnHover              | no       | Boolean                                                                                      | false                                        | If hovered features should be highlighted                                                                                                          | false  |
| highlightVectorRulesPolygon   | no       | **[highlightVectorRulesPolygon](#portalconfigmapmousehoverhighlightvectorrulespolygon)**     |                                              | Specify the fill color and outline color and stroke width for highlighting the polygon features as well as a zoom parameter.                       | false  |
| highlightVectorRulesPointLine | no       | **[highlightVectorRulesPointLine](#portalconfigmapmousehoverhighlightvectorrulespointline)** |                                              | Specify outline color and stroke width for highlighting lines and fill color and scale factor for highlighting points as well as a zoom parameter. | false  |

**Example**

```json
{
    "mouseHover": {
        "numFeaturesToShow": 1,
        "infoText": "Exampletext",
        "fontFamily": "Arial",
        "fontStyle": "Italic",
        "fontWeight": "Normal",
        "fontSize": 12,
        "fontColor": "#FF0000",
        "titleFontFamily": "Helvetica",
        "titleFontStyle": "Normal",
        "titleFontWeight": "Bold",
        "titleFontSize": 16,
        "titleFontColor": "#1A43BF",
        "infoBorderRadius": 4,
        "lineHeight": 1.6,
        "highlightOnHover": true,
        "highlightVectorRulesPolygon": {
            "fill": {
                "color": [255, 255, 255, 0.5]
            },
            "stroke": {
                "width": 4,
                "color": [255, 0, 0, 0.9]
            }
        },
        "highlightVectorRulesPointLine": {
            "stroke": {
                "width": 8,
                "color": [255, 0, 255, 0.9]
            },
            "image": {
                "scale": 2
            }
        }
    }
}
```

***

##### portalConfig.map.mouseHover.highlightVectorRulesPolygon {data-toc-label='HighlightVectorRulesPolygon'}

Specify the fill color and outline color and stroke width for highlighting the polygon features as well as a zoom level.

| Name   | Required | Type                                                                                | Default | Description             | Expert |
| ------ | -------- | ----------------------------------------------------------------------------------- | ------- | ----------------------- | ------ |
| fill   | no       | **[fill](#portalconfigmapmousehovermousehoverhighlightvectorrulespolygonfill)**     |         | Possible setting: color | false  |
| stroke | no       | **[stroke](#portalconfigmapmousehovermousehoverhighlightvectorrulespolygonstroke)** |         | Possible setting: width | false  |

***

###### portalConfig.map.mouseHover.highlightVectorRulesPolygon.fill {data-toc-label='Fill'}
| Name  | Required | Type    | Default              | Description                    | Expert |
| ----- | -------- | ------- | -------------------- | ------------------------------ | ------ |
| color | no       | Float[] | [255, 255, 255, 0.5] | Possible setting: color (RGBA) | false  |

```json
"fill": {
    "color": [215, 102, 41, 0.9]
}
```

***

###### portalConfig.map.mouseHover.highlightVectorRulesPolygon.stroke {data-toc-label='Stroke'}
| Name  | Required | Type    | Default          | Description                    | Expert |
| ----- | -------- | ------- | ---------------- | ------------------------------ | ------ |
| width | no       | Integer | 1                | Possible setting: width        | false  |
| color | no       | Float[] | [255, 0, 0, 0.9] | Possible setting: color (RGBA) | false  |

```json
"stroke": {
    "width": 4 ,
    "color": [255, 0, 255, 0.9]
}
```

***


##### portalConfig.map.mouseHover.highlightVectorRulesPointLine {data-toc-label='HighlightVectorRulesPointLine'}

Specify outline color and stroke width for highlighting lines and fill color and scale factor for highlighting points. Also a zoom level.

| Name   | Required | Type                                                                                  | Default | Description             | Expert |
| ------ | -------- | ------------------------------------------------------------------------------------- | ------- | ----------------------- | ------ |
| fill   | no       | **[fill](#portalconfigmapmousehovermousehoverhighlightvectorrulespointlinefill)**     |         | Possible setting: color | false  |
| stroke | no       | **[stroke](#portalconfigmapmousehovermousehoverhighlightvectorrulespointlinestroke)** |         | Possible setting: width | false  |
| image  | no       | **[image](#portalconfigmapmousehovermousehoverhighlightvectorrulespointlineimage)**   |         | Possible setting: scale | false  |

***
###### portalConfig.map.mouseHover.highlightVectorRulesPointLine.fill {data-toc-label='Fill'}
| Name  | Required | Type    | Default              | Description                    | Expert |
| ----- | -------- | ------- | -------------------- | ------------------------------ | ------ |
| color | no       | Float[] | [255, 255, 255, 0.5] | Possible setting: color (RGBA) | false  |

```json
"fill": {
    "color": [215, 102, 41, 0.9]
}
```

***

###### portalConfig.map.mouseHover.highlightVectorRulesPointLine.stroke {data-toc-label='Stroke'}
| Name  | Required | Type    | Default              | Description                    | Expert |
| ----- | -------- | ------- | -------------------- | ------------------------------ | ------ |
| width | no       | Integer | 1                    | Possible setting: width        | false  |
| color | no       | Float[] | [255, 255, 255, 0.5] | Possible setting: color (RGBA) | false  |

```json
"stroke": {
    "width": 4 ,
    "color": [255, 0, 255, 0.9]
}
```

***

###### portalConfig.map.mouseHover.highlightVectorRulesPointLine.image {data-toc-label='Image'}
| Name  | Required | Type    | Default | Description             | Expert |
| ----- | -------- | ------- | ------- | ----------------------- | ------ |
| scale | no       | Integer | 1.5     | Possible setting: scale | false  |

```json
"image": {
    "scale": 2
}
```

***

#### portalConfig.map.zoomTo {data-toc-label='Zoom To'}
Configuration for the URL query parameters `zoomToFeatureId` and `zoomToGeometry`.

| Name          | Required | Type                                      | Default | Description                                                                                                                                    | Expert |
| ------------- | -------- | ----------------------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| addFeatures   | no       | Boolean                                   | true    | Specifies whether the desired features should be added to the map in a separate layer.                                                         | false  |
| allowedValues | no       | String[]                                  |         | Only relevant when `id` equal `zoomToGeometry`. Further filters the values allowed in the URL query parameters.                                | false  |
| id            | yes      | enum["zoomToFeatureId", "zoomToGeometry"] |         | Id of the URL query parameter the configuration refers to.                                                                                     | false  |
| layerId       | yes      | String                                    |         | Id of the layer the feature should be fetched from.                                                                                            | false  |
| property      | yes      | String                                    |         | Name of the property the features should be filtered by.                                                                                       | false  |
| styleId       | no       | String                                    |         | Only relevant when `id` equal `zoomToFeatureId`. Id of the `styleObject` that should be used to style the features retrieved from the service. | false  |

**Example**:

```json
{
    "zoomTo": [
        {
            "id": "zoomToGeometry",
            "layerId": "1692",
            "property": "bezirk_name",
            "allowedValues": [
                "ALTONA",
                "HARBURG",
                "HAMBURG-NORD",
                "BERGEDORF",
                "EIMSBÜTTEL",
                "HAMBURG-MITTE",
                "WANDSBEK"
            ]
        },
        {
            "id": "zoomToFeatureId",
            "layerId": "4560",
            "property": "flaechenid",
            "styleId": "location_eventlotse"
        }
    ]
}
```

***
