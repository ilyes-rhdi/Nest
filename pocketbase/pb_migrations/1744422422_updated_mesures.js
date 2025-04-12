/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_3657947827")

  // update field
  collection.fields.addAt(4, new Field({
    "hidden": false,
    "id": "number2375268457",
    "max": null,
    "min": null,
    "name": "humiditer_out",
    "onlyInt": false,
    "presentable": false,
    "required": false,
    "system": false,
    "type": "number"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_3657947827")

  // update field
  collection.fields.addAt(4, new Field({
    "hidden": false,
    "id": "number2375268457",
    "max": null,
    "min": null,
    "name": "tension",
    "onlyInt": false,
    "presentable": false,
    "required": false,
    "system": false,
    "type": "number"
  }))

  return app.save(collection)
})
