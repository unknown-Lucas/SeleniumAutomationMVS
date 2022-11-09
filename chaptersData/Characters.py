from dataclasses import dataclass, field

@dataclass
class UnlockPrice:
    gold : str = ''
    gleanium : str = ''
    ticket : str = ''

@dataclass
class Data:
    name: str
    specialization: str
    title :str
    description: str
    image: str
    unlock: UnlockPrice
    voiceActor:str = ''
    attributes:list = field(default_factory = list)

@dataclass
class Characters:
    character_id : int
    data : Data
    skills : list = field(default_factory = list)
    attacks :  list = field(default_factory = list)
    passives : str = ''
    universe: str = ''

    