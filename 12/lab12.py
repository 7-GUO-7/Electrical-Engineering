import cv2
import numpy
import math

myimg=cv2.imread("target.jpg",cv2.IMREAD_GRAYSCALE)
# myimg=cv2.resize(myimg,(308,288))
corner=cv2.goodFeaturesToTrack(myimg,150,0.01,10,blockSize=3,k=0.04 )

num_row=len(myimg)
num_column=len(myimg[0])

gradient_img=myimg.copy()
# gradient_img=gradient_img.astype(float)
angle_img=myimg.copy()
# angle_img=angle_img.astype(float)


for t1 in range(num_row):
    for t2 in range(num_column):
        gradient_img[t1][t2] = float(0)
        angle_img[t1][t2] = float(0)

for k1 in range(1,num_row-1):

    for k2 in range(1,num_column-1):
        gradient_data = numpy.sqrt(pow(float(int(myimg[k1 + 1][k2]) - int(myimg[k1 - 1][k2])), 2)
           + pow(float( int(myimg[k1][k2 + 1]) - int(myimg[k1][k2 - 1])), 2))

        if (int(myimg[k1][k2 + 1]) - int(myimg[k1][k2 - 1])) == 0:
            if int(myimg[k1 + 1][k2]) - int(myimg[k1 - 1][k2]) > 0:
                angle_data = 90.0
            else:
                angle_data = 270.0

        else:
            if (int(myimg[k1 + 1][k2]) - int(myimg[k1 - 1][k2]) >= 0) \
                    and (int(myimg[k1][k2 + 1]) - int(myimg[k1][k2 - 1]) > 0):
                angle_data = math.atan(float((int(myimg[k1 + 1][k2]) - int(myimg[k1 - 1][k2])))
                                       / (int(myimg[k1][k2 + 1]) - int(myimg[k1][k2 - 1]))) \
                             / math.pi * 180

            if (int(myimg[k1 + 1][k2]) - int(myimg[k1 - 1][k2]) >= 0) \
                    and (int(myimg[k1][k2 + 1]) - int(myimg[k1][k2 - 1]) < 0):
                angle_data = 180 - abs(math.atan(float((int(myimg[k1 + 1][k2]) - int(myimg[k1 - 1][k2])))
                                           / (int(myimg[k1][k2 + 1]) - int(myimg[k1][k2 - 1])))
                                 / math.pi * 180)

            if (int(myimg[k1 + 1][k2]) - int(myimg[k1 - 1][k2]) <= 0) \
                    and (int(myimg[k1][k2 + 1]) - int(myimg[k1][k2 - 1]) < 0):
                angle_data = abs(math.atan(float((int(myimg[k1 + 1][k2]) - int(myimg[k1 - 1][k2])))
                                           / (int(myimg[k1][k2 + 1]) - int(myimg[k1][k2 - 1])))
                                 / math.pi * 180) + 180

            if (int(myimg[k1 + 1][k2]) - int(myimg[k1 - 1][k2]) <= 0) \
                    and (int(myimg[k1][k2 + 1]) - int(myimg[k1][k2 - 1]) > 0):
                angle_data = 360 - abs(math.atan(float((int(myimg[k1 + 1][k2]) - int(myimg[k1 - 1][k2])))
                                           / (int(myimg[k1][k2 + 1]) - int(myimg[k1][k2 - 1]))) / math.pi * 180)

        gradient_img[k1][k2] = gradient_data

        angle_img[k1][k2] = angle_data





