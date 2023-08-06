config = {
    # these values are related to the user's environment
    'env': {
        'databases': {
            'postgres_host': '127.0.0.1',
            'postgres_name': 'jesse_db',
            'postgres_port': 5432,
            'postgres_username': 'jesse_user',
            'postgres_password': 'password',
        },

        'logging': {
            'order_submission': True,
            'order_cancellation': True,
            'order_execution': True,
            'position_opened': True,
            'position_increased': True,
            'position_reduced': True,
            'position_closed': True,
            'shorter_period_candles': False,
            'trading_candles': True,
            'balance_update': True,
        },

        'exchanges': {
            'Sandbox': {
                'fee': 0,
                'starting_balance': 10000,
            },

            # https://www.bitfinex.com
            'Bitfinex': {
                'fee': 0.002,
                'starting_balance': 10000,
            },

            # https://www.binance.com
            'Binance': {
                'fee': 0.001,
                'starting_balance': 10000,
            },

            # https://www.binance.com
            'Binance Futures': {
                'fee': 0.0002,
                'starting_balance': 10000,
            },

            # https://testnet.binancefuture.com
            'Testnet Binance Futures': {
                'fee': 0.0002,
                'starting_balance': 10000,
            },

            # https://pro.coinbase.com
            'Coinbase': {
                'fee': 0.005,
                'starting_balance': 10000,
            },
        },

        # changes the metrics output of the backtest
        'metrics': {
            'sharpe_ratio': True,
            'calmar_ratio': False,
            'sortino_ratio': False,
            'omega_ratio': False,
            'winning_streak': False,
            'losing_streak': False,
            'largest_losing_trade': False,
            'largest_winning_trade': False,
            'total_winning_trades': False,
            'total_losing_trades': False,
        },

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Optimize mode
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #
        # Below configurations are related to the optimize mode
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        'optimization': {
            # sharpe, calmar, sortino, omega
            'ratio': 'sharpe',
        },

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Data
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #
        # Below configurations are related to the data
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        'data': {
            # The minimum number of warmup candles that is loaded before each session.
            'warmup_candles_num': 210,
        }
    },

    # These values are just placeholders used by Jesse at runtime
    'app': {
        # list of currencies to consider
        'considering_symbols': [],
        # The symbol to trade.
        'trading_symbols': [],

        # list of time frames to consider
        'considering_timeframes': [],
        # Which candle type do you intend trade on
        'trading_timeframes': [],

        # list of exchanges to consider
        'considering_exchanges': [],
        # list of exchanges to consider
        'trading_exchanges': [],

        'considering_candles': [],

        # dict of registered live trade drivers
        'live_drivers': {},

        # Accepted values are: 'backtest', 'livetrade', 'fitness'.
        'trading_mode': '',

        # variable used for test-driving the livetrade mode
        'is_test_driving': False,

        # this would enable many console.log()s in the code, which are helpful for debugging.
        'debug_mode': False,

        # setting this value to False would disable few validation checks which
        # are required for live trading on real markets, however, it is useful
        # for doing backtests simulations while faster strategy development.
        'strategy-validation': True
    },
}

backup_config = config.copy()


def set_config(c):
    """

    :param c:
    """
    global config
    config['env'] = c
    # add sandbox because it isn't in the local config file
    config['env']['exchanges']['Sandbox'] = {
        'fee': 0,
        'starting_balance': 10000,
    }


def reset_config():
    """

    """
    global config
    config = backup_config.copy()
