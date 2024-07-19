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

    raw = pd.DataFrame(data, columns=['time', 'edge', 'lane', 'vehicle', 'pos', 'speed'])
    raw['time'] = raw['time'].astype(float).astype(int)
    raw['pos'] = raw['pos'].astype(float)
    raw['speed'] = raw['speed'].astype(float)    

    columns = raw[raw['edge'].str.startswith('saida')]['edge'].unique()
    df_results = pd.DataFrame(columns=columns)

    for saida in columns:
        df_edge = raw[raw['edge'] == saida]
        df_edge = df_edge.sort_values(by='time')
        vehicles = df_edge['vehicle'].unique()
        num_vehicles = len(vehicles)
        min_time = df_edge['time'].min()
        max_time = df_edge[df_edge['vehicle'] == vehicles[-1]]['time'].min()
        flux = num_vehicles / (max_time - min_time)
        df_results[saida] = [flux]

    return df_results

    
def calculate_fluxes(file_names):
    df = pd.DataFrame()
    for file_name in file_names:
        df = pd.concat([df, calculate_flux(file_name)], axis=0)
    df = df.reset_index(drop=True)

    return df
          
        
if __name__ == '__main__':
    f = [f'results/rawDump_{i}.xml' for i in range(1, 30+1)]
    calculate_fluxes(f)