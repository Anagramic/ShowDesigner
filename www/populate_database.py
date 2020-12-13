from ShowDesigner import db, InputDevice

db.drop_all()
db.create_all()

# Input Devices
id1 = InputDevice(Model="SM57", Manufacturer="Shure", Type="Dynamic")
db.session.add(id1)

id2 = InputDevice(Model="SM58", Manufacturer="Shure", Type="Dynamic")
db.session.add(id2)

id3 = InputDevice(Model="NT5", Manufacturer="Rode", Type="Condenser")
db.session.add(id3)

db.session.commit()