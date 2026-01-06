from typing import List, Dict
import json


def calculate_panels(
    panel_width: int, panel_height: int, roof_width: int, roof_height: int
) -> int:
    # simple fit
    def fit(rw, rh, pw, ph) -> int:
        """
        Dado ancho y alto de paneles(pw,ph) y el techo(pw,ph)
        Calcula cuantos paneles cabrían en UNA orientación específica.
        """

        if pw <= 0 or ph <= 0 or pw > rw or ph > rh:
            return 0
        return (rw // pw) * (rh // ph)

    def get_max_for_split(dim_to_split, static_dim, orientations):
        """
        Dado las orientaciones con rotaicones de 90° prueba todas las combinaciones posibles en cada punto de la grilla donde podría ir un panel.

        """
        best = 0

        split_points = set()  # Set elimina los duplicados
        for pw, ph in orientations:
            split_points.update(range(pw, dim_to_split, pw))
            split_points.update(range(ph, dim_to_split, ph))

        # Todos los puntos en donde habría un panel seǵun su tamaño
        for split in split_points:
            for pw1, ph1 in orientations:
                for (
                    pw2,
                    ph2,
                ) in orientations:  # Es necesario hacer este nivel de nesteo?
                    count = fit(static_dim, split, pw1, ph1) + fit(
                        static_dim, dim_to_split - split, pw2, ph2
                    )
                    if count > best:
                        best = count
        return best

    # Nos limitaremos a dos orientaciones posibles para los paneles con rotaciones de 90°
    orientations = {(panel_width, panel_height), (panel_height, panel_width)}

    # Calculamos para ambas orientaciones considerando todo el techo
    max_panels = max(fit(roof_width, roof_height, pw, ph) for pw, ph in orientations)

    if panel_height != panel_width:
        # Ahora revisamos para casos en donde los paneles no son cuadrados
        max_panels = max(
            max_panels,
            get_max_for_split(roof_height, roof_width, orientations),
        )
        max_panels = max(
            max_panels,
            get_max_for_split(roof_width, roof_height, orientations),
        )

    return max_panels


def run_tests() -> None:
    with open("test_cases.json", "r") as f:
        data = json.load(f)
        test_cases: List[Dict[str, int]] = [
            {
                "panel_w": test["panelW"],
                "panel_h": test["panelH"],
                "roof_w": test["roofW"],
                "roof_h": test["roofH"],
                "expected": test["expected"],
            }
            for test in data["testCases"]
        ]

    print("Corriendo tests:")
    print("-------------------")

    for i, test in enumerate(test_cases, 1):
        result = calculate_panels(
            test["panel_w"], test["panel_h"], test["roof_w"], test["roof_h"]
        )
        passed = result == test["expected"]

        print(f"Test {i}:")
        print(
            f"  Panels: {test['panel_w']}x{test['panel_h']}, "
            f"Roof: {test['roof_w']}x{test['roof_h']}"
        )
        print(f"  Expected: {test['expected']}, Got: {result}")
        print(f"  Status: {'✅ PASSED' if passed else '❌ FAILED'}\n")


def main() -> None:
    print("🐕 Wuuf wuuf wuuf 🐕")
    print("================================\n")

    run_tests()


if __name__ == "__main__":
    main()
