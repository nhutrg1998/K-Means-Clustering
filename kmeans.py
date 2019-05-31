
import math
import csv
import sys
import random
from prettytable import PrettyTable

k = 1
max_iteration = 500
centroids = []
new_centroids = []
classes = []
cluster = []

def input(input_file):
    file = open(input_file, 'r')
    data = list(csv.reader(file))    
    return data[0], data[1:]

def output(model_file, assignments_file, SSE, attributes, centroids, classes, itemset):

    # Write to model file
    file = open(model_file, 'w')
    file.write('Sum of squared errors: ' + str(SSE) + '\n')
    file.write('Cluster centroids:\n')        
    table = PrettyTable()
    table.add_column('Attribute', attributes)
    for i in range(k):
        table.add_column('Cluster {} ({})'.format(i, len(classes[i])), centroids[i])
    file.write(str(table))
    file.close()

    # Write to assignments file
    file = open(assignments_file, 'w')
    writer = csv.writer(file)
    attributes.append('Cluster')
    writer.writerow(attributes)
    for item in range(len(itemset)):
        itemset[item].append(cluster[item])
        writer.writerow(itemset[item])
    file.close()

def dist(a, b):
    squared_distance = 0

    for i in range(len(a)):
        squared_distance += (a[i]-b[i])**2

    ans = math.sqrt(squared_distance)
    return ans

def average(a):
    ans = []
    for i in range(len(a[0])):
        sum = 0
        for j in a:
            sum += int(j[i])
        ans.append(sum/len(a))
    return ans

if __name__ == '__main__':
    
    k = int(sys.argv[4])
    data = input(sys.argv[1])
    itemset = data[1]

    # Định dạng lại itemset
    for x in range(len(itemset)):
        for y in range(len(itemset[x])):
            itemset[x][y] = int(itemset[x][y])

    # Khởi tạo
    centroids = random.choices(itemset, k=k)
    classes = [[centroids[i]] for i in range(k)]
    cluster = [0 for i in range(len(itemset))]

    # print("Centroids: ")
    # for i in centroids:
    #     print(i)

    # Bắt đầu thuật toán K-Means
    for iteration in range(max_iteration):
        print("Vòng lặp thứ: {} ...".format(iteration))

        print("Tính khoảng cách và gom cụm ...")
        for item in range(len(itemset)):
            distances = [(dist(itemset[item], centroid)) for centroid in centroids]
            classification = distances.index(min(distances))
            classes[classification].append(itemset[item])
            cluster[item] = classification

        # print("Classes: ")
        # for i in classes:
        #     print("Class {}: ".format(classes.index(i)))
        #     for j in i:
        #         print(j)

        print("Tính tâm cụm mới ...")
        new_centroids = [average(classes[i]) for i in range(k)]

        distance = [(dist(centroids[i], new_centroids[i])) for i in range(len(centroids))]
        if (dist(distance, [0 for i in centroids]) < 0.0000000001):
            print("Tâm cụm mới không thay đổi so với tâm cụm cũ, tính SSE và dừng thuật toán ...")
            SSE = 0
            for i in range(k):
                for item in classes[i]:
                    SSE += dist(item, centroids[i])
            print("SSE = {}".format(SSE))
            print("Ghi các kết quả vào file ...")
            output(sys.argv[2], sys.argv[3], SSE, data[0], centroids, classes, itemset)
            break
        else: 
            print("Tâm cụm mới khác tâm cụm cũ, tiếp tục vòng lặp tiếp theo ...")
            centroids = new_centroids
            classes = [[centroids[i]] for i in range(k)]
    
    print("Kết thúc.")
    