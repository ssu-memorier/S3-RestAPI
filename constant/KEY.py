from utils import client

KEY_PATH = "assets/aws_keys.json"
READ_MODE = "r"
UTF8 = "utf-8"

S3CLIENT, S3BUCKET = client.getClientBucket(KEY_PATH, READ_MODE)
