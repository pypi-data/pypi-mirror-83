import requests

from dice import DICE, DOMAIN

if __name__ == "__main__":
    for k, d in DICE.items():
        for k2, v in d.items():
            name = f"{k}_{k2}.png"
            r = requests.get(DOMAIN + v, stream=True)
            if r.status_code == 200:
                with open(f"imgs/{name}", "wb") as f:
                    for chunk in r:
                        f.write(chunk)
            else:
                print(name, "failed!")
