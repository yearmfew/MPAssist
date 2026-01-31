Module: about
Module ID (Key): about
Module Name: About

Description and Purpose
The About module provides visitors with a concise overview of the portal, highlighting its mission, version details, credits, and key contacts so stakeholders immediately understand the map’s context and ownership.

Dependencies
- Requires a slot in the main menu or secondary menu so users can open the legal and metadata dialog while navigating the portal.
- Depends on accessible metadata endpoints (cswUrl, metaUrl, metaId, and optional privacy or accessibility URLs) but has no map or layer prerequisites.
- Can be invoked from other modules such as layerInformation when users follow metadata links.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "about",
	"cswUrl": "https://metaver.de/csw",
	"metaUrl": "https://metaver.de/trefferanzeige?docuuid=40D48B03-AD1D-407B-B04D-B5BC6855BE15",
	"metaId": "40D48B03-AD1D-407B-B04D-B5BC6855BE15"
}
```

Module: addWMS
Module ID (Key): addWMSj
Module Name: Add WMS

Description and Purpose
The Add WMS module lets power users plug external Web Map Service endpoints into the portal on demand, enabling rapid access to new map layers by entering a service URL, browsing its layer list, and toggling selected content for instant visualization.

Dependencies
- Must be exposed through map.controls.startModule or a menu entry so users can open the dialog while the map is active.
- Requires the layer catalog (layerTree/layerSelection) to accept the imported WMS layers, including folder placement and visibility handling.
- Relies on reachable third-party WMS services provided by the user at runtime.

Example Config Entry (portal/master/config.json)
```json
{
	"map": {
		"controls": {
			"startModule": {
				"secondaryMenu": [
					{
						"type": "addWMS"
					}
				]
			}
		}
	}
}
```

Module: alerting
Module ID (Key): alerting
Module Name: Alerting

Description and Purpose
The Alerting module surfaces time-sensitive announcements such as maintenance notices, emergency hints, or policy updates directly inside the portal interface so every visitor is aware of critical changes before interacting with the map.

Dependencies
- Operates at portal scope and therefore needs to be initialized in portalConfig.alerts (config.json) or via alerting.fetchBroadcastUrl (config.js) to know which messages to show.
- Stores dismissed alerts in browser storage (localStorageDisplayedAlertsKey) so the same user is not interrupted repeatedly.
- Has no direct dependency on map layers but often links to modules like shareView or menu to guide users toward impacted content.

Example Config Entry (docs/User/Portal-Config/config.js.md example adapted for config.json)
```json
{
	"portalConfig": {
		"alerts": {
			"qs-release": {
				"category": "Portal zur Abnahme!",
				"content": "Dieses Geoportal dient der Qualitätskontrolle durch den Kunden.<br>Es ist aufgrund von möglichen Fehlern <b>nicht</b> zur Nutzung für alltägliche oder berufliche Aufgaben geeignet!",
				"creationDate": "01/09/22",
				"mustBeConfirmed": true,
				"once": false
			}
		}
	}
}
```

Module: baselayerSwitcher
Module ID (Key): baselayerSwitcher
Module Name: Baselayer Switcher

Description and Purpose
The Baselayer Switcher module gives users quick control over background cartography, letting them toggle between aerial imagery, vector streets, grayscale canvases, or other base layers to set the visual foundation for thematic overlays.

Dependencies
- Requires the map.baselayerSwitcher block plus configured baselayers inside layerConfig.baselayer.elements.
- Works together with layerSelection and layerTree to ensure only one baselayer is active at a time.
- Depends on the map being initialized in 2D or 3D so the control can manipulate the active view.

Example Config Entry (portal/master/config.json)
```json
{
	"map": {
		"baselayerSwitcher": {
			"active": true
		}
	}
}
```

Module: bufferAnalysis
Module ID (Key): bufferAnalysis
Module Name: Buffer Analysis

Description and Purpose
The Buffer Analysis module allows analysts to draw buffer zones around points, lines, or polygons, instantly highlighting proximity areas that support planning tasks such as impact studies, accessibility checks, or safety perimeters.

Dependencies
- Requires the map canvas plus either drawn geometries or selected features to act as buffer seeds.
- Benefits from selectFeatures, draw, or featureLister so users can choose the geometries that need buffering.
- Consumes the portal’s projection settings to ensure buffer distances are calculated in the correct coordinate system.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "bufferAnalysis"
}
```

Module: compareFeatures
Module ID (Key): compareFeatures
Module Name: Compare Features

Description and Purpose
The Compare Features module enables side-by-side inspection of attributes from multiple selected features, helping users detect differences in classification, status, dimensions, or ownership without switching between popups.

