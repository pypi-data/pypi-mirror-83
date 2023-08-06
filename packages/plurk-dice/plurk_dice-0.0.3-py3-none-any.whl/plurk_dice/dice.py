import re
from base64 import b64encode
from random import choice
from typing import Dict, Union, List

import requests

DOMAIN = "https://s.plurk.com/"

DICE_ALIAS = {
    "dice4": 4,
    "dice": 6,
    "dice8": 8,
    "dice09": "digit",
    "數字骰": "digit",
    "dice10": 10,
    "dice12": 12,
    "dice20": 20,
    "draw": "lots",
    "lot": "lots",
    "bz": "bzz",
    "bzzz": "bzz",
}
DICE = {
    4: {  # YELLOW
        1: "8119f8d3c6530e1f96f5ae683641dfc3.png",
        2: "ab7b1d70a2989e4411276da40aab8cd4.png",
        3: "b68892fd60fbada8fe730ebaa51d93a1.png",
        4: "a1fe8924e7dc4a4252b8e2c89fc729a4.png",
    },
    6: {  # DICE
        1: "dde5171bb9139e692053f9ac66cbd564.png",
        2: "e7e1ede2d97726bf418a3abf9064869c.png",
        3: "c3e6d94310590416f656079db8ded155.png",
        4: "8329e14c55b7176a1030bf2be1c734dd.png",
        5: "ac7f20875fca82628e66933742ff5c36.png",
        6: "7c9a7af9caf0bcbadc74ec87400eb66d.png",
    },
    8: {  # PINK
        1: "c7909a13f2a1d82f6a8ec88806cedd5f.png",
        2: "8e09eec35e1ae9a9c506260f46f5fa80.png",
        3: "d7366d5512962df2cf1038627b3387f9.png",
        4: "e61038f50e60112b6cd029604a2e0c6a.png",
        5: "375320099fed5bcd480a33ceea294eb7.png",
        6: "17c9123ed084f917ede14447afdfabdf.png",
        7: "7cbe3526bf770399d9bed3e5217cc21f.png",
        8: "7b990c34dc8f63d90a06a67b8eaf56aa.png",
    },
    "digit": {
        0: "5d4b453d526bae111dd6f1cc5a8ff511.png",
        1: "03cd4200ea60e40a8619d22832b8565b.png",
        4: "2285e26f9a6267a73287077e75f426e5.png",
        5: "4f2d6e246649f284d0828905bf27e9b2.png",
        7: "32828c24085ea758139ed225458c7346.png",
        8: "bc8815c9ac0694dfa16bd19f0a52e008.png",
        9: "58d382c8ac312fb1471fc9ea586a961b.png",
    },
    10: {  # BLUE
        1: "c7b659f9a40b3aab4467416bac70743f.png",
        2: "9693e838340f3214072694beb7f6666b.png",
        3: "77b92b78a34a41fbe5482ea5a3ad79b9.png",
        4: "469377ad967761959d56e0db98bf0b48.png",
        5: "b4c493ae25e627b9af85750de47a98b4.png",
        6: "865614d05bcd6c9cd100684c5990c5c8.png",
        7: "e2af8a8d37c81179d61d38b2117cf625.png",
        8: "d96522745618c7861c15d3ceb56a0176.png",
        9: "5c201b2947b36c83a701537ce3b8cbc9.png",
        10: "001b8fae9b328c7d36a9e7f69d8fa922.png",
    },
    12: {  # WHITE
        1: "fdcbab46fbd767ad21ad4f8392622aa8.png",
        2: "16a33566c4e19dd18f1de9bf64c827c7.png",
        3: "659cc49e9386c3a804cdbe8b3e79aa9e.png",
        4: "83275472ae5574dff8cbff064e91a372.png",
        5: "128b9b64556f85d794770fa5523013b0.png",
        6: "e9863814d8baa64a10afaa0e740853d8.png",
        7: "ada656fad2ff0a7b0dd2a9c02c48bbd9.png",
        8: "31c19af18e7083b34a83011fa559d29f.png",
        9: "1397312c8b92664cb843663c03405f86.png",
        10: "8a18f029b74f50c318c881bf66f68562.png",
        11: "07c3b99baf30d0858d515c9fe52bef30.png",
        12: "4694141aad1682240b2d3718beeccf67.png",
    },
    20: {  # ORANGE
        1: "a517007a048ca131f7f1d778d1af9684.png",
        2: "27866de1cbed77d98cd8a886205c9dcb.png",
        3: "1a5cc269b657e7a814aca8aba27fa64f.png",
        4: "dcdec54c7152053492e01800b81e0e15.png",
        5: "bdd7628d6c87271ac349c84a24b5f138.png",
        6: "33203dae72cad566e2a140b531f802f2.png",
        7: "ff94b39b3f0927042f8479fac0fd92d1.png",
        8: "ad61d499e90390b525bcb1315e6f8e5c.png",
        9: "d305cc0e3cdf2ec56e6c9baa7c684f4a.png",
        10: "8f36fda06d7b86c7f612974b3ea52bdd.png",
        11: "d305cc0e3cdf2ec56e6c9baa7c684f4a.png",
        12: "3f8817112e4c988c89d8467e424f4feb.png",
        13: "73ca275f83000a6ddf34f98ab8759acc.png",
        14: "565fefd777bff763bf53bb2cf8f6f0f0.png",
        15: "611615a7152225c461050a3569ea1a2d.png",
        16: "1a33f859f00b5d98944892ee9333eb7c.png",
        17: "eacfe781bac35c429c2d747f3fd1ba94.png",
        18: "c7907086d6db450a140f5192baa88f37.png",
        19: "cf737a26669f491dd38e534007ea5dc4.png",
        20: "22ecc6bed8b99c6a111d5dbc65dc08fd.png",
    },
    "bzz": {
        "R": "129b757f2346a6e5ea782c79f0337ba9.png",
        "G": "5a2a63fa773e68797ec69a1303bfa3b9.png",
        "B": "e3481a0219283c49455d8af6012980ea.png",
        "K": "7bd4d66256fc805da4dd178b9fdbe3ce.png",
    },
    "lots": {
        "大吉": "469ccf8828b6eb697bbc55b35ed84202.png",
        "吉": "ed13a8c77dc92dd28996680c13f2fd92.png",
        "中吉": "a6f7de6aae635f616b67505261bc5291.png",
        "小吉": "3f1a1cc77b0a248ce7352509645efa87.png",
        "小凶": "c12ee0dbd02bf5329682919b39ebdeb3.png",
        "凶": "a3e3b6789eff8173ac192af1ed3f243a.png",
        "大凶": "bfe98f4effe412f4e5c9199cc27f6888.png",
    },
}


class Dice:
    def __init__(self, side: Union[int, str]):
        self.dice = DICE[side]

    def __getitem__(self, key: Union[str, int]) -> str:
        return DOMAIN + self.dice[key]

    def roll(self, base64=False) -> Dict[str, Union[str, int]]:
        """Roll the dice.

        Returns:
            Tuple[Union[str, int], str]: (key, url) pair
        """
        key = choice(list(self.dice.keys()))
        dice = {"result": key, "url": self[key]}
        if base64:
            dice["base64"] = to_base64(dice["url"])
        return dice

    @classmethod
    def parse(cls, text: str, **kwargs) -> List[Dict[str, Union[str, int]]]:
        """Parse text like usage in Plurk.

        Args:
            text (str): Text input
            kwargs: passed into `cls.roll()`

        Returns:
            List[Dict[str, Union[str, int]]]: All results from parsed dices.
        """
        results = re.findall(r"\((.*?)\)", text)
        return [cls(DICE_ALIAS.get(r, r)).roll(**kwargs) for r in results]


def to_base64(url: str) -> str:
    res = requests.get(url)
    return b64encode(res.content).decode()
