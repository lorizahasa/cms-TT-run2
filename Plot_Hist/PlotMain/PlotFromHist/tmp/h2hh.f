      double precision function h2hh_hdec(imssm)
      implicit double precision (a-h,o-z)
      complex*16 c03_hdec,cc0
      double precision lamb_hdec,mij,mij0
      double precision mst12,mst22,mt,lt,lst1,lst2
      dimension xglbb(2,2),xghbb(2,2),xgctb(2,2)
      common/param_hdec/gf,alph,amtau,ammuon,amz,amw
      common/hmass_hdec/amsm,ama,amhl,amhh,amch,amar
      common/gluino_hdec/amg,amsb1,amsb2,sth,cth,
     .              glbb(2,2),ghbb(2,2),gabb(2,2),
     .              amst1,amst2,stht,ctht,
     .              gltt(2,2),ghtt(2,2),gatt(2,2)
c     common/sqnlo_hdec/amsb(2),sthb,cthb,glbb(2,2),ghbb(2,2),gabb,
c    .                  amst(2),stht,ctht,gltt(2,2),ghtt(2,2),gatt
      common/coup_hdec/gat,gab,glt,glb,ght,ghb,gzah,gzal,
     .            ghhh,glll,ghll,glhh,ghaa,glaa,glvv,ghvv,
     .            glpm,ghpm,b,a
      common/masses_hdec/ams,amc,amb,amt0
      common/break_hdec/amel,amer,amsq,amur,amdr,al,au,ad,amu,am20
c     common/squarkhiggs_hdec/theb,amg,ionsh,idth
      common/trilinear_hdec/au00,ad00,au1,ad1
      common/hhss_hdec/flltt(2,2),fhhtt(2,2),flhtt(2,2)
      a0(am,xmu2)=am**2*(1+dlog(xmu2/am**2))
      cc0(q12,q22,q32,am1,am2,am3) = c03_hdec(q12,q32,q22,am1,am2,am3)
      nc = 3
      pi = 4*datan(1.d0)
      v=1.d0/dsqrt(dsqrt(2.d0)*gf)
      tgb = dtan(b)
      sb = dsin(b)
      cb = dcos(b)
      sa = dsin(a)
      ca = dcos(a)
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      auu = au1
c     auu = au
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      fac = 1
c     amt = fac*amt0
      amt = amt0
      xmu = amt
      ep = 1.d-0
      amh = amhh*ep
      aml = amhl*ep
      cof = nc/(4*pi)**2/v**3
      xx1 = 0
      xx2 = 0
      xm0 = ghll*amz**2/v
c--2HDM
      dghll = -8*cof*amt**4*sa*ca**2/sb**3*(-2+3*dlog(xmu**2/amt**2))
      sigh = 2*cof*v*amt**2*ght*glt*(2*a0(amt,xmu**2)
     .             +(4*amt**2-amh**2)*b02_hdec(amh**2,amt,amt,xmu**2))
      sigl = 2*cof*v*amt**2*ght*glt*(2*a0(amt,xmu**2)
     .             +(4*amt**2-aml**2)*b02_hdec(aml**2,amt,amt,xmu**2))
      sig0 = 2*cof*v*amt**2*ght*glt*(2*a0(amt,xmu**2)
     .                        +4*amt**2*b02_hdec(0.d0,amt,amt,xmu**2))
      dzh = 2*cof*v*amt**2*ght*ght*(-b02_hdec(amh**2,amt,amt,xmu**2)
     .            +(4*amt**2-amh**2)*bp02_hdec(amh**2,amt,amt,xmu**2))
      dzl = 2*cof*v*amt**2*glt*glt*(-b02_hdec(aml**2,amt,amt,xmu**2)
     .            +(4*amt**2-aml**2)*bp02_hdec(aml**2,amt,amt,xmu**2))
      dad = -sig0/(amh**2-aml**2)
      dzheff = 2*cof*v*amt**2*ght*ght*(-b02_hdec(0.d0,amt,amt,xmu**2)
     .                       +4*amt**2*bp02_hdec(0.d0,amt,amt,xmu**2))
      dzleff = 2*cof*v*amt**2*glt*glt*(-b02_hdec(0.d0,amt,amt,xmu**2)
     .                       +4*amt**2*bp02_hdec(0.d0,amt,amt,xmu**2))
      dzeff = 2*cof*v*amt**2*ght*glt*(-b02_hdec(0.d0,amt,amt,xmu**2)
     .                       +4*amt**2*bp02_hdec(0.d0,amt,amt,xmu**2))
      xm1 = 8*cof*amt**4*sa*ca**2/sb**3*(b02_hdec(amh**2,amt,amt,xmu**2)
     .    + 2*b02_hdec(aml**2,amt,amt,xmu**2)
     .    + (4*amt**2-amh**2/2-aml**2)*dreal(
     .       cc0(amh**2,aml**2,aml**2,amt,amt,amt)))
      xm2 = ghll*(dzh/2+dzl) + glll*(sigh/(amh**2-aml**2)+dad)
     .                     - 2*glhh*(sigl/(amh**2-aml**2)+dad)
      xm3 = dghll
      xm4 = ghll*(-dzheff/2-dzleff) - glll*amh**2*dzeff/(amh**2-aml**2)
     .                            + 2*glhh*aml**2*dzeff/(amh**2-aml**2)
      xx1 = xm1+xm2+xm3+xm4
