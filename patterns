#!/usr/bin/env python
# block_Mens_Classic_Shirt_Aldrich.py
# pattern no. 211 A1
# This is a pattern block to be used to make other patterns.

from tmtpl.constants import *
from tmtpl.pattern   import *
from tmtpl.document   import *
from tmtpl.client   import Client
from tmtpl.curves  import GetCurveControlPoints

from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *
from pysvg.builders import *


def pattern(doc, A, B, C, D, E, F, G, cd):
    # Yoke - A
    # Back - B
    # Front - C
    # Sleeve - D
    # Cuff - E
    # Collar Stand - F
    # Collar - G
    
    #pattern points
    a = rPoint(A, 'a', 0.0, 0.0) # nape
    b = rPoint(B, 'b',a.x ,a.y + (cd.scye_depth + 4*CM)) 
    c = rPoint(B, 'c', a.x, a.y + (cd.natural_waist_length + 3*CM)) 
    d = rPoint(B, 'd', a.x, a.y + (SHIRT_LENGTH + 8*CM)) 
    e = rPoint(C, 'e', a.x + (cd.chest_circumference/2.0 + 12*CM), b.y)
    f = rPoint(C, 'f', e.x, a.y) 
    g = rPoint(C, 'g', e.x, d.y) 
    h = rPoint(A, 'h', a.x + (cd.neck_circumference/5.0 - 0.5*CM), a.y)
    i = rPoint(A, 'i', h.x, h.y - (4.5*CM))
    j = rPoint(A, 'j',a.x, a.y + (linelength(a,b)/5.0 + 2*CM))
    k = rPoint(A, 'k', a.x + (cd.across_B/2.0 + 12*CM), j.y)
    l = rPoint(B, 'l', k.x, b.y)
    m = rPoint(A, 'm', k.x, a.y)
    n = rPoint(A, 'n', m.x + (0.75*CM), m.y)
    o = rPoint(A, 'o', k.x - (10*CM), k.y) 
    p = rPoint(B, 'p', k.x, k.y + (0.75*CM))
    q = rPoint(C, 'q', b.x + (lineLength(b,e)/4.0 + 0.5*CM), b.y)
    r = rPoint(C, 'r', q.x, c.y)
    s = rPoint(C, 's', q.x, d.y)
    t = rPoint(C, 't', f.x, f.y + (4.5*CM))
    u = rPoint(C, 'u', t.x - (cd.Neck_circumference/5.0 - 1*CM), t.y)
    v= rPoint(C, 'v', t.x, t.y + (cd.neck_circumference/5.0 - 2.5*CM))
    w= rPoint(B, 'w', k.x, k.y + (1.5*CM))
    x = rPointP(C, 'x', pntOnCircle(u, (lineLength(i,n) + 0.5*CM),'y',w.y, 'x','<',u.x))
    y = rPoint(C, 'y', e.x - (cd.chest_circumference/3.0 + 4.5*CM), e.y)
    z = rPoint(C, 'z', y.x, y.y - (3*CM))
    
    aa = rPointP(C, 'aa', pntOnLine(z,x,lineLength(z,x)/2.0))
    bb = rPoint(C, 'bb', v.x + (1.5*CM), v.y)
    cc = rPoint(C, 'cc', bb.x + (3.5*CM), v.y)
    dd = rPoint(C, 'dd', r.x + (2*CM), r.y)
    ee = rPoint(B, 'ee', r.x - (2*CM), r.y)
    ff = rPoint(C, 'ff', s.x, s.y - (20*CM)) 
    gg = rPoint(C, 'gg', ff.x + (1*CM), ff.y)
    hh = rPoint(B, 'hh', ff.x - (1*CM), ff.y)
    ii = rPointP(C, 'ii', pntOnLine(g,s,lineLength(g,s)/2.0))
    jj = rPointP(B, 'jj', pntOnLine(d,s,lineLength(d,s)/2.0))
    kk = rPoint(C, 'kk', ii.x, ii.y - (4*CM))
    ll = rPoint(B, 'll', j.x - (2*CM), j.y)
    mm = rPointP(B, 'mm', pntFromDistanceAndAngle(l,3*CM,angleOfDegree(45)))
    nn = rPointP(C, 'nn', pntFromDistanceAndAngle(y,1.75*CM,angleOfDegree(135)))
    oo = rPoint(B, 'oo', ll.x, d.y)
    pp = rPoint(C, 'pp', cc.x, kk.y)
    qq = rPoint(C, 'qq', bb.x, kk.y)
    rr = rPoint(C, 'rr', v.x, kk.y)
    ss = rPointP(B, 'ss', q)
    sa = rPoint(D, 'sa', 0.0, 0.0)
    sb = rPoint(D, 'sb', sa.x, sa.y + (cd.armscye_depth/4.0))
    sc = rPoint(D, 'sc', sa.x, sa.y + (cd.D_length + 6*CM))
    sd = rPoint(D, 'sd', sa.x, sb.y + (lineLength(sb,sc)/2.0))
    se = rPoint(D, 'se', sb.x - (cd.scye_depth/2.0), sb.y)
    sf = rPoint(D, 'sf', se.x, sc.y)
    sg = rPoint(D, 'sg', sb.x + (cd.scye_depth/2.0), sb.y)
    sh = rPoint(D, 'sh', sg.x, sc.y)
    si = rPointP(D, 'si', pntOnLine(se,sa,lineLength(se,sa)/4.0))
    sj = rPointP(D, 'sj', pntFromDistanceAndAngle(pntOnLine(se,sa,lineLength(se,sa)/2.0),1*CM,angleOfDegree(135)))
    sk = rPointP(D, 'sk', pntFromDistanceAndAngle(pntOnLine(se,sa,lineLength(se,sa)*3/4.0),2*CM,angleFromDegree(135)))
    sl = rPointP(D, 'sl', pntFromDistanceAndAngle(pntOnLine(sg,sa,lineLength(sg,sa)/4.0),1*CM,angleFromDegree(225)))
    sm = rPointP(D, 'sm', pntOnLine(sg,sa,lineLength(sg,sa)/2.0))
    sn = rPointP(D, 'sn', pntFromDistanceAndAngle(pntOnLine(sg,sa,lineLength(sg,sa)*3/4.0),1*CM,angleFromDegree(45)))
    so = rPointP(D, 'so', pntOnLine(sf,sc,lineLength(sf,sc)/3.0))
    sp = rPointP(D, 'sp', pntOnLine(sh,sc,lineLength(sh,sc)/3.0))
    sq = rPointP(D, 'sq', midPointP(sf,so))
    sr = rPointP(D, 'sr', midPointP(sh,sp))
    st = rPointP(D, 'st', midPointP(sc,so))
    su = rPoint(D, 'su', st.x, st.y - (15*CM))
    sv = rPoint(D, 'sv', st.x, st.y + (1*CM))
    sw = rPointP(D, 'sw', pntOnLineY(se,sq,sd.y))
    sx = rPointP(D, 'sx', pntOnLineY(sg,sr,sd.y))
    sy = rPointP(D, 'sy', midPointP(sb,sd))
    sz = rPointP(D, 'sz', pntOnLineY(se,sq,sd.y))
    ca = rPoint(E, 'ca', 0.0, 0.0)
    cb = rPoint(E, 'cb', ca.x + (25.5*CM), ca.y)
    cd = rPoint(E, 'cd', ca.x - (3*CM), ca.y)
    ce = rPoint(E, 'ce', cb.x + (3*CM), ca.y)
    cf = rPoint(E, 'cf', ca.x, ca.y + (7.5*CM))
    cg = rPoint(E, 'cg', cb.x, cf.y)
    ch = rPoint(E, 'ch', cd.x, cf.y - (3*CM))
    ci = rPoint(E, 'ci', ce.x, cg.y - (3*CM))
    ka = rPoint(F, 'ka', 0.0, 0.0)
    kb = rPoint(F, 'kb', ka.x + (curveLength(a,i) + curveLength(u,v)), ka.y)
    kc = rPoint(F, 'kc', kb,x + (1.5*CM + 1.25*CM), ka.y)
    kd = rPoint(F, 'kd', ka.x + (lineLength(ka,kb)*3/4.0), ka.y)
    ke = rPoint(G, 'ke', ka.x, ka.y - (8*CM + 2*CM))
    kf = rPointP(F, 'kf', midPointP(ka,ke))
    kg = rPoint(G, 'kg', kb.x, kf.y)
    kh = rPoint(F, 'kh', kc.x, kf.y)
    ki = rPoint(F, 'ki', kh.x - (1*CM), kf.y)
    kj = rPoint(F, 'kj', kc.x, kc.y - (0.75*CM))
    kl = rPoint(F, 'kl', ki.x, ki.y + (0.75*CM))
    km = rPoint(F, 'km', ka.x, ka.y - (0.5*CM))
    kn  = rPointP(F, 'kn', micPointP(kf,kg))
    ko = rPoint(F, 'ko', kg.x, kg.y + (1*CM))
    kp = rPointP(F, 'kp', pntOnLineP(kh,kc,1*CM))
    kq = rPoint(G, 'kq', kg.x + (1*CM), ke.y - (1*CM))
    kr = rPoint(G, 'kr', kn.x, ke.y)
    ks = rPointP(F, 'ks', pntOnCurveX(d,j,b.x))

    # return all variables to the calling program
    return locals()

# vi:set ts=4 sw=4 expandtab:

