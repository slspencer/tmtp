def interpolateBezierCurve(P0, P1, P2, P3, t=100):

    '''
    Accepts parameters for one bezier curve as P0, P1, P2, P3 where P0 & P3 are knot points, and P1 & P2 are control points
    Returns curvePoints[] array of interpolated points along curve
    based on work by Gernot Hoffmann - http://www.antigrain.com/research/bezier_interpolation/index.html
    '''

    curvePoints = []
    NUM_STEPS = t - 1

    x0, y0 = P0.x, P0.y
    x1, y1 = P1.x, P1.y
    x2, y2 = P2.x, P2.y
    x3, y3 = P3.x, P3.y

    dx0 = x1 - x0
    dy0 = y1 - y0
    dx1 = x2 - x1
    dy1 = y2 - y1
    dx2 = x3 - x2
    dy2 = y3 - y2

    subdiv_step  = 1.0 / (NUM_STEPS + 1)
    subdiv_step2 = subdiv_step*subdiv_step
    subdiv_step3 = subdiv_step*subdiv_step*subdiv_step

    pre1 = 3.0 * subdiv_step
    pre2 = 3.0 * subdiv_step2
    pre4 = 6.0 * subdiv_step2
    pre5 = 6.0 * subdiv_step3

    tmp1x = x0 - x1 * 2.0 + x2
    tmp1y = y0 - y1 * 2.0 + y2

    tmp2x = (x1 - x2)*3.0 - x0 + x3
    tmp2y = (y1 - y2)*3.0 - y0 + y3

    fx = x0
    fy = y0

    dfx = (x1 - x0)*pre1 + tmp1x*pre2 + tmp2x*subdiv_step3
    dfy = (y1 - y0)*pre1 + tmp1y*pre2 + tmp2y*subdiv_step3

    ddfx = tmp1x*pre4 + tmp2x*pre5
    ddfy = tmp1y*pre4 + tmp2y*pre5

    dddfx = tmp2x*pre5
    dddfy = tmp2y*pre5

    pnt = Pnt(x0, y0)
    curvePoints.append(pnt) # 1st point is 1st knot P0
    print '0', curvePoints[0].x,  curvePoints[0].y
    #step = NUM_STEPS
    i = 1
    while (i <= NUM_STEPS):
        fx   = fx + dfx
        fy   = fy + dfy
        dfx  = dfx + ddfx
        dfy  = dfy + ddfy
        ddfx = ddfx + dddfx
        ddfy = ddfy + dddfy
        pnt = Pnt(fx, fy)
        curvePoints.append(pnt)
        print i, curvePoints[i].x,  curvePoints[i].y
        i = i + 1


    pnt = Pnt(x3, y3)
    curvePoints.append(pnt) # Last point is 2nd knot P3
    print i, curvePoints[i].x,  curvePoints[i].y


    return curvePoints