c     write(6,*)'hh1: ',2*xm1/xm0,2*xm2/xm0,2*xm3/xm0,2*xm4/xm0
      if(imssm.ne.0)then
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
c      am1 = fac*dsqrt((amsq**2+amur**2+2*amt**2
c    .       -dsqrt((amsq**2-amur**2)**2+4*amt**2*(au-amu*cb/sb)**2))/2)
c      am2 = fac*dsqrt((amsq**2+amur**2+2*amt**2
c    .       +dsqrt((amsq**2-amur**2)**2+4*amt**2*(au-amu*cb/sb)**2))/2)
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       am1 = fac*amst1
       am2 = fac*amst2
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       qt = (am1+am2)/2
       rmt = runm_hdec(qt,6)
       ct = (auu-amu*cb/sb)/(am1**2-am2**2)
       dt = (auu+amu*sb/cb)/(am1**2-am2**2)
       et = (auu-amu*ca/sa)/(am1**2-am2**2)
       ft = (auu+amu*sa/ca)/(am1**2-am2**2)
       gt = 2 + (am1**2+am2**2)/(am1**2-am2**2)*dlog(am2**2/am1**2)
c      sth = stht
c      cth = ctht
c      s2t = 2*sth*cth
c      c2t = cth**2-sth**2
       s2t = 2*rmt*ct
       c2t = dsqrt(1-s2t**2)
       if((amsq**2-amur**2)/(am1**2-am2**2).lt.0.d0) c2t = -c2t
       xlim = 1.d-10
       if(dabs(1-s2t**2).le.xlim) c2t = 0
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       glrl = rmt/2*(auu*glt+amu*ght)
       glrh = rmt/2*(auu*ght-amu*glt)
       g11l = rmt**2*glt + glrl*s2t
       g22l = rmt**2*glt - glrl*s2t
       g12l = glrl*c2t
       g11h = rmt**2*ght + glrh*s2t
       g22h = rmt**2*ght - glrh*s2t
       g12h = glrh*c2t
       f11ll = rmt**2*glt*glt
       f12ll = 0
       f22ll = rmt**2*glt*glt
       f11hh = rmt**2*ght*ght
       f12hh = 0
       f22hh = rmt**2*ght*ght
       f11lh = rmt**2*glt*ght
       f12lh = 0
       f22lh = rmt**2*glt*ght
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
c      g11l = amz**2*gltt(1,1)
c      g22l = amz**2*gltt(2,2)
c      g12l = amz**2*gltt(1,2)
c      g11h = amz**2*ghtt(1,1)
c      g22h = amz**2*ghtt(2,2)
c      g12h = amz**2*ghtt(1,2)
c      f11ll = amz**2*flltt(1,1)
c      f22ll = amz**2*flltt(2,2)
c      f12ll = amz**2*flltt(1,2)
c      f11hh = amz**2*fhhtt(1,1)
c      f22hh = amz**2*fhhtt(2,2)
c      f12hh = amz**2*fhhtt(1,2)
c      f11lh = amz**2*flhtt(1,1)
c      f22lh = amz**2*flhtt(2,2)
c      f12lh = amz**2*flhtt(1,2)
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       tl1 = dlog(am1**2/xmu**2)
       tl2 = dlog(am2**2/xmu**2)
       delta = 1 - 4*amt**2*(auu-amu*cb/sb)**2/(am2**2-am1**2)**2
       d_hlhlhh = delta*((am1**2-am2**2)*ft*(2*et+ft)*(tl1-tl2)
     .            +3*(am1**2-am2**2)**2*ct*et*ft**2*gt)
       dtghll =-4*cof*rmt**4*sa*ca**2/sb**3
     .        * (3*(tl1+tl2)+(am1**2-am2**2)*ct*(et+2*ft)*(tl1-tl2)
     .          +d_hlhlhh + 2*(amt**2/am1**2*(1+(am1**2-am2**2)*ct*et)
     .                        *(1+(am1**2-am2**2)*ct*ft)**2
     .                        +amt**2/am2**2*(1-(am1**2-am2**2)*ct*et)
     .                        *(1-(am1**2-am2**2)*ct*ft)**2))
       tsigh =-2*cof*v*(f11lh*a0(am1,xmu**2)+f22lh*a0(am2,xmu**2)
     .                 +2*g11l*g11h*b02_hdec(amh**2,am1,am1,xmu**2)
     .                 +2*g22l*g22h*b02_hdec(amh**2,am2,am2,xmu**2)
     .                 +4*g12l*g12h*b02_hdec(amh**2,am1,am2,xmu**2))
       tsigl =-2*cof*v*(f11lh*a0(am1,xmu**2)+f22lh*a0(am2,xmu**2)
     .                 +2*g11l*g11h*b02_hdec(aml**2,am1,am1,xmu**2)
     .                 +2*g22l*g22h*b02_hdec(aml**2,am2,am2,xmu**2)
     .                 +4*g12l*g12h*b02_hdec(aml**2,am1,am2,xmu**2))
       tsig0 =-2*cof*v*(f11lh*a0(am1,xmu**2)+f22lh*a0(am2,xmu**2)
     .                 +2*g11l*g11h*b02_hdec(0.d0,am1,am1,xmu**2)
     .                 +2*g22l*g22h*b02_hdec(0.d0,am2,am2,xmu**2)
     .                 +4*g12l*g12h*b02_hdec(0.d0,am1,am2,xmu**2))
       dtzh =-4*cof*v*(g11h*g11h*bp02_hdec(amh**2,am1,am1,xmu**2)
     .                +g22h*g22h*bp02_hdec(amh**2,am2,am2,xmu**2)
     .              +2*g12h*g12h*bp02_hdec(amh**2,am1,am2,xmu**2))
       dtzl =-4*cof*v*(g11l*g11l*bp02_hdec(aml**2,am1,am1,xmu**2)
     .                +g22l*g22l*bp02_hdec(aml**2,am2,am2,xmu**2)
     .              +2*g12l*g12l*bp02_hdec(aml**2,am1,am2,xmu**2))
       dtad = -tsig0/(amh**2-aml**2)
       dtzheff =-4*cof*v*(g11h*g11h*bp02_hdec(0.d0,am1,am1,xmu**2)
     .                   +g22h*g22h*bp02_hdec(0.d0,am2,am2,xmu**2)
     .                 +2*g12h*g12h*bp02_hdec(0.d0,am1,am2,xmu**2))
       dtzleff =-4*cof*v*(g11l*g11l*bp02_hdec(0.d0,am1,am1,xmu**2)
     .                   +g22l*g22l*bp02_hdec(0.d0,am2,am2,xmu**2)
     .                 +2*g12l*g12l*bp02_hdec(0.d0,am1,am2,xmu**2))
       dtzeff =-4*cof*v*(g11l*g11h*bp02_hdec(0.d0,am1,am1,xmu**2)
     .                  +g22l*g22h*bp02_hdec(0.d0,am2,am2,xmu**2)
     .                +2*g12l*g12h*bp02_hdec(0.d0,am1,am2,xmu**2))
       ym1 =-16*cof*(
     .  g11h*g11l*g11l*dreal(cc0(amh**2,aml**2,aml**2,am1,am1,am1))
     . +g11h*g12l*g12l*dreal(cc0(amh**2,aml**2,aml**2,am1,am1,am2))
     . +g12h*g11l*g12l*dreal(cc0(amh**2,aml**2,aml**2,am1,am2,am1))
     . +g12h*g12l*g11l*dreal(cc0(amh**2,aml**2,aml**2,am2,am1,am1))
     . +g22h*g12l*g12l*dreal(cc0(amh**2,aml**2,aml**2,am2,am2,am1))
     . +g12h*g22l*g12l*dreal(cc0(amh**2,aml**2,aml**2,am2,am1,am2))
     . +g12h*g12l*g22l*dreal(cc0(amh**2,aml**2,aml**2,am1,am2,am2))
     . +g22h*g22l*g22l*dreal(cc0(amh**2,aml**2,aml**2,am2,am2,am2))
     .  )
       ym2 =-4*cof*(g11h*f11ll*b02_hdec(amh**2,am1,am1,xmu**2)
     .           +2*g12h*f12ll*b02_hdec(amh**2,am1,am2,xmu**2)
     .             +g22h*f22ll*b02_hdec(amh**2,am2,am2,xmu**2)
     .           +2*g11l*f11lh*b02_hdec(aml**2,am1,am1,xmu**2)
     .           +4*g12l*f12lh*b02_hdec(aml**2,am1,am2,xmu**2)
     .           +2*g22l*f22lh*b02_hdec(aml**2,am2,am2,xmu**2))
       ym3 = dtghll
       ym4 = ghll*(dtzh/2+dtzl) + glll*(tsigh/(amh**2-aml**2)+dtad)
     .                        - 2*glhh*(tsigl/(amh**2-aml**2)+dtad)
       ym5 = ghll*(-dtzheff/2-dtzleff)
     .     -   glll*amh**2*dtzeff/(amh**2-aml**2)
     .     + 2*glhh*aml**2*dtzeff/(amh**2-aml**2)
       xx2 = ym1+ym2+ym3+ym4+ym5
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
c     mst12 = am1**2
c     mst22 = am2**2
c     mt = amt
c     lt = dlog(amt**2/xmu**2)
c     lst1 = dlog(am1**2/xmu**2)
c     lst2 = dlog(am2**2/xmu**2)
c     at = au

