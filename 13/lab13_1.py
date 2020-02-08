import cv2
import sys, os, time

def colorHistogram(img, init_row, init_col):
    ROW, COL, CLR = img.shape
    BGR = [0] * 3
    for i in range(init_row, init_row + ROW / 2):
        for j in range(init_col, init_col + COL / 2):
            BGR[0] += img[i][j][0]
            BGR[1] += img[i][j][1]
            BGR[2] += img[i][j][2]
    total = BGR[0] + BGR[1] + BGR[2]
    for c in range(3):
        BGR[c] = float(BGR[c]) / total
    return BGR


def extractFeature(img):
    ROW, COL, CLR = img.shape
    feature = colorHistogram(img, 0, 0) + colorHistogram(img, 0, COL / 2) \
  + colorHistogram(img, ROW / 2,0) + colorHistogram(img,ROW / 2, COL / 2)
    return feature


def hashFeature(raw_feature, mask):
    feature = [0] * 12
    for i in range(12):
        if raw_feature[i] < 0.3:
            feature[i] = 0
        elif raw_feature[i] < 0.6:
            feature[i] = 1
        else:
            feature[i] = 2
    result = []
    for n in mask:
        C = 2
        i = n / C
        result.append(n % C < feature[i])
    val = 0
    for i in range(len(result)):
        val += result[i] * (2 ** i)
    return val



target = cv2.imread(sys.argv[1])
# target=cv2.imread('target.jpg')
dataset = sys.argv[2]
# dataset='Dataset'
mask = sys.argv[3:]
# mask=[4,12,20]

for i in range(len(mask)):
    mask[i] = int(mask[i])

lib1 = {}
lib2 = {}
for root, dirs, files in os.walk(dataset):
    for filename in files:
        img = cv2.imread(os.path.join(root, filename))
        feature = extractFeature(img)
        hash_val = hashFeature(feature, mask)
        lib2[filename] = feature
        d = lib1.get(hash_val, {})
        d[filename] = feature
        lib1[hash_val] = d



t0 = time.clock()
for t in range(50):
    feature = extractFeature(target)
    hash_val = hashFeature(feature, mask)
    d = lib1[hash_val]
    min_d = 4
    name = ''
    for key, value in d.items():
        dis = 0
        for i in range(12):
            dis += (value[i] - feature[i]) ** 2
        dis = dis ** 0.5
        if dis < min_d:
            min_d = dis
            name = key
t1 = time.clock()
print name
print 'LSH:', (t1 - t0)/50

t0 = time.clock()
for t in range(50):
    feature = extractFeature(target)
    min_d = 11
    name = ''
    for key, value in lib2.items():
        dis = 0
        for i in range(12):
            dis += (value[i] - feature[i]) ** 2
        dis = dis ** 0.5
        if dis < min_d:
            min_d = dis
            name = key
t1 = time.clock()
print name
print 'NN:', (t1 - t0)/50