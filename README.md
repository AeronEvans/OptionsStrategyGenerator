# OptionsStrategyGenerator


https://github.com/user-attachments/assets/52d3ea2e-5d28-4d40-83bb-ef7d22cb174a

This application was developed using Python, Flask, and Polygon's stock and option API. The application fetches the latest available stock prices, using the free version of Polygon's API, which allows up to 5 calls per minute and provides end-of-day pricing information. As such, the stock price returned will reflect the most recent business day's closing value. Keep in mind that due to the limitations of the free API tier, the data you receive doesn't include the latest market movements if you require more frequent updates.

The api calls are written such that if the 5 per minute limit is exceeded, the function waits 20 seconds and tries again. This can cause some long wait times.

Application is limited to strategies featuring options that all that expire on the same date and are European style.
