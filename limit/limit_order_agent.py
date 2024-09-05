from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []  # Initialize an order book

    def on_price_tick(self, product_id: str, price: float):
        """
        Called whenever the price of a product changes. Executes any orders that meet the price condition.
        """
        # Check if IBM price is below 100 and buy 1000 shares
        if product_id == "IBM" and price < 100:
            self.execution_client.execute_order(product_id, 1000, 'buy')

        # Execute orders based on their limit and price
        for order in self.orders:
            if order['product_id'] == product_id:
                if order['flag'] == 'buy' and price <= order['limit']:
                    self.execution_client.execute_order(order['product_id'], order['amount'], 'buy')
                elif order['flag'] == 'sell' and price >= order['limit']:
                    self.execution_client.execute_order(order['product_id'], order['amount'], 'sell')

    def add_order(self, buy_sell_flag: str, product_id: str, amount: int, limit: float):
        """
        Adds an order to the order book to be executed when the price condition is met.
        """
        order = {
            'flag': buy_sell_flag,
            'product_id': product_id,
            'amount': amount,
            'limit': limit
        }
        self.orders.append(order)
