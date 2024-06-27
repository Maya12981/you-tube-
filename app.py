import os
import pytube

def download_playlist(playlist_url, output_folder, resolution="progressive", progress_bar=True):
    """Downloads a YouTube playlist to the specified folder.

    Args:
        playlist_url (str): The URL of the YouTube playlist.
        output_folder (str): The folder where the videos will be downloaded.
        resolution (str, optional): The desired video resolution (e.g., "720p", "progressive"). Defaults to "progressive".
        progress_bar (bool, optional): Whether to show a progress bar for each video. Defaults to True.

    Raises:
        pytube.exceptions.PyTubeException: If there's an error downloading the playlist or videos.
    """

    try:
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Get playlist object
        playlist = pytube.Playlist(playlist_url)

        # Iterate through videos
        for video_index, video in enumerate(playlist.videos):

            # Get video title with sanitized filename characters
            video_title = video.title.replace("|", "").replace("\\", "").replace(":", "").replace("*", "").replace("?", "").replace('"', '')

            # Choose stream based on resolution or progressive
            if resolution == "progressive":
                stream = video.streams.filter(progressive=True).order_by('resolution').desc().first()
            else:
                try:
                    stream = video.streams.filter(resolution=resolution).first()
                except pytube.exceptions.PyTubeException:
                    print(f"Warning: Resolution '{resolution}' not found for video '{video_title}'. Downloading progressive stream.")
                    stream = video.streams.filter(progressive=True).order_by('resolution').desc().first()

            # Download the video
            if progress_bar:
                print(f"Downloading video {video_index+1} of {len(playlist.videos)}: {video_title}")
            try:
                stream.download(output_path=output_folder, filename=f"{video_index+1}. {video_title}.{stream.subtype}")
            except pytube.exceptions.PyTubeException as e:
                print(f"Error downloading video '{video_title}': {e}")

        print("Playlist download complete!")

    except pytube.exceptions.PyTubeException as e:
        print(f"Error downloading playlist: {e}")

# Example usage
playlist_url = "https://www.youtube.com/playlist?list=PL-Jc9JyrGxT8VPvMfVk1vkzYMGGtK_i-p"  # Replace with your playlist URL
output_folder = "downloaded_playlist"
resolution = "720p"  # Optional, defaults to "progressive"
download_playlist(playlist_url, output_folder, resolution)