Dependencies
- Needs one or more vector layers with accessible attributes so the comparison table can populate data.
- Often triggered after getFeatureInfo, featureLister, or selectFeatures have produced a result set.
- Accessible through the secondary menu; no special map configuration beyond layer availability is required.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "compareFeatures"
}
```

Module: compareMaps
Module ID (Key): compareMaps
Module Name: Compare Maps

Description and Purpose
The Compare Maps module opens synchronized map views, often through swipe or split-screen layouts, so users can contrast datasets, time steps, or styling scenarios while maintaining geographic alignment.

Dependencies
- Requires at least two visible layers (WMS or WFS) that support layered rendering in the same projection so the swiper works correctly.
- Integrates with the layer catalog to present only currently active layers as selectable options.
- Uses the map rendering engine plus the shared layerSwiper helper to keep both halves in sync.

Example Config Entry (docs/User/Portal-Config/config.json.md)
```json
{
	"type": "compareMaps"
}
```

Module: contact
Module ID (Key): contact
Module Name: Contact

Description and Purpose
The Contact module centralizes communication channels like support mail, phone numbers, and feedback forms, ensuring portal visitors know exactly how to reach data owners or administrators for assistance.

Dependencies
- Requires mail endpoints defined through from and to arrays plus a serviceId that maps to backend mail handling.
- Can inherit context from modules such as layerInformation, so it should remain accessible from the same menu side to preserve navigation history.
- Does not require specific map layers but often accompanies metadata-driven workflows.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "contact",
	"serviceId": "80001",
	"includeSystemInfo": true,
	"fileUpload": true,
	"infoMessage": "",
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
	]
}
```

Module: controls
Module ID (Key): controls
Module Name: Controls

Description and Purpose
The Controls module bundles the portal’s navigational widgets such as zooming, orientation, reset, or 3D view toggles, giving end users consistent access to essential map interactions regardless of the active theme.

Dependencies
- Lives inside map.controls and therefore requires the main map view to be initialized.
- Individual controls (rotation, tiltView, startModule, button3d, expandable helpers) depend on the presence of 2D/3D renderers and optional orientation settings.
- Works closely with maps core logic to manipulate the current viewport.

Example Config Entry (portal/master/config.json)
```json
{
	"map": {
		"controls": {
			"rotation": {
				"showResetRotationAlways": true,
				"showResetRotation": true,
				"rotationIcons": true,
				"moveDistance": 2500,
				"compass2d": true
			},
			"zoom": true,
			"tiltView": true,
			"startModule": {
				"secondaryMenu": [
					{
						"type": "addWMS"
					}
				]
			},
			"totalView": true,
			"button3d": true,
			"expandable": {
				"backForward": true,
				"orientation": {
					"zoomMode": "once",
					"poiDistances": [
						500,
						1000,
						2000
					]
				},
				"freeze": true,
				"fullScreen": true,
				"exampleControl": true
			}
		}
	}
}
```

Module: coordToolkit
Module ID (Key): coordToolkit
Module Name: Coordinate Toolkit

Description and Purpose
The Coordinate Toolkit module provides utilities for coordinate display, conversion, and copy-to-clipboard actions, empowering professionals to exchange precise locations between the portal and external systems.

Dependencies
- Requires map context so the toolkit can read the pointer position or a clicked feature.
- Needs optional height information by referencing a WMS layer (heightLayerId and heightElementName) if altitude should be shown.
- Integrates with coordInfo to show CRS documentation, making it useful inside the secondary menu.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "coordToolkit",
	"heightLayerId": "19173",
	"heightElementName": "value_0",
	"heightValueWater": "-20",
	"heightValueBuilding": "200",
	"zoomLevel": 5,
	"heightLayerInfo": "Grundlage der Höheninformation ist das \"Digitalge Höhenmodell Hamburg DGM 1\" mit Höhenangaben im Koordinatenreferenzsystem DE_DHHN2016_NH.",
	"coordInfo": {
		"title": "Koordinatenreferenzsystem für 2D-Lageangaben, Erläuterungen",
		"explanations": [
			"ETRS89_UTM32, EPSG 4647 (zE-N): Bezugssystem ETRS89, Abbildungsvorschrift UTM, Zone 32",
			"EPSG 25832: Bezugssystem ETRS89, Abbildungsvorschrift UTM, Zone 32",
			"ETRS89_3GK3: Bezugssystem ETRS89, Abbildungsvorschrift Gauß-Krüger, 3. Meridianstreifen",
			"EPSG 8395: Bezugssystem ETRS89, Abbildungsvorschrift Gauß-Krüger, 3. Meridianstreifen",
			"DE_DHDN_3GK3, EPSG 31467: Bezugssystem DHDN, Abbildungsvorschrift Gauß-Krüger, 3. Meridianstreifen"
		]
	}
}
```

Module: copyrightConstraints
Module ID (Key): copyrightConstraints
Module Name: Copyright Constraints

Description and Purpose
The Copyright Constraints module transparently communicates licensing terms, attribution notices, and usage restrictions for each layer so users understand how data may be reused or distributed.

Dependencies
- Requires metadata from the active layer (typically via layerInformation or CSW records) so it can display correct legal text.
- Belongs in a menu section because it is a purely informational tool and does not touch the map.
- Does not need any special map configuration.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "copyrightConstraints"
}
```

Module: draw
Module ID (Key): draw
Module Name: Draw

Description and Purpose
The Draw module equips users with sketching tools for points, lines, polygons, and text, enabling them to annotate the map, measure custom shapes, or prepare simple illustrations for export and sharing.

Dependencies
- Requires the map view plus an internal drawing layer to store user sketches.
- Works well with selectFeatures, print, or shareView when annotations need to be shared.
- Benefits from a configured symbol library but otherwise has no external service dependency.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "draw"
}
```

Module: draw_old
Module ID (Key): draw_old
Module Name: Draw (Legacy)

Description and Purpose
The Draw (Legacy) module preserves an earlier drawing workflow to support portals that still depend on its interaction model, ensuring backward compatibility during transitions to the newer drawing experience.

Dependencies
- Needs the map to provide legacy drawing interactions and should not be used simultaneously with the new Draw module unless users need both UIs.
- Can enhance sketches by pulling icons of currently active layers (addIconsOfActiveLayers).
- Shares the same annotation layer as other drawing tools, so exported data remain consistent.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "draw_old",
	"enableAttributesSelector": true,
	"addIconsOfActiveLayers": true
}
```

