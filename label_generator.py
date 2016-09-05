import file
import model
import view
import gui


#Loads default configuration settings
settings = file.load_settings()
file = file.File("default.json")

model = model.Model(file.config)

view = view.View(model, settings)
image = view.create_image()
gui.main()
