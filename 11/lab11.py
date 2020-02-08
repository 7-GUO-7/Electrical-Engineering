import cv2
import numpy

myimg=cv2.imread("dataset/3.jpg",cv2.IMREAD_GRAYSCALE)
myimg=cv2.GaussianBlur(myimg,(3,3),0) # after Gauss.

img=cv2.imread("dataset/3.jpg",cv2.IMREAD_COLOR)
Canny_img = cv2.Canny(img, 50, 150) #standard Canny.

cv2.namedWindow("Canny")
cv2.imshow("Canny",Canny_img)



num_row=len(myimg)
num_column=len(myimg[0])
angle_list=[]

for k1 in range(0,num_row-1):
    angle_per_row=[]

    for k2 in range(0,num_column-1):
        gradient_row=float(int(myimg[k1][k2+1])-int(myimg[k1][k2])
                           +int(myimg[k1+1][k2+1])-int(myimg[k1+1][k2]))/2
        gradient_column=float(int(myimg[k1][k2])-int(myimg[k1+1][k2])
                              +int(myimg[k1][k2+1])-int(myimg[k1+1][k2+1]))/2

        gradient=int(numpy.sqrt(numpy.square(gradient_row)+numpy.square(gradient_column)))

        myimg[k1][k2] = gradient

        if gradient_row:
            tan_angle=gradient_column/gradient_row
        else:
            tan_angle='0'

        angle_per_row.append(tan_angle)
    angle_list.append(angle_per_row)

# turn to gradient picture


old_img=myimg.copy()
transfer_list=[]

transfer_per_row=[]
for k2 in range(0,num_column-1):
    transfer_per_row.append(0)
transfer_list.append(transfer_per_row)



for k1 in range(1,num_row-1):
    transfer_per_row = []
    transfer_per_row.append(0)
    for k2 in range(1,num_column-1):


        if angle_list[k1][k2]=='0':
            if myimg[k1][k2]>myimg[k1-1][k2] and myimg[k1][k2]>myimg[k1+1][k2]:
                transfer_per_row.append(1)
            else:
                transfer_per_row.append(0)

        else:
            if angle_list[k1][k2]<1 and angle_list[k1][k2]>0:
                tmp1=angle_list[k1][k2]*myimg[k1][k2-1]+\
                     (1-angle_list[k1][k2])*myimg[k1-1][k2-1]
                tmp2=angle_list[k1][k2]*myimg[k1][k2+1]+\
                     (1-angle_list[k1][k2])*myimg[k1+1][k2+1]

                if myimg[k1][k2] >tmp1 and myimg[k1][k2] > tmp2:
                    transfer_per_row.append(1)
                else:
                    transfer_per_row.append(0)

            if angle_list[k1][k2] >= 1:
                tmp_angle_tan=(1/angle_list[k1][k2])
                tmp1 = tmp_angle_tan * myimg[k1-1][k2] + \
                       (1 - tmp_angle_tan) * myimg[k1 - 1][k2 - 1]
                tmp2 = tmp_angle_tan * myimg[k1+1][k2] + \
                       (1 - tmp_angle_tan) * myimg[k1 + 1][k2 + 1]
                if myimg[k1][k2] >tmp1 and myimg[k1][k2] > tmp2:
                    transfer_per_row.append(1)
                else:
                    transfer_per_row.append(0)


            if angle_list[k1][k2] <= -1 :
                tmp_angle_tan = abs(1 / angle_list[k1][k2])
                tmp1 = tmp_angle_tan * myimg[k1 - 1][k2] +\
                       (1 - tmp_angle_tan) * myimg[k1 - 1][k2 + 1]
                tmp2 = tmp_angle_tan * myimg[k1 + 1][k2] + \
                       (1 - tmp_angle_tan) * myimg[k1 + 1][k2 - 1]
                if myimg[k1][k2] > tmp1 and myimg[k1][k2] > tmp2:
                    transfer_per_row.append(1)
                else:
                    transfer_per_row.append(0)


            if angle_list[k1][k2] > -1 and angle_list[k1][k2] <= 0:
                tmp_angle_tan = abs(angle_list[k1][k2])
                tmp1 = tmp_angle_tan * myimg[k1][k2+1] + \
                       (1 - tmp_angle_tan) * myimg[k1 - 1][k2]
                tmp2 = tmp_angle_tan * myimg[k1][k2-1] + \
                       (1 - tmp_angle_tan) * myimg[k1 + 1][k2]
                if myimg[k1][k2] > tmp1 and myimg[k1][k2] > tmp2:
                    transfer_per_row.append(1)
                else:
                    transfer_per_row.append(0)

    transfer_list.append(transfer_per_row)


