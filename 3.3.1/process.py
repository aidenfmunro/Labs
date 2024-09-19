import os
import matplotlib.pyplot as plt
import numpy             as np
import pandas            as pd

def main():

    # focus

    data_focus = pd.read_csv('data/3.3.1_focus.csv')

    print(data_focus)

    magnetic_field_ascending     = data_focus.iloc[1:, 0]
    magnetic_current_ascending   = data_focus.iloc[1:, 1]

    magnetic_field_descending    = data_focus.iloc[1:, 2]
    magnetic_current_descending  = data_focus.iloc[1:, 3]

    num_focuses                  = data_focus.iloc[1:7, 5]

    focus_current_ascending      = data_focus.iloc[1:7, 4]
    focus_current_descending     = data_focus.iloc[1:7, 6]


    print(num_focuses)
    print(focus_current_ascending)
    print(focus_current_descending)

    # magnet

    data_magnet = pd.to_numeric(pd.read_csv('data/3.3.1_magnet.csv'))

    v70_magnetic_current  = data_magnet.iloc[2:, 0]  # 70
    v70_anode_current     = data_magnet.iloc[2:, 1]

    v80_magnetic_current  = data_magnet.iloc[2:, 2]  # 80
    v80_anode_current     = data_magnet.iloc[2:, 3]

    v90_magnetic_current  = data_magnet.iloc[2:, 4]  # 90
    v90_anode_current     = data_magnet.iloc[2:, 5]

    v100_magnetic_current = data_magnet.iloc[2:, 6]  # 100
    v100_anode_current    = data_magnet.iloc[2:, 7]

    v110_magnetic_current = data_magnet.iloc[2:, 8]  # 110
    v110_anode_current    = data_magnet.iloc[2:, 9]

    v120_magnetic_current = data_magnet.iloc[2:, 10] # 120
    v120_anode_current    = data_magnet.iloc[2:, 11]

    print(v120_anode_current.to_numpy() * 100)
    print(v120_anode_current)

    plt.plot(v70_magnetic_current, v70_anode_current)
    plt.grid(visible = True, which='major', axis='both', alpha=1)
    plt.show()


if __name__ == "__main__":
    main()


