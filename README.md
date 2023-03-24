# BackTerm
BackTerm is a command-line tool that allows you to download random images from [Unsplash](https://unsplash.com) and set them as the background for the Windows Terminal or Windows Terminal Preview. You can customize the images by specifying parameters like color, resolution, orientation, and more.

## Installation
To use BackTerm, you'll need to have Python 3.6 or higher installed on your machine. You'll also need to install the requests library, which you can do by running the following command:

```bash
pip install requests
```
Once you've installed the required dependencies, you can download the BackTerm code from GitHub. You can either download the code as a ZIP file and extract it, or you can clone the repository using Git:

```bash
git clone https://github.com/hadasvolk/BackTerm.git
```


## Usage
To use BackTerm, you'll need to sign up for an Unsplash API key. You can do this by visiting the [Unsplash Developers](https://unsplash.com/developers) page and following the instructions there.

Once you've obtained your API key, you can use it to run BackTerm. Open a terminal window and navigate to the folder where you've saved the BackTerm code. Then, run the following command:


```bash
python backterm.py --api-key YOUR_API_KEY
```
By default, BackTerm will search for dark, abstract, and patterned images with a resolution of 3440x1440, landscape orientation, high content filter, and ordered by popularity. You can customize these parameters using command-line arguments:

```bash
--color: Specify a primary color for the image (default: 'black').
--resolution: Specify the image resolution (default: '3440x1440').
--orientation: Specify the image orientation (default: 'landscape').
--query: Specify a custom search query to find images that match your interests (default: 'dark,abstract,pattern').
--content-filter: Filter images by content rating (default: 'high').
--order-by: Order search results by 'relevant', 'latest', or 'popular' (default).
```

To set the background for Windows Terminal Preview, use the --preview flag:
```bash
python backterm.py --api-key YOUR_API_KEY --preview
```

## Attribution
BackTerm uses the Unsplash API to download images. By using BackTerm, you agree to comply with the Unsplash API Guidelines.

To comply with the guidelines, BackTerm automatically downloads the attribution information for each image you download and displays it in the console when the image is set as the background. Please ensure that you provide proper attribution when using images downloaded by BackTerm.

## License
[INSERT LICENSE HERE]