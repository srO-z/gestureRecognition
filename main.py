import cv2
import mediapipe as mp
import time
import os 
import psutil

# 创建一个VideoCapture对象，用于捕获视频
cap = cv2.VideoCapture(0)

# 创建一个Hands对象，用于检测手部姿势
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.5)

# 创建一个DrawingSpec对象，用于绘制手部关键点和连接线
mpDraw = mp.solutions.drawing_utils

handLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=3)

handConStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=5)

# 初始化时间
pTime = 0
cTime = 0
flag=0
flag2=0
flag_edge=0
while True:
    # 读取视频帧
    ret, img = cap.read()
    if ret:
        # 将BGR格式的图像转换为RGB格式
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 处理图像，检测手部姿势
        result = hands.process(imgRGB)

        # 获取图像的高度和宽度
        imgHeight = img.shape[0]
        imgWidth = img.shape[1]

        if result.multi_hand_landmarks:
            # 遍历检测到的每个手部姿势
            for handLms in result.multi_hand_landmarks:
                # 绘制手部关键点和连接线
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle)
                for i, lm in enumerate(handLms.landmark):
                    # 获取每个关键点的坐标
                    xPos = int(lm.x * imgWidth)
                    yPos = int(lm.y * imgHeight)
                        
                    # 在关键点处绘制数字
                    cv2.putText(img, str(i), (xPos-25, yPos+5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)
                    
                    # 检测食指向左滑动
                    flag_finger=0
                    if i == 8 and handLms.landmark[4].x < handLms.landmark[5].x and handLms.landmark[5].x < handLms.landmark[6].x and handLms.landmark[6].x < handLms.landmark[7].x and handLms.landmark[7].x < handLms.landmark[8].x and flag==0:
                        print(handLms.landmark[4].x,handLms.landmark[5].x,handLms.landmark[6].x,handLms.landmark[7].x)

                        #打开edge
                        if flag_edge==0:
                            flag_edge=1
                            os.startfile("F:/manySofts/bilibili/哔哩哔哩.exe")
                        #关闭edge
                        elif flag_edge==1:
                            flag_edge=0
                            for proc in psutil.process_iter(['name']):
                                try:
                                    # 查找进程名为msedge.exe的进程
                                    if proc.info['name'] == '哔哩哔哩.exe':
                                        # 关闭进程
                                        proc.kill()
                                except:
                                    pass

                        
                                
                        flag=1
                    elif i == 8 and not(handLms.landmark[4].x < handLms.landmark[5].x and handLms.landmark[5].x < handLms.landmark[6].x and handLms.landmark[6].x < handLms.landmark[7].x):
                        flag=0

                    # 检测大拇指向上移动
                    if i == 4 and handLms.landmark[3].y > handLms.landmark[4].y and handLms.landmark[2].y > handLms.landmark[3].y and handLms.landmark[1].y > handLms.landmark[2].y and flag2==0:
                        print(2)
                        flag2=1
                    elif i == 4 and not(handLms.landmark[3].y > handLms.landmark[4].y and handLms.landmark[2].y > handLms.landmark[3].y and handLms.landmark[1].y > handLms.landmark[2].y):
                        flag2=0

              
        # 计算帧率
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        # 在图像上绘制帧率
        # cv2.putText(img, f"FPS : {int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        # 显示图像
        # cv2.imshow('img', img)

    # 按下q键退出循环
    if cv2.waitKey(1) == ord('q'):
        break


