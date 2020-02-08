import cv2
import numpy
import matplotlib.pyplot as plt
img=cv2.imread("images/img1.png",cv2.IMREAD_GRAYSCALE)
gray=img.ravel()
# use ravel() to decrease the dimension


# plt.hist(gray, bins=100,density=1,color='black')
# # plt.hist(gray, bins=100,normed=1,color='black')
# plt.title("Gray picture of img1")
# plt.show()

# cv2.namedWindow("Image")
# cv2.imshow("Image",img)
# cv2.waitKey(0)

y=len(img)
x=len(img[0])
gradient={}
for t in range (361):
    gradient[t]=0
for k1 in range(1,x-1):
    for k2 in range(1,y-1):
        tmp=int(numpy.sqrt(pow(float(img[k2+1][k1])-float(img[k2-1][k1]),2)
                           +pow(float(img[k2][k1+1])-float(img[k2][k1-1]),2)))
        gradient[tmp]+=1

gradient_list=[]
sum=0
for t in range (361):
    gradient_list.append(gradient[t])
    sum+=gradient[t]
for t in range (361):
    gradient_list[t]/=float(sum)

plt.bar(range(361),gradient_list,align="center",color="black")
plt.title("Gragient of img1")
plt.show()