vector_final=[]
length=len(corner)
for i in range (length):

    y = corner[i][0][0]
    x = corner[i][0][1]

    main_direction_vote=[]
    for o in range(36):
        main_direction_vote.append(0)

    gradient=[]
    angle=[]


    x=int(x)
    y=int(y)


    for k1 in range(x-3,x+3):
        for k2 in range(y-3,y+3):

            gradient_data=gradient_img[k1][k2]
            angle_data=angle_img[k1][k2]


            gradient.append(gradient_data)
            angle.append(angle_data)

            choice = int(angle_data / 10)
            if choice==36:
                choice=0
            main_direction_vote[choice] += gradient_data

    max=main_direction_vote[0]
    direction=0
    for o in range(36):
        if main_direction_vote[o]>max:
            direction=o
            max=main_direction_vote[o]
    direction *= 10
    direction+=5


    new_gradient = []
    new_angle = []
    for k2 in range(- 8, 8):
        new_gradient_per_row=[]
        new_angle_per_row=[]
        for k1 in range(- 8, 8):
            y_new = k1 * math.cos(-direction / 180 * math.pi) + \
                    k2 * math.sin(-direction / 180 * math.pi)
            x_new = k2 * math.cos(-direction / 180 * math.pi) - \
                    k1 * math.sin(-direction / 180 * math.pi)
            x_new=x_new+x
            y_new=y_new+y

            x_up = int(x_new)
            x_down = x_up + 1
            y_left = int(y_new)
            y_right = y_left + 1

            try:
                new_gradient_data=gradient_img[x_up][y_left]*(x_down-x_new)*(y_right-y_new)\
                              +gradient_img[x_down][y_left]*(x_new-x_up)*(y_right-y_new)\
                              +gradient_img[x_up][y_right]*(x_down-x_new)*(y_new-y_left)\
                              +gradient_img[x_down][y_right]*(x_new-x_up)*(y_new-y_left)
                new_angle_data=((angle_img[x_up][y_left]-direction+360)%360)*(x_down-x_new)*(y_right-y_new)\
                              +((angle_img[x_down][y_left]-direction+360)%360)*(x_new-x_up)*(y_right-y_new)\
                              +((angle_img[x_up][y_right]-direction+360)%360)*(x_down-x_new)*(y_new-y_left)\
                              +((angle_img[x_down][y_right]-direction+360)%360)*(x_new-x_up)*(y_new-y_left)


            except:
                new_gradient_data=0
                new_angle_data=0

            new_gradient_per_row.append(new_gradient_data)
            new_angle_per_row.append(new_angle_data)



        new_gradient.append(new_gradient_per_row)
        new_angle.append(new_angle_per_row)

    vote_per_point=[]

    final_vote=[]
    for o in range(8):
        final_vote.append(0)

    for k1 in range(0,4):
        for k2 in range(0,4):
            final_vote[int(new_angle[k1][k2])/45] += 1
    vote_per_point.extend(final_vote)


    for o in range(8):
        final_vote[o]=0

    for k1 in range(4,8):
        for k2 in range(0,4):
            final_vote[int(new_angle[k1][k2])/45]+=1
    vote_per_point.extend(final_vote)


    for o in range(8):
        final_vote[o]=0
    for k1 in range(8,12):
        for k2 in range(0,4):
            final_vote[int(new_angle[k1][k2])/45]+=1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o]=0
    for k1 in range(12,16):
        for k2 in range(0,4):
            final_vote[int(new_angle[k1][k2])/45]+=1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o]=0
    for k1 in range(0,4):
        for k2 in range(4,8):
            final_vote[int(new_angle[k1][k2])/45]+=1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o]=0

    for k1 in range(4,8):
        for k2 in range(4,8):
            final_vote[int(new_angle[k1][k2])/45]+=1
    vote_per_point.extend(final_vote)


    for o in range(8):
        final_vote[o]=0
    for k1 in range(8,12):
        for k2 in range(4,8):
            final_vote[int(new_angle[k1][k2])/45]+=1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o]=0
    for k1 in range(12,16):
        for k2 in range(4,8):
            final_vote[int(new_angle[k1][k2])/45]+=1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o] = 0
    for k1 in range(0, 4):
        for k2 in range(8, 12):
            final_vote[int(new_angle[k1][k2]) / 45] += 1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o] = 0

    for k1 in range(4, 8):
        for k2 in range(8, 12):
            final_vote[int(new_angle[k1][k2]) / 45] += 1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o] = 0
    for k1 in range(8, 12):
        for k2 in range(8, 12):
            final_vote[int(new_angle[k1][k2]) / 45] += 1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o] = 0
    for k1 in range(12, 16):
        for k2 in range(8, 12):
            final_vote[int(new_angle[k1][k2]) / 45] +=1
    vote_per_point.extend(final_vote)


    for o in range(8):
        final_vote[o] = 0
    for k1 in range(0, 4):
        for k2 in range(12, 16):
            final_vote[int(new_angle[k1][k2]) / 45] += 1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o] = 0

    for k1 in range(4, 8):
        for k2 in range(12, 16):
            final_vote[int(new_angle[k1][k2]) / 45] += 1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o] = 0
    for k1 in range(8, 12):
        for k2 in range(12, 16):
            final_vote[int(new_angle[k1][k2]) / 45] += 1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o] = 0
    for k1 in range(12, 16):
        for k2 in range(12, 16):
            final_vote[int(new_angle[k1][k2]) / 45] += 1
    vote_per_point.extend(final_vote)

    len_per_point=len(vote_per_point)
    sum=0
    for p in range(len_per_point):
        sum+=(vote_per_point[p])**2
    sum=math.sqrt(float(sum))+0.000001
    for p in range(len_per_point):
        vote_per_point[p]=float(vote_per_point[p])/sum

    vector_final.append(vote_per_point)

