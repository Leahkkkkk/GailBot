# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-09 11:25:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-15 16:34:11


from typing import List, Any, Dict
import time
from copy import deepcopy
# Third party imports
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.websocket import RecognizeCallback, AudioSource

from gailbot.configs.utils import get_engine_conf
from gailbot.core.utils.media import MediaHandler
from gailbot.core.utils.general import (
    make_dir,
    get_extension,
    get_name,
    is_file,
    get_size
)

_ENGINE_CONF = get_engine_conf("watson")

class WatsonCore:

    # TODO: This needs to load the configs somehow

    def __init__(self, apikey : str, region : str):


        self.apikey = apikey
        self.region = region
        self.media_h = MediaHandler()

        # Parse confs
        self._regions = _ENGINE_CONF["watson"]["regions"]['"uris']
        self._format_to_content_types = _ENGINE_CONF["watson"]["format_to_content"]
        self._defaults = _ENGINE_CONF["watson"]["defaults"]
        self.max_size_bytes = _ENGINE_CONF["watson"]["max_file_size_bytes"]

        if not self._is_api_key_valid(apikey):
            raise Exception(f"Apikey {apikey} invalid")
        if not region in self._regions:
            raise Exception(
                f"Region {region} not in {list(self._regions.keys())}"
            )

    @property
    def supported_formats(self) -> List[str]:
        return self.media_h.supported_formats()

    @property
    def regions(self) -> Dict:
        return

    @property
    def defaults(self) -> Dict:
        return self._defaults

    def websockets_recognize(
        self,
        audio_path : str,
        outdir : str,
        recognize_callback : RecognizeCallback,
        base_language_model : str,
        language_customization_id : str = "",
        acoustic_customization_id : str = ""
    ) -> Any:

        assert is_file(audio_path), f"Not a file {audio_path}"
        make_dir(outdir,overwrite=True)

        if get_size(audio_path) >= self.max_size_bytes:
            # TODO: Convert to an opus file using the media handler.
            # This is because opus is a hugely compressed file format that
            # we can use.
            raise NotImplementedError()

        # Create the stt service and run
        authenticator = IAMAuthenticator(self.apikey)
        stt = SpeechToTextV1(authenticator=authenticator)
        stt.set_service_url(self.regions[self.region])


        with open(audio_path, "rb") as f:
            # Prepare args
            source = AudioSource(f)
            content_type = self._format_to_content_types[get_extension(audio_path)]
            kwargs = deepcopy(self.defaults).update({
                "audio": source,
                "content_type" : content_type,
                "recognize_callback": recognize_callback,
                "model" : base_language_model,
                "language_customization_id": language_customization_id,
                "acoustic_customization_id": acoustic_customization_id,
                "base_model_version": None,
                "keywords" : None,

            })
            stt.recognize_using_websocket(**kwargs)


    ###############
    # PRIVATE
    ##############

    def _is_api_key_valid(self, apikey: str, url: str) -> bool:
        try:
            stt = self._initialize_stt_service(apikey)
            stt.set_service_url(url)
            stt.list_models()
            return True
        except:
            return False



