import sys
import importlib

aliases = ["backbone", "data", "external", "utils", "layers", "scripts", "web"] # REKKEFØLGEN ER VIKTIG FOR DEPANDANCIES, IKKE ENDRE

for name in aliases:
    sys.modules[name] = importlib.import_module(f"yolact_submodule.{name}")

from ros_yolact_node.ros_yolact_code import main

main()
