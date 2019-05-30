# -*- coding: utf-8 -*-
# =============================================================================
# Read and write output
# =============================================================================
import csv
from prettytable import PrettyTable
from decimal import Decimal

def get_input(input_file):
    data_file = open(input_file, 'r')
    data = list(csv.reader(data_file))    
    return data[0], data[1:]


def write_output(output_file, SSE, attributes, centroids, clusters, data):
    with open(output_file, 'w') as f:
        f.write('Sum of squared errors: ' + str(SSE) + '\n')
        f.write('Cluster centroids:\n')        
        table = PrettyTable()
        table.add_column('Attribute', attributes)
        for index in range(len(centroids)):
            cen = centroids[index]
            clus = clusters[index]            
            convert = lambda cen: [Decimal(val).quantize(Decimal('1.000')) for val in cen]
            table.add_column('Cluster ' + str(index) + '(' + str(len(clus) / len(data) * 100)[0:4] + '%)', convert(cen))
        f.write(str(table))
        
def write_assignment(output_file, attributes, clusters):
    with open(output_file, 'w', newline = '') as f:
        writer = csv.writer(f)
        attributes += ['Cluster']
        writer.writerow(attributes)        
        for index, c in enumerate(clusters):
            for val in c:                
                writer.writerow(list(val.astype(int)) + [index])