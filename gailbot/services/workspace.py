# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:05:38
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-10 13:25:26

import sys
import os
from typing import Dict
from config import config_from_toml
from configs.utils import get_base_conf_path
from core.utils.general import (
    make_dir,
    move
)
class Workspace:
    """Manages the entire underlying workspace for GailBot"""

    def __init__(self):
        # Set up the workspace.
        self.base_conf = config_from_toml(get_base_conf_path())

    @property
    def sources_ws(self):
        return self.sources_ws

    @property
    def settings_ws(self):
        return self.settings_ws

    @property
    def engines_ws(self):
        return self.engines_ws

    @property
    def plugins_ws(self):
        return self.plugins_ws

    @property
    def engine_conf_paths(self):
        return self.engine_conf_paths


    def init_workspace(self, workspace_dir : str):
        """Initialize and return True if successful"""

        make_dir(workspace_dir,overwrite=False)

        ws_paths = self._construct_abs_paths(
            workspace_dir, self.base_conf.paths.workspace.to_dict()
        )
        self.sources_ws = ws_paths["sources_ws"]
        self.settings_ws = ws_paths["settings_ws"]
        self.plugins_ws = ws_paths["plugins_ws"]
        self.engines_ws = ws_paths["engines_ws"]

        self.engine_conf_paths = self._construct_abs_paths(
            workspace_dir, self.base_conf.paths.engines.confs
        )

        # Make dirs
        make_dir(self.source_ws, overwrite=True)
        make_dir(self.plugins_ws, overwrite=False)
        make_dir(self.engines_ws, overwrite=True)
        make_dir(self.settings_ws, overwrite=False)
        # Move default settings to the specified workspace
        move(self.base_conf.paths.settings.default_conf_path,self.settings_ws)

    def reset(self):
        pass

    def _construct_abs_paths(self, root_path, rel_paths : Dict) -> Dict:
        res = dict()
        for k, v in rel_paths.items():
            res[k] = os.path.join(root_path,v)
        return res




