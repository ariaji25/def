# import CV2 libray to load the image data
import cv2
import matplotlib.pyplot as plt
import numpy as np

class DirectionalElementFeature:
  
  class DirectionalOrientation:
    LEFT_DIRECTION = 5
    RIGTH_DIRECTION = 3
    HORIXONTAL_DIRECTION = 4
    VERTICAL_DIRECTION = 2

    def __init__(self):
      pass
    
    def count(self, zone, direction : int):
        return np.count_nonzero(zone == direction)
    
    def countDirection(self, wZone, zone, direction):
      # result = np.array()
      x = 0
      for i in range(len(zone)):
        x_temp = np.count_nonzero(zone[i]==direction)
        x_temp = wZone[i] * x_temp
        x = x+x_temp
      return x

  directional_orientation = DirectionalOrientation()
  
  def __init__(self):
    pass
  def getFeatureFrom(self, path):
    image = self.loadImage(path)
    # plt.imshow(image, 'gray')
    # plt.show()
    binary_data = self.covertToBinaryPixel(image)
    countour_data = self.countourExtraction(binary_data)
    dot_orientation = self.dotOrientation(countour_data)
    subareas = self.makeSubArea(dot_orientation)
    return self.vectorConstraction(subareas)
    
  def loadImage(self, path):
    # load the image data using cv2 with called the 'imread' function
    print(path)
    image =  cv2.imread(path)
    # resize the image to be 64x64 pixel size
    image = cv2.resize(image, (64,64), interpolation = cv2.INTER_AREA)
    # tresholding binary
    ret,tresh = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
    # show to loaded image
    return tresh
  
  def covertToBinaryPixel(self, image):
    # take the gray part of the image
    # and inverse the value of matriks when it 0 to 1, and 1 to 0
    binary_data = image[:,:,0]
    # print(len(binary_data[0]))
    h,w = binary_data.shape
    for line in range(h):
      for row in range(w):
        if binary_data[line,row]==0 :
          binary_data[line,row] = 1
        else:
          binary_data[line,row]=0
    return binary_data
    # plt.imshow(binary_data, 'gray')
    # plt.show()
  
  def countourExtraction(self, binary_data):
    # doing simple edge detection
    edge_detecct = binary_data
    h,w = edge_detecct.shape
    edge_detecct_result = np.zeros((h,w))
    edge_detecct_result[:,:]=1
    for i in range(h):
      for j in range(w):
        if j+1 < w and j-1 >=0 and i+1 < h and i-1 >=0:
          # print(edge_detecct[i,j-1])
          if edge_detecct[i,j] == 0:
            if edge_detecct[i,j+1]==1 or edge_detecct[i,j-1]==1 or edge_detecct[i+1,j]==1 or edge_detecct[i-1,j]==1:
              # print(edge_detecct[i,j])
              edge_detecct_result[i,j]=0
            else:
              edge_detecct_result[i,j]=1
          # # elif edge_detecct[i,j+1]==0 and edge_detecct[i,j+1]==0:
        else:
          None
    return edge_detecct_result
  
  def dotOrientation(self, edge_detecct_result):
    edge_detecct_result_with_padding = np.pad(edge_detecct_result, 0)

    dot_orientation = np.zeros((64,64))
    w,h = edge_detecct_result_with_padding.shape
    dot_orientation.shape
    for i in range(w):
      for j in range(h):
        if edge_detecct_result_with_padding[i,j] == 0:
          if edge_detecct_result_with_padding[i-1,j-1] == 0:
            dot_orientation[i,j] = 5
          elif edge_detecct_result_with_padding[i-1,j] == 0:
            dot_orientation[i,j] = 2
          elif edge_detecct_result_with_padding[i-1,j+1] == 0:
            dot_orientation[i,j] = 3  
          elif edge_detecct_result_with_padding[i,j+1] == 0:
            dot_orientation[i,j] = 4
          elif edge_detecct_result_with_padding[i+1,j+1] == 0:
            dot_orientation[i,j] = 5
          elif edge_detecct_result_with_padding[i+1,j] == 0:
            dot_orientation[i,j] = 2
          elif edge_detecct_result_with_padding[i+1,j-1] == 0:
            dot_orientation[i,j] = 3  
          elif edge_detecct_result_with_padding[i+1,j-1] == 0:
            dot_orientation[i,j] = 4
    return dot_orientation

  def makeSubArea(self, dot_orientation):
    x = 0
    subarea = []
    for i in range(7):
      tmp = dot_orientation[x:x+16]
      index = 0
      for i in range(7):
        subarea.append(tmp[0:16 , index:index+16])
        index=index+8
      x=x+8
    return subarea
    # for i in range(49):
    #     plt.subplot(7,7,i+1), plt.imshow(subarea[i], 'gray')
    #     # plt.title(subname[i])
    #     plt.xticks([]),plt.yticks([])
    # plt.show

  def getTheZoneForSubarea(self, subarea):
    A_zone = subarea[6:10, 6:10]
    # print(A_zone.shape)
    B_zone = subarea[4:12, 4:12]
    # print(B_zone.shape)
    C_zone = subarea[2:14,2:14]
    # print(C_zone.shape)
    D_zone = subarea[0:16,0:16]
    # print(D_zone.shape)
    allzone = [A_zone, B_zone, C_zone, D_zone]
    zone_names = ["A_zone", "B_zone", "C_zone", "D_zone"]
    # for i in range(4):
    #     plt.subplot(1,4,i+1), plt.imshow(allzone[i], 'gray')
    #     plt.title(zone_names[i])
    #     plt.xticks([]),plt.yticks([])
    # plt.show
    return [A_zone, B_zone, C_zone, D_zone]
  
  def vectorConstraction(self, subareas):
    # vectour constraction
    w = [4, 3, 2, 1]
    result = []
    for area in subareas:
      zones = self.getTheZoneForSubarea(area)
      x1 = self.directional_orientation.countDirection(w, zones, self.directional_orientation.LEFT_DIRECTION)  
      x2 = self.directional_orientation.countDirection(w, zones, self.directional_orientation.RIGTH_DIRECTION) 
      x3 = self.directional_orientation.countDirection(w, zones, self.directional_orientation.HORIXONTAL_DIRECTION)
      x4 = self.directional_orientation.countDirection(w, zones, self.directional_orientation.VERTICAL_DIRECTION)
      result.append(x1)
      result.append(x2)
      result.append(x3)
      result.append(x4)

    # len(result)
    return result