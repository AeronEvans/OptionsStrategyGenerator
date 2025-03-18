from dataclasses import dataclass
from typing import List, Callable
try:
    from OptionsWebsite.Strategies_Library import *
    from OptionsWebsite.Polygon_Library import *
except:
    from Strategies_Library import *
    from Polygon_Library import *


class OptionPosition:
    def __init__(self, strike: float, is_call: bool, is_long: bool, premium: float):
        self.strike = round(strike, 2)
        self.is_call = is_call  # True for call, False for put
        self.is_long = is_long  # True for long position, False for short position
        self.premium = round(premium, 2)

    def __repr__(self):
        return (f"OptionPosition(strike={self.strike:.2f}, is_call={self.is_call}, "
                f"is_long={self.is_long}, premium={self.premium:.2f})")

    def __eq__(self, other):
        if not isinstance(other, OptionPosition):
            return False
        return (self.strike == other.strike and
                self.is_call == other.is_call and
                self.is_long == other.is_long and
                self.premium == other.premium)




def find_closest_option(market, target_strike, contract="call"):
    return min(market, key=lambda x: abs(x['strike_price'] - target_strike))


def create_strategy_profit_calculator(positions: List[OptionPosition]) -> Callable[[float], float]:
    def profit_function(stock_price: float) -> float:
        total_profit = 0
        for position in positions:
            if position.is_call:
                intrinsic_value = max(0, stock_price - position.strike)
            else:  # Put option
                intrinsic_value = max(0, position.strike - stock_price)
            position_multiplier = 1 if position.is_long else -1
            position_premium = position.premium * position_multiplier
            position_payoff = intrinsic_value * position_multiplier
            
            total_profit += position_payoff - position_premium
            
        return total_profit
    return profit_function


#list of strategies


def create_bull_call_spread(
    long_strike: float,
    short_strike: float,
    long_premium: float,
    short_premium: float
) -> Callable[[float], float]:
    positions = [
        OptionPosition(long_strike, is_call=True, is_long=True, premium=long_premium),
        OptionPosition(short_strike, is_call=True, is_long=False, premium=short_premium)
    ]
    return create_strategy_profit_calculator(positions), positions

def create_long_call(
    strike: float,
    premium: float
) -> Callable[[float], float]:
    positions = [OptionPosition(strike, is_call=True, is_long=True, premium=premium)]
    return create_strategy_profit_calculator(positions), positions

def create_iron_condor(
    long_put_strike: float,
    short_put_strike: float,
    short_call_strike: float,
    long_call_strike: float,
    long_put_premium: float,
    short_put_premium: float,
    short_call_premium: float,
    long_call_premium: float
) -> Callable[[float], float]:
    positions = [
        OptionPosition(long_put_strike, is_call=False, is_long=True, premium=long_put_premium),
        OptionPosition(short_put_strike, is_call=False, is_long=False, premium=short_put_premium),
        OptionPosition(short_call_strike, is_call=True, is_long=False, premium=short_call_premium),
        OptionPosition(long_call_strike, is_call=True, is_long=True, premium=long_call_premium)
    ]
    return create_strategy_profit_calculator(positions), positions

def create_bear_put_spread(
    long_put_strike: float,
    short_put_strike: float,
    long_premium: float,
    short_premium: float
) -> Callable[[float], float]:
    positions = [
        OptionPosition(long_put_strike, is_call=False, is_long=True, premium=long_premium),
        OptionPosition(short_put_strike, is_call=False, is_long=False, premium=short_premium)
    ]
    return create_strategy_profit_calculator(positions), positions

def create_long_put(
    strike: float,
    premium: float
) -> Callable[[float], float]:
    positions = [OptionPosition(strike, is_call=False, is_long=True, premium=premium)]

    return create_strategy_profit_calculator(positions), positions

