import json
import requests


def main():
    data = {
        'text': '''Всем привет. 27 декабря планирую посетить Тадж Махал. Так как я одна, если есть желающие можем организовать групповой тур.''',
    }

    response = requests.post("http://localhost:8013", data=json.dumps(data))

    if response.status_code == 200:
        print("POST request was successful")
        result = json.loads(response.text)
        print(result)
    else:
        print(f"POST request failed with status code: {response.status_code}")


if __name__ == '__main__':
    main()

