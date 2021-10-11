import json

# API KEY (username)
# KyM0jVCxAhqsNqAsZ2nOm8H7j
#
# API KEY SECRET (password)
# MTo25vmP8W4YVKCRlYfigIEBlGsCOEIKBoxKFtFJxZiupwaaJK
#
# Bearer Token (Access token)
# AAAAAAAAAAAAAAAAAAAAALVMUgEAAAAAgrak%2BqrETp%2FJUhc%2FbgsS27qWWAI%3D4zb8Pz5iRpLENmpDvGKbLko8px3huB6MeALsxVQQRomfTf6ir0

credentials = {}
credentials["API_KEY"] = "KyM0jVCxAhqsNqAsZ2nOm8H7j"
credentials["API_KEY_SECRET"] = "MTo25vmP8W4YVKCRlYfigIEBlGsCOEIKBoxKFtFJxZiupwaaJK"
credentials["BEARER_TOKEN"] = "AAAAAAAAAAAAAAAAAAAAALVMUgEAAAAAgrak%2BqrETp%2FJUhc%2FbgsS27qWWAI%3D4zb8Pz5iRpLENmpDvGKbLko8px3huB6MeALsxVQQRomfTf6ir0"

with open("twitter_credentials.json", "w") as file:
    json.dump(credentials, file)