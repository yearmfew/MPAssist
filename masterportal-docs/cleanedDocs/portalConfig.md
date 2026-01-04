## portalConfig {data-toc-label='Portal Config'}
The section *portalConfig* controls the following properties:

1. Menu entries in main menu and availability as well as order of modules (*mainMenu*)
2. Configuration of the map and elements placed on it (*map*)
3. Footer configuration (*portalFooter*)
4. Menu entries in secondary menu and availability as well as order of modules (*secondaryMenu*)
5. Type of topic selection (*tree*)

The configuration options listed in the following table exist:

| Name          | Required | Type                                          | Default | Description                                                                                                                                                                                                    | Expert |
| ------------- | -------- | --------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| mainMenu      | no       | **[menu](#portalconfigmenu)**                 |         | Menu entries in main menu and their order are configured in this entry. The order of modules corresponds to the order in the object specifying them; see **[Modules](#portalconfigmenusectionsmodules)**.      | false  |
| map           | no       | **[map](#portalconfigmap)**                   |         | Configuration of the map and elements placed on it.                                                                                                                                                            | false  |
| portalFooter  | no       | **[portalFooter](#portalconfigportalfooter)** |         | Possibility to configure the content of the portal footer.                                                                                                                                                     | false  | xxx |
| secondaryMenu | no       | **[menu](#portalconfigmenu)**                 |         | Menu entries in secondary menu and their order are configured in this entry. The order of modules corresponds to the order in the object specifying them; see **[Modules](#portalconfigmenusectionsmodules)**. | false  |
| tree          | no       | **[tree](#portalconfigtree)**                 |         | Configuration of the topic selection tree.                                                                                                                                                                     | false  |

**Example**

```json
{
    "portalConfig": {
        "mainMenu": {},
        "map": {},
        "portalFooter": {},
        "secondaryMenu": {},
        "tree": {}
    }
}
```

***