Module: featureLister
Module ID (Key): featureLister
Module Name: Feature Lister

Description and Purpose
The Feature Lister module compiles query results or selected layers into sortable tables, letting users browse, filter, and jump to individual features directly from a structured list.

Dependencies
- Requires one or more queryable layers (usually WFS or SensorThings) to populate the listing.
- Works closely with selectFeatures and filter to define the feature set and can highlight geometries on the map when rows are hovered.
- Needs map highlight styles (point/line/polygon) so selected features are emphasized visually.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "featureLister",
	"maxFeatures": 10,
	"showGraphicalSelect": true,
	"bufferDistance": 500,
	"highlightVectorRulesPolygon": {
		"fill": {
			"color": [255, 0, 127, 0.9]
		},
		"stroke": {
			"width": 3,
			"color": [0, 204, 204, 0.9]
		}
	},
	"highlightVectorRulesPointLine": {
		"stroke": {
			"width": 7,
			"color": [0, 153, 0, 0.9]
		},
		"image": {
			"scale": 2
		}
	}
}
```

Module: fileImport
Module ID (Key): fileImport
Module Name: File Import

Description and Purpose
The File Import module enables users to upload GIS files such as GeoJSON, KML, Shapefile packages, or CSV datasets and visualize them immediately on the map for quick analyses without server-side integration.

Dependencies
- Requires access to the map view so imported geometries can be drawn in the correct projection.
- Works with styleVT or custom styles when customStylingOption is enabled to let users colorize imported data.
- May interact with featureLister or selectFeatures after the ad-hoc layer has been added.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "fileImport",
	"customStylingOption": true
}
```

Module: filter
Module ID (Key): filter
Module Name: Filter

Description and Purpose
The Filter module offers configurable criteria, such as attribute values, categories, or numeric ranges, to refine visible features, helping users focus on the subsets most relevant to their current decision-making.

Dependencies
- Requires at least one data layer defined in layers so the module knows which attributes to expose as filter controls.
- Often combined with featureLister to present the filtered results in a table and with selectFeatures for spatial follow-up actions.
- Needs map access to hide/show features when filter changes are applied.

Example Config Entry (portalconfigs/geojson_example/config.json)
```json
{
	"name": "Kategorieauswahl",
	"liveZoomToFeatures": false,
	"layers": [
		{
			"active": true,
			"layerId": "contributions",
			"strategy": "active",
			"showHits": false,
			"snippets": [
				{
					"type": "dropdown",
					"attrName": "Thema",
					"operator": "IN",
					"display": "list",
					"multiselect": true,
					"prechecked": "all",
					"showAllValues": true,
					"resetLayer": true
				}
			]
		}
	],
	"type": "filter"
}
```

Module: getFeatureInfo
Module ID (Key): getFeatureInfo
Module Name: Get Feature Info

Description and Purpose
The Get Feature Info module lets users click the map to retrieve descriptive attributes, media, and hyperlinks from underlying layers, acting as the primary inspection tool for understanding spatial objects.

Dependencies
- Requires the map plus queryable layers (WMS, WFS, SensorThings, etc.) with configured GFI attributes.
- Works with highlight styles (2D and 3D) so selected features stand out when the info panel is open.
- May hide map markers when vector highlighting is used, so those options must be set explicitly.

Example Config Entry (portal/master/config.json)
```json
{
	"map": {
		"getFeatureInfo": {
			"coloredHighlighting3D": {
				"enabled": true,
				"color": "PURPLE"
			},
			"highlightVectorRules": {
				"fill": {
					"color": [215, 102, 41, 0.9]
				},
				"image": {
					"scale": 1.5
				},
				"stroke": {
					"width": 4,
					"color": [215, 102, 41, 0.9]
				},
				"text": {
					"scale": 2
				}
			},
			"hideMapMarkerOnVectorHighlight": false
		}
	}
}
```

Module: language
Module ID (Key): language
Module Name: Language

Description and Purpose
The Language module allows visitors to switch the portal interface between supported locales, ensuring menus, labels, and instructions remain accessible to multilingual audiences.