for k1 in range(0,num_column):

    myimg[num_row-1][k1]=0

for k2 in range(0,num_row):

    myimg[k2][num_column-1]=0

myimg_high=myimg.copy()
myimg_low=myimg.copy()


for k1 in range(0,num_row-1):

    for k2 in range(0,num_column-1):

        if transfer_list[k1][k2] and myimg_high[k1][k2]>10:
            myimg_high[k1][k2]=255
        else:
            myimg_high[k1][k2]=0


for k1 in range(0,num_row-1):

    for k2 in range(0,num_column-1):

        if transfer_list[k1][k2] and myimg_low[k1][k2]>2:
            myimg_low[k1][k2]=255
        else:
            myimg_low[k1][k2]=0



myimg_new=myimg_high.copy()


# found=[]
# to_find=[]

def connect(myimg_new,k1,k2,myimg_low):
# while k1<num_row-1 and k2<num_column-1:
    if k1>=num_row-1 or k2>=num_column-1 or k1<0 or k2<0:
        return

    if myimg_new[k1][k2]:
        if myimg_low[k1+1][k2]:
            myimg_new[k1+1][k2]=255
            # found.append([k1,k2])
            # to_find.append([k1+1,k2])
            # return k1+1,k2
            # connect(myimg_new,k1+1,k2,myimg_low)
        if myimg_low[k1-1][k2]:
            myimg_new[k1-1][k2]=255
            # found.append([k1, k2])
            # to_find.append([k1 - 1, k2])
            # connect(myimg_new, k1 - 1, k2,myimg_low)
            # return k1 -1, k2
        if myimg_low[k1][k2+1]:
            myimg_new[k1][k2+1]=255
            # found.append([k1, k2])
            # to_find.append([k1 , k2+1])
            # connect(myimg_new, k1, k2+1,myimg_low)
            # return k1 , k2+1
        if myimg_low[k1][k2-1]:
            myimg_new[k1][k2-1]=255
            # found.append([k1, k2])
            # to_find.append([k1 , k2-1])
            # connect(myimg_new, k1, k2 - 1, myimg_low)
            # return k1,k2-1
        if myimg_low[k1+1][k2+1]:
            myimg_new[k1+1][k2+1]=255
            # found.append([k1, k2])
            # to_find.append([k1+1, k2 - 1])
            # connect(myimg_new, k1 + 1, k2+1,myimg_low)
            # return k1 + 1, k2+1
        if myimg_low[k1+1][k2-1]:
            myimg_new[k1+1][k2-1]=255
            # found.append([k1, k2])
            # to_find.append([k1+1, k2 - 1])
            # connect(myimg_new, k1+1, k2 - 1, myimg_low)
            # return k1 + 1, k2-1
        if myimg_low[k1-1][k2+1]:
            myimg_new[k1 - 1][k2+1] = 255
            # found.append([k1, k2])
            # to_find.append([k1-1, k2 + 1])
            # connect(myimg_new, k1-1, k2 + 1, myimg_low)
            # return k1 - 1, k2+1
        if myimg_low[k1-1][k2-1]:
            myimg_new[k1-1][k2-1]=255
            # found.append([k1, k2])
            # to_find.append([k1-1, k2 - 1])
            # connect(myimg_new, k1-1, k2 - 1, myimg_low)
            # return k1-1,k2-1




for k1 in range(0,num_row-1):
    for k2 in range(0,num_column-1):
        connect(myimg_new,k1,k2,myimg_low)


        # to_find.append([k1,k2])
        # while len(to_find):
        #     ans1=to_find[0][0]
        #     ans2=to_find[0][1]
        #     connect(myimg_new,ans1,ans2,myimg_low)
        #     to_find.remove(to_find[0])
        # to_find=[]




# for k1 in range(0,num_row):
#     for k2 in range(0,num_column):
#         if myimg_high[k1][k2]!=myimg_new[k1][k2]:
#             print "dif"

# print myimg_new

cv2.namedWindow("MY_high")
cv2.imshow("MY_high",myimg_high)

cv2.namedWindow("MY_low")
cv2.imshow("MY_low",myimg_low)

cv2.namedWindow("MY_old")
cv2.imshow("MY_old",old_img)

cv2.namedWindow("MY_new")
cv2.imshow("MY_new",myimg_new)

# cv2.namedWindow("Image")
# cv2.imshow("Image",img)

cv2.waitKey(0)