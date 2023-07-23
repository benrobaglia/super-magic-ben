# Copyright 2022 Cartesi Pte. Ltd.
#
# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from os import environ
import traceback
import logging
import requests
import json
from web3 import Web3
import base64
from py_expression_eval import Parser
from speaker_id import SpeakerId, AudioConverter, write_bytes_to_file, convert_flac_to_mono_wav

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

audio_converter = AudioConverter()
speaker_id = SpeakerId()

def decode_hex_json(payload):
    # Convert hex to bytes
    json_bytes = Web3.toBytes(hexstr=payload)
    # Decode bytes to string
    json_string = json_bytes.decode()
    # Load string as JSON
    json_obj = json.loads(json_string)
    # Get the base64 string
    audio_b64str = json_obj['audio_bytes']
    # Convert back to bytes
    audio_b64bytes = audio_b64str.encode()
    # Decode the base64 bytes to get original audio data
    audio_bytes = base64.b64decode(audio_b64bytes)
    return json_obj['function'], audio_bytes


def hex2bytes(hex):
    return bytes.fromhex(hex[2:])

def hex2str(hex):
    """
    Decodes a hex string into a regular string
    """
    return bytes.fromhex(hex[2:]).decode("utf-8")

def str2hex(str):
    """
    Encodes a string as a hex string
    """
    return "0x" + str.encode("utf-8").hex()


def handle_advance(data):
    # logger.info(f"Received advance request data {data}")
    logger.info(f"Received advance request data {data}")

    status = "accept"
    try:
        # Compute x-vector of the wav file and add it to the dictionary
        function_to_call, audio_bytes = decode_hex_json(data["payload"]) # 0 executes create_speaker and 1 executes verify_speaker
        write_bytes_to_file(audio_bytes, 'temp.flac')
        convert_flac_to_mono_wav('temp.flac')
        logger.info(f"Received input")
        if function_to_call == 0:
            output = speaker_id.create_speaker('temp.wav', f'speaker_reference')
        elif function_to_call == 1:
            output = speaker_id.verify_speaker('temp.wav', f'speaker_reference')
        # Emits notice with result of calculation
        logger.info(f"Adding notice with payload: '{output}', {str2hex(str(output))}")
        response = requests.post(rollup_server + "/notice", json={"payload": str2hex(str(output))})
        logger.info(f"Received notice status {response.status_code} body {response.content}")

    except Exception as e:
        status = "reject"
        msg = f"Error processing data {data}\n{traceback.format_exc()}"
        logger.error(msg)
        response = requests.post(rollup_server + "/report", json={"payload": str2hex(msg)})
        logger.info(f"Received report status {response.status_code} body {response.content}")

    return status

def handle_inspect(data):
    print(data["payload"])
    audio_converter.hex_to_wav(data["payload"][2:], 'temp.wav')
    logger.info(f"Received input")
    output = speaker_id.create_speaker('temp.wav', f'speaker_{len(speaker_id.speaker_dic)}')
    print(output)
    logger.info(f"Received inspect request data {data}")
    logger.info("Adding report")
    response = requests.post(rollup_server + "/report", json={"payload": str2hex(str(output))})
    logger.info(f"Received report status {response.status_code}")
    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}
rollup_address = None


while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        if "metadata" in data:
            metadata = data["metadata"]
            if metadata["epoch_index"] == 0 and metadata["input_index"] == 0:
                rollup_address = metadata["msg_sender"]
                logger.info(f"Captured rollup address: {rollup_address}")
                continue
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
