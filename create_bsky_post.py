#!/usr/bin/env python3

import os
import sys
import json
import argparse
from typing import Dict
from datetime import datetime, timezone
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup

def bsky_login_session(pds_url: str, handle: str, password: str) -> Dict:
    resp = requests.post(
        pds_url + "/xrpc/com.atproto.server.createSession",
        json={"identifier": handle, "password": password},
    )
    resp.raise_for_status()
    return resp.json()


def upload_file(pds_url, access_token, filename, img_bytes) -> Dict:
    suffix = filename.split(".")[-1].lower()
    mimetype = "application/octet-stream"
    if suffix in ["png"]:
        mimetype = "image/png"
    elif suffix in ["jpeg", "jpg"]:
        mimetype = "image/jpeg"
    elif suffix in ["webp"]:
        mimetype = "image/webp"

    # WARNING: a non-naive implementation would strip EXIF metadata from JPEG files here by default
    resp = requests.post(
        pds_url + "/xrpc/com.atproto.repo.uploadBlob",
        headers={
            "Content-Type": mimetype,
            "Authorization": "Bearer " + access_token,
        },
        data=img_bytes,
    )
    resp.raise_for_status()
    return resp.json()["blob"]


def upload_image(
    pds_url: str, access_token: str, image_path: str, alt_text: str
) -> Dict:
    images = []
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    # this size limit specified in the app.bsky.embed.images lexicon
    if len(img_bytes) > 1000000:
        raise Exception(
            f"image file size too large. 1000000 bytes maximum, got: {len(img_bytes)}"
        )
    blob = upload_file(pds_url, access_token, image_path, img_bytes)
    images.append({"alt": alt_text or "", "image": blob})
    return {
        "$type": "app.bsky.embed.images",
        "images": images,
    }


def create_post(args):
    session = bsky_login_session(args.pds_url, args.handle, args.password)

    # trailing "Z" is preferred over "+00:00"
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # these are the required fields which every post must include
    post = {
        "$type": "app.bsky.feed.post",
        "text": args.text,
        "createdAt": now,
        "langs": ["en-US"]
    }

    # Image upload
    if args.image:
        # Assuming `args.image` is a list of file paths to image files
        image_url = upload_image(args.pds_url, session["accessJwt"], "resources/today_sp.jpg", f"{args.text}")["images"]
        
        # Embed images in the post
        post["embed"] = {
            "$type": "app.bsky.embed.images",
            "images": image_url
        }
    
    print("creating post:", file=sys.stderr)
    print(json.dumps(post, indent=2), file=sys.stderr)

    resp = requests.post(
        args.pds_url + "/xrpc/com.atproto.repo.createRecord",
        headers={"Authorization": "Bearer " + session["accessJwt"]},
        json={
            "repo": session["did"],
            "collection": "app.bsky.feed.post",
            "record": post,
        },
    )
    print("createRecord response:", file=sys.stderr)
    print(json.dumps(resp.json(), indent=2))
    resp.raise_for_status()


def main():
    parser = argparse.ArgumentParser(description="bsky.app post upload")
    parser.add_argument(
        "--pds-url", default=os.environ.get("ATP_PDS_HOST") or "https://bsky.social"
    )
    load_dotenv()
    parser.add_argument("--handle", default=os.getenv("ATP_AUTH_HANDLE"))
    parser.add_argument("--password", default=os.getenv("ATP_AUTH_PASSWORD"))
    parser.add_argument("text", type=str, default="")
    parser.add_argument("--image", action="append")
    parser.add_argument("--alt-text")
    parser.add_argument("--langs", action="append")
    parser.add_argument("--reply-to")
    parser.add_argument("--embed-url")
    parser.add_argument("--embed-ref")
    args = parser.parse_args()
    if not (args.handle and args.password):
        print(args.handle)
        print("both handle and password are required", file=sys.stderr)
        sys.exit(-1)
    if args.image and len(args.image) > 4:
        print("at most 4 images per post", file=sys.stderr)
        sys.exit(-1)

    # Check if `text` is a file and read content if so
    if os.path.isfile(args.text):
        with open(args.text, 'r', encoding='utf-8') as f:
            args.text = f.read()
    
    create_post(args)


if __name__ == "__main__":
    main()