Dependencies
- Requires localized resource bundles under locales/ that match the configured portal languages.
- Belongs in a menu section so users can switch languages without leaving the current view.
- No layer or map dependency besides updating localized labels in other modules.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "language"
}
```

Module: layerClusterToggler
Module ID (Key): layerClusterToggler
Module Name: Layer Cluster Toggler

Description and Purpose
The Layer Cluster Toggler module lets users switch between clustered and individual feature representations, balancing overview clarity and precise inspection when working with dense point datasets.

Dependencies
- Requires a list of cluster-ready layer IDs (layerIdList) so it knows which layers to manage.
- Needs the map view and rendering engine to toggle cluster sources at runtime.
- Often paired with point-heavy datasets shown via layerTree.

Example Config Entry (portal/basic/config.json)
```json
{
	"type": "layerClusterToggler",
	"layerIdList": [
		"8712.1",
		"8712.2",
		"8712.3",
		"8712.4"
	]
}
```

Module: layerInformation
Module ID (Key): layerInformation
Module Name: Layer Information

Description and Purpose
The Layer Information module displays descriptive metadata, such as data source, update frequency, scale hints, and responsible organization, so users can assess the reliability of each map layer.

Dependencies
- Retrieves metadata either from layer definitions or via CSW requests, so accurate dataset references per layer are essential.
- Triggered from the layerTree, layerPills, or search results, meaning those modules must pass the selected layer context.
- Optional portal-wide settings (e.g., showUrlGlobal) reside under portalConfig.layerInformation.

Example Config Entry (portal/master/config.json inspired)
```json
{
	"portalConfig": {
		"layerInformation": {
			"showUrlGlobal": true
		}
	}
}
```

Module: layerPills
Module ID (Key): layerPills
Module Name: Layer Pills

Description and Purpose
The Layer Pills module presents frequently used layers as compact toggle buttons, enabling rapid activation or deactivation without opening the full catalog.

Dependencies
- Requires map.layerPills.active plus a list of highlighted layers defined in the topic tree so pills can be generated.
- Works with layerTree to keep visibility synchronized.
- Needs map styling so toggled layers immediately update the view.

Example Config Entry (portal/master/config.json)
```json
{
	"map": {
		"layerPills": {
			"active": true
		}
	}
}
```

Module: layerSelection
Module ID (Key): layerSelection
Module Name: Layer Selection

Description and Purpose
The Layer Selection module offers a focused interface for choosing active analysis layers or defining selection sets, streamlining workflows where only a subset of available content matters.

Dependencies
- Backed by the layer catalog from layerConfig so users can browse folders, backgrounds, and subject layers.
- Usually launched from the Add Layer button, meaning tree.addLayerButton must be enabled for the menu to open.
- Integrates with searchBar instances dedicated to the layer catalog to support searching inside the selection view.

Example Config Entry (portal/master/config.json)
```json
{
	"tree": {
		"addLayerButton": {
			"active": true,
			"searchBar": {
				"active": true,
				"searchInterfaceInstances": [
					{
						"id": "elasticSearch_0",
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

Module: layerSlider
Module ID (Key): layerSlider
Module Name: Layer Slider

Description and Purpose
The Layer Slider module provides a draggable handle to fade between overlapping layers or time slices, letting users visually compare changes such as before-and-after imagery or scenario outputs.

Dependencies
- Requires at least two configured layer IDs that are visible in the current map projection.
- Works best with WMS or raster layers that share the same extent and resolution.
- Uses the map render stack to update layer opacity in real time.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "layerSlider",
	"layerIds": [
		{
			"title": "common:modules.layerSlider.serviceOne",
			"layerId": "19173"
		},
		{
			"title": "common:modules.layerSlider.serviceTwo",
			"layerId": "2426"
		},
		{
			"title": "common:modules.layerSlider.serviceThree",
			"layerId": "8712"
		},
		{
			"title": "common:modules.layerSlider.serviceFour",
			"layerId": "1711"
		}
	]
}
```

Module: layerTree
Module ID (Key): layerTree
Module Name: Layer Tree

Description and Purpose
The Layer Tree module organizes the entire catalog into hierarchical groups with visibility, transparency, and ordering controls, serving as the central point for managing thematic overlays.

Dependencies
- Requires layerConfig definitions (baselayer and subjectlayer sections) to populate the tree.
- Configuration options such as singleBaselayer, showFolderPath, and highlightedFeatures tailor how the tree behaves.
- Interacts with layerSelection, layerPills, and modules like legend to keep UI state synchronized.

Example Config Entry (portal/master/config.json)
```json
{
	"tree": {
		"singleBaselayer": false,
		"showFolderPath": true,
		"addLayerButton": {
			"active": true,
			"searchBar": {
				"active": true,
				"searchInterfaceInstances": [
					{
						"id": "elasticSearch_0",
						"searchCategory": "Thema (externe Fachdaten)"
					},
					{
						"id": "topicTree",
						"searchCategory": "Thema"
					}
				]
			}
		},
		"highlightedFeatures": {
			"layerName": "common:shared.js.utils.selectedFeatures",
			"active": true
		},
		"layerIDsToStyle": [
			{
				"id": "1933",
				"styles": "geofox_stations",
				"name": "Haltestellen",
				"legendURL": "https://geoportal.metropolregion.hamburg.de/legende_mrh/hvv-bus.png"
			}
		]
	}
}
```

Module: legend
Module ID (Key): legend
Module Name: Legend

Description and Purpose
The Legend module renders symbology explanations, color ramps, and icon keys for active layers so users can immediately interpret map styling without consulting external documentation.

Dependencies
- Needs access to the currently visible layers to resolve legend URLs or inline swatches.
- Can be placed in either menu; it should stay synchronized with layerTree and layerPills.
- Pulls legend graphics from each layer definition (e.g., WMS legendURL).

Example Config Entry (portal/master/config.json)
```json
{
	"type": "legend"
}
```

Module: login
Module ID (Key): login
Module Name: Login

Description and Purpose
The Login module handles authentication flows that gate premium datasets or administrative tools, presenting credential forms and status indicators to authorized users.

Dependencies
- Requires identity provider configuration plus a menu entry so users can open the login UI.
- Works closely with protected modules (such as wfst or modeler3D) that should only appear for authenticated users.
- Does not rely on specific layers but may unlock restricted services after successful authentication.

Example Config Entry (portalconfigs/connected_urban_simulations/config.json)
```json
{
	"type": "login"
}
```

Module: measure
Module ID (Key): measure
Module Name: Measure

Description and Purpose
The Measure module lets users calculate distances, areas, and perimeters directly on the map, providing on-the-fly feedback for planning, compliance, or engineering assessments.

Dependencies
- Needs an active map view along with the spatial reference information to translate sketch units into meters.
- Works with drawing layers so measured geometries can be visualized.
- Often combined with coordToolkit or print for sharing results.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "measure"
}
```

Module: menu
Module ID (Key): menu
Module Name: Menu

Description and Purpose
The Menu module aggregates navigation shortcuts, favorite tools, and thematic entries, acting as the primary launcher for modules within the portal.

Dependencies
- Requires configuration of mainMenu and optionally secondaryMenu, including titles, sections, and widths.
- Each menu side references other modules via type, so those modules must be registered in the module store.
- Integrates with urlParams to restore menu state when permalinks or shared views are used.

Example Config Entry (portal/master/config.json)
```json
{
	"mainMenu": {
		"expanded": true,
		"title": {
			"text": "Master",
			"logo": "https://geodienste.hamburg.de/lgv-config/img/hh-logo.png",
			"link": "https://geoinfo.hamburg.de",
			"toolTip": "Landesbetrieb Geoinformation und Vermessung"
		},
		"sections": [
			[
				{
					"type": "about",
					"cswUrl": "https://metaver.de/csw",
					"metaUrl": "https://metaver.de/trefferanzeige?docuuid=40D48B03-AD1D-407B-B04D-B5BC6855BE15",
					"metaId": "40D48B03-AD1D-407B-B04D-B5BC6855BE15"
				},
				{
					"type": "legend"
				}
			]
		]
	}
}
```

Module: modeler3D
Module ID (Key): modeler3D
Module Name: Modeler 3D

Description and Purpose
The Modeler 3D module opens immersive three-dimensional scenes where users can explore buildings, terrain, or planning models with tilt, orbit, and section views.

Dependencies
- Requires Cesium-based 3D map mode plus configured Tileset or Entity layers that contain building IDs referenced by the tool.
- Needs attribute mappings such as gmlIdPath, allowedAttributes, and optional PVO color dictionaries.
- Works with highlight styles and external XML definitions (e.g., building function catalogs) to display semantic information.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "modeler3D",
	"gmlIdPath": "gmlid",
	"updateAllLayers": false,
	"highlightStyle": {
		"silhouetteColor": "#E20D0F",
		"silhouetteSize": 4
	},
	"allowedAttributes": [
		"Gebaeudefunktion",
		"Wertbezeichnung"
	],
	"pvoColors": {
		"housing": "#ff0000",
		"commercial": "#666666",
		"public": "#44ff44"
	},
	"buildingSource": "ALKIS",
	"buildingFunctionURL": "https://geoportal-hamburg.de/3Dprojektplaner/buildingFunctionTypeAdV.xml"
}
```

Module: modules-store
Module ID (Key): modules-store
Module Name: Modules Store

Description and Purpose
The Modules Store module orchestrates shared data for all other modules, providing a central registry that keeps module states synchronized so the portal behaves consistently.

Dependencies
- Automatically registers every module’s Vuex store and therefore depends on the module definitions inside src/modules.
- Required by the root Vuex store to mount namespaces like Modules/Draw or Modules/WfsSearch.
- Has no config.json surface; it simply glues module states to the application.

Example Config Entry (implicit)
This infrastructure component is not configured through config.json. It is wired in src/modules/modules-store/indexModules.js, so no portal configuration snippet is necessary.

Module: mouseHover
Module ID (Key): mouseHover
Module Name: Mouse Hover

Description and Purpose
The Mouse Hover module reveals quick tooltips or highlights when users glide over features, enabling rapid inspection without committing to clicks.

Dependencies
- Requires map interactions plus layers that expose mouseHoverField definitions.
- Configuration under map.mouseHover sets how many features to show and the localization key for the info text.
- Works in tandem with getFeatureInfo to offer both hover and click-based inspection.

Example Config Entry (portal/master/config.json)
```json
{
	"map": {
		"mouseHover": {
			"numFeaturesToShow": 2,
			"infoText": "common:modules.mouseHover.infoText"
		}
	}
}
```

Module: news
Module ID (Key): news
Module Name: News

Description and Purpose
The News module surfaces curated updates, project milestones, or release notes inside the portal to keep stakeholders informed about new datasets and capabilities.

Dependencies
- Requires JSON feeds or localized strings referenced by the module to populate headline and description text.
- Typically resides in the main menu, sharing space with modules like about or contact.
- Does not depend on map content but may link to specific layers or share views.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "news"
}
```

Module: openConfig
Module ID (Key): openConfig
Module Name: Open Config

Description and Purpose
The Open Config module lets advanced users load alternate configuration files or switch project setups on the fly, granting flexibility for demonstration or testing scenarios.

Dependencies
- Requires network access to fetch new configuration files from the paths users provide.
- Appears in the menu so administrators can trigger the action while reviewing the map.
- Interacts with the entire portal initialization pipeline because it reloads configuration state.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "openConfig"
}
```

Module: portalFooter
Module ID (Key): portalFooter
Module Name: Portal Footer

Description and Purpose
The Portal Footer module consistently displays legal links, contact references, and branding at the bottom of the interface, reinforcing trust and compliance requirements.

Dependencies
- Requires portalConfig.portalFooter to define URLs, aliases, and optional scale line visibility.
- Often links to the same resources referenced by about or contact, so those endpoints must remain accessible.
- No map dependency beyond optionally showing a scale bar.

Example Config Entry (portal/master/config.json)
```json
{
	"portalFooter": {
		"urls": [
			{
				"bezeichnung": "common:modules.portalFooter.designation",
				"url": "https://geoinfo.hamburg.de/",
				"alias": "Landesbetrieb Geoinformation und Vermessung",
				"alias_mobile": "LGV Hamburg"
			},
			{
				"url": "mailto:LGVGeoPortal-Hilfe@gv.hamburg.de?subject=Kartenunstimmigkeiten%20melden",
				"alias": "common:modules.portalFooter.mapDiscrepancy"
			}
		],
		"scaleLine": true
	}
}
```

Module: print
Module ID (Key): print
Module Name: Print

Description and Purpose
The Print module packages the current map extent, selected layers, legend, and notes into printable layouts or PDFs so users can distribute professional map outputs offline.

Dependencies
- Requires a configured print service (printServiceId, printAppId) that understands the Masterportal print schema.
- Uses current map selections, so it must read from layerTree, legend, and map state.
- Often paired with shareView or routing outputs to document planning scenarios.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "print",
	"printServiceId": "mapfish",
	"printAppId": "master",
	"filename": "Ausdruck",
	"title": "Mein Titel",
	"currentLayoutName": "A4 Hochformat",
	"printMapMarker": true
}
```

Module: routing
Module ID (Key): routing
Module Name: Routing

Description and Purpose
The Routing module calculates turn-by-turn directions between locations, allowing users to plan journeys, compare travel modes, and visualize proposed routes directly on the map.

Dependencies
- Requires routing backends (BKG ORS/TSR or similar) defined via geosearch, geosearchReverse, directionsSettings, isochronesSettings, and tsrSettings.
- Uses the map and marker layers to show start/end points plus computed paths.
- Works with searchBar to seed origin/destination coordinates, and with shareView to preserve chosen routes.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "routing",
	"icon": "bi-signpost-2",
	"geosearch": {
		"type": "BKG",
		"serviceId": "5",
		"bbox": {
			"CYCLING": "9.6,53.40,10.4,53.84"
		}
	},
	"geosearchReverse": {
		"type": "BKG",
		"serviceId": "5"
	},
	"directionsSettings": {
		"type": "ORS",
		"serviceId": "bkg_ors",
		"speedProfile": "CAR",
		"elevation": true,
		"batchProcessing": {
			"enabled": false,
			"active": false
		}
	},
	"isochronesSettings": {
		"type": "ORS",
		"serviceId": "bkg_ors",
		"speedProfile": "CAR",
		"batchProcessing": {
			"enabled": false,
			"active": false
		}
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

Module: scaleSwitcher
Module ID (Key): scaleSwitcher
Module Name: Scale Switcher

Description and Purpose
The Scale Switcher module presents a scale bar and offers quick jumps to standard scales, helping users maintain cartographic awareness while zooming.

Dependencies
- Requires connection to the map view so zoom level changes update both the bar and quick-select buttons.
- Typically lives in the secondary menu or map controls.
- No layer-specific requirements.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "scaleSwitcher"
}
```

Module: searchBar
Module ID (Key): searchBar
Module Name: Search Bar

Description and Purpose
The Search Bar module provides a unified search experience across addresses, parcels, points of interest, and configured services, enabling users to find locations quickly.

Dependencies
- Needs at least one searchInterfaces entry referencing backend services such as ElasticSearch, Gazetteer, Komoot Photon, or Topic Tree.
- Works with maps to set markers, zoom, or highlight results, and with modules like routing for follow-up actions.
- Appears in the main menu header, so placeholder texts and result templates should be localized.

Example Config Entry (portal/master/config.json)
```json
{
	"mainMenu": {
		"searchBar": {
			"placeholder": "common:modules.searchBar.placeholder.addressTopic",
			"searchInterfaces": [
				{
					"type": "elasticSearch",
					"searchInterfaceId": "elasticSearch_0",
					"serviceId": "elastic_prod",
					"requestType": "GET",
					"hitTemplate": "layer",
					"payload": {
						"id": "query",
						"params": {
							"query_string": "",
							"typ": [
								"sensorthings",
								"wms"
							],
							"size": 30
						}
					},
					"resultEvents": {
						"onClick": [
							"addLayerToTopicTree"
						],
						"buttons": [
							"showInTree",
							"showLayerInfo"
						]
					}
				},
				{
					"type": "gazetteer",
					"serviceId": "6",
					"searchAddress": true,
					"searchHouseNumbers": true,
					"searchParcels": true,
					"resultEvents": {
						"onClick": [
							"setMarker",
							"zoomToResult",
							"highlight3DTileByCoordinates"
						],
						"buttons": [
							"startRouting"
						]
					}
				}
			]
		}
	}
}
```

Module: selectFeatures
Module ID (Key): selectFeatures
Module Name: Select Features

Description and Purpose
The Select Features module gives users rectangle, polygon, or freehand selection tools to gather multiple features and trigger downstream analyses or exports.

Dependencies
- Requires queryable layers so selections can be evaluated server- or client-side.
- Often combined with featureLister, bufferAnalysis, or wfsSearch for additional processing.
- Needs the map view and vector highlighting styles to show the selection footprint.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "selectFeatures"
}
```

Module: shadow
Module ID (Key): shadow
Module Name: Shadow

Description and Purpose
The Shadow module simulates sun position and resulting shadow footprints for chosen dates and times, supporting urban planning scenarios focused on daylight exposure.

Dependencies
- Works with 3D map mode or building layers to project shadows realistically.
- Requires map interactions to set the date/time and to toggle isShadowEnabled.
- Often pairs with modeler3D for scenario analysis.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "shadow",
	"isShadowEnabled": true
}
```

Module: shareView
Module ID (Key): shareView
Module Name: Share View

Description and Purpose
The Share View module generates sharable links or embed snippets that capture the current extent, active layers, and selections so collaborators can open the exact same map state.

Dependencies
- Relies on urlParams core to serialize map, menu, and module state into the generated URL.
- Needs at least one sharing channel configured (e.g., QR codes, social networks).
- Typically available in both main and secondary menus for quick access.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "shareView",
	"facebookShare": true,
	"qrShare": true
}
```

Module: statisticDashboard
Module ID (Key): statisticDashboard
Module Name: Statistic Dashboard

Description and Purpose
The Statistic Dashboard module visualizes key indicators—charts, counters, trend lines—linked to spatial datasets, allowing decision makers to interpret numerical insights alongside the map.

Dependencies
- Requires one or more data layers plus the referenced attributes and filter definitions (mappingFilter, timeStepsFilter).
- Needs color schemes and palette definitions to render choropleth maps and line charts.
- Often used in the secondary menu, pulling geometries via OAF or WFS endpoints.

Example Config Entry (portalconfigs/mrhportal/config.json)
```json
{
	"type": "statisticDashboard",
	"colorScheme": {
		"referenceRegion": [155, 155, 155, 0.7],
		"lineCharts": [[74, 0, 30, 1], [117, 18, 50, 1], [189, 47, 83, 1]]
	},
	"minNumberOfClasses": 3,
	"maxNumberOfClasses": 9,
	"numberOfClasses": 5,
	"selectableColorPalettes": [
		{"key": "YlGn", "label": "Gelb-Grün"},
		{"key": "YlOrRd", "label": "Gelb-Rot"}
	],
	"selectedColorPaletteIndex": 0,
	"opacity": 0.9,
	"data": [
		{
			"layerId": "33162",
			"levelName": "Kreise",
			"geometryAttribute": "geom",
			"oafRequestCRS": "http://www.opengis.net/def/crs/EPSG/0/25832",
			"geomRequestParams": {
				"datetime": "2022-12-31",
				"limit": 100
			},
			"timeStepsFilter": {
				"5": "Die letzten 5 Jahre",
				"10": "Die letzten 10 Jahre",
				"all": "Alle Jahre"
			}
		}
	]
}
```

Module: styleVT
Module ID (Key): styleVT
Module Name: Style Vector Tiles

Description and Purpose
The Style Vector Tiles module lets administrators adjust colors, labels, and symbol rules of vector-tile layers live within the portal, ensuring thematic styling matches branding or analytical needs.

Dependencies
- Requires vector tile layers with configurable styles, typically referenced via vtStyles.
- Works in tandem with layerTree to determine which layer is being styled.
- Needs write access (client side) to update style definitions on the fly.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "styleVT"
}
```

Module: wfsSearch
Module ID (Key): wfsSearch
Module Name: WFS Search

Description and Purpose
The WFS Search module queries external Web Feature Service endpoints with dynamic filters, returning rich attribute lists and map highlights for technical users who need authoritative data directly from source services.

Dependencies
- Requires one or more instances configured with service URLs, stored queries, and result list layouts.
- Depends on the map to show highlights (highlightVectorRules*) and to zoom to returned features.
- Often uses selectSource files for code lists and integrates with featureViaURL or layerTree for follow-up actions.

Example Config Entry (portal/master/config.json)
```json
{
	"type": "wfsSearch",
	"description": "common:modules.wfsSearch.description_parcel",
	"zoomLevel": 7,
	"instances": [
		{
			"title": "common:modules.wfsSearch.parcelSearch",
			"userHelp": "hide",
			"zoomButtonInColumn": true,
			"resultList": {
				"gemarkungsname": "Gemarkungsname",
				"flurstueck_lang": "Flurstücknummer - lang",
				"geometry": "Zoomen"
			},
			"requestConfig": {
				"gazetteer": {
					"namespaces": [
						"http://www.adv-online.de/namespaces/adv/dog",
						"http://geodienste.hamburg.de/dog_gages/services/wfs_dog?SERVICE=WFS&VERSION=2.0.0&REQUEST=DescribeFeatureType&OUTPUTFORMAT=application/gml+xml;+version=3.2&TYPENAME=dog:Flurstueckskoordinaten&NAMESPACES=xmlns(dog,http://www.adv-online.de/namespaces/adv/dog)"
					],
					"memberSuffix": "member"
				},
				"restLayerId": "6",
				"storedQueryId": "Flurstueck"
			},
			"selectSource": "https://geodienste.hamburg.de/lgv-config/gemarkungen_hh.json"
		}
	]
}
```

Module: wfst
Module ID (Key): wfst
Module Name: WFST Editing

Description and Purpose
The WFST Editing module empowers authorized users to insert, update, or delete spatial features via transactional WFS operations, enabling collaborative data maintenance inside the portal.

Dependencies
- Requires editable WFS layers (IDs listed in layerIds) plus permissions for each geometry type button.
- Depends on the map for drawing/editing, and on login or backend auth to ensure only authorized edits are sent.
- Can integrate with layerInformation to display metadata about the editable layers.

Example Config Entry (portal/basic/config.json)
```json
{
	"type": "wfst",
	"name": "WFS-T Tool",
	"delete": true,
	"update": true,
	"multiUpdate": [
		{
			"layerId": "lgvpoint",
			"available": true,
			"configAttributes": ["name"],
			"controlAttributes": ["gemeinde"]
		}
	],
	"layerIds": [
		"lgvpolygon",
		"lgvpoint",
		"lgvline",
		"1122"
	],
	"toggleLayer": false
}
```

Module: wmsTime
Module ID (Key): wmsTime
Module Name: WMS Time

Description and Purpose
The WMS Time module exposes temporal controls for time-enabled WMS layers so users can scrub through dated imagery or forecasts and observe change over time.

Dependencies
- Requires at least one layer whose service definition sets "time": true (typically in resources/services.json or layerConfig), so the time slider knows which dataset to control.
- Integrates with layerSwiper and compareMaps to ensure time-aware layers render correctly when swiped or compared.
- Needs the map plus the WMS capabilities document to read available time steps.

Example Config Entry (portal/basic/resources/services.json)
```json
{
	"id": "dop_zeitreihe_belaubt",
	"name": "Luftbilder Hamburg - DOP Zeitreihe belaubt",
	"url": "https://qs-geodienste.hamburg.de/wms_dop_zeitreihe_belaubt",
	"typ": "WMS",
	"layers": "dop_zeitreihe_belaubt",
	"time": true
}
```

Module: layers (core)
Module ID (Key): layers
Module Name: Layers Core

Description and Purpose
The Layers Core module manages every map layer’s lifecycle, including loading, styling, visibility, ordering, and grouping, ensuring thematic content behaves predictably no matter which data source or rendering technology is used.

Dependencies
- Driven entirely by layerConfig where baselayers, subject layers, styles, and loading strategies are defined.
- Interacts with modules like layerTree, layerPills, measure, and print which all rely on normalized layer definitions.
- Requires correct service URLs and metadata so downstream components (GFI, legend, attribution) work as expected.

Example Config Entry (portal/master/config.json)
```json
{
	"layerConfig": {
		"subjectlayer": {
			"elements": [
				{
					"id": "1711",
					"name": "Krankenhäuser",
					"typ": "WFS",
					"visibility": false,
					"loadingStrategy": "all",
					"searchField": "name",
					"mouseHoverField": ["name", "adresse"]
				}
			]
		}
	}
}
```

Module: maps (core)
Module ID (Key): maps
Module Name: Maps Core

Description and Purpose
The Maps Core module orchestrates map instances, including view handling, highlighting, markers, interactions, and synchronization, so all visual components respond consistently to user navigation and application state.

Dependencies
- Requires portalConfig.map settings such as mapView, mapMarker, and interaction definitions.
- Works with controls, mouseHover, getFeatureInfo, and 3D parameters to provide a cohesive map experience.
- Reads basemap definitions from layerConfig to initialize base layers.

Example Config Entry (portal/master/config.json)
```json
{
	"map": {
		"mapView": {
			"backgroundImage": "https://geodienste.hamburg.de/lgv-config/img/backgroundCanvas.jpeg",
			"startZoomLevel": 4,
			"startCenter": [565874, 5934140],
			"mapInteractions": {
				"interactionModes": {
					"altShiftDragRotate": true,
					"twoFingerPan": true
				}
			}
		},
		"mapMarker": {
			"pointStyleId": "mapMarker_geo-alt-fill"
		}
	}
}
```

Module: urlParams (core)
Module ID (Key): urlParams
Module Name: URL Parameters Core

Description and Purpose
The URL Parameters Core module reads and writes map state into URL parameters, allowing deep links that recreate extents, active layers, selected features, or tool modes, which is essential for collaboration and bookmarking.

Dependencies
- Automatically hooks into shareView, menu, maps, and module stores to capture their state when a permalink is generated or when a URL is loaded.
- Requires configuration of the features or actions that should react to URL input, such as map.featureViaURL, zoomTo, or module-specific urlParams handlers.
- Works best when modules expose sanitized urlParams getters so complex states can be serialized.

Example Config Entry (portal/master/config.json)
```json
{
	"map": {
		"featureViaURL": {
			"zoomTo": "42",
			"epsg": 4326,
			"layers": [
				{
					"id": "42",
					"geometryType": "Point",
					"name": "Punkt Feature",
					"styleId": "location_eventlotse"
				}
			]
		},
		"zoomTo": [
			{
				"id": "zoomToGeometry",
				"layerId": "1692",
				"property": "bezirk_name",
				"allowedValues": [
					"ALTONA",
					"HARBURG",
					"HAMBURG-NORD"
				]
			}
		]
	}
}
```
