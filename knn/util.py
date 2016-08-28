import math, sys, inspect

def bPointInCircle(fPointX, fPointY, fCircleX, fCircleY, fRadius):
    oPoint = complex(fPointX, fPointY)
    oCircle = complex(fCircleX, fCircleY)
    if abs(oPoint - oCircle) < fRadius:
        return True
    else:
        return False
        
def bPointInRectangle(fPointX, fPointY, fRectTopLeftX, fRectTopLeftY, fRectBottomRightX, fRectBottomRightY):
    if not (fRectTopLeftX <= fPointX <= fRectBottomRightX or fRectTopLeftX >= fPointX >= fRectBottomRightX):
        return False
    if not (fRectTopLeftY <= fPointY <= fRectBottomRightY or fRectTopLeftY >= fPointY >= fRectBottomRightY):
        return False
    return True

def bCircleIntersectRectangle(fRectTopLeftX=0, fRectTopLeftY=10, fRectBottomRightX=20, fRectBottomRightY=0, #矩形左上点和右下点坐标
                              fCircleX=0, fCircleY=0,   #圆心
                              fRadius=10):             #圆半径
                              
    o1 = complex(fRectTopLeftX, fRectTopLeftY)
    o4 = complex(fRectBottomRightX, fRectBottomRightY)
    
    o2 = complex(fRectBottomRightX, fRectTopLeftY)
    o3 = complex(fRectTopLeftX, fRectBottomRightY)
    
    bO1 = bPointInCircle(fCircleX, fCircleY, o1.real, o1.imag, fRadius)
    bO2 = bPointInCircle(fCircleX, fCircleY, o2.real, o2.imag, fRadius)
    bO3 = bPointInCircle(fCircleX, fCircleY, o3.real, o3.imag, fRadius)
    bO4 = bPointInCircle(fCircleX, fCircleY, o4.real, o4.imag, fRadius)
    
    bABCD = bPointInRectangle(fCircleX, fCircleY, o1.real, o1.imag + fRadius, o2.real, o2.imag - fRadius)
    bEFGH = bPointInRectangle(fCircleX, fCircleY, o3.real, o3.imag + fRadius, o4.real, o4.imag - fRadius)
    
    bIJKL = bPointInRectangle(fCircleX, fCircleY, o1.real - fRadius, o1.imag, o3.real + fRadius, o3.imag)
    bMNOP = bPointInRectangle(fCircleX, fCircleY, o2.real - fRadius, o2.imag, o4.real + fRadius, o4.imag)
    
    #print bO1 , bO2 , bO3 , bO4 , bABCD , bEFGH , bIJKL , bMNOP
    return bO1 or bO2 or bO3 or bO4 or bABCD or bEFGH or bIJKL or bMNOP

def log(*args):
	print('[' + str(inspect.stack()[1][2]) + ']', *args)
