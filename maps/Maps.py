from csv import field_size_limit
from dataclasses import dataclass, field

@dataclass
class Layout:
  mode: str
  description:str   

@dataclass
class Data:
    mapName: str
    origin: str
    image : str
    layout : field(default_factory=list)
    npc: field(default_factory=list)  

@dataclass
class Maps:
    map_id : int
    universe : str
    data : Data 
    
