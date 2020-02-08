import cv2
import matplotlib.pyplot as plt
img=cv2.imread("images/img1.png",cv2.IMREAD_COLOR)
# B G R row before column row1 row2 row3...

# print img[:,:,0]
B=img[:, :, 0].ravel()
G=img[:, :, 1].ravel()
R=img[:, :, 2].ravel()
sum_B=0
sum_G=0
sum_R=0
for b1 in B:
    sum_B+=b1
for g1 in G:
    sum_G+=g1
for r1 in R:
    sum_R+=r1
sum_all=sum_B+sum_G+sum_R
sum_B/=float(sum_all)
sum_G/=float(sum_all)
sum_R/=float(sum_all)
RGB_LIST=[sum_B,sum_G,sum_R]
Xtips=['B','G','R']

# plt.figure(figsize=(10,30))
plt.bar(range(3),RGB_LIST,align="center",color=['B','G','R'],label=['B','G','R'])
# plt.hist(range(3),RGB_LIST,align="center",color=['B','G','R'],label=['B','G','R'])
plt.xticks(range(3),Xtips)
for xx, yy in zip(range(3),RGB_LIST):

    plt.text(xx, yy, str(yy), ha='center')
plt.title("RGB picture for img1")
plt.show()



# plt.figure(figsize=(15, 5))
# ax1 = plt.subplot(131)
# # sublot(a,b,c) divide into a*b and it is the cth picture
#
# ax1.hist(img[:, :, 0].ravel(), density=1,bins=50, color='b')
# ax1.set_title("B")
# # use ravel() to decrease the dimension
# # connect each 2-dim vector to a 1-dim vector
# ax2 = plt.subplot(132)
# ax2.hist(img[:, :, 1].ravel(), density=1,bins=50, color='g')
# ax2.set_title("G")
#
# ax3 = plt.subplot(133)
# ax3.hist(img[:, :, 2].ravel(),density=1, bins=50, color='r')
# ax3.set_title("R")
# plt.show()

# cv2.namedWindow("Image")
# cv2.imshow("Image",img)
# cv2.waitKey(0)