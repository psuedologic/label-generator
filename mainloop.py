import label_generator
import gui
import saveload

gui.main()
config = saveload.load_config("default.json")
config = label_generator.derive_config(config)