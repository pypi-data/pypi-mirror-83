# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['options_reticle']

package_data = \
{'': ['*'], 'options_reticle': ['templates/*']}

install_requires = \
['jinja2>=2.11.2,<3.0.0',
 'more-itertools>=8.5.0,<9.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.6.1,<2.0.0',
 'requests-whaor>=0.2.1,<0.3.0',
 'toml>=0.10.1,<0.11.0',
 'typer[all]>=0.3.2,<0.4.0',
 'yfs>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['options-reticle = options_reticle.core:app']}

setup_kwargs = {
    'name': 'options-reticle',
    'version': '0.3.1',
    'description': 'Generate OTM strike targets from tradingview watchlists.',
    'long_description': "\n![alt text](images/options_reticle_v4.png)\n\n<!-- # [FDD] **Options Reticle** -->\n# ***[FDD] Options Reticle caters to degenerate traders and gamblers worldwide, reaching out for long distant contract expiration and just OTM strike placement.***\n\n## 🍾🍾 **Congratulations on your choice of Options Reticle.** 🎉🎉\n\n### The Options Reticle provides a targeting system overlay that will show a horizontal OTM strike price and verticle expiration target. If you're thinking as soon as the expiration date has passed, this overlay will be useless; you're right but, you can use the `options-reticle` CLI tool to generate a new overlay from a watchlist exported from TradingView.\n\n\n## Install with [pipx](https://github.com/pipxproject/pipx)\n\n```bash\n$ pipx install options-reticle\n```\n### [>> WATCH THE SCRIPT RUN HERE <<](https://asciinema.org/a/366342)\n\n![alt text](images/aapl_basic.gif)\n\n[![alt text](https://www.tradingview.com/x/U95ddn6i/)](https://www.tradingview.com/x/U95ddn6i/)\n\n[![alt text](https://www.tradingview.com/x/bjJedDvF/)](https://www.tradingview.com/x/bjJedDvF/)\n\n[![alt text](https://www.tradingview.com/x/c1Md17a8/)](https://www.tradingview.com/x/c1Md17a8/)\n\n[![alt text](https://www.tradingview.com/x/cLFQzQFW/)](https://www.tradingview.com/x/cLFQzQFW/)\n\n\n## OVERLAY FEATURES:\n* `Quick Action PUT (QAP) Mode` - When you flip the chart by adding a 0- in front of the symbol, you will see the PUT contract target.\n* `Strike Price / Expiration Crosshairs`.\n* `Fill Mode` - Shows a fill between the historical price and the target strike price. It will show green when ITM and red when OTM.\n* `Target information panel` - Shows the company name, days till expiration, month and day of expiration, strike price, dollars OTM or ITM, and the contract type.\n* `Emotion Indicator` - Shows an exact representation of your feelings based on if you were in the trade. It has an accuracy of 99.9 percent.\n\n## QUICK ACTION PUT (QAP) MODE:\nThis style of reticle is not visible until you flip the chart. The advantage of the (QAP) is that it maintains the same appearance as the standard style of reticle, making PUT contract targeting feel the same. When targeting with (QAP) mode, be aware that the chart prices are reversed. Up is down, and down is up; this can be confusing but will feel normal overtime. Activate QAP mode by appending a `0-` to the symbol of the chart. If nothing appears, no put option data was found for that symbol.\n\n[![alt text](https://www.tradingview.com/x/z9Uqdo2h/)](https://www.tradingview.com/x/z9Uqdo2h/)\n\n## CALIBRATING YOUR RETICLE\nThe overlay is generated using the options-reticle CLI tool found on GitHub. The adjustment script will parse a watchlist exported from TradingView then download options data for each ticker in the watchlist. The max amount of symbols you can add to a single overlay is about 200. Any more than 200 and the overlay will crash. Luckily, If you use a TradingView watchlist with more than 200 ticker symbols to generate overlays, the options-reticle command-line tool will automatically create multiple overlays with 200 tickers each. You can add multiple overlays to your chart to get all the tickers in the watchlist.\n\n## RETICLE GENERATION AND MOUNTING:\n1. Add all the tickers you want to track into a watchlist on Tradingview.\n2. Export the watchlist into a txt file using TradingView's watchlist export list button.\n3. Open the terminal and change to the directory with the downloaded watchlist txt file.\n4. Install options-reticle command tool with pipx. pipx install tradingview-options-reticle.\n5. Run the command options-reticle download --watchlist {name of watchlist.txt file}. This will download the options data to an options_data.toml in the same directory as the watchlist txt file.\n6. Run the command options-reticle build --options-data-input-path options_data.toml. This will generate the overlay scripts. If the watch list has more than 200 ticker symbols, it will generate a separate overlay script for every 200 ticker symbol chunk.\n7. Copy and paste each of the generated overlay scripts one at a time into the Pine Editor on TradingView, then click the Add to Chart button. Make sure you copy the entire code.\n\n### EXAMPLE OF RETICLE GENERATION\n[![asciicast](https://asciinema.org/a/366342.png)](https://asciinema.org/a/366342)\n\n## FUTURE FEATURES:\n* Give the choice to generate PUT option contracts without using QAP mode. This option will allow you to use the input settings to change the contract type without flipping the chart.\n* Max OTM target argument - This will allow the option-reticle CLI to generate overlays with deeper OTM contracts. It currently only searches for the first OTM contract.\n* Add the ability to change the crosshair line type. [dash, dotted, solid]\n\n## TODO\n* [ ] More Testing.\n* [ ] More Features.\n* [ ] More Docs.\n\n## Contact Information\nTelegram = Twitter = Tradingview = Discord = @dgnsrekt\n\nEmail = dgnsrekt@pm.me\n",
    'author': 'dgnsrekt',
    'author_email': 'dgnsrekt@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dgnsrekt/tradingview-options-reticle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
