import numpy as np
import xml.etree.ElementTree as ET
from typing import List, Optional

class Parser:
    def __init__(
        self,
        place_ids: List[str],
        trans_ids: List[str],
        place_names: List[Optional[str]],
        trans_names: List[Optional[str]],
        I: np.ndarray,   
        O: np.ndarray, 
        M0: np.ndarray
    ):
        self.place_ids = place_ids
        self.trans_ids = trans_ids
        self.place_names = place_names
        self.trans_names = trans_names
        self.I = I
        self.O = O
        self.M0 = M0

    @classmethod
    def from_pnml(cls, filename: str) -> "Parser":
        tree = ET.parse(filename)
        root = tree.getroot()
        
        ns = {'pnml': 'http://www.pnml.org/version-2009/grammar/pnml'}
        
        place_ids = []
        place_names = []
        for place in root.findall('.//pnml:place', ns):
            place_id = place.get('id')
            place_ids.append(place_id)
            name_elem = place.find('pnml:name/pnml:text', ns)
            place_name = name_elem.text if name_elem is not None else ''
            place_names.append(place_name)
        
        trans_ids = []
        trans_names = []
        for transition in root.findall('.//pnml:transition', ns):
            trans_id = transition.get('id')
            trans_ids.append(trans_id)
            name_elem = transition.find('pnml:name/pnml:text', ns)
            trans_name = name_elem.text if name_elem is not None else ''
            trans_names.append(trans_name)
        
        I = np.zeros((len(trans_ids), len(place_ids)), dtype=int)
        O = np.zeros((len(trans_ids), len(place_ids)), dtype=int)
        M0 = np.zeros(len(place_ids), dtype=int)
        
        for arc in root.findall('.//pnml:arc', ns):
            source_id = arc.get('source')
            target_id = arc.get('target')
            
            weight_elem = arc.find('pnml:inscription/pnml:text', ns)
            weight = int(weight_elem.text) if weight_elem is not None and weight_elem.text else 1
            
            if source_id in place_ids and target_id in trans_ids:
                place_idx = place_ids.index(source_id)
                trans_idx = trans_ids.index(target_id)
                I[trans_idx, place_idx] = weight
            
            elif source_id in trans_ids and target_id in place_ids:
                place_idx = place_ids.index(target_id)
                trans_idx = trans_ids.index(source_id)
                O[trans_idx, place_idx] = weight
        
        for place in root.findall('.//pnml:place', ns):
            place_id = place.get('id')
            initial_marking_elem = place.find('pnml:initialMarking/pnml:text', ns)
            if initial_marking_elem is not None and initial_marking_elem.text:
                place_idx = place_ids.index(place_id)
                M0[place_idx] = int(initial_marking_elem.text)
    
        return cls(place_ids, trans_ids, place_names, trans_names, I, O, M0)

    def __str__(self) -> str:
        s = []
        s.append("Places: " + str(self.place_ids))
        s.append("Place names: " + str(self.place_names))
        s.append("\nTransitions: " + str(self.trans_ids))
        s.append("Transition names: " + str(self.trans_names))
        s.append("\nI (input) matrix:")
        s.append(np.array2string(self.I, separator=' '))
        s.append("\nO (output) matrix:")
        s.append(np.array2string(self.O, separator=' '))
        s.append("\nInitial marking M0:")
        s.append(np.array2string(self.M0, separator=' '))
        return "\n".join(s)