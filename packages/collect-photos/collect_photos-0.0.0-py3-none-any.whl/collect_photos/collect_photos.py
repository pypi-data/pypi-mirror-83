from collect_photos import AwsTasks
from collect_photos.mounting import Mounting


class CollectPhotos:
    HelpMSG = """
    collect-photos start [directory]
        This Logs the Files and then starts uploading each of the photos up to AWS. 
        It is not recommended to run this command once all the data about each of 
        the photos is uploaded to AWS. The cost is that it will take a longer time
        to finish
         
        Thank You So Much LQZ.  
            Matthew Wen
        
        ARGS
        - directory: Directory Where the Halftoning Photos are located
        * NOTE: YOU ONLY NEED to run with ONCE with the same directory. DO NOT
        split it up based off of page #.
        
    collect-photos resume [directory]
        This connects directly to AWS, Scan for Files that are not uploaded yet. 
        And then resume uploading the reset of the photos. If you ever need to 
        stop uploading, you can use this command to continue uploading the 
        photos. 
        
        ARGS
        - directory: Directory Where the Halftoning Photos are located
        * NOTE: YOU ONLY NEED to run with ONCE with the same directory. DO NOT
        split it up based off of page #.
    """

    def __init__(self):
        pass

    @staticmethod
    def run(args):
        if len(args) < 3:
            print(CollectPhotos.HelpMSG)
            return
        directory = args[2]
        try:
            if args[1] == "start":
                CollectPhotos.start(directory)
            if args[1] == "resume":
                CollectPhotos.resume(directory)
        except KeyboardInterrupt:
            pass

    @staticmethod
    def log_status(i, num_files, service):
        if i % (int(num_files / 30) + 1) == 0:
            print(" -> {}% Done Uploading to {}".format(int(i / num_files * 100), service), end="\r")

    @staticmethod
    def upload_s3(list_files: list, mount: Mounting):
        num_files = len(list_files)
        for i, item in enumerate(list_files):
            AwsTasks.upload_file(item, mount)
            CollectPhotos.log_status(i, num_files, "s3")
        print("\nThank You SO MUCH LQZ!!!")

    @staticmethod
    def start(directory):
        temp = Mounting(directory)

        print("Started Logging Photos Into Database")
        files = temp.list_files_in_directory()
        num_files = len(files)

        if num_files == 0:
            print("Make Sure You Sent in the Correct Directory")

        db_client = AwsTasks.get_dynamodb_client(None)
        for i, item in enumerate(files):
            AwsTasks.log_file(item, client=db_client)
            CollectPhotos.log_status(i, num_files, "dynamodb")
        print("\nThere are {} Number of Files to Upload".format(len(files)))

        files = AwsTasks.scan_missing()
        if files is None or len(files) == 0:
            print("Already Finished! Thanks")
            return
        print("Found {} files out of {} files that need to upload".format(len(files), num_files))
        CollectPhotos.upload_s3(files, temp)

    @staticmethod
    def resume(directory):
        temp = Mounting(directory)
        files = AwsTasks.scan_missing()
        if files is None or len(files) == 0:
            print("Already Finished! Thanks")
            return
        print("Found {} file{} that still needed to be uploaded".format(len(files), "s" if len(files) != 1 else ""))
        files = [item["name"] for item in files]
        CollectPhotos.upload_s3(files, temp)
