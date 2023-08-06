# Plurk Dice

## Install

```bash
pip install plurk-dice
```

## Usage

```python
>>> from plurk_dice import Dice

# Roll a dice directly

>>> Dice(20).roll()
{'result': 7, 'url': 'https://s.plurk.com/ff94b39b3f0927042f8479fac0fd92d1.png'}

>>> Dice("bzz").roll(base64=True)
{'result': 'B', 'url': 'https://s.plurk.com/e3481a0219283c49455d8af6012980ea.png', 'base64': 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAARxJREFUeNqs1bFLAmEYx/H3Ui6c2sR0jByV3EWE2gMRkyJpcDOXBsF2JynrDwhqUf8MHaWWtKWtocBwDhzCvhePcYOHd+/bC5/hOR5+vHfv3XOWrb6V5krgEEOMlxc3lP6KoYEbpP8jMIU48riTWjswigpCUmdwiz3dwCpyrnqOJLJhjbB91Fz1APeY4CNo4A5aciCf6Mjzm/51OK+NT1voYYERDlb1+Q0L4VrC+tj16vUTZuESX7iSnSqTwDpmaMJe178u7AxvOJedKpPAE7ygEuDgPANLeEI5SJhX4BEeUQwatirQuc1nnZ0tOV/KJiIooI42urojKCyz7BinuMCDwUj7HV/veJUPvK8MlyW/AGdQbsvEmJsE/ggwAMem4bIle0IVAAAAAElFTkSuQmCC'}

# Roll dices parse from text

>>> Dice.parse("(dice20)(dice8)")
[{'result': 2, 'url': 'https://s.plurk.com/27866de1cbed77d98cd8a886205c9dcb.png'}, {'result': 6, 'url': 'https://s.plurk.com/17c9123ed084f917ede14447afdfabdf.png'}]
>>> Dice.parse("(dice20)(dice8)", base64=True)
...
```

## Support emojis

- [x] ![dice4](https://s.plurk.com/a1fe8924e7dc4a4252b8e2c89fc729a4.png)
- [x] ![dice](https://s.plurk.com/7c9a7af9caf0bcbadc74ec87400eb66d.png)
- [ ] ~~(dice2)~~
- [x] ![dice8](https://s.plurk.com/7b990c34dc8f63d90a06a67b8eaf56aa.png)
- [x] ![digit](https://s.plurk.com/58d382c8ac312fb1471fc9ea586a961b.png)
- [x] ![dice10](https://s.plurk.com/001b8fae9b328c7d36a9e7f69d8fa922.png)
- [x] ![dice12](https://s.plurk.com/4694141aad1682240b2d3718beeccf67.png)
- [x] ![dice20](https://s.plurk.com/22ecc6bed8b99c6a111d5dbc65dc08fd.png)
- [x] ![bzz](https://s.plurk.com/129b757f2346a6e5ea782c79f0337ba9.png)
- [x] ![lots](https://s.plurk.com/469ccf8828b6eb697bbc55b35ed84202.png)

## Run tests

```bash
python -m unittest
```
