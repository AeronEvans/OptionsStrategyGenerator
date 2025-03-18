import numpy as np
from dataclasses import dataclass
from typing import List, Callable
import matplotlib
import matplotlib.pyplot as plt
try:
    from OptionsWebsite.Strategies_Library import *
    from OptionsWebsite.Polygon_Library import *
except:
    from Strategies_Library import *
    from Polygon_Library import *
import io



def plot_result(strategy, profit_function, current_price, target_price):
    # Generate a range of prices

    prices = np.linspace(min(current_price,target_price)*0.75,max(current_price,target_price)*1.25,100)
    profits = [profit_function(price) for price in prices]
    
    # Calculate the profit at the target price
    target_profit = profit_function(target_price)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(prices, profits, label='Profit vs Price')
    
    # Add vertical lines for current and target prices
    ax.axvline(x=current_price, color='red', linestyle='--', label=f'Current Price: {current_price}')
    ax.axvline(x=target_price, color='green', linestyle='--', label=f'Target Price: {target_price}')
    
    # Set plot titles and labels
    ax.set_title(strategy + ' Profit vs Price')
    ax.set_xlabel('Price of the underlying ($)')
    ax.set_ylabel('Profit ($)')
    ax.grid(True)
    
    # Show the legend in the top-left corner
    ax.legend(loc='upper left')

    # Display the profit label in the top-right corner inside the chart
    ax.text(0.95, 0.95, f'Profit at target price: {target_profit:.2f}', color='green', fontsize=12,
            ha='right', va='top', transform=ax.transAxes,
            bbox=dict(facecolor='white', edgecolor='green', boxstyle='round,pad=0.5'))

    # Display the plot
    plt.show()

def plot_result_image(strategy, profit_function, current_price, target_price):
    matplotlib.use('Agg')
    prices = np.linspace(min(current_price, target_price) * 0.75, max(current_price, target_price) * 1.25, 50)
    profits = [profit_function(price) for price in prices]
    
    target_profit = profit_function(target_price)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(prices, profits, label='Strategy profit')
    ax.axvline(x=current_price, color='red', linestyle='--', label=f'Current Price: {current_price}')
    ax.axvline(x=target_price, color='green', linestyle='--', label=f'Target Price: {target_price}')
    
    # Add the profit label at the target price
    ax.text(0.95, 0.95, f'Profit at target price: {target_profit:.2f}', color='green', fontsize=12,
            ha='right', va='bottom', transform=ax.transAxes,
            bbox=dict(facecolor='white', edgecolor='green', boxstyle='round,pad=0.5'))

    # Set plot titles and labels
    ax.set_title(strategy + ' Strategy Profit vs Price of the Underlying', fontsize=17, pad=20)
    ax.set_xlabel('Price of the underlying ($)')
    ax.set_ylabel('Profit ($)')
    ax.grid(True)
    ax.legend(loc='upper left')

    # Save the plot to a BytesIO object
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', dpi=300, bbox_inches='tight')
    plt.close(fig)  # Close the figure to free memory
    img_io.seek(0)  # Move the pointer to the start of the BytesIO object

    return img_io  # Return the image object



