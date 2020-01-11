from importlib import import_module
import config


def load_extensions(app):
    for extension in app.config["EXTENSIONS"]:
        # Split data in form `extension.path:factory_function`
        module_name, factory = extension.split(":")
        # Dynamically import extension module.
        ext = import_module(module_name)
        # Invoke factory passing app.
        getattr(ext, factory)(app)


def init_app(app, obj=config.Config):
    app.config.from_object(obj)
