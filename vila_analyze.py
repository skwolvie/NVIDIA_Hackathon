# vila_analyze.py
import os
import requests
import uuid
from config import VILA_API_KEY

VILA_URL = "https://ai.api.nvidia.com/v1/vlm/nvidia/vila"
ASSET_URL = "https://api.nvcf.nvidia.com/v2/nvcf/assets"

def upload_asset(video_path):
    ext = "mp4"
    with open(video_path, "rb") as f:
        data_input = f.read()

    headers = {
        "Authorization": f"Bearer {VILA_API_KEY}",
        "Content-Type": "application/json",
        "accept": "application/json",
    }

    auth_res = requests.post(
        ASSET_URL,
        headers=headers,
        json={"contentType": "video/mp4", "description": video_path},
    )
    auth_res.raise_for_status()
    auth_data = auth_res.json()

    upload_res = requests.put(
        auth_data["uploadUrl"],
        data=data_input,
        headers={
            "x-amz-meta-nvcf-asset-description": video_path,
            "content-type": "video/mp4",
        },
    )
    upload_res.raise_for_status()

    return str(uuid.UUID(auth_data["assetId"]))

def analyze_and_rank(video_paths):
    asset_ids = [upload_asset(path) for path in video_paths]
    asset_refs = ",".join(asset_ids)
    print("Uploaded all videos. Analyzing...")

    headers = {
        "Authorization": f"Bearer {VILA_API_KEY}",
        "Content-Type": "application/json",
        "NVCF-INPUT-ASSET-REFERENCES": asset_refs,
        "NVCF-FUNCTION-ASSET-IDS": asset_refs,
        "Accept": "application/json",
    }

    messages = [{
        "role": "user",
        "content": (
            "These videos are moments from a travel journey. "
            "Please suggest the best sequence to make them feel like a continuous story. "
            "Return only the sorted filenames from video_1.mp4 to video_5.mp4."
        )
    }]

    payload = {
        "max_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.7,
        "seed": 42,
        "messages": messages,
        "model": "nvidia/vila"
    }

    response = requests.post(VILA_URL, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()["choices"][0]["message"]["content"]
    print(f"VILA suggested order: {result}")

    ordered = [name.strip() for name in result.split() if name.startswith("video_")]
    ordered_paths = [os.path.join(os.path.dirname(video_paths[0]), name) for name in ordered]

    return ordered_paths