print vector_final




############################################


myimg_search=cv2.imread("dataset/3.jpg",cv2.IMREAD_GRAYSCALE)

corner_search=cv2.goodFeaturesToTrack(myimg_search,150,0.01,10,blockSize=3,k=0.04 )
# cv2.namedWindow("myimg_search")
# cv2.imshow("myimg_search",myimg_search)

num_row_search=len(myimg_search)
num_column_search=len(myimg_search[0])

gradient_img_search=myimg_search.copy()
# gradient_img_search=gradient_img_search.astype(float)
angle_img_search=myimg_search.copy()
# angle_img_search=angle_img_search.astype(float)


for t1 in range(num_row_search):
    for t2 in range(num_column_search):
        gradient_img_search[t1][t2] = float(0)
        angle_img_search[t1][t2] = float(0)

for k1 in range(1,num_row_search-1):

    for k2 in range(1,num_column_search-1):
        gradient_data_search = numpy.sqrt(pow(float(int(myimg_search[k1 + 1][k2]) - int(myimg_search[k1 - 1][k2])), 2) + pow(float(
            int(myimg_search[k1][k2 + 1]) - int(myimg_search[k1][k2 - 1])), 2))

        if (int(myimg_search[k1][k2 + 1]) - int(myimg_search[k1][k2 - 1])) == 0:
            if int(myimg_search[k1 + 1][k2]) - int(myimg_search[k1 - 1][k2]) > 0:
                angle_data_search = 90.0
            else:
                angle_data_search = 270.0

        else:
            if (int(myimg_search[k1 + 1][k2]) - int(myimg_search[k1 - 1][k2]) >= 0) \
                    and (int(myimg_search[k1][k2 + 1]) - int(myimg_search[k1][k2 - 1]) > 0):
                angle_data_search = math.atan(float((int(myimg_search[k1 + 1][k2]) - int(myimg_search[k1 - 1][k2])))
                                       / (int(myimg_search[k1][k2 + 1]) - int(myimg_search[k1][k2 - 1]))) \
                             / math.pi * 180

            if (int(myimg_search[k1 + 1][k2]) - int(myimg_search[k1 - 1][k2]) >= 0) \
                    and (int(myimg_search[k1][k2 + 1]) - int(myimg_search[k1][k2 - 1]) < 0):
                angle_data_search =180 - abs(math.atan(float((int(myimg_search[k1 + 1][k2]) - int(myimg_search[k1 - 1][k2])))
                                           / (int(myimg_search[k1][k2 + 1]) - int(myimg_search[k1][k2 - 1])))
                                 / math.pi * 180)

            if (int(myimg_search[k1 + 1][k2]) - int(myimg_search[k1 - 1][k2]) <= 0) \
                    and (int(myimg_search[k1][k2 + 1]) - int(myimg_search[k1][k2 - 1]) < 0):
                angle_data_search = abs(math.atan(float((int(myimg_search[k1 + 1][k2]) - int(myimg_search[k1 - 1][k2])))
                                           / (int(myimg_search[k1][k2 + 1]) - int(myimg_search[k1][k2 - 1])))
                                 / math.pi * 180) + 180

            if (int(myimg_search[k1 + 1][k2]) - int(myimg_search[k1 - 1][k2]) <= 0) \
                    and (int(myimg_search[k1][k2 + 1]) - int(myimg_search[k1][k2 - 1]) > 0):
                angle_data_search = 360 - abs(math.atan(float((int(myimg_search[k1 + 1][k2]) - int(myimg_search[k1 - 1][k2])))
                                           / (int(myimg_search[k1][k2 + 1]) - int(myimg_search[k1][k2 - 1]))) / math.pi * 180)

        gradient_img_search[k1][k2] = gradient_data_search

        angle_img_search[k1][k2] = angle_data_search