def strategy_picker(market, current_price, target_price, chosen_strategy=None, position_strikes={}):
    if chosen_strategy == "Long Call" or (chosen_strategy is None and target_price > current_price * 1.3):
        strategy = "Long Call"
        long_call_strike = position_strikes.get("long_call_strike", target_price * 0.95)
        long_call_premium = get_option_contract_cost(find_closest_option(market, long_call_strike)["ticker"])
        profit_function, positions = create_long_call(long_call_strike, long_call_premium)
        strategy_cost = round(long_call_premium, 2)

    elif chosen_strategy == "Bull Call Spread" or (target_price > current_price * 1.1 and chosen_strategy is None):
        strategy = "Bull Call Spread"
        long_call_strike = position_strikes.get("long_call_strike", target_price * 0.95)
        short_call_strike = position_strikes.get("short_call_strike", target_price * 1.05)
        long_call_premium = get_option_contract_cost(find_closest_option(market, long_call_strike)["ticker"])
        short_call_premium = get_option_contract_cost(find_closest_option(market, short_call_strike)["ticker"])
        profit_function, positions = create_bull_call_spread(long_call_strike, short_call_strike,
                                                 long_call_premium, short_call_premium)
        strategy_cost = round(long_call_premium - short_call_premium, 2)

    elif chosen_strategy == "Iron Condor" or (target_price > current_price * 0.9 and chosen_strategy is None):
        strategy = "Iron Condor"
        long_put_strike = position_strikes.get("long_put_strike", target_price * 0.90)
        short_put_strike = position_strikes.get("short_put_strike", target_price * 0.95)
        short_call_strike = position_strikes.get("short_call_strike", target_price * 1.05)
        long_call_strike = position_strikes.get("long_call_strike", target_price * 1.10)
        
        long_put_premium = get_option_contract_cost(find_closest_option(market, long_put_strike)["ticker"].replace("C", "P"))
        short_put_premium = get_option_contract_cost(find_closest_option(market, short_put_strike)["ticker"].replace("C", "P"))
        short_call_premium = get_option_contract_cost(find_closest_option(market, short_call_strike)["ticker"])
        long_call_premium = get_option_contract_cost(find_closest_option(market, long_call_strike)["ticker"])
        
        profit_function, positions = create_iron_condor(long_put_strike, short_put_strike, short_call_strike, long_call_strike,
                                             long_put_premium, short_put_premium, short_call_premium, long_call_premium)
        strategy_cost = round((long_put_premium + long_call_premium) - (short_put_premium + short_call_premium), 2)

    elif chosen_strategy == "Bear Put Spread" or (target_price > current_price * 0.7 and chosen_strategy is None):
        strategy = "Bear Put Spread"
        long_put_strike = position_strikes.get("long_put_strike", target_price * 1.05)
        short_put_strike = position_strikes.get("short_put_strike", target_price * 0.95)
        long_put_premium = get_option_contract_cost(find_closest_option(market, long_put_strike)["ticker"].replace("C", "P"))
        short_put_premium = get_option_contract_cost(find_closest_option(market, short_put_strike)["ticker"].replace("C", "P"))
        profit_function, positions = create_bear_put_spread(long_put_strike, short_put_strike,
                                                 long_put_premium, short_put_premium)
        strategy_cost = round(long_put_premium - short_put_premium, 2)

    elif chosen_strategy == "Long Put" or (target_price < current_price * 0.7 and chosen_strategy is None):
        strategy = "Long Put"
        long_put_strike = position_strikes.get("long_put_strike", target_price * 1.05)
        long_put_premium = get_option_contract_cost(find_closest_option(market, long_put_strike)["ticker"].replace("C", "P"))
        profit_function, positions = create_long_put(long_put_strike, long_put_premium)
        strategy_cost = round(long_put_premium, 2)

    return strategy, profit_function, strategy_cost, positions







def main():
    global date
    date = "2025-02-21"
    ticker = "BKNG"
    expiration_dates = ['2025-02-28','2025-03-07', '2025-03-14', '2025-03-21', '2025-03-28', '2025-04-04', '2025-04-17', '2025-05-16',
                        '2025-06-20', '2025-07-18', '2025-08-15', '2025-09-19', '2025-11-21', '2025-12-19', '2026-01-16', '2026-03-20',
                        '2026-06-18', '2026-09-18', '2026-12-18', '2027-01-15', '2027-06-17']
    
    expiration = expiration_dates[3]

    current_price = get_stock_price(ticker, date)
    print("current price: ", current_price)
    target_price = float(input("Target price: "))

    market = get_option_market(ticker, expiration)


    strategy, profit_function, strategy_cost, positions = strategy_picker(market, current_price, target_price)
    print("Strategy: ", strategy)

    for position in positions:
        print(repr(position))

    print("price of implementing the strategy = ", strategy_cost)
    plot_result(strategy, profit_function, current_price, target_price)



if __name__ == "__main__":
    main()