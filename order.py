import threading
import time
from datetime import datetime, timedelta

from scipy.special import order
from sqlalchemy import false
from sqlalchemy.sql.functions import current_time


class OrderStatusTracker:
    def __init__(self):
        self.order_statuses = {}

    def start_tracking(self, order_id):
        self.order_statuses[order_id] = {
            'status': 'Pending',
            'start_time': datetime.now()
        }
        threading.Thread(target=self._update_status, args=(order_id,), daemon=True).start()

    def _update_status(self, order_id):
        while True:
            time.sleep(60)
            current_time = datetime.now()
            start_time = self.order_statuses[order_id]['start_time']
            elapsed_time = (current_time - start_time).total_seconds() / 60

            if elapsed_time < 5:
                self.order_statuses[order_id]['status'] = 'Preparing'
            elif elapsed_time < 20:
                self.order_statuses[order_id]['status'] = 'Prepared'
            elif elapsed_time < 30:
                self.order_statuses[order_id]['status'] = 'Out for delivery'
            else:
                self.order_statuses[order_id]['status'] = 'Delivered'
                break

    def get_order_status(self, order_id):
        return self.order_statuses.get(order_id, {}).get('status', 'Order not found')

    def cancel_order(self, order_id):
        current_time = datetime.now()
        start_time = self.order_statuses[order_id]['start_time']
        elapsed_time = (current_time - start_time).total_seconds() / 60

        if elapsed_time < 5:
            self.order_statuses[order_id]['status'] = 'Cancelled'
            return True
        else:
            return False