vector_final_search=[]
length=len(corner_search)
for i in range (length):

    y = corner_search[i][0][0]
    x = corner_search[i][0][1]

    main_direction_vote=[]
    for o in range(36):
        main_direction_vote.append(0)

    gradient=[]
    angle=[]


    x=int(x)
    y=int(y)


    for k1 in range(x-3,x+3):
        for k2 in range(y-3,y+3):
            gradient_data_search=gradient_img_search[k1][k2]
            angle_data_search=angle_img_search[k1][k2]


            gradient.append(gradient_data_search)
            angle.append(angle_data_search)

            choice = int(angle_data_search / 10)
            if choice==36:
                choice=0
            main_direction_vote[choice] += gradient_data_search

    max=main_direction_vote[0]
    direction=0
    for o in range(36):
        if main_direction_vote[o]>max:
            direction=o
            max=main_direction_vote[o]
    direction *= 10
    direction+=5


    new_gradient = []
    new_angle = []
    for k2 in range(- 8, 8):
        new_gradient_per_row=[]
        new_angle_per_row=[]
        for k1 in range(- 8, 8):
            y_new = k1 * math.cos(-direction / 180 * math.pi) + k2 * math.sin(-direction / 180 * math.pi)
            x_new = k2 * math.cos(-direction / 180 * math.pi) - k1 * math.sin(-direction / 180 * math.pi)
            x_new=x_new+x
            y_new=y_new+y

            x_up = int(x_new)
            x_down = x_up + 1
            y_left = int(y_new)
            y_right = y_left + 1
            try:
                new_gradient_data_search=gradient_img_search[x_up][y_left]*(x_down-x_new)*(y_right-y_new)\
                              +gradient_img_search[x_down][y_left]*(x_new-x_up)*(y_right-y_new)\
                              +gradient_img_search[x_up][y_right]*(x_down-x_new)*(y_new-y_left)\
                              +gradient_img_search[x_down][y_right]*(x_new-x_up)*(y_new-y_left)
                new_angle_data_search=((angle_img_search[x_up][y_left]-direction+360)%360)*(x_down-x_new)*(y_right-y_new)\
                              +((angle_img_search[x_down][y_left]-direction+360)%360)*(x_new-x_up)*(y_right-y_new)\
                              +((angle_img_search[x_up][y_right]-direction+360)%360)*(x_down-x_new)*(y_new-y_left)\
                              +((angle_img_search[x_down][y_right]-direction+360)%360)*(x_new-x_up)*(y_new-y_left)
            except:
                new_gradient_data_search=0
                new_angle_data_search=0



            new_gradient_per_row.append(new_gradient_data_search)
            new_angle_per_row.append(new_angle_data_search)



        new_gradient.append(new_gradient_per_row)
        new_angle.append(new_angle_per_row)

    vote_per_point=[]

    final_vote=[]
    for o in range(8):
        final_vote.append(0)

    for k1 in range(0,4):
        for k2 in range(0,4):
            final_vote[int(new_angle[k1][k2])/45] += 1
    vote_per_point.extend(final_vote)


    for o in range(8):
        final_vote[o]=0

    for k1 in range(4,8):
        for k2 in range(0,4):
            final_vote[int(new_angle[k1][k2])/45]+=1
    vote_per_point.extend(final_vote)


    for o in range(8):
        final_vote[o]=0
    for k1 in range(8,12):
        for k2 in range(0,4):
            final_vote[int(new_angle[k1][k2])/45]+=1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o]=0
    for k1 in range(12,16):
        for k2 in range(0,4):
            final_vote[int(new_angle[k1][k2])/45]+=1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o]=0
    for k1 in range(0,4):
        for k2 in range(4,8):
            final_vote[int(new_angle[k1][k2])/45]+=1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o]=0

    for k1 in range(4,8):
        for k2 in range(4,8):
            final_vote[int(new_angle[k1][k2])/45]+=1
    vote_per_point.extend(final_vote)


    for o in range(8):
        final_vote[o]=0
    for k1 in range(8,12):
        for k2 in range(4,8):
            final_vote[int(new_angle[k1][k2])/45]+=1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o]=0
    for k1 in range(12,16):
        for k2 in range(4,8):
            final_vote[int(new_angle[k1][k2])/45]+=1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o] = 0
    for k1 in range(0, 4):
        for k2 in range(8, 12):
            final_vote[int(new_angle[k1][k2]) / 45] += 1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o] = 0

    for k1 in range(4, 8):
        for k2 in range(8, 12):
            final_vote[int(new_angle[k1][k2]) / 45] += 1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o] = 0
    for k1 in range(8, 12):
        for k2 in range(8, 12):
            final_vote[int(new_angle[k1][k2]) / 45] += 1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o] = 0
    for k1 in range(12, 16):
        for k2 in range(8, 12):
            final_vote[int(new_angle[k1][k2]) / 45] += 1
    vote_per_point.extend(final_vote)


    for o in range(8):
        final_vote[o] = 0
    for k1 in range(0, 4):
        for k2 in range(12, 16):
            final_vote[int(new_angle[k1][k2]) / 45] += 1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o] = 0

    for k1 in range(4, 8):
        for k2 in range(12, 16):
            final_vote[int(new_angle[k1][k2]) / 45] +=1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o] = 0
    for k1 in range(8, 12):
        for k2 in range(12, 16):
            final_vote[int(new_angle[k1][k2]) / 45] += 1
    vote_per_point.extend(final_vote)

    for o in range(8):
        final_vote[o] = 0
    for k1 in range(12, 16):
        for k2 in range(12, 16):
            final_vote[int(new_angle[k1][k2]) / 45] += 1#new_gradient[k1][k2]
    vote_per_point.extend(final_vote)

    len_per_point=len(vote_per_point)
    sum=0
    for p in range(len_per_point):
        sum+=(vote_per_point[p])**2
    sum=math.sqrt(float(sum))+0.000001
    # tmp = numpy.array(vote_per_point)
    # norm = numpy.linalg.norm(tmp)
    # print norm
    for p in range(len_per_point):
        vote_per_point[p]=float(vote_per_point[p])/sum


    vector_final_search.append(vote_per_point)

