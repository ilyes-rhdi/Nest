/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_3657947827")

  // add field
  collection.fields.addAt(6, new Field({
    "hidden": false,
    "id": "number4069000174",
    "max": null,
    "min": null,
    "name": "temperature_out",
    "onlyInt": false,
    "presentable": false,
    "required": false,
    "system": false,
    "type": "number"
  }))

  // add field
  collection.fields.addAt(7, new Field({
    "hidden": false,
    "id": "number1831405905",
    "max": null,
    "min": null,
    "name": "power_consumption_W",
    "onlyInt": false,
    "presentable": false,
    "required": false,
    "system": false,
    "type": "number"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_3657947827")

  // remove field
  collection.fields.removeById("number4069000174")

  // remove field
  collection.fields.removeById("number1831405905")

  return app.save(collection)
})
