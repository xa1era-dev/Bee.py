class ModuleIsNotActive(Exception):
    def __init__(self) -> None:
        self.message = "ModulesIsNotActive: Rooms is not active"
        super().__init__(self.message)