c     t1_s1s1s1=(-8*(2*((mst12-mst22)**2+6*gt*mst12*mst22)*ct**2*mt**
c    . 2-3*gt*mst12*mst22)*(at-ct*mst12+ct*mst22)**3*ct*mt**4)/((
c    . mst12-mst22)*(sb+1)*(sb-1)*cb*mst12*mst22*v**3)

c     t1_s1s1s2=(8*(12*at*ct**3*gt*mst12**2*mst22*mt**2+12*at*ct**3*
c    . gt*mst12*mst22**2*mt**2+2*at*ct**3*mst12**3*mt**2-2*at*ct**3*
c    . mst12**2*mst22*mt**2-2*at*ct**3*mst12*mst22**2*mt**2+2*at*ct**
c    . 3*mst22**3*mt**2-3*at*ct*gt*mst12**2*mst22-3*at*ct*gt*mst12*
c    . mst22**2-4*ct**2*gt*mst12**2*mst22*mt**2+4*ct**2*gt*mst12*
c    . mst22**2*mt**2-2*ct**2*mst12**3*mt**2+6*ct**2*mst12**2*mst22*
c    . mt**2-6*ct**2*mst12*mst22**2*mt**2+2*ct**2*mst22**3*mt**2+gt*
c    . mst12**2*mst22-gt*mst12*mst22**2-2*mst12**2*mst22+2*mst12*
c    . mst22**2)*(at-ct*mst12+ct*mst22)**2*mt**4)/((mst12+mst22)*(
c    . mst12-mst22)*(sb+1)*(sb-1)*mst12*mst22*sb*v**3)

