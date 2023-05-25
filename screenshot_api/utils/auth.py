def get_sub(user: dict):
    for attribute in user["UserAttributes"]:
        if attribute["Name"] == "sub":
            return attribute["Value"]
