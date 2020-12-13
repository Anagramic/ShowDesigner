from ShowDesigner import db, InputDevice, OutputDevice, StageBox, Show

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

#Output Devices
od1 = OutputDevice(Model="Ha-4000", Manufacturer="Behringer", Type="Headphone amp")
db.session.add(od1)

od2 = OutputDevice(Model="TD-12", Manufacturer="Titan", Type="Speaker")
db.session.add(od2)

od3 = OutputDevice(Model="VQ1500D", Manufacturer="Behringer", Type="Subwoofer")
db.session.add(od3)

db.session.commit()

#Stage Boxes
sd1 = StageBox(Inputs=16, Outputs=4)
db.session.add(sd1)

sd2 = StageBox(Inputs=8, Outputs=8)
db.session.add(sd1)

db.session.commit()

#Shows
sh1 = Show(Name="Rent", Date_from="20/09/21", Date_to="20/09/21",Company="CTC", Venue="The Leys")
db.session.add(sh1)

sh2 = Show(Name="West Side Story", Date_from="13/04/21", Date_to="20/04/21",Company="Chaos", Venue="The Arts")
db.session.add(sh2)

db.session.commit()