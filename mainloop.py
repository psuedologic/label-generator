import gui
import saveload

gui.main()
config = saveload.load_config("default.json")
label_generator(config)
