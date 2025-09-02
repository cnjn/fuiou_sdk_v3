import os
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider


def upload_file(file_path: str, object_name: str):
    """
    上传文件到OSS
    """
    auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())
    bucket = oss2.Bucket(auth, os.getenv("OSS_ENDPOINT"), os.getenv("OSS_BUCKET"), region=os.getenv("OSS_REGION"))
    result = bucket.put_object_from_file(object_name, file_path)
    assert result.resp.status == 200, f"上传文件失败: {result.resp.status}"
    return result.resp.response.url