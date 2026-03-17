import my_module as md
import pandas as  pd

# folder_path = "copper_sulphate_png"
# diameters, distances_to_bottom = md.find_red_circle_diameters_and_distances(folder_path)
# md.convert_pxl_to_m(diameters, 282)
# md.convert_pxl_to_m(distances_to_bottom,282)
# md.create_csv_file("copper_sulphate.csv", ("diameter", diameters), ("distance from bottom", distances_to_bottom))
df = pd.read_csv('copper_sulphate.csv')
df['distance from bottom'] = df['distance from bottom'] - 0.1
df.to_csv('copper_sulphate.csv')