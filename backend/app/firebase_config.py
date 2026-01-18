import os
from firebase_admin import credentials, firestore, storage
import firebase_admin

# Load environment variables from .env file
private_key = os.getenv("MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCuomqBmh94J7KV\nsFxHyfknrQLpBeNn0Q1dujvCp2iqCtNv0dLFV35n/SxHmG3g4jrIa+HqFrrXxyd6\nGgtLyxSRwRNvkhrUY/BrnvEQof48v14q//h5tjSOf+cgq4890HKIPnmt9Tbm9zlO\nz2thuTzrHMCqMv7R/Bv2F1jgQruGM1WlOrrrU0hyz6yEiPwAJ35FHzfHwFlXl+l5\n7Oz/6iB8xWX/MXh4SfJ8KRTn5yhMV8bNh8pdT07wg8sVWTw5tAT9XYjReDwPsoWO\nDlnSh+8fqjPz9uIjBpjo6S3bxPxGfpO3098Vm3CNeJtLWk0I4rngyXOUwJevEMB5\nv75tTupVAgMBAAECggEAAlpJTYrY7YU5ZHIJDZA0xVpRGE2+QSM28czlFQus1GJL\ndBhIpY8hcpSzAJmW3LP83z+G07Yag8wuJbi372g3vs6crKuJpX6y2eb9BUCYHH47\n2PVJsMK/Oq6R8PsmtZ+QihyEsU7aU7+/u6ZTN8XnV8feIkeIGSZImSbk3raUxgDM\nI5LXrTtFgXJXViWDoEo5zMsFOCzo7ia/yu16FH6UYlm696rwDH6HxVRLyaKPsQo2\nQ5t2gwAKplLUb3FEGEGVBONXXAXs2O/f6N0w+yDVWC1OTeUq456leWfVthxgUUxT\nmdMPrZpPzFeRR8RdPdv8d226fwtTbkWN/kiPdTByAQKBgQDuj0ZayuNkBkBJjef7\nzY/94p4Fd++ky69La4q0G4mCRZj6kxM0Fhzk0LQoS2b50TxMVOZzc4HEOs2Gzq6z\neEmRd35L2I7Xu/8fks/42Wrog5Q6ZnkKEHcpindwAtcgQ8ychPElsDxoayW1/qY3\nIaXB1Do2LP85gdtyUA41lHs4VQKBgQC7ZsJDQWKnsG2fRrKoKJVNApuswhDNLKIB\n0c2Swpm5g9sRyRL4BqymfSqdhhkCpS2DE7wmPKPd3gt8Fael6b1kq/fcPdAI6ZZ/\nELHY5RBrxkD9PVRALV7E3UeLXSTsByXH5LjHEpgPN6ZXUkRnmpPVsNTApgZh/Xe5\nJv70B/7qAQKBgQDA9s2O1TwXhWLs3EdAi6ckUvFFNR137HXviJ6aTwfsgwVZ8it/\nXz+h6hs/2LYD7rZae/Yofs8BfhsPJxFzBCJl8wUKrrHkWSHlVSi6fosWZpA4qPjR\nJj5tMJ6p0PJYG99e3737oVFLmRfY3ZFvWN0uKs+nUMBlsN9j2NOVjXQaPQKBgFGa\ni5kxzb3rq7Ch3oYvNeRU8GkoEJznhJx6OaRgrQQFkM2L24C5l1DgTEBP9nAacVkU\nrOeRnGGuoR2laF1tDRXbdJEpMX/QB8LJCEjEZoQnzoD3xco0d4IOQWtEYiGNczw6\nMuQtCp4Fw59eqX7b5ug0mlBRe5IMB6hOfNLS8IQBAoGBANeEyYsErLd8rQhwbWYr\n+WQputIfbCJQ+EgeiCiJmZDHuBfcWMq8AtItP4WRpjv0W43iwzWIZYtou5I5g2tL\nm7n9D7fCp3WqVaRmSHLUQFLXnAcu9m2PHo7+nPYz7LoHCmC6BcKKhznwUHIL4oyL\nnJ73cZlr8C/LZhx84PKzZBDb")
private_key_id = os.getenv("dd860b73567463fa4c4ef575abc5029bc9db9c9f")

# Check if credentials exist
if not private_key or not private_key_id:
    raise RuntimeError("FIREBASE_PRIVATE_KEY or FIREBASE_PRIVATE_KEY_ID is not set in the environment variables")

# Replace escaped newlines with actual newlines in the private key
private_key = private_key.replace("\\n", "\n")

# Firebase service account key configuration
service_account_key = {
    "type": "service_account",
    "project_id": "speak-sharp-6bd84",
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": "firebase-adminsdk-fbsvc@speak-sharp-6bd84.iam.gserviceaccount.com",
    "client_id": "107155883031098895083",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40speak-sharp-6bd84.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# Initialize Firebase
cred = credentials.Certificate(service_account_key)

firebase_admin.initialize_app(cred, {
    'storageBucket': 'speak-sharp-6bd84.firebasestorage.app'
})

# Create database instance
db = firestore.client()