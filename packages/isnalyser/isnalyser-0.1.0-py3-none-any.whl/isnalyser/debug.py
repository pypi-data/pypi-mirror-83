from graph import draw_graph, view_graph

# import os
# print(os.listdir('./../'))
#path to the csv file with the transmitters
path_to_file_transmitters = 'isnalyser/example_data/Transmitters-Ali.csv'  
# path_to_file_transmitters = 'isnalyser/example_data/Transmitters_example.csv'  

# import os
# print(os.listdir('Isnalyser_Ali/'))

# import pandas as pd
# df = pd.read_csv('Transmitters-Ali.csv')
# print(df.shape)
#path to the csv file with the transmissions
path_to_file_transmissions = 'isnalyser/example_data/Transmission-Ali.csv'
# path_to_file_transmissions = 'isnalyser/example_data/Transmissions_example.csv'

# time lapse (in years)
timeline_step = 25 # works for large graph
timeline_step = 15 # works for small example

#Attribute a color to one (with a personalised dictionary) or each origin ('auto')
#Example to highlight transmitters coming from 'I'
# color_origin = {'I':'red'}
#Try also: 
#color_origin = 'auto' # --> use up to 20 different colosr
#color_origin = {} # --> all black by default

#format in which the graph should be displayed
graph_format = 'pdf'

# draw_graph(path_to_file_transmitters, path_to_file_transmissions, timeline_step, color_origin)
view_graph(path_to_file_transmitters, path_to_file_transmissions, timeline_step, color_origin="auto", use_example=True	)