print vector_final_search

pair_point=[]
pair_count=0
for i1 in range(len(vector_final)):
    for i2 in range(len(vector_final_search)):
        pair=numpy.vdot(vector_final[i1],vector_final_search[i2])
        if pair>=0.76:
            print pair
            pair_point.append(i1)
            pair_point.append(i2)
            pair_count+=1



row1=num_row
column1=num_column
row2=num_row_search
column2=num_column_search
# row1,column1= myimg.shape
# row2,column2= myimg_search.shape
answer_row=numpy.maximum(row1,row2)
result=numpy.zeros(shape=(answer_row,column1+column2,3),dtype=numpy.uint8)
for i1 in range (row1):
    for i2 in range(column1):
        result[i1][i2]=myimg[i1][i2]

for i1 in range(row2):
    for i2 in range(column2):
        result[i1][i2+column1]=myimg_search[i1][i2]

for t in range(pair_count):
    cv2.line(result,(int(corner[pair_point[2*t]][0][0]),int(corner[pair_point[2*t]][0][1])),
    (int(corner_search[pair_point[2*t+1]][0][0])+column1,int(corner_search[pair_point[2*t+1]][0][1]))
     ,(0,0,255),1)

myimg_print = numpy.zeros(shape=(row1, column1, 3), dtype=numpy.uint8)
for i1 in range (row1):
    for i2 in range(column1):
        myimg_print[i1][i2]=myimg[i1][i2]
for t in range(pair_count):

    cv2.circle(myimg_print,(corner[pair_point[2*t]][0][0],corner[pair_point[2*t]][0][1]),
               10,(0,0,255),2)
cv2.imshow('myimg',myimg_print)

myimg_search_print = numpy.zeros(shape=(row2, column2, 3), dtype=numpy.uint8)
for i1 in range (row2):
    for i2 in range(column2):
        myimg_search_print[i1][i2]=myimg_search[i1][i2]
for t in range(pair_count):
    cv2.circle(myimg_search_print,(corner_search[pair_point[2*t+1]][0][0],
                                   corner_search[pair_point[2*t+1]][0][1]),10,(0,0,255),2)

cv2.imshow('result',result)

cv2.imshow('myimg_search',myimg_search_print)
# cv2.imwrite('result',result)



cv2.waitKey(0)