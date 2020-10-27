<h1>Stock Bot</h1>

<p>Stock bot is a program that integrates alpaca trading to automatically trade a set fleet of stocks during trading hours.</p>

<h2>Installation</h2>

<p>Requirements</p>

<ul>
  <li>Python 3.8</li>
  <li>Alpaca Markets account, the website is <a href=alpaca.markets>alpaca.markets</a></li>
  <li>Preferred IDE: Pycharm</li>
</ul>

<p>Make sure that your python is updated to the newest version. Go to alpaca.markets and sign into your account, once there you will need to make sure your account
is set to paper trading. In your paper trading overview find your api keys located on the rightside panel you need to copy your api key and secret key to insert into the api.py program.</p>

<p>*Note*: secret api key will only appear once when your api key is generated, make sure to save it in a safe location</p>

<p>Installing the program and external modules</p>

<p>In order to use this program you will need to install the modules provided by alpaca markets at <a href=https://github.com/alpacahq/alpaca-trade-api-python>alpaca github</a>.</p>
<p>Using pycharm create a new project and select VCS|Get From Version Control. Once in the version control menu select github and enter in this projects url. You will also need to install pandas, you can do so in your terminal using</p>

<pre><code>pip install pandas</code></pre>

Once you have the source code from this project and the alpaca and pandas modules installed you should be able to start trading.
