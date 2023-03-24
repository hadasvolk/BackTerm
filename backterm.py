import argparse
import json
import logging
import os
import random
import requests


logging.basicConfig(level=logging.INFO)

UNSPLASH_API_BASE_URL = "https://api.unsplash.com"


def build_query_params(args):
    query_params = {
        "client_id": args.api_key,
        "query": args.query,
        "orientation": args.orientation,
        "content_filter": args.content_filter,
        "order_by": args.order_by,
        "per_page": 30,
    }

    return query_params



def download_random_image(api_key, args):
    query_params = build_query_params(args)
    query_params['color'] = args.color

    try:
        response = requests.get(f"{UNSPLASH_API_BASE_URL}/search/photos", params=query_params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error fetching images from Unsplash: {e}")
        return None

    search_results = response.json()

    if not search_results['results']:
        logging.error("No images found.")
        return None

    random_image = random.choice(search_results['results'])
    image_url = random_image['urls']['raw'] + f'&fit=crop&w={args.resolution.split("x")[0]}&h={args.resolution.split("x")[1]}&q=80'

    try:
        image_response = requests.get(image_url)
        image_response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error fetching image file from Unsplash: {e}")
        return None

    image_path = os.path.join(os.path.expanduser('~'), 'Pictures', 'random_background.jpg')

    with open(image_path, 'wb') as f:
        f.write(image_response.content)

    # Save attribution information
    attribution = {
        'photographer': random_image['user']['name'],
        'profile_url': random_image['user']['links']['html'],
        'unsplash_url': "https://unsplash.com"
    }

    with open(os.path.join(os.path.expanduser('~'), 'Pictures', 'random_background_attribution.json'), 'w') as f:
        json.dump(attribution, f)

    return image_path



def update_windows_terminal_settings(image_path, is_preview):
    if image_path is None:
        logging.error("No image to set as background.")
        return

    try:
        # Locate the settings.json file
        if is_preview:
            settings_path = os.path.expandvars(
                r'%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminalPreview_8wekyb3d8bbwe\LocalState\settings.json'
            )
        else:
            settings_path = os.path.expandvars(
                r'%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json'
            )

        # Load the current settings
        with open(settings_path, 'r') as f:
            settings = json.load(f)

        # Update the backgroundImage setting for the default profile
        default_profile_guid = settings['defaultProfile']
        for profile in settings['profiles']['list']:
            if profile['guid'] == default_profile_guid:
                profile['backgroundImage'] = image_path
                break

        # Save the updated settings
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)

    except Exception as e:
        logging.error(f"Error updating Windows Terminal settings: {e}")


def main():
    parser = argparse.ArgumentParser(description="Download a random image from Unsplash and set it as the Windows Terminal background.")
    parser.add_argument(
        "--api-key", required=True, help="Your Unsplash API key."
    )
    parser.add_argument(
        "--color", default="black", help="Specify a primary color for the image (default: 'black')."
    )
    parser.add_argument(
        "--resolution", default="3440x1440", help="Specify the image resolution (default: '3440x1440')."
    )
    parser.add_argument(
        "--orientation", choices=["landscape", "portrait", "squarish"], default="landscape",
        help="Specify the image orientation (default: 'landscape')."
    )
    parser.add_argument(
        "--query", default="dark,abstract,pattern", help="Specify a custom search query to find images that match your interests (default: 'dark,abstract,pattern')."
    )
    parser.add_argument(
        "--content-filter", choices=["low", "high", "latest"], default="high",
        help="Filter images by content rating. Options: 'low', 'high' (default), 'latest'."
    )
    parser.add_argument(
        "--order-by", choices=["relevant", "latest", "popular"], default="popular",
        help="Order search results by 'relevant', 'latest', or 'popular' (default)."
    )
    parser.add_argument(
        "--preview", action="store_true", help="Use this flag to set the background for Windows Terminal Preview."
    )

    args = parser.parse_args()

    logging.info("Downloading random image...")
    image_path = download_random_image(args.api_key, args)

    if image_path:
        logging.info("Downloaded image successfully. Updating Windows Terminal settings...")
        update_windows_terminal_settings(image_path, args.preview)
        logging.info("Windows Terminal background updated.")

        # Load and display attribution information
        with open(os.path.join(os.path.expanduser('~'), 'Pictures', 'random_background_attribution.json'), 'r') as f:
            attribution = json.load(f)

        print("\nImage attribution:")
        print(f"Photographer: {attribution['photographer']}")
        print(f"Profile URL: {attribution['profile_url']}")
        print(f"Image source: {attribution['unsplash_url']}\n")

    else:
        logging.error("Failed to download image.")


if __name__ == "__main__":
    main()

