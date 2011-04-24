#!/usr/bin/env python
#

import re

def parseTransform(transform):
    # translate (x,y)
    # scale (sx, sy)
    # skewX(angle)
    # skewY(angle)
    # rotate (angle, cx, cy)
    # matrix(a, b, c, d, e, f)

    print 'Input = <%s>' % transform

    # Every transform in the list ends with parens
    
    transforms = re.split(r'\)', transform)

    gotatranslate = False
    output = ''

    for tr in transforms:
        # I don't know why we get an empty string at the end
        if tr == '':
            continue
        tr = tr.strip()

        trparts = re.split(r',|\(', tr)
        trans = trparts[0].strip()
        if trans == 'translate':
            tx = trparts[1].strip()
            ty = trparts[2].strip()
            if not gotatranslate:
                print 'First translate'
                # make the adjustment
            result = '%s(%s,%s) ' % (trans, tx, ty)
        elif trans == 'scale':
            tx = trparts[1].strip()
            ty = trparts[2].strip()
            result = '%s(%s,%s) ' % (trans, tx, ty)
        elif trans == 'skewX':
            tx = trparts[1].strip()
            result = '%s(%s) ' % (trans, tx)
        elif trans == 'skewY':
            tx = trparts[1].strip()
            result = '%s(%s) ' % (trans, tx)
        elif trans == 'rotate':
            an = trparts[1].strip()
            tx = trparts[2].strip()
            ty = trparts[3].strip()
            result = '%s(%s,%s,%s) ' % (trans, an, tx, ty)
        elif trans == 'matrix':
            ma = trparts[1].strip()
            mb = trparts[2].strip()
            mc = trparts[3].strip()
            md = trparts[3].strip()
            me = trparts[3].strip()
            mf = trparts[3].strip()
            result = '%s(%s,%s,%s,%s,%s,%s) ' % (trans, ma, mb, mc, md, me, mf)
        else:
            print 'Unexpected transformation %s' % trans

        print result
        output = output + result

    print output
    return



tr = 'translate (3,4) translate( 344.567, 34.9) rotate(20, 30, 40)'

parseTransform(tr)

