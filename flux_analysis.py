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
    columns = columns.tolist()
    columns.append('type')

    df_results = pd.DataFrame(columns=columns)

    for saida in columns[:-1]:
        df_edge = raw[raw['edge'] == saida]
        df_edge = df_edge.sort_values(by='time')
        vehicles = df_edge['vehicle'].unique()
        cars = [v for v in vehicles if v.startswith('C')]
        buses = [v for v in vehicles if v.startswith('O')]
        num_cars = len(cars)
        num_buses = len(buses)        
        min_time = df_edge['time'].min()
        max_time_cars = df_edge[df_edge['vehicle'] == cars[-1]]['time'].min()        
        max_time_buses = df_edge[df_edge['vehicle'] == buses[-1]]['time'].min()
        cars_flux = num_cars / (max_time_cars - min_time)
        buses_flux = num_buses / (max_time_buses - min_time)        
        df_results[saida] = [cars_flux, buses_flux]
        df_results['type'] = ['car', 'bus']
    
    return df_results
    
def calculate_fluxes(file_names):
    df = pd.DataFrame()
    for file_name in file_names:
        df = pd.concat([df, calculate_flux(file_name)], axis=0)
    df = df.reset_index(drop=True)
    df = df.groupby('type', as_index=False).mean()
    return df
                  
if __name__ == '__main__':
    result = calculate_flux('rawDump.xml')
   
    # f = [f'results1/rawDump_{i}.xml' for i in range(1, 3+1)]
    # results = calculate_fluxes(f)
    # print(results)