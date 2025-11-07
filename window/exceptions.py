class MonitorNumberError(Exception):
    def __init__(self, monitor_number: int):
        super().__init__(f'Монитор с номером {monitor_number} не существует.')
