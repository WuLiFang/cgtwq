if True:
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import cgtwq


def main():
    db = cgtwq.Database("proj_sdktest")
    username = os.getenv("CGTEAMWORK_USERNAME", "")
    password = os.getenv("CGTEAMWORK_PASSWORD", "")
    if username and password:
        account = cgtwq.login(
            username,
            password,
        )
        db.token = account.token
    else:
        cgtwq.DesktopClient().connect()
    resp = db.call(
        "c_field",
        "get_in_module",
        field_array=["field_name"],
        module_array=["file", "history", "note", "version"],
    )
    print(resp)


if __name__ == "__main__":
    main()
