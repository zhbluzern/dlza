import paramiko
import os
from zipfile import ZipFile
from dotenv import load_dotenv
import boto3 
from botocore.client import Config
import re

class goobiSSHConn:
    def __init__(self,logger):
        # 🔐 SSH-Verbindungsdaten
        load_dotenv()
        self.hostname = os.getenv("goobiSSHIP")
        self.port = os.getenv("goobiSSHPort")
        self.username = os.getenv("goobiSSHUser")
        self.private_key_path = os.getenv("goobiSSHPPK")
        self.logger = logger

        # 🔌 SSH-Verbindung aufbauen
        self.key = paramiko.RSAKey.from_private_key_file(self.private_key_path)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.hostname, self.port, self.username, pkey=self.key)

        # 📥 SFTP-Session starten
        self.sftp = self.ssh.open_sftp()

    # 📁 Dateien herunterladen
    def downloadFile(self, remote_file, local_file):
        self.sftp.get(remote_file, local_file)
        self.logger.log(f'✅ Downloaded: {remote_file} → {local_file}')


# sftp.close()
# ssh.close()

class goobiS3Conn():
    def __init__(self, logger):
        # 📄 LogFile
        self.logger = logger

        # 🔐 S3-Verbindungsdaten
        load_dotenv()
        self.aws_access_key_id = os.getenv("aws_access_key_id")
        self.aws_secret_access_key= os.getenv("aws_secret_access_key")
        self.region_name=os.getenv("aws_region")

        # 🌐 Custom S3 endpoint
        self.endpoint_url = os.getenv("aws_endpoint")
        self.bucket = os.getenv("aws_bucket")
        # 🛠 Create S3 client
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            endpoint_url=self.endpoint_url,
            config=Config(signature_version='s3v4'),
           # region_name=os.getenv("aws_region") # often ignored by custom S3
        )


if __name__ == "__main__":
    goobiSSH = goobiSSHConn()
    remote_dir = "/opt/digiverso/goobi/metadata/10643/"
    ls = goobiSSH.sftp.listdir(remote_dir)
    metaFiles = ["meta.xml", "meta_anchor.xml"]
    for file in ls:
        if file in metaFiles:
            goobiSSH.downloadFile(f"{remote_dir}{file}", f"boilerplate/zentralgut/test_{file}")

    # remote_file="/opt/digiverso/goobi/rulesets/ruleset.xml"
    # local_file="boilerplate/ruleset.xml"
    # #goobiSSH.downloadFile(remote_file,local_file)
    # rulesets = goobiSSH.sftp.listdir("/opt/digiverso/goobi/rulesets/")
    # print(rulesets)


    # s3Conn = goobiS3Conn()
    # response = s3Conn.s3.list_objects_v2(Bucket=s3Conn.bucket, Prefix="10643/")
    # #print(response)
    # print(response["Prefix"])
    # for obj in response.get('Contents', []):
    #     print(obj['Key'])
        # fileName = re.sub(response["Prefix"],"",obj["Key"])
        # localPath = f"boilerplate/zentralgut/{fileName}"
        # s3Conn.s3.download_file(s3Conn.bucket, obj['Key'], localPath)
        # print(f"✅ Downloaded { obj['Key']} → {localPath}")