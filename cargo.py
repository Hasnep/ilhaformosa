from helpers import *


class Cargo(object):
    def __init__(self):
        self.types = ["tea", "silk", "porcelain", "jade"]
        self.base_prices = {"tea": 100, "silk": 200, "porcelain": 300, "jade": 400}
        self.global_values = {cargo_type: 0 for cargo_type in self.types}
        self.volatility = 20
        self.control = 10
        self.variability = 1

    def calculate_prices(self, local_values: dict) -> dict:
        prices = {
            cargo_type: None for cargo_type in self.types
        }  # TODO: Find out if it is quicker to preallocate a dict
        for cargo_type in self.types:
            prices[cargo_type] = round_to(
                self.base_prices[cargo_type]
                * (1 + self.volatility / 1000)
                ** (self.global_values[cargo_type] + local_values[cargo_type])
            )
        return prices

    def my_inverse_logit(self, x: float) -> float:
        return math.exp(x / self.control) / (1 + math.exp(x / self.control))

    def randomise_values(self, starting_values: dict, n_days: int) -> dict:
        values = {cargo_type: None for cargo_type in self.types}
        for cargo_type, starting_value in starting_values.items():
            this_cargos_value = starting_value
            for day in range(n_days):
                if random.random() > self.my_inverse_logit(this_cargos_value):
                    this_cargos_value += 1
                else:
                    this_cargos_value -= 1
                this_cargos_value += random.gauss(0, self.variability)
            values[cargo_type] = this_cargos_value
        return values

    def table_cargo_prices(
        self, cargo_prices: dict, cargo_owned: dict
    ) -> None:  # TODO: Add 'cargo_bought_for: dict'
        table_aligned_print(
            column_names=["Price", "Owned"],
            column_aligns=["r", "r"],
            row_keys=self.types,
            column_dicts=[price_per_weight(cargo_prices), weight(cargo_owned)],
            show_row_keys=True,
        )
        return


cargo = Cargo()
