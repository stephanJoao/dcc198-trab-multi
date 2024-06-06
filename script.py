import xml.etree.ElementTree as ET
import pandas as pd

data = []

tree = ET.parse('resultados-completos.xml')
root = tree.getroot()

# timesteps
for child in root:
	# edge
	for subchild in child:
		# lane
		for subsubchild in subchild:
			# vehicle
			for subsubsubchild in subsubchild:
				new_row = [child.attrib['time'], subchild.attrib['id'], subsubchild.attrib['id'], subsubsubchild.attrib['id'], subsubsubchild.attrib['pos'], subsubsubchild.attrib['speed']]
				data.append(new_row)

df = pd.DataFrame(data, columns=['time', 'edge', 'lane', 'vehicle', 'pos', 'speed'])

print(df.head(10))