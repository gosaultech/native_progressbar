import sys
import urllib.request
import time


def progress_bar(byte_count, total_bytes, status="", start_time=None, bar_length=20):
    """
    Displays a progress bar showing the download progress.

    Args:
    byte_count (int): The current count of downloaded bytes.
    total_bytes (int): The total number of bytes to be downloaded.
    status (str): An optional status message to be displayed.
    start_time (float): The start time of the download operation.
    """

    # bar logic goes here

    filled_len = int(round(bar_length * byte_count / float(total_bytes)))
    percent = round(100.0 * byte_count / float(total_bytes), 1)
    CSI = "\x1B["

    # if 1.0 <= percent <= 25.0:
    #     bar = (CSI+"31m" + u'\u2588' + CSI + "0m")  * filled_len + u'\u2591' * (bar_length - filled_len)
    # elif 26.0 < percent <= 75.0:
    #     bar = (CSI+"33m" + u'\u2588' + CSI + "0m")  * filled_len + u'\u2591' * (bar_length - filled_len)
    # elif 76.0 < percent <= 99.0:
    #     bar = (CSI+"32m" + u'\u2588' + CSI + "0m")  * filled_len + u'\u2591' * (bar_length - filled_len)
    # else:
    #     bar = (CSI+"34m" + u'\u2588' + CSI + "0m")  * filled_len + u'\u2591' * (bar_length - filled_len)
    # Nice way to remember getting rid of if conditions and making it run faster.
    colors = {
        (1.0, 25.0): CSI + "31m",
        (26.0, 75.0): CSI + "33m",
        (76.0, 99.0): CSI + "32m",
        (100.0, 100.0): CSI + "32m",
    }
    for r, color in colors.items():
        if r[0] <= percent <= r[1]:
            bar = (color + "\u2588" + CSI + "0m") * filled_len + "\u2591" * (
                bar_length - filled_len
            )
            if start_time:
                elapsed_time = time.time() - start_time
                transfer_rate = byte_count / elapsed_time
                remaining_size = total_bytes - byte_count

                if total_bytes >= 5 * 1024 * 1024:
                    total_bytes = total_bytes / (1024 * 1024)
                    total_size_unit = "MB"

                elif total_bytes >= 2 * 1024:
                    total_bytes = total_bytes / 1024
                    total_size_unit = "KB"

                if remaining_size >= 5 * 1024 * 1024:
                    remaining_size = remaining_size / (1024 * 1024)
                    size_unit = "MB"

                elif remaining_size >= 2 * 1024:
                    remaining_size = remaining_size / 1024
                    size_unit = "KB"

                else:
                    size_unit = "B"

                status += " | Rate: {:.2f} MB/s | Remaining: {:.2f} {} ({:.1f}% of total {:.2f} {})".format(
                    transfer_rate / (1024 * 1024),
                    remaining_size,
                    size_unit,
                    percent,
                    total_bytes,
                    total_size_unit,
                )
                if remaining_size > transfer_rate:
                    if size_unit == "MB":
                        remaining_time = remaining_size * 1024 * 1024 / transfer_rate
                    else:
                        remaining_time = remaining_size * 1024 / transfer_rate

                    if remaining_time > 3600:
                        status += " | Time remaining: {:.2f} hours".format(
                            remaining_time / 3600
                        )
                    elif remaining_time > 60:
                        status += " | Time remaining: {:.2f} minutes".format(
                            remaining_time / 60
                        )
                    else:
                        status += " | Time remaining: {:.2f} seconds".format(
                            remaining_time
                        )

            sys.stdout.write("\r{0}| {1}% {2}".format(bar, percent, status))
            sys.stdout.flush()


url = "https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi"
filename = "wsl_update_x64.msi"


with urllib.request.urlopen(url) as response, open(filename, "wb") as out_file:
    content_length = int(response.headers["Content-Length"])
    downloaded = 0
    block_size = 1024
    start_time = time.time()

    while True:
        data = response.read(block_size)
        if not data:
            break
        downloaded += len(data)
        out_file.write(data)
        progress_bar(
            downloaded, content_length, f"Downloading... {filename}", start_time
        )
    print()
