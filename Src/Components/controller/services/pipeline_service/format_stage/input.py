# Standard imports
from typing import Dict,  Any
from dataclasses import dataclass

@dataclass
class FormatPluginInput:
    analysis_stage_outputs: Dict[str, Any]