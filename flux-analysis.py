import xml.etree.ElementTree as ET
import pandas as pd

def calculate_flux(file_name):
    data = []
    tree = ET.parse(file_name)
    root = tree.getroot()

    # timesteps
    for child in root:
        # edge
        for subchild in child:
            # lane
            for subsubchild in subchild:
                # vehicle
                for subsubsubchild in subsubchild:
                    new_row = [
                        child.attrib['time'], 
                        subchild.attrib['id'], 
                        subsubchild.attrib['id'], 
                        subsubsubchild.attrib['id'], 
                        subsubsubchild.attrib['pos'], 
                        subsubsubchild.attrib['speed']
                    ]
                    data.append(new_row)

    df = pd.DataFrame(data, columns=['time', 'edge', 'lane', 'vehicle', 'pos', 'speed'])
    df['time'] = df['time'].astype(float).astype(int)
    df['pos'] = df['pos'].astype(float)
    df['speed'] = df['speed'].astype(float)    

    columns = df[df['edge'].str.startswith('saida')]['edge'].unique()
    df_results = pd.DataFrame(columns=columns)

    for saida in columns:
        df_edge = df[df['edge'] == saida]
        df_edge = df_edge.sort_values(by='time')
        vehicles = df_edge['vehicle'].unique()
        num_vehicles = len(vehicles)
        min_time = df_edge['time'].min()
        max_time = df_edge[df_edge['vehicle'] == vehicles[-1]]['time'].min()
        flux = num_vehicles / (max_time - min_time)
        df_results[saida] = [flux]

    print(df_results)
        
calculate_flux('rawDump.xml')