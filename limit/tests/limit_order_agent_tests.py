import unittest
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient

# Mocking the ExecutionClient to track executed orders without real executions
class MockExecutionClient(ExecutionClient):
    def __init__(self):
        self.executed_orders = []

    def execute_order(self, product_id, amount, action):
        # Simulate executing the order and storing the result
        self.executed_orders.append({
            'product_id': product_id,
            'amount': amount,
            'action': action
        })

class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self):
        # Set up a mock execution client and a LimitOrderAgent instance for testing
        self.execution_client = MockExecutionClient()
        self.agent = LimitOrderAgent(self.execution_client)

    def test_buy_ibm_below_100(self):
        # Test that IBM is bought when the price goes below $100
        self.agent.on_price_tick('IBM', 99)
        self.assertEqual(len(self.execution_client.executed_orders), 1)
        self.assertEqual(self.execution_client.executed_orders[0]['product_id'], 'IBM')
        self.assertEqual(self.execution_client.executed_orders[0]['amount'], 1000)
        self.assertEqual(self.execution_client.executed_orders[0]['action'], 'buy')

    def test_add_order_and_execute(self):
        # Add a new order for a different product and simulate a price tick to execute it
        self.agent.add_order('buy', 'PRODUCT_X', 500, 50.0)
        self.agent.on_price_tick('PRODUCT_X', 49)
        self.assertEqual(len(self.execution_client.executed_orders), 1)
        self.assertEqual(self.execution_client.executed_orders[0]['product_id'], 'PRODUCT_X')
        self.assertEqual(self.execution_client.executed_orders[0]['amount'], 500)
        self.assertEqual(self.execution_client.executed_orders[0]['action'], 'buy')

    def test_order_not_executed_if_limit_not_met(self):
        # Test that an order is not executed if the price does not meet the limit
        self.agent.add_order('sell', 'PRODUCT_X', 500, 60.0)
        self.agent.on_price_tick('PRODUCT_X', 59)
        self.assertEqual(len(self.execution_client.executed_orders), 0)  # No orders should be executed

if __name__ == '__main__':
    unittest.main()


