
from test import Test

if __name__ == "__main__":
    dna1 = {
        'normal_mean_branch': 2,
        'normal_std_branch': 1.0,
        'normal_mean_orientation': 0,
        'normal_std_orientation': 1.0,
        'max_width': 5.0,
        'max_height': 20.0,
        "height_growth_multiplier": 1.5,
        "weight_growth_multiplier": 2.0,
    }

    time_simulated = 6
    test = Test(dna1)
    test.sow(time_simulated)

