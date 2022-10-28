from restAPI import manage


if __name__ == "__main__":
    with open("assets/test.pdf", "rb") as file:
        jsonData = {
            "file": file,
            "keyName": "test/test.pdf",
            "fileName": "test.pdf",
            "action": "upload"
        }

        manage.app(jsonData)
