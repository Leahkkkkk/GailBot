# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-09 11:25:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 11:59:32

from typing import List, Any, Dict
import time
from copy import deepcopy
# Third party imports
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.websocket import RecognizeCallback, AudioSource
from gailbot.configs.utils import WATSON_DATA
from gailbot.core.utils.media import MediaHandler
from gailbot.core.utils.general import (
    make_dir,
    is_directory,
    get_extension,
    get_name,
    is_file,
    get_size,
    run_cmd, 
    get_cmd_status,
    delete,
    CMD_STATUS
)
class WatsonCore:
    """
    TODO: documentation
    
    """
    def __init__(self, apikey : str, region : str):
        self.apikey = apikey
        self.region = region
        self.media_h = MediaHandler()

        # Parse confs
        self._regions = WATSON_DATA.regions_uris
        self._format_to_content_types = WATSON_DATA.format_to_content 
        self._defaults = WATSON_DATA.defaults
        self.max_size_bytes = WATSON_DATA.max_file_size_bytes

        if not self._is_api_key_valid(apikey, self._regions[region]):
            raise Exception(f"Apikey {apikey} invalid")
        if not region in self._regions:
            raise Exception(
                f"Region {region} not in {list(self._regions.keys())}"
            )

    @property
    def supported_formats(self) -> List[str]:
        """
        Access the supported formats of an instance of object WatsonCore

        Returns:
            List[str] : list of supported formats
        """
        return self.media_h.supported_formats

    @property
    def regions(self) -> Dict:
        """
        Access the regions of an instance of object WatsonCore

        Returns: 
            Dict representing the regions
        """
        return self._regions

    @property
    def defaults(self) -> Dict:
        """
        Access the defaults of an instance of object WatsonCore

        Returns: 
            Dict representing the defaults
        """
        return self._defaults

    def is_file_supported(self, file:str) -> bool:
        """
        Determines if a given file is supported

        Args:
            file (str) : file name to check if supported

        Returns: True if the file is supported, false if not.
        """
        return get_extension(file) in self.supported_formats
    
    def websockets_recognize(
        self,
        audio_path : str,
        outdir : str,
        recognize_callback : RecognizeCallback,
        base_language_model : str,
        language_customization_id : str = "",
        acoustic_customization_id : str = ""
    ) -> Any:
        """
        Transcribes the provided audio stream using a websocket connections.
        All attributes MUST be set before using this method.

        Args:
            audio_path (str) : audio_path websockets attribute
            outdir (str) : outdir websockets attribute
            recognize_callback (RecognizeCallback) : recognize_callback websockets attribute
            base_language_model (str) : base_language_model websockets attribute
            language_customization_id (str) : language_customization_id websockets attribute
            acoustic_customization_id (str) : acoustic_customization_id websockets attribute

        Returns:   

        """

        # Checks all the input data is valid
        assert is_file(audio_path), f"Not a file {audio_path}"
        try: 
            if not is_directory(outdir): 
                raise Exception
            make_dir(f"{outdir}/watson_engine_ws", overwrite=True)
            assert is_directory(outdir)
            self.engine_workspace_dir = f"{outdir}/watson_engine_ws"
        except:
            raise Exception 
        if get_size(audio_path) >= self.max_size_bytes:
            audio_path = self._convert_to_opus(audio_path)

        # Create the stt service and run
        authenticator = IAMAuthenticator(self.apikey)
        stt = SpeechToTextV1(authenticator=authenticator)
        stt.set_service_url(self.regions[self.region])

        with open(audio_path, "rb") as f:
            # Prepare args
            source = AudioSource(f)
            content_type = self._format_to_content_types[get_extension(audio_path)]
            kwargs = deepcopy(self.defaults)
            kwargs.update({
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
            """ TODO:  how will the outdir be used and should we delete it anytime?"""
            # delete(self.engine_workspace_dir)
            


    ###############
    # PRIVATE
    ##############
    def _is_api_key_valid(self, apikey: str, url: str) -> bool:
        """
        Determines if given Watson API key is valid

        Args:
            apikey (str) : apikey of which to determine validity
            url (str) : URL to set service url of speech to text service
        """
        try:
            stt = self._initialize_stt_service(apikey)
            stt.set_service_url(url)
            stt.list_models()
            return True
        except:
            return False

    def _initialize_stt_service(self, apikey: str) -> SpeechToTextV1:
        """
        Initializes the speech to text services

        Args:
            apikey (str) : API key to pass into the IAMAuthenticator

        Returns:
            Newly initialized speech to text service
        """
        authenticator = IAMAuthenticator(apikey)
        stt = SpeechToTextV1(authenticator=authenticator)
        return stt

    def _convert_to_opus(self, audio_path: str, workspace: str) -> str:
        """
        Convert audio stream to .opus format 

        Args:
            audio_path (str) : path to the audio file for which to convert 
                to .opus format
            workspace (str) : Workspace of the output directory in which to put 
                the newly converted file

        Returns:
            String representing the path to the newly converted output file
        """
        out_path = "{}/{}.opus".format(
            workspace, get_name(audio_path)
        )
        cmd_str = "ffmpeg -y -i {} -strict -2  {}".format(audio_path, out_path)
        pid = run_cmd([cmd_str])
        
        while True:
            match get_cmd_status(pid):
                case CMD_STATUS.STOPPED:
                    raise ChildProcessError
                case CMD_STATUS.FINISHED:
                    break 
                case CMD_STATUS.ERROR:
                    raise ChildProcessError
                case CMD_STATUS.NOTFOUND:
                    raise ProcessLookupError
        return out_path