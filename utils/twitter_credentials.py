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
credentials["API_KEY"] = "1447462574723829760-Ar1jUV4tWsvJG3lnoLvQAmVI2yq3PX"
credentials["API_KEY_SECRET"] = "qKbhfoUeQd09lB12SsOzs4D5q4hcSm2kVosQwOh7SoIZi"
credentials["BEARER_TOKEN"] = "AAAAAAAAAAAAAAAAAAAAALVMUgEAAAAAgrak%2BqrETp%2FJUhc%2FbgsS27qWWAI%3D4zb8Pz5iRpLENmpDvGKbLko8px3huB6MeALsxVQQRomfTf6ir0"
credentials["CONSUMER_KEY"] = "4foLTMr6CL4IWGJX1AlL1E2Gu"
credentials["CONSUMER_SECRET"] = "gZaUXnHazaFnAt774rmgwctmsTdMq2IQXF7ZdsKP65cxGL0I6J"

with open("../app/files/twitter_credentials.json", "w") as file:
    json.dump(credentials, file)