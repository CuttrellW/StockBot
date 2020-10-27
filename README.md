<h1>Stock Bot</h1>

<p>Stock bot is a program that utilizes Alpaca Trading API to autonomously trade a set of stocks determined by the user during trading hours.</p>

<h2>Installation</h2>

<p>Requirements</p>

<ul>
  <li>Python 3.8</li>
  <li>Alpaca Markets account, the website is <a href=alpaca.markets>alpaca.markets</a></li>
  <li>Preferred IDE: Pycharm</li>
  <li>Alpaca Trading API python library- The github for this library can be found <a href=https://github.com/alpacahq/alpaca-trade-api-python>here</a></li>
</ul>



<p>Make sure that your python is updated to the newest version. Go to alpaca.markets and sign into your account, once there you will need to make sure your account
is set to paper trading. In your paper trading overview find your api keys located on the rightside panel you need to copy your api key and secret key to insert into the api.py program.</p>

<p>*Note*: secret api key will only appear once when your api key is generated, make sure to save it in a safe location</p>

<p>Installing the program and external modules</p>

<p>In order to use this program you will need to install the modules provided by alpaca markets at <a href=https://github.com/alpacahq/alpaca-trade-api-python>alpaca github</a>.</p>

<p>Note: the current version of alpaca-trade-api will install an incompatable version of numPy. This can be resolved by installing and older version (1.18)</p>

<h2>Using the program</h2>

<p>In order to run this program, you must insert your Api Key Id and Secret Key into api.py</p>

<p>The program will trade a set of stocks in the default fleet, you can change these symbols by changing the strings elements of the list in fleet.py, then running the program again.</p>
