import hashlib
import platform


def get_client_id() -> str:
    raw = platform.platform() + platform.machine() + platform.processor() + \
        platform.release() + platform.version()
    return hashlib.sha512(hashlib.sha256(raw.encode()).digest()).hexdigest()