c     t1_s1s2s2=(8*(12*at**2*ct**3*gt*mst12**2*mst22*mt**2+12*at**2*
c    . ct**3*gt*mst12*mst22**2*mt**2+2*at**2*ct**3*mst12**3*mt**2-2*
c    . at**2*ct**3*mst12**2*mst22*mt**2-2*at**2*ct**3*mst12*mst22**2*
c    . mt**2+2*at**2*ct**3*mst22**3*mt**2-3*at**2*ct*gt*mst12**2*
c    . mst22-3*at**2*ct*gt*mst12*mst22**2-8*at*ct**2*gt*mst12**2*
c    . mst22*mt**2+8*at*ct**2*gt*mst12*mst22**2*mt**2-4*at*ct**2*
c    . mst12**3*mt**2+12*at*ct**2*mst12**2*mst22*mt**2-12*at*ct**2*
c    . mst12*mst22**2*mt**2+4*at*ct**2*mst22**3*mt**2+2*at*gt*mst12**
c    . 2*mst22-2*at*gt*mst12*mst22**2-4*at*mst12**2*mst22+4*at*mst12*
c    . mst22**2+ct*gt*mst12**3*mst22-2*ct*gt*mst12**2*mst22**2+ct*gt*
c    . mst12*mst22**3-2*ct*mst12**3*mst22+2*ct*mst12**3*mt**2+4*ct*
c    . mst12**2*mst22**2-2*ct*mst12**2*mst22*mt**2-2*ct*mst12*mst22**
c    . 3-2*ct*mst12*mst22**2*mt**2+2*ct*mst22**3*mt**2)*(at-ct*mst12+
c    . ct*mst22)*mt**4)/((mst12+mst22)*(mst12-mst22)*cb*mst12*mst22*
c    . sb**2*v**3)

