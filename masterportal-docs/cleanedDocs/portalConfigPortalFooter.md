### portalConfig.portalFooter {data-toc-label='Portal Footer'}
Possibility to configure the content of the portal footer.

| Name           | Required | Type                                        | Default                       | Description                                                            | Expert |
| -------------- | -------- | ------------------------------------------- | ----------------------------- | ---------------------------------------------------------------------- | ------ |
| configPaths    | no       | String[]                                    | ["portalConfig.portalFooter"] | Path array of possible config locations. First one found will be used. | false  |
| scaleLine      | no       | Boolean                                     | true                          | Shows if Scale should be shown in footer.                              | false  |
| scaleLineWidth | no       | Number                                      | 2                             | Width of the scale line in cm.                                         | false  |
| seperator      | no       | String                                      | "` \| `"                      | The seperator between urls.                                            | false  |
| urls           | no       | **[urls](#portalconfigportalfooterurls)**[] | []                            | Urls, that should be displayed in the footer.                          | false  |

**Example**

```json
"portalFooter": {
    "urls": [
    {
        "bezeichnung": "common:modules.portalFooter.designation",
        "url": "https://geoinfo.hamburg.de/",
        "alias": "Landesbetrieb Geoinformation und Vermessung",
        "alias_mobile": "LGV Hamburg"
    },
    {
        "url": "mailto:LGVGeoPortal-Hilfe@gv.hamburg.de?subject=Kartenunstimmigkeiten%20melden&body=Zur%20weiteren%20Bearbeitung%20bitten%20wir%20Sie%20die%20nachstehenden%20Angaben%20zu%20machen.%20Bei%20Bedarf%20fügen%20Sie%20bitte%20noch%20einen%20Screenshot%20hinzu.%20Vielen%20Dank!%0A%0A1.%20Name:%0A2.%20Telefon:%0A3.%20Anliegen",
        "alias": "common:modules.portalFooter.mapDiscrepancy"
    }
    ],
    "scaleLine": true
}
```

#### portalConfig.portalFooter.urls {data-toc-label='Urls'}

A Url can be defined in various ways.

| Name         | Required | Type   | Default | Description                                                                                                         | Expert |
| ------------ | -------- | ------ | ------- | ------------------------------------------------------------------------------------------------------------------- | ------ |
| alias        | yes      | String |         | Displayed name of the link in desktop-view.                                                                         | false  |
| alias_mobile | no       | String |         | Displayed name of the link in mobile-view. If this is not specified, the link will not be displayed in mobile-view. | false  |
| bezeichnung  | no       | String |         | Displayed description next to the link.                                                                             | false  |
| url          | yes      | String |         | The Url for the link.                                                                                               | false  |

**Example**

```json
{
    "bezeichnung": "common:modules.portalFooter.designation",
    "url": "https://geoinfo.hamburg.de/",
    "alias": "Landesbetrieb Geoinformation und Vermessung",
    "alias_mobile": "LGV Hamburg"
}
```

***
