from collect_photos import AwsTasks
from collect_photos.mounting import Mounting


def test_log_file():
    AwsTasks.log_file("logged_file")


def test_query_file():
    print(AwsTasks.query_file("logged_file"))


def test_load_upload_files():
    mount = Mounting(".")
    for item in mount.list_files_in_directory():
        AwsTasks.upload_file(item, mount)

def test_scan_missing():
    print(AwsTasks.scan_missing())