c     t1_s2s2s2=(8*((2*(mst12**2*mst22+mst12**2*mt**2-5*mst12*mst22**
c    . 2+2*mst12*mst22*mt**2+mst22**2*mt**2)-3*(mst12-mst22)*gt*mst12
c    . *mst22+6*(lst2-lt)*(mst12+mst22)*mst12*mst22+3*(2*(mst12*mst22
c    . -mst12*mt**2-mst22*mt**2)-gt*mst12*mst22)*(mst12-mst22)*at*ct+
c    . 3*(2*((mst12-mst22)**2+2*gt*mst12*mst22)*ct**2*mt**2-(gt-2)*
c    . mst12*mst22)*at**2)*(mst12-mst22)-(2*((mst12-mst22)**2+6*gt*
c    . mst12*mst22)*ct**2*mt**2-3*gt*mst12*mst22)*(mst12+mst22)*at**3
c    . *ct)*mt**4)/((mst12+mst22)*(mst12-mst22)*mst12*mst22*sb**3*v**
c    . 3)

c     t2_s2s2s2 =-16*mt**4/v**3/sb**3*(3*lt+2)
c     t1_s2s2s2=t1_s2s2s2-t2_s2s2s2

c     t1_hlhlhh = -sa*ca**2*t1_s2s2s2 - ca*(ca**2-2*sa**2)*t1_s1s2s2
c    .        +sa*(2*ca**2-sa**2)*t1_s1s1s2 - sa**2*ca*t1_s1s1s1
c     t1_hlhlhh = t1_hlhlhh*v**3/2*cof
c     write(6,*)t1_hlhlhh
c     write(6,*)dtghll
c     write(6,*)
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
c      write(6,*)'hh2: ',2*(ym1+ym2)/xm0,2*ym3/xm0,2*ym4/xm0,2*ym5/xm0
c      write(6,*)'hh: ',ym1,ym2,ym3,ym4,ym5
c      write(6,*)
c      write(6,*)ym1+ym2,ym4
c      write(6,*)ym3,ym5
c      write(6,*)
c      write(6,*)dtzh,dtzl
c      write(6,*)dtzheff,dtzleff
c      write(6,*)
c      write(6,*)tsigh/(amh**2-aml**2),tsigl/(amh**2-aml**2)
c      write(6,*)dtad,dtad
c      write(6,*)dtad-dtzeff/(amh**2-aml**2),dtad-dtzeff/(amh**2-aml**2)
c      write(6,*)
c      write(6,*)am1,am2
c      write(6,*)
      endif
      dummy = 2*(xx1+xx2)/xm0
      h2hh_hdec = dummy
c     hlo=gf/16/dsqrt(2d0)/pi*amz**4/amh*beta_hdec(aml**2/amh**2)
c    .   *ghll**2
c     write(6,*)hlo,hlo*(1+dummy),1+dummy
      return
      end

