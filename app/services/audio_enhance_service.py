import time
import logging
from io import BytesIO

import requests
from requests.auth import HTTPBasicAuth
from app.config import settings
from app.repositories.audio_file_repository import AudioFileRepository


class AudioEnhanceService:
    BASE_URL = "https://api.dolby.com"
    AUTH_URL = "https://api.dolby.io/v1/auth/token"

    def __init__(self, api_key, api_secret):
        self.access_token = self._get_access_token(api_key, api_secret)
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _get_access_token(self, api_key, api_secret):
        payload = {"grant_type": "client_credentials", "expires_in": 1800}
        response = requests.post(self.AUTH_URL, data=payload, auth=HTTPBasicAuth(api_key, api_secret))
        response.raise_for_status()
        return response.json()["access_token"]

    def _api_request(self, method, endpoint, **kwargs):
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response.json()

    def upload_file(self, audio_buffer, dlb_url):
        data = self._api_request("POST", "/media/input", json={"url": dlb_url})
        presigned_url = data["url"]
        logging.info(f"Uploading to DOLBY")
        requests.put(presigned_url, data=audio_buffer)

    def enhance_media(self, input_url, output_url):
        body = {"input": input_url, "output": output_url}
        return self._api_request("POST", "/media/enhance", json=body)["job_id"]

    def get_job_status(self, job_id):
        return self._api_request("GET", "/media/enhance", params={"job_id": job_id})

    def download_file_to_buffer(self, dlb_out) -> BytesIO:
        params = {"url": dlb_out}
        with requests.get(f"{self.BASE_URL}/media/output", params=params, headers=self.headers,
                          stream=True) as response:
            response.raise_for_status()
            buffer = BytesIO()
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    buffer.write(chunk)
        buffer.seek(0)
        return buffer


def enhance_and_persist_audio(audio_buffer, call_id):
    audio_repository = AudioFileRepository()
    audio_file_reference = audio_repository.get_audio_file_by_call_id(call_id)
    enhancer = AudioEnhanceService(settings.DOLBY_AUDIO_KEY, settings.DOLBY_AUDIO_SECRET)

    dlb_in = "dlb://in/enhance"
    dlb_out = "dlb://out/enhance"

    enhancer.upload_file(audio_buffer, dlb_in)
    job_id = enhancer.enhance_media(dlb_in, dlb_out)

    while True:
        status = enhancer.get_job_status(job_id)
        if status["status"] not in {"Pending", "Running"}:
            break
        print(".", end="", flush=True)
        time.sleep(5.0)

    enhanced_file_path = f"{call_id}/{call_id}_enhanced.wav"
    enhanced_audio_buffer = enhancer.download_file_to_buffer(dlb_out)
    audio_repository.save_audio_file_to_bucket(enhanced_audio_buffer, enhanced_file_path)

    updated_audio_file = audio_file_reference.model_copy(update={
        "enhanced_file_path": enhanced_file_path
    })

    audio_repository.update_audio_file(call_id, updated_audio_file)
