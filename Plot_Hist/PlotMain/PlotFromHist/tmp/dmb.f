 
      double precision function t134p_hdec(am1,am2,mu)
      implicit double precision (a-h,o-z)
      double precision m1,m2,mu,ll1,ll2
      complex*16 li2_hdec
      sp(a) = dreal(li2_hdec(dcmplx(a,0.d0)))
      pi = 4*datan(1.d0)
      zeta2 = pi**2/6
      if(am1.lt.am2)then
       m1 = am1
       m2 = am2
      else
       m1 = am2
       m2 = am1
      endif
      ll1 = dlog(mu**2/m1**2)
      ll2 = dlog(mu**2/m2**2)
      if(m1.eq.m2)then
       dummy = 7*(m1**2+m2**2)/2
     .       + m1**2*(ll1**2+3*ll1) + m2**2*(ll2**2+3*ll2)
     .       - m1**2/2*dlog(m1**2/m2**2)**2
      else
       dummy = 7*(m1**2+m2**2)/2
     .       + m1**2*(ll1**2+3*ll1) + m2**2*(ll2**2+3*ll2)
     .       + (m1**2-m2**2)*(dlog(m1**2/m2**2)*dlog(1-m1**2/m2**2)
     .                       + sp(m1**2/m2**2)-zeta2)
     .       - m1**2/2*dlog(m1**2/m2**2)**2
      endif
      t134p_hdec = dummy/mu**2
      return
      end
 
c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 
      double precision function t134_hdec(am1,am2,am3,mu)
      implicit double precision (a-h,o-z)
      double precision m1,m2,m3,mu,ll1,ll2,ll3
      complex*16 sp,li2_hdec,lam,ll,cx,cy,phi
      sp(cx) = li2_hdec(cx)
      lam(cx,cy) = (1-cx-cy)**2-4*cx*cy
      phi(cx,cy,ll) = (2*cdlog((1+cx-cy-ll)/2)*cdlog((1-cx+cy-ll)/2)
     .              -cdlog(cx)*cdlog(cy)+2*zeta2
     .              -2*sp((1+cx-cy-ll)/2)-2*sp((1-cx+cy-ll)/2))/ll
      eps = 1.d-15
      rim = dcmplx(1.d0,eps)
      pi = 4*datan(1.d0)
      zeta2 = pi**2/6
      m1 = dmin1(am1,am2,am3)
      m3 = dmax1(am1,am2,am3)
      if(m1.eq.am2.and.m3.eq.am3.or.m1.eq.am3.and.m3.eq.am2) m2 = am1
      if(m1.eq.am1.and.m3.eq.am3.or.m1.eq.am3.and.m3.eq.am1) m2 = am2
      if(m1.eq.am1.and.m3.eq.am2.or.m1.eq.am2.and.m3.eq.am1) m2 = am3
      cx = m1**2/m3**2*rim
      cy = m2**2/m3**2*rim
      ll1 = dlog(mu**2/m1**2)
      ll2 = dlog(mu**2/m2**2)
      ll3 = dlog(mu**2/m3**2)
      ll = cdsqrt(lam(cx,cy))
      dummy = 7*(m1**2+m2**2+m3**2)/2
     .      + m1**2*(ll1**2+3*ll1) + m2**2*(ll2**2+3*ll2)
     .      + m3**2*(ll3**2+3*ll3)
     .      +  (m1**2-m2**2-m3**2)/4*dlog(m2**2/m3**2)**2
     .      + (-m1**2+m2**2-m3**2)/4*dlog(m1**2/m3**2)**2
     .      + (-m1**2-m2**2+m3**2)/4*dlog(m1**2/m2**2)**2
     .      + m3**2/2*lam(cx,cy)*phi(cx,cy,ll)
      t134_hdec = dummy/mu**2
      return
      end
 
c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 
      double precision function
     .       felw_hdec(scale,amu,amg,amsb1,amsb2,amst1,amst2,amt)
      implicit double precision (b-h,o-q,s-z), complex*16 (a,r)
      double precision amg,amsb1,amsb2,amst1,amst2,amu,amt
      double precision mg,mb1,mb2,mt1,mt2,mu,mt
      double precision anomalous
      double precision a
      complex*16 sp,li2_hdec,xgl,xt1,xt2,xt,xb1,xb2
      sp(r) = li2_hdec(r)
      fi(a,b,c) = (a*b*log(a/b)+b*c*log(b/c)+c*a*log(c/a))
     .          / (a-b)/(b-c)/(a-c)
      t134p(a,b,c)  = t134p_hdec(a,b,c)
      t134(a,b,c,d) = t134_hdec(a,b,c,d)

      eps = 1.d-15
      pi = 4*datan(1.d0)
      zeta2 = pi**2/6

      fnorm = 1/amu**2

      cf = 4/3.d0

      rim = dcmplx(1.d0,eps)

      mt  = amt
      mu  = dabs(amu)
      mg  = amg
      mt1 = amst1
      mt2 = amst2
      mb1 = amsb1
      mb2 = amsb2

      xt  = amt**2/amu**2   * rim
      xgl = amg**2/amu**2   * rim
      xt1 = amst1**2/amu**2 * rim
      xt2 = amst2**2/amu**2 * rim
      xb1 = amsb1**2/amu**2 * rim
      xb2 = amsb2**2/amu**2 * rim

      r22=(4*log(xgl)**2*(-xt1**2*xt2+xt1*xt2**2+xt1-xt2)+4*log(xgl)*
     . log(xt1)*xt1*(-xt2**2+2*xt2-1)+4*log(xgl)*log(xt2)*xt2*(xt1**2
     . -2*xt1+1)+12*log(xgl)*(-xt1**2*xt2+xt1*xt2**2+xt1-xt2)+log(xt1
     . )**2*xt1*(xt2**2-2*xt2+1)+2*log(xt1)*xt1*(-xt1*xt2**2+2*xt1*
     . xt2-xt1-2*xt2**2+4*xt2-2)+log(xt2)**2*xt2*(-xt1**2+2*xt1-1)+2*
     . log(xt2)*xt2*(xt1**2*xt2+2*xt1**2-2*xt1*xt2-4*xt1+xt2+2)+t134p
     . (mu,mt1,mg)*xgl*(-xt1*xt2**2+2*xt1*xt2-xt1-xt2**2+2*xt2-1)+
     . t134p(mu,mt2,mg)*xgl*(xt1**2*xt2+xt1**2-2*xt1*xt2-2*xt1+xt2+1)
     . +14*(-xt1**2*xt2+xt1*xt2**2+xt1-xt2))/(2*(xt1**3*xt2**2-2*xt1
     . **3*xt2+xt1**3-xt1**2*xt2**3+3*xt1**2*xt2-2*xt1**2+2*xt1*xt2**
     . 3-3*xt1*xt2**2+xt1-xt2**3+2*xt2**2-xt2))

      r42=(8*log(xgl)**2*(xt1**2*xt2-xt1*xt2**2-xt1+xt2)+8*log(xgl)*
     . log(xt1)*xt1*(xt2**2-2*xt2+1)+8*log(xgl)*log(xt2)*xt2*(-xt1**2
     . +2*xt1-1)+24*log(xgl)*(xt1**2*xt2-xt1*xt2**2-xt1+xt2)+2*log(
     . xt1)**2*xt1*(-xt2**2+2*xt2-1)+log(xt1)*xt1*(5*xt1*xt2**2-10*
     . xt1*xt2+5*xt1+7*xt2**2-14*xt2+7)+2*log(xt2)**2*xt2*(xt1**2-2*
     . xt1+1)+log(xt2)*xt2*(-5*xt1**2*xt2-7*xt1**2+10*xt1*xt2+14*xt1-
     . 5*xt2-7)+2*t134p(mt1,mu,mg)*xgl*(xt1*xt2**2-2*xt1*xt2+xt1+xt2
     . **2-2*xt2+1)+2*t134p(mt2,mu,mg)*xgl*(-xt1**2*xt2-xt1**2+2*xt1*
     . xt2+2*xt1-xt2-1)+28*(xt1**2*xt2-xt1*xt2**2-xt1+xt2))/(2*(xt1**
     . 3*xt2**2-2*xt1**3*xt2+xt1**3-xt1**2*xt2**3+3*xt1**2*xt2-2*xt1
     . **2+2*xt1*xt2**3-3*xt1*xt2**2+xt1-xt2**3+2*xt2**2-xt2))

      ans3=t134(mt2,mg,mt,mg)*xgl*(-xb1*xgl*xt1+xb1*xgl-xb1*xt*xt1+
     . xb1*xt+xb1*xt1*xt2-xb1*xt2-xb2*xgl*xt1+xb2*xgl-xb2*xt*xt1+xb2*
     . xt+xb2*xt1*xt2-xb2*xt2+2*xgl**2*xt1-2*xgl**2+2*xgl*xt*xt1-2*
     . xgl*xt-2*xgl*xt1*xt2+2*xgl*xt2)+t134(mu,mb1,mt,mg)*xgl*(-xb1*
     . xb2*xt1+xb1*xb2*xt2+xb1*xgl*xt1-xb1*xgl*xt2-xb2*xt*xt1+xb2*xt*
     . xt2+xb2*xt1-xb2*xt2+xgl*xt*xt1-xgl*xt*xt2-xgl*xt1+xgl*xt2)+
     . t134(mu,mb2,mt,mg)*xgl*(-xb1*xb2*xt1+xb1*xb2*xt2-xb1*xt*xt1+
     . xb1*xt*xt2+xb1*xt1-xb1*xt2+xb2*xgl*xt1-xb2*xgl*xt2+xgl*xt*xt1-
     . xgl*xt*xt2-xgl*xt1+xgl*xt2)+t134(mu,mg,mt,mg)*xgl*(xb1*xgl*xt1
     . -xb1*xgl*xt2+xb1*xt*xt1-xb1*xt*xt2-xb1*xt1+xb1*xt2+xb2*xgl*xt1
     . -xb2*xgl*xt2+xb2*xt*xt1-xb2*xt*xt2-xb2*xt1+xb2*xt2-2*xgl**2*
     . xt1+2*xgl**2*xt2-2*xgl*xt*xt1+2*xgl*xt*xt2+2*xgl*xt1-2*xgl*xt2
     . )
      ans2=t134(mt1,mb1,mt,mg)*xgl*(-xb1*xb2*xt2+xb1*xb2+xb1*xgl*xt2-
     . xb1*xgl-xb2*xt*xt2+xb2*xt+xb2*xt1*xt2-xb2*xt1+xgl*xt*xt2-xgl*
     . xt-xgl*xt1*xt2+xgl*xt1)+t134(mt1,mb2,mt,mg)*xgl*(-xb1*xb2*xt2+
     . xb1*xb2-xb1*xt*xt2+xb1*xt+xb1*xt1*xt2-xb1*xt1+xb2*xgl*xt2-xb2*
     . xgl+xgl*xt*xt2-xgl*xt-xgl*xt1*xt2+xgl*xt1)+t134(mt1,mg,mt,mg)*
     . xgl*(xb1*xgl*xt2-xb1*xgl+xb1*xt*xt2-xb1*xt-xb1*xt1*xt2+xb1*xt1
     . +xb2*xgl*xt2-xb2*xgl+xb2*xt*xt2-xb2*xt-xb2*xt1*xt2+xb2*xt1-2*
     . xgl**2*xt2+2*xgl**2-2*xgl*xt*xt2+2*xgl*xt+2*xgl*xt1*xt2-2*xgl*
     . xt1)+t134(mt2,mb1,mt,mg)*xgl*(xb1*xb2*xt1-xb1*xb2-xb1*xgl*xt1+
     . xb1*xgl+xb2*xt*xt1-xb2*xt-xb2*xt1*xt2+xb2*xt2-xgl*xt*xt1+xgl*
     . xt+xgl*xt1*xt2-xgl*xt2)+t134(mt2,mb2,mt,mg)*xgl*(xb1*xb2*xt1-
     . xb1*xb2+xb1*xt*xt1-xb1*xt-xb1*xt1*xt2+xb1*xt2-xb2*xgl*xt1+xb2*
     . xgl-xgl*xt*xt1+xgl*xt+xgl*xt1*xt2-xgl*xt2)+ans3
      ans1=log(xb1)*log(xt1)*xb1*xt1*(-xb2*xt2+xb2+xgl*xt2-xgl)+log(
     . xb1)*log(xt2)*xb1*xt2*(xb2*xt1-xb2-xgl*xt1+xgl)+log(xb2)*log(
     . xt1)*xb2*xt1*(-xb1*xt2+xb1+xgl*xt2-xgl)+log(xb2)*log(xt2)*xb2*
     . xt2*(xb1*xt1-xb1-xgl*xt1+xgl)+log(xgl)*log(xt1)*xt1*(4*xb1*xb2
     . *xt2-4*xb1*xb2-3*xb1*xgl*xt2+3*xb1*xgl-3*xb2*xgl*xt2+3*xb2*xgl
     . +2*xgl**2*xt2-2*xgl**2)+log(xgl)*log(xt2)*xt2*(-4*xb1*xb2*xt1+
     . 4*xb1*xb2+3*xb1*xgl*xt1-3*xb1*xgl+3*xb2*xgl*xt1-3*xb2*xgl-2*
     . xgl**2*xt1+2*xgl**2)+log(xt1)**2*xt1*(-xb1*xb2*xt2+xb1*xb2+xb1
     . *xgl*xt2-xb1*xgl+xb2*xgl*xt2-xb2*xgl-xgl**2*xt2+xgl**2)+4*log(
     . xt1)*xt1*(xb1*xb2*xt2-xb1*xb2-xb1*xgl*xt2+xb1*xgl-xb2*xgl*xt2+
     . xb2*xgl+xgl**2*xt2-xgl**2)+log(xt2)**2*xt2*(xb1*xb2*xt1-xb1*
     . xb2-xb1*xgl*xt1+xb1*xgl-xb2*xgl*xt1+xb2*xgl+xgl**2*xt1-xgl**2)
     . +4*log(xt2)*xt2*(-xb1*xb2*xt1+xb1*xb2+xb1*xgl*xt1-xb1*xgl+xb2*
     . xgl*xt1-xb2*xgl-xgl**2*xt1+xgl**2)+ans2
      r52=ans1/(4*(xb1*xb2*xt1**2*xt2-xb1*xb2*xt1**2-xb1*xb2*xt1*xt2
     . **2+xb1*xb2*xt1+xb1*xb2*xt2**2-xb1*xb2*xt2-xb1*xgl*xt1**2*xt2+
     . xb1*xgl*xt1**2+xb1*xgl*xt1*xt2**2-xb1*xgl*xt1-xb1*xgl*xt2**2+
     . xb1*xgl*xt2-xb2*xgl*xt1**2*xt2+xb2*xgl*xt1**2+xb2*xgl*xt1*xt2
     . **2-xb2*xgl*xt1-xb2*xgl*xt2**2+xb2*xgl*xt2+xgl**2*xt1**2*xt2-
     . xgl**2*xt1**2-xgl**2*xt1*xt2**2+xgl**2*xt1+xgl**2*xt2**2-xgl**
     . 2*xt2))

      ans1=8*log(xgl)**2*(xt1**2*xt2-xt1**2-xt1*xt2**2+xt1+xt2**2-xt2
     . )+4*log(xgl)*log(xt1)*xt1*(4*xt1*xt2**2-8*xt1*xt2+4*xt1-3*xt2
     . **2+6*xt2-3)+4*log(xgl)*log(xt2)*xt2*(-4*xt1**2*xt2+3*xt1**2+8
     . *xt1*xt2-6*xt1-4*xt2+3)+12*log(xgl)*(xt1**2*xt2-xt1**2-xt1*xt2
     . **2+xt1+xt2**2-xt2)+log(xt1)**2*xt1*(-8*xt1*xt2**2+16*xt1*xt2-
     . 8*xt1+5*xt2**2-10*xt2+5)+4*log(xt1)*xt1*(3*xt1*xt2**2-6*xt1*
     . xt2+3*xt1-2*xt2**2+4*xt2-2)+log(xt2)**2*xt2*(8*xt1**2*xt2-5*
     . xt1**2-16*xt1*xt2+10*xt1+8*xt2-5)+4*log(xt2)*xt2*(-3*xt1**2*
     . xt2+2*xt1**2+6*xt1*xt2-4*xt1-3*xt2+2)+4*t134p(mt1,mt1,mg)*xgl*
     . (xt1*xt2**2-2*xt1*xt2+xt1+xt2**2-2*xt2+1)+4*t134p(mt2,mt2,mg)*
     . xgl*(-xt1**2*xt2-xt1**2+2*xt1*xt2+2*xt1-xt2-1)+4*t134p(mu,mt1,
     . mg)*xgl*(-xt1*xt2**2+2*xt1*xt2-xt1-xt2**2+2*xt2-1)+4*t134p(mu,
     . mt2,mg)*xgl*(xt1**2*xt2+xt1**2-2*xt1*xt2-2*xt1+xt2+1)+8*(xt1**
     . 2*xt2-xt1**2-xt1*xt2**2+xt1+xt2**2-xt2)
      r72=ans1/(8*(xt1**3*xt2**2-2*xt1**3*xt2+xt1**3-xt1**2*xt2**3+3*
     . xt1**2*xt2-2*xt1**2+2*xt1*xt2**3-3*xt1*xt2**2+xt1-xt2**3+2*xt2
     . **2-xt2))

      ans5=2*((2*((14*xt2-15+14*xt1+5*xt)*xt-((xt2-3)*xt2+xt1**2+(4*
     . xt2-3)*xt1))*xgl**3+(4*xt2-3+4*xt1-8*xt)*xgl**4-((2*xt+3)*(xt-
     . xt1)**2*(xt-xt2)**2+2*xgl**5)-(2*(2*((3*xt2-2)*xt2+3*xt1**2)+(
     . 5*xt2-4)*xt1)*xt-((4*(xt2-3)*xt1-3*xt2)*xt2+(4*xt2-3)*xt1**2)-
     . 2*(24*xt2-23+24*xt1)*xt**2-10*xt**3)*xgl**2-2*((2*((3*xt2-2)*
     . xt2+3*xt1**2)+(5*xt2-4)*xt1)*xt**2+(3*((xt2-1)*xt1**2-xt2**2)+
     . (3*xt2+5)*xt1*xt2)*xt-(14*xt2-15+14*xt1)*xt**3+((xt2-3)*xt1-3*
     . xt2)*xt1*xt2+4*xt**4)*xgl)*(xt1-1)*(xt2-1)-(2*(xt+xt1)*xgl-(xt
     . -xt1)**2-xgl**2)*(2*(xt+xt2)*xgl-(xt-xt2)**2-xgl**2)*(xt-1+xgl
     . )*(xt2-2+xt1)*t134(mu,mt,mg,mg)*xgl)*(xt1-xt2)
      ans4=-2*((2*((xt-xt1)**2*(xt-xt2)**2+xgl**4-(6*xt**2+10*xt*xt1+
     . 10*xt*xt2-12*xt-xt1**2-4*xt1*xt2-xt2**2)*xgl**2-2*(xt1+xt2-xt)
     . *xgl**3+2*(((2*xt2-3)*xt2+2*xt1**2+(7*xt2-3)*xt1)*xt-(5*xt2-6+
     . 5*xt1)*xt**2-(xt1+xt2)*xt1*xt2+xt**3)*xgl)*(xt1-1)*(xt2-1)+(2*
     . (xt+xt1)*xgl-(xt-xt1)**2-xgl**2)*(2*(xt+xt2)*xgl-(xt-xt2)**2-
     . xgl**2)*(xt2-2+xt1)*log(xgl))*(xt1-xt2)+(2*(xt+xt1)*xgl+(xt-
     . xt1)**2*(xt1-2)-xgl**2*xt1)*(2*(xt+xt2)*xgl-(xt-xt2)**2-xgl**2
     . )*(log(xgl)-log(xt1))*(xt2-1)**2-(2*(xt+xt1)*xgl-(xt-xt1)**2-
     . xgl**2)*(2*(xt+xt2)*xgl+(xt-xt2)**2*(xt2-2)-xgl**2*xt2)*(log(
     . xgl)-log(xt2))*(xt1-1)**2)*(log(xgl)-log(xt))*xt+ans5
      ans3=-(4*((xt-xt2**2+xt2)*(xt-xt2)**2+xgl**3-((xt2+1)*xt2+xt)*
     . xgl**2-((xt+4*xt2**2)*xt-(2*xt2-1)*xt2**2)*xgl)+(((xt+xt2)*(xt
     . -xt2)*(xt2-2)-4*xt*xt2)*xgl+(xt+2*xt2)*(xt2-2)*xgl**2-(xt-xt2)
     . **2*(xt2-2)*xt-(xt2-2)*xgl**3)*(log(xgl)-log(xt2)))*(2*(xt+xt1
     . )*xgl-(xt-xt1)**2-xgl**2)*(log(xgl)-log(xt2))*(xt1-1)**2+(4*((
     . xt-xt1**2+xt1)*(xt-xt1)**2+xgl**3-((xt1+1)*xt1+xt)*xgl**2-((xt
     . +4*xt1**2)*xt-(2*xt1-1)*xt1**2)*xgl)+(((xt+xt1)*(xt-xt1)*(xt1-
     . 2)-4*xt*xt1)*xgl+(xt+2*xt1)*(xt1-2)*xgl**2-(xt-xt1)**2*(xt1-2)
     . *xt-(xt1-2)*xgl**3)*(log(xgl)-log(xt1)))*(2*(xt+xt2)*xgl-(xt-
     . xt2)**2-xgl**2)*(log(xgl)-log(xt1))*(xt2-1)**2+ans4
      ans2=(2*(((xt+2*xt2)*xt+(xt2-4)*xt2)*xgl+(xt2+2+xt)*xgl**2-(xt+
     . xt2-2)*(xt-xt2)**2-xgl**3)*(xt1-1)**2*t134(mt2,mt,mg,mg)*xgl-(
     . 2*(xt+xt2)*xgl-(xt-xt2)**2-xgl**2)*(xt2-2+xt1)*(log(xgl)+4)*(
     . xgl+xt)*(xt1-xt2)*log(xgl))*(2*(xt+xt1)*xgl-(xt-xt1)**2-xgl**2
     . )-2*(((xt+2*xt1)*xt+(xt1-4)*xt1)*xgl+(xt1+2+xt)*xgl**2-(xt+xt1
     . -2)*(xt-xt1)**2-xgl**3)*(2*(xt+xt2)*xgl-(xt-xt2)**2-xgl**2)*(
     . xt2-1)**2*t134(mt1,mt,mg,mg)*xgl+((2*(xt1+xt2)-xgl)*xgl**3-(xt
     . -xt1)**2*(xt-xt2)**2+(2*xt**2+6*xt*xt1+6*xt*xt2-8*xt-xt1**2-4*
     . xt1*xt2-xt2**2)*xgl**2-2*(((xt2-2)*xt2+xt1**2+2*(3*xt2-1)*xt1)
     . *xt-(3*xt2-4+3*xt1)*xt**2-(xt1+xt2)*xt1*xt2)*xgl)*(log(xgl)-
     . log(xt))**2*(xt1-xt2)*(xt1-1)*(xt2-1)*xt+ans3
      ans1=-ans2
      r82=ans1/(4*((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)*((xt-xt2)**2+
     . xgl**2-2*(xt+xt2)*xgl)*(xt1-xt2)*(xt1-1)**2*(xt2-1)**2)

      ans2=4*log(xt2)*xt2*(-3*xt1**3*xt2+2*xt1**3+3*xt1**2*xt2**2+4*
     . xt1**2*xt2-4*xt1**2-6*xt1*xt2**2+xt1*xt2+2*xt1+3*xt2**2-2*xt2)
     . +4*(xt1**3*xt2-xt1**3-2*xt1**2*xt2**2+xt1**2*xt2+xt1**2+xt1*
     . xt2**3+xt1*xt2**2-2*xt1*xt2-xt2**3+xt2**2)
      ans1=4*log(xgl)*log(xt1)*xt1*(2*xt1**2*xt2**2-4*xt1**2*xt2+2*
     . xt1**2-2*xt1*xt2**3+3*xt1*xt2**2-xt1+xt2**3-2*xt2**2+xt2)+4*
     . log(xgl)*log(xt2)*xt2*(-2*xt1**3*xt2+xt1**3+2*xt1**2*xt2**2+3*
     . xt1**2*xt2-2*xt1**2-4*xt1*xt2**2+xt1+2*xt2**2-xt2)+4*log(xgl)*
     . (xt1**3*xt2-xt1**3-2*xt1**2*xt2**2+xt1**2*xt2+xt1**2+xt1*xt2**
     . 3+xt1*xt2**2-2*xt1*xt2-xt2**3+xt2**2)+log(xt1)**2*xt1*(-6*xt1
     . **2*xt2**2+12*xt1**2*xt2-6*xt1**2+2*xt1*xt2**3-xt1*xt2**2-4*
     . xt1*xt2+3*xt1+xt2**3-2*xt2**2+xt2)+4*log(xt1)*log(xt2)*xt1*xt2
     . *(xt1**2*xt2-xt1**2+xt1*xt2**2-4*xt1*xt2+3*xt1-xt2**2+3*xt2-2)
     . +4*log(xt1)*xt1*(3*xt1**2*xt2**2-6*xt1**2*xt2+3*xt1**2-3*xt1*
     . xt2**3+4*xt1*xt2**2+xt1*xt2-2*xt1+2*xt2**3-4*xt2**2+2*xt2)+log
     . (xt2)**2*xt2*(2*xt1**3*xt2+xt1**3-6*xt1**2*xt2**2-xt1**2*xt2-2
     . *xt1**2+12*xt1*xt2**2-4*xt1*xt2+xt1-6*xt2**2+3*xt2)+ans2
      r92=ans1/(8*(xt1**4*xt2**2-2*xt1**4*xt2+xt1**4-2*xt1**3*xt2**3+
     . 2*xt1**3*xt2**2+2*xt1**3*xt2-2*xt1**3+xt1**2*xt2**4+2*xt1**2*
     . xt2**3-6*xt1**2*xt2**2+2*xt1**2*xt2+xt1**2-2*xt1*xt2**4+2*xt1*
     . xt2**3+2*xt1*xt2**2-2*xt1*xt2+xt2**4-2*xt2**3+xt2**2))

      ans6=-sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2)*(((xt1-xt2)*xt1+
     . 4*xt**2)*(log(xt+xt1-xgl-sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl
     . **2))-log(xt+xt1-xgl+sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))
     . )+4*log(xt-xt1-xgl+sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))*
     . xt**2-4*log(xt-xt1-xgl-sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2
     . ))*xt**2-(xt1-xt2)*log(-(xt-xt1+xgl+sqrt(-2*(xt+xt1)*xgl+(xt-
     . xt1)**2+xgl**2)))*xt1+(xt1-xt2)*log(-(xt-xt1+xgl-sqrt(-2*(xt+
     . xt1)*xgl+(xt-xt1)**2+xgl**2)))*xt1)*(xt-xt1+xgl)*xt2
      ans5=-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2)*(((xt1-xt2)*xt2-
     . 4*xt**2)*(log(xt+xt2-xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl
     . **2))-log(xt+xt2-xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))
     . )-4*log(xt-xt2-xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))*
     . xt**2+4*log(xt-xt2-xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2
     . ))*xt**2-(xt1-xt2)*log(-(xt-xt2+xgl+sqrt(-2*(xt+xt2)*xgl+(xt-
     . xt2)**2+xgl**2)))*xt2+(xt1-xt2)*log(-(xt-xt2+xgl-sqrt(-2*(xt+
     . xt2)*xgl+(xt-xt2)**2+xgl**2)))*xt2)*(xt-xt2+xgl)*xt1+ans6
      ans4=4*(xgl+xt-xt1)*(xgl-xt-xt1)*log(xt-xt1-xgl+sqrt(-2*(xt+xt1
     . )*xgl+(xt-xt1)**2+xgl**2))*xt**2*xt2+4*(xgl+xt-xt1)*(xgl-xt-
     . xt1)*log(xt-xt1-xgl-sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))*
     . xt**2*xt2+(xgl+xt-xt2)*(xgl-xt-xt2)*(xt1-xt2)*log(-(xt-xt2+xgl
     . +sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2)))*xt1*xt2+(xgl+xt-
     . xt2)*(xgl-xt-xt2)*(xt1-xt2)*log(-(xt-xt2+xgl-sqrt(-2*(xt+xt2)*
     . xgl+(xt-xt2)**2+xgl**2)))*xt1*xt2+(xgl+xt-xt1)*(xgl-xt-xt1)*(
     . xt1-xt2)*log(-(xt-xt1+xgl+sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl
     . **2)))*xt1*xt2+(xgl+xt-xt1)*(xgl-xt-xt1)*(xt1-xt2)*log(-(xt-
     . xt1+xgl-sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2)))*xt1*xt2+
     . ans5
      ans3=(2*((xt1+xt2-2*xt-2*xgl)*(xt1-xt2)+(xt1-xt2-8*xt)*log(xt2)
     . *xt2+(xt1-xt2+8*xt)*log(xt1)*xt1-6*(xt1-xt2)*log(xt)*xt-(xt1+
     . xt2+2*xt)*(xt1-xt2)*log(xgl))*xt*xt2+(xgl+xt-xt2)*(xgl-xt-xt2)
     . *(4*xt**2-xt1*xt2+xt2**2)*log(xt+xt2-xgl+sqrt(-2*(xt+xt2)*xgl+
     . (xt-xt2)**2+xgl**2))+(xgl+xt-xt2)*(xgl-xt-xt2)*(4*xt**2-xt1*
     . xt2+xt2**2)*log(xt+xt2-xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+
     . xgl**2)))*xt1-(xgl+xt-xt1)*(xgl-xt-xt1)*(4*xt**2+xt1**2-xt1*
     . xt2)*log(xt+xt1-xgl+sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))*
     . xt2-(xgl+xt-xt1)*(xgl-xt-xt1)*(4*xt**2+xt1**2-xt1*xt2)*log(xt+
     . xt1-xgl-sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))*xt2-4*(xgl+
     . xt-xt2)*(xgl-xt-xt2)*log(xt-xt2-xgl+sqrt(-2*(xt+xt2)*xgl+(xt-
     . xt2)**2+xgl**2))*xt**2*xt1-4*(xgl+xt-xt2)*(xgl-xt-xt2)*log(xt-
     . xt2-xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))*xt**2*xt1+
     . ans4
      ans7=((xt1-1)*log(xt2)*xt2-(xt2-1)*log(xt1)*xt1)
      ans2=ans3*ans7
      ans1=-ans2
      rat2=ans1/(16*(xt1-xt2)**2*(xt1-1)*(xt2-1)*xt**2*xt1*xt2)

      ans5=((log(-(xt-xt2+xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2
     . )))-log(xt+xt2-xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))+
     . log(-(xt-xt2+xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2)))-
     . log(xt+xt2-xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2)))*(xt+
     . xt2-xgl)*(xt-xt2+xgl)-2*(xt1+xt2-2*xgl)*xt+(log(-(xt-xt1+xgl-
     . sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2)))-log(xt+xt1-xgl+sqrt
     . (-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))+log(-(xt-xt1+xgl+sqrt(-2
     . *(xt+xt1)*xgl+(xt-xt1)**2+xgl**2)))-log(xt+xt1-xgl-sqrt(-2*(xt
     . +xt1)*xgl+(xt-xt1)**2+xgl**2)))*(xt+xt1-xgl)*(xt-xt1+xgl))*(
     . xt1-xt2)*log(xgl)
      ans4=sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2)*(log(xt+xt2-xgl-
     . sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))-log(xt+xt2-xgl+sqrt(
     . -2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))-log(-(xt-xt2+xgl+sqrt(-2*
     . (xt+xt2)*xgl+(xt-xt2)**2+xgl**2)))+log(-(xt-xt2+xgl-sqrt(-2*(
     . xt+xt2)*xgl+(xt-xt2)**2+xgl**2))))*(xt-xt2+xgl)*((xt1-1)*log(
     . xt2)*xt2-(xt2-1)*log(xt1)*xt1)+2*((log(xgl)-log(xt2))**2*(2*xt
     . -xt2)*(xt1-1)*xt2-2*(xt1-xt2)*log(xgl)**2*xt-(log(xgl)-log(xt1
     . ))**2*(2*xt-xt1)*(xt2-1)*xt1)*xt+sqrt(-2*(xt+xt1)*xgl+(xt-xt1)
     . **2+xgl**2)*(log(xt+xt1-xgl-sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+
     . xgl**2))-log(xt+xt1-xgl+sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**
     . 2))-log(-(xt-xt1+xgl+sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))
     . )+log(-(xt-xt1+xgl-sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))))
     . *(xt-xt1+xgl)*((xt1-1)*log(xt2)*xt2-(xt2-1)*log(xt1)*xt1)+ans5
      ans3=-ans4
      ans2=-(((log(-(xt-xt2+xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl
     . **2)))-log(xt+xt2-xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2)
     . )+log(-(xt-xt2+xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2)))-
     . log(xt+xt2-xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2)))*(xt+
     . xt2-xgl)*(xt-xt2+xgl)-2*(xt1+xt2-2*xgl)*xt+(log(-(xt-xt1+xgl-
     . sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2)))-log(xt+xt1-xgl+sqrt
     . (-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))+log(-(xt-xt1+xgl+sqrt(-2
     . *(xt+xt1)*xgl+(xt-xt1)**2+xgl**2)))-log(xt+xt1-xgl-sqrt(-2*(xt
     . +xt1)*xgl+(xt-xt1)**2+xgl**2)))*(xt+xt1-xgl)*(xt-xt1+xgl))*(
     . xt2-1)-2*((log(xgl)-log(xt2))*xt2-log(xgl))*(xt1-xt2)*xt)*(log
     . (xgl)-log(xt1))*xt1+ans3
      ans1=(((log(-(xt-xt2+xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**
     . 2)))-log(xt+xt2-xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))+
     . log(-(xt-xt2+xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2)))-
     . log(xt+xt2-xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2)))*(xt+
     . xt2-xgl)*(xt-xt2+xgl)-2*(xt1+xt2-2*xgl)*xt+(log(-(xt-xt1+xgl-
     . sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2)))-log(xt+xt1-xgl+sqrt
     . (-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))+log(-(xt-xt1+xgl+sqrt(-2
     . *(xt+xt1)*xgl+(xt-xt1)**2+xgl**2)))-log(xt+xt1-xgl-sqrt(-2*(xt
     . +xt1)*xgl+(xt-xt1)**2+xgl**2)))*(xt+xt1-xgl)*(xt-xt1+xgl))*(
     . xt1-1)-2*(xt1-xt2)*log(xgl)*xt)*(log(xgl)-log(xt2))*xt2+ans2
      rlt2=ans1/(8*(xt1-xt2)*(xt1-1)*(xt2-1)*xt**2)

      ans3=(2*(((log(xgl)-log(xt2))*(xt1-1)**2*xt2-(xt1-xt2)**2*log(
     . xgl)+(xt2+1-7*xt)*(xt2-1)*xt1)*xt1-(7*xt1**2-3*xt2-2*(xt2+1)*
     . xt1)*(xt2-1)*xgl)*xt1+(2*((2*(xt2+1)*xt1+3*xt2)*xt-2*xt1**3)*
     . xt1-(log(xt-xt1-xgl-sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))-
     . log(xt+xt1-xgl-sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))+log(
     . xt-xt1-xgl+sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))-log(xt+
     . xt1-xgl+sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2)))*(xt+xt1-xgl
     . )*(xt-xt1+xgl)*(xt1**2-xt2))*(xt2-1))*(log(xgl)-log(xt1))
      ans2=sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2)*(log(xt+xt1-xgl-
     . sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))-log(xt+xt1-xgl+sqrt(
     . -2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))+log(xt-xt1-xgl+sqrt(-2*(
     . xt+xt1)*xgl+(xt-xt1)**2+xgl**2))-log(xt-xt1-xgl-sqrt(-2*(xt+
     . xt1)*xgl+(xt-xt1)**2+xgl**2)))*((xt1**2-xt2)*(xt2-1)*log(xt1)-
     . (xt1-1)**2*log(xt2)*xt2-(xt1-xt2)*(xt1-1)*(xt2-1))*(xt-xt1+xgl
     . )+((log(xt-xt1-xgl-sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))-
     . log(xt+xt1-xgl-sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))+log(
     . xt-xt1-xgl+sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))-log(xt+
     . xt1-xgl+sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2)))*(xt+xt1-xgl
     . )*(xt-xt1+xgl)+2*(5*xt+xt1+5*xgl)*xt1)*((log(xgl)-log(xt2))*(
     . xt1-1)**2*xt2-(xt1-xt2)**2*log(xgl))+ans3
      ans1=2*(((log(xgl)-log(xt2))**2*(xt1-1)**2*xt2-(xt1-xt2)**2*log
     . (xgl)**2)*(xgl+xt)+(xt2+1-5*xt)*(xt2-1)*xt1**2)*xt1-(log(xt-
     . xt1-xgl-sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))-log(xt+xt1-
     . xgl-sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))+log(xt-xt1-xgl+
     . sqrt(-2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2))-log(xt+xt1-xgl+sqrt(
     . -2*(xt+xt1)*xgl+(xt-xt1)**2+xgl**2)))*(xt+xt1-xgl)*(xt-xt1+xgl
     . )*(xt1-xt2)*(xt1-1)*(xt2-1)-2*(xt+xt1+xgl)*(log(xgl)-log(xt1))
     . **2*(xt1**2-xt2)*(xt2-1)*xt1-2*(5*xt*xt2+xt1**3+5*(xt1-xt2)*(
     . xt1-1)*xgl-(5*(xt2+1)*xt-xt2)*xt1)*(xt2-1)*xt1-2*((log(xgl)-
     . log(xt1))*(xt1**2-xt2)*(xt2-1)-(log(xgl)-log(xt2))*(xt1-1)**2*
     . xt2+((xt1-xt2)*log(xgl)+(xt1-1)*(xt2-1))*(xt1-xt2))*(log(xgl)-
     . log(xt))*xt*xt1+ans2
      rmt12=ans1/(4*(xt1-xt2)**2*(xt1-1)**2*(xt2-1)*xt1)

      ans3=((log(xt-xt2-xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))
     . -log(xt+xt2-xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))+log(
     . xt-xt2-xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))-log(xt+
     . xt2-xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2)))*(xt+xt2-xgl
     . )*(xt-xt2+xgl)+2*(log(xgl)-log(xt2))*xt2**2+2*(5*xt+xt2+5*xgl)
     . *xt2)*(log(xgl)-log(xt1))*(xt2-1)**2*xt1+(2*(((2*xt2+3)*xt+xt2
     . **2)*xt1**2-(xt1-xt2)**2*log(xgl)*xt2-((7*xt2**2+3)*xt+2*xt2**
     . 3)*xt1)*xt2+(log(xt-xt2-xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+
     . xgl**2))-log(xt+xt2-xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**
     . 2))+log(xt-xt2-xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))-
     . log(xt+xt2-xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2)))*(xt+
     . xt2-xgl)*(xt-xt2+xgl)*(xt1-xt2**2)*(xt1-1)+2*(((7*xt-1)*xt2-2*
     . (xt-xt2**2))*xt2-((7*xt2-2)*xt2-(2*xt2+3)*xt1)*(xt1-1)*xgl)*
     . xt2)*(log(xgl)-log(xt2))
      ans2=-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2)*(log(xt+xt2-xgl-
     . sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))-log(xt+xt2-xgl+sqrt(
     . -2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))+log(xt-xt2-xgl+sqrt(-2*(
     . xt+xt2)*xgl+(xt-xt2)**2+xgl**2))-log(xt-xt2-xgl-sqrt(-2*(xt+
     . xt2)*xgl+(xt-xt2)**2+xgl**2)))*((xt1-xt2**2)*(xt1-1)*log(xt2)+
     . (xt2-1)**2*log(xt1)*xt1-(xt1-xt2)*(xt1-1)*(xt2-1))*(xt-xt2+xgl
     . )-((log(xt-xt2-xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))-
     . log(xt+xt2-xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))+log(
     . xt-xt2-xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))-log(xt+
     . xt2-xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2)))*(xt+xt2-xgl
     . )*(xt-xt2+xgl)+2*(5*xt+xt2+5*xgl)*xt2)*(xt1-xt2)**2*log(xgl)+
     . ans3
      ans1=(log(xt-xt2-xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))-
     . log(xt+xt2-xgl-sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))+log(
     . xt-xt2-xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2))-log(xt+
     . xt2-xgl+sqrt(-2*(xt+xt2)*xgl+(xt-xt2)**2+xgl**2)))*(xt+xt2-xgl
     . )*(xt-xt2+xgl)*(xt1-xt2)*(xt1-1)*(xt2-1)+2*((log(xgl)-log(xt1)
     . )**2*(xt2-1)**2*xt1-(xt1-xt2)**2*log(xgl)**2)*(xgl+xt)*xt2+2*(
     . xt+xt2+xgl)*(log(xgl)-log(xt2))**2*(xt1-xt2**2)*(xt1-1)*xt2+2*
     . (5*xt+xt2+5*xgl)*(xt1-xt2)*(xt1-1)*(xt2-1)*xt2+2*((log(xgl)-
     . log(xt1))*(xt2-1)**2*xt1+(log(xgl)-log(xt2))*(xt1-xt2**2)*(xt1
     . -1)-((xt1-xt2)*log(xgl)-(xt1-1)*(xt2-1))*(xt1-xt2))*(log(xgl)-
     . log(xt))*xt*xt2+ans2
      rmt22=ans1/(4*(xt1-xt2)**2*(xt1-1)*(xt2-1)**2*xt2)

c     relw = r22+r42+r52+r72+r82+r92+rat2+rlt2+rmt12+rmt22
      relw = r22+r42+r52+r72+r82+r92+rlt2+rmt12+rmt22
      bo  = fi(amst1**2,amst2**2,amu**2)
      relw = cf*relw/bo

      anomalous =-cf
      finscale = 2*dlog(scale**2/amg**2)
      felw_hdec = dreal(relw)*fnorm + anomalous + finscale

c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
c     write(6,*)'dat: ',dreal(cf*rat2/bo)*fnorm
c     write(6,*)'tot: ',felw_hdec
c     write(6,*)
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
c     ff = fnorm*cf/bo
c     write(6,*)
c     write(6,*)'ind: ',dreal(ff*r22),dreal(ff*r42),
c    . dreal(ff*r52),dreal(ff*r72),dreal(ff*r82),
c    . dreal(ff*r92),dreal(ff*rlt2),dreal(ff*rmt12),
c    . dreal(ff*rmt22),dreal(relw/amu**2)
c     write(6,*)'     ',-1/4.d0,3/4.d0,-1/2.d0,-1/12.d0,-1/3.d0,1/6.d0,
c    .       (5+3*dlog(amg**2/amt**2))/8,0.d0,1/2.d0,1/2.d0
c     write(6,*)
c     write(6,*)'dat: ',dreal(cf*rat2/bo)*fnorm
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

      return
      end
 
c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 
      double precision function fqcd_hdec(scale,amt,amg,amsb1,amsb2,
     .                         amst1,amst2,amsu1,amsu2,amsd1,amsd2,xxt)
      implicit double precision (b-h,o-q,s-z), complex*16 (a,r)
      double precision amt,amg,amsb1,amsb2,amst1,amst2,
     .                 amsu1,amsu2,amsd1,amsd2
      double precision mt,mg,mb1,mb2,mt1,mt2,ms1,ms2,mu
      complex*16 sp,li2_hdec,xt,xgl,xt1,xt2,xb1,xb2,xs1,xs2,xq
      double precision m,mq
      double precision anomalous
      double precision a
      complex*16 xp,xm
      sp(r) = li2_hdec(r)
      xp(m) = (amg**2+amt**2-m**2)/2/amg**2/rim
     . +cdsqrt(((amg**2+amt**2-m**2)/2/amg**2/rim)**2-amt**2/amg**2/rim)
      xm(m) = (amg**2+amt**2-m**2)/2/amg**2/rim
     . -cdsqrt(((amg**2+amt**2-m**2)/2/amg**2/rim)**2-amt**2/amg**2/rim)
      fi(a,b,c) = (a*b*log(a/b)+b*c*log(b/c)+c*a*log(c/a))
     .          / (a-b)/(b-c)/(a-c)
      t134p(a,b,c)  = t134p_hdec(a,b,c)
      t134(a,b,c,d) = t134_hdec(a,b,c,d)

      eps = 1.d-15
      pi = 4*datan(1.d0)
      zeta2 = pi**2/6

      ca = 3
      cf = 4/3.d0
      tr = 1/2.d0
      nu = 2
      nd = 2
      nf = nu+nd+1

      fnorm = 4/amg**2

      rim = dcmplx(1.d0,eps)

      mq  = amt
      mt  = amt
      mg  = amg
      mu  = amg
      mt1 = amsb1
      mt2 = amsb2
      mb1 = amsb1
      mb2 = amsb2

      xq  = amt**2/amg**2   * rim
      xt  = amt**2/amg**2   * rim
      xgl = amg**2/amg**2   * rim
      xt1 = amsb1**2/amg**2 * rim
      xt2 = amsb2**2/amg**2 * rim
      xb1 = amsb1**2/amg**2 * rim
      xb2 = amsb2**2/amg**2 * rim

c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
c--comparison with luminita
c     amsu1 =  998.540d0
c     amsu2 =  999.385d0
c     amsd1 = 1001.770d0
c     amsd2 = 1001.310d0
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

      r12=(log(xb1)**2*xb1*(-2*xb1*xb2**2+4*xb1*xb2-2*xb1+xb2**2-2*
     . xb2+1)+4*log(xb1)*xb1*(xb1*xb2**2-2*xb1*xb2+xb1-xb2**2+2*xb2-1
     . )+log(xb2)**2*xb2*(2*xb1**2*xb2-xb1**2-4*xb1*xb2+2*xb1+2*xb2-1
     . )+4*log(xb2)*xb2*(-xb1**2*xb2+xb1**2+2*xb1*xb2-2*xb1-xb2+1)+4*
     . t134p(mb1,mb1,mg)*xb1*(xb2**2-2*xb2+1)+4*t134p(mb1,mg,mg)*(-
     . xb1*xb2**2+2*xb1*xb2-xb1-xb2**2+2*xb2-1)+4*t134p(mb2,mb2,mg)*
     . xb2*(-xb1**2+2*xb1-1)+4*t134p(mb2,mg,mg)*(xb1**2*xb2+xb1**2-2*
     . xb1*xb2-2*xb1+xb2+1)+4*t134p(mg,mg,mg)*(-xb1**2+2*xb1+xb2**2-2
     . *xb2))/(16*(xb1**3*xb2**2-2*xb1**3*xb2+xb1**3-xb1**2*xb2**3+3*
     . xb1**2*xb2-2*xb1**2+2*xb1*xb2**3-3*xb1*xb2**2+xb1-xb2**3+2*xb2
     . **2-xb2))

      r22=(4*log(xgl)**2*(-xt1**2*xt2+xt1*xt2**2+xt1-xt2)+4*log(xgl)*
     . log(xt1)*xt1*(-xt2**2+2*xt2-1)+4*log(xgl)*log(xt2)*xt2*(xt1**2
     . -2*xt1+1)+12*log(xgl)*(-xt1**2*xt2+xt1*xt2**2+xt1-xt2)+log(xt1
     . )**2*xt1*(xt2**2-2*xt2+1)+2*log(xt1)*xt1*(-xt1*xt2**2+2*xt1*
     . xt2-xt1-2*xt2**2+4*xt2-2)+log(xt2)**2*xt2*(-xt1**2+2*xt1-1)+2*
     . log(xt2)*xt2*(xt1**2*xt2+2*xt1**2-2*xt1*xt2-4*xt1+xt2+2)+t134p
     . (mu,mt1,mg)*xgl*(-xt1*xt2**2+2*xt1*xt2-xt1-xt2**2+2*xt2-1)+
     . t134p(mu,mt2,mg)*xgl*(xt1**2*xt2+xt1**2-2*xt1*xt2-2*xt1+xt2+1)
     . +14*(-xt1**2*xt2+xt1*xt2**2+xt1-xt2))/(2*(xt1**3*xt2**2-2*xt1
     . **3*xt2+xt1**3-xt1**2*xt2**3+3*xt1**2*xt2-2*xt1**2+2*xt1*xt2**
     . 3-3*xt1*xt2**2+xt1-xt2**3+2*xt2**2-xt2))

      r32=(log(xb1)**2*xb1*(-xb2**2+2*xb2-1)+2*log(xb1)*xb1*(2*xb1*
     . xb2**2-4*xb1*xb2+2*xb1+xb2**2-2*xb2+1)+log(xb2)**2*xb2*(xb1**2
     . -2*xb1+1)+2*log(xb2)*xb2*(-2*xb1**2*xb2-xb1**2+4*xb1*xb2+2*xb1
     . -2*xb2-1)+2*t134p(mb1,mg,mg)*(2*xb1*xb2**2-4*xb1*xb2+2*xb1-xb2
     . **2+2*xb2-1)+2*t134p(mb2,mg,mg)*(-2*xb1**2*xb2+xb1**2+4*xb1*
     . xb2-2*xb1-2*xb2+1)+3*t134p(mg,mg,mg)*(xb1**2*xb2-xb1**2-xb1*
     . xb2**2+xb1+xb2**2-xb2)+14*(xb1**2*xb2-xb1*xb2**2-xb1+xb2))/(8*
     . (xb1**3*xb2**2-2*xb1**3*xb2+xb1**3-xb1**2*xb2**3+3*xb1**2*xb2-
     . 2*xb1**2+2*xb1*xb2**3-3*xb1*xb2**2+xb1-xb2**3+2*xb2**2-xb2))

      r42=(8*log(xgl)**2*(xt1**2*xt2-xt1*xt2**2-xt1+xt2)+8*log(xgl)*
     . log(xt1)*xt1*(xt2**2-2*xt2+1)+8*log(xgl)*log(xt2)*xt2*(-xt1**2
     . +2*xt1-1)+24*log(xgl)*(xt1**2*xt2-xt1*xt2**2-xt1+xt2)+2*log(
     . xt1)**2*xt1*(-xt2**2+2*xt2-1)+log(xt1)*xt1*(5*xt1*xt2**2-10*
     . xt1*xt2+5*xt1+7*xt2**2-14*xt2+7)+2*log(xt2)**2*xt2*(xt1**2-2*
     . xt1+1)+log(xt2)*xt2*(-5*xt1**2*xt2-7*xt1**2+10*xt1*xt2+14*xt1-
     . 5*xt2-7)+2*t134p(mt1,mu,mg)*xgl*(xt1*xt2**2-2*xt1*xt2+xt1+xt2
     . **2-2*xt2+1)+2*t134p(mt2,mu,mg)*xgl*(-xt1**2*xt2-xt1**2+2*xt1*
     . xt2+2*xt1-xt2-1)+28*(xt1**2*xt2-xt1*xt2**2-xt1+xt2))/(2*(xt1**
     . 3*xt2**2-2*xt1**3*xt2+xt1**3-xt1**2*xt2**3+3*xt1**2*xt2-2*xt1
     . **2+2*xt1*xt2**3-3*xt1*xt2**2+xt1-xt2**3+2*xt2**2-xt2))

      r52=(log(xb1)**2*xb1*(2*xb1*xb2**2-4*xb1*xb2+2*xb1-xb2**2+2*xb2
     . -1)+4*log(xb1)*xb1*(-xb1*xb2**2+2*xb1*xb2-xb1+xb2**2-2*xb2+1)+
     . log(xb2)**2*xb2*(-2*xb1**2*xb2+xb1**2+4*xb1*xb2-2*xb1-2*xb2+1)
     . +4*log(xb2)*xb2*(xb1**2*xb2-xb1**2-2*xb1*xb2+2*xb1+xb2-1)+2*
     . t134p(mb1,mb2,mg)*(xb1**2*xb2-xb1**2-xb1*xb2**2+xb1+xb2**2-xb2
     . )+2*t134p(mb1,mg,mg)*(-xb1**2*xb2+xb1**2+2*xb1*xb2-2*xb1-xb2+1
     . )+2*t134p(mb2,mg,mg)*(xb1*xb2**2-2*xb1*xb2+xb1-xb2**2+2*xb2-1)
     . )/(16*(xb1**3*xb2**2-2*xb1**3*xb2+xb1**3-xb1**2*xb2**3+3*xb1**
     . 2*xb2-2*xb1**2+2*xb1*xb2**3-3*xb1*xb2**2+xb1-xb2**3+2*xb2**2-
     . xb2))

      r62=(log(xb1)**2*xb1*(xb2**2-2*xb2+1)+2*log(xb1)*xb1*(-xb2**2+2
     . *xb2-1)+log(xb2)**2*xb2*(-xb1**2+2*xb1-1)+2*log(xb2)*xb2*(xb1
     . **2-2*xb1+1)+2*t134p(mb1,mg,mg)*(xb1*xb2**2-2*xb1*xb2+xb1+xb2
     . **2-2*xb2+1)+2*t134p(mb2,mg,mg)*(-xb1**2*xb2-xb1**2+2*xb1*xb2+
     . 2*xb1-xb2-1)+2*t134p(mg,mg,mg)*(xb1**2*xb2+xb1**2-xb1*xb2**2-3
     . *xb1-xb2**2+3*xb2))/(8*(xb1**3*xb2**2-2*xb1**3*xb2+xb1**3-xb1
     . **2*xb2**3+3*xb1**2*xb2-2*xb1**2+2*xb1*xb2**3-3*xb1*xb2**2+xb1
     . -xb2**3+2*xb2**2-xb2))

      ans1=8*log(xgl)**2*(xt1**2*xt2-xt1**2-xt1*xt2**2+xt1+xt2**2-xt2
     . )+4*log(xgl)*log(xt1)*xt1*(4*xt1*xt2**2-8*xt1*xt2+4*xt1-3*xt2
     . **2+6*xt2-3)+4*log(xgl)*log(xt2)*xt2*(-4*xt1**2*xt2+3*xt1**2+8
     . *xt1*xt2-6*xt1-4*xt2+3)+12*log(xgl)*(xt1**2*xt2-xt1**2-xt1*xt2
     . **2+xt1+xt2**2-xt2)+log(xt1)**2*xt1*(-8*xt1*xt2**2+16*xt1*xt2-
     . 8*xt1+5*xt2**2-10*xt2+5)+4*log(xt1)*xt1*(3*xt1*xt2**2-6*xt1*
     . xt2+3*xt1-2*xt2**2+4*xt2-2)+log(xt2)**2*xt2*(8*xt1**2*xt2-5*
     . xt1**2-16*xt1*xt2+10*xt1+8*xt2-5)+4*log(xt2)*xt2*(-3*xt1**2*
     . xt2+2*xt1**2+6*xt1*xt2-4*xt1-3*xt2+2)+4*t134p(mt1,mt1,mg)*xgl*
     . (xt1*xt2**2-2*xt1*xt2+xt1+xt2**2-2*xt2+1)+4*t134p(mt2,mt2,mg)*
     . xgl*(-xt1**2*xt2-xt1**2+2*xt1*xt2+2*xt1-xt2-1)+4*t134p(mu,mt1,
     . mg)*xgl*(-xt1*xt2**2+2*xt1*xt2-xt1-xt2**2+2*xt2-1)+4*t134p(mu,
     . mt2,mg)*xgl*(xt1**2*xt2+xt1**2-2*xt1*xt2-2*xt1+xt2+1)+8*(xt1**
     . 2*xt2-xt1**2-xt1*xt2**2+xt1+xt2**2-xt2)
      r72=ans1/(8*(xt1**3*xt2**2-2*xt1**3*xt2+xt1**3-xt1**2*xt2**3+3*
     . xt1**2*xt2-2*xt1**2+2*xt1*xt2**3-3*xt1*xt2**2+xt1-xt2**3+2*xt2
     . **2-xt2))

      r82=(log(xb1)**2*(xb1*xb2**2-2*xb1*xb2+xb1-2*xb2**2+4*xb2-2)+4*
     . log(xb1)*(-xb1**2*xb2**2+2*xb1**2*xb2-xb1**2+xb1*xb2**2-2*xb1*
     . xb2+xb1+xb2**2-2*xb2+1)+log(xb2)**2*(-xb1**2*xb2+2*xb1**2+2*
     . xb1*xb2-4*xb1-xb2+2)+4*log(xb2)*(xb1**2*xb2**2-xb1**2*xb2-xb1
     . **2-2*xb1*xb2**2+2*xb1*xb2+2*xb1+xb2**2-xb2-1)+2*t134p(mb1,mg,
     . mg)*(-xb1*xb2**2+2*xb1*xb2-xb1+xb2**2-2*xb2+1)+2*t134p(mb2,mg,
     . mg)*(xb1**2*xb2-xb1**2-2*xb1*xb2+2*xb1+xb2-1)+10*(-xb1**2*xb2+
     . xb1**2+xb1*xb2**2-xb1-xb2**2+xb2))/(8*(xb1**3*xb2**2-2*xb1**3*
     . xb2+xb1**3-xb1**2*xb2**3+3*xb1**2*xb2-2*xb1**2+2*xb1*xb2**3-3*
     . xb1*xb2**2+xb1-xb2**3+2*xb2**2-xb2))

      ans2=4*log(xt2)*xt2*(-3*xt1**3*xt2+2*xt1**3+3*xt1**2*xt2**2+4*
     . xt1**2*xt2-4*xt1**2-6*xt1*xt2**2+xt1*xt2+2*xt1+3*xt2**2-2*xt2)
     . +4*(xt1**3*xt2-xt1**3-2*xt1**2*xt2**2+xt1**2*xt2+xt1**2+xt1*
     . xt2**3+xt1*xt2**2-2*xt1*xt2-xt2**3+xt2**2)
      ans1=4*log(xgl)*log(xt1)*xt1*(2*xt1**2*xt2**2-4*xt1**2*xt2+2*
     . xt1**2-2*xt1*xt2**3+3*xt1*xt2**2-xt1+xt2**3-2*xt2**2+xt2)+4*
     . log(xgl)*log(xt2)*xt2*(-2*xt1**3*xt2+xt1**3+2*xt1**2*xt2**2+3*
     . xt1**2*xt2-2*xt1**2-4*xt1*xt2**2+xt1+2*xt2**2-xt2)+4*log(xgl)*
     . (xt1**3*xt2-xt1**3-2*xt1**2*xt2**2+xt1**2*xt2+xt1**2+xt1*xt2**
     . 3+xt1*xt2**2-2*xt1*xt2-xt2**3+xt2**2)+log(xt1)**2*xt1*(-6*xt1
     . **2*xt2**2+12*xt1**2*xt2-6*xt1**2+2*xt1*xt2**3-xt1*xt2**2-4*
     . xt1*xt2+3*xt1+xt2**3-2*xt2**2+xt2)+4*log(xt1)*log(xt2)*xt1*xt2
     . *(xt1**2*xt2-xt1**2+xt1*xt2**2-4*xt1*xt2+3*xt1-xt2**2+3*xt2-2)
     . +4*log(xt1)*xt1*(3*xt1**2*xt2**2-6*xt1**2*xt2+3*xt1**2-3*xt1*
     . xt2**3+4*xt1*xt2**2+xt1*xt2-2*xt1+2*xt2**3-4*xt2**2+2*xt2)+log
     . (xt2)**2*xt2*(2*xt1**3*xt2+xt1**3-6*xt1**2*xt2**2-xt1**2*xt2-2
     . *xt1**2+12*xt1*xt2**2-4*xt1*xt2+xt1-6*xt2**2+3*xt2)+ans2
      r92=ans1/(8*(xt1**4*xt2**2-2*xt1**4*xt2+xt1**4-2*xt1**3*xt2**3+
     . 2*xt1**3*xt2**2+2*xt1**3*xt2-2*xt1**3+xt1**2*xt2**4+2*xt1**2*
     . xt2**3-6*xt1**2*xt2**2+2*xt1**2*xt2+xt1**2-2*xt1*xt2**4+2*xt1*
     . xt2**3+2*xt1*xt2**2-2*xt1*xt2+xt2**4-2*xt2**3+xt2**2))

      mt1 = amst1
      mt2 = amst2
      xt1 = amst1**2/amg**2 * rim
      xt2 = amst2**2/amg**2 * rim

      ralsca2=(-((9*log(xb1)-10)*(xb2-1)*log(xb1)*xb1-(9*log(xb2)-10)
     . *(xb1-1)*log(xb2)*xb2))/(48*(xb1-xb2)*(xb1-1)*(xb2-1))

      ralscf2=(-((xb1-1)*log(xb2)*xb2-(xb2-1)*log(xb1)*xb1))/(8*(xb1-
     . xb2)*(xb1-1)*(xb2-1))

      rmb12=(-((((2*xb1**3-3*xb2-(xb2-6)*xb1**2-2*(xb2+1)*xb1)*xb1+(
     . xb1**2-xb2)*(xb1-1)**2*log(-(xb1-1)))*(xb2-1)+(xb1-1)**2*log(
     . xb2)*xb1**2*xb2)*log(xb1)-(((xb1**2-xb2)*(xb1+1)*(xb2-1)*log(
     . xb1)**2-(xb1-1)**2*log(xb2)**2*xb2)*xb1+((xb1-xb2)*(xb2-1)+(
     . xb1-1)*log(xb2)*xb2)*((xb1+5)*xb1+(xb1-1)**2*log(-(xb1-1)))*(
     . xb1-1))))/(4*(xb1-xb2)**2*(xb1-1)**2*(xb2-1)*xb1)

      rmb22=(-(((xb1-xb2**2)*(xb1-1)*(xb2+1)*log(xb2)**2+(xb2-1)**2*
     . log(xb1)**2*xb1)*xb2+((xb2+5)*xb2+(xb2-1)**2*log(-(xb2-1)))*(
     . xb1-xb2)*(xb1-1)*(xb2-1)-((xb2-1)**2*log(-(xb2-1))-log(xb2)*
     . xb2**2+(xb2+5)*xb2)*(xb2-1)**2*log(xb1)*xb1+((2*(xb2**2+3*xb2-
     . 1)*xb2-(xb2**2+2*xb2+3)*xb1)*xb2-(xb1-xb2**2)*(xb2-1)**2*log(-
     . (xb2-1)))*(xb1-1)*log(xb2)))/(4*(xb1-xb2)**2*(xb1-1)*(xb2-1)**
     . 2*xb2)

      rmgca2=(-((3*log(xb1)-14)*(xb1+1)*(xb2-1)**2*log(xb1)*xb1-(3*
     . log(xb2)-14)*(xb1-1)**2*(xb2+1)*log(xb2)*xb2-28*(xb1-xb2)*(xb1
     . -1)*(xb2-1)))/(16*(xb1-xb2)*(xb1-1)**2*(xb2-1)**2)

      ms1 = amsu1
      ms2 = amsu2
      xs1 = amsu1**2/amg**2 * rim
      xs2 = amsu2**2/amg**2 * rim

      ans2=2*t134p(mb2,ms1,mg)*(xb1**2*xb2-xb1**2*xs1-2*xb1*xb2+2*xb1
     . *xs1+xb2-xs1)+2*t134p(mb2,ms2,mg)*(xb1**2*xb2-xb1**2*xs2-2*xb1
     . *xb2+2*xb1*xs2+xb2-xs2)+2*t134p(mg,ms1,mg)*(-2*xb1**2*xb2+xb1
     . **2*xs1+xb1**2+2*xb1*xb2**2-2*xb1*xs1-xb2**2*xs1-xb2**2+2*xb2*
     . xs1)+2*t134p(mg,ms2,mg)*(-2*xb1**2*xb2+xb1**2*xs2+xb1**2+2*xb1
     . *xb2**2-2*xb1*xs2-xb2**2*xs2-xb2**2+2*xb2*xs2)+12*(xb1**2*xb2*
     . xs1+xb1**2*xb2*xs2+xb1**2*xb2-xb1**2*xs1-xb1**2*xs2-xb1**2-xb1
     . *xb2**2*xs1-xb1*xb2**2*xs2-xb1*xb2**2+xb1*xs1+xb1*xs2+xb1+xb2
     . **2*xs1+xb2**2*xs2+xb2**2-xb2*xs1-xb2*xs2-xb2)
      ans1=log(xb1)**2*xb1*(-xb2**2*xs1-xb2**2*xs2+2*xb2*xs1+2*xb2*
     . xs2-xs1-xs2)+2*log(xb1)*log(xs1)*xb1*xs1*(-xb2**2+2*xb2-1)+2*
     . log(xb1)*log(xs2)*xb1*xs2*(-xb2**2+2*xb2-1)+4*log(xb1)*xb1*(
     . xb2**2*xs1+xb2**2*xs2-2*xb2*xs1-2*xb2*xs2+xs1+xs2)+log(xb2)**2
     . *xb2*(xb1**2*xs1+xb1**2*xs2-2*xb1*xs1-2*xb1*xs2+xs1+xs2)+2*log
     . (xb2)*log(xs1)*xb2*xs1*(xb1**2-2*xb1+1)+2*log(xb2)*log(xs2)*
     . xb2*xs2*(xb1**2-2*xb1+1)+4*log(xb2)*xb2*(-xb1**2*xs1-xb1**2*
     . xs2+2*xb1*xs1+2*xb1*xs2-xs1-xs2)+log(xs1)**2*xs1*(xb1**2*xb2-
     . xb1**2-xb1*xb2**2+xb1+xb2**2-xb2)+8*log(xs1)*xs1*(-xb1**2*xb2+
     . xb1**2+xb1*xb2**2-xb1-xb2**2+xb2)+log(xs2)**2*xs2*(xb1**2*xb2-
     . xb1**2-xb1*xb2**2+xb1+xb2**2-xb2)+8*log(xs2)*xs2*(-xb1**2*xb2+
     . xb1**2+xb1*xb2**2-xb1-xb2**2+xb2)+2*t134p(mb1,ms1,mg)*(-xb1*
     . xb2**2+2*xb1*xb2-xb1+xb2**2*xs1-2*xb2*xs1+xs1)+2*t134p(mb1,ms2
     . ,mg)*(-xb1*xb2**2+2*xb1*xb2-xb1+xb2**2*xs2-2*xb2*xs2+xs2)+ans2
      ru102=ans1/(8*(xb1**3*xb2**2-2*xb1**3*xb2+xb1**3-xb1**2*xb2**3+3
     . *xb1**2*xb2-2*xb1**2+2*xb1*xb2**3-3*xb1*xb2**2+xb1-xb2**3+2*
     . xb2**2-xb2))

      rualstr2=(-((log(xs2)-6+log(xs1))*((xb1-1)*log(xb2)*xb2-(xb2-1)*
     . log(xb1)*xb1)+3*((xb1-1)*log(xb2)**2*xb2-(xb2-1)*log(xb1)**2*
     . xb1)))/(24*(xb1-xb2)*(xb1-1)*(xb2-1))

      rumgtr2=((xs2-6+xs1+log(xs2)+log(xs1)+(log(xs2-1)-log(xs2))*(xs2
     . -1)**2+(log(xs1-1)-log(xs1))*(xs1-1)**2)*((xb1+1)*(xb2-1)**2*
     . log(xb1)*xb1-(xb1-1)**2*(xb2+1)*log(xb2)*xb2)+2*((log(xs2-1)-
     . log(xs2))*(xs2-1)**2+log(xs1)+log(xs2)+(log(xs1-1)-log(xs1))*(
     . xs1-1)**2)*(xb1-xb2)*(xb1-1)*(xb2-1)+(xb1+1)*(xb2-1)**2*log(
     . xb1)**2*xb1-(xb1-1)**2*(xb2+1)*log(xb2)**2*xb2+2*(xs2-6+xs1)*(
     . xb1-xb2)*(xb1-1)*(xb2-1))/(8*(xb1-xb2)*(xb1-1)**2*(xb2-1)**2)

      ms1 = amsd1
      ms2 = amsd2
      xs1 = amsd1**2/amg**2 * rim
      xs2 = amsd2**2/amg**2 * rim

      ans2=2*t134p(mb2,ms1,mg)*(xb1**2*xb2-xb1**2*xs1-2*xb1*xb2+2*xb1
     . *xs1+xb2-xs1)+2*t134p(mb2,ms2,mg)*(xb1**2*xb2-xb1**2*xs2-2*xb1
     . *xb2+2*xb1*xs2+xb2-xs2)+2*t134p(mg,ms1,mg)*(-2*xb1**2*xb2+xb1
     . **2*xs1+xb1**2+2*xb1*xb2**2-2*xb1*xs1-xb2**2*xs1-xb2**2+2*xb2*
     . xs1)+2*t134p(mg,ms2,mg)*(-2*xb1**2*xb2+xb1**2*xs2+xb1**2+2*xb1
     . *xb2**2-2*xb1*xs2-xb2**2*xs2-xb2**2+2*xb2*xs2)+12*(xb1**2*xb2*
     . xs1+xb1**2*xb2*xs2+xb1**2*xb2-xb1**2*xs1-xb1**2*xs2-xb1**2-xb1
     . *xb2**2*xs1-xb1*xb2**2*xs2-xb1*xb2**2+xb1*xs1+xb1*xs2+xb1+xb2
     . **2*xs1+xb2**2*xs2+xb2**2-xb2*xs1-xb2*xs2-xb2)
      ans1=log(xb1)**2*xb1*(-xb2**2*xs1-xb2**2*xs2+2*xb2*xs1+2*xb2*
     . xs2-xs1-xs2)+2*log(xb1)*log(xs1)*xb1*xs1*(-xb2**2+2*xb2-1)+2*
     . log(xb1)*log(xs2)*xb1*xs2*(-xb2**2+2*xb2-1)+4*log(xb1)*xb1*(
     . xb2**2*xs1+xb2**2*xs2-2*xb2*xs1-2*xb2*xs2+xs1+xs2)+log(xb2)**2
     . *xb2*(xb1**2*xs1+xb1**2*xs2-2*xb1*xs1-2*xb1*xs2+xs1+xs2)+2*log
     . (xb2)*log(xs1)*xb2*xs1*(xb1**2-2*xb1+1)+2*log(xb2)*log(xs2)*
     . xb2*xs2*(xb1**2-2*xb1+1)+4*log(xb2)*xb2*(-xb1**2*xs1-xb1**2*
     . xs2+2*xb1*xs1+2*xb1*xs2-xs1-xs2)+log(xs1)**2*xs1*(xb1**2*xb2-
     . xb1**2-xb1*xb2**2+xb1+xb2**2-xb2)+8*log(xs1)*xs1*(-xb1**2*xb2+
     . xb1**2+xb1*xb2**2-xb1-xb2**2+xb2)+log(xs2)**2*xs2*(xb1**2*xb2-
     . xb1**2-xb1*xb2**2+xb1+xb2**2-xb2)+8*log(xs2)*xs2*(-xb1**2*xb2+
     . xb1**2+xb1*xb2**2-xb1-xb2**2+xb2)+2*t134p(mb1,ms1,mg)*(-xb1*
     . xb2**2+2*xb1*xb2-xb1+xb2**2*xs1-2*xb2*xs1+xs1)+2*t134p(mb1,ms2
     . ,mg)*(-xb1*xb2**2+2*xb1*xb2-xb1+xb2**2*xs2-2*xb2*xs2+xs2)+ans2
      rd102=ans1/(8*(xb1**3*xb2**2-2*xb1**3*xb2+xb1**3-xb1**2*xb2**3+3
     . *xb1**2*xb2-2*xb1**2+2*xb1*xb2**3-3*xb1*xb2**2+xb1-xb2**3+2*
     . xb2**2-xb2))

      rdalstr2=(-((log(xs2)-6+log(xs1))*((xb1-1)*log(xb2)*xb2-(xb2-1)*
     . log(xb1)*xb1)+3*((xb1-1)*log(xb2)**2*xb2-(xb2-1)*log(xb1)**2*
     . xb1)))/(24*(xb1-xb2)*(xb1-1)*(xb2-1))

      rdmgtr2=((xs2-6+xs1+log(xs2)+log(xs1)+(log(xs2-1)-log(xs2))*(xs2
     . -1)**2+(log(xs1-1)-log(xs1))*(xs1-1)**2)*((xb1+1)*(xb2-1)**2*
     . log(xb1)*xb1-(xb1-1)**2*(xb2+1)*log(xb2)*xb2)+2*((log(xs2-1)-
     . log(xs2))*(xs2-1)**2+log(xs1)+log(xs2)+(log(xs1-1)-log(xs1))*(
     . xs1-1)**2)*(xb1-xb2)*(xb1-1)*(xb2-1)+(xb1+1)*(xb2-1)**2*log(
     . xb1)**2*xb1-(xb1-1)**2*(xb2+1)*log(xb2)**2*xb2+2*(xs2-6+xs1)*(
     . xb1-xb2)*(xb1-1)*(xb2-1))/(8*(xb1-xb2)*(xb1-1)**2*(xb2-1)**2)

      ms1 = amsb1
      ms2 = amsb2
      xs1 = amsb1**2/amg**2 * rim
      xs2 = amsb2**2/amg**2 * rim

      ans1=log(xb1)**2*xb1*(xb1**2*xb2-xb1**2-4*xb1*xb2**2+6*xb1*xb2-
     . 2*xb1-xb2**3+3*xb2**2-2*xb2)+2*log(xb1)*log(xb2)*xb1*xb2*(xb1
     . **2-2*xb1-xb2**2+2*xb2)+4*log(xb1)*xb1*(-2*xb1**2*xb2+2*xb1**2
     . +3*xb1*xb2**2-2*xb1*xb2-xb1+xb2**3-4*xb2**2+3*xb2)+log(xb2)**2
     . *xb2*(xb1**3+4*xb1**2*xb2-3*xb1**2-xb1*xb2**2-6*xb1*xb2+2*xb1+
     . xb2**2+2*xb2)+4*log(xb2)*xb2*(-xb1**3-3*xb1**2*xb2+4*xb1**2+2*
     . xb1*xb2**2+2*xb1*xb2-3*xb1-2*xb2**2+xb2)+2*t134p(mb1,mb2,mg)*(
     . -xb1**3+xb1**2*xb2+2*xb1**2-xb1*xb2**2-2*xb1+xb2**3-2*xb2**2+2
     . *xb2)+2*t134p(mb1,mg,mg)*(xb1**3-2*xb1**2*xb2-xb1**2+xb1*xb2**
     . 2+2*xb1*xb2-xb2**2)+2*t134p(mb2,mg,mg)*(-xb1**2*xb2+xb1**2+2*
     . xb1*xb2**2-2*xb1*xb2-xb2**3+xb2**2)+12*(xb1**3*xb2-xb1**3-xb1*
     . xb2**3+xb1+xb2**3-xb2)
      rb102=ans1/(8*(xb1**3*xb2**2-2*xb1**3*xb2+xb1**3-xb1**2*xb2**3+3
     . *xb1**2*xb2-2*xb1**2+2*xb1*xb2**3-3*xb1*xb2**2+xb1-xb2**3+2*
     . xb2**2-xb2))

      rbalstr2=(-((log(xs2)-6+log(xs1))*((xb1-1)*log(xb2)*xb2-(xb2-1)*
     . log(xb1)*xb1)+3*((xb1-1)*log(xb2)**2*xb2-(xb2-1)*log(xb1)**2*
     . xb1)))/(24*(xb1-xb2)*(xb1-1)*(xb2-1))

      rbmgtr2=((xs2-6+xs1+log(xs2)+log(xs1)+(log(xs2-1)-log(xs2))*(xs2
     . -1)**2+(log(xs1-1)-log(xs1))*(xs1-1)**2)*((xb1+1)*(xb2-1)**2*
     . log(xb1)*xb1-(xb1-1)**2*(xb2+1)*log(xb2)*xb2)+2*((log(xs2-1)-
     . log(xs2))*(xs2-1)**2+log(xs1)+log(xs2)+(log(xs1-1)-log(xs1))*(
     . xs1-1)**2)*(xb1-xb2)*(xb1-1)*(xb2-1)+(xb1+1)*(xb2-1)**2*log(
     . xb1)**2*xb1-(xb1-1)**2*(xb2+1)*log(xb2)**2*xb2+2*(xs2-6+xs1)*(
     . xb1-xb2)*(xb1-1)*(xb2-1))/(8*(xb1-xb2)*(xb1-1)**2*(xb2-1)**2)

      ms1 = amst1
      ms2 = amst2
      xs1 = amst1**2/amg**2 * rim
      xs2 = amst2**2/amg**2 * rim

      ans14=-8*log(xs2)*xb1*xb2**2*xs2-4*log(xs2)*xb1*xq**2*xs2-4*log
     . (xs2)*xb1*xq*xs2**2-4*log(xs2)*xb1*xq*xs2+8*log(xs2)*xb1*xs2**
     . 3-16*log(xs2)*xb1*xs2**2+8*log(xs2)*xb1*xs2-4*log(xs2)*xb2**2*
     . xq**2*xs2-4*log(xs2)*xb2**2*xq*xs2**2-4*log(xs2)*xb2**2*xq*xs2
     . +8*log(xs2)*xb2**2*xs2**3-16*log(xs2)*xb2**2*xs2**2+8*log(xs2)
     . *xb2**2*xs2+4*log(xs2)*xb2*xq**2*xs2+4*log(xs2)*xb2*xq*xs2**2+
     . 4*log(xs2)*xb2*xq*xs2-8*log(xs2)*xb2*xs2**3+16*log(xs2)*xb2*
     . xs2**2-8*log(xs2)*xb2*xs2
      ans13=-log(xs2)**2*xb1*xb2**2*xq**2*xs2+log(xs2)**2*xb1*xb2**2*
     . xs2**3-2*log(xs2)**2*xb1*xb2**2*xs2**2+log(xs2)**2*xb1*xb2**2*
     . xs2+log(xs2)**2*xb1*xq**2*xs2-log(xs2)**2*xb1*xs2**3+2*log(xs2
     . )**2*xb1*xs2**2-log(xs2)**2*xb1*xs2+log(xs2)**2*xb2**2*xq**2*
     . xs2-log(xs2)**2*xb2**2*xs2**3+2*log(xs2)**2*xb2**2*xs2**2-log(
     . xs2)**2*xb2**2*xs2-log(xs2)**2*xb2*xq**2*xs2+log(xs2)**2*xb2*
     . xs2**3-2*log(xs2)**2*xb2*xs2**2+log(xs2)**2*xb2*xs2-4*log(xs2)
     . *xb1**2*xb2*xq**2*xs2-4*log(xs2)*xb1**2*xb2*xq*xs2**2-4*log(
     . xs2)*xb1**2*xb2*xq*xs2+8*log(xs2)*xb1**2*xb2*xs2**3-16*log(xs2
     . )*xb1**2*xb2*xs2**2+8*log(xs2)*xb1**2*xb2*xs2+4*log(xs2)*xb1**
     . 2*xq**2*xs2+4*log(xs2)*xb1**2*xq*xs2**2+4*log(xs2)*xb1**2*xq*
     . xs2-8*log(xs2)*xb1**2*xs2**3+16*log(xs2)*xb1**2*xs2**2-8*log(
     . xs2)*xb1**2*xs2+4*log(xs2)*xb1*xb2**2*xq**2*xs2+4*log(xs2)*xb1
     . *xb2**2*xq*xs2**2+4*log(xs2)*xb1*xb2**2*xq*xs2-8*log(xs2)*xb1*
     . xb2**2*xs2**3+16*log(xs2)*xb1*xb2**2*xs2**2+ans14
      ans12=-4*log(xb2)**2*xb1*xb2*xq*xs1-8*log(xb2)**2*xb1*xb2*xq*
     . xs2**2+4*log(xb2)**2*xb1*xb2*xq*xs2-4*log(xb2)**2*xb1*xb2*xq+2
     . *log(xb2)**2*xb1*xb2*xs1*xs2**2-4*log(xb2)**2*xb1*xb2*xs1*xs2+
     . 2*log(xb2)**2*xb1*xb2*xs1+2*log(xb2)**2*xb1*xb2*xs2**3-4*log(
     . xb2)**2*xb1*xb2*xs2**2+2*log(xb2)**2*xb1*xb2*xs2+2*log(xb2)**2
     . *xb2*xq**3-log(xb2)**2*xb2*xq**2*xs1-5*log(xb2)**2*xb2*xq**2*
     . xs2-4*log(xb2)**2*xb2*xq**2+2*log(xb2)**2*xb2*xq*xs1*xs2+2*log
     . (xb2)**2*xb2*xq*xs1+4*log(xb2)**2*xb2*xq*xs2**2-2*log(xb2)**2*
     . xb2*xq*xs2+2*log(xb2)**2*xb2*xq-log(xb2)**2*xb2*xs1*xs2**2+2*
     . log(xb2)**2*xb2*xs1*xs2-log(xb2)**2*xb2*xs1-log(xb2)**2*xb2*
     . xs2**3+2*log(xb2)**2*xb2*xs2**2-log(xb2)**2*xb2*xs2+log(xs2)**
     . 2*xb1**2*xb2*xq**2*xs2-log(xs2)**2*xb1**2*xb2*xs2**3+2*log(xs2
     . )**2*xb1**2*xb2*xs2**2-log(xs2)**2*xb1**2*xb2*xs2-log(xs2)**2*
     . xb1**2*xq**2*xs2+log(xs2)**2*xb1**2*xs2**3-2*log(xs2)**2*xb1**
     . 2*xs2**2+log(xs2)**2*xb1**2*xs2+ans13
      ans11=4*log(xb1)**2*xb1*xq**2-2*log(xb1)**2*xb1*xq*xs1*xs2-2*
     . log(xb1)**2*xb1*xq*xs1-4*log(xb1)**2*xb1*xq*xs2**2+2*log(xb1)
     . **2*xb1*xq*xs2-2*log(xb1)**2*xb1*xq+log(xb1)**2*xb1*xs1*xs2**2
     . -2*log(xb1)**2*xb1*xs1*xs2+log(xb1)**2*xb1*xs1+log(xb1)**2*xb1
     . *xs2**3-2*log(xb1)**2*xb1*xs2**2+log(xb1)**2*xb1*xs2+2*log(xb2
     . )**2*xb1**2*xb2*xq**3-log(xb2)**2*xb1**2*xb2*xq**2*xs1-5*log(
     . xb2)**2*xb1**2*xb2*xq**2*xs2-4*log(xb2)**2*xb1**2*xb2*xq**2+2*
     . log(xb2)**2*xb1**2*xb2*xq*xs1*xs2+2*log(xb2)**2*xb1**2*xb2*xq*
     . xs1+4*log(xb2)**2*xb1**2*xb2*xq*xs2**2-2*log(xb2)**2*xb1**2*
     . xb2*xq*xs2+2*log(xb2)**2*xb1**2*xb2*xq-log(xb2)**2*xb1**2*xb2*
     . xs1*xs2**2+2*log(xb2)**2*xb1**2*xb2*xs1*xs2-log(xb2)**2*xb1**2
     . *xb2*xs1-log(xb2)**2*xb1**2*xb2*xs2**3+2*log(xb2)**2*xb1**2*
     . xb2*xs2**2-log(xb2)**2*xb1**2*xb2*xs2-4*log(xb2)**2*xb1*xb2*xq
     . **3+2*log(xb2)**2*xb1*xb2*xq**2*xs1+10*log(xb2)**2*xb1*xb2*xq
     . **2*xs2+8*log(xb2)**2*xb1*xb2*xq**2-4*log(xb2)**2*xb1*xb2*xq*
     . xs1*xs2+ans12
      ans10=5*log(xb1)**2*xb1*xb2**2*xq**2*xs2+4*log(xb1)**2*xb1*xb2
     . **2*xq**2-2*log(xb1)**2*xb1*xb2**2*xq*xs1*xs2-2*log(xb1)**2*
     . xb1*xb2**2*xq*xs1-4*log(xb1)**2*xb1*xb2**2*xq*xs2**2+2*log(xb1
     . )**2*xb1*xb2**2*xq*xs2-2*log(xb1)**2*xb1*xb2**2*xq+log(xb1)**2
     . *xb1*xb2**2*xs1*xs2**2-2*log(xb1)**2*xb1*xb2**2*xs1*xs2+log(
     . xb1)**2*xb1*xb2**2*xs1+log(xb1)**2*xb1*xb2**2*xs2**3-2*log(xb1
     . )**2*xb1*xb2**2*xs2**2+log(xb1)**2*xb1*xb2**2*xs2+4*log(xb1)**
     . 2*xb1*xb2*xq**3-2*log(xb1)**2*xb1*xb2*xq**2*xs1-10*log(xb1)**2
     . *xb1*xb2*xq**2*xs2-8*log(xb1)**2*xb1*xb2*xq**2+4*log(xb1)**2*
     . xb1*xb2*xq*xs1*xs2+4*log(xb1)**2*xb1*xb2*xq*xs1+8*log(xb1)**2*
     . xb1*xb2*xq*xs2**2-4*log(xb1)**2*xb1*xb2*xq*xs2+4*log(xb1)**2*
     . xb1*xb2*xq-2*log(xb1)**2*xb1*xb2*xs1*xs2**2+4*log(xb1)**2*xb1*
     . xb2*xs1*xs2-2*log(xb1)**2*xb1*xb2*xs1-2*log(xb1)**2*xb1*xb2*
     . xs2**3+4*log(xb1)**2*xb1*xb2*xs2**2-2*log(xb1)**2*xb1*xb2*xs2-
     . 2*log(xb1)**2*xb1*xq**3+log(xb1)**2*xb1*xq**2*xs1+5*log(xb1)**
     . 2*xb1*xq**2*xs2+ans11
      ans9=-4*t134(mb1,mq,ms2,mg)*xb1*xb2+2*t134(mb1,mq,ms2,mg)*xb1*
     . xq**2-4*t134(mb1,mq,ms2,mg)*xb1*xq*xs2-4*t134(mb1,mq,ms2,mg)*
     . xb1*xq+2*t134(mb1,mq,ms2,mg)*xb1*xs2**2-4*t134(mb1,mq,ms2,mg)*
     . xb1*xs2+2*t134(mb1,mq,ms2,mg)*xb1+2*t134(mb1,mq,ms2,mg)*xb2**2
     . *xq**3-6*t134(mb1,mq,ms2,mg)*xb2**2*xq**2*xs2-4*t134(mb1,mq,
     . ms2,mg)*xb2**2*xq**2+6*t134(mb1,mq,ms2,mg)*xb2**2*xq*xs2**2+2*
     . t134(mb1,mq,ms2,mg)*xb2**2*xq-2*t134(mb1,mq,ms2,mg)*xb2**2*xs2
     . **3+4*t134(mb1,mq,ms2,mg)*xb2**2*xs2**2-2*t134(mb1,mq,ms2,mg)*
     . xb2**2*xs2-4*t134(mb1,mq,ms2,mg)*xb2*xq**3+12*t134(mb1,mq,ms2,
     . mg)*xb2*xq**2*xs2+8*t134(mb1,mq,ms2,mg)*xb2*xq**2-12*t134(mb1,
     . mq,ms2,mg)*xb2*xq*xs2**2-4*t134(mb1,mq,ms2,mg)*xb2*xq+4*t134(
     . mb1,mq,ms2,mg)*xb2*xs2**3-8*t134(mb1,mq,ms2,mg)*xb2*xs2**2+4*
     . t134(mb1,mq,ms2,mg)*xb2*xs2+2*t134(mb1,mq,ms2,mg)*xq**3-6*t134
     . (mb1,mq,ms2,mg)*xq**2*xs2-4*t134(mb1,mq,ms2,mg)*xq**2+6*t134(
     . mb1,mq,ms2,mg)*xq*xs2**2+2*t134(mb1,mq,ms2,mg)*xq-2*t134(mb1,
     . mq,ms2,mg)*xs2**3+4*t134(mb1,mq,ms2,mg)*xs2**2-2*t134(mb1,mq,
     . ms2,mg)*xs2-2*log(xb1)**2*xb1*xb2**2*xq**3+log(xb1)**2*xb1*xb2
     . **2*xq**2*xs1+ans10
      ans8=4*t134(mb1,mq,ms1,mg)*xb2*xq**2*xs1+8*t134(mb1,mq,ms1,mg)*
     . xb2*xq**2*xs2+8*t134(mb1,mq,ms1,mg)*xb2*xq**2-8*t134(mb1,mq,
     . ms1,mg)*xb2*xq*xs1*xs2-8*t134(mb1,mq,ms1,mg)*xb2*xq*xs1-4*t134
     . (mb1,mq,ms1,mg)*xb2*xq*xs2**2+8*t134(mb1,mq,ms1,mg)*xb2*xq*xs2
     . -4*t134(mb1,mq,ms1,mg)*xb2*xq+4*t134(mb1,mq,ms1,mg)*xb2*xs1*
     . xs2**2-8*t134(mb1,mq,ms1,mg)*xb2*xs1*xs2+4*t134(mb1,mq,ms1,mg)
     . *xb2*xs1+2*t134(mb1,mq,ms1,mg)*xq**3-2*t134(mb1,mq,ms1,mg)*xq
     . **2*xs1-4*t134(mb1,mq,ms1,mg)*xq**2*xs2-4*t134(mb1,mq,ms1,mg)*
     . xq**2+4*t134(mb1,mq,ms1,mg)*xq*xs1*xs2+4*t134(mb1,mq,ms1,mg)*
     . xq*xs1+2*t134(mb1,mq,ms1,mg)*xq*xs2**2-4*t134(mb1,mq,ms1,mg)*
     . xq*xs2+2*t134(mb1,mq,ms1,mg)*xq-2*t134(mb1,mq,ms1,mg)*xs1*xs2
     . **2+4*t134(mb1,mq,ms1,mg)*xs1*xs2-2*t134(mb1,mq,ms1,mg)*xs1+2*
     . t134(mb1,mq,ms2,mg)*xb1*xb2**2*xq**2-4*t134(mb1,mq,ms2,mg)*xb1
     . *xb2**2*xq*xs2-4*t134(mb1,mq,ms2,mg)*xb1*xb2**2*xq+2*t134(mb1,
     . mq,ms2,mg)*xb1*xb2**2*xs2**2-4*t134(mb1,mq,ms2,mg)*xb1*xb2**2*
     . xs2+2*t134(mb1,mq,ms2,mg)*xb1*xb2**2-4*t134(mb1,mq,ms2,mg)*xb1
     . *xb2*xq**2+8*t134(mb1,mq,ms2,mg)*xb1*xb2*xq*xs2+8*t134(mb1,mq,
     . ms2,mg)*xb1*xb2*xq-4*t134(mb1,mq,ms2,mg)*xb1*xb2*xs2**2+8*t134
     . (mb1,mq,ms2,mg)*xb1*xb2*xs2+ans9
      ans7=2*t134(mb1,mq,ms1,mg)*xb1*xb2**2*xq**2-4*t134(mb1,mq,ms1,
     . mg)*xb1*xb2**2*xq*xs2-4*t134(mb1,mq,ms1,mg)*xb1*xb2**2*xq+2*
     . t134(mb1,mq,ms1,mg)*xb1*xb2**2*xs2**2-4*t134(mb1,mq,ms1,mg)*
     . xb1*xb2**2*xs2+2*t134(mb1,mq,ms1,mg)*xb1*xb2**2-4*t134(mb1,mq,
     . ms1,mg)*xb1*xb2*xq**2+8*t134(mb1,mq,ms1,mg)*xb1*xb2*xq*xs2+8*
     . t134(mb1,mq,ms1,mg)*xb1*xb2*xq-4*t134(mb1,mq,ms1,mg)*xb1*xb2*
     . xs2**2+8*t134(mb1,mq,ms1,mg)*xb1*xb2*xs2-4*t134(mb1,mq,ms1,mg)
     . *xb1*xb2+2*t134(mb1,mq,ms1,mg)*xb1*xq**2-4*t134(mb1,mq,ms1,mg)
     . *xb1*xq*xs2-4*t134(mb1,mq,ms1,mg)*xb1*xq+2*t134(mb1,mq,ms1,mg)
     . *xb1*xs2**2-4*t134(mb1,mq,ms1,mg)*xb1*xs2+2*t134(mb1,mq,ms1,mg
     . )*xb1+2*t134(mb1,mq,ms1,mg)*xb2**2*xq**3-2*t134(mb1,mq,ms1,mg)
     . *xb2**2*xq**2*xs1-4*t134(mb1,mq,ms1,mg)*xb2**2*xq**2*xs2-4*
     . t134(mb1,mq,ms1,mg)*xb2**2*xq**2+4*t134(mb1,mq,ms1,mg)*xb2**2*
     . xq*xs1*xs2+4*t134(mb1,mq,ms1,mg)*xb2**2*xq*xs1+2*t134(mb1,mq,
     . ms1,mg)*xb2**2*xq*xs2**2-4*t134(mb1,mq,ms1,mg)*xb2**2*xq*xs2+2
     . *t134(mb1,mq,ms1,mg)*xb2**2*xq-2*t134(mb1,mq,ms1,mg)*xb2**2*
     . xs1*xs2**2+4*t134(mb1,mq,ms1,mg)*xb2**2*xs1*xs2-2*t134(mb1,mq,
     . ms1,mg)*xb2**2*xs1-4*t134(mb1,mq,ms1,mg)*xb2*xq**3+ans8
      ans15=(xq**2-2*xq*xs1-2*xq+xs1**2-2*xs1+1)
      ans6=ans7*ans15
      ans5=-ans6
      ans4=(4*(2*(xs1-1)**2-xq**2-(xs1+1)*xq)-(xs1-1+xq)*(xs1-1-xq)*
     . log(xs1))*(2*(xs2+1)*xq-(xs2-1)**2-xq**2)*(xb1-xb2)*(xb1-1)*(
     . xb2-1)*log(xs1)*xs1+ans5
      ans3=-ans4
      ans17=4*(3*((xs1+1)*xs1+xs2**2+xs2-1)+2*(3*xq**2+2)*xq+((2*xq**
     . 2-5*xq+8)*xq-3*(xs1+xs2)**2)*(xs1+xs2)-(4*xq-3*xs1*xs2)*(2*xs1
     . **2+3*xs1*xs2+2*xs2**2)+2*(3*xs1**2-8*xs1*xs2+3*xs2**2)*(xs1+
     . xs2)*xq-(13*xq**2+4*xs1*xs2)*xq**2+((3*xs1**2-2*xs1*xs2+3*xs2
     . **2)*xq-2*(xs1+xs2)*xq**2-3*(xs1+xs2)*xs1*xs2+6*xq**3)*(xq-xs1
     . )*(xq-xs2))*(xb1-xb2)*(xb1-1)*(xb2-1)+4*(2*((xs2-1)**2+xs1**2+
     . 2*(2*xs2-1)*xs1+(5*xq**2-1)*xq)-(xs1**2-4*xs1*xs2+xs2**2)*xq-2
     . *(xq**2+2*xs1*xs2)*(xs1+xs2)+(xs1-1-xq)*(2*(xs2+1)*xq-(xs2-1)
     . **2-xq**2)*log(xs1)*xs1+(2*(xs1+1)*xq-(xs1-1)**2-xq**2)*(xs2-1
     . -xq)*log(xs2)*xs2+(xs1+xs2-6*xq)*xq+((xs1+xs2)*xq-4*xq**2+2*
     . xs1*xs2)*(xq-xs1)*(xq-xs2))*(xb1-xb2)*(xb1-1)*(xb2-1)*log(xq)*
     . xq
      ans16=-2*(2*((xs1-1)**2*xs1-xq**3-(3*xs1-1)*xq*xs1+(3*xs1+1)*xq
     . **2)+(xq**2-2*xq*xs1+xs1**2-2*xs1+1)*(xq-xs1-1)*xb2-(2*((xs1+1
     . )*xq-(xs1-1)**2)*xb2-(xq**2-2*xq*xs1+xs1**2-2*xs1+1)*(xq-xs1-1
     . ))*xb1)*(2*(xs2+1)*xq-(xs2-1)**2-xq**2)*(xb1-xb2)*t134(mg,mq,
     . ms1,mg)-2*((xs2-1)**2+xs1**2+2*(2*xs2-1)*xs1+2*(xq+1)*(xq-1)*
     . xq+(xq-2*xs1*xs2)*(xs1+xs2)-(xs1**2-4*xs1*xs2+xs2**2)*xq-(xq**
     . 2-xs1*xs2)*(xq-xs1)*(xq-xs2))*(xb1-xb2)*(xb1-1)*(xb2-1)*log(xq
     . )**2*xq-2*((2*((xs2-1)**2*xs2-xq**3-(3*xs2-1)*xq*xs2+(3*xs2+1)
     . *xq**2)+(xq**2-2*xq*xs2+xs2**2-2*xs2+1)*(xq-xs2-1)*xb2-(2*((
     . xs2+1)*xq-(xs2-1)**2)*xb2-(xq**2-2*xq*xs2+xs2**2-2*xs2+1)*(xq-
     . xs2-1))*xb1)*(xb1-xb2)*t134(mg,mq,ms2,mg)+((xq-xs1+xb2)*t134(
     . mb2,mq,ms1,mg)+(xq-xs2+xb2)*t134(mb2,mq,ms2,mg))*(2*(xs2+1)*xq
     . -(xs2-1)**2-xq**2)*(xb1-1)**2)*(2*(xs1+1)*xq-(xs1-1)**2-xq**2)
     . +ans17
      ans2=2*(2*(xs1+xs2-2*xq)-log(xs2)*xs2-log(xs1)*xs1+2*log(xq)*xq
     . )*((xb1-1)**2*log(xb2)*xb2-(xb2-1)**2*log(xb1)*xb1)*(2*(xs1+1)
     . *xq-(xs1-1)**2-xq**2)*(2*(xs2+1)*xq-(xs2-1)**2-xq**2)+ans3+
     . ans16
      ans1=-ans2
      rt102=ans1/(8*((xs1-1)**2+xq**2-2*(xs1+1)*xq)*((xs2-1)**2+xq**2-
     . 2*(xs2+1)*xq)*(xb1-xb2)*(xb1-1)**2*(xb2-1)**2)

      rtalstr2=(-((log(xs2)-6+log(xs1))*((xb1-1)*log(xb2)*xb2-(xb2-1)*
     . log(xb1)*xb1)+3*((xb1-1)*log(xb2)**2*xb2-(xb2-1)*log(xb1)**2*
     . xb1)))/(24*(xb1-xb2)*(xb1-1)*(xb2-1))

      rtmgtr2=((xs2-6+xs1-2*xq+(xq+1)*log(xs2)+(xq+1)*log(xs1)-2*log(
     . xq)*xq-(xs2-1-xq)*log(xp(ms2))*xp(ms2)-(xs1-1-xq)*log(xp(ms1))
     . *xp(ms1)-(xs2-1-xq)*log(xm(ms2))*xm(ms2)-(xs1-1-xq)*log(xm(ms1
     . ))*xm(ms1)+(xs2-1-xq)*log(xp(ms2)-1)*xp(ms2)+(xs1-1-xq)*log(xp
     . (ms1)-1)*xp(ms1)+(xs2-1-xq)*log(xm(ms2)-1)*xm(ms2)+(xs1-1-xq)*
     . log(xm(ms1)-1)*xm(ms1))*((xb1+1)*(xb2-1)**2*log(xb1)*xb1-(xb1-
     . 1)**2*(xb2+1)*log(xb2)*xb2)+2*((log(xs1)+log(xs2))*(xq+1)-2*
     . log(xq)*xq)*(xb1-xb2)*(xb1-1)*(xb2-1)+(xb1+1)*(xb2-1)**2*log(
     . xb1)**2*xb1-(xb1-1)**2*(xb2+1)*log(xb2)**2*xb2+2*((log(xm(ms2)
     . -1)-log(xm(ms2)))*xm(ms2)+(log(xp(ms2)-1)-log(xp(ms2)))*xp(ms2
     . ))*(xs2-1-xq)*(xb1-xb2)*(xb1-1)*(xb2-1)+2*((log(xm(ms1)-1)-log
     . (xm(ms1)))*xm(ms1)+(log(xp(ms1)-1)-log(xp(ms1)))*xp(ms1))*(xs1
     . -1-xq)*(xb1-xb2)*(xb1-1)*(xb2-1)+2*(xs2-6+xs1-2*xq)*(xb1-xb2)*
     . (xb1-1)*(xb2-1))/(8*(xb1-xb2)*(xb1-1)**2*(xb2-1)**2)

c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      ans2=(((3*xs1-1)*(xs1-1)+3*xq**2-2*(3*xs1+2)*xq-(xq-xs1+1)*(xq-
     . xs1-1)*xb2-(((xs1-1)*(xs1-3)+xq**2-2*(xs1+2)*xq)*xb2+(xq-xs1+1
     . )*(xq-xs1-1))*xb1)*(2*(xs2+1)*xq-(xs2-1)**2-xq**2)*t134(mg,mq,
     . ms1,mg)-2*(2*(2*xs2-1+2*xq-(xq-xs2)**2)*log(xs1)*xs1-3*((xs2+2
     . +xs1)*xq+(xs1-1)*(xs2-1)-3*xq**2)*(xs1-xs2)-2*(2*xs1-1+2*xq-(
     . xq-xs1)**2)*log(xs2)*xs2)*(xb1-1)*(xb2-1)*log(xq)*xq)*(xb1-xb2
     . )
      ans1=((2*(xs1+1)*xq-(xs1-1)**2-xq**2)*(xs2-1+xq)*(log(xs2)-6)*
     . log(xs2)*xs2-(xs1-1+xq)*(2*(xs2+1)*xq-(xs2-1)**2-xq**2)*(log(
     . xs1)-6)*log(xs1)*xs1)*(xb1-xb2)*(xb1-1)*(xb2-1)+((t134(mb1,mq,
     . ms1,mg)-t134(mb1,mq,ms2,mg))*(xb1+1)*(xb2-1)**2-(t134(mb2,mq,
     . ms1,mg)-t134(mb2,mq,ms2,mg))*(xb1-1)**2*(xb2+1))*(2*(xs1+1)*xq
     . -(xs1-1)**2-xq**2)*(2*(xs2+1)*xq-(xs2-1)**2-xq**2)-((xs2+2+xs1
     . )*xq+(xs1-1)*(xs2-1)-3*xq**2)*(xb1-xb2)*(xb1-1)*(xb2-1)*(xs1-
     . xs2)*log(xq)**2*xq+14*(xs2-1+xs1-(xq+xs1)*(xq+xs2)+2*(xq**2-
     . xs1*xs2)*xq)*(xb1-xb2)*(xb1-1)*(xb2-1)*(xs1-xs2)-((3*xs2-1)*(
     . xs2-1)+3*xq**2-2*(3*xs2+2)*xq-(xq-xs2+1)*(xq-xs2-1)*xb2-(((xs2
     . -1)*(xs2-3)+xq**2-2*(xs2+2)*xq)*xb2+(xq-xs2+1)*(xq-xs2-1))*xb1
     . )*(2*(xs1+1)*xq-(xs1-1)**2-xq**2)*(xb1-xb2)*t134(mg,mq,ms2,mg)
     . +ans2
      rtp102=ans1/(2*((xs1-1)**2+xq**2-2*(xs1+1)*xq)*((xs2-1)**2+xq**2-
     . 2*(xs2+1)*xq)*(xb1-xb2)*(xb1-1)**2*(xb2-1)**2*(xs1-xs2))

      rmgtrt2=(-((log(xp(ms2)-1)-log(xp(ms2)))*xp(ms2)+log(xs1)-log(
     . xs2)-(log(xp(ms1)-1)-log(xp(ms1)))*xp(ms1)+(log(xm(ms2)-1)-log
     . (xm(ms2)))*xm(ms2)-(log(xm(ms1)-1)-log(xm(ms1)))*xm(ms1))*((
     . xb1+1)*(xb2-1)**2*log(xb1)*xb1-(xb1-1)**2*(xb2+1)*log(xb2)*xb2
     . +2*(xb1-xb2)*(xb1-1)*(xb2-1)))/(4*(xb1-xb2)*(xb1-1)**2*(xb2-1)
     . **2)

      fact = amt**2*xxt/amg**3
      rtp102 = fact * rtp102
      fact = 2*amt**2*xxt/(amst1**2-amst2**2)/amg
      rmgtrt2 = fact * rmgtrt2
      rtp102 = rtp102 + rmgtrt2
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

      rctca = ralsca2 + rmgca2
      rctcf = ralscf2 + rmb12 + rmb22
      ructtr = rualstr2 + rumgtr2
      rdcttr = rdalstr2 + rdmgtr2
      rbcttr = rbalstr2 + rbmgtr2
      rtcttr = rtalstr2 + rtmgtr2

      bo  =-2*fi(amsb1**2,amsb2**2,amg**2)

      rca = r12 + r22/4 + r32 + r52 + r62 + rctca
      rcf = -r22/2 - r42/2 - 2*r52 - r72/2 + r82 - r92/2 + rctcf
      rtr = nu*(ru102 + ructtr) + nd*(rd102 + rdcttr)
      rtrb= rb102 + rbcttr
      rtrt= rt102 + rtp102 + rtcttr + bo/3*dlog(amg**2/amt**2)/fnorm

      rqcd = ca*rca + cf*rcf + tr*(rtr+rtrb+rtrt)
      rqcd = rqcd/bo
      anomalous = - cf/4
      finscale = (11*ca-4*tr*nf)/12*dlog(scale**2/amg**2)
      fqcd_hdec = dreal(rqcd)*fnorm + anomalous + finscale

c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
c     fac = fnorm/bo
c     write(6,*)'par: ',scale,amg,amsb1,amsb2,amst1,amst2
c     write(6,*)'C_A: ',dreal(ca*r12*fac),dreal(ca*r22/4*fac),
c    .                  dreal(ca*r32*fac),dreal(ca*r42*fac),
c    .                  dreal(ca*r62*fac),dreal(ca*rctca*fac)
c     write(6,*)'C_F: ',dreal(-cf*r22/2*fac),dreal(-cf*r42/2*fac),
c    .  dreal(-2*cf*r52*fac),dreal(cf*r72/2*fac),dreal(cf*r82*fac),
c    .                  dreal(-cf*r92/2*fac),dreal(cf*rctcf*fac)
c     write(6,*)'T_R: ',dreal(tr*rtr*fac),dreal(tr*rtrb*fac),
c    .                  dreal(tr*rtrt*fac)
c     write(6,*)'rtrt ',dreal(tr*rt102*fac),dreal(tr*rtp102*fac),
c    .                  dreal(tr*rtcttr*fac),3*dlog(amg**2/amt**2)
c     write(6,*)'QCD: ',dreal(ca*rca*fac),dreal(cf*rcf*fac),
c    .                  dreal(tr*(rtr+rtrb+rtrt)*fac),anomalous,finscale
c     write(6,*)'sum: ',fqcd_hdec
c     write(6,*)
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
c     fac = fnorm/bo
c     ysu = tr*dreal(nu*(ru102+ructtr)*fac
c    .              -4*nu/12.d0*dlog(scale**2/amg**2))
c     ysd = tr*dreal(nd*(rd102+rdcttr)*fac
c    .              -4*nd/12.d0*dlog(scale**2/amg**2))
c     ysb = tr*dreal(rtrb*fac-4/12.d0*dlog(scale**2/amg**2))
c     yst = tr*dreal(rtrt-rtp102)*fac
c     ystp= tr*dreal(rtp102/xxt)*fac
c     fac = 0.7705157934627561d0*0.088374016132112168d0/pi
c     ysu  = ysu * fac
c     ysd  = ysd * fac
c     ysb  = ysb * fac
c     yst  = yst * fac
c     ystp = ystp* fac
c     write(6,*)'dmb: '
c     write(6,*)'full ',dreal(rqcd)*fnorm*fac,anomalous*fac,finscale*fac
c     write(6,*)'CA = ',ca*(dreal(rca)*fnorm/bo
c    .                     +11/12.d0*dlog(scale**2/amg**2))*fac
c     write(6,*)'CF = ',cf*(dreal(rcf)*fnorm/bo-1/4.d0)*fac
c     write(6,*)'TR = ',tr*(dreal(rtr+rtrb+rtrt)*fnorm/bo
c    .                     -4*nf/12.d0*dlog(scale**2/amg**2))*fac
c     write(6,*)'su,sd,sb,st: ',ysu,ysd,ysb,yst,ystp*xxt,ystp
c     write(6,*)'xt = ',xxt
c     write(6,*)
c>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

      return
      end
 
c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 
      double precision function fsqcd_hdec(scale,amt,amg,amsb1,amsb2,
     .                         amst1,amst2,amsu1,amsu2,amsd1,amsd2)
      implicit double precision (b-h,o-q,s-z), complex*16 (a,r)
      double precision amt,amg,amsb1,amsb2,amst1,amst2,
     .                 amsu1,amsu2,amsd1,amsd2
      double precision mt,mg,mb1,mb2,mt1,mt2,ms1,ms2,mu
      complex*16 sp,li2_hdec,xt,xgl,xt1,xt2,xb1,xb2,xs1,xs2,xq
      double precision m,mq
      double precision anomalous
      double precision a
      complex*16 xp,xm
      sp(r) = li2_hdec(r)
      xp(m) = (amg**2+amt**2-m**2)/2/amg**2/rim
     . +cdsqrt(((amg**2+amt**2-m**2)/2/amg**2/rim)**2-amt**2/amg**2/rim)
      xm(m) = (amg**2+amt**2-m**2)/2/amg**2/rim
     . -cdsqrt(((amg**2+amt**2-m**2)/2/amg**2/rim)**2-amt**2/amg**2/rim)
      fi(a,b,c) = (a*b*log(a/b)+b*c*log(b/c)+c*a*log(c/a))
     .          / (a-b)/(b-c)/(a-c)
      t134p(a,b,c)  = t134p_hdec(a,b,c)
      t134(a,b,c,d) = t134_hdec(a,b,c,d)

      eps = 1.d-15
      pi = 4*datan(1.d0)
      zeta2 = pi**2/6

      ca = 3
      cf = 4/3.d0
      tr = 1/2.d0
      nu = 2
      nd = 2
      nf = nu+nd+1

      fnorm = 4/amg**2

      rim = dcmplx(1.d0,eps)

      mq  = amt
      mt  = amt
      mg  = amg
      mu  = amg
      mt1 = amsd1
      mt2 = amsd2
      mb1 = amsd1
      mb2 = amsd2

      xq  = amt**2/amg**2   * rim
      xt  = amt**2/amg**2   * rim
      xgl = amg**2/amg**2   * rim
      xt1 = amsd1**2/amg**2 * rim
      xt2 = amsd2**2/amg**2 * rim
      xb1 = amsd1**2/amg**2 * rim
      xb2 = amsd2**2/amg**2 * rim

      r12=(log(xb1)**2*xb1*(-2*xb1*xb2**2+4*xb1*xb2-2*xb1+xb2**2-2*
     . xb2+1)+4*log(xb1)*xb1*(xb1*xb2**2-2*xb1*xb2+xb1-xb2**2+2*xb2-1
     . )+log(xb2)**2*xb2*(2*xb1**2*xb2-xb1**2-4*xb1*xb2+2*xb1+2*xb2-1
     . )+4*log(xb2)*xb2*(-xb1**2*xb2+xb1**2+2*xb1*xb2-2*xb1-xb2+1)+4*
     . t134p(mb1,mb1,mg)*xb1*(xb2**2-2*xb2+1)+4*t134p(mb1,mg,mg)*(-
     . xb1*xb2**2+2*xb1*xb2-xb1-xb2**2+2*xb2-1)+4*t134p(mb2,mb2,mg)*
     . xb2*(-xb1**2+2*xb1-1)+4*t134p(mb2,mg,mg)*(xb1**2*xb2+xb1**2-2*
     . xb1*xb2-2*xb1+xb2+1)+4*t134p(mg,mg,mg)*(-xb1**2+2*xb1+xb2**2-2
     . *xb2))/(16*(xb1**3*xb2**2-2*xb1**3*xb2+xb1**3-xb1**2*xb2**3+3*
     . xb1**2*xb2-2*xb1**2+2*xb1*xb2**3-3*xb1*xb2**2+xb1-xb2**3+2*xb2
     . **2-xb2))

      r22=(4*log(xgl)**2*(-xt1**2*xt2+xt1*xt2**2+xt1-xt2)+4*log(xgl)*
     . log(xt1)*xt1*(-xt2**2+2*xt2-1)+4*log(xgl)*log(xt2)*xt2*(xt1**2
     . -2*xt1+1)+12*log(xgl)*(-xt1**2*xt2+xt1*xt2**2+xt1-xt2)+log(xt1
     . )**2*xt1*(xt2**2-2*xt2+1)+2*log(xt1)*xt1*(-xt1*xt2**2+2*xt1*
     . xt2-xt1-2*xt2**2+4*xt2-2)+log(xt2)**2*xt2*(-xt1**2+2*xt1-1)+2*
     . log(xt2)*xt2*(xt1**2*xt2+2*xt1**2-2*xt1*xt2-4*xt1+xt2+2)+t134p
     . (mu,mt1,mg)*xgl*(-xt1*xt2**2+2*xt1*xt2-xt1-xt2**2+2*xt2-1)+
     . t134p(mu,mt2,mg)*xgl*(xt1**2*xt2+xt1**2-2*xt1*xt2-2*xt1+xt2+1)
     . +14*(-xt1**2*xt2+xt1*xt2**2+xt1-xt2))/(2*(xt1**3*xt2**2-2*xt1
     . **3*xt2+xt1**3-xt1**2*xt2**3+3*xt1**2*xt2-2*xt1**2+2*xt1*xt2**
     . 3-3*xt1*xt2**2+xt1-xt2**3+2*xt2**2-xt2))

      r32=(log(xb1)**2*xb1*(-xb2**2+2*xb2-1)+2*log(xb1)*xb1*(2*xb1*
     . xb2**2-4*xb1*xb2+2*xb1+xb2**2-2*xb2+1)+log(xb2)**2*xb2*(xb1**2
     . -2*xb1+1)+2*log(xb2)*xb2*(-2*xb1**2*xb2-xb1**2+4*xb1*xb2+2*xb1
     . -2*xb2-1)+2*t134p(mb1,mg,mg)*(2*xb1*xb2**2-4*xb1*xb2+2*xb1-xb2
     . **2+2*xb2-1)+2*t134p(mb2,mg,mg)*(-2*xb1**2*xb2+xb1**2+4*xb1*
     . xb2-2*xb1-2*xb2+1)+3*t134p(mg,mg,mg)*(xb1**2*xb2-xb1**2-xb1*
     . xb2**2+xb1+xb2**2-xb2)+14*(xb1**2*xb2-xb1*xb2**2-xb1+xb2))/(8*
     . (xb1**3*xb2**2-2*xb1**3*xb2+xb1**3-xb1**2*xb2**3+3*xb1**2*xb2-
     . 2*xb1**2+2*xb1*xb2**3-3*xb1*xb2**2+xb1-xb2**3+2*xb2**2-xb2))

      r42=(8*log(xgl)**2*(xt1**2*xt2-xt1*xt2**2-xt1+xt2)+8*log(xgl)*
     . log(xt1)*xt1*(xt2**2-2*xt2+1)+8*log(xgl)*log(xt2)*xt2*(-xt1**2
     . +2*xt1-1)+24*log(xgl)*(xt1**2*xt2-xt1*xt2**2-xt1+xt2)+2*log(
     . xt1)**2*xt1*(-xt2**2+2*xt2-1)+log(xt1)*xt1*(5*xt1*xt2**2-10*
     . xt1*xt2+5*xt1+7*xt2**2-14*xt2+7)+2*log(xt2)**2*xt2*(xt1**2-2*
     . xt1+1)+log(xt2)*xt2*(-5*xt1**2*xt2-7*xt1**2+10*xt1*xt2+14*xt1-
     . 5*xt2-7)+2*t134p(mt1,mu,mg)*xgl*(xt1*xt2**2-2*xt1*xt2+xt1+xt2
     . **2-2*xt2+1)+2*t134p(mt2,mu,mg)*xgl*(-xt1**2*xt2-xt1**2+2*xt1*
     . xt2+2*xt1-xt2-1)+28*(xt1**2*xt2-xt1*xt2**2-xt1+xt2))/(2*(xt1**
     . 3*xt2**2-2*xt1**3*xt2+xt1**3-xt1**2*xt2**3+3*xt1**2*xt2-2*xt1
     . **2+2*xt1*xt2**3-3*xt1*xt2**2+xt1-xt2**3+2*xt2**2-xt2))

      r52=(log(xb1)**2*xb1*(2*xb1*xb2**2-4*xb1*xb2+2*xb1-xb2**2+2*xb2
     . -1)+4*log(xb1)*xb1*(-xb1*xb2**2+2*xb1*xb2-xb1+xb2**2-2*xb2+1)+
     . log(xb2)**2*xb2*(-2*xb1**2*xb2+xb1**2+4*xb1*xb2-2*xb1-2*xb2+1)
     . +4*log(xb2)*xb2*(xb1**2*xb2-xb1**2-2*xb1*xb2+2*xb1+xb2-1)+2*
     . t134p(mb1,mb2,mg)*(xb1**2*xb2-xb1**2-xb1*xb2**2+xb1+xb2**2-xb2
     . )+2*t134p(mb1,mg,mg)*(-xb1**2*xb2+xb1**2+2*xb1*xb2-2*xb1-xb2+1
     . )+2*t134p(mb2,mg,mg)*(xb1*xb2**2-2*xb1*xb2+xb1-xb2**2+2*xb2-1)
     . )/(16*(xb1**3*xb2**2-2*xb1**3*xb2+xb1**3-xb1**2*xb2**3+3*xb1**
     . 2*xb2-2*xb1**2+2*xb1*xb2**3-3*xb1*xb2**2+xb1-xb2**3+2*xb2**2-
     . xb2))

      r62=(log(xb1)**2*xb1*(xb2**2-2*xb2+1)+2*log(xb1)*xb1*(-xb2**2+2
     . *xb2-1)+log(xb2)**2*xb2*(-xb1**2+2*xb1-1)+2*log(xb2)*xb2*(xb1
     . **2-2*xb1+1)+2*t134p(mb1,mg,mg)*(xb1*xb2**2-2*xb1*xb2+xb1+xb2
     . **2-2*xb2+1)+2*t134p(mb2,mg,mg)*(-xb1**2*xb2-xb1**2+2*xb1*xb2+
     . 2*xb1-xb2-1)+2*t134p(mg,mg,mg)*(xb1**2*xb2+xb1**2-xb1*xb2**2-3
     . *xb1-xb2**2+3*xb2))/(8*(xb1**3*xb2**2-2*xb1**3*xb2+xb1**3-xb1
     . **2*xb2**3+3*xb1**2*xb2-2*xb1**2+2*xb1*xb2**3-3*xb1*xb2**2+xb1
     . -xb2**3+2*xb2**2-xb2))

      ans1=8*log(xgl)**2*(xt1**2*xt2-xt1**2-xt1*xt2**2+xt1+xt2**2-xt2
     . )+4*log(xgl)*log(xt1)*xt1*(4*xt1*xt2**2-8*xt1*xt2+4*xt1-3*xt2
     . **2+6*xt2-3)+4*log(xgl)*log(xt2)*xt2*(-4*xt1**2*xt2+3*xt1**2+8
     . *xt1*xt2-6*xt1-4*xt2+3)+12*log(xgl)*(xt1**2*xt2-xt1**2-xt1*xt2
     . **2+xt1+xt2**2-xt2)+log(xt1)**2*xt1*(-8*xt1*xt2**2+16*xt1*xt2-
     . 8*xt1+5*xt2**2-10*xt2+5)+4*log(xt1)*xt1*(3*xt1*xt2**2-6*xt1*
     . xt2+3*xt1-2*xt2**2+4*xt2-2)+log(xt2)**2*xt2*(8*xt1**2*xt2-5*
     . xt1**2-16*xt1*xt2+10*xt1+8*xt2-5)+4*log(xt2)*xt2*(-3*xt1**2*
     . xt2+2*xt1**2+6*xt1*xt2-4*xt1-3*xt2+2)+4*t134p(mt1,mt1,mg)*xgl*
     . (xt1*xt2**2-2*xt1*xt2+xt1+xt2**2-2*xt2+1)+4*t134p(mt2,mt2,mg)*
     . xgl*(-xt1**2*xt2-xt1**2+2*xt1*xt2+2*xt1-xt2-1)+4*t134p(mu,mt1,
     . mg)*xgl*(-xt1*xt2**2+2*xt1*xt2-xt1-xt2**2+2*xt2-1)+4*t134p(mu,
     . mt2,mg)*xgl*(xt1**2*xt2+xt1**2-2*xt1*xt2-2*xt1+xt2+1)+8*(xt1**
     . 2*xt2-xt1**2-xt1*xt2**2+xt1+xt2**2-xt2)
      r72=ans1/(8*(xt1**3*xt2**2-2*xt1**3*xt2+xt1**3-xt1**2*xt2**3+3*
     . xt1**2*xt2-2*xt1**2+2*xt1*xt2**3-3*xt1*xt2**2+xt1-xt2**3+2*xt2
     . **2-xt2))

      r82=(log(xb1)**2*(xb1*xb2**2-2*xb1*xb2+xb1-2*xb2**2+4*xb2-2)+4*
     . log(xb1)*(-xb1**2*xb2**2+2*xb1**2*xb2-xb1**2+xb1*xb2**2-2*xb1*
     . xb2+xb1+xb2**2-2*xb2+1)+log(xb2)**2*(-xb1**2*xb2+2*xb1**2+2*
     . xb1*xb2-4*xb1-xb2+2)+4*log(xb2)*(xb1**2*xb2**2-xb1**2*xb2-xb1
     . **2-2*xb1*xb2**2+2*xb1*xb2+2*xb1+xb2**2-xb2-1)+2*t134p(mb1,mg,
     . mg)*(-xb1*xb2**2+2*xb1*xb2-xb1+xb2**2-2*xb2+1)+2*t134p(mb2,mg,
     . mg)*(xb1**2*xb2-xb1**2-2*xb1*xb2+2*xb1+xb2-1)+10*(-xb1**2*xb2+
     . xb1**2+xb1*xb2**2-xb1-xb2**2+xb2))/(8*(xb1**3*xb2**2-2*xb1**3*
     . xb2+xb1**3-xb1**2*xb2**3+3*xb1**2*xb2-2*xb1**2+2*xb1*xb2**3-3*
     . xb1*xb2**2+xb1-xb2**3+2*xb2**2-xb2))

      ans2=4*log(xt2)*xt2*(-3*xt1**3*xt2+2*xt1**3+3*xt1**2*xt2**2+4*
     . xt1**2*xt2-4*xt1**2-6*xt1*xt2**2+xt1*xt2+2*xt1+3*xt2**2-2*xt2)
     . +4*(xt1**3*xt2-xt1**3-2*xt1**2*xt2**2+xt1**2*xt2+xt1**2+xt1*
     . xt2**3+xt1*xt2**2-2*xt1*xt2-xt2**3+xt2**2)
      ans1=4*log(xgl)*log(xt1)*xt1*(2*xt1**2*xt2**2-4*xt1**2*xt2+2*
     . xt1**2-2*xt1*xt2**3+3*xt1*xt2**2-xt1+xt2**3-2*xt2**2+xt2)+4*
     . log(xgl)*log(xt2)*xt2*(-2*xt1**3*xt2+xt1**3+2*xt1**2*xt2**2+3*
     . xt1**2*xt2-2*xt1**2-4*xt1*xt2**2+xt1+2*xt2**2-xt2)+4*log(xgl)*
     . (xt1**3*xt2-xt1**3-2*xt1**2*xt2**2+xt1**2*xt2+xt1**2+xt1*xt2**
     . 3+xt1*xt2**2-2*xt1*xt2-xt2**3+xt2**2)+log(xt1)**2*xt1*(-6*xt1
     . **2*xt2**2+12*xt1**2*xt2-6*xt1**2+2*xt1*xt2**3-xt1*xt2**2-4*
     . xt1*xt2+3*xt1+xt2**3-2*xt2**2+xt2)+4*log(xt1)*log(xt2)*xt1*xt2
     . *(xt1**2*xt2-xt1**2+xt1*xt2**2-4*xt1*xt2+3*xt1-xt2**2+3*xt2-2)
     . +4*log(xt1)*xt1*(3*xt1**2*xt2**2-6*xt1**2*xt2+3*xt1**2-3*xt1*
     . xt2**3+4*xt1*xt2**2+xt1*xt2-2*xt1+2*xt2**3-4*xt2**2+2*xt2)+log
     . (xt2)**2*xt2*(2*xt1**3*xt2+xt1**3-6*xt1**2*xt2**2-xt1**2*xt2-2
     . *xt1**2+12*xt1*xt2**2-4*xt1*xt2+xt1-6*xt2**2+3*xt2)+ans2
      r92=ans1/(8*(xt1**4*xt2**2-2*xt1**4*xt2+xt1**4-2*xt1**3*xt2**3+
     . 2*xt1**3*xt2**2+2*xt1**3*xt2-2*xt1**3+xt1**2*xt2**4+2*xt1**2*
     . xt2**3-6*xt1**2*xt2**2+2*xt1**2*xt2+xt1**2-2*xt1*xt2**4+2*xt1*
     . xt2**3+2*xt1*xt2**2-2*xt1*xt2+xt2**4-2*xt2**3+xt2**2))

      mt1 = amst1
      mt2 = amst2
      xt1 = amst1**2/amg**2 * rim
      xt2 = amst2**2/amg**2 * rim

      ralsca2=(-((9*log(xb1)-10)*(xb2-1)*log(xb1)*xb1-(9*log(xb2)-10)
     . *(xb1-1)*log(xb2)*xb2))/(48*(xb1-xb2)*(xb1-1)*(xb2-1))

      ralscf2=(-((xb1-1)*log(xb2)*xb2-(xb2-1)*log(xb1)*xb1))/(8*(xb1-
     . xb2)*(xb1-1)*(xb2-1))

      rmb12=(-((((2*xb1**3-3*xb2-(xb2-6)*xb1**2-2*(xb2+1)*xb1)*xb1+(
     . xb1**2-xb2)*(xb1-1)**2*log(-(xb1-1)))*(xb2-1)+(xb1-1)**2*log(
     . xb2)*xb1**2*xb2)*log(xb1)-(((xb1**2-xb2)*(xb1+1)*(xb2-1)*log(
     . xb1)**2-(xb1-1)**2*log(xb2)**2*xb2)*xb1+((xb1-xb2)*(xb2-1)+(
     . xb1-1)*log(xb2)*xb2)*((xb1+5)*xb1+(xb1-1)**2*log(-(xb1-1)))*(
     . xb1-1))))/(4*(xb1-xb2)**2*(xb1-1)**2*(xb2-1)*xb1)

      rmb22=(-(((xb1-xb2**2)*(xb1-1)*(xb2+1)*log(xb2)**2+(xb2-1)**2*
     . log(xb1)**2*xb1)*xb2+((xb2+5)*xb2+(xb2-1)**2*log(-(xb2-1)))*(
     . xb1-xb2)*(xb1-1)*(xb2-1)-((xb2-1)**2*log(-(xb2-1))-log(xb2)*
     . xb2**2+(xb2+5)*xb2)*(xb2-1)**2*log(xb1)*xb1+((2*(xb2**2+3*xb2-
     . 1)*xb2-(xb2**2+2*xb2+3)*xb1)*xb2-(xb1-xb2**2)*(xb2-1)**2*log(-
     . (xb2-1)))*(xb1-1)*log(xb2)))/(4*(xb1-xb2)**2*(xb1-1)*(xb2-1)**
     . 2*xb2)

      rmgca2=(-((3*log(xb1)-14)*(xb1+1)*(xb2-1)**2*log(xb1)*xb1-(3*
     . log(xb2)-14)*(xb1-1)**2*(xb2+1)*log(xb2)*xb2-28*(xb1-xb2)*(xb1
     . -1)*(xb2-1)))/(16*(xb1-xb2)*(xb1-1)**2*(xb2-1)**2)

      ms1 = amsu1
      ms2 = amsu2
      xs1 = amsu1**2/amg**2 * rim
      xs2 = amsu2**2/amg**2 * rim

      ans2=2*t134p(mb2,ms1,mg)*(xb1**2*xb2-xb1**2*xs1-2*xb1*xb2+2*xb1
     . *xs1+xb2-xs1)+2*t134p(mb2,ms2,mg)*(xb1**2*xb2-xb1**2*xs2-2*xb1
     . *xb2+2*xb1*xs2+xb2-xs2)+2*t134p(mg,ms1,mg)*(-2*xb1**2*xb2+xb1
     . **2*xs1+xb1**2+2*xb1*xb2**2-2*xb1*xs1-xb2**2*xs1-xb2**2+2*xb2*
     . xs1)+2*t134p(mg,ms2,mg)*(-2*xb1**2*xb2+xb1**2*xs2+xb1**2+2*xb1
     . *xb2**2-2*xb1*xs2-xb2**2*xs2-xb2**2+2*xb2*xs2)+12*(xb1**2*xb2*
     . xs1+xb1**2*xb2*xs2+xb1**2*xb2-xb1**2*xs1-xb1**2*xs2-xb1**2-xb1
     . *xb2**2*xs1-xb1*xb2**2*xs2-xb1*xb2**2+xb1*xs1+xb1*xs2+xb1+xb2
     . **2*xs1+xb2**2*xs2+xb2**2-xb2*xs1-xb2*xs2-xb2)
      ans1=log(xb1)**2*xb1*(-xb2**2*xs1-xb2**2*xs2+2*xb2*xs1+2*xb2*
     . xs2-xs1-xs2)+2*log(xb1)*log(xs1)*xb1*xs1*(-xb2**2+2*xb2-1)+2*
     . log(xb1)*log(xs2)*xb1*xs2*(-xb2**2+2*xb2-1)+4*log(xb1)*xb1*(
     . xb2**2*xs1+xb2**2*xs2-2*xb2*xs1-2*xb2*xs2+xs1+xs2)+log(xb2)**2
     . *xb2*(xb1**2*xs1+xb1**2*xs2-2*xb1*xs1-2*xb1*xs2+xs1+xs2)+2*log
     . (xb2)*log(xs1)*xb2*xs1*(xb1**2-2*xb1+1)+2*log(xb2)*log(xs2)*
     . xb2*xs2*(xb1**2-2*xb1+1)+4*log(xb2)*xb2*(-xb1**2*xs1-xb1**2*
     . xs2+2*xb1*xs1+2*xb1*xs2-xs1-xs2)+log(xs1)**2*xs1*(xb1**2*xb2-
     . xb1**2-xb1*xb2**2+xb1+xb2**2-xb2)+8*log(xs1)*xs1*(-xb1**2*xb2+
     . xb1**2+xb1*xb2**2-xb1-xb2**2+xb2)+log(xs2)**2*xs2*(xb1**2*xb2-
     . xb1**2-xb1*xb2**2+xb1+xb2**2-xb2)+8*log(xs2)*xs2*(-xb1**2*xb2+
     . xb1**2+xb1*xb2**2-xb1-xb2**2+xb2)+2*t134p(mb1,ms1,mg)*(-xb1*
     . xb2**2+2*xb1*xb2-xb1+xb2**2*xs1-2*xb2*xs1+xs1)+2*t134p(mb1,ms2
     . ,mg)*(-xb1*xb2**2+2*xb1*xb2-xb1+xb2**2*xs2-2*xb2*xs2+xs2)+ans2
      ru102=ans1/(8*(xb1**3*xb2**2-2*xb1**3*xb2+xb1**3-xb1**2*xb2**3+3
     . *xb1**2*xb2-2*xb1**2+2*xb1*xb2**3-3*xb1*xb2**2+xb1-xb2**3+2*
     . xb2**2-xb2))

      rualstr2=(-((log(xs2)-6+log(xs1))*((xb1-1)*log(xb2)*xb2-(xb2-1)*
     . log(xb1)*xb1)+3*((xb1-1)*log(xb2)**2*xb2-(xb2-1)*log(xb1)**2*
     . xb1)))/(24*(xb1-xb2)*(xb1-1)*(xb2-1))

      rumgtr2=((xs2-6+xs1+log(xs2)+log(xs1)+(log(xs2-1)-log(xs2))*(xs2
     . -1)**2+(log(xs1-1)-log(xs1))*(xs1-1)**2)*((xb1+1)*(xb2-1)**2*
     . log(xb1)*xb1-(xb1-1)**2*(xb2+1)*log(xb2)*xb2)+2*((log(xs2-1)-
     . log(xs2))*(xs2-1)**2+log(xs1)+log(xs2)+(log(xs1-1)-log(xs1))*(
     . xs1-1)**2)*(xb1-xb2)*(xb1-1)*(xb2-1)+(xb1+1)*(xb2-1)**2*log(
     . xb1)**2*xb1-(xb1-1)**2*(xb2+1)*log(xb2)**2*xb2+2*(xs2-6+xs1)*(
     . xb1-xb2)*(xb1-1)*(xb2-1))/(8*(xb1-xb2)*(xb1-1)**2*(xb2-1)**2)

      ms1 = amsd1
      ms2 = amsd2
      xs1 = amsd1**2/amg**2 * rim
      xs2 = amsd2**2/amg**2 * rim

      ans2=2*t134p(mb2,ms1,mg)*(xb1**2*xb2-xb1**2*xs1-2*xb1*xb2+2*xb1
     . *xs1+xb2-xs1)+2*t134p(mb2,ms2,mg)*(xb1**2*xb2-xb1**2*xs2-2*xb1
     . *xb2+2*xb1*xs2+xb2-xs2)+2*t134p(mg,ms1,mg)*(-2*xb1**2*xb2+xb1
     . **2*xs1+xb1**2+2*xb1*xb2**2-2*xb1*xs1-xb2**2*xs1-xb2**2+2*xb2*
     . xs1)+2*t134p(mg,ms2,mg)*(-2*xb1**2*xb2+xb1**2*xs2+xb1**2+2*xb1
     . *xb2**2-2*xb1*xs2-xb2**2*xs2-xb2**2+2*xb2*xs2)+12*(xb1**2*xb2*
     . xs1+xb1**2*xb2*xs2+xb1**2*xb2-xb1**2*xs1-xb1**2*xs2-xb1**2-xb1
     . *xb2**2*xs1-xb1*xb2**2*xs2-xb1*xb2**2+xb1*xs1+xb1*xs2+xb1+xb2
     . **2*xs1+xb2**2*xs2+xb2**2-xb2*xs1-xb2*xs2-xb2)
      ans1=log(xb1)**2*xb1*(-xb2**2*xs1-xb2**2*xs2+2*xb2*xs1+2*xb2*
     . xs2-xs1-xs2)+2*log(xb1)*log(xs1)*xb1*xs1*(-xb2**2+2*xb2-1)+2*
     . log(xb1)*log(xs2)*xb1*xs2*(-xb2**2+2*xb2-1)+4*log(xb1)*xb1*(
     . xb2**2*xs1+xb2**2*xs2-2*xb2*xs1-2*xb2*xs2+xs1+xs2)+log(xb2)**2
     . *xb2*(xb1**2*xs1+xb1**2*xs2-2*xb1*xs1-2*xb1*xs2+xs1+xs2)+2*log
     . (xb2)*log(xs1)*xb2*xs1*(xb1**2-2*xb1+1)+2*log(xb2)*log(xs2)*
     . xb2*xs2*(xb1**2-2*xb1+1)+4*log(xb2)*xb2*(-xb1**2*xs1-xb1**2*
     . xs2+2*xb1*xs1+2*xb1*xs2-xs1-xs2)+log(xs1)**2*xs1*(xb1**2*xb2-
     . xb1**2-xb1*xb2**2+xb1+xb2**2-xb2)+8*log(xs1)*xs1*(-xb1**2*xb2+
     . xb1**2+xb1*xb2**2-xb1-xb2**2+xb2)+log(xs2)**2*xs2*(xb1**2*xb2-
     . xb1**2-xb1*xb2**2+xb1+xb2**2-xb2)+8*log(xs2)*xs2*(-xb1**2*xb2+
     . xb1**2+xb1*xb2**2-xb1-xb2**2+xb2)+2*t134p(mb1,ms1,mg)*(-xb1*
     . xb2**2+2*xb1*xb2-xb1+xb2**2*xs1-2*xb2*xs1+xs1)+2*t134p(mb1,ms2
     . ,mg)*(-xb1*xb2**2+2*xb1*xb2-xb1+xb2**2*xs2-2*xb2*xs2+xs2)+ans2
      rd102=ans1/(8*(xb1**3*xb2**2-2*xb1**3*xb2+xb1**3-xb1**2*xb2**3+3
     . *xb1**2*xb2-2*xb1**2+2*xb1*xb2**3-3*xb1*xb2**2+xb1-xb2**3+2*
     . xb2**2-xb2))

      rdalstr2=(-((log(xs2)-6+log(xs1))*((xb1-1)*log(xb2)*xb2-(xb2-1)*
     . log(xb1)*xb1)+3*((xb1-1)*log(xb2)**2*xb2-(xb2-1)*log(xb1)**2*
     . xb1)))/(24*(xb1-xb2)*(xb1-1)*(xb2-1))

      rdmgtr2=((xs2-6+xs1+log(xs2)+log(xs1)+(log(xs2-1)-log(xs2))*(xs2
     . -1)**2+(log(xs1-1)-log(xs1))*(xs1-1)**2)*((xb1+1)*(xb2-1)**2*
     . log(xb1)*xb1-(xb1-1)**2*(xb2+1)*log(xb2)*xb2)+2*((log(xs2-1)-
     . log(xs2))*(xs2-1)**2+log(xs1)+log(xs2)+(log(xs1-1)-log(xs1))*(
     . xs1-1)**2)*(xb1-xb2)*(xb1-1)*(xb2-1)+(xb1+1)*(xb2-1)**2*log(
     . xb1)**2*xb1-(xb1-1)**2*(xb2+1)*log(xb2)**2*xb2+2*(xs2-6+xs1)*(
     . xb1-xb2)*(xb1-1)*(xb2-1))/(8*(xb1-xb2)*(xb1-1)**2*(xb2-1)**2)

      ms1 = amsb1
      ms2 = amsb2
      xs1 = amsb1**2/amg**2 * rim
      xs2 = amsb2**2/amg**2 * rim

      ans2=2*t134p(mb2,ms1,mg)*(xb1**2*xb2-xb1**2*xs1-2*xb1*xb2+2*xb1
     . *xs1+xb2-xs1)+2*t134p(mb2,ms2,mg)*(xb1**2*xb2-xb1**2*xs2-2*xb1
     . *xb2+2*xb1*xs2+xb2-xs2)+2*t134p(mg,ms1,mg)*(-2*xb1**2*xb2+xb1
     . **2*xs1+xb1**2+2*xb1*xb2**2-2*xb1*xs1-xb2**2*xs1-xb2**2+2*xb2*
     . xs1)+2*t134p(mg,ms2,mg)*(-2*xb1**2*xb2+xb1**2*xs2+xb1**2+2*xb1
     . *xb2**2-2*xb1*xs2-xb2**2*xs2-xb2**2+2*xb2*xs2)+12*(xb1**2*xb2*
     . xs1+xb1**2*xb2*xs2+xb1**2*xb2-xb1**2*xs1-xb1**2*xs2-xb1**2-xb1
     . *xb2**2*xs1-xb1*xb2**2*xs2-xb1*xb2**2+xb1*xs1+xb1*xs2+xb1+xb2
     . **2*xs1+xb2**2*xs2+xb2**2-xb2*xs1-xb2*xs2-xb2)
      ans1=log(xb1)**2*xb1*(-xb2**2*xs1-xb2**2*xs2+2*xb2*xs1+2*xb2*
     . xs2-xs1-xs2)+2*log(xb1)*log(xs1)*xb1*xs1*(-xb2**2+2*xb2-1)+2*
     . log(xb1)*log(xs2)*xb1*xs2*(-xb2**2+2*xb2-1)+4*log(xb1)*xb1*(
     . xb2**2*xs1+xb2**2*xs2-2*xb2*xs1-2*xb2*xs2+xs1+xs2)+log(xb2)**2
     . *xb2*(xb1**2*xs1+xb1**2*xs2-2*xb1*xs1-2*xb1*xs2+xs1+xs2)+2*log
     . (xb2)*log(xs1)*xb2*xs1*(xb1**2-2*xb1+1)+2*log(xb2)*log(xs2)*
     . xb2*xs2*(xb1**2-2*xb1+1)+4*log(xb2)*xb2*(-xb1**2*xs1-xb1**2*
     . xs2+2*xb1*xs1+2*xb1*xs2-xs1-xs2)+log(xs1)**2*xs1*(xb1**2*xb2-
     . xb1**2-xb1*xb2**2+xb1+xb2**2-xb2)+8*log(xs1)*xs1*(-xb1**2*xb2+
     . xb1**2+xb1*xb2**2-xb1-xb2**2+xb2)+log(xs2)**2*xs2*(xb1**2*xb2-
     . xb1**2-xb1*xb2**2+xb1+xb2**2-xb2)+8*log(xs2)*xs2*(-xb1**2*xb2+
     . xb1**2+xb1*xb2**2-xb1-xb2**2+xb2)+2*t134p(mb1,ms1,mg)*(-xb1*
     . xb2**2+2*xb1*xb2-xb1+xb2**2*xs1-2*xb2*xs1+xs1)+2*t134p(mb1,ms2
     . ,mg)*(-xb1*xb2**2+2*xb1*xb2-xb1+xb2**2*xs2-2*xb2*xs2+xs2)+ans2
      rb102=ans1/(8*(xb1**3*xb2**2-2*xb1**3*xb2+xb1**3-xb1**2*xb2**3+3
     . *xb1**2*xb2-2*xb1**2+2*xb1*xb2**3-3*xb1*xb2**2+xb1-xb2**3+2*
     . xb2**2-xb2))

      rbalstr2=(-((log(xs2)-6+log(xs1))*((xb1-1)*log(xb2)*xb2-(xb2-1)*
     . log(xb1)*xb1)+3*((xb1-1)*log(xb2)**2*xb2-(xb2-1)*log(xb1)**2*
     . xb1)))/(24*(xb1-xb2)*(xb1-1)*(xb2-1))

      rbmgtr2=((xs2-6+xs1+log(xs2)+log(xs1)+(log(xs2-1)-log(xs2))*(xs2
     . -1)**2+(log(xs1-1)-log(xs1))*(xs1-1)**2)*((xb1+1)*(xb2-1)**2*
     . log(xb1)*xb1-(xb1-1)**2*(xb2+1)*log(xb2)*xb2)+2*((log(xs2-1)-
     . log(xs2))*(xs2-1)**2+log(xs1)+log(xs2)+(log(xs1-1)-log(xs1))*(
     . xs1-1)**2)*(xb1-xb2)*(xb1-1)*(xb2-1)+(xb1+1)*(xb2-1)**2*log(
     . xb1)**2*xb1-(xb1-1)**2*(xb2+1)*log(xb2)**2*xb2+2*(xs2-6+xs1)*(
     . xb1-xb2)*(xb1-1)*(xb2-1))/(8*(xb1-xb2)*(xb1-1)**2*(xb2-1)**2)

      ms1 = amst1
      ms2 = amst2
      xs1 = amst1**2/amg**2 * rim
      xs2 = amst2**2/amg**2 * rim

      ans14=-8*log(xs2)*xb1*xb2**2*xs2-4*log(xs2)*xb1*xq**2*xs2-4*log
     . (xs2)*xb1*xq*xs2**2-4*log(xs2)*xb1*xq*xs2+8*log(xs2)*xb1*xs2**
     . 3-16*log(xs2)*xb1*xs2**2+8*log(xs2)*xb1*xs2-4*log(xs2)*xb2**2*
     . xq**2*xs2-4*log(xs2)*xb2**2*xq*xs2**2-4*log(xs2)*xb2**2*xq*xs2
     . +8*log(xs2)*xb2**2*xs2**3-16*log(xs2)*xb2**2*xs2**2+8*log(xs2)
     . *xb2**2*xs2+4*log(xs2)*xb2*xq**2*xs2+4*log(xs2)*xb2*xq*xs2**2+
     . 4*log(xs2)*xb2*xq*xs2-8*log(xs2)*xb2*xs2**3+16*log(xs2)*xb2*
     . xs2**2-8*log(xs2)*xb2*xs2
      ans13=-log(xs2)**2*xb1*xb2**2*xq**2*xs2+log(xs2)**2*xb1*xb2**2*
     . xs2**3-2*log(xs2)**2*xb1*xb2**2*xs2**2+log(xs2)**2*xb1*xb2**2*
     . xs2+log(xs2)**2*xb1*xq**2*xs2-log(xs2)**2*xb1*xs2**3+2*log(xs2
     . )**2*xb1*xs2**2-log(xs2)**2*xb1*xs2+log(xs2)**2*xb2**2*xq**2*
     . xs2-log(xs2)**2*xb2**2*xs2**3+2*log(xs2)**2*xb2**2*xs2**2-log(
     . xs2)**2*xb2**2*xs2-log(xs2)**2*xb2*xq**2*xs2+log(xs2)**2*xb2*
     . xs2**3-2*log(xs2)**2*xb2*xs2**2+log(xs2)**2*xb2*xs2-4*log(xs2)
     . *xb1**2*xb2*xq**2*xs2-4*log(xs2)*xb1**2*xb2*xq*xs2**2-4*log(
     . xs2)*xb1**2*xb2*xq*xs2+8*log(xs2)*xb1**2*xb2*xs2**3-16*log(xs2
     . )*xb1**2*xb2*xs2**2+8*log(xs2)*xb1**2*xb2*xs2+4*log(xs2)*xb1**
     . 2*xq**2*xs2+4*log(xs2)*xb1**2*xq*xs2**2+4*log(xs2)*xb1**2*xq*
     . xs2-8*log(xs2)*xb1**2*xs2**3+16*log(xs2)*xb1**2*xs2**2-8*log(
     . xs2)*xb1**2*xs2+4*log(xs2)*xb1*xb2**2*xq**2*xs2+4*log(xs2)*xb1
     . *xb2**2*xq*xs2**2+4*log(xs2)*xb1*xb2**2*xq*xs2-8*log(xs2)*xb1*
     . xb2**2*xs2**3+16*log(xs2)*xb1*xb2**2*xs2**2+ans14
      ans12=-4*log(xb2)**2*xb1*xb2*xq*xs1-8*log(xb2)**2*xb1*xb2*xq*
     . xs2**2+4*log(xb2)**2*xb1*xb2*xq*xs2-4*log(xb2)**2*xb1*xb2*xq+2
     . *log(xb2)**2*xb1*xb2*xs1*xs2**2-4*log(xb2)**2*xb1*xb2*xs1*xs2+
     . 2*log(xb2)**2*xb1*xb2*xs1+2*log(xb2)**2*xb1*xb2*xs2**3-4*log(
     . xb2)**2*xb1*xb2*xs2**2+2*log(xb2)**2*xb1*xb2*xs2+2*log(xb2)**2
     . *xb2*xq**3-log(xb2)**2*xb2*xq**2*xs1-5*log(xb2)**2*xb2*xq**2*
     . xs2-4*log(xb2)**2*xb2*xq**2+2*log(xb2)**2*xb2*xq*xs1*xs2+2*log
     . (xb2)**2*xb2*xq*xs1+4*log(xb2)**2*xb2*xq*xs2**2-2*log(xb2)**2*
     . xb2*xq*xs2+2*log(xb2)**2*xb2*xq-log(xb2)**2*xb2*xs1*xs2**2+2*
     . log(xb2)**2*xb2*xs1*xs2-log(xb2)**2*xb2*xs1-log(xb2)**2*xb2*
     . xs2**3+2*log(xb2)**2*xb2*xs2**2-log(xb2)**2*xb2*xs2+log(xs2)**
     . 2*xb1**2*xb2*xq**2*xs2-log(xs2)**2*xb1**2*xb2*xs2**3+2*log(xs2
     . )**2*xb1**2*xb2*xs2**2-log(xs2)**2*xb1**2*xb2*xs2-log(xs2)**2*
     . xb1**2*xq**2*xs2+log(xs2)**2*xb1**2*xs2**3-2*log(xs2)**2*xb1**
     . 2*xs2**2+log(xs2)**2*xb1**2*xs2+ans13
      ans11=4*log(xb1)**2*xb1*xq**2-2*log(xb1)**2*xb1*xq*xs1*xs2-2*
     . log(xb1)**2*xb1*xq*xs1-4*log(xb1)**2*xb1*xq*xs2**2+2*log(xb1)
     . **2*xb1*xq*xs2-2*log(xb1)**2*xb1*xq+log(xb1)**2*xb1*xs1*xs2**2
     . -2*log(xb1)**2*xb1*xs1*xs2+log(xb1)**2*xb1*xs1+log(xb1)**2*xb1
     . *xs2**3-2*log(xb1)**2*xb1*xs2**2+log(xb1)**2*xb1*xs2+2*log(xb2
     . )**2*xb1**2*xb2*xq**3-log(xb2)**2*xb1**2*xb2*xq**2*xs1-5*log(
     . xb2)**2*xb1**2*xb2*xq**2*xs2-4*log(xb2)**2*xb1**2*xb2*xq**2+2*
     . log(xb2)**2*xb1**2*xb2*xq*xs1*xs2+2*log(xb2)**2*xb1**2*xb2*xq*
     . xs1+4*log(xb2)**2*xb1**2*xb2*xq*xs2**2-2*log(xb2)**2*xb1**2*
     . xb2*xq*xs2+2*log(xb2)**2*xb1**2*xb2*xq-log(xb2)**2*xb1**2*xb2*
     . xs1*xs2**2+2*log(xb2)**2*xb1**2*xb2*xs1*xs2-log(xb2)**2*xb1**2
     . *xb2*xs1-log(xb2)**2*xb1**2*xb2*xs2**3+2*log(xb2)**2*xb1**2*
     . xb2*xs2**2-log(xb2)**2*xb1**2*xb2*xs2-4*log(xb2)**2*xb1*xb2*xq
     . **3+2*log(xb2)**2*xb1*xb2*xq**2*xs1+10*log(xb2)**2*xb1*xb2*xq
     . **2*xs2+8*log(xb2)**2*xb1*xb2*xq**2-4*log(xb2)**2*xb1*xb2*xq*
     . xs1*xs2+ans12
      ans10=5*log(xb1)**2*xb1*xb2**2*xq**2*xs2+4*log(xb1)**2*xb1*xb2
     . **2*xq**2-2*log(xb1)**2*xb1*xb2**2*xq*xs1*xs2-2*log(xb1)**2*
     . xb1*xb2**2*xq*xs1-4*log(xb1)**2*xb1*xb2**2*xq*xs2**2+2*log(xb1
     . )**2*xb1*xb2**2*xq*xs2-2*log(xb1)**2*xb1*xb2**2*xq+log(xb1)**2
     . *xb1*xb2**2*xs1*xs2**2-2*log(xb1)**2*xb1*xb2**2*xs1*xs2+log(
     . xb1)**2*xb1*xb2**2*xs1+log(xb1)**2*xb1*xb2**2*xs2**3-2*log(xb1
     . )**2*xb1*xb2**2*xs2**2+log(xb1)**2*xb1*xb2**2*xs2+4*log(xb1)**
     . 2*xb1*xb2*xq**3-2*log(xb1)**2*xb1*xb2*xq**2*xs1-10*log(xb1)**2
     . *xb1*xb2*xq**2*xs2-8*log(xb1)**2*xb1*xb2*xq**2+4*log(xb1)**2*
     . xb1*xb2*xq*xs1*xs2+4*log(xb1)**2*xb1*xb2*xq*xs1+8*log(xb1)**2*
     . xb1*xb2*xq*xs2**2-4*log(xb1)**2*xb1*xb2*xq*xs2+4*log(xb1)**2*
     . xb1*xb2*xq-2*log(xb1)**2*xb1*xb2*xs1*xs2**2+4*log(xb1)**2*xb1*
     . xb2*xs1*xs2-2*log(xb1)**2*xb1*xb2*xs1-2*log(xb1)**2*xb1*xb2*
     . xs2**3+4*log(xb1)**2*xb1*xb2*xs2**2-2*log(xb1)**2*xb1*xb2*xs2-
     . 2*log(xb1)**2*xb1*xq**3+log(xb1)**2*xb1*xq**2*xs1+5*log(xb1)**
     . 2*xb1*xq**2*xs2+ans11
      ans9=-4*t134(mb1,mq,ms2,mg)*xb1*xb2+2*t134(mb1,mq,ms2,mg)*xb1*
     . xq**2-4*t134(mb1,mq,ms2,mg)*xb1*xq*xs2-4*t134(mb1,mq,ms2,mg)*
     . xb1*xq+2*t134(mb1,mq,ms2,mg)*xb1*xs2**2-4*t134(mb1,mq,ms2,mg)*
     . xb1*xs2+2*t134(mb1,mq,ms2,mg)*xb1+2*t134(mb1,mq,ms2,mg)*xb2**2
     . *xq**3-6*t134(mb1,mq,ms2,mg)*xb2**2*xq**2*xs2-4*t134(mb1,mq,
     . ms2,mg)*xb2**2*xq**2+6*t134(mb1,mq,ms2,mg)*xb2**2*xq*xs2**2+2*
     . t134(mb1,mq,ms2,mg)*xb2**2*xq-2*t134(mb1,mq,ms2,mg)*xb2**2*xs2
     . **3+4*t134(mb1,mq,ms2,mg)*xb2**2*xs2**2-2*t134(mb1,mq,ms2,mg)*
     . xb2**2*xs2-4*t134(mb1,mq,ms2,mg)*xb2*xq**3+12*t134(mb1,mq,ms2,
     . mg)*xb2*xq**2*xs2+8*t134(mb1,mq,ms2,mg)*xb2*xq**2-12*t134(mb1,
     . mq,ms2,mg)*xb2*xq*xs2**2-4*t134(mb1,mq,ms2,mg)*xb2*xq+4*t134(
     . mb1,mq,ms2,mg)*xb2*xs2**3-8*t134(mb1,mq,ms2,mg)*xb2*xs2**2+4*
     . t134(mb1,mq,ms2,mg)*xb2*xs2+2*t134(mb1,mq,ms2,mg)*xq**3-6*t134
     . (mb1,mq,ms2,mg)*xq**2*xs2-4*t134(mb1,mq,ms2,mg)*xq**2+6*t134(
     . mb1,mq,ms2,mg)*xq*xs2**2+2*t134(mb1,mq,ms2,mg)*xq-2*t134(mb1,
     . mq,ms2,mg)*xs2**3+4*t134(mb1,mq,ms2,mg)*xs2**2-2*t134(mb1,mq,
     . ms2,mg)*xs2-2*log(xb1)**2*xb1*xb2**2*xq**3+log(xb1)**2*xb1*xb2
     . **2*xq**2*xs1+ans10
      ans8=4*t134(mb1,mq,ms1,mg)*xb2*xq**2*xs1+8*t134(mb1,mq,ms1,mg)*
     . xb2*xq**2*xs2+8*t134(mb1,mq,ms1,mg)*xb2*xq**2-8*t134(mb1,mq,
     . ms1,mg)*xb2*xq*xs1*xs2-8*t134(mb1,mq,ms1,mg)*xb2*xq*xs1-4*t134
     . (mb1,mq,ms1,mg)*xb2*xq*xs2**2+8*t134(mb1,mq,ms1,mg)*xb2*xq*xs2
     . -4*t134(mb1,mq,ms1,mg)*xb2*xq+4*t134(mb1,mq,ms1,mg)*xb2*xs1*
     . xs2**2-8*t134(mb1,mq,ms1,mg)*xb2*xs1*xs2+4*t134(mb1,mq,ms1,mg)
     . *xb2*xs1+2*t134(mb1,mq,ms1,mg)*xq**3-2*t134(mb1,mq,ms1,mg)*xq
     . **2*xs1-4*t134(mb1,mq,ms1,mg)*xq**2*xs2-4*t134(mb1,mq,ms1,mg)*
     . xq**2+4*t134(mb1,mq,ms1,mg)*xq*xs1*xs2+4*t134(mb1,mq,ms1,mg)*
     . xq*xs1+2*t134(mb1,mq,ms1,mg)*xq*xs2**2-4*t134(mb1,mq,ms1,mg)*
     . xq*xs2+2*t134(mb1,mq,ms1,mg)*xq-2*t134(mb1,mq,ms1,mg)*xs1*xs2
     . **2+4*t134(mb1,mq,ms1,mg)*xs1*xs2-2*t134(mb1,mq,ms1,mg)*xs1+2*
     . t134(mb1,mq,ms2,mg)*xb1*xb2**2*xq**2-4*t134(mb1,mq,ms2,mg)*xb1
     . *xb2**2*xq*xs2-4*t134(mb1,mq,ms2,mg)*xb1*xb2**2*xq+2*t134(mb1,
     . mq,ms2,mg)*xb1*xb2**2*xs2**2-4*t134(mb1,mq,ms2,mg)*xb1*xb2**2*
     . xs2+2*t134(mb1,mq,ms2,mg)*xb1*xb2**2-4*t134(mb1,mq,ms2,mg)*xb1
     . *xb2*xq**2+8*t134(mb1,mq,ms2,mg)*xb1*xb2*xq*xs2+8*t134(mb1,mq,
     . ms2,mg)*xb1*xb2*xq-4*t134(mb1,mq,ms2,mg)*xb1*xb2*xs2**2+8*t134
     . (mb1,mq,ms2,mg)*xb1*xb2*xs2+ans9
      ans7=2*t134(mb1,mq,ms1,mg)*xb1*xb2**2*xq**2-4*t134(mb1,mq,ms1,
     . mg)*xb1*xb2**2*xq*xs2-4*t134(mb1,mq,ms1,mg)*xb1*xb2**2*xq+2*
     . t134(mb1,mq,ms1,mg)*xb1*xb2**2*xs2**2-4*t134(mb1,mq,ms1,mg)*
     . xb1*xb2**2*xs2+2*t134(mb1,mq,ms1,mg)*xb1*xb2**2-4*t134(mb1,mq,
     . ms1,mg)*xb1*xb2*xq**2+8*t134(mb1,mq,ms1,mg)*xb1*xb2*xq*xs2+8*
     . t134(mb1,mq,ms1,mg)*xb1*xb2*xq-4*t134(mb1,mq,ms1,mg)*xb1*xb2*
     . xs2**2+8*t134(mb1,mq,ms1,mg)*xb1*xb2*xs2-4*t134(mb1,mq,ms1,mg)
     . *xb1*xb2+2*t134(mb1,mq,ms1,mg)*xb1*xq**2-4*t134(mb1,mq,ms1,mg)
     . *xb1*xq*xs2-4*t134(mb1,mq,ms1,mg)*xb1*xq+2*t134(mb1,mq,ms1,mg)
     . *xb1*xs2**2-4*t134(mb1,mq,ms1,mg)*xb1*xs2+2*t134(mb1,mq,ms1,mg
     . )*xb1+2*t134(mb1,mq,ms1,mg)*xb2**2*xq**3-2*t134(mb1,mq,ms1,mg)
     . *xb2**2*xq**2*xs1-4*t134(mb1,mq,ms1,mg)*xb2**2*xq**2*xs2-4*
     . t134(mb1,mq,ms1,mg)*xb2**2*xq**2+4*t134(mb1,mq,ms1,mg)*xb2**2*
     . xq*xs1*xs2+4*t134(mb1,mq,ms1,mg)*xb2**2*xq*xs1+2*t134(mb1,mq,
     . ms1,mg)*xb2**2*xq*xs2**2-4*t134(mb1,mq,ms1,mg)*xb2**2*xq*xs2+2
     . *t134(mb1,mq,ms1,mg)*xb2**2*xq-2*t134(mb1,mq,ms1,mg)*xb2**2*
     . xs1*xs2**2+4*t134(mb1,mq,ms1,mg)*xb2**2*xs1*xs2-2*t134(mb1,mq,
     . ms1,mg)*xb2**2*xs1-4*t134(mb1,mq,ms1,mg)*xb2*xq**3+ans8
      ans15=(xq**2-2*xq*xs1-2*xq+xs1**2-2*xs1+1)
      ans6=ans7*ans15
      ans5=-ans6
      ans4=(4*(2*(xs1-1)**2-xq**2-(xs1+1)*xq)-(xs1-1+xq)*(xs1-1-xq)*
     . log(xs1))*(2*(xs2+1)*xq-(xs2-1)**2-xq**2)*(xb1-xb2)*(xb1-1)*(
     . xb2-1)*log(xs1)*xs1+ans5
      ans3=-ans4
      ans17=4*(3*((xs1+1)*xs1+xs2**2+xs2-1)+2*(3*xq**2+2)*xq+((2*xq**
     . 2-5*xq+8)*xq-3*(xs1+xs2)**2)*(xs1+xs2)-(4*xq-3*xs1*xs2)*(2*xs1
     . **2+3*xs1*xs2+2*xs2**2)+2*(3*xs1**2-8*xs1*xs2+3*xs2**2)*(xs1+
     . xs2)*xq-(13*xq**2+4*xs1*xs2)*xq**2+((3*xs1**2-2*xs1*xs2+3*xs2
     . **2)*xq-2*(xs1+xs2)*xq**2-3*(xs1+xs2)*xs1*xs2+6*xq**3)*(xq-xs1
     . )*(xq-xs2))*(xb1-xb2)*(xb1-1)*(xb2-1)+4*(2*((xs2-1)**2+xs1**2+
     . 2*(2*xs2-1)*xs1+(5*xq**2-1)*xq)-(xs1**2-4*xs1*xs2+xs2**2)*xq-2
     . *(xq**2+2*xs1*xs2)*(xs1+xs2)+(xs1-1-xq)*(2*(xs2+1)*xq-(xs2-1)
     . **2-xq**2)*log(xs1)*xs1+(2*(xs1+1)*xq-(xs1-1)**2-xq**2)*(xs2-1
     . -xq)*log(xs2)*xs2+(xs1+xs2-6*xq)*xq+((xs1+xs2)*xq-4*xq**2+2*
     . xs1*xs2)*(xq-xs1)*(xq-xs2))*(xb1-xb2)*(xb1-1)*(xb2-1)*log(xq)*
     . xq
      ans16=-2*(2*((xs1-1)**2*xs1-xq**3-(3*xs1-1)*xq*xs1+(3*xs1+1)*xq
     . **2)+(xq**2-2*xq*xs1+xs1**2-2*xs1+1)*(xq-xs1-1)*xb2-(2*((xs1+1
     . )*xq-(xs1-1)**2)*xb2-(xq**2-2*xq*xs1+xs1**2-2*xs1+1)*(xq-xs1-1
     . ))*xb1)*(2*(xs2+1)*xq-(xs2-1)**2-xq**2)*(xb1-xb2)*t134(mg,mq,
     . ms1,mg)-2*((xs2-1)**2+xs1**2+2*(2*xs2-1)*xs1+2*(xq+1)*(xq-1)*
     . xq+(xq-2*xs1*xs2)*(xs1+xs2)-(xs1**2-4*xs1*xs2+xs2**2)*xq-(xq**
     . 2-xs1*xs2)*(xq-xs1)*(xq-xs2))*(xb1-xb2)*(xb1-1)*(xb2-1)*log(xq
     . )**2*xq-2*((2*((xs2-1)**2*xs2-xq**3-(3*xs2-1)*xq*xs2+(3*xs2+1)
     . *xq**2)+(xq**2-2*xq*xs2+xs2**2-2*xs2+1)*(xq-xs2-1)*xb2-(2*((
     . xs2+1)*xq-(xs2-1)**2)*xb2-(xq**2-2*xq*xs2+xs2**2-2*xs2+1)*(xq-
     . xs2-1))*xb1)*(xb1-xb2)*t134(mg,mq,ms2,mg)+((xq-xs1+xb2)*t134(
     . mb2,mq,ms1,mg)+(xq-xs2+xb2)*t134(mb2,mq,ms2,mg))*(2*(xs2+1)*xq
     . -(xs2-1)**2-xq**2)*(xb1-1)**2)*(2*(xs1+1)*xq-(xs1-1)**2-xq**2)
     . +ans17
      ans2=2*(2*(xs1+xs2-2*xq)-log(xs2)*xs2-log(xs1)*xs1+2*log(xq)*xq
     . )*((xb1-1)**2*log(xb2)*xb2-(xb2-1)**2*log(xb1)*xb1)*(2*(xs1+1)
     . *xq-(xs1-1)**2-xq**2)*(2*(xs2+1)*xq-(xs2-1)**2-xq**2)+ans3+
     . ans16
      ans1=-ans2
      rt102=ans1/(8*((xs1-1)**2+xq**2-2*(xs1+1)*xq)*((xs2-1)**2+xq**2-
     . 2*(xs2+1)*xq)*(xb1-xb2)*(xb1-1)**2*(xb2-1)**2)

      rtalstr2=(-((log(xs2)-6+log(xs1))*((xb1-1)*log(xb2)*xb2-(xb2-1)*
     . log(xb1)*xb1)+3*((xb1-1)*log(xb2)**2*xb2-(xb2-1)*log(xb1)**2*
     . xb1)))/(24*(xb1-xb2)*(xb1-1)*(xb2-1))

      rtmgtr2=((xs2-6+xs1-2*xq+(xq+1)*log(xs2)+(xq+1)*log(xs1)-2*log(
     . xq)*xq-(xs2-1-xq)*log(xp(ms2))*xp(ms2)-(xs1-1-xq)*log(xp(ms1))
     . *xp(ms1)-(xs2-1-xq)*log(xm(ms2))*xm(ms2)-(xs1-1-xq)*log(xm(ms1
     . ))*xm(ms1)+(xs2-1-xq)*log(xp(ms2)-1)*xp(ms2)+(xs1-1-xq)*log(xp
     . (ms1)-1)*xp(ms1)+(xs2-1-xq)*log(xm(ms2)-1)*xm(ms2)+(xs1-1-xq)*
     . log(xm(ms1)-1)*xm(ms1))*((xb1+1)*(xb2-1)**2*log(xb1)*xb1-(xb1-
     . 1)**2*(xb2+1)*log(xb2)*xb2)+2*((log(xs1)+log(xs2))*(xq+1)-2*
     . log(xq)*xq)*(xb1-xb2)*(xb1-1)*(xb2-1)+(xb1+1)*(xb2-1)**2*log(
     . xb1)**2*xb1-(xb1-1)**2*(xb2+1)*log(xb2)**2*xb2+2*((log(xm(ms2)
     . -1)-log(xm(ms2)))*xm(ms2)+(log(xp(ms2)-1)-log(xp(ms2)))*xp(ms2
     . ))*(xs2-1-xq)*(xb1-xb2)*(xb1-1)*(xb2-1)+2*((log(xm(ms1)-1)-log
     . (xm(ms1)))*xm(ms1)+(log(xp(ms1)-1)-log(xp(ms1)))*xp(ms1))*(xs1
     . -1-xq)*(xb1-xb2)*(xb1-1)*(xb2-1)+2*(xs2-6+xs1-2*xq)*(xb1-xb2)*
     . (xb1-1)*(xb2-1))/(8*(xb1-xb2)*(xb1-1)**2*(xb2-1)**2)

      rctca = ralsca2 + rmgca2
      rctcf = ralscf2 + rmb12 + rmb22
      ructtr = rualstr2 + rumgtr2
      rdcttr = rdalstr2 + rdmgtr2
      rbcttr = rbalstr2 + rbmgtr2
      rtcttr = rtalstr2 + rtmgtr2

      rtp102 = 0

      bo  =-2*fi(amsb1**2,amsb2**2,amg**2)

      rca = r12 + r22/4 + r32 + r52 + r62 + rctca
      rcf = -r22/2 - r42/2 - 2*r52 - r72/2 + r82 - r92/2 + rctcf
      rtr = nu*(ru102 + ructtr) + nd*(rd102 + rdcttr)
      rtrb= rb102 + rbcttr
      rtrt= rt102 + rtp102 + rtcttr + bo/3*dlog(amg**2/amt**2)/fnorm

      rqcd = ca*rca + cf*rcf + tr*(rtr+rtrb+rtrt)
      rqcd = rqcd/bo
      anomalous = - cf/4
      finscale = (11*ca-4*tr*nf)/12*dlog(scale**2/amg**2)
      fsqcd_hdec = dreal(rqcd)*fnorm + anomalous + finscale

      return
      end
 
      double precision function
     .                fal1_hdec(bm1,bmu,amg,amsb1,amsb2,st,ct)
      implicit double precision (b-h,o-q,s-z), complex*16 (a,r)
      double precision amg,amsb1,amsb2,am1,amu
      double precision mg,mb1,mb2,m1,mu
      double precision a
      double complex sp,li2,xgl,xg1,xb1,xb2
c     sp(r) = li2(r)
      fi(a,b,c) = (a*b*log(a/b)+b*c*log(b/c)+c*a*log(c/a))
     .          / (a-b)/(b-c)/(a-c)
      t134p(xa,b,c)  = t134p_hdec(xa,b,c)
      t134(xa,b,c,d) = t134_hdec(xa,b,c,d)

      pi = 4*datan(1.d0)
      zeta2 = pi**2/6
      eps = 1.d-15
      icontribution = 0

      am1 = dabs(bm1)
      amu = dabs(bmu)
      del = 1.d-6
      if(bm1.eq.amu) amu = dabs(bmu)*(1+del)

      fnorm = 1/am1**2

      cf = 4/3.d0

      rim = dcmplx(1.d0,eps)

      st2 = st**2
      ct2 = ct**2
      s2t = 2*st*ct
      c2t = ct**2-st**2

      m1  = am1
      mu  = amu
      mg  = amg
      mb1 = amsb1
      mb2 = amsb2

      xgl = amg**2/amu**2   * rim
      xg1 = am1**2/amu**2 * rim
      xb1 = amsb1**2/amu**2 * rim
      xb2 = amsb2**2/amu**2 * rim

c--r2
      r212=((((log(xb1)-log(xg1))*xg1-2*(xb1+2*xg1))*(log(xb1)-log(
     . xg1))*(xb2-xg1)**2*xb1-((log(xb2)-log(xg1))*xg1-2*(xb2+2*xg1))
     . *(log(xb2)-log(xg1))*(xb1-xg1)**2*xb2-((xb1+xg1)*(xb2-xg1)**2*
     . t134p(m1,mb1,m1)-(xb1-xg1)**2*(xb2+xg1)*t134p(m1,mb2,m1)+14*(
     . xb1*xb2-xg1**2)*(xb1-xb2))*xg1)*xg1)/(6*(xb1-xb2)*(xb1-xg1)**2
     . *(xb2-xg1)**2)

      ans5=-14*(((((2*xb2**2-xg1)*(xg1+1)+xb2**3-(xg1**2+xg1+1)*xb2)*
     . xb1*xg1+(xg1+1-2*xb2)*xb2*xg1**2-(xb2**2-xg1)*xb1**4)*xb2-(xb2
     . **4+2*xg1**2-(5*xb2**2+2*xg1)*(xg1+1)*xb2+(2*xg1**2+7*xg1+2)*
     . xb2**2)*xb1**3-(((xg1**2+xg1+1)*xb2-(xg1+1)*xg1)*xg1-(xg1**2+4
     . *xg1+1)*(xg1+1)*xb2**2+(2*xg1**2+7*xg1+2)*xb2**3)*xb1**2)*st2+
     . (xb1**2-xg1)*(xb2-xg1)**2*(xb2-1)**2*xb1)*(xb1-xb2)*(xg1-1)*
     . ct2
      ans4=-((((xb1+xb2)*(xb2-xg1)*(xb2-1)*t134p(mb2,mb1,m1)*ct2*xg1+
     . 14*(xb1-xb2)*(xb2**2-xg1)*xb2)*(xb1-xg1)*(xb1-1)-(xb1+xb2)*(
     . xb2-xg1)**2*(xb2-1)**2*t134p(mb1,mb2,m1)*ct2*xg1)*(xb1-1)*(xg1
     . -1)*st2+((xb1-xb2)*st2+xb2-1)*(xb1-xb2)*(xb1-xg1)*(xb1+1)*(xb2
     . -xg1)**2*(xb2-1)*t134p(mu,mb1,m1)*ct2*xg1)*(xb1-xg1)+2*(((2*(2
     . *xb1**2-xg1)-(xg1+1)*xb1+3*(xg1+1-2*xb1)*st2*xb1)*(xb2-1)*(xg1
     . -1)-((xb1-xb2)*st2+xb2-1)*(xb1-xg1)**2*log(xg1))*(xb2-xg1)-(
     . xg1+1-xb2-xb1)*(log(xb2)-log(xg1))*(xb1-xg1)*(xb1-1)*(xg1-1)*
     . st2*xb2)*(log(xb1)-log(xg1))*(xb1-xb2)*(xb2-xg1)*(xb2-1)*ct2*
     . xb1+ans5
      ans3=((((((xb1-xb2)*ct2-(xb1-1))*(xb1-xg1)**2*(xb2-xg1)*(xb2+1)
     . *t134p(mu,mb2,m1)*st2+((xb1-xb2)*st2+xb2-xg1)*(xb1+xg1)*(xb1-1
     . )*(xb2-1)**2*t134p(m1,mb1,m1)*ct2)*(xb2-xg1)-((xb1-xb2)*ct2-(
     . xb1-xg1))*(xb1-xg1)*(xb1-1)*(xb2+xg1)*(xb2-1)**2*t134p(m1,mb2,
     . m1)*st2)*xg1-((xg1+1-2*xb2)*ct2*xb2+xb2**2-xg1)*(log(xb2)-log(
     . xg1))**2*(xb1-xg1)**2*(xb1-1)*(xg1-1)*st2*xb2)*(xb1-1)-((xg1+1
     . -2*xb1)*st2*xb1+xb1**2-xg1)*(log(xb1)-log(xg1))**2*(xb2-xg1)**
     . 2*(xb2-1)**2*(xg1-1)*ct2*xb1-(((xb1-xb2)**2*st2-(xb2-1)**2*xb1
     . )*ct2-(xb1-1)**2*st2*xb2)*(xb1-xg1)**2*(xb2-xg1)**2*log(xg1)**
     . 2+2*(((2*xb1+1)*(xb2-1)**2-3*(xb1-xb2)**2*st2)*ct2+(xb1-1)**2*
     . (2*xb2+1)*st2)*(xb1-xg1)**2*(xb2-xg1)**2*log(xg1)+2*((2*(2*xb2
     . **2-xg1)-(xg1+1)*xb2+3*(xg1+1-2*xb2)*ct2*xb2)*(xb1-1)*(xg1-1)+
     . ((xb1-xb2)*ct2-(xb1-1))*(xb2-xg1)**2*log(xg1))*(log(xb2)-log(
     . xg1))*(xb1-xg1)**2*(xb1-1)*st2*xb2)*(xb1-xb2)+ans4
      ans2=ans3*xg1
      ans1=-ans2
      r222=ans1/(4*(xb1-xb2)*(xb1-xg1)**2*(xb1-1)**2*(xb2-xg1)**2*(
     . xb2-1)**2*(xg1-1))

      ans4=14*((((2*xb2**2-xg1)*(xg1+1)+xb2**3-(xg1**2+xg1+1)*xb2)*
     . xb1*xg1+(xg1+1-2*xb2)*xb2*xg1**2-(xb2**2-xg1)*xb1**4)*xb2-(xb2
     . **4+2*xg1**2-(5*xb2**2+2*xg1)*(xg1+1)*xb2+(2*xg1**2+7*xg1+2)*
     . xb2**2)*xb1**3-(((xg1**2+xg1+1)*xb2-(xg1+1)*xg1)*xg1-(xg1**2+4
     . *xg1+1)*(xg1+1)*xb2**2+(2*xg1**2+7*xg1+2)*xb2**3)*xb1**2)*(xb1
     . -xb2)*(xg1-1)
      ans3=(((xg1+1-2*xb2)*(log(xb2)-log(xg1))**2*(xb1-1)**2*(xg1-1)*
     . xb2**2+(log(xg1)+6)*(xb1-xb2)**2*(xb2-xg1)**2*log(xg1))*(xb1-
     . xg1)**2+(xg1+1-2*xb1)*(log(xb1)-log(xg1))**2*(xb2-xg1)**2*(xb2
     . -1)**2*(xg1-1)*xb1**2-2*(3*(xg1+1-2*xb2)*(xb1-1)*(xg1-1)*xb2+(
     . xb1-xb2)*(xb2-xg1)**2*log(xg1))*(log(xb2)-log(xg1))*(xb1-xg1)
     . **2*(xb1-1)*xb2-2*((3*(xg1+1-2*xb1)*(xb2-1)*(xg1-1)*xb1-(xb1-
     . xb2)*(xb1-xg1)**2*log(xg1))*(xb2-xg1)-(xg1+1-xb2-xb1)*(log(xb2
     . )-log(xg1))*(xb1-xg1)*(xb1-1)*(xg1-1)*xb2)*(log(xb1)-log(xg1))
     . *(xb2-xg1)*(xb2-1)*xb1)*(xb1-xb2)+(((((xb1+1)*(xb2-1)*t134p(mu
     . ,mb1,m1)-(xb1-1)*(xb2+1)*t134p(mu,mb2,m1))*(xb1-xg1)*(xb2-xg1)
     . **2+(xb1-1)**2*(xb2+xg1)*(xb2-1)**2*t134p(m1,mb2,m1))*(xb1-xg1
     . )-(xb1+xg1)*(xb1-1)**2*(xb2-xg1)*(xb2-1)**2*t134p(m1,mb1,m1))*
     . (xb1-xb2)**2+((xb1-xg1)*(xb1-1)*t134p(mb2,mb1,m1)-(xb2-xg1)*(
     . xb2-1)*t134p(mb1,mb2,m1))*(xb1+xb2)*(xb1-xg1)*(xb1-1)*(xb2-xg1
     . )*(xb2-1)*(xg1-1))*xg1+ans4
      ans2=3*ans3*ct2*st2*xg1
      ans1=-ans2
      r22p2=ans1/(4*(xb1-xb2)*(xb1-xg1)**2*(xb1-1)**2*(xb2-xg1)**2*(
     . xb2-1)**2*(xg1-1))

      r222 = r222 + r22p2

      ans4=14*(((((2*xb2**2-xg1)*(xg1+1)+xb2**3-(xg1**2+xg1+1)*xb2)*
     . xb1*xg1+(xg1+1-2*xb2)*xb2*xg1**2-(xb2**2-xg1)*xb1**4)*xb2-(xb2
     . **4+2*xg1**2-(5*xb2**2+2*xg1)*(xg1+1)*xb2+(2*xg1**2+7*xg1+2)*
     . xb2**2)*xb1**3-(((xg1**2+xg1+1)*xb2-(xg1+1)*xg1)*xg1-(xg1**2+4
     . *xg1+1)*(xg1+1)*xb2**2+(2*xg1**2+7*xg1+2)*xb2**3)*xb1**2)*st2+
     . (xb1-xg1)**2*(xb1-1)**2*(xb2**2-xg1)*xb2)*(xb1-xb2)*(xg1-1)*
     . ct2
      ans3=(((xb1-xb2)**2*st2-(xb1-1)**2*xb2)*ct2-(xb2-1)**2*st2*xb1)
     . *(xb1-xb2)*(xb1-xg1)**2*(xb2-xg1)**2*log(xg1)**2+2*((3*(xb1-
     . xb2)**2*st2-(xb1-1)**2*(2*xb2+1))*ct2-(2*xb1+1)*(xb2-1)**2*st2
     . )*(xb1-xb2)*(xb1-xg1)**2*(xb2-xg1)**2*log(xg1)-2*((2*(2*xb2**2
     . -xg1)-(xg1+1)*xb2+3*(xg1+1-2*xb2)*st2*xb2)*(xb1-1)*(xg1-1)+((
     . xb1-xb2)*st2-(xb1-1))*(xb2-xg1)**2*log(xg1))*(log(xb2)-log(xg1
     . ))*(xb1-xb2)*(xb1-xg1)**2*(xb1-1)*ct2*xb2-2*(((2*(2*xb1**2-xg1
     . )-(xg1+1)*xb1+3*(xg1+1-2*xb1)*ct2*xb1)*(xb2-1)*(xg1-1)-((xb1-
     . xb2)*ct2+xb2-1)*(xb1-xg1)**2*log(xg1))*(xb2-xg1)-(xg1+1-xb2-
     . xb1)*(log(xb2)-log(xg1))*(xb1-xg1)*(xb1-1)*(xg1-1)*ct2*xb2)*(
     . log(xb1)-log(xg1))*(xb1-xb2)*(xb2-xg1)*(xb2-1)*st2*xb1+ans4
      ans2=((14*((2*xb2+1+xb1**2)*xg1**2+((xb2+2)*xb1**2+xb2)*xb2-((2
     . *xb2+1)*xb1**2+(xb2+2)*xb2)*xg1)*(xb2-1)**2*st2*xb1-((xb1-xb2)
     . *st2-(xb1-1))*(xb1-xg1)**2*(xb1-1)*(xb2-xg1)**2*(xb2+1)*t134p(
     . mu,mb2,m1)*ct2+((xb1-xb2)*st2-(xb1-xg1))*(xb1-xg1)*(xb1-1)**2*
     . (xb2+xg1)*(xb2-1)**2*t134p(m1,mb2,m1)*ct2+((xb1-xb2)*ct2+xb2-1
     . )*(xb1-xg1)**2*(xb1+1)*(xb2-xg1)**2*(xb2-1)*t134p(mu,mb1,m1)*
     . st2-((xb1-xb2)*ct2+xb2-xg1)*(xb1+xg1)*(xb1-1)**2*(xb2-xg1)*(
     . xb2-1)**2*t134p(m1,mb1,m1)*st2)*xg1+((xg1+1-2*xb2)*st2*xb2+xb2
     . **2-xg1)*(log(xb2)-log(xg1))**2*(xb1-xg1)**2*(xb1-1)**2*(xg1-1
     . )*ct2*xb2+((xg1+1-2*xb1)*ct2*xb1+xb1**2-xg1)*(log(xb1)-log(xg1
     . ))**2*(xb2-xg1)**2*(xb2-1)**2*(xg1-1)*st2*xb1)*(xb1-xb2)+(((
     . xb1-xg1)*(xb1-1)*t134p(mb2,mb1,m1)-(xb2-xg1)*(xb2-1)*t134p(mb1
     . ,mb2,m1))*(xb1+xb2)*(xb1-xg1)*(xb1-1)*(xb2-xg1)*(xg1-1)*ct2*
     . xg1-14*(xb1**2*xb2**2+xg1**4)*(xb1-xb2)*(xb2-1)*xb1)*(xb2-1)*
     . st2+ans3
      ans1=ans2*xg1
      r232=ans1/(2*(xb1-xb2)*(xb1-xg1)**2*(xb1-1)**2*(xb2-xg1)**2*(
     . xb2-1)**2*(xg1-1))

      r22=r212+r222+r232

c--r4
      r412=(-((2*(log(xb1)-log(xg1))*xg1-(5*xb1+7*xg1))*(log(xb1)-log
     . (xg1))*(xb2-xg1)**2*xb1-(2*(log(xb2)-log(xg1))*xg1-(5*xb2+7*
     . xg1))*(log(xb2)-log(xg1))*(xb1-xg1)**2*xb2-2*((xb1+xg1)*(xb2-
     . xg1)**2*t134p(mb1,m1,m1)-(xb1-xg1)**2*(xb2+xg1)*t134p(mb2,m1,
     . m1)+14*(xb1*xb2-xg1**2)*(xb1-xb2))*xg1)*xg1)/(6*(xb1-xb2)*(xb1
     . -xg1)**2*(xb2-xg1)**2)

      ans3=-28*((((st2-1)*(xb2**2-3)*xb2-2)*xb1-(xb1**4+xb2**2-3*(xb2
     . **2+1)*xb1**2)*st2)*xb2-((st2-1)*(3*xb2**2-1)+2*xb2**3)*xb1**3
     . )*xg1**2+28*(((2*(2*st2-1)+(st2-1)*(xb2**2-3)*xb2)*xb1+(3*xb2
     . **2-1-(xb2**2+1)*xb1**2)*st2)*xb1-(2*(2*st2-1)*xb2-(st2-1)*(
     . xb2**2+1))*xb2)*xb1*xb2*xg1-28*((2*(2*st2-1)*xb2-(st2-1)*(xb2
     . **2+1))*xb1**3+(xb2**2+1+(xb2**2-3)*xb1**2)*st2*xb2-(2*(2*st2-
     . 1)*xb2**3-(st2-1)*(3*xb2**2-1))*xb1)*xg1**3
      ans2=((17*xb2**2-7*xg1-5*(xg1+1)*xb2)*(xg1-1)-4*(xb2-xg1)**2*
     . log(xg1)-2*(log(xb2)-log(xg1))*(xb2**2-xg1)*(xg1-1))*(log(xb2)
     . -log(xg1))*(xb1-xg1)**2*(xb1-1)**2*st2*xb2-2*(((xb1+xg1)*(xb1-
     . 1)**2*t134p(mb1,m1,m1)-(xb1-xg1)**2*(xb1+1)*t134p(mb1,mu,m1))*
     . (st2-1)*(xb2-xg1)**2*(xb2-1)**2-((xb2+xg1)*(xb2-1)**2*t134p(
     . mb2,m1,m1)-(xb2-xg1)**2*(xb2+1)*t134p(mb2,mu,m1))*(xb1-xg1)**2
     . *(xb1-1)**2*st2)*xg1+((7*xb1*xb2+5*xb1+5*xb2-17)*(xb1-xb2)*st2
     . +(7*xb1+5)*(xb2-1)**2+2*((xb1*xb2-1)*(xb1-xb2)*st2+(xb2-1)**2*
     . xb1)*log(xg1))*(xb1-xg1)**2*(xb2-xg1)**2*log(xg1)-28*(((st2-1)
     . *(xb2**2+1)+2*xb2)*xb1-(xb1**2+1)*st2*xb2)*(xb1**2*xb2**2+xg1
     . **4)-((17*xb1**2-7*xg1-5*(xg1+1)*xb1)*(xg1-1)-4*(xb1-xg1)**2*
     . log(xg1)-2*(log(xb1)-log(xg1))*(xb1**2-xg1)*(xg1-1))*(log(xb1)
     . -log(xg1))*(st2-1)*(xb2-xg1)**2*(xb2-1)**2*xb1+ans3
      ans1=ans2*xg1
      r422=ans1/(4*(xb1-xg1)**2*(xb1-1)**2*(xb2-xg1)**2*(xb2-1)**2*(
     . xg1-1))

      ans3=-28*((3*xb2**2-1-(xb2**2+1)*xb1**2)*(st2-1)*xb1+((xb2**2-4
     . *xb2+1)*st2+2*xb2)*xb2+((xb2**3-3*xb2+4)*st2-2)*xb1**2)*xb1*
     . xb2*xg1+((17*xb1**2-7*xg1-5*(xg1+1)*xb1)*(xg1-1)-4*(xb1-xg1)**
     . 2*log(xg1)-2*(log(xb1)-log(xg1))*(xb1**2-xg1)*(xg1-1))*(log(
     . xb1)-log(xg1))*(xb2-xg1)**2*(xb2-1)**2*st2*xb1-28*(((xb1**4+
     . xb2**2-3*(xb2**2+1)*xb1**2)*(st2-1)-((xb2**2-3)*st2*xb2+2)*xb1
     . )*xb2+((3*xb2**2-1)*st2-2*xb2**3)*xb1**3)*xg1**2
      ans2=2*(14*(((xb2**2+1)*st2-2*xb2)*xb1-(st2-1)*(xb1**2+1)*xb2)*
     . (xb1**2*xb2**2+xg1**4)+(log(xb2)-log(xg1))**2*(st2-1)*(xb1-xg1
     . )**2*(xb1-1)**2*(xb2**2-xg1)*(xg1-1)*xb2)-((17*xb2**2-7*xg1-5*
     . (xg1+1)*xb2)*(xg1-1)-4*(xb2-xg1)**2*log(xg1))*(log(xb2)-log(
     . xg1))*(st2-1)*(xb1-xg1)**2*(xb1-1)**2*xb2+2*(((xb1+xg1)*(xb1-1
     . )**2*t134p(mb1,m1,m1)-(xb1-xg1)**2*(xb1+1)*t134p(mb1,mu,m1))*(
     . xb2-xg1)**2*(xb2-1)**2*st2-((xb2+xg1)*(xb2-1)**2*t134p(mb2,m1,
     . m1)-(xb2-xg1)**2*(xb2+1)*t134p(mb2,mu,m1))*(st2-1)*(xb1-xg1)**
     . 2*(xb1-1)**2)*xg1-((7*xb1*xb2+5*xb1+5*xb2-17)*(xb1-xb2)*st2-(
     . xb1-1)**2*(7*xb2+5)+2*((xb1*xb2-1)*(xb1-xb2)*st2-(xb1-1)**2*
     . xb2)*log(xg1))*(xb1-xg1)**2*(xb2-xg1)**2*log(xg1)-28*(((xb2**2
     . -4*xb2+1)*st2+2*xb2)*xb1**3-(xb2**2+1+(xb2**2-3)*xb1**2)*(st2-
     . 1)*xb2+(2*(2*st2-1)*xb2**3-(3*xb2**2-1)*st2)*xb1)*xg1**3+ans3
      ans1=ans2*xg1
      r432=ans1/(2*(xb1-xg1)**2*(xb1-1)**2*(xb2-xg1)**2*(xb2-1)**2*(
     . xg1-1))

      r42=r412+r422+r432

c--r5
      r512=(-(((xb2-2*xgl+xb1)*(log(xg1)-log(xgl))*xgl-4*(xb1-xgl)*(
     . xb2-xgl))*(log(xb2)-log(xg1))*(xb1-xg1)*xb2-((log(xb1)-log(xg1
     . ))**2*(2*xb1-xgl)*(xb2-xg1)*(xb2-xgl)*xb1-(log(xb2)-log(xg1))
     . **2*(xb1-xg1)*(xb1-xgl)*(2*xb2-xgl)*xb2)-(((xb2-2*xgl+xb1)*(
     . log(xg1)-log(xgl))*xgl-4*(xb1-xgl)*(xb2-xgl))*(xb2-xg1)-(log(
     . xb2)-log(xg1))*(xb1-xb2)*(xg1-xgl)*xb2)*(log(xb1)-log(xg1))*
     . xb1+(((xb1-xb2)*(xg1-xgl)*t134p(m1,mg,m1)+(xb1-xgl)*(xb2-xg1)*
     . t134p(mb1,mg,m1)-(xb1-xg1)*(xb2-xgl)*t134p(mb2,mg,m1))*(xb2-2*
     . xgl+xb1)+((t134p(m1,mb1,m1)-t134p(mb2,mb1,m1))*(xb1-xg1)*(xb2-
     . xgl)+(t134p(m1,mb2,m1)-t134p(mb1,mb2,m1))*(xb1-xgl)*(xb2-xg1))
     . *(xb1-xb2))*xg1)*xg1)/(6*(xb1-xb2)*(xb1-xg1)*(xb1-xgl)*(xb2-
     . xg1)*(xb2-xgl))

      r522=(((log(xb1)-log(xg1))**2*(2*xb1-xg1)*(xb2-xg1)*(xb2-xgl)*
     . xb1-(log(xb2)-log(xg1))**2*(xb1-xg1)*(xb1-xgl)*(2*xb2-xg1)*xb2
     . -(log(xgl)-4-log(xg1))*(log(xg1)-log(xgl))*(xb1-xb2)*(xb1-xg1)
     . *(xb2-xg1)*xgl-((log(xg1)-log(xgl))*(xb1-xb2)*xgl-4*(xb1-xgl)*
     . (xb2-xg1))*(log(xb2)-log(xg1))*(xb1-xg1)*xb2-(((log(xg1)-log(
     . xgl))*(xb1-xb2)*xgl+4*(xb1-xg1)*(xb2-xgl))*(xb2-xg1)-(log(xb2)
     . -log(xg1))*(xb1-xb2)*(xg1-xgl)*xb2)*(log(xb1)-log(xg1))*xb1-((
     . (xb1-xg1)*(xb2-xgl)*t134p(m1,mb1,m1)-(xb1-xgl)*(xb2-xg1)*t134p
     . (m1,mb2,m1)-(xb1-xb2)*(xg1-xgl)*t134p(m1,mg,m1))*(xb2-2*xg1+
     . xb1)-((t134p(mb1,mb2,m1)-t134p(mb1,mg,m1))*(xb1-xgl)*(xb2-xg1)
     . +(t134p(mb2,mb1,m1)-t134p(mb2,mg,m1))*(xb1-xg1)*(xb2-xgl))*(
     . xb1-xb2))*xg1)*xg1)/(6*(xb1-xb2)*(xb1-xg1)*(xb1-xgl)*(xb2-xg1)
     . *(xb2-xgl))

      ans5=-((2*xgl+1-3*xb2)*xb1+(xgl+2)*xb2-3*xgl-(3*xb1-3*xb2+xgl-1
     . -3*(xb1-xb2)*st2)*(xb1-xb2)*st2)*(xb1-xg1)*(xb2-xg1)*(xgl-1)*
     . t134p(mu,mg,m1)-((2*xg1+xgl)*xb2-3*xg1*xgl+(xg1+2*xgl-3*xb2)*
     . xb1-(3*xb1-3*xb2-xg1+xgl-3*(xb1-xb2)*st2)*(xb1-xb2)*st2)*(xb1-
     . 1)*(xb2-1)*(xg1-xgl)*t134p(m1,mg,m1)
      ans4=(3*(xb1-xb2)*st2**2-(xb2-1)+(2*xb2+1-3*xb1)*st2)*(xb1-xg1)
     . *(xb1-xgl)*(xb2-xg1)*(xb2-1)*t134p(mu,mb2,m1)+((3*st2**2-2*st2
     . +1)*(xb1-xgl)*(xb2-xg1)*(xb2-1)*t134p(mb1,mb2,m1)-(3*st2**2-4*
     . st2+2)*(xb1-xg1)*(xb1-1)*(xb2-xgl)*t134p(mb2,mb1,m1))*(xb1-xb2
     . )*(xg1-1)+(3*(xb1-xb2)*st2**2-2*(xb2-xgl)+(4*xb2-xgl-3*xb1)*
     . st2)*(xb1-xg1)*(xb1-1)*(xb2-xgl)*(xg1-1)*t134p(mb2,mg,m1)-(3*(
     . xb1-xb2)*st2**2-(xb2-xg1)+(2*xb2+xg1-3*xb1)*st2)*(xb1-xgl)*(
     . xb1-1)*(xb2-xg1)*(xb2-1)*t134p(m1,mb2,m1)-(3*(xb1-xb2)*st2**2+
     . 2*(xb1-1)+(3*xb2+1-4*xb1)*st2)*(xb1-xg1)*(xb1-1)*(xb2-xg1)*(
     . xb2-xgl)*t134p(mu,mb1,m1)-(3*(xb1-xb2)*st2**2+xb1-xgl+(3*xb2-
     . xgl-2*xb1)*st2)*(xb1-xgl)*(xb2-xg1)*(xb2-1)*(xg1-1)*t134p(mb1,
     . mg,m1)+(3*(xb1-xb2)*st2**2+2*(xb1-xg1)+(3*xb2+xg1-4*xb1)*st2)*
     . (xb1-xg1)*(xb1-1)*(xb2-xgl)*(xb2-1)*t134p(m1,mb1,m1)+ans5
      ans3=2*ans4*xg1
      ans7=-2*((2*xgl+1-3*xb2)*xb1+(xgl+2)*xb2-3*xgl-(3*xb1-3*xb2+xgl
     . -1-3*(xb1-xb2)*st2)*(xb1-xb2)*st2)*(log(xg1)-log(xgl))*(xb1-
     . xg1)*(xb2-xg1)*log(xg1)*xgl-2*(((3*(xb1-xb2)*st2**2-(xb2-1)+(2
     . *xb2+1-3*xb1)*st2)*(xb2-xg1)*log(xg1)+2*(st2-2)*(xb1-1)*(xb2-
     . xgl)*(xg1-1))*(xb1-xgl)-(3*(xb1-xb2)*st2**2-2*(xb2-xgl)+(4*xb2
     . -xgl-3*xb1)*st2)*(log(xg1)-log(xgl))*(xb1-1)*(xg1-1)*xgl)*(log
     . (xb2)-log(xg1))*(xb1-xg1)*xb2
      ans6=2*(((((xgl+2)*xg1+xgl)*xb2-(xb2**2+3*xg1)*xgl+2*(xb2-xgl)*
     . xb1**2-((3*(xg1+1)-xb2)*xb2-((2*xgl+1)*xg1+2*xgl))*xb1)*(2*st2
     . -1)-3*(((xgl+1)*xg1+xgl)*xb2-(xb2**2+2*xg1)*xgl+(xb2-xgl)*xb1
     . **2-((2*(xg1+1)-xb2)*xb2-((xgl+1)*xg1+xgl))*xb1)*st2**2)*(log(
     . xb2)-log(xg1))*(xg1-1)*xb2+(((3*(xb1-xb2)*st2**2+2*(xb1-1)+(3*
     . xb2+1-4*xb1)*st2)*(xb1-xg1)*log(xg1)+2*(st2+1)*(xb1-xgl)*(xb2-
     . 1)*(xg1-1))*(xb2-xgl)-(3*(xb1-xb2)*st2**2+xb1-xgl+(3*xb2-xgl-2
     . *xb1)*st2)*(log(xg1)-log(xgl))*(xb2-1)*(xg1-1)*xgl)*(xb2-xg1))
     . *(log(xb1)-log(xg1))*xb1+(((6*st2**2-5*st2-2)*xb2-(st2-2)*xgl)
     . *(log(xb2)-log(xg1))**2*(xb1-xg1)*(xb1-xgl)*(xb1-1)*xb2+((6*
     . st2**2-7*st2-1)*xb1+(st2+1)*xgl)*(log(xb1)-log(xg1))**2*(xb2-
     . xg1)*(xb2-xgl)*(xb2-1)*xb1)*(xg1-1)-(xb2-3+2*xb1-(xb1-xb2)*st2
     . )*(log(xg1)+4)*(xb1-xg1)*(xb1-xgl)*(xb2-xg1)*(xb2-xgl)*log(xg1
     . )+ans7
      ans2=ans3+ans6
      ans1=ans2*xg1
      r532=ans1/(16*(xb1-xg1)*(xb1-xgl)*(xb1-1)*(xb2-xg1)*(xb2-xgl)*(
     . xb2-1)*(xg1-1))

      ans5=(xb2**2+3*xgl-(xgl+1)*xb2-2*(xgl+1-xb1)*xb1-(4*xb1-2*xb2-
     . xgl-1-3*(xb1-xb2)*st2)*(xb1-xb2)*st2)*(xb1-xg1)*(xb2-xg1)*(xgl
     . -1)*t134p(mu,mg,m1)+(xb2**2+3*xg1*xgl-(xg1+xgl)*xb2-2*(xg1+xgl
     . -xb1)*xb1-(4*xb1-2*xb2-xg1-xgl-3*(xb1-xb2)*st2)*(xb1-xb2)*st2)
     . *(xb1-1)*(xb2-1)*(xg1-xgl)*t134p(m1,mg,m1)
      ans4=(3*(xb1-xb2)*st2**2-(xb2-1)+(2*xb2+1-3*xb1)*st2)*(xb1-xg1)
     . *(xb1-1)*(xb2-xg1)*(xb2-xgl)*t134p(mu,mb1,m1)+3*((xb1-xg1)*(
     . xb1-1)*(xb2-xgl)*t134p(mb2,mb1,m1)-(xb1-xgl)*(xb2-xg1)*(xb2-1)
     . *t134p(mb1,mb2,m1))*(st2-1)*(xb1-xb2)*(xg1-1)*st2+(3*(xb1-xb2)
     . *st2**2-(xb2-xgl)+(2*xb2+xgl-3*xb1)*st2)*(xb1-xgl)*(xb2-xg1)*(
     . xb2-1)*(xg1-1)*t134p(mb1,mg,m1)-(3*(xb1-xb2)*st2**2-(xb2-xg1)+
     . (2*xb2+xg1-3*xb1)*st2)*(xb1-xg1)*(xb1-1)*(xb2-xgl)*(xb2-1)*
     . t134p(m1,mb1,m1)-(3*(xb1-xb2)*st2**2+2*(xb1-1)+(3*xb2+1-4*xb1)
     . *st2)*(xb1-xg1)*(xb1-xgl)*(xb2-xg1)*(xb2-1)*t134p(mu,mb2,m1)-(
     . 3*(xb1-xb2)*st2**2+2*(xb1-xgl)+(3*xb2+xgl-4*xb1)*st2)*(xb1-xg1
     . )*(xb1-1)*(xb2-xgl)*(xg1-1)*t134p(mb2,mg,m1)+(3*(xb1-xb2)*st2
     . **2+2*(xb1-xg1)+(3*xb2+xg1-4*xb1)*st2)*(xb1-xgl)*(xb1-1)*(xb2-
     . xg1)*(xb2-1)*t134p(m1,mb2,m1)+ans5
      ans3=2*ans4*xg1
      ans7=2*((((3*(xb1-xb2)*st2**2-(xb2-1)+(2*xb2+1-3*xb1)*st2)*(xb1
     . -xg1)*log(xg1)-2*(st2+1)*(xb1-xgl)*(xb2-1)*(xg1-1))*(xb2-xgl)-
     . (3*(xb1-xb2)*st2**2-(xb2-xgl)+(2*xb2+xgl-3*xb1)*st2)*(log(xg1)
     . -log(xgl))*(xb2-1)*(xg1-1)*xgl)*(xb2-xg1)-3*(((xgl+1)*xg1+xgl)
     . *xb2-(xb2**2+2*xg1)*xgl+(xb2-xgl)*xb1**2-((2*(xg1+1)-xb2)*xb2-
     . ((xgl+1)*xg1+xgl))*xb1)*(log(xb2)-log(xg1))*(st2-1)*(xg1-1)*
     . st2*xb2)*(log(xb1)-log(xg1))*xb1
      ans6=((3*(2*st2**2-st2+1)*xb1-(st2+1)*xgl)*(log(xb1)-log(xg1))
     . **2*(xb2-xg1)*(xb2-xgl)*(xb2-1)*xb1+(3*(2*st2**2-3*st2+2)*xb2+
     . (st2-2)*xgl)*(log(xb2)-log(xg1))**2*(xb1-xg1)*(xb1-xgl)*(xb1-1
     . )*xb2)*(xg1-1)+(xb2-3+2*xb1-(xb1-xb2)*st2)*(log(xg1)+4)*(xb1-
     . xg1)*(xb1-xgl)*(xb2-xg1)*(xb2-xgl)*log(xg1)-2*(xb2**2+3*xgl-(
     . xgl+1)*xb2-2*(xgl+1-xb1)*xb1-(4*xb1-2*xb2-xgl-1-3*(xb1-xb2)*
     . st2)*(xb1-xb2)*st2)*(log(xg1)-log(xgl))*(xb1-xg1)*(xb2-xg1)*
     . log(xg1)*xgl-2*(((3*(xb1-xb2)*st2**2+2*(xb1-1)+(3*xb2+1-4*xb1)
     . *st2)*(xb2-xg1)*log(xg1)-2*(st2-2)*(xb1-1)*(xb2-xgl)*(xg1-1))*
     . (xb1-xgl)-(3*(xb1-xb2)*st2**2+2*(xb1-xgl)+(3*xb2+xgl-4*xb1)*
     . st2)*(log(xg1)-log(xgl))*(xb1-1)*(xg1-1)*xgl)*(log(xb2)-log(
     . xg1))*(xb1-xg1)*xb2+ans7
      ans2=ans3+ans6
      ans1=ans2*xg1
      r542=ans1/(16*(xb1-xg1)*(xb1-xgl)*(xb1-1)*(xb2-xg1)*(xb2-xgl)*(
     . xb2-1)*(xg1-1))

      ans4=(((((xb2-xg1)*t134p(mu,mb1,m1)-(xb2-1)*t134p(m1,mb1,m1)+(
     . t134p(mb2,mb1,m1)-t134p(mb2,mg,m1))*(xg1-1))*(xb1-1)*(xb2-xgl)
     . -(xb1-xgl)*(xb2-xg1)*(xb2-1)*t134p(mu,mb2,m1))*(xb1-xg1)-(((
     . t134p(mb1,mb2,m1)-t134p(mb1,mg,m1))*(xg1-1)-(xb1-1)*t134p(m1,
     . mb2,m1))*(xb1-xgl)*(xb2-xg1)*(xb2-1)-((xb1-xg1)*(xb2-xg1)*(xgl
     . -1)*t134p(mu,mg,m1)+(xb1-1)*(xb2-1)*(xg1-xgl)*t134p(m1,mg,m1))
     . *(xb1-xb2)))*xg1+(log(xg1)-log(xgl))*(xb1-xb2)*(xb1-xg1)*(xb2-
     . xg1)*log(xg1)*xgl)*(xb1-xb2)
      ans3=((((xgl+1)*xg1+xgl)*xb2-(xb2**2+2*xg1)*xgl+(xb2-xgl)*xb1**
     . 2-((2*(xg1+1)-xb2)*xb2-((xgl+1)*xg1+xgl))*xb1)*(log(xb2)-log(
     . xg1))*(xg1-1)*xb2+((log(xg1)-log(xgl))*(xb2-1)*(xg1-1)*xgl-(
     . xb1-xg1)*(xb2-xgl)*log(xg1))*(xb1-xb2)*(xb2-xg1))*(log(xb1)-
     . log(xg1))*xb1-(((log(xb1)-log(xg1))**2*(xb2-xg1)*(xb2-xgl)*(
     . xb2-1)*xb1**2+(log(xb2)-log(xg1))**2*(xb1-xg1)*(xb1-xgl)*(xb1-
     . 1)*xb2**2)*(xg1-1)+((log(xg1)-log(xgl))*(xb1-1)*(xg1-1)*xgl-(
     . xb1-xgl)*(xb2-xg1)*log(xg1))*(log(xb2)-log(xg1))*(xb1-xb2)*(
     . xb1-xg1)*xb2)+ans4
      ans5=(st2-1)*st2*xg1
      ans2=3*ans3*ans5
      ans1=-ans2
      r53p2=ans1/(8*(xb1-xg1)*(xb1-xgl)*(xb1-1)*(xb2-xg1)*(xb2-xgl)*(
     . xb2-1)*(xg1-1))

      ans3=-(((((xb2-xg1)*t134p(mu,mb1,m1)-(xb2-1)*t134p(m1,mb1,m1)+(
     . t134p(mb2,mb1,m1)-t134p(mb2,mg,m1))*(xg1-1))*(xb1-1)*(xb2-xgl)
     . -(xb1-xgl)*(xb2-xg1)*(xb2-1)*t134p(mu,mb2,m1))*(xb1-xg1)-(((
     . t134p(mb1,mb2,m1)-t134p(mb1,mg,m1))*(xg1-1)-(xb1-1)*t134p(m1,
     . mb2,m1))*(xb1-xgl)*(xb2-xg1)*(xb2-1)-((xb1-xg1)*(xb2-xg1)*(xgl
     . -1)*t134p(mu,mg,m1)+(xb1-1)*(xb2-1)*(xg1-xgl)*t134p(m1,mg,m1))
     . *(xb1-xb2)))*xg1-(log(xg1)-log(xgl))*(xb1-xb2)*(xb1-xg1)*(xb2-
     . xg1)*log(xg1)*xgl)*(xb1-xb2)
      ans2=((((xgl+1)*xg1+xgl)*xb2-(xb2**2+2*xg1)*xgl+(xb2-xgl)*xb1**
     . 2-((2*(xg1+1)-xb2)*xb2-((xgl+1)*xg1+xgl))*xb1)*(log(xb2)-log(
     . xg1))*(xg1-1)*xb2+((log(xg1)-log(xgl))*(xb2-1)*(xg1-1)*xgl-(
     . xb1-xg1)*(xb2-xgl)*log(xg1))*(xb1-xb2)*(xb2-xg1))*(log(xb1)-
     . log(xg1))*xb1-(((log(xb1)-log(xg1))**2*(xb2-xg1)*(xb2-xgl)*(
     . xb2-1)*xb1**2+(log(xb2)-log(xg1))**2*(xb1-xg1)*(xb1-xgl)*(xb1-
     . 1)*xb2**2)*(xg1-1)+((log(xg1)-log(xgl))*(xb1-1)*(xg1-1)*xgl-(
     . xb1-xgl)*(xb2-xg1)*log(xg1))*(log(xb2)-log(xg1))*(xb1-xb2)*(
     . xb1-xg1)*xb2)+ans3
      ans4=(st2-1)*st2*xg1
      ans1=3*ans2*ans4
      r54p2=ans1/(8*(xb1-xg1)*(xb1-xgl)*(xb1-1)*(xb2-xg1)*(xb2-xgl)*(
     . xb2-1)*(xg1-1))

      r532 = r532 + r53p2
      r542 = r542 + r54p2

      ratio = amg/am1
      r52=ratio*r512+r522+r532+ratio*r542

c--r7
      ans6=-2*(2*(13*st2**2-13*st2-1)*xb1**2*xb2**2+5*(st2-1)*(xb1**4
     . +xb2**4)*st2+(24*st2**2-24*st2+1)*(xb1**2+xb2**2)*xb1*xb2)*xg1
      ans5=(2*(st2-1)*(xb1-xb2)*st2-(xb2-xg1))*(xb1-xb2)**2*(xb1+xg1)
     . *t134p(m1,mb1,m1)*xg1+2*(st2-1)*(5*xb1**2+4*xb1*xb2+5*xb2**2)*
     . (xb1+xb2)*st2*xb1*xb2-(2*(st2-1)*(xb1-xb2)*st2+xb1-xg1)*(xb1-
     . xb2)**2*(xb2+xg1)*t134p(m1,mb2,m1)*xg1-2*((10*st2**2-10*st2+1)
     . *(xb1**2+xb2**2)+2*(4*st2**2-4*st2-1)*xb1*xb2)*xg1**3+2*((27*
     . st2**2-27*st2-1)*xb1*xb2+(15*st2**2-15*st2+1)*(xb1**2-xb1*xb2+
     . xb2**2))*(xb1+xb2)*xg1**2-(2*((5*xb2-3*xg1)*xb2-(xb2+xg1)*xb1)
     . *(st2-1)*st2+(3*xb2-xg1)*xb2-(xb2+xg1)*xb1)*(xb1-xg1)**2*t134p
     . (mb2,mb2,m1)*xg1-(2*((xb1+xb2)*(xb1-xb2)-2*(xb2-xg1)*xb1)*(st2
     . -1)*st2-(xb1+xb2)*(xb2-xg1))*(xb1-xg1)**2*t134p(mb2,mb1,m1)*
     . xg1+(2*((xb1+2*xb2)*xb1-(xb2+2*xg1)*xb2)*(st2-1)*st2+(xb1+xb2)
     . *(xb1-xg1))*(xb2-xg1)**2*t134p(mb1,mb2,m1)*xg1-(2*(5*xb1**2-
     . xb2*xg1-(xb2+3*xg1)*xb1)*(st2-1)*st2+3*xb1**2-xb2*xg1-(xb2+xg1
     . )*xb1)*(xb2-xg1)**2*t134p(mb1,mb1,m1)*xg1+ans6
      ans4=4*ans5
      ans8=2*(2*(((xb2-xg1)*xb2**2*xg1-7*xb1**4-(19*xb2-28*xg1)*xb1**
     . 3-(3*xb2**2-2*xb2*xg1+4*xg1**2)*xb1*xb2+(5*xb2**2+17*xb2*xg1-
     . 19*xg1**2)*xb1**2)*(st2-1)*st2-(4*xb1-3*xg1)*(xb1-xb2)*(xb2-
     . xg1)*xb1)*(xb2-xg1)-(2*((2*st2**2-2*st2-1)*xb1*xb2+(st2-1)*(
     . xb1**2+xb2**2)*st2)*xg1**3-(4*(st2-1)*(xb1**2-xb1*xb2+xb2**2)*
     . st2-xb1*xb2)*(xb1+xb2)*xb1*xb2-((8*st2**2-8*st2-3)*xb1*xb2+4*(
     . st2-1)*(xb1**2-xb1*xb2+xb2**2)*st2)*(xb1+xb2)*xg1**2+(2*((st2-
     . 1)*(xb1**4+xb2**4)*st2-2*xb1**2*xb2**2)+(10*st2**2-10*st2-1)*(
     . xb1**2+xb2**2)*xb1*xb2)*xg1)*(log(xb2)-log(xg1)))*(log(xb1)-
     . log(xg1))
      ans7=-(2*((xb2-xg1)*xb2**2*xg1-2*xb1**4-2*(8*xb2-9*xg1)*xb1**3-
     . 2*(xb2**2+xb2*xg1-xg1**2)*xb1*xb2+(8*xb2**2+7*xb2*xg1-13*xg1**
     . 2)*xb1**2)*(st2-1)*st2-(11*xb1**2+6*xb2*xg1-(9*xb2+8*xg1)*xb1)
     . *(xb2-xg1)*xb1)*(log(xb1)-log(xg1))**2*(xb2-xg1)+(4*(((5*xb2**
     . 2+2*xb2*xg1-xg1**2-(3*xb2-xg1)*xb1)*xb1**2-(7*xb2**2-28*xb2*
     . xg1+19*xg1**2)*xb2**2-(19*xb2**2-17*xb2*xg1+4*xg1**2)*xb1*xb2)
     . *(st2-1)*st2+(xb1-xb2)*(xb1-xg1)*(4*xb2-3*xg1)*xb2)-(2*((4*xb2
     . +xg1-xb1)*(2*xb2-xg1)*xb1**2-(2*xb2**2-18*xb2*xg1+13*xg1**2)*
     . xb2**2-(16*xb2**2-7*xb2*xg1-2*xg1**2)*xb1*xb2)*(st2-1)*st2+(9*
     . xb1*xb2-6*xb1*xg1-11*xb2**2+8*xb2*xg1)*(xb1-xg1)*xb2)*(log(xb2
     . )-log(xg1)))*(log(xb2)-log(xg1))*(xb1-xg1)+ans8
      ans3=ans4+ans7
      ans2=ans3*xg1
      ans1=-ans2
      r712=ans1/(24*(xb1-xb2)**2*(xb1-xg1)**2*(xb2-xg1)**2)

      ans4=2*((((xb2-xg1)*xb2**2*xg1-7*xb1**4-(19*xb2-28*xg1)*xb1**3-
     . (3*xb2**2-2*xb2*xg1+4*xg1**2)*xb1*xb2+(5*xb2**2+17*xb2*xg1-19*
     . xg1**2)*xb1**2)*(st2-1)*st2-2*(xb1-xb2)*(xb1-xg1)*(xb2-xg1)*
     . xb1)*(xb2-xg1)-(((st2-1)*(xb1**4+xb2**4)*st2-4*xb1**2*xb2**2+(
     . 5*st2**2-5*st2-1)*(xb1**2+xb2**2)*xb1*xb2+(2*(st2**2-st2-1)*
     . xb1*xb2+(st2-1)*(xb1**2+xb2**2)*st2)*xg1**2)*xg1-(((2*st2+1)*(
     . 2*st2-3)*xb1*xb2+2*(st2-1)*(xb1**2-xb1*xb2+xb2**2)*st2)*xg1**2
     . +(2*(st2-1)*(xb1**2-xb1*xb2+xb2**2)*st2-xb1*xb2)*xb1*xb2)*(xb1
     . +xb2))*(log(xb2)-log(xg1)))*(log(xb1)-log(xg1))
      ans3=(2*(((5*xb2**2+2*xb2*xg1-xg1**2-(3*xb2-xg1)*xb1)*xb1**2-(7
     . *xb2**2-28*xb2*xg1+19*xg1**2)*xb2**2-(19*xb2**2-17*xb2*xg1+4*
     . xg1**2)*xb1*xb2)*(st2-1)*st2+2*(xb1-xb2)*(xb1-xg1)*(xb2-xg1)*
     . xb2)-(((4*xb2+xg1-xb1)*(2*xb2-xg1)*xb1**2-(2*xb2**2-18*xb2*xg1
     . +13*xg1**2)*xb2**2-(16*xb2**2-7*xb2*xg1-2*xg1**2)*xb1*xb2)*(
     . st2-1)*st2+(xb1-3*xb2)*(xb1-xg1)*(xb2-xg1)*xb2)*(log(xb2)-log(
     . xg1)))*(log(xb2)-log(xg1))*(xb1-xg1)+ans4
      ans2=4*(((xb1-xb2)*st2-(xb1-xg1))*((xb1-xb2)*st2+xb2-xg1)*((xb1
     . +xg1)*t134p(m1,mb1,m1)-(xb2+xg1)*t134p(m1,mb2,m1))*(xb1-xb2)*
     . xg1+(xb2-2*xg1+xb1)*(st2-1)*(5*xb1**2+4*xb1*xb2+5*xb2**2)*(xb1
     . -xg1)*(xb2-xg1)*st2-(((5*xb2-3*xg1)*xb2-(xb2+xg1)*xb1)*(st2-1)
     . *st2+2*(xb2-xg1)*xb2)*(xb1-xg1)**2*t134p(mb2,mb2,m1)*xg1-(((
     . xb1+xb2)*(xb1-xb2)-2*(xb2-xg1)*xb1)*(st2-1)*st2-(xb1+xb2)*(xb2
     . -xg1))*(xb1-xg1)**2*t134p(mb2,mb1,m1)*xg1+(((xb1+2*xb2)*xb1-(
     . xb2+2*xg1)*xb2)*(st2-1)*st2+(xb1+xb2)*(xb1-xg1))*(xb2-xg1)**2*
     . t134p(mb1,mb2,m1)*xg1-((5*xb1**2-xb2*xg1-(xb2+3*xg1)*xb1)*(st2
     . -1)*st2+2*(xb1-xg1)*xb1)*(xb2-xg1)**2*t134p(mb1,mb1,m1)*xg1)-(
     . ((xb2-xg1)*xb2**2*xg1-2*xb1**4-2*(8*xb2-9*xg1)*xb1**3-2*(xb2**
     . 2+xb2*xg1-xg1**2)*xb1*xb2+(8*xb2**2+7*xb2*xg1-13*xg1**2)*xb1**
     . 2)*(st2-1)*st2-(3*xb1-xb2)*(xb1-xg1)*(xb2-xg1)*xb1)*(log(xb1)-
     . log(xg1))**2*(xb2-xg1)+ans3
      ans1=ans2*xg1
      r722=ans1/(24*(xb1-xb2)**2*(xb1-xg1)**2*(xb2-xg1)**2)

      ans4=-4*(((xb1+xg1)*t134p(m1,mb1,m1)-(xb2+xg1)*t134p(m1,mb2,m1)
     . )*(xb1-xb2)**3-((5*xb2-3*xg1)*xb2-(xb2+xg1)*xb1)*(xb1-xg1)**2*
     . t134p(mb2,mb2,m1)-((xb1+xb2)*(xb1-xb2)-2*(xb2-xg1)*xb1)*(xb1-
     . xg1)**2*t134p(mb2,mb1,m1)+((xb1+2*xb2)*xb1-(xb2+2*xg1)*xb2)*(
     . xb2-xg1)**2*t134p(mb1,mb2,m1)-(5*xb1**2-xb2*xg1-(xb2+3*xg1)*
     . xb1)*(xb2-xg1)**2*t134p(mb1,mb1,m1))*xg1
      ans3=(((xb2-xg1)*xb2**2*xg1-2*xb1**4-2*(8*xb2-9*xg1)*xb1**3-2*(
     . xb2**2+xb2*xg1-xg1**2)*xb1*xb2+(8*xb2**2+7*xb2*xg1-13*xg1**2)*
     . xb1**2)*(log(xb1)-log(xg1))**2-4*(xb2-2*xg1+xb1)*(5*xb1**2+4*
     . xb1*xb2+5*xb2**2)*(xb1-xg1))*(xb2-xg1)-(2*((5*xb2**2+2*xb2*xg1
     . -xg1**2-(3*xb2-xg1)*xb1)*xb1**2-(7*xb2**2-28*xb2*xg1+19*xg1**2
     . )*xb2**2-(19*xb2**2-17*xb2*xg1+4*xg1**2)*xb1*xb2)-((4*xb2+xg1-
     . xb1)*(2*xb2-xg1)*xb1**2-(2*xb2**2-18*xb2*xg1+13*xg1**2)*xb2**2
     . -(16*xb2**2-7*xb2*xg1-2*xg1**2)*xb1*xb2)*(log(xb2)-log(xg1)))*
     . (log(xb2)-log(xg1))*(xb1-xg1)-2*(((xb2-xg1)*xb2**2*xg1-7*xb1**
     . 4-(19*xb2-28*xg1)*xb1**3-(3*xb2**2-2*xb2*xg1+4*xg1**2)*xb1*xb2
     . +(5*xb2**2+17*xb2*xg1-19*xg1**2)*xb1**2)*(xb2-xg1)+((xb1-xg1)
     . **2*xb1+(xb2-xg1)**2*xb2)*((2*xb2-xg1)*xb1-xb2*xg1)*(log(xb2)-
     . log(xg1)))*(log(xb1)-log(xg1))+ans4
      ans5=(st2-1)*st2*xg1
      ans2=ans3*ans5
      ans1=-ans2
      r72p2=ans1/(24*(xb1-xb2)**2*(xb1-xg1)**2*(xb2-xg1)**2)

      r722 = r722 + r72p2

      ans8=-((((7*(3*xb2**2+xg1)*(xg1+1)*xb2-2*(xb2**2+xg1)*(xb2**2-
     . xg1)-8*(2*xg1**2+3*xg1+2)*xb2**2)*xb2-(xb1-4*xb2-xg1-1)*(3*xb2
     . **2-2*xb2*xg1-2*xb2+xg1)*xb1**2)*xb1-(2*xb2**4+13*xg1**2-2*(2*
     . xb2**2+9*xg1)*(xg1+1)*xb2+(2*xg1**2+25*xg1+2)*xb2**2)*xb2**2-(
     . 17*xb2**4+xg1**2-2*(xb2**2-xg1)*(xg1+1)*xb2-2*(4*xg1**2+xg1+4)
     . *xb2**2)*xb1**2)*st2**3+(3*(3*xb1**2*xb2**2-2*xb1**2*xb2*xg1-2
     . *xb1**2*xb2+xb1**2*xg1-21*xb1*xb2**3+14*xb1*xb2**2*xg1+14*xb1*
     . xb2**2-7*xb1*xb2*xg1+28*xb2**4-22*xb2**3*xg1-22*xb2**3+16*xb2
     . **2*xg1)*st2**2-2*(xb1-xb2)*(11*xb2**2-8*xb2*xg1-8*xb2+5*xg1)*
     . xb2)*(xb1-xg1)*(xb1-1))
      ans7=2*(((18*xb2**2-xg1)*(xg1+1)-31*xb2**3+(2*xg1**2-7*xg1+2)*
     . xb2+(3*xb2**2+xg1-2*(xg1+1)*xb2)*xb1)*xb1**3-(xb2**4-20*xg1**2
     . -2*(xb2**2-14*xg1)*(xg1+1)*xb2+(xg1**2-35*xg1+1)*xb2**2)*xb2**
     . 2-(xb2**4+12*xg1**2+(37*xb2**2-2*xg1)*(xg1+1)*xb2-(29*xg1**2+
     . 25*xg1+29)*xb2**2)*xb1*xb2+(39*xb2**4+xg1**2+(xb2**2+9*xg1)*(
     . xg1+1)*xb2-3*(7*xg1**2+6*xg1+7)*xb2**2)*xb1**2)*st2+ans8
      ans9=(log(xb2)-log(xg1))**2*(xb1-xg1)*(xb1-1)*(xg1-1)
      ans6=ans7*ans9
      ans12=((xb2-xg1)*(xb2-1)*xb2**2*xg1+2*xb1**6-2*(2*(xg1+1)-xb2)*
     . xb1**5-((21*(xg1+1)-17*xb2)*xb2-(2*xg1**2+25*xg1+2))*xb1**4-2*
     . ((xb2**2-xg1)*(xg1+1)*xb2+xg1**2-(xg1**2+1)*xb2**2)*xb1*xb2-2*
     . ((xb2**2+9*xg1)*(xg1+1)+6*xb2**3-4*(2*xg1**2+3*xg1+2)*xb2)*xb1
     . **3+(3*xb2**4+13*xg1**2+(5*xb2**2-7*xg1)*(xg1+1)*xb2-2*(4*xg1
     . **2+xg1+4)*xb2**2)*xb1**2)*st2**3
      ans11=(3*(2*(2*(xg1+1)-xb2-xb1)*xb1**4-(3*xb2**2+5*xg1-3*(xg1+1
     . )*xb2)*xb2*xg1-((7*(xg1+1)-11*xb2)*xb2+2*xg1**2-3*xg1+2)*xb1**
     . 3+((xb2**2-4*xg1)*(xg1+1)-9*xb2**3+(6*xg1**2-xg1+6)*xb2)*xb1**
     . 2+((6*xb2**2+5*xg1)*(xg1+1)*xb2+3*xg1**2-(6*xg1**2+7*xg1+6)*
     . xb2**2)*xb1)*st2**2+(11*xb1**2-8*xb1*xg1-8*xb1+5*xg1)*(xb1-xb2
     . )*(xb2-xg1)*(xb2-1))*xb1-((xb2-xg1)*(xb2-1)*xb2**2*xg1-4*xb1**
     . 6+4*(2*(xg1+1)-xb2)*xb1**5+2*((xg1-1)**2*xb2**2-6*xg1**2-(xb2
     . **2-3*xg1)*(xg1+1)*xb2)*xb1*xb2-((31*(xg1+1)-39*xb2)*xb2+4*xg1
     . **2-23*xg1+4)*xb1**4-2*((xb2**2+11*xg1)*(xg1+1)+14*xb2**3-(13*
     . xg1**2+8*xg1+13)*xb2)*xb1**3+(3*xb2**4+17*xg1**2+5*(3*xb2**2+
     . xg1)*(xg1+1)*xb2-6*(3*xg1**2+2*xg1+3)*xb2**2)*xb1**2)*st2+
     . ans12
      ans13=(log(xb1)-log(xg1))**2*(xb2-xg1)*(xb2-1)*(xg1-1)
      ans10=ans11*ans13
      ans18=-((2*((6*xb2**2-xg1)*(xg1+1)-19*xb2**3+3*(xg1**2+xg1+1)*
     . xb2+(5*xb2**2+xg1-3*(xg1+1)*xb2)*xb1)*xb1**2-(5*xb2**4+11*xg1
     . **2+2*(27*xb2**2+4*xg1)*(xg1+1)*xb2-(47*xg1**2+46*xg1+47)*xb2
     . **2)*xb2)*xb1-(7*xb2**4-33*xg1**2-2*(7*xb2**2-19*xg1)*(xg1+1)*
     . xb2+(7*xg1**2-36*xg1+7)*xb2**2)*xb2**2+2*(32*xb2**4+xg1**2-7*(
     . xg1+1)*xb2**3-(11*xg1**2-3*xg1+11)*xb2**2)*xb1**2)*st2
      ans17=((((xg1+1)*xg1+9*xb2**3-(3*xg1**2+5*xg1+3)*xb2-(5*xb2**2+
     . xg1-3*(xg1+1)*xb2)*xb1)*xb1**2-(5*xb2**4+4*xg1**2-(26*xb2**2+
     . 17*xg1)*(xg1+1)*xb2+(19*xg1**2+39*xg1+19)*xb2**2)*xb2)*xb1-(7*
     . xb2**4+19*xg1**2-14*(xb2**2+2*xg1)*(xg1+1)*xb2+(7*xg1**2+44*
     . xg1+7)*xb2**2)*xb2**2-(16*xb2**4+xg1**2-(5*xb2**2+2*xg1)*(xg1+
     . 1)*xb2-(5*xg1**2-7*xg1+5)*xb2**2)*xb1**2)*st2**3+(3*(5*xb1**2*
     . xb2**2-3*xb1**2*xb2*xg1-3*xb1**2*xb2+xb1**2*xg1-13*xb1*xb2**3+
     . 7*xb1*xb2**2*xg1+7*xb1*xb2**2-xb1*xb2*xg1+24*xb2**4-20*xb2**3*
     . xg1-20*xb2**3+16*xb2**2*xg1)*st2**2-4*(xb1-xb2)*(4*xb2**2-3*
     . xb2*xg1-3*xb2+2*xg1)*xb2)*(xb1-xg1)*(xb1-1)+ans18
      ans19=(xb1-1)*(xg1-1)
      ans16=ans17*ans19
      ans20=-((2*(2*(xb2+2)-3*xb1)*xb1+xb2**2-6*xb2-1)*st2-((xb1-xb2)
     . **2*st2**3-6*(xb1-xb2)*(xb1-1)*st2**2-2*(xb1-1)**2))*(xb1-xb2)
     . *(xb1-xg1)*(xb2-xg1)**2*log(xg1)*xb2
      ans15=ans16+ans20
      ans21=(log(xb2)-log(xg1))*(xb1-xg1)
      ans14=2*ans15*ans21
      ans25=((((5*(xg1+1)-4*xb2-4*xb1)*xb1**2+((xg1+1)*xb2-4*xg1)*xb2
     . -2*(xb2**2+3*xg1-2*(xg1+1)*xb2)*xb1-(((xg1+1-2*xb2-2*xb1)*xb1+
     . 2*(xg1+1+xb2)*xb2)*xb1-((xg1+1)*xb2+2*xg1)*xb2)*st2)*(xb2-xg1)
     . **2*(xb2-1)**2*t134p(mb1,mb2,m1)-(2*(((xg1+1-2*xb2)*xb1-(xb2-
     . xg1)*(xb2-1))*xb1-(xb2**2+3*xg1-2*(xg1+1)*xb2)*xb2)-((xg1+1-2*
     . xb2)*(xb1+xb2)*(xb1-xb2)+2*(xb2-xg1)*(xb2-1)*xb1)*st2)*(xb1-
     . xg1)**2*(xb1-1)**2*t134p(mb2,mb1,m1))*(st2-1)*st2+(2*(3*((5*
     . xb2**2+xg1-3*(xg1+1)*xb2)*xb2-(3*xb2**2-xg1-(xg1+1)*xb2)*xb1)*
     . st2**2-(3*xb2**2-xg1-(xg1+1)*xb2)*(xb1-xb2))-((7*xb2**2+3*xg1-
     . 5*(xg1+1)*xb2)*xb2-(3*xb2**2-xg1-(xg1+1)*xb2)*xb1)*st2**3-2*((
     . 13*xb2**2+xg1-7*(xg1+1)*xb2)*xb2-3*(3*xb2**2-xg1-(xg1+1)*xb2)*
     . xb1)*st2)*(xb1-xg1)**2*(xb1-1)**2*t134p(mb2,mb2,m1))*(xg1-1)
      ans24=(3*(5*xb1**3-3*xb1**2-7*xb2**2+(9*xb2-4)*xb1*xb2)*st2**2-
     . ((5*xb1**2+4*xb1*xb2+5*xb2**2)*(xb1+xb2-2)*st2**3+2*(3*xb1*xb2
     . -xb1-2*xb2)*(xb1-xb2))-(2*(5*xb1**2+9*xb2**2)*xb1-(5*xb2+13)*
     . xb2**2-(9*xb2+1)*xb1**2)*st2)*(xb1-1)*(xb2-1)*xg1**3+(((5*(xg1
     . +1)+3*xb2)*xb1**2-(7*xb1**3+xb2*xg1)-((xg1+1)*xb2+3*xg1)*xb1)*
     . st2**3-(3*st2**2+1)*(3*xb1**2-xb1*xg1-xb1-xg1)*(xb1-xb2)-((7*(
     . xg1+1)+9*xb2)*xb1**2-(13*xb1**3+3*xb2*xg1)-(3*(xg1+1)*xb2+xg1)
     . *xb1)*st2)*(xb2-xg1)**2*(xb2-1)**2*(xg1-1)*t134p(mb1,mb1,m1)+
     . ans25
      ans23=(((2*(2*(xb2+2*xg1)-3*xb1)*xb1+xb2**2-6*xb2*xg1-xg1**2)*
     . st2-((xb1-xb2)**2*st2**3-6*(xb1-xb2)*(xb1-xg1)*st2**2-2*(xb1-
     . xg1)**2))*(xb1-1)**2*(xb2+xg1)*(xb2-1)**2*t134p(m1,mb2,m1)-((2
     . *(2*(xb2+2)-3*xb1)*xb1+xb2**2-6*xb2-1)*st2-((xb1-xb2)**2*st2**
     . 3-6*(xb1-xb2)*(xb1-1)*st2**2-2*(xb1-1)**2))*(xb1-xg1)**2*(xb2-
     . xg1)**2*(xb2+1)*t134p(mu,mb2,m1)-((xb1-xb2)**2*st2**3+(xb2-1)
     . **2-3*(xb1+xb2-2)*(xb1-xb2)*st2**2+(2*(xb2-3+xb1)*xb1-(3*xb2**
     . 2-4*xb2-1))*st2)*(xb1-xg1)**2*(xb1+1)*(xb2-xg1)**2*t134p(mu,
     . mb1,m1)+((xb1-xb2)**2*st2**3+(xb2-xg1)**2-3*(xb1+xb2-2*xg1)*(
     . xb1-xb2)*st2**2+(2*(xb2-3*xg1+xb1)*xb1-(3*xb2**2-4*xb2*xg1-xg1
     . **2))*st2)*(xb1+xg1)*(xb1-1)**2*(xb2-1)**2*t134p(m1,mb1,m1))*(
     . xb1-xb2)+ans24
      ans22=4*ans23*xg1
      ans31=-(xb2-xg1)**2*(xb2-1)**2*xb2**2*xg1-(3*xb2**6-3*xb2**2*
     . xg1**2-2*xg1**3-2*(6*xb2**4-7*xg1**2)*(xg1+1)*xb2-2*(3*xg1**2+
     . 11*xg1+3)*(xg1+1)*xb2**3+3*(5*xg1**2+12*xg1+5)*xb2**4)*xb1**2+
     . (2*(xb2**4+5*xg1**2)*(xg1+1)*xb2+xg1**3+2*(xg1**2+11*xg1+1)*(
     . xg1+1)*xb2**3-(4*xg1**2+15*xg1+4)*xb2**4-(11*xg1**2+32*xg1+11)
     . *xb2**2*xg1)*xb1*xb2+(2*(5*xb2**4-2*xg1**2)*(xg1+1)-5*xb2**5-(
     . xg1**2+4*xg1+1)*xb2**3-2*(3*xg1**2+13*xg1+3)*(xg1+1)*xb2**2+(
     . 16*xg1**2+43*xg1+16)*xb2*xg1)*xb1**3
      ans30=((2*(3*xb2**2+xg1)*(xg1+1)+xb2**3-(4*xg1**2+9*xg1+4)*xb2)
     . *xb1**5-((3*xb2**2+xg1-2*(xg1+1)*xb2)*xb1**6+(xb2-xg1)**2*(xb2
     . -1)**2*xb2**2*xg1)-((3*xb2**2+xg1)*(xg1**2+4*xg1+1)+2*(xg1+1)*
     . xb2**3-2*(xg1**2+5*xg1+1)*(xg1+1)*xb2)*xb1**4-(3*xb2**6+6*xb2
     . **2*xg1**2+xg1**3-2*(3*xb2**4+2*xb2**2*xg1+2*xg1**2)*(xg1+1)*
     . xb2+3*(xg1**2+4*xg1+1)*xb2**4)*xb1**2-(2*(xb2**4-2*xb2**2*xg1-
     . xg1**2)*(xg1+1)-xb2**5-2*(xg1**2+4*xg1+1)*xb2**3+(5*xg1**2+11*
     . xg1+5)*xb2*xg1)*xb1**3+(2*((xb2**4+2*xg1**2)*(xg1+1)*xb2-xg1**
     . 3+(xg1**2+5*xg1+1)*(xg1+1)*xb2**3)-(4*xg1**2+9*xg1+4)*xb2**4-(
     . 5*xg1**2+11*xg1+5)*xb2**2*xg1)*xb1*xb2)*st2+2*((xg1**2+4*xg1+1
     . )*xg1-4*(xg1+1)*xb2**3-2*(xg1**2+8*xg1+1)*(xg1+1)*xb2+3*(3*xg1
     . **2+8*xg1+3)*xb2**2)*xb1**4+2*(3*xb2**2+xg1-2*(xg1+1)*xb2)*xb1
     . **6+2*(xb2**2-4*xb2*xg1-4*xb2+2*xg1)*(2*xb2-xg1-1)*xb1**5+
     . ans31
      ans32=(log(xb2)-log(xg1))*(st2-1)*(xg1-1)*st2
      ans29=ans30*ans32
      ans45=2*xb1**2*xb2**3*xg1+12*xb1**2*xb2**3+8*xb1**2*xb2**2*xg1
     . **3+2*xb1**2*xb2**2*xg1**2-4*xb1**2*xb2**2*xg1-6*xb1**2*xb2**2
     . +2*xb1**2*xb2*xg1**3-4*xb1**2*xb2*xg1**2+2*xb1**2*xb2*xg1-4*
     . xb1**2*xg1**3+4*xb1**2*xg1**2-4*xb1*xb2**4*xg1**2+4*xb1*xb2**4
     . *xg1+4*xb1*xb2**3*xg1**3+4*xb1*xb2**3*xg1**2-8*xb1*xb2**3*xg1-
     . 8*xb1*xb2**2*xg1**3+4*xb1*xb2**2*xg1**2+4*xb1*xb2**2*xg1+4*xb1
     . *xb2*xg1**3-4*xb1*xb2*xg1**2
      ans44=-7*st2*xb1*xb2**2*xg1**2+6*st2*xb1*xb2**2*xg1-7*st2*xb1*
     . xb2*xg1**3+7*st2*xb1*xb2*xg1**2-st2*xb2**5*xg1**2+st2*xb2**5*
     . xg1+st2*xb2**4*xg1**3+st2*xb2**4*xg1**2-2*st2*xb2**4*xg1-2*st2
     . *xb2**3*xg1**3+st2*xb2**3*xg1**2+st2*xb2**3*xg1+st2*xb2**2*xg1
     . **3-st2*xb2**2*xg1**2+8*xb1**4*xb2**3*xg1-8*xb1**4*xb2**3-8*
     . xb1**4*xb2**2*xg1**2-8*xb1**4*xb2**2*xg1+16*xb1**4*xb2**2+16*
     . xb1**4*xb2*xg1**2-8*xb1**4*xb2*xg1-8*xb1**4*xb2-8*xb1**4*xg1**
     . 2+8*xb1**4*xg1-8*xb1**3*xb2**4*xg1+8*xb1**3*xb2**4+2*xb1**3*
     . xb2**3*xg1**2+8*xb1**3*xb2**3*xg1-10*xb1**3*xb2**3+6*xb1**3*
     . xb2**2*xg1**3-4*xb1**3*xb2**2*xg1**2+2*xb1**3*xb2**2*xg1-4*xb1
     . **3*xb2**2-12*xb1**3*xb2*xg1**3+2*xb1**3*xb2*xg1**2+4*xb1**3*
     . xb2*xg1+6*xb1**3*xb2+6*xb1**3*xg1**3-6*xb1**3*xg1+6*xb1**2*xb2
     . **4*xg1**2-6*xb1**2*xb2**4-6*xb1**2*xb2**3*xg1**3-8*xb1**2*xb2
     . **3*xg1**2+ans45
      ans43=-16*st2*xb1**3*xb2**2*xg1**3+4*st2*xb1**3*xb2**2*xg1**2-
     . 17*st2*xb1**3*xb2**2*xg1+29*st2*xb1**3*xb2**2+14*st2*xb1**3*
     . xb2*xg1**3-17*st2*xb1**3*xb2*xg1**2+19*st2*xb1**3*xb2*xg1-16*
     . st2*xb1**3*xb2+2*st2*xb1**3*xg1**3-2*st2*xb1**3*xg1-5*st2*xb1
     . **2*xb2**5*xg1+5*st2*xb1**2*xb2**5+5*st2*xb1**2*xb2**4*xg1-5*
     . st2*xb1**2*xb2**4+5*st2*xb1**2*xb2**3*xg1**3-20*st2*xb1**2*xb2
     . **3*xg1**2+20*st2*xb1**2*xb2**3*xg1-5*st2*xb1**2*xb2**3-10*st2
     . *xb1**2*xb2**2*xg1**3+20*st2*xb1**2*xb2**2*xg1**2-15*st2*xb1**
     . 2*xb2**2*xg1+5*st2*xb1**2*xb2**2-st2*xb1**2*xb2*xg1**3+6*st2*
     . xb1**2*xb2*xg1**2-5*st2*xb1**2*xb2*xg1+6*st2*xb1**2*xg1**3-6*
     . st2*xb1**2*xg1**2+3*st2*xb1*xb2**5*xg1**2-3*st2*xb1*xb2**5-3*
     . st2*xb1*xb2**4*xg1**3-9*st2*xb1*xb2**4*xg1**2+6*st2*xb1*xb2**4
     . *xg1+6*st2*xb1*xb2**4+9*st2*xb1*xb2**3*xg1**3+6*st2*xb1*xb2**3
     . *xg1**2-12*st2*xb1*xb2**3*xg1-3*st2*xb1*xb2**3+st2*xb1*xb2**2*
     . xg1**3+ans44
      ans42=-6*st2**2*xb1**2*xb2**2-33*st2**2*xb1**2*xb2*xg1**3+9*st2
     . **2*xb1**2*xb2*xg1**2+24*st2**2*xb1**2*xb2*xg1+9*st2**2*xb1**2
     . *xg1**3-9*st2**2*xb1**2*xg1**2-15*st2**2*xb1*xb2**2*xg1**3+15*
     . st2**2*xb1*xb2**2*xg1**2+15*st2**2*xb1*xb2*xg1**3-15*st2**2*
     . xb1*xb2*xg1**2+14*st2*xb1**6*xb2*xg1-14*st2*xb1**6*xb2-14*st2*
     . xb1**6*xg1+14*st2*xb1**6+10*st2*xb1**5*xb2**2*xg1-10*st2*xb1**
     . 5*xb2**2-28*st2*xb1**5*xb2*xg1**2-10*st2*xb1**5*xb2*xg1+38*st2
     . *xb1**5*xb2+28*st2*xb1**5*xg1**2-28*st2*xb1**5-32*st2*xb1**4*
     . xb2**3*xg1+32*st2*xb1**4*xb2**3+12*st2*xb1**4*xb2**2*xg1**2+32
     . *st2*xb1**4*xb2**2*xg1-44*st2*xb1**4*xb2**2+14*st2*xb1**4*xb2*
     . xg1**3-2*st2*xb1**4*xb2*xg1**2-10*st2*xb1**4*xb2*xg1-2*st2*xb1
     . **4*xb2-14*st2*xb1**4*xg1**3-10*st2*xb1**4*xg1**2+10*st2*xb1**
     . 4*xg1+14*st2*xb1**4+13*st2*xb1**3*xb2**4*xg1-13*st2*xb1**3*xb2
     . **4+13*st2*xb1**3*xb2**3*xg1**2-13*st2*xb1**3*xb2**3*xg1+ans43
      ans41=-21*st2**2*xb1**4*xb2*xg1**3-45*st2**2*xb1**4*xb2*xg1**2+
     . 39*st2**2*xb1**4*xb2*xg1+27*st2**2*xb1**4*xb2+21*st2**2*xb1**4
     . *xg1**3+39*st2**2*xb1**4*xg1**2-39*st2**2*xb1**4*xg1-21*st2**2
     . *xb1**4-12*st2**2*xb1**3*xb2**4*xg1+12*st2**2*xb1**3*xb2**4-6*
     . st2**2*xb1**3*xb2**3*xg1**2+12*st2**2*xb1**3*xb2**3*xg1-6*st2
     . **2*xb1**3*xb2**3+3*st2**2*xb1**3*xb2**2*xg1**3-33*st2**2*xb1
     . **3*xb2**2*xg1**2+39*st2**2*xb1**3*xb2**2*xg1-9*st2**2*xb1**3*
     . xb2**2+21*st2**2*xb1**3*xb2*xg1**3+39*st2**2*xb1**3*xb2*xg1**2
     . -63*st2**2*xb1**3*xb2*xg1+3*st2**2*xb1**3*xb2-24*st2**2*xb1**3
     . *xg1**3+24*st2**2*xb1**3*xg1+6*st2**2*xb1**2*xb2**4*xg1**2-6*
     . st2**2*xb1**2*xb2**4-6*st2**2*xb1**2*xb2**3*xg1**3-6*st2**2*
     . xb1**2*xb2**3*xg1+12*st2**2*xb1**2*xb2**3+30*st2**2*xb1**2*xb2
     . **2*xg1**3-6*st2**2*xb1**2*xb2**2*xg1**2-18*st2**2*xb1**2*xb2
     . **2*xg1+ans42
      ans40=-2*st2**3*xb1*xb2**3*xg1**2+4*st2**3*xb1*xb2**3*xg1+3*st2
     . **3*xb1*xb2**3+6*st2**3*xb1*xb2**2*xg1**3-4*st2**3*xb1*xb2**2*
     . xg1**2-2*st2**3*xb1*xb2**2*xg1-4*st2**3*xb1*xb2*xg1**3+4*st2**
     . 3*xb1*xb2*xg1**2+st2**3*xb2**5*xg1**2-st2**3*xb2**5*xg1-st2**3
     . *xb2**4*xg1**3-st2**3*xb2**4*xg1**2+2*st2**3*xb2**4*xg1+2*st2
     . **3*xb2**3*xg1**3-st2**3*xb2**3*xg1**2-st2**3*xb2**3*xg1-st2**
     . 3*xb2**2*xg1**3+st2**3*xb2**2*xg1**2-21*st2**2*xb1**6*xb2*xg1+
     . 21*st2**2*xb1**6*xb2+21*st2**2*xb1**6*xg1-21*st2**2*xb1**6-15*
     . st2**2*xb1**5*xb2**2*xg1+15*st2**2*xb1**5*xb2**2+42*st2**2*xb1
     . **5*xb2*xg1**2+15*st2**2*xb1**5*xb2*xg1-57*st2**2*xb1**5*xb2-
     . 42*st2**2*xb1**5*xg1**2+42*st2**2*xb1**5+24*st2**2*xb1**4*xb2
     . **3*xg1-24*st2**2*xb1**4*xb2**3+6*st2**2*xb1**4*xb2**2*xg1**2-
     . 24*st2**2*xb1**4*xb2**2*xg1+18*st2**2*xb1**4*xb2**2+ans41
      ans39=-24*st2**3*xb1**3*xb2**2-47*st2**3*xb1**3*xb2*xg1**3-20*
     . st2**3*xb1**3*xb2*xg1**2+48*st2**3*xb1**3*xb2*xg1+19*st2**3*
     . xb1**3*xb2+28*st2**3*xb1**3*xg1**3-28*st2**3*xb1**3*xg1+5*st2
     . **3*xb1**2*xb2**5*xg1-5*st2**3*xb1**2*xb2**5-5*st2**3*xb1**2*
     . xb2**4*xg1+5*st2**3*xb1**2*xb2**4-5*st2**3*xb1**2*xb2**3*xg1**
     . 3+12*st2**3*xb1**2*xb2**3*xg1**2-12*st2**3*xb1**2*xb2**3*xg1+5
     . *st2**3*xb1**2*xb2**3-12*st2**3*xb1**2*xb2**2*xg1**3-12*st2**3
     . *xb1**2*xb2**2*xg1**2+29*st2**3*xb1**2*xb2**2*xg1-5*st2**3*xb1
     . **2*xb2**2+36*st2**3*xb1**2*xb2*xg1**3-19*st2**3*xb1**2*xb2*
     . xg1**2-17*st2**3*xb1**2*xb2*xg1-19*st2**3*xb1**2*xg1**3+19*st2
     . **3*xb1**2*xg1**2-3*st2**3*xb1*xb2**5*xg1**2+3*st2**3*xb1*xb2
     . **5+3*st2**3*xb1*xb2**4*xg1**3+5*st2**3*xb1*xb2**4*xg1**2-2*
     . st2**3*xb1*xb2**4*xg1-6*st2**3*xb1*xb2**4-5*st2**3*xb1*xb2**3*
     . xg1**3+ans40
      ans38=log(xg1)*xb1*xb2*xg1**3+7*st2**3*xb1**6*xb2*xg1-7*st2**3*
     . xb1**6*xb2-7*st2**3*xb1**6*xg1+7*st2**3*xb1**6+5*st2**3*xb1**5
     . *xb2**2*xg1-5*st2**3*xb1**5*xb2**2-14*st2**3*xb1**5*xb2*xg1**2
     . -5*st2**3*xb1**5*xb2*xg1+19*st2**3*xb1**5*xb2+14*st2**3*xb1**5
     . *xg1**2-14*st2**3*xb1**5+16*st2**3*xb1**4*xb2**3*xg1-16*st2**3
     . *xb1**4*xb2**3-26*st2**3*xb1**4*xb2**2*xg1**2-16*st2**3*xb1**4
     . *xb2**2*xg1+42*st2**3*xb1**4*xb2**2+7*st2**3*xb1**4*xb2*xg1**3
     . +63*st2**3*xb1**4*xb2*xg1**2-37*st2**3*xb1**4*xb2*xg1-33*st2**
     . 3*xb1**4*xb2-7*st2**3*xb1**4*xg1**3-37*st2**3*xb1**4*xg1**2+37
     . *st2**3*xb1**4*xg1+7*st2**3*xb1**4-9*st2**3*xb1**3*xb2**4*xg1+
     . 9*st2**3*xb1**3*xb2**4-5*st2**3*xb1**3*xb2**3*xg1**2+9*st2**3*
     . xb1**3*xb2**3*xg1-4*st2**3*xb1**3*xb2**3+19*st2**3*xb1**3*xb2
     . **2*xg1**3+25*st2**3*xb1**3*xb2**2*xg1**2-20*st2**3*xb1**3*xb2
     . **2*xg1+ans39
      ans37=-4*log(xg1)*st2*xb1*xb2**3*xg1**2+4*log(xg1)*st2*xb1*xb2
     . **2*xg1**3-log(xg1)*st2*xb1*xb2**2*xg1**2+log(xg1)*st2*xb1*xb2
     . *xg1**3+log(xg1)*xb1**4*xb2**3-log(xg1)*xb1**4*xb2**2*xg1-2*
     . log(xg1)*xb1**4*xb2**2+2*log(xg1)*xb1**4*xb2*xg1+log(xg1)*xb1
     . **4*xb2-log(xg1)*xb1**4*xg1-log(xg1)*xb1**3*xb2**4-log(xg1)*
     . xb1**3*xb2**3*xg1+2*log(xg1)*xb1**3*xb2**3+2*log(xg1)*xb1**3*
     . xb2**2*xg1**2+2*log(xg1)*xb1**3*xb2**2*xg1-log(xg1)*xb1**3*xb2
     . **2-4*log(xg1)*xb1**3*xb2*xg1**2-log(xg1)*xb1**3*xb2*xg1+2*log
     . (xg1)*xb1**3*xg1**2+2*log(xg1)*xb1**2*xb2**4*xg1-log(xg1)*xb1
     . **2*xb2**3*xg1**2-4*log(xg1)*xb1**2*xb2**3*xg1-log(xg1)*xb1**2
     . *xb2**2*xg1**3+2*log(xg1)*xb1**2*xb2**2*xg1**2+2*log(xg1)*xb1
     . **2*xb2**2*xg1+2*log(xg1)*xb1**2*xb2*xg1**3-log(xg1)*xb1**2*
     . xb2*xg1**2-log(xg1)*xb1**2*xg1**3-log(xg1)*xb1*xb2**4*xg1**2+
     . log(xg1)*xb1*xb2**3*xg1**3+2*log(xg1)*xb1*xb2**3*xg1**2-2*log(
     . xg1)*xb1*xb2**2*xg1**3-log(xg1)*xb1*xb2**2*xg1**2+ans38
      ans36=-5*log(xg1)*st2*xb1**4*xb2**3+5*log(xg1)*st2*xb1**4*xb2**
     . 2*xg1+10*log(xg1)*st2*xb1**4*xb2**2+2*log(xg1)*st2*xb1**4*xb2*
     . xg1**2+2*log(xg1)*st2*xb1**4*xb2*xg1+log(xg1)*st2*xb1**4*xb2-2
     . *log(xg1)*st2*xb1**4*xg1**3-12*log(xg1)*st2*xb1**4*xg1**2-log(
     . xg1)*st2*xb1**4*xg1+3*log(xg1)*st2*xb1**3*xb2**4+7*log(xg1)*
     . st2*xb1**3*xb2**3*xg1-4*log(xg1)*st2*xb1**3*xb2**3-10*log(xg1)
     . *st2*xb1**3*xb2**2*xg1**2-16*log(xg1)*st2*xb1**3*xb2**2*xg1-
     . log(xg1)*st2*xb1**3*xb2**2+14*log(xg1)*st2*xb1**3*xb2*xg1**2-
     . log(xg1)*st2*xb1**3*xb2*xg1+6*log(xg1)*st2*xb1**3*xg1**3+2*log
     . (xg1)*st2*xb1**3*xg1**2-6*log(xg1)*st2*xb1**2*xb2**4*xg1+log(
     . xg1)*st2*xb1**2*xb2**3*xg1**2+8*log(xg1)*st2*xb1**2*xb2**3*xg1
     . +5*log(xg1)*st2*xb1**2*xb2**2*xg1**3+2*log(xg1)*st2*xb1**2*xb2
     . **2*xg1**2+2*log(xg1)*st2*xb1**2*xb2**2*xg1-10*log(xg1)*st2*
     . xb1**2*xb2*xg1**3-log(xg1)*st2*xb1**2*xb2*xg1**2-log(xg1)*st2*
     . xb1**2*xg1**3+3*log(xg1)*st2*xb1*xb2**4*xg1**2-3*log(xg1)*st2*
     . xb1*xb2**3*xg1**3+ans37
      ans35=-12*log(xg1)*st2**2*xb1**4*xb2**2+3*log(xg1)*st2**2*xb1**
     . 4*xb2*xg1**2+3*log(xg1)*st2**2*xb1**4*xg1**3+12*log(xg1)*st2**
     . 2*xb1**4*xg1**2-3*log(xg1)*st2**2*xb1**3*xb2**4-3*log(xg1)*st2
     . **2*xb1**3*xb2**3*xg1+6*log(xg1)*st2**2*xb1**3*xb2**3+9*log(
     . xg1)*st2**2*xb1**3*xb2**2*xg1**2+18*log(xg1)*st2**2*xb1**3*xb2
     . **2*xg1-3*log(xg1)*st2**2*xb1**3*xb2*xg1**3-18*log(xg1)*st2**2
     . *xb1**3*xb2*xg1**2-6*log(xg1)*st2**2*xb1**3*xg1**3+6*log(xg1)*
     . st2**2*xb1**2*xb2**4*xg1-3*log(xg1)*st2**2*xb1**2*xb2**3*xg1**
     . 2-12*log(xg1)*st2**2*xb1**2*xb2**3*xg1-3*log(xg1)*st2**2*xb1**
     . 2*xb2**2*xg1**3+12*log(xg1)*st2**2*xb1**2*xb2*xg1**3-3*log(xg1
     . )*st2**2*xb1*xb2**4*xg1**2+3*log(xg1)*st2**2*xb1*xb2**3*xg1**3
     . +6*log(xg1)*st2**2*xb1*xb2**3*xg1**2-6*log(xg1)*st2**2*xb1*xb2
     . **2*xg1**3+2*log(xg1)*st2*xb1**6*xb2-2*log(xg1)*st2*xb1**6*xg1
     . -4*log(xg1)*st2*xb1**5*xb2*xg1-6*log(xg1)*st2*xb1**5*xb2+4*log
     . (xg1)*st2*xb1**5*xg1**2+6*log(xg1)*st2*xb1**5*xg1+ans36
      ans34=log(xg1)*st2**3*xb1**6*xb2-log(xg1)*st2**3*xb1**6*xg1-3*
     . log(xg1)*st2**3*xb1**5*xb2**2+log(xg1)*st2**3*xb1**5*xb2*xg1+2
     . *log(xg1)*st2**3*xb1**5*xg1**2+3*log(xg1)*st2**3*xb1**4*xb2**3
     . +3*log(xg1)*st2**3*xb1**4*xb2**2*xg1-5*log(xg1)*st2**3*xb1**4*
     . xb2*xg1**2-log(xg1)*st2**3*xb1**4*xg1**3-log(xg1)*st2**3*xb1**
     . 3*xb2**4-5*log(xg1)*st2**3*xb1**3*xb2**3*xg1+3*log(xg1)*st2**3
     . *xb1**3*xb2**2*xg1**2+3*log(xg1)*st2**3*xb1**3*xb2*xg1**3+2*
     . log(xg1)*st2**3*xb1**2*xb2**4*xg1+log(xg1)*st2**3*xb1**2*xb2**
     . 3*xg1**2-3*log(xg1)*st2**3*xb1**2*xb2**2*xg1**3-log(xg1)*st2**
     . 3*xb1*xb2**4*xg1**2+log(xg1)*st2**3*xb1*xb2**3*xg1**3-3*log(
     . xg1)*st2**2*xb1**6*xb2+3*log(xg1)*st2**2*xb1**6*xg1+3*log(xg1)
     . *st2**2*xb1**5*xb2**2+3*log(xg1)*st2**2*xb1**5*xb2*xg1+6*log(
     . xg1)*st2**2*xb1**5*xb2-6*log(xg1)*st2**2*xb1**5*xg1**2-6*log(
     . xg1)*st2**2*xb1**5*xg1+3*log(xg1)*st2**2*xb1**4*xb2**3-9*log(
     . xg1)*st2**2*xb1**4*xb2**2*xg1+ans35
      ans46=(xb2-xg1)
      ans33=ans34*ans46
      ans28=ans29+ans33
      ans47=(log(xb1)-log(xg1))
      ans27=2*ans28*ans47
      ans26=-ans27
      ans5=4*(3*(5*xb1**5-7*xb2**3+(7*xb2-8)*(xb2+1)*xb1**3+(12*xb2+5
     . )*xb1**4+(2*xb2**2-5*xb2-20)*xb1*xb2**2+(16*xb2**2+xb2-7)*xb1
     . **2*xb2)*st2**2-(((10*xb1**2+20*xb1*xb2+10*xb1-xb2-11)*xb1**3-
     . (5*xb2**2+5*xb2+8)*xb2**3-(10*xb2**2+13*xb2+31)*xb1*xb2**2+(27
     . *xb2**2+9*xb2+8)*xb1**2*xb2)*st2+2*(2*xb1**3*xb2+6*xb1**2*xb2
     . **2+xb1**2*xb2-xb1**2+xb1*xb2**3-xb1*xb2**2-6*xb1*xb2-2*xb2**2
     . )*(xb1-xb2)+(xb1**3+2*xb1**2*xb2+xb1**2+2*xb1*xb2**2-2*xb1*xb2
     . -3*xb1+xb2**3+xb2**2-3*xb2)*(5*xb1**2+4*xb1*xb2+5*xb2**2)*st2
     . **3))*(xb1-1)*(xb2-1)*xg1**2+ans6+ans10+ans14+ans22+ans26
      ans4=((((xb1-xb2)*st2-3*(xb1-2))*(xb1-xb2)*st2+2*xb1**2-2*xb1*
     . xb2-6*xb1-xb2**2+6*xb2+1)*(xb1-xb2)*st2+2*(xb1**2+1)*xb2+(xb2
     . **2-6*xb2+1)*xb1)*(log(xg1)+4)*(xb1-xb2)*(xb1-xg1)**2*(xb2-xg1
     . )**2*log(xg1)+4*(((10*xb1**4+9*xb1**2*xb2**2-5*xb2**4)*(xb2-1)
     . +10*(xb2+1)*xb1**5-(5*xb2**2+5*xb2+26)*xb1*xb2**3+(9*xb2**2+9*
     . xb2-2)*xb1**3*xb2)*st2+(xb1**3*xb2+xb1**3+xb1**2*xb2-xb1**2+
     . xb1*xb2**3+xb1*xb2**2-4*xb1*xb2+xb2**3-xb2**2)*(5*xb1**2+4*xb1
     . *xb2+5*xb2**2)*st2**3+2*(2*xb1**2*xb2+2*xb1**2+xb1*xb2**2+3*
     . xb1*xb2-4*xb1+xb2**2-5*xb2)*(xb1-xb2)*xb1*xb2-3*(5*(xb2+1)*xb1
     . **4+2*(xb2-8)*xb2**3+(2*xb2**2+7*xb2-13)*xb1*xb2**2+(2*xb2**2+
     . 7*xb2-5)*xb1**3+(5*xb2**2+7*xb2-8)*xb1**2*xb2)*st2**2*xb1)*(
     . xb1-1)*(xb2-1)*xg1+ans5
      ans3=4*((((xb1**2+13*xb2**2)*(xb2-1)+20*xb1**3)*xb1-(10*xb2**2+
     . 13*xb2+13)*xb2**2+(18*xb2**2-xb2-1)*xb1**2)*st2+2*((5*xb1**2*
     . xb2-xb1**2+4*xb1*xb2**2-3*xb1*xb2-xb1-2*xb2**2-2*xb2)*(xb1-xb2
     . )+(5*xb1**2+4*xb1*xb2+5*xb2**2)*(xb1**2+xb1*xb2-xb1+xb2**2-xb2
     . -1)*st2**3)+3*(7*(xb2+1)*xb2**2-10*xb1**4-(7*xb2-3)*xb1**3-(11
     . *xb2**2-11*xb2-4)*xb1*xb2-(14*xb2**2-7*xb2-3)*xb1**2)*st2**2)*
     . (xb1-1)*(xb2-1)*xg1**3+4*(3*(5*(xb1**2+xb2**2)*xb1+(2*xb2-9)*
     . xb2**2+(2*xb2-5)*xb1**2)*st2**2*xb1-((5*xb1**2+4*xb1*xb2+5*xb2
     . **2)*(xb1**2-xb1+xb2**2-xb2)*st2**3+2*(2*xb1+xb2-3)*(xb1-xb2)*
     . xb1*xb2)-(2*(5*xb1**3-5*xb1**2-9*xb2**2)*xb1-5*(xb2-1)*xb2**3+
     . 9*(xb2+1)*xb1**2*xb2)*st2)*(xb1-1)*(xb2-1)*xb1*xb2+ans4
      ans2=ans3*xg1
      ans1=-ans2
      r732=ans1/(16*(xb1-xb2)*(xb1-xg1)**2*(xb1-1)**2*(xb2-xg1)**2*(
     . xb2-1)**2*(xg1-1))

      ans8=-(xb2-6+5*xb1-(xb1-xb2)*st2)*(xb1-xb2)**2*(xb1-xg1)*(xb2-
     . xg1)**2*log(xg1)*xb2
      ans7=((2*((3*xb2**2-xg1)*(xg1+1)-15*xb2**3+(3*xg1**2+5*xg1+3)*
     . xb2+(5*xb2**2+xg1-3*(xg1+1)*xb2)*xb1)*xb1**2-(5*xb2**4+7*xg1**
     . 2+2*(23*xb2**2+5*xg1)*(xg1+1)*xb2-(41*xg1**2+42*xg1+41)*xb2**2
     . )*xb2)*xb1-(7*xb2**4-29*xg1**2-2*(7*xb2**2-16*xg1)*(xg1+1)*xb2
     . +7*(xg1**2-4*xg1+1)*xb2**2)*xb2**2+2*(28*xb2**4+xg1**2-2*(4*
     . xb2**2+xg1)*(xg1+1)*xb2-(8*xg1**2-7*xg1+8)*xb2**2)*xb1**2+((((
     . xg1+1)*xg1+9*xb2**3-(3*xg1**2+5*xg1+3)*xb2-(5*xb2**2+xg1-3*(
     . xg1+1)*xb2)*xb1)*xb1**2-(5*xb2**4+4*xg1**2-(26*xb2**2+17*xg1)*
     . (xg1+1)*xb2+(19*xg1**2+39*xg1+19)*xb2**2)*xb2)*xb1-(7*xb2**4+
     . 19*xg1**2-14*(xb2**2+2*xg1)*(xg1+1)*xb2+(7*xg1**2+44*xg1+7)*
     . xb2**2)*xb2**2-(16*xb2**4+xg1**2-(5*xb2**2+2*xg1)*(xg1+1)*xb2-
     . (5*xg1**2-7*xg1+5)*xb2**2)*xb1**2)*st2)*(xb1-1)*(xg1-1)+ans8
      ans9=(log(xb2)-log(xg1))*(xb1-xg1)
      ans6=2*ans7*ans9
      ans13=-((5*(xg1+1)-4*xb2-4*xb1)*xb1**2+((xg1+1)*xb2-4*xg1)*xb2-
     . 2*(xb2**2+3*xg1-2*(xg1+1)*xb2)*xb1-(((xg1+1-2*xb2-2*xb1)*xb1+2
     . *(xg1+1+xb2)*xb2)*xb1-((xg1+1)*xb2+2*xg1)*xb2)*st2)*(xb2-xg1)
     . **2*(xb2-1)**2*(xg1-1)*t134p(mb1,mb2,m1)-((xb2-6*xg1+5*xb1-(
     . xb1-xb2)*st2)*(xb1-1)**2*(xb2+xg1)*(xb2-1)**2*t134p(m1,mb2,m1)
     . -(xb2-6+5*xb1-(xb1-xb2)*st2)*(xb1-xg1)**2*(xb2-xg1)**2*(xb2+1)
     . *t134p(mu,mb2,m1)+(2*(2*xb2-3+xb1)-(xb1-xb2)*st2)*(xb1-xg1)**2
     . *(xb1+1)*(xb2-xg1)**2*t134p(mu,mb1,m1)-(2*(2*xb2-3*xg1+xb1)-(
     . xb1-xb2)*st2)*(xb1+xg1)*(xb1-1)**2*(xb2-1)**2*t134p(m1,mb1,m1)
     . )*(xb1-xb2)**2
      ans12=(((2*(((xg1+1-2*xb2)*xb1-(xb2-xg1)*(xb2-1))*xb1-(xb2**2+3
     . *xg1-2*(xg1+1)*xb2)*xb2)-((xg1+1-2*xb2)*(xb1+xb2)*(xb1-xb2)+2*
     . (xb2-xg1)*(xb2-1)*xb1)*st2)*t134p(mb2,mb1,m1)-((23*xb2**2+3*
     . xg1-13*(xg1+1)*xb2)*xb2-5*(3*xb2**2-xg1-(xg1+1)*xb2)*xb1-((7*
     . xb2**2+3*xg1-5*(xg1+1)*xb2)*xb2-(3*xb2**2-xg1-(xg1+1)*xb2)*xb1
     . )*st2)*t134p(mb2,mb2,m1))*(xb1-xg1)**2*(xb1-1)**2-(((5*(xg1+1)
     . +3*xb2)*xb1**2-(7*xb1**3+xb2*xg1)-((xg1+1)*xb2+3*xg1)*xb1)*st2
     . -4*(4*xb1**3+xb2*xg1+(xg1+1)*xb1*xb2-(2*(xg1+1)+3*xb2)*xb1**2)
     . )*(xb2-xg1)**2*(xb2-1)**2*t134p(mb1,mb1,m1))*(xg1-1)+((5*xb2+
     . 11)*xb2**2-10*xb1**3-2*(9*xb2-2)*xb1*xb2+(9*xb2-1)*xb1**2+(5*
     . xb1**2+4*xb1*xb2+5*xb2**2)*(xb1+xb2-2)*st2)*(xb1-1)*(xb2-1)*
     . xg1**3+ans13
      ans11=4*ans12*xg1
      ans10=-ans11
      ans19=-(xb2-xg1)**2*(xb2-1)**2*xb2**2*xg1-(3*xb2**6-3*xb2**2*
     . xg1**2-2*xg1**3-2*(6*xb2**4-7*xg1**2)*(xg1+1)*xb2-2*(3*xg1**2+
     . 11*xg1+3)*(xg1+1)*xb2**3+3*(5*xg1**2+12*xg1+5)*xb2**4)*xb1**2+
     . (2*(xb2**4+5*xg1**2)*(xg1+1)*xb2+xg1**3+2*(xg1**2+11*xg1+1)*(
     . xg1+1)*xb2**3-(4*xg1**2+15*xg1+4)*xb2**4-(11*xg1**2+32*xg1+11)
     . *xb2**2*xg1)*xb1*xb2+(2*(5*xb2**4-2*xg1**2)*(xg1+1)-5*xb2**5-(
     . xg1**2+4*xg1+1)*xb2**3-2*(3*xg1**2+13*xg1+3)*(xg1+1)*xb2**2+(
     . 16*xg1**2+43*xg1+16)*xb2*xg1)*xb1**3
      ans18=((2*(3*xb2**2+xg1)*(xg1+1)+xb2**3-(4*xg1**2+9*xg1+4)*xb2)
     . *xb1**5-((3*xb2**2+xg1-2*(xg1+1)*xb2)*xb1**6+(xb2-xg1)**2*(xb2
     . -1)**2*xb2**2*xg1)-((3*xb2**2+xg1)*(xg1**2+4*xg1+1)+2*(xg1+1)*
     . xb2**3-2*(xg1**2+5*xg1+1)*(xg1+1)*xb2)*xb1**4-(3*xb2**6+6*xb2
     . **2*xg1**2+xg1**3-2*(3*xb2**4+2*xb2**2*xg1+2*xg1**2)*(xg1+1)*
     . xb2+3*(xg1**2+4*xg1+1)*xb2**4)*xb1**2-(2*(xb2**4-2*xb2**2*xg1-
     . xg1**2)*(xg1+1)-xb2**5-2*(xg1**2+4*xg1+1)*xb2**3+(5*xg1**2+11*
     . xg1+5)*xb2*xg1)*xb1**3+(2*((xb2**4+2*xg1**2)*(xg1+1)*xb2-xg1**
     . 3+(xg1**2+5*xg1+1)*(xg1+1)*xb2**3)-(4*xg1**2+9*xg1+4)*xb2**4-(
     . 5*xg1**2+11*xg1+5)*xb2**2*xg1)*xb1*xb2)*st2+2*((xg1**2+4*xg1+1
     . )*xg1-4*(xg1+1)*xb2**3-2*(xg1**2+8*xg1+1)*(xg1+1)*xb2+3*(3*xg1
     . **2+8*xg1+3)*xb2**2)*xb1**4+2*(3*xb2**2+xg1-2*(xg1+1)*xb2)*xb1
     . **6+2*(xb2**2-4*xb2*xg1-4*xb2+2*xg1)*(2*xb2-xg1-1)*xb1**5+
     . ans19
      ans20=(log(xb2)-log(xg1))*(xg1-1)
      ans17=ans18*ans20
      ans25=-(14*xb1**5+24*xb1**4*xb2-28*xb1**4*xg1-28*xb1**4-16*xb1
     . **3*xb2**2-8*xb1**3*xb2*xg1-8*xb1**3*xb2+14*xb1**3*xg1**2+16*
     . xb1**3*xg1+14*xb1**3+5*xb1**2*xb2**3+3*xb1**2*xb2**2*xg1+3*xb1
     . **2*xb2**2-8*xb1**2*xb2*xg1**2+13*xb1**2*xb2*xg1-8*xb1**2*xb2+
     . 4*xb1**2*xg1**2+4*xb1**2*xg1-3*xb1*xb2**3*xg1-3*xb1*xb2**3+3*
     . xb1*xb2**2*xg1**2+6*xb1*xb2**2*xg1+3*xb1*xb2**2-3*xb1*xb2*xg1
     . **2-3*xb1*xb2*xg1-10*xb1*xg1**2+xb2**3*xg1-xb2**2*xg1**2-xb2**
     . 2*xg1+xb2*xg1**2)*(xb1-xb2)
      ans24=((xb2-xg1)*(xb2-1)*xb2**2*xg1+7*xb1**6-(14*(xg1+1)-5*xb2)
     . *xb1**5-(2*(13*(xg1+1)-8*xb2)*xb2-(7*xg1**2+44*xg1+7))*xb1**4-
     . ((3*xb2**2+2*xg1)*(xg1+1)*xb2-4*xg1**2-(3*xg1**2+5*xg1+3)*xb2
     . **2)*xb1*xb2-((5*xb2**2+28*xg1)*(xg1+1)+9*xb2**3-(19*xg1**2+39
     . *xg1+19)*xb2)*xb1**3+(5*xb2**4+19*xg1**2-17*(xg1+1)*xb2*xg1-(5
     . *xg1**2-7*xg1+5)*xb2**2)*xb1**2)*st2+ans25
      ans26=(xb2-1)*(xg1-1)
      ans23=ans24*ans26
      ans27=-(2*(2*xb2-3+xb1)-(xb1-xb2)*st2)*(xb1-xb2)**2*(xb1-xg1)**
     . 2*(xb2-xg1)*log(xg1)*xb1
      ans22=ans23+ans27
      ans28=(xb2-xg1)
      ans21=ans22*ans28
      ans16=ans17+ans21
      ans29=(log(xb1)-log(xg1))
      ans15=2*ans16*ans29
      ans14=-ans15
      ans5=(((xb2-xg1)*(xb2-1)*xb2**2*xg1+2*xb1**6-2*(2*(xg1+1)-xb2)*
     . xb1**5-((21*(xg1+1)-17*xb2)*xb2-(2*xg1**2+25*xg1+2))*xb1**4-2*
     . ((xb2**2-xg1)*(xg1+1)*xb2+xg1**2-(xg1**2+1)*xb2**2)*xb1*xb2-2*
     . ((xb2**2+9*xg1)*(xg1+1)+6*xb2**3-4*(2*xg1**2+3*xg1+2)*xb2)*xb1
     . **3+(3*xb2**4+13*xg1**2+(5*xb2**2-7*xg1)*(xg1+1)*xb2-2*(4*xg1
     . **2+xg1+4)*xb2**2)*xb1**2)*st2+(xb2-xg1)*(xb2-1)*xb2**2*xg1-4*
     . xb1**6+4*(2*(xg1+1)-xb2)*xb1**5-2*((21*(xg1+1)-25*xb2)*xb2+2*
     . xg1**2-17*xg1+2)*xb1**4+((xb2**2-30*xg1)*(xg1+1)-39*xb2**3+(34
     . *xg1**2+21*xg1+34)*xb2)*xb1**3-((2*xb2**2-11*xg1)*(xg1+1)*xb2+
     . 17*xg1**2-(2*xg1**2-9*xg1+2)*xb2**2)*xb1*xb2+(3*xb2**4+22*xg1
     . **2+(23*xb2**2+8*xg1)*(xg1+1)*xb2-(26*xg1**2+23*xg1+26)*xb2**2
     . )*xb1**2)*(log(xb1)-log(xg1))**2*(xb2-xg1)*(xb2-1)*(xg1-1)+
     . ans6+ans10+ans14
      ans4=((2*xb2**4-35*xg1**2-4*(xb2**2-12*xg1)*(xg1+1)*xb2+(2*xg1
     . **2-59*xg1+2)*xb2**2)*xb2**2-(2*xb1-17*xb2-2*xg1-2)*(3*xb2**2-
     . 2*xb2*xg1-2*xb2+xg1)*xb1**3+(2*xb2**4+19*xg1**2+(63*xb2**2-xg1
     . )*(xg1+1)*xb2-5*(10*xg1**2+9*xg1+10)*xb2**2)*xb1*xb2-(67*xb2**
     . 4+2*xg1**2-(xb2**2-13*xg1)*(xg1+1)*xb2-(34*xg1**2+25*xg1+34)*
     . xb2**2)*xb1**2-(((7*(3*xb2**2+xg1)*(xg1+1)*xb2-2*(xb2**2+xg1)*
     . (xb2**2-xg1)-8*(2*xg1**2+3*xg1+2)*xb2**2)*xb2-(xb1-4*xb2-xg1-1
     . )*(3*xb2**2-2*xb2*xg1-2*xb2+xg1)*xb1**2)*xb1-(2*xb2**4+13*xg1
     . **2-2*(2*xb2**2+9*xg1)*(xg1+1)*xb2+(2*xg1**2+25*xg1+2)*xb2**2)
     . *xb2**2-(17*xb2**4+xg1**2-2*(xb2**2-xg1)*(xg1+1)*xb2-2*(4*xg1
     . **2+xg1+4)*xb2**2)*xb1**2)*st2)*(log(xb2)-log(xg1))**2*(xb1-
     . xg1)*(xb1-1)*(xg1-1)+ans5
      ans3=4*((2*(11*xb2+5+5*xb1)*xb1-(2*xb2**2-3*xb2+9))*xb1**3-(5*
     . xb2**2+5*xb2+6)*xb2**3-(8*xb2**2+9*xb2+33)*xb1*xb2**2+(25*xb2
     . **2+xb2+6)*xb1**2*xb2-(xb1**3+2*xb1**2*xb2+xb1**2+2*xb1*xb2**2
     . -2*xb1*xb2-3*xb1+xb2**3+xb2**2-3*xb2)*(5*xb1**2+4*xb1*xb2+5*
     . xb2**2)*st2)*(xb1-1)*(xb2-1)*xg1**2+ans4
      ans2=4*(2*((xb2-9)*xb2**2+5*xb1**3+(xb2-5)*xb1**2)*xb1-5*(xb2-1
     . )*xb2**3+(5*xb2+9)*xb1**2*xb2-(5*xb1**2+4*xb1*xb2+5*xb2**2)*(
     . xb1**2-xb1+xb2**2-xb2)*st2)*(xb1-1)*(xb2-1)*xb1*xb2-(xb2-6+2*
     . xb1-(xb1-xb2)*st2)*(log(xg1)+4)*(xb1-xb2)**3*(xb1-xg1)**2*(xb2
     . -xg1)**2*log(xg1)-4*((3*xb2+1+20*xb1)*xb1**3-(10*xb2**2+11*xb2
     . +11)*xb2**2+(14*xb2**2-3*xb2+1)*xb1**2+(15*xb2**2-15*xb2-4)*
     . xb1*xb2-2*(5*xb1**2+4*xb1*xb2+5*xb2**2)*(xb1**2+xb1*xb2-xb1+
     . xb2**2-xb2-1)*st2)*(xb1-1)*(xb2-1)*xg1**3-4*(5*(2*(xb2+1)*xb1
     . **5-(xb2-1)*xb2**4)+(5*xb2+7)*xb1**3*xb2**2+2*(xb2**2+6*xb2-5)
     . *xb1**4+(2*xb2**2+7*xb2-13)*xb1**2*xb2**2-(5*xb2**2+3*xb2+24)*
     . xb1*xb2**3-(xb1**3*xb2+xb1**3+xb1**2*xb2-xb1**2+xb1*xb2**3+xb1
     . *xb2**2-4*xb1*xb2+xb2**3-xb2**2)*(5*xb1**2+4*xb1*xb2+5*xb2**2)
     . *st2)*(xb1-1)*(xb2-1)*xg1+ans3
      ans30=(st2-1)*st2*xg1
      ans1=ans2*ans30
      r73p2=ans1/(16*(xb1-xb2)*(xb1-xg1)**2*(xb1-1)**2*(xb2-xg1)**2*(
     . xb2-1)**2*(xg1-1))

      r732 = r732 + r73p2

      r72=r712+r722+r732

c--r8
      r812=(((log(xb2)-log(xg1))**2*(xb1-xg1)**2*(xb2-2*xg1)*xgl+2*(2
     . *xb1*xb2*xgl+3*xg1**3)*(xb1-xb2)-(log(xb1)-log(xg1))**2*(xb1-2
     . *xg1)*(xb2-xg1)**2*xgl-2*(xb2-2*xg1+xb1)*(xb1-xb2)*(xg1-xgl)*
     . t134p(m1,mg,m1)*xg1-2*(3*xb2-2*xgl+3*xb1)*(xb1-xb2)*xg1**2+2*(
     . (3*xb2-2*xgl)*xb1-2*xb2*xgl)*(xb1-xb2)*xg1-(log(xgl)-4-log(xg1
     . ))*(log(xg1)-log(xgl))*(xb1-xb2)*(xb1-xg1)*(xb2-xg1)*xgl-2*((
     . log(xg1)-log(xgl))*(xb2-2*xg1)*xgl+2*(xb2**2-xb2*xg1-xg1*xgl))
     . *(log(xb2)-log(xg1))*(xb1-xg1)**2+2*((log(xg1)-log(xgl))*(xb1-
     . 2*xg1)*xgl+2*(xb1**2-xb1*xg1-xg1*xgl))*(log(xb1)-log(xg1))*(
     . xb2-xg1)**2-2*((2*xg1-xgl-xb1)*(xb2-xg1)**2*t134p(mb1,mg,m1)-(
     . 2*xg1-xgl-xb2)*(xb1-xg1)**2*t134p(mb2,mg,m1))*xg1)*xg1)/(12*(
     . xb1-xb2)*(xb1-xg1)**2*(xb2-xg1)**2)

      ans9=(xb2-xg1)**2*(xb2-1)**2*(xg1-1)
      ans8=(2*(2*(3*(((2*xgl+1)*xg1+2*xgl+(xgl+1+xg1)*xb2)*xb1**2+xb1
     . **4-xb2*xg1*xgl-(xb2+xgl)*xb1*xg1-(3*xgl+1+xg1+xb2)*xb1**3)*
     . st2**2+(xb1**3-xb1**2*xg1-xb1**2*xgl-xb1**2+xb1*xg1+xg1*xgl)*(
     . xb1-xb2)-2*(((3*xgl+1)*xg1+3*xgl+(xgl+1+xg1)*xb2)*xb1**2+xb1**
     . 4-xb2*xg1*xgl-(xb2+2*xgl)*xb1*xg1-(4*xgl+1+xg1+xb2)*xb1**3)*
     . st2)-(2*(3*xb1**3+2*xb2*xg1-2*(xg1+1)*xb1**2-((xg1+1)*xb2-xg1)
     . *xb1)*st2-(3*(2*(xb1**3+xb2*xg1)-(xb1+xb2)*(xg1+1)*xb1)*st2**2
     . +(xb1*xg1+xb1-2*xg1)*(xb1-xb2)))*log(xgl)*xgl+(2*(3*xb1**3+2*
     . xb2*xg1-2*(xg1+1)*xb1**2-((xg1+1)*xb2-xg1)*xb1)*st2-(3*(2*(xb1
     . **3+xb2*xg1)-(xb1+xb2)*(xg1+1)*xb1)*st2**2+(xb1*xg1+xb1-2*xg1)
     . *(xb1-xb2)))*log(xg1)*xgl)-(2*(3*xb1**3+2*xb2*xg1-2*(xg1+1)*
     . xb1**2-((xg1+1)*xb2-xg1)*xb1)*st2-(3*(2*(xb1**3+xb2*xg1)-(xb1+
     . xb2)*(xg1+1)*xb1)*st2**2+(xb1*xg1+xb1-2*xg1)*(xb1-xb2)))*(log(
     . xb1)-log(xg1))*xgl)*(log(xb1)-log(xg1))*ans9
      ans7=2*(((3*(2*(xb2**3-xg1*xgl)+3*(xg1+1)*xb2*xgl-(4*xgl+1+xg1)
     . *xb2**2+((2*xgl-1-xg1)*xb2-((xgl-2)*xg1+xgl))*xb1)*st2**2+2*((
     . 2*xgl-1-xg1)*xb2-((xgl-2)*xg1+xgl))*(xb1-xb2)-2*(((5*xgl-1)*
     . xg1+5*xgl)*xb2+3*(xb2**3-xg1*xgl)-(7*xgl+1+xg1)*xb2**2+2*((2*
     . xgl-1-xg1)*xb2-((xgl-2)*xg1+xgl))*xb1)*st2)*(xb1-xg1)**2*(xb1-
     . 1)*(xg1-1)*t134p(mb2,mg,m1)-(((4*xgl-3+9*xb2)*xb1+2*((xgl-3)*
     . xb2-3*xgl))*(2*st2-1)-3*((2*xgl-3)*xb2-4*xgl+(2*xgl-3+6*xb2)*
     . xb1)*st2**2)*(xb1-xb2)*(xb2-1)*xg1**3)*(xb1-1)-(((2*(2*xb1-xb2
     . -xg1)-3*(xb1-xb2)*st2)*(xb1-xb2)*st2-(2*(xb1-2*xg1)*xb1+xb2**2
     . -2*xb2*xg1+3*xg1**2))*(xb1-1)**2*(xb2-1)**2*(xg1-xgl)*t134p(m1
     . ,mg,m1)+((2*(2*xb1-xb2-1)-3*(xb1-xb2)*st2)*(xb1-xb2)*st2-(2*(
     . xb1-2)*xb1+xb2**2-2*xb2+3))*(xb1-xg1)**2*(xb2-xg1)**2*(xgl-1)*
     . t134p(mu,mg,m1))*(xb1-xb2))*xg1+ans8
      ans6=-2*(2*(3*((((2*xgl+1)*xg1+2*xgl)*xb2+xb2**3-xg1*xgl-(3*xgl
     . +1+xg1)*xb2**2)*xb2+((xgl+1+xg1)*xb2**2-(xb2**3+xb2*xg1+xg1*
     . xgl))*xb1)*st2**2+2*((xgl+1+xg1)*xb2**2-(xb2**3+xb2*xg1+xg1*
     . xgl))*(xb1-xb2)-2*((((3*xgl+2)*xg1+3*xgl)*xb2+2*xb2**3-xg1*xgl
     . -(5*xgl+2+2*xg1)*xb2**2)*xb2+2*((xgl+1+xg1)*xb2**2-(xb2**3+xb2
     . *xg1+xg1*xgl))*xb1)*st2)+(3*(((xg1+1)*xb2-2*xg1)*xb1+(xg1+1-2*
     . xb2)*xb2**2)*st2**2+2*((xg1+1)*xb2-2*xg1)*(xb1-xb2)+2*((3*xb2
     . **2-xg1-(xg1+1)*xb2)*xb2-2*((xg1+1)*xb2-2*xg1)*xb1)*st2)*(log(
     . xg1)-log(xgl))*xgl)*(log(xb2)-log(xg1))*(xb1-xg1)**2*(xb1-1)**
     . 2*(xg1-1)+ans7
      ans5=2*(3*((4*xgl+1+xg1-2*xb1)*xb1**2+((xgl-2)*xg1+xgl)*xb2+2*
     . xg1*xgl-((2*xgl-1-xg1)*xb2+3*(xg1+1)*xgl)*xb1)*st2**2-(xb1*xg1
     . -2*xb1*xgl+xb1+xg1*xgl-2*xg1+xgl)*(xb1-xb2)-2*((5*xgl+2+2*xg1-
     . 3*xb1)*xb1**2+((xgl-2)*xg1+xgl)*xb2+3*xg1*xgl-((4*xgl+1)*xg1+4
     . *xgl+(2*xgl-1-xg1)*xb2)*xb1)*st2)*(xb2-xg1)**2*(xb2-1)**2*(xg1
     . -1)*t134p(mb1,mg,m1)*xg1+ans6
      ans4=2*(2*((xb2**2+3*xg1-(xg1+1)*xb2-2*(xg1+1-xb1)*xb1)*(2*st2-
     . 1)-3*(xb2**2+2*xg1-(xg1+1)*xb2-(xg1+1-xb1)*xb1)*st2**2)*(xb1-1
     . )*(xb2-1)*(xg1-1)-((2*(2*xb1-xb2-1)-3*(xb1-xb2)*st2)*(xb1-xb2)
     . *st2-(2*(xb1-2)*xb1+xb2**2-2*xb2+3))*(xb1-xg1)*(xb2-xg1)*log(
     . xg1))*(log(xg1)-log(xgl))*(xb1-xb2)*(xb1-xg1)*(xb2-xg1)*xgl-2*
     . (((3*xb2**3-10*xgl-6*(xgl+3)*xb2+(4*xgl-3)*xb2**2)*xb1+((9*xb2
     . +4*xgl-3)*(2*xb2+1)+2*(3*xb2+2*xgl)*xb1)*xb1**2+2*((xb2+2)*(
     . xb2-2)*xgl+(xgl-3)*xb2)*xb2)*(2*st2-1)-3*((2*(xb2**2-3)*xgl+(2
     . *xgl-3)*xb2)*xb2+((6*xb2+2*xgl-3)*(2*xb2+1)+(3*xb2+2*xgl)*xb1)
     . *xb1**2+(3*xb2**3+4*xb2**2*xgl-6*xgl-4*(xgl+3)*xb2)*xb1)*st2**
     . 2)*(xb1-xb2)*(xb1-1)*(xb2-1)*xg1**2+ans5
      ans3=(3*(((xg1+1)*xb2-2*xg1)*xb1+(xg1+1-2*xb2)*xb2**2)*st2**2+2
     . *((xg1+1)*xb2-2*xg1)*(xb1-xb2)+2*((3*xb2**2-xg1-(xg1+1)*xb2)*
     . xb2-2*((xg1+1)*xb2-2*xg1)*xb1)*st2)*(log(xb2)-log(xg1))**2*(
     . xb1-xg1)**2*(xb1-1)**2*(xg1-1)*xgl-2*(3*((3*xb2+2*xgl)*(xb2+1)
     . *xb1**3+2*(xb2-1)*xb2**2*xgl+(3*xb2**2+9*xb2+2*xgl)*(xb2-1)*
     . xb1**2+((2*xgl-9)*xb2-8*xgl+(2*xgl+3)*xb2**2)*xb1*xb2)*st2**2-
     . (2*((3*xb2+2*xgl)*(xb2+1)*xb1**3+(xb2-1)*xb2**2*xgl)+(3*xb2**2
     . +12*xb2+4*xgl)*(xb2-1)*xb1**2+((2*xgl-15)*xb2-12*xgl+(2*xgl+3)
     . *xb2**2)*xb1*xb2)*(2*st2-1))*(xb1-xb2)*(xb1-1)*(xb2-1)*xg1+
     . ans4
      ans2=(2*(3*((3*xb2+2*xgl)*xb1**2+2*(xb2-1)*xb2*xgl+(3*xb2**2-6*
     . xb2-2*xgl)*xb1)*st2**2-(2*((3*xb2+2*xgl)*xb1**2+(xb2-1)*xb2*
     . xgl)+(3*xb2**2-9*xb2-4*xgl)*xb1)*(2*st2-1))*(xb1-1)*(xb2-1)*
     . xb1*xb2-((2*(2*xb1-xb2-1)-3*(xb1-xb2)*st2)*(xb1-xb2)*st2-(2*(
     . xb1-2)*xb1+xb2**2-2*xb2+3))*(log(xg1)+4)*(xb1-xg1)**2*(xb2-xg1
     . )**2*log(xg1)*xgl+((xb2**2+3*xg1-(xg1+1)*xb2-2*(xg1+1-xb1)*xb1
     . )*(2*st2-1)-3*(xb2**2+2*xg1-(xg1+1)*xb2-(xg1+1-xb1)*xb1)*st2**
     . 2)*(log(xg1)-log(xgl))**2*(xb1-xg1)*(xb1-1)*(xb2-xg1)*(xb2-1)*
     . (xg1-1)*xgl+2*((((8*xgl-3+15*xb2)*xb1+3*(4*xb2+2*xgl+1)*(xb2-1
     . ))*xb1-2*(3*((xgl+1)*xb2+xgl)-(2*xgl-3)*xb2**2))*(2*st2-1)-3*(
     . (4*xgl-3)*xb2**2-4*xgl-(4*xgl+3)*xb2+((4*xgl-3+9*xb2)*xb1+(9*
     . xb2+4*xgl+3)*(xb2-1))*xb1)*st2**2)*(xb1-1)*(xb2-1)*xg1**3)*(
     . xb1-xb2)+ans3
      ans1=ans2*xg1
      r822=ans1/(8*(xb1-xb2)*(xb1-xg1)**2*(xb1-1)**2*(xb2-xg1)**2*(
     . xb2-1)**2*(xg1-1))

      ans6=(2*(2*(((2*xgl+1)*xg1+2*xgl+(xgl+1+xg1)*xb2)*xb1**2+xb1**4
     . -xb2*xg1*xgl-(xb2+xgl)*xb1*xg1-(3*xgl+1+xg1+xb2)*xb1**3)+(2*(
     . xb1**3+xb2*xg1)-(xb1+xb2)*(xg1+1)*xb1)*log(xgl)*xgl-(2*(xb1**3
     . +xb2*xg1)-(xb1+xb2)*(xg1+1)*xb1)*log(xg1)*xgl)+(2*(xb1**3+xb2*
     . xg1)-(xb1+xb2)*(xg1+1)*xb1)*(log(xb1)-log(xg1))*xgl)*(log(xb1)
     . -log(xg1))*(xb2-xg1)**2*(xb2-1)**2*(xg1-1)
      ans5=2*((2*(xb2**3-xg1*xgl)+3*(xg1+1)*xb2*xgl-(4*xgl+1+xg1)*xb2
     . **2+((2*xgl-1-xg1)*xb2-((xgl-2)*xg1+xgl))*xb1)*(xb1-xg1)**2*(
     . xb1-1)**2*(xg1-1)*t134p(mb2,mg,m1)+(((2*xgl-3)*xb2-4*xgl+(2*
     . xgl-3+6*xb2)*xb1)*(xb1-1)*(xb2-1)*xg1**3+((xb1-xg1)**2*(xb2-
     . xg1)**2*(xgl-1)*t134p(mu,mg,m1)+(xb1-1)**2*(xb2-1)**2*(xg1-xgl
     . )*t134p(m1,mg,m1))*(xb1-xb2)**2)*(xb1-xb2))*xg1-2*(2*((((2*xgl
     . +1)*xg1+2*xgl)*xb2+xb2**3-xg1*xgl-(3*xgl+1+xg1)*xb2**2)*xb2+((
     . xgl+1+xg1)*xb2**2-(xb2**3+xb2*xg1+xg1*xgl))*xb1)+(((xg1+1)*xb2
     . -2*xg1)*xb1+(xg1+1-2*xb2)*xb2**2)*(log(xg1)-log(xgl))*xgl)*(
     . log(xb2)-log(xg1))*(xb1-xg1)**2*(xb1-1)**2*(xg1-1)+ans6
      ans4=2*((2*(xb2**2-3)*xgl+(2*xgl-3)*xb2)*xb2+((6*xb2+2*xgl-3)*(
     . 2*xb2+1)+(3*xb2+2*xgl)*xb1)*xb1**2+(3*xb2**3+4*xb2**2*xgl-6*
     . xgl-4*(xgl+3)*xb2)*xb1)*(xb1-xb2)*(xb1-1)*(xb2-1)*xg1**2-2*(2*
     . (xb2**2+2*xg1-(xg1+1)*xb2-(xg1+1-xb1)*xb1)*(xb1-1)*(xb2-1)*(
     . xg1-1)-(xb1-xb2)**2*(xb1-xg1)*(xb2-xg1)*log(xg1))*(log(xg1)-
     . log(xgl))*(xb1-xb2)*(xb1-xg1)*(xb2-xg1)*xgl+2*((4*xgl+1+xg1-2*
     . xb1)*xb1**2+((xgl-2)*xg1+xgl)*xb2+2*xg1*xgl-((2*xgl-1-xg1)*xb2
     . +3*(xg1+1)*xgl)*xb1)*(xb2-xg1)**2*(xb2-1)**2*(xg1-1)*t134p(mb1
     . ,mg,m1)*xg1+ans5
      ans3=((((xg1+1)*xb2-2*xg1)*xb1+(xg1+1-2*xb2)*xb2**2)*(log(xb2)-
     . log(xg1))**2*(xb1-1)**2*(xg1-1)+(log(xg1)+4)*(xb1-xb2)**3*(xb2
     . -xg1)**2*log(xg1))*(xb1-xg1)**2*xgl+2*((3*xb2+2*xgl)*xb1**2+2*
     . (xb2-1)*xb2*xgl+(3*xb2**2-6*xb2-2*xgl)*xb1)*(xb1-xb2)*(xb1-1)*
     . (xb2-1)*xb1*xb2-(xb2**2+2*xg1-(xg1+1)*xb2-(xg1+1-xb1)*xb1)*(
     . log(xg1)-log(xgl))**2*(xb1-xb2)*(xb1-xg1)*(xb1-1)*(xb2-xg1)*(
     . xb2-1)*(xg1-1)*xgl-2*((4*xgl-3)*xb2**2-4*xgl-(4*xgl+3)*xb2+((4
     . *xgl-3+9*xb2)*xb1+(9*xb2+4*xgl+3)*(xb2-1))*xb1)*(xb1-xb2)*(xb1
     . -1)*(xb2-1)*xg1**3-2*((3*xb2+2*xgl)*(xb2+1)*xb1**3+2*(xb2-1)*
     . xb2**2*xgl+(3*xb2**2+9*xb2+2*xgl)*(xb2-1)*xb1**2+((2*xgl-9)*
     . xb2-8*xgl+(2*xgl+3)*xb2**2)*xb1*xb2)*(xb1-xb2)*(xb1-1)*(xb2-1)
     . *xg1+ans4
      ans7=(st2-1)*st2*xg1
      ans2=3*ans3*ans7
      ans1=-ans2
      r82p2=ans1/(8*(xb1-xb2)*(xb1-xg1)**2*(xb1-1)**2*(xb2-xg1)**2*(
     . xb2-1)**2*(xg1-1))

      r822 = r822 + r82p2

      r82=r812+r822

c--r9
      ans3=-((2*(3*((xb2**2-8*xb2*xg1+5*xg1**2)*xb2-(xb2+xg1)*xb1**2+
     . (6*xb2**2-3*xb2*xg1+xg1**2)*xb1)*(st2-1)*st2+2*(xb1-xg1)*(3*
     . xb2-2*xg1)*xb2)*(log(xb2)-log(xg1))*(xb1-xb2)-((((2*xb2+xg1)*
     . xb1-3*(2*xb2-xg1)*xb2)*xb2-3*(st2-1)*(xb1*xg1-2*xb2**2+xb2*xg1
     . )*(xb1-3*xb2)*st2)*(log(xb2)-log(xg1))**2*(xb1-xg1)-4*(3*(xb2-
     . 2*xg1+xb1)*(st2-1)*st2-xg1)*(xb1-xb2)**2*(xb2-xg1)))*(xb1-xg1)
     . +((6*xb1**2-xb2*xg1-(2*xb2+3*xg1)*xb1)*xb1+3*(st2-1)*(2*xb1**2
     . -xb1*xg1-xb2*xg1)*(3*xb1-xb2)*st2)*(log(xb1)-log(xg1))**2*(xb2
     . -xg1)**2)
      ans2=2*((2*(3*((2*st2**2-2*st2+1)*xb1*xb2+(st2-1)*(xb1**2-xb1*
     . xb2+xb2**2)*st2)*xg1**2+(3*st2**2-3*st2+1)*xb1**2*xb2**2)*(xb1
     . +xb2)-(2*(3*st2**2-3*st2+2)*xb1*xb2+3*(st2-1)*(xb1**2+xb2**2)*
     . st2)*xg1**3-(8*(3*st2**2-3*st2+1)*xb1**2*xb2**2+3*(st2-1)*(xb1
     . **4+xb2**4)*st2+(3*st2**2-3*st2+2)*(xb1**2+xb2**2)*xb1*xb2)*
     . xg1)*(log(xb2)-log(xg1))-(3*((xb2-xg1)*xb2*xg1-xb1**3-2*(3*xb2
     . -4*xg1)*xb1**2+(xb2**2+3*xb2*xg1-5*xg1**2)*xb1)*(st2-1)*st2-2*
     . (3*xb1-2*xg1)*(xb2-xg1)*xb1)*(xb1-xb2)*(xb2-xg1))*(log(xb1)-
     . log(xg1))+ans3
      ans1=ans2*xg1
      r912=ans1/(24*(xb1-xb2)**2*(xb1-xg1)**2*(xb2-xg1)**2)

      r91p2=(-(2*((((xb1+xb2)*xg1**3-2*xb1**2*xb2**2-2*(xb1**2+xb1*
     . xb2+xb2**2)*xg1**2)*(xb1+xb2)+(xb1**4+xb1**3*xb2+8*xb1**2*xb2
     . **2+xb1*xb2**3+xb2**4)*xg1)*(log(xb2)-log(xg1))+((xb2-xg1)*xb2
     . *xg1-xb1**3-2*(3*xb2-4*xg1)*xb1**2+(xb2**2+3*xb2*xg1-5*xg1**2)
     . *xb1)*(xb1-xb2)*(xb2-xg1))*(log(xb1)-log(xg1))+(2*((xb2**2-8*
     . xb2*xg1+5*xg1**2)*xb2-(xb2+xg1)*xb1**2+(6*xb2**2-3*xb2*xg1+xg1
     . **2)*xb1)*(xb1-xb2)-((2*xb2-xg1)*xb2-xb1*xg1)*(log(xb2)-log(
     . xg1))*(xb1-3*xb2)*(xb1-xg1))*(log(xb2)-log(xg1))*(xb1-xg1)+((
     . log(xb1)-log(xg1))**2*(2*xb1**2-xb1*xg1-xb2*xg1)*(3*xb1-xb2)*(
     . xb2-xg1)+4*(xb1+xb2-2*xg1)*(xb1-xb2)**2*(xb1-xg1))*(xb2-xg1))*
     . (st2-1)*st2*xg1)/(24*(xb1-xb2)**2*(xb1-xg1)**2*(xb2-xg1)**2)

      r912 = r912 + r91p2

      ans6=(2*(3*(5*xb2**2-xg1-2*(xg1+1)*xb2)*xb2**2+(xb2**2-xg1)*xb1
     . **2-(9*xb2**2-11*xg1+(xg1+1)*xb2)*xb1*xb2)*st2+3*(6*(xg1+1-2*
     . xb2)*xb2**3-(xb1-7*xb2)*(xb2**2-xg1)*xb1)*st2**2+(xb1*xb2**2-
     . xb1*xg1-3*xb2**3+2*xb2**2*xg1+2*xb2**2-xb2*xg1)*(xb1-3*xb2)*
     . st2**3+6*(xb1-xb2)*(xb2**2-xg1)*xb2)*(log(xb2)-log(xg1))**2*(
     . xb1-xg1)*(xb1-1)**2*(xg1-1)
      ans5=(4*((xb2**2+xg1-3*(xg1+1)*xb2)*xb1+2*(xb1**2+xg1)*xb2+(xb1
     . **2-xb1*xg1-xb1+xb2**2-xb2*xg1-xb2+2*xg1)*(xb1-xb2)*st2**3+3*(
     . (xg1+1+2*xb2)*xb1**2-(xb1**3-2*xb2*xg1)-(3*(xg1+1)-xb2)*xb1*
     . xb2)*st2**2-(2*(xg1+1+3*xb2-xb1)*xb1**2-(xb2**2-5*xg1-(xg1+1)*
     . xb2)*xb2+(3*xb2**2+xg1-9*(xg1+1)*xb2)*xb1)*st2)*(xb1-1)*(xb2-1
     . )*(xg1-1)+((((xb1-xb2)*st2-3*(xb1-2))*(xb1-xb2)*st2+2*xb1**2-2
     . *xb1*xb2-6*xb1-xb2**2+6*xb2+1)*(xb1-xb2)*st2+2*(xb1**2+1)*xb2+
     . (xb2**2-6*xb2+1)*xb1)*(log(xg1)+4)*(xb1-xg1)*(xb2-xg1)*log(xg1
     . ))*(xb1-xb2)*(xb2-xg1)+ans6
      ans7=(xb1-xg1)
      ans4=ans5*ans7
      ans14=-((3*(3*xb1**2*xb2**2-xb1**2*xb2*xg1-xb1**2*xb2-xb1**2*
     . xg1-11*xb1*xb2**3+5*xb1*xb2**2*xg1+5*xb1*xb2**2+xb1*xb2*xg1+12
     . *xb2**4-8*xb2**3*xg1-8*xb2**3+4*xb2**2*xg1)*st2**2-4*(xb1-xb2)
     . *(2*xb2-xg1-1)*xb2**2)*(xb1-xg1)*(xb1-1)-(3*xb1**3*xb2**2-xb1
     . **3*xb2*xg1-xb1**3*xb2-xb1**3*xg1-8*xb1**2*xb2**3+3*xb1**2*xb2
     . **2*xg1+3*xb1**2*xb2**2+xb1**2*xb2*xg1**2-2*xb1**2*xb2*xg1+xb1
     . **2*xb2+xb1**2*xg1**2+xb1**2*xg1+8*xb1*xb2**3*xg1+8*xb1*xb2**3
     . -6*xb1*xb2**2*xg1**2-9*xb1*xb2**2*xg1-6*xb1*xb2**2+3*xb1*xb2*
     . xg1**2+3*xb1*xb2*xg1-xb1*xg1**2-xb2**5+2*xb2**4*xg1+2*xb2**4-
     . xb2**3*xg1**2-12*xb2**3*xg1-xb2**3+8*xb2**2*xg1**2+8*xb2**2*
     . xg1-5*xb2*xg1**2)*(xb1-xb2)*st2**3)
      ans13=((2*(3*xb2**2-xg1-(xg1+1)*xb2)*xb1**3+(xb2**4-34*xb2**3*
     . xg1-34*xb2**3+21*xb2**2*xg1**2+18*xb2**2*xg1+21*xb2**2+7*xg1**
     . 2)*xb2+2*((2*xb2**2+xg1)*(xg1+1)-13*xb2**3+(xg1**2+5*xg1+1)*
     . xb2)*xb1**2+2*((4*xb2**2+xg1)*(4*xb2**2-xg1)+(3*xb2**2-4*xg1)*
     . (xg1+1)*xb2-(5*xg1**2+3*xg1+5)*xb2**2)*xb1)*xb1-(xb2**4-7*xg1
     . **2-2*(xb2**2-9*xg1)*(xg1+1)*xb2+(xg1**2-28*xg1+1)*xb2**2)*xb2
     . **2)*st2+ans14
      ans15=(xb1-1)*(xg1-1)
      ans12=ans13*ans15
      ans16=((2*(2*(xb2+2)-3*xb1)*xb1+xb2**2-6*xb2-1)*st2-((xb1-xb2)
     . **2*st2**3-6*(xb1-xb2)*(xb1-1)*st2**2-2*(xb1-1)**2))*(xb1-xb2)
     . *(xb1-xg1)*(xb2-xg1)**2*log(xg1)*xb2
      ans11=ans12+ans16
      ans17=(log(xb2)-log(xg1))*(xb1-xg1)
      ans10=2*ans11*ans17
      ans9=-ans10
      ans23=-((2*(3*xb2**2+xg1)*(xg1+1)*xb2-(xg1**2+4*xg1+1)*xg1-(3*
     . xg1**2+4*xg1+3)*xb2**2)*xb1**4-(((3*xb2**2+xg1)*xb2-2*(xg1+1)*
     . xg1)*xb1**5-((xb2**2-xg1)*xb1**6-(xb2-xg1)**2*(xb2-1)**2*xb2**
     . 2*xg1))-(xb2**4+2*xg1**2-2*(xb2**2+2*xg1)*(xg1+1)*xb2+(xg1**2+
     . 7*xg1+1)*xb2**2)*xb1*xb2*xg1+(xb2**6+4*xb2*xg1**3+4*xb2*xg1**2
     . -xg1**3+2*(xg1**2+6*xg1+1)*(xg1+1)*xb2**3-(3*xg1**2+4*xg1+3)*
     . xb2**4-2*(4*xg1**2+7*xg1+4)*xb2**2*xg1)*xb1**2+(2*(3*xb2**4+
     . xg1**2)*(xg1+1)-3*xb2**5-6*(xg1**2+4*xg1+1)*xb2**3+2*(xg1**2+6
     . *xg1+1)*(xg1+1)*xb2**2-(xg1**2+7*xg1+1)*xb2*xg1)*xb1**3)*st2
      ans22=(2*(3*xb2**4+2*xg1**2)*(xg1+1)-3*xb2**5-2*(xg1**2+3*xg1+1
     . )*(xg1+1)*xb2**2-3*(xg1**2+4*xg1+1)*xb2**3+(4*xg1**2+13*xg1+4)
     . *xb2*xg1)*xb1**3-(2*((3*xb2**2-2*xg1)*(xg1+1)-2*xb2*xg1)*xb1**
     . 5-(2*(xb2**2-xg1)*xb1**6+(xb2-xg1)**2*(xb2-1)**2*xb2**2*xg1)+2
     . *((xg1**2+4*xg1+1+4*(xg1+1)*xb2)*xg1-(3*xg1**2+8*xg1+3)*xb2**2
     . )*xb1**4+(5*xb2**4+xg1**2-2*(5*xb2**2+4*xg1)*(xg1+1)*xb2+5*(
     . xg1**2+4*xg1+1)*xb2**2)*xb1*xb2*xg1)-(xb2**6+2*xg1**3-2*(3*xb2
     . **4-2*xg1**2)*(xg1+1)*xb2-2*(2*xg1**2+9*xg1+2)*(xg1+1)*xb2**3+
     . (4*xg1**2+7*xg1+4)*xb2**2*xg1+(9*xg1**2+20*xg1+9)*xb2**4)*xb1
     . **2+ans23
      ans24=(log(xb2)-log(xg1))*(st2-1)*(xg1-1)*st2
      ans21=ans22*ans24
      ans37=-2*xb1**2*xb2*xg1**3+2*xb1**2*xb2*xg1
      ans36=-st2*xb2**5*xg1-st2*xb2**4*xg1**3-st2*xb2**4*xg1**2+2*st2
     . *xb2**4*xg1+2*st2*xb2**3*xg1**3-st2*xb2**3*xg1**2-st2*xb2**3*
     . xg1-st2*xb2**2*xg1**3+st2*xb2**2*xg1**2+4*xb1**4*xb2**3*xg1-4*
     . xb1**4*xb2**3-4*xb1**4*xb2**2*xg1**2-4*xb1**4*xb2**2*xg1+8*xb1
     . **4*xb2**2+8*xb1**4*xb2*xg1**2-4*xb1**4*xb2*xg1-4*xb1**4*xb2-4
     . *xb1**4*xg1**2+4*xb1**4*xg1-4*xb1**3*xb2**4*xg1+4*xb1**3*xb2**
     . 4+2*xb1**3*xb2**3*xg1**2+4*xb1**3*xb2**3*xg1-6*xb1**3*xb2**3+2
     . *xb1**3*xb2**2*xg1**3-4*xb1**3*xb2**2*xg1**2+2*xb1**3*xb2**2*
     . xg1-4*xb1**3*xb2*xg1**3+2*xb1**3*xb2*xg1**2+2*xb1**3*xb2+2*xb1
     . **3*xg1**3-2*xb1**3*xg1+2*xb1**2*xb2**4*xg1**2-2*xb1**2*xb2**4
     . -2*xb1**2*xb2**3*xg1**3-4*xb1**2*xb2**3*xg1**2+2*xb1**2*xb2**3
     . *xg1+4*xb1**2*xb2**3+4*xb1**2*xb2**2*xg1**3+2*xb1**2*xb2**2*
     . xg1**2-4*xb1**2*xb2**2*xg1-2*xb1**2*xb2**2+ans37
      ans35=9*st2*xb1**3*xb2*xg1**2-15*st2*xb1**3*xb2*xg1-12*st2*xb1
     . **3*xb2-6*st2*xb1**3*xg1**3+6*st2*xb1**3*xg1-3*st2*xb1**2*xb2
     . **5*xg1+3*st2*xb1**2*xb2**5+4*st2*xb1**2*xb2**4*xg1**2+3*st2*
     . xb1**2*xb2**4*xg1-7*st2*xb1**2*xb2**4-st2*xb1**2*xb2**3*xg1**3
     . -12*st2*xb1**2*xb2**3*xg1**2+8*st2*xb1**2*xb2**3*xg1+5*st2*xb1
     . **2*xb2**3+10*st2*xb1**2*xb2**2*xg1**3+8*st2*xb1**2*xb2**2*xg1
     . **2-17*st2*xb1**2*xb2**2*xg1-st2*xb1**2*xb2**2-11*st2*xb1**2*
     . xb2*xg1**3+2*st2*xb1**2*xb2*xg1**2+9*st2*xb1**2*xb2*xg1+2*st2*
     . xb1**2*xg1**3-2*st2*xb1**2*xg1**2+st2*xb1*xb2**5*xg1**2-st2*
     . xb1*xb2**5-st2*xb1*xb2**4*xg1**3-11*st2*xb1*xb2**4*xg1**2+10*
     . st2*xb1*xb2**4*xg1+2*st2*xb1*xb2**4+11*st2*xb1*xb2**3*xg1**3+
     . 10*st2*xb1*xb2**3*xg1**2-20*st2*xb1*xb2**3*xg1-st2*xb1*xb2**3-
     . 21*st2*xb1*xb2**2*xg1**3+11*st2*xb1*xb2**2*xg1**2+10*st2*xb1*
     . xb2**2*xg1+11*st2*xb1*xb2*xg1**3-11*st2*xb1*xb2*xg1**2+st2*xb2
     . **5*xg1**2+ans36
      ans34=27*st2**2*xb1*xb2**2*xg1**3-15*st2**2*xb1*xb2**2*xg1**2-
     . 12*st2**2*xb1*xb2**2*xg1-15*st2**2*xb1*xb2*xg1**3+15*st2**2*
     . xb1*xb2*xg1**2+2*st2*xb1**6*xb2*xg1-2*st2*xb1**6*xb2-2*st2*xb1
     . **6*xg1+2*st2*xb1**6-2*st2*xb1**5*xb2**2*xg1+2*st2*xb1**5*xb2
     . **2-4*st2*xb1**5*xb2*xg1**2+2*st2*xb1**5*xb2*xg1+2*st2*xb1**5*
     . xb2+4*st2*xb1**5*xg1**2-4*st2*xb1**5-16*st2*xb1**4*xb2**3*xg1+
     . 16*st2*xb1**4*xb2**3+20*st2*xb1**4*xb2**2*xg1**2+16*st2*xb1**4
     . *xb2**2*xg1-36*st2*xb1**4*xb2**2+2*st2*xb1**4*xb2*xg1**3-30*
     . st2*xb1**4*xb2*xg1**2+10*st2*xb1**4*xb2*xg1+18*st2*xb1**4*xb2-
     . 2*st2*xb1**4*xg1**3+10*st2*xb1**4*xg1**2-10*st2*xb1**4*xg1+2*
     . st2*xb1**4+7*st2*xb1**3*xb2**4*xg1-7*st2*xb1**3*xb2**4+3*st2*
     . xb1**3*xb2**3*xg1**2-7*st2*xb1**3*xb2**3*xg1+4*st2*xb1**3*xb2
     . **3-12*st2*xb1**3*xb2**2*xg1**3-12*st2*xb1**3*xb2**2*xg1**2+9*
     . st2*xb1**3*xb2**2*xg1+15*st2*xb1**3*xb2**2+18*st2*xb1**3*xb2*
     . xg1**3+ans35
      ans33=-6*st2**2*xb1**3*xb2**3*xg1**2+6*st2**2*xb1**3*xb2**3+9*
     . st2**2*xb1**3*xb2**2*xg1**3+21*st2**2*xb1**3*xb2**2*xg1**2-15*
     . st2**2*xb1**3*xb2**2*xg1-15*st2**2*xb1**3*xb2**2-9*st2**2*xb1
     . **3*xb2*xg1**3-15*st2**2*xb1**3*xb2*xg1**2+15*st2**2*xb1**3*
     . xb2*xg1+9*st2**2*xb1**3*xb2-6*st2**2*xb1**2*xb2**4*xg1**2+6*
     . st2**2*xb1**2*xb2**4+6*st2**2*xb1**2*xb2**3*xg1**3+12*st2**2*
     . xb1**2*xb2**3*xg1**2-6*st2**2*xb1**2*xb2**3*xg1-12*st2**2*xb1
     . **2*xb2**3-18*st2**2*xb1**2*xb2**2*xg1**3-6*st2**2*xb1**2*xb2
     . **2*xg1**2+18*st2**2*xb1**2*xb2**2*xg1+6*st2**2*xb1**2*xb2**2+
     . 9*st2**2*xb1**2*xb2*xg1**3+3*st2**2*xb1**2*xb2*xg1**2-12*st2**
     . 2*xb1**2*xb2*xg1+3*st2**2*xb1**2*xg1**3-3*st2**2*xb1**2*xg1**2
     . +12*st2**2*xb1*xb2**4*xg1**2-12*st2**2*xb1*xb2**4*xg1-12*st2**
     . 2*xb1*xb2**3*xg1**3-12*st2**2*xb1*xb2**3*xg1**2+24*st2**2*xb1*
     . xb2**3*xg1+ans34
      ans32=-4*st2**3*xb1*xb2*xg1**2-st2**3*xb2**5*xg1**2+st2**3*xb2
     . **5*xg1+st2**3*xb2**4*xg1**3+st2**3*xb2**4*xg1**2-2*st2**3*xb2
     . **4*xg1-2*st2**3*xb2**3*xg1**3+st2**3*xb2**3*xg1**2+st2**3*xb2
     . **3*xg1+st2**3*xb2**2*xg1**3-st2**3*xb2**2*xg1**2-3*st2**2*xb1
     . **6*xb2*xg1+3*st2**2*xb1**6*xb2+3*st2**2*xb1**6*xg1-3*st2**2*
     . xb1**6+3*st2**2*xb1**5*xb2**2*xg1-3*st2**2*xb1**5*xb2**2+6*st2
     . **2*xb1**5*xb2*xg1**2-3*st2**2*xb1**5*xb2*xg1-3*st2**2*xb1**5*
     . xb2-6*st2**2*xb1**5*xg1**2+6*st2**2*xb1**5+12*st2**2*xb1**4*
     . xb2**3*xg1-12*st2**2*xb1**4*xb2**3-18*st2**2*xb1**4*xb2**2*xg1
     . **2-12*st2**2*xb1**4*xb2**2*xg1+30*st2**2*xb1**4*xb2**2-3*st2
     . **2*xb1**4*xb2*xg1**3+21*st2**2*xb1**4*xb2*xg1**2-3*st2**2*xb1
     . **4*xb2*xg1-15*st2**2*xb1**4*xb2+3*st2**2*xb1**4*xg1**3-3*st2
     . **2*xb1**4*xg1**2+3*st2**2*xb1**4*xg1-3*st2**2*xb1**4+ans33
      ans31=8*st2**3*xb1**3*xb2*xg1**2+5*st2**3*xb1**3*xb2+8*st2**3*
     . xb1**3*xg1**3-8*st2**3*xb1**3*xg1+3*st2**3*xb1**2*xb2**5*xg1-3
     . *st2**3*xb1**2*xb2**5+4*st2**3*xb1**2*xb2**4*xg1**2-3*st2**3*
     . xb1**2*xb2**4*xg1-st2**3*xb1**2*xb2**4-7*st2**3*xb1**2*xb2**3*
     . xg1**3-4*st2**3*xb1**2*xb2**3*xg1**2+11*st2**3*xb1**2*xb2**3+
     . 12*st2**3*xb1**2*xb2**2*xg1**3-5*st2**3*xb1**2*xb2**2*xg1-7*
     . st2**3*xb1**2*xb2**2-5*st2**3*xb1**2*xb2*xg1**2+5*st2**3*xb1**
     . 2*xb2*xg1-5*st2**3*xb1**2*xg1**3+5*st2**3*xb1**2*xg1**2-st2**3
     . *xb1*xb2**5*xg1**2+st2**3*xb1*xb2**5+st2**3*xb1*xb2**4*xg1**3-
     . st2**3*xb1*xb2**4*xg1**2+2*st2**3*xb1*xb2**4*xg1-2*st2**3*xb1*
     . xb2**4+st2**3*xb1*xb2**3*xg1**3+2*st2**3*xb1*xb2**3*xg1**2-4*
     . st2**3*xb1*xb2**3*xg1+st2**3*xb1*xb2**3-6*st2**3*xb1*xb2**2*
     . xg1**3+4*st2**3*xb1*xb2**2*xg1**2+2*st2**3*xb1*xb2**2*xg1+4*
     . st2**3*xb1*xb2*xg1**3+ans32
      ans30=log(xg1)*xb1*xb2*xg1**3+st2**3*xb1**6*xb2*xg1-st2**3*xb1
     . **6*xb2-st2**3*xb1**6*xg1+st2**3*xb1**6-st2**3*xb1**5*xb2**2*
     . xg1+st2**3*xb1**5*xb2**2-2*st2**3*xb1**5*xb2*xg1**2+st2**3*xb1
     . **5*xb2*xg1+st2**3*xb1**5*xb2+2*st2**3*xb1**5*xg1**2-2*st2**3*
     . xb1**5+8*st2**3*xb1**4*xb2**3*xg1-8*st2**3*xb1**4*xb2**3-6*st2
     . **3*xb1**4*xb2**2*xg1**2-8*st2**3*xb1**4*xb2**2*xg1+14*st2**3*
     . xb1**4*xb2**2+st2**3*xb1**4*xb2*xg1**3+17*st2**3*xb1**4*xb2*
     . xg1**2-11*st2**3*xb1**4*xb2*xg1-7*st2**3*xb1**4*xb2-st2**3*xb1
     . **4*xg1**3-11*st2**3*xb1**4*xg1**2+11*st2**3*xb1**4*xg1+st2**3
     . *xb1**4-11*st2**3*xb1**3*xb2**4*xg1+11*st2**3*xb1**3*xb2**4+5*
     . st2**3*xb1**3*xb2**3*xg1**2+11*st2**3*xb1**3*xb2**3*xg1-16*st2
     . **3*xb1**3*xb2**3+5*st2**3*xb1**3*xb2**2*xg1**3-13*st2**3*xb1
     . **3*xb2**2*xg1**2+8*st2**3*xb1**3*xb2**2*xg1-13*st2**3*xb1**3*
     . xb2*xg1**3+ans31
      ans29=-4*log(xg1)*st2*xb1*xb2**3*xg1**2+4*log(xg1)*st2*xb1*xb2
     . **2*xg1**3-log(xg1)*st2*xb1*xb2**2*xg1**2+log(xg1)*st2*xb1*xb2
     . *xg1**3+log(xg1)*xb1**4*xb2**3-log(xg1)*xb1**4*xb2**2*xg1-2*
     . log(xg1)*xb1**4*xb2**2+2*log(xg1)*xb1**4*xb2*xg1+log(xg1)*xb1
     . **4*xb2-log(xg1)*xb1**4*xg1-log(xg1)*xb1**3*xb2**4-log(xg1)*
     . xb1**3*xb2**3*xg1+2*log(xg1)*xb1**3*xb2**3+2*log(xg1)*xb1**3*
     . xb2**2*xg1**2+2*log(xg1)*xb1**3*xb2**2*xg1-log(xg1)*xb1**3*xb2
     . **2-4*log(xg1)*xb1**3*xb2*xg1**2-log(xg1)*xb1**3*xb2*xg1+2*log
     . (xg1)*xb1**3*xg1**2+2*log(xg1)*xb1**2*xb2**4*xg1-log(xg1)*xb1
     . **2*xb2**3*xg1**2-4*log(xg1)*xb1**2*xb2**3*xg1-log(xg1)*xb1**2
     . *xb2**2*xg1**3+2*log(xg1)*xb1**2*xb2**2*xg1**2+2*log(xg1)*xb1
     . **2*xb2**2*xg1+2*log(xg1)*xb1**2*xb2*xg1**3-log(xg1)*xb1**2*
     . xb2*xg1**2-log(xg1)*xb1**2*xg1**3-log(xg1)*xb1*xb2**4*xg1**2+
     . log(xg1)*xb1*xb2**3*xg1**3+2*log(xg1)*xb1*xb2**3*xg1**2-2*log(
     . xg1)*xb1*xb2**2*xg1**3-log(xg1)*xb1*xb2**2*xg1**2+ans30
      ans28=-5*log(xg1)*st2*xb1**4*xb2**3+5*log(xg1)*st2*xb1**4*xb2**
     . 2*xg1+10*log(xg1)*st2*xb1**4*xb2**2+2*log(xg1)*st2*xb1**4*xb2*
     . xg1**2+2*log(xg1)*st2*xb1**4*xb2*xg1+log(xg1)*st2*xb1**4*xb2-2
     . *log(xg1)*st2*xb1**4*xg1**3-12*log(xg1)*st2*xb1**4*xg1**2-log(
     . xg1)*st2*xb1**4*xg1+3*log(xg1)*st2*xb1**3*xb2**4+7*log(xg1)*
     . st2*xb1**3*xb2**3*xg1-4*log(xg1)*st2*xb1**3*xb2**3-10*log(xg1)
     . *st2*xb1**3*xb2**2*xg1**2-16*log(xg1)*st2*xb1**3*xb2**2*xg1-
     . log(xg1)*st2*xb1**3*xb2**2+14*log(xg1)*st2*xb1**3*xb2*xg1**2-
     . log(xg1)*st2*xb1**3*xb2*xg1+6*log(xg1)*st2*xb1**3*xg1**3+2*log
     . (xg1)*st2*xb1**3*xg1**2-6*log(xg1)*st2*xb1**2*xb2**4*xg1+log(
     . xg1)*st2*xb1**2*xb2**3*xg1**2+8*log(xg1)*st2*xb1**2*xb2**3*xg1
     . +5*log(xg1)*st2*xb1**2*xb2**2*xg1**3+2*log(xg1)*st2*xb1**2*xb2
     . **2*xg1**2+2*log(xg1)*st2*xb1**2*xb2**2*xg1-10*log(xg1)*st2*
     . xb1**2*xb2*xg1**3-log(xg1)*st2*xb1**2*xb2*xg1**2-log(xg1)*st2*
     . xb1**2*xg1**3+3*log(xg1)*st2*xb1*xb2**4*xg1**2-3*log(xg1)*st2*
     . xb1*xb2**3*xg1**3+ans29
      ans27=-12*log(xg1)*st2**2*xb1**4*xb2**2+3*log(xg1)*st2**2*xb1**
     . 4*xb2*xg1**2+3*log(xg1)*st2**2*xb1**4*xg1**3+12*log(xg1)*st2**
     . 2*xb1**4*xg1**2-3*log(xg1)*st2**2*xb1**3*xb2**4-3*log(xg1)*st2
     . **2*xb1**3*xb2**3*xg1+6*log(xg1)*st2**2*xb1**3*xb2**3+9*log(
     . xg1)*st2**2*xb1**3*xb2**2*xg1**2+18*log(xg1)*st2**2*xb1**3*xb2
     . **2*xg1-3*log(xg1)*st2**2*xb1**3*xb2*xg1**3-18*log(xg1)*st2**2
     . *xb1**3*xb2*xg1**2-6*log(xg1)*st2**2*xb1**3*xg1**3+6*log(xg1)*
     . st2**2*xb1**2*xb2**4*xg1-3*log(xg1)*st2**2*xb1**2*xb2**3*xg1**
     . 2-12*log(xg1)*st2**2*xb1**2*xb2**3*xg1-3*log(xg1)*st2**2*xb1**
     . 2*xb2**2*xg1**3+12*log(xg1)*st2**2*xb1**2*xb2*xg1**3-3*log(xg1
     . )*st2**2*xb1*xb2**4*xg1**2+3*log(xg1)*st2**2*xb1*xb2**3*xg1**3
     . +6*log(xg1)*st2**2*xb1*xb2**3*xg1**2-6*log(xg1)*st2**2*xb1*xb2
     . **2*xg1**3+2*log(xg1)*st2*xb1**6*xb2-2*log(xg1)*st2*xb1**6*xg1
     . -4*log(xg1)*st2*xb1**5*xb2*xg1-6*log(xg1)*st2*xb1**5*xb2+4*log
     . (xg1)*st2*xb1**5*xg1**2+6*log(xg1)*st2*xb1**5*xg1+ans28
      ans26=log(xg1)*st2**3*xb1**6*xb2-log(xg1)*st2**3*xb1**6*xg1-3*
     . log(xg1)*st2**3*xb1**5*xb2**2+log(xg1)*st2**3*xb1**5*xb2*xg1+2
     . *log(xg1)*st2**3*xb1**5*xg1**2+3*log(xg1)*st2**3*xb1**4*xb2**3
     . +3*log(xg1)*st2**3*xb1**4*xb2**2*xg1-5*log(xg1)*st2**3*xb1**4*
     . xb2*xg1**2-log(xg1)*st2**3*xb1**4*xg1**3-log(xg1)*st2**3*xb1**
     . 3*xb2**4-5*log(xg1)*st2**3*xb1**3*xb2**3*xg1+3*log(xg1)*st2**3
     . *xb1**3*xb2**2*xg1**2+3*log(xg1)*st2**3*xb1**3*xb2*xg1**3+2*
     . log(xg1)*st2**3*xb1**2*xb2**4*xg1+log(xg1)*st2**3*xb1**2*xb2**
     . 3*xg1**2-3*log(xg1)*st2**3*xb1**2*xb2**2*xg1**3-log(xg1)*st2**
     . 3*xb1*xb2**4*xg1**2+log(xg1)*st2**3*xb1*xb2**3*xg1**3-3*log(
     . xg1)*st2**2*xb1**6*xb2+3*log(xg1)*st2**2*xb1**6*xg1+3*log(xg1)
     . *st2**2*xb1**5*xb2**2+3*log(xg1)*st2**2*xb1**5*xb2*xg1+6*log(
     . xg1)*st2**2*xb1**5*xb2-6*log(xg1)*st2**2*xb1**5*xg1**2-6*log(
     . xg1)*st2**2*xb1**5*xg1+3*log(xg1)*st2**2*xb1**4*xb2**3-9*log(
     . xg1)*st2**2*xb1**4*xb2**2*xg1+ans27
      ans38=(xb2-xg1)
      ans25=ans26*ans38
      ans20=ans21+ans25
      ans39=(log(xb1)-log(xg1))
      ans19=2*ans20*ans39
      ans18=-ans19
      ans8=-(3*((2*(xg1+1)*xb2+3*xg1)*xb1-(3*xb1**3-xb1**2*xb2+5*xb2*
     . xg1))*st2**2*xb1-((3*xb1**3-xb1**2*xb2-2*xb1**2*xg1-2*xb1**2+
     . xb1*xg1+xb2*xg1)*(3*xb1-xb2)*st2**3+3*(xb1**2-xg1)*(xb1-xb2)*
     . xb1)-(6*(xg1+1+xb2)*xb1**3-(15*xb1**4+14*xb1*xb2*xg1-xb2**2*
     . xg1)-(xb2**2-3*xg1-4*(xg1+1)*xb2)*xb1**2)*st2)*(log(xb1)-log(
     . xg1))**2*(xb2-xg1)**2*(xb2-1)**2*(xg1-1)+ans9+ans18
      ans3=ans4+ans8
      ans2=ans3*xg1
      ans1=-ans2
      r922=ans1/(16*(xb1-xb2)*(xb1-xg1)**2*(xb1-1)**2*(xb2-xg1)**2*(
     . xb2-1)**2*(xg1-1))

      ans6=-(xb2-2+xb1-(xb1-xb2)*st2)*(xb1-xb2)**2*(xb1-xg1)*(xb2-xg1
     . )**2*log(xg1)*xb2
      ans5=((2*((xb2**2+xg1)*(xg1+1)-7*xb2**3+(xg1**2+xg1+1)*xb2+(3*
     . xb2**2-xg1-(xg1+1)*xb2)*xb1)*xb1**2+((xb2**2+xg1)*(xb2**2-xg1)
     . +3*(xg1-1)**2*xb2**2-6*(xb2**2-xg1)*(xg1+1)*xb2)*xb2)*xb1-(xb2
     . **4+xg1**2-2*(xg1+1)*xb2**3+(xg1**2+1)*xb2**2)*xb2**2+2*(2*xb2
     . **4-xg1**2+6*(xg1+1)*xb2**3-(4*xg1**2+5*xg1+4)*xb2**2)*xb1**2-
     . (3*xb1**3*xb2**2-xb1**3*xb2*xg1-xb1**3*xb2-xb1**3*xg1-8*xb1**2
     . *xb2**3+3*xb1**2*xb2**2*xg1+3*xb1**2*xb2**2+xb1**2*xb2*xg1**2-
     . 2*xb1**2*xb2*xg1+xb1**2*xb2+xb1**2*xg1**2+xb1**2*xg1+8*xb1*xb2
     . **3*xg1+8*xb1*xb2**3-6*xb1*xb2**2*xg1**2-9*xb1*xb2**2*xg1-6*
     . xb1*xb2**2+3*xb1*xb2*xg1**2+3*xb1*xb2*xg1-xb1*xg1**2-xb2**5+2*
     . xb2**4*xg1+2*xb2**4-xb2**3*xg1**2-12*xb2**3*xg1-xb2**3+8*xb2**
     . 2*xg1**2+8*xb2**2*xg1-5*xb2*xg1**2)*(xb1-xb2)*st2)*(xb1-1)*(
     . xg1-1)+ans6
      ans7=(log(xb2)-log(xg1))*(xb1-xg1)
      ans4=2*ans5*ans7
      ans13=-((xb1-xb2)*st2-2*(xb1-1))*(xb1-xb2)**2*(xb1-xg1)**2*(xb2
     . -xg1)*log(xg1)*xb1
      ans12=((xb2-xg1)*(xb2-1)*xb2**2*xg1+2*xb1**6-2*(2*(xg1+1)+xb2)*
     . xb1**5+2*(xg1**2+6*xg1+1+2*xb2**2)*xb1**4+((xb2**2+2*xg1)*(xg1
     . +1)*xb2-3*xg1**2-(xg1**2+3*xg1+1)*xb2**2)*xb1*xb2-((7*xb2**2+8
     . *xg1)*(xg1+1)-3*xb2**3-(2*xg1**2+3*xg1+2)*xb2)*xb1**3-(3*(xb2
     . **4-2*xg1**2)-(2*xb2**2-xg1)*(xg1+1)*xb2-(xg1**2+3*xg1+1)*xb2
     . **2)*xb1**2-(xb1**5-2*xb1**4*xg1-2*xb1**4+8*xb1**3*xb2**2-8*
     . xb1**3*xb2*xg1-8*xb1**3*xb2+xb1**3*xg1**2+12*xb1**3*xg1+xb1**3
     . -3*xb1**2*xb2**3-3*xb1**2*xb2**2*xg1-3*xb1**2*xb2**2+6*xb1**2*
     . xb2*xg1**2+9*xb1**2*xb2*xg1+6*xb1**2*xb2-8*xb1**2*xg1**2-8*xb1
     . **2*xg1+xb1*xb2**3*xg1+xb1*xb2**3-xb1*xb2**2*xg1**2+2*xb1*xb2
     . **2*xg1-xb1*xb2**2-3*xb1*xb2*xg1**2-3*xb1*xb2*xg1+5*xb1*xg1**2
     . +xb2**3*xg1-xb2**2*xg1**2-xb2**2*xg1+xb2*xg1**2)*(xb1-xb2)*st2
     . )*(xb2-1)*(xg1-1)+ans13
      ans14=(xb2-xg1)
      ans11=ans12*ans14
      ans17=-(2*(xb2**2-xg1)*xb1**6+(xb2-xg1)**2*(xb2-1)**2*xb2**2*
     . xg1-2*((xb2**2-2*xg1)*(xg1+1)+2*xb2**3)*xb1**5-2*((xg1**2+1-4*
     . (xg1+1)*xb2)*xb2**2+(xg1**2+4*xg1+1)*xg1)*xb1**4-(xb2**4+xg1**
     . 2-2*(xb2**2+2*xg1)*(xg1+1)*xb2+(xg1**2+8*xg1+1)*xb2**2)*xb1*
     . xb2*xg1+((xb2**4+xg1**2)*xb2-2*(xb2**4-2*xg1**2)*(xg1+1)+2*(
     . xg1**2+xg1+1)*(xg1+1)*xb2**2-3*(xg1**2+4*xg1+1)*xb2**3)*xb1**3
     . -(xb2**6+2*xg1**3-2*(xb2**2+5*xg1)*(xg1+1)*xb2**3+(xg1**2+4*
     . xg1+1)*xb2**4+(4*xg1**2+7*xg1+4)*xb2**2*xg1)*xb1**2)
      ans16=((2*(3*xb2**2+xg1)*(xg1+1)*xb2-(xg1**2+4*xg1+1)*xg1-(3*
     . xg1**2+4*xg1+3)*xb2**2)*xb1**4-(((3*xb2**2+xg1)*xb2-2*(xg1+1)*
     . xg1)*xb1**5-((xb2**2-xg1)*xb1**6-(xb2-xg1)**2*(xb2-1)**2*xb2**
     . 2*xg1))-(xb2**4+2*xg1**2-2*(xb2**2+2*xg1)*(xg1+1)*xb2+(xg1**2+
     . 7*xg1+1)*xb2**2)*xb1*xb2*xg1+(xb2**6+4*xb2*xg1**3+4*xb2*xg1**2
     . -xg1**3+2*(xg1**2+6*xg1+1)*(xg1+1)*xb2**3-(3*xg1**2+4*xg1+3)*
     . xb2**4-2*(4*xg1**2+7*xg1+4)*xb2**2*xg1)*xb1**2+(2*(3*xb2**4+
     . xg1**2)*(xg1+1)-3*xb2**5-6*(xg1**2+4*xg1+1)*xb2**3+2*(xg1**2+6
     . *xg1+1)*(xg1+1)*xb2**2-(xg1**2+7*xg1+1)*xb2*xg1)*xb1**3)*st2+
     . ans17
      ans18=(log(xb2)-log(xg1))*(xg1-1)
      ans15=ans16*ans18
      ans10=ans11+ans15
      ans19=(log(xb1)-log(xg1))
      ans9=2*ans10*ans19
      ans8=(4*((xg1+1-xb2)*xb2**2-2*xb1**3+(2*(xg1+1)+xb2)*xb1**2-((
     . xg1+1)*xb2+2*xg1)*xb1+(xb1**2-xb1*xg1-xb1+xb2**2-xb2*xg1-xb2+2
     . *xg1)*(xb1-xb2)*st2)*(xb1-1)*(xb2-1)*(xg1-1)-(xb2-2+2*xb1-(xb1
     . -xb2)*st2)*(log(xg1)+4)*(xb1-xb2)**2*(xb1-xg1)*(xb2-xg1)*log(
     . xg1))*(xb1-xb2)*(xb1-xg1)*(xb2-xg1)-((6*xb1**4-xb1*xb2*xg1+xb2
     . **2*xg1-(xb2**2-6*xg1)*xb1**2-(6*(xg1+1)-xb2)*xb1**3-(3*xb1**3
     . -xb1**2*xb2-2*xb1**2*xg1-2*xb1**2+xb1*xg1+xb2*xg1)*(3*xb1-xb2)
     . *st2)*(log(xb1)-log(xg1))**2*(xb2-xg1)**2*(xb2-1)**2-((7*xb2**
     . 2-3*xg1-2*(xg1+1)*xb2)*xb1*xb2-(2*xb1**2+3*xb2**2)*(xb2**2-xg1
     . )+(xb1*xb2**2-xb1*xg1-3*xb2**3+2*xb2**2*xg1+2*xb2**2-xb2*xg1)*
     . (xb1-3*xb2)*st2)*(log(xb2)-log(xg1))**2*(xb1-xg1)**2*(xb1-1)**
     . 2)*(xg1-1)+ans9
      ans3=ans4+ans8
      ans20=(st2-1)*st2*xg1
      ans2=3*ans3*ans20
      ans1=-ans2
      r92p2=ans1/(16*(xb1-xb2)*(xb1-xg1)**2*(xb1-1)**2*(xb2-xg1)**2*(
     . xb2-1)**2*(xg1-1))

      r922 = r922 + r92p2

      r92=r912+r922

c--rct
      ans5=-2*((((((2*(xb2-2*xg1)+xb1)*xb1**2-(xb2-xg1)*xb2*xg1-(xb2
     . **2+xb2*xg1-3*xg1**2)*xb1)*s2t**2+2*(4*xb1**2+3*xg1*xgl-2*(xg1
     . -xgl)*xb1)*(xb2-xg1)-2*(2*xb1-xg1)*(xb2-xg1)*c2t**2*xb1)*(xb1-
     . xb2)*xb2-2*(log(-(xb2-xgl))-log(xgl))*(xb1-xg1)*(xb2-xg1)*(xb2
     . -xgl)**2*xb1)*xb1+2*((log(-(xb1-xgl))-log(xgl))*(xb1**2-xb2*
     . xg1)*(xb1-xgl)**2-(log(xg1)-log(xgl))*(xb1**2-2*xg1*xgl)*(xb1-
     . xb2)*xb1)*(xb2-xg1)*xb2)*(xb2-xg1)+((((2*xb1**2-xb1*xb2+2*xb2
     . **2)*s2t**2+9*xb1*xb2)*(xb1+xb2)-((xb1**2+xb2**2)*s2t**2+6*xb1
     . *xb2)*xg1)*xg1**2-((xb2-2*xg1+xb1)*(xb1-xg1)*(xb2-xg1)*c2t**2-
     . (s2t**2+3)*(xb1+xb2)*xb1*xb2)*xb1*xb2-((xb1**4+xb2**4)*s2t**2+
     . 3*(xb1**2+xb2**2)*xb1*xb2+4*(s2t**2+3)*xb1**2*xb2**2)*xg1)*(
     . log(xb2)-log(xg1))*xb1*xb2)*(log(xb1)-log(xg1))
      ans4=-2*(((((xb2+xg1)*xb1**2-(xb2-xg1)*(xb2-3*xg1)*xb2-(2*xb2**
     . 2-xb2*xg1+xg1**2)*xb1)*s2t**2-2*(4*xb2**2+3*xg1*xgl-2*(xg1-xgl
     . )*xb2)*(xb1-xg1)+2*(xb1-xg1)*(2*xb2-xg1)*c2t**2*xb2)*(xb1-xb2)
     . *xb2-2*(log(-(xb2-xgl))-log(xgl))*(xb1*xg1-xb2**2)*(xb1-xg1)*(
     . xb2-xgl)**2)*xb1-2*((log(-(xb1-xgl))-log(xgl))*(xb1-xgl)**2*(
     . xb2-xg1)*xb2-(log(xg1)-log(xgl))*(xb1-xb2)*(xb2**2-2*xg1*xgl)*
     . xb1)*(xb1-xg1)*xb2)*(log(xb2)-log(xg1))*(xb1-xg1)+ans5
      ans3=(4*((((xb2-xg1+xb1)*s2t**2-(2*xg1+5*xgl)+c2t**2*xg1)*(xb1-
     . xb2)*xb2-(log(-(xb2-xgl))-log(xgl))*(xb1-xg1)*(xb2-xgl)**2)*
     . xb1+((log(-(xb1-xgl))-log(xgl))*(xb1-xgl)**2*(xb2-xg1)+(log(
     . xg1)-log(xgl))*(xb1-xb2)*(xg1-2*xgl)*xb1)*xb2)*(xb1-xb2)*(xb2-
     . xg1)+(((xb1*xg1-xb2**2)*xb1+3*(xb2-xg1)*xb2**2)*s2t**2+(7*xb2
     . **2+4*xg1*xgl)*xb2-(xb2**2+6*xb2*xg1+4*xg1*xgl)*xb1+((xb2+2*
     . xg1)*xb1-3*xb2**2)*c2t**2*xb2)*(log(xb2)-log(xg1))**2*(xb1-xg1
     . )*xb1*xb2)*(xb1-xg1)+(7*xb1**3-xb1**2*xb2-4*xb2*xg1*xgl-2*(3*
     . xb2-2*xgl)*xb1*xg1+(3*xb1**3+xb2**2*xg1-(xb2+3*xg1)*xb1**2)*
     . s2t**2-(3*xb1**2-xb1*xb2-2*xb2*xg1)*c2t**2*xb1)*(log(xb1)-log(
     . xg1))**2*(xb2-xg1)**2*xb1*xb2+ans4
      ans2=ans3*xg1
      ans1=-ans2
      rct12=ans1/(24*(xb1-xb2)**2*(xb1-xg1)**2*(xb2-xg1)**2*xb1*xb2)

      ans10=(((xb2-6)*xb2-(16*xgl-1)+2*(xb2+4*xgl)*xb1)*xb1+2*(2*(xb2
     . **2+3)*xgl-(4*xgl-1)*xb2)-(xb1*xb2+4*xb1*xgl+4*xb2*xgl-8*xgl-1
     . )*(xb1-xb2)*st2-(2*(xb1-1)**2*xb1+(xb2-1)**2*xb2-(xb1**2+xb1*
     . xb2-2*xb1+xb2**2-2*xb2+1)*(xb1-xb2)*st2)*s2t**2-(2*(xb1**2+1)*
     . xb2+(xb2**2-6*xb2+1)*xb1-(xb1*xb2-1)*(xb1-xb2)*st2)*c2t**2)*
     . log(xg1)*xb1*xb2
      ans9=4*((2*((xb2-6)*xb2-(10*xgl-1)+(2*xb2+5*xgl)*xb1)*xb1+5*(
     . xb2**2+3)*xgl-2*(5*xgl-2)*xb2-(2*xb1*xb2+5*xb1*xgl+5*xb2*xgl-
     . 10*xgl-2)*(xb1-xb2)*st2-(2*(xb1-1)**2*xb1+(xb2-1)**2*xb2-(xb1
     . **2+xb1*xb2-2*xb1+xb2**2-2*xb2+1)*(xb1-xb2)*st2)*s2t**2-(2*(
     . xb1**2+1)*xb2+(xb2**2-6*xb2+1)*xb1-(xb1*xb2-1)*(xb1-xb2)*st2)*
     . c2t**2)*xb1*xb2+(2*((xb2**3+3*xb2-xgl)*xgl-(2*xgl+1)*xb2**2)*
     . xb1-(2*(xb2-xgl)**2*xb1**3+(xb2-1)**2*xb2*xgl**2)-(xb2**3-6*
     . xb2**2-4*xgl**2+(8*xgl+1)*xb2)*xb1**2+(xb1**2*xb2**2-2*xb1**2*
     . xb2*xgl+xb1**2*xgl**2-2*xb1*xb2**2*xgl+xb1*xb2*xgl**2+4*xb1*
     . xb2*xgl-xb1*xb2-2*xb1*xgl**2+xb2**2*xgl**2-2*xb2*xgl**2+xgl**2
     . )*(xb1-xb2)*st2)*log(xgl)-(st2-2)*(xb1-1)**2*(xb2-xgl)**2*log(
     . -(xb2-xgl))*xb1+(st2+1)*(xb1-xgl)**2*(xb2-1)**2*log(-(xb1-xgl)
     . )*xb2)+ans10
      ans11=(xb1-xg1)*(xb2-xg1)*log(xg1)
      ans8=ans9*ans11
      ans12=-4*(((((5*xgl-4)*xg1+5*xgl)*xb2-5*(xb2**2+3*xg1)*xgl-2*(2
     . *xb2+5*xgl)*xb1**2+2*((3*(xg1+1)-xb2)*xb2+(5*xgl-1)*xg1+5*xgl)
     . *xb1+(2*xb1*xb2+5*xb1*xgl+5*xb2*xgl-5*xg1*xgl-2*xg1-5*xgl)*(
     . xb1-xb2)*st2+(2*(xb1-xg1)*(xb1-1)*xb1+(xb2-xg1)*(xb2-1)*xb2-(
     . xb1**2+xb1*xb2-xb1*xg1-xb1+xb2**2-xb2*xg1-xb2+xg1)*(xb1-xb2)*
     . st2)*s2t**2+((xb2**2+xg1-3*(xg1+1)*xb2)*xb1+2*(xb1**2+xg1)*xb2
     . -(xb1*xb2-xg1)*(xb1-xb2)*st2)*c2t**2)*xb2+(log(-(xb2-xgl))-log
     . (xgl))*(st2-2)*(xb1-xg1)*(xb1-1)*(xb2-xgl)**2)*xb1-(log(-(xb1-
     . xgl))-log(xgl))*(st2+1)*(xb1-xgl)**2*(xb2-xg1)*(xb2-1)*xb2)*(
     . xb1-1)*(xb2-1)*(xg1-1)
      ans7=ans8+ans12
      ans13=(xb2-xg1)
      ans6=ans7*ans13
      ans14=-(4*((2*(((xgl+1)*xg1+xgl)*xb2-(xb2**2+3*xg1)*xgl+(xb2-2*
     . xgl)*xb1**2)-((3*(xg1+1)-xb2)*xb2-((4*xgl+1)*xg1+4*xgl))*xb1-(
     . xb1*xb2-2*xb1*xgl-2*xb2*xgl+2*xg1*xgl-xg1+2*xgl)*(xb1-xb2)*st2
     . )*(xb1-1)*(xb2-1)*(xg1-1)+(((xb2-6)*xb2+8*xgl+1+2*(xb2-2*xgl)*
     . xb1)*xb1-2*((xb2**2+3)*xgl-(2*xgl+1)*xb2)-(xb1*xb2-2*xb1*xgl-2
     . *xb2*xgl+4*xgl-1)*(xb1-xb2)*st2)*(xb1-xg1)*(xb2-xg1)*log(xg1))
     . *(log(xg1)-log(xgl))*(xb2-xg1)+(7*xb2+4*xgl-s2t**2*xb1-3*c2t**
     . 2*xb2)*(log(xb2)-log(xg1))**2*(st2-2)*(xb1-xg1)*(xb1-1)**2*(
     . xb2**2-xg1)*(xg1-1))*xb1*xb2
      ans5=ans6+ans14
      ans15=(xb1-xg1)
      ans4=ans5*ans15
      ans43=-12*xb1*xb2*xg1**3*xgl+6*xb1*xb2*xg1**2*xgl+6*xb1*xb2*xg1
     . *xgl+6*xb1*xg1**3*xgl-6*xb1*xg1**2*xgl
      ans42=8*xb1**4*xg1-4*xb1**3*xb2**3*xg1**2+14*xb1**3*xb2**3*xg1*
     . xgl-14*xb1**3*xb2**3*xgl+4*xb1**3*xb2**3+4*xb1**3*xb2**2*xg1**
     . 3-14*xb1**3*xb2**2*xg1**2*xgl+8*xb1**3*xb2**2*xg1**2-14*xb1**3
     . *xb2**2*xg1*xgl-4*xb1**3*xb2**2*xg1+28*xb1**3*xb2**2*xgl-8*xb1
     . **3*xb2**2-8*xb1**3*xb2*xg1**3+28*xb1**3*xb2*xg1**2*xgl-4*xb1
     . **3*xb2*xg1**2-14*xb1**3*xb2*xg1*xgl+8*xb1**3*xb2*xg1-14*xb1**
     . 3*xb2*xgl+4*xb1**3*xb2+4*xb1**3*xg1**3-14*xb1**3*xg1**2*xgl+14
     . *xb1**3*xg1*xgl-4*xb1**3*xg1-4*xb1**2*xb2**3*xg1**2*xgl+4*xb1
     . **2*xb2**3*xgl+4*xb1**2*xb2**2*xg1**3*xgl+8*xb1**2*xb2**2*xg1
     . **2*xgl-4*xb1**2*xb2**2*xg1*xgl-8*xb1**2*xb2**2*xgl-8*xb1**2*
     . xb2*xg1**3*xgl-4*xb1**2*xb2*xg1**2*xgl+8*xb1**2*xb2*xg1*xgl+4*
     . xb1**2*xb2*xgl+4*xb1**2*xg1**3*xgl-4*xb1**2*xg1*xgl-6*xb1*xb2
     . **3*xg1**2*xgl+6*xb1*xb2**3*xg1*xgl+6*xb1*xb2**2*xg1**3*xgl+6*
     . xb1*xb2**2*xg1**2*xgl-12*xb1*xb2**2*xg1*xgl+ans43
      ans41=-14*st2*xb1**3*xb2*xg1*xgl+8*st2*xb1**3*xb2*xg1-14*st2*
     . xb1**3*xb2*xgl+4*st2*xb1**3*xb2+4*st2*xb1**3*xg1**3-14*st2*xb1
     . **3*xg1**2*xgl+14*st2*xb1**3*xg1*xgl-4*st2*xb1**3*xg1-4*st2*
     . xb1**2*xb2**3*xg1**2*xgl+4*st2*xb1**2*xb2**3*xgl+4*st2*xb1**2*
     . xb2**2*xg1**3*xgl+8*st2*xb1**2*xb2**2*xg1**2*xgl-4*st2*xb1**2*
     . xb2**2*xg1*xgl-8*st2*xb1**2*xb2**2*xgl-8*st2*xb1**2*xb2*xg1**3
     . *xgl-4*st2*xb1**2*xb2*xg1**2*xgl+8*st2*xb1**2*xb2*xg1*xgl+4*
     . st2*xb1**2*xb2*xgl+4*st2*xb1**2*xg1**3*xgl-4*st2*xb1**2*xg1*
     . xgl-6*st2*xb1*xb2**3*xg1**2*xgl+6*st2*xb1*xb2**3*xg1*xgl+6*st2
     . *xb1*xb2**2*xg1**3*xgl+6*st2*xb1*xb2**2*xg1**2*xgl-12*st2*xb1*
     . xb2**2*xg1*xgl-12*st2*xb1*xb2*xg1**3*xgl+6*st2*xb1*xb2*xg1**2*
     . xgl+6*st2*xb1*xb2*xg1*xgl+6*st2*xb1*xg1**3*xgl-6*st2*xb1*xg1**
     . 2*xgl+8*xb1**4*xb2**3*xg1-8*xb1**4*xb2**3-8*xb1**4*xb2**2*xg1
     . **2-8*xb1**4*xb2**2*xg1+16*xb1**4*xb2**2+16*xb1**4*xb2*xg1**2-
     . 8*xb1**4*xb2*xg1-8*xb1**4*xb2-8*xb1**4*xg1**2+ans42
      ans40=-2*s2t**2*xb1**2*xg1**2+s2t**2*xb1*xb2**4*xg1**2-s2t**2*
     . xb1*xb2**4*xg1-s2t**2*xb1*xb2**3*xg1**3-s2t**2*xb1*xb2**3*xg1
     . **2+2*s2t**2*xb1*xb2**3*xg1+2*s2t**2*xb1*xb2**2*xg1**3-s2t**2*
     . xb1*xb2**2*xg1**2-s2t**2*xb1*xb2**2*xg1-s2t**2*xb1*xb2*xg1**3+
     . s2t**2*xb1*xb2*xg1**2+8*st2*xb1**4*xb2**3*xg1-8*st2*xb1**4*xb2
     . **3-8*st2*xb1**4*xb2**2*xg1**2-8*st2*xb1**4*xb2**2*xg1+16*st2*
     . xb1**4*xb2**2+16*st2*xb1**4*xb2*xg1**2-8*st2*xb1**4*xb2*xg1-8*
     . st2*xb1**4*xb2-8*st2*xb1**4*xg1**2+8*st2*xb1**4*xg1-4*st2*xb1
     . **3*xb2**3*xg1**2+14*st2*xb1**3*xb2**3*xg1*xgl-14*st2*xb1**3*
     . xb2**3*xgl+4*st2*xb1**3*xb2**3+4*st2*xb1**3*xb2**2*xg1**3-14*
     . st2*xb1**3*xb2**2*xg1**2*xgl+8*st2*xb1**3*xb2**2*xg1**2-14*st2
     . *xb1**3*xb2**2*xg1*xgl-4*st2*xb1**3*xb2**2*xg1+28*st2*xb1**3*
     . xb2**2*xgl-8*st2*xb1**3*xb2**2-8*st2*xb1**3*xb2*xg1**3+28*st2*
     . xb1**3*xb2*xg1**2*xgl-4*st2*xb1**3*xb2*xg1**2+ans41
      ans39=2*s2t**2*xb1**4*xb2+2*s2t**2*xb1**4*xg1**3+6*s2t**2*xb1**
     . 4*xg1**2-6*s2t**2*xb1**4*xg1-2*s2t**2*xb1**4-3*s2t**2*xb1**3*
     . xb2**4*xg1+3*s2t**2*xb1**3*xb2**4+3*s2t**2*xb1**3*xb2**3*xg1**
     . 2+3*s2t**2*xb1**3*xb2**3*xg1-6*s2t**2*xb1**3*xb2**3-6*s2t**2*
     . xb1**3*xb2**2*xg1**2+3*s2t**2*xb1**3*xb2**2*xg1+3*s2t**2*xb1**
     . 3*xb2**2+4*s2t**2*xb1**3*xb2*xg1**3+3*s2t**2*xb1**3*xb2*xg1**2
     . -7*s2t**2*xb1**3*xb2*xg1-4*s2t**2*xb1**3*xg1**3+4*s2t**2*xb1**
     . 3*xg1+s2t**2*xb1**2*xb2**4*xg1**2-s2t**2*xb1**2*xb2**4-s2t**2*
     . xb1**2*xb2**3*xg1**3-2*s2t**2*xb1**2*xb2**3*xg1**2+s2t**2*xb1
     . **2*xb2**3*xg1+2*s2t**2*xb1**2*xb2**3+2*s2t**2*xb1**2*xb2**2*
     . xg1**3+s2t**2*xb1**2*xb2**2*xg1**2-2*s2t**2*xb1**2*xb2**2*xg1-
     . s2t**2*xb1**2*xb2**2-3*s2t**2*xb1**2*xb2*xg1**3+2*s2t**2*xb1**
     . 2*xb2*xg1**2+s2t**2*xb1**2*xb2*xg1+2*s2t**2*xb1**2*xg1**3+
     . ans40
      ans38=-2*s2t**2*st2*xb1**2*xb2**3*xg1**2+s2t**2*st2*xb1**2*xb2
     . **3*xg1+2*s2t**2*st2*xb1**2*xb2**3+2*s2t**2*st2*xb1**2*xb2**2*
     . xg1**3+s2t**2*st2*xb1**2*xb2**2*xg1**2-2*s2t**2*st2*xb1**2*xb2
     . **2*xg1-s2t**2*st2*xb1**2*xb2**2-s2t**2*st2*xb1**2*xb2*xg1**2+
     . s2t**2*st2*xb1**2*xb2*xg1-s2t**2*st2*xb1**2*xg1**3+s2t**2*st2*
     . xb1**2*xg1**2+s2t**2*st2*xb1*xb2**4*xg1**2-s2t**2*st2*xb1*xb2
     . **4*xg1-s2t**2*st2*xb1*xb2**3*xg1**3-s2t**2*st2*xb1*xb2**3*xg1
     . **2+2*s2t**2*st2*xb1*xb2**3*xg1+2*s2t**2*st2*xb1*xb2**2*xg1**3
     . -s2t**2*st2*xb1*xb2**2*xg1**2-s2t**2*st2*xb1*xb2**2*xg1-s2t**2
     . *st2*xb1*xb2*xg1**3+s2t**2*st2*xb1*xb2*xg1**2-2*s2t**2*xb1**6*
     . xb2*xg1+2*s2t**2*xb1**6*xb2+2*s2t**2*xb1**6*xg1-2*s2t**2*xb1**
     . 6+4*s2t**2*xb1**5*xb2*xg1**2-4*s2t**2*xb1**5*xb2-4*s2t**2*xb1
     . **5*xg1**2+4*s2t**2*xb1**5-2*s2t**2*xb1**4*xb2*xg1**3-6*s2t**2
     . *xb1**4*xb2*xg1**2+6*s2t**2*xb1**4*xb2*xg1+ans39
      ans37=-s2t**2*st2*xb1**6*xb2-s2t**2*st2*xb1**6*xg1+s2t**2*st2*
     . xb1**6-2*s2t**2*st2*xb1**5*xb2*xg1**2+2*s2t**2*st2*xb1**5*xb2+
     . 2*s2t**2*st2*xb1**5*xg1**2-2*s2t**2*st2*xb1**5+s2t**2*st2*xb1
     . **4*xb2*xg1**3+3*s2t**2*st2*xb1**4*xb2*xg1**2-3*s2t**2*st2*xb1
     . **4*xb2*xg1-s2t**2*st2*xb1**4*xb2-s2t**2*st2*xb1**4*xg1**3-3*
     . s2t**2*st2*xb1**4*xg1**2+3*s2t**2*st2*xb1**4*xg1+s2t**2*st2*
     . xb1**4-3*s2t**2*st2*xb1**3*xb2**4*xg1+3*s2t**2*st2*xb1**3*xb2
     . **4+3*s2t**2*st2*xb1**3*xb2**3*xg1**2+3*s2t**2*st2*xb1**3*xb2
     . **3*xg1-6*s2t**2*st2*xb1**3*xb2**3-6*s2t**2*st2*xb1**3*xb2**2*
     . xg1**2+3*s2t**2*st2*xb1**3*xb2**2*xg1+3*s2t**2*st2*xb1**3*xb2
     . **2-2*s2t**2*st2*xb1**3*xb2*xg1**3+3*s2t**2*st2*xb1**3*xb2*xg1
     . **2-s2t**2*st2*xb1**3*xb2*xg1+2*s2t**2*st2*xb1**3*xg1**3-2*s2t
     . **2*st2*xb1**3*xg1+s2t**2*st2*xb1**2*xb2**4*xg1**2-s2t**2*st2*
     . xb1**2*xb2**4-s2t**2*st2*xb1**2*xb2**3*xg1**3+ans38
      ans36=-4*c2t**2*st2*xb1**3*xb2**2*xg1**2+2*c2t**2*st2*xb1**3*
     . xb2**2*xg1+4*c2t**2*st2*xb1**3*xb2**2+4*c2t**2*st2*xb1**3*xb2*
     . xg1**3+2*c2t**2*st2*xb1**3*xb2*xg1**2-4*c2t**2*st2*xb1**3*xb2*
     . xg1-2*c2t**2*st2*xb1**3*xb2-2*c2t**2*st2*xb1**3*xg1**3+2*c2t**
     . 2*st2*xb1**3*xg1-4*c2t**2*xb1**4*xb2**3*xg1+4*c2t**2*xb1**4*
     . xb2**3+4*c2t**2*xb1**4*xb2**2*xg1**2+4*c2t**2*xb1**4*xb2**2*
     . xg1-8*c2t**2*xb1**4*xb2**2-8*c2t**2*xb1**4*xb2*xg1**2+4*c2t**2
     . *xb1**4*xb2*xg1+4*c2t**2*xb1**4*xb2+4*c2t**2*xb1**4*xg1**2-4*
     . c2t**2*xb1**4*xg1+2*c2t**2*xb1**3*xb2**3*xg1**2-2*c2t**2*xb1**
     . 3*xb2**3-2*c2t**2*xb1**3*xb2**2*xg1**3-4*c2t**2*xb1**3*xb2**2*
     . xg1**2+2*c2t**2*xb1**3*xb2**2*xg1+4*c2t**2*xb1**3*xb2**2+4*c2t
     . **2*xb1**3*xb2*xg1**3+2*c2t**2*xb1**3*xb2*xg1**2-4*c2t**2*xb1
     . **3*xb2*xg1-2*c2t**2*xb1**3*xb2-2*c2t**2*xb1**3*xg1**3+2*c2t**
     . 2*xb1**3*xg1+s2t**2*st2*xb1**6*xb2*xg1+ans37
      ans35=-4*log(xgl)*xb1**2*xb2**2*xgl**2-4*log(xgl)*xb1**2*xb2*
     . xg1**2*xgl**2+2*log(xgl)*xb1**2*xb2*xg1*xgl**2+2*log(xgl)*xb1
     . **2*xb2*xgl**2+2*log(xgl)*xb1**2*xg1**2*xgl**2-2*log(xgl)*xb1
     . **2*xg1*xgl**2+2*log(xgl)*xb2**3*xg1**2*xgl**2-2*log(xgl)*xb2
     . **3*xg1*xgl**2-2*log(xgl)*xb2**2*xg1**3*xgl**2-2*log(xgl)*xb2
     . **2*xg1**2*xgl**2+4*log(xgl)*xb2**2*xg1*xgl**2+4*log(xgl)*xb2*
     . xg1**3*xgl**2-2*log(xgl)*xb2*xg1**2*xgl**2-2*log(xgl)*xb2*xg1*
     . xgl**2-2*log(xgl)*xg1**3*xgl**2+2*log(xgl)*xg1**2*xgl**2-4*c2t
     . **2*st2*xb1**4*xb2**3*xg1+4*c2t**2*st2*xb1**4*xb2**3+4*c2t**2*
     . st2*xb1**4*xb2**2*xg1**2+4*c2t**2*st2*xb1**4*xb2**2*xg1-8*c2t
     . **2*st2*xb1**4*xb2**2-8*c2t**2*st2*xb1**4*xb2*xg1**2+4*c2t**2*
     . st2*xb1**4*xb2*xg1+4*c2t**2*st2*xb1**4*xb2+4*c2t**2*st2*xb1**4
     . *xg1**2-4*c2t**2*st2*xb1**4*xg1+2*c2t**2*st2*xb1**3*xb2**3*xg1
     . **2-2*c2t**2*st2*xb1**3*xb2**3-2*c2t**2*st2*xb1**3*xb2**2*xg1
     . **3+ans36
      ans34=4*log(xg1)*xb1*xb2*xg1**2*xgl+4*log(xg1)*xb1*xb2*xg1*xgl+
     . 4*log(xg1)*xb1*xg1**3*xgl-4*log(xg1)*xb1*xg1**2*xgl-2*log(xgl)
     . *st2*xb1**2*xb2**3*xg1*xgl**2+2*log(xgl)*st2*xb1**2*xb2**3*xgl
     . **2+2*log(xgl)*st2*xb1**2*xb2**2*xg1**2*xgl**2+2*log(xgl)*st2*
     . xb1**2*xb2**2*xg1*xgl**2-4*log(xgl)*st2*xb1**2*xb2**2*xgl**2-4
     . *log(xgl)*st2*xb1**2*xb2*xg1**2*xgl**2+2*log(xgl)*st2*xb1**2*
     . xb2*xg1*xgl**2+2*log(xgl)*st2*xb1**2*xb2*xgl**2+2*log(xgl)*st2
     . *xb1**2*xg1**2*xgl**2-2*log(xgl)*st2*xb1**2*xg1*xgl**2+2*log(
     . xgl)*st2*xb2**3*xg1**2*xgl**2-2*log(xgl)*st2*xb2**3*xg1*xgl**2
     . -2*log(xgl)*st2*xb2**2*xg1**3*xgl**2-2*log(xgl)*st2*xb2**2*xg1
     . **2*xgl**2+4*log(xgl)*st2*xb2**2*xg1*xgl**2+4*log(xgl)*st2*xb2
     . *xg1**3*xgl**2-2*log(xgl)*st2*xb2*xg1**2*xgl**2-2*log(xgl)*st2
     . *xb2*xg1*xgl**2-2*log(xgl)*st2*xg1**3*xgl**2+2*log(xgl)*st2*
     . xg1**2*xgl**2-2*log(xgl)*xb1**2*xb2**3*xg1*xgl**2+2*log(xgl)*
     . xb1**2*xb2**3*xgl**2+2*log(xgl)*xb1**2*xb2**2*xg1**2*xgl**2+2*
     . log(xgl)*xb1**2*xb2**2*xg1*xgl**2+ans35
      ans33=-6*log(xg1)*xb1**3*xb2**3*xg1-4*log(xg1)*xb1**3*xb2**3*
     . xgl-4*log(xg1)*xb1**3*xb2**2*xg1**2*xgl+6*log(xg1)*xb1**3*xb2
     . **2*xg1**2-4*log(xg1)*xb1**3*xb2**2*xg1*xgl+12*log(xg1)*xb1**3
     . *xb2**2*xg1+8*log(xg1)*xb1**3*xb2**2*xgl+8*log(xg1)*xb1**3*xb2
     . *xg1**2*xgl-12*log(xg1)*xb1**3*xb2*xg1**2-4*log(xg1)*xb1**3*
     . xb2*xg1*xgl-6*log(xg1)*xb1**3*xb2*xg1-4*log(xg1)*xb1**3*xb2*
     . xgl-4*log(xg1)*xb1**3*xg1**2*xgl+6*log(xg1)*xb1**3*xg1**2+4*
     . log(xg1)*xb1**3*xg1*xgl+5*log(xg1)*xb1**2*xb2**3*xg1**2-2*log(
     . xg1)*xb1**2*xb2**3*xg1-5*log(xg1)*xb1**2*xb2**2*xg1**3-8*log(
     . xg1)*xb1**2*xb2**2*xg1**2+4*log(xg1)*xb1**2*xb2**2*xg1+10*log(
     . xg1)*xb1**2*xb2*xg1**3+log(xg1)*xb1**2*xb2*xg1**2-2*log(xg1)*
     . xb1**2*xb2*xg1-5*log(xg1)*xb1**2*xg1**3+2*log(xg1)*xb1**2*xg1
     . **2-4*log(xg1)*xb1*xb2**3*xg1**2*xgl+4*log(xg1)*xb1*xb2**3*xg1
     . *xgl+4*log(xg1)*xb1*xb2**2*xg1**3*xgl+4*log(xg1)*xb1*xb2**2*
     . xg1**2*xgl-8*log(xg1)*xb1*xb2**2*xg1*xgl-8*log(xg1)*xb1*xb2*
     . xg1**3*xgl+ans34
      ans32=5*log(xg1)*st2*xb1**2*xb2**3*xg1**2-2*log(xg1)*st2*xb1**2
     . *xb2**3*xg1-5*log(xg1)*st2*xb1**2*xb2**2*xg1**3-8*log(xg1)*st2
     . *xb1**2*xb2**2*xg1**2+4*log(xg1)*st2*xb1**2*xb2**2*xg1+10*log(
     . xg1)*st2*xb1**2*xb2*xg1**3+log(xg1)*st2*xb1**2*xb2*xg1**2-2*
     . log(xg1)*st2*xb1**2*xb2*xg1-5*log(xg1)*st2*xb1**2*xg1**3+2*log
     . (xg1)*st2*xb1**2*xg1**2-4*log(xg1)*st2*xb1*xb2**3*xg1**2*xgl+4
     . *log(xg1)*st2*xb1*xb2**3*xg1*xgl+4*log(xg1)*st2*xb1*xb2**2*xg1
     . **3*xgl+4*log(xg1)*st2*xb1*xb2**2*xg1**2*xgl-8*log(xg1)*st2*
     . xb1*xb2**2*xg1*xgl-8*log(xg1)*st2*xb1*xb2*xg1**3*xgl+4*log(xg1
     . )*st2*xb1*xb2*xg1**2*xgl+4*log(xg1)*st2*xb1*xb2*xg1*xgl+4*log(
     . xg1)*st2*xb1*xg1**3*xgl-4*log(xg1)*st2*xb1*xg1**2*xgl-2*log(
     . xg1)*xb1**4*xb2**3*xg1+5*log(xg1)*xb1**4*xb2**3+2*log(xg1)*xb1
     . **4*xb2**2*xg1**2-log(xg1)*xb1**4*xb2**2*xg1-10*log(xg1)*xb1**
     . 4*xb2**2-4*log(xg1)*xb1**4*xb2*xg1**2+8*log(xg1)*xb1**4*xb2*
     . xg1+5*log(xg1)*xb1**4*xb2+2*log(xg1)*xb1**4*xg1**2-5*log(xg1)*
     . xb1**4*xg1+4*log(xg1)*xb1**3*xb2**3*xg1*xgl+ans33
      ans31=-4*log(xg1)*s2t**2*xb1**3*xg1**2-2*log(xg1)*s2t**2*xb1**2
     . *xb2*xg1**2+2*log(xg1)*s2t**2*xb1**2*xg1**3-2*log(xg1)*st2*xb1
     . **4*xb2**3*xg1+5*log(xg1)*st2*xb1**4*xb2**3+2*log(xg1)*st2*xb1
     . **4*xb2**2*xg1**2-log(xg1)*st2*xb1**4*xb2**2*xg1-10*log(xg1)*
     . st2*xb1**4*xb2**2-4*log(xg1)*st2*xb1**4*xb2*xg1**2+8*log(xg1)*
     . st2*xb1**4*xb2*xg1+5*log(xg1)*st2*xb1**4*xb2+2*log(xg1)*st2*
     . xb1**4*xg1**2-5*log(xg1)*st2*xb1**4*xg1+4*log(xg1)*st2*xb1**3*
     . xb2**3*xg1*xgl-6*log(xg1)*st2*xb1**3*xb2**3*xg1-4*log(xg1)*st2
     . *xb1**3*xb2**3*xgl-4*log(xg1)*st2*xb1**3*xb2**2*xg1**2*xgl+6*
     . log(xg1)*st2*xb1**3*xb2**2*xg1**2-4*log(xg1)*st2*xb1**3*xb2**2
     . *xg1*xgl+12*log(xg1)*st2*xb1**3*xb2**2*xg1+8*log(xg1)*st2*xb1
     . **3*xb2**2*xgl+8*log(xg1)*st2*xb1**3*xb2*xg1**2*xgl-12*log(xg1
     . )*st2*xb1**3*xb2*xg1**2-4*log(xg1)*st2*xb1**3*xb2*xg1*xgl-6*
     . log(xg1)*st2*xb1**3*xb2*xg1-4*log(xg1)*st2*xb1**3*xb2*xgl-4*
     . log(xg1)*st2*xb1**3*xg1**2*xgl+6*log(xg1)*st2*xb1**3*xg1**2+4*
     . log(xg1)*st2*xb1**3*xg1*xgl+ans32
      ans30=log(xg1)*s2t**2*st2*xb1**4*xb2*xg1**2+4*log(xg1)*s2t**2*
     . st2*xb1**4*xb2*xg1+log(xg1)*s2t**2*st2*xb1**4*xb2-log(xg1)*s2t
     . **2*st2*xb1**4*xg1**3-4*log(xg1)*s2t**2*st2*xb1**4*xg1**2-log(
     . xg1)*s2t**2*st2*xb1**4*xg1-2*log(xg1)*s2t**2*st2*xb1**3*xb2*
     . xg1**2-2*log(xg1)*s2t**2*st2*xb1**3*xb2*xg1+2*log(xg1)*s2t**2*
     . st2*xb1**3*xg1**3+2*log(xg1)*s2t**2*st2*xb1**3*xg1**2+log(xg1)
     . *s2t**2*st2*xb1**2*xb2*xg1**2-log(xg1)*s2t**2*st2*xb1**2*xg1**
     . 3-2*log(xg1)*s2t**2*xb1**6*xb2+2*log(xg1)*s2t**2*xb1**6*xg1+4*
     . log(xg1)*s2t**2*xb1**5*xb2*xg1+4*log(xg1)*s2t**2*xb1**5*xb2-4*
     . log(xg1)*s2t**2*xb1**5*xg1**2-4*log(xg1)*s2t**2*xb1**5*xg1-2*
     . log(xg1)*s2t**2*xb1**4*xb2*xg1**2-8*log(xg1)*s2t**2*xb1**4*xb2
     . *xg1-2*log(xg1)*s2t**2*xb1**4*xb2+2*log(xg1)*s2t**2*xb1**4*xg1
     . **3+8*log(xg1)*s2t**2*xb1**4*xg1**2+2*log(xg1)*s2t**2*xb1**4*
     . xg1+4*log(xg1)*s2t**2*xb1**3*xb2*xg1**2+4*log(xg1)*s2t**2*xb1
     . **3*xb2*xg1-4*log(xg1)*s2t**2*xb1**3*xg1**3+ans31
      ans29=-log(xg1)*c2t**2*st2*xb1**2*xb2*xg1**2+log(xg1)*c2t**2*
     . st2*xb1**2*xg1**3-log(xg1)*c2t**2*xb1**4*xb2**3+log(xg1)*c2t**
     . 2*xb1**4*xb2**2*xg1+2*log(xg1)*c2t**2*xb1**4*xb2**2-2*log(xg1)
     . *c2t**2*xb1**4*xb2*xg1-log(xg1)*c2t**2*xb1**4*xb2+log(xg1)*c2t
     . **2*xb1**4*xg1+2*log(xg1)*c2t**2*xb1**3*xb2**3*xg1-2*log(xg1)*
     . c2t**2*xb1**3*xb2**2*xg1**2-4*log(xg1)*c2t**2*xb1**3*xb2**2*
     . xg1+4*log(xg1)*c2t**2*xb1**3*xb2*xg1**2+2*log(xg1)*c2t**2*xb1
     . **3*xb2*xg1-2*log(xg1)*c2t**2*xb1**3*xg1**2-log(xg1)*c2t**2*
     . xb1**2*xb2**3*xg1**2+log(xg1)*c2t**2*xb1**2*xb2**2*xg1**3+2*
     . log(xg1)*c2t**2*xb1**2*xb2**2*xg1**2-2*log(xg1)*c2t**2*xb1**2*
     . xb2*xg1**3-log(xg1)*c2t**2*xb1**2*xb2*xg1**2+log(xg1)*c2t**2*
     . xb1**2*xg1**3+log(xg1)*s2t**2*st2*xb1**6*xb2-log(xg1)*s2t**2*
     . st2*xb1**6*xg1-2*log(xg1)*s2t**2*st2*xb1**5*xb2*xg1-2*log(xg1)
     . *s2t**2*st2*xb1**5*xb2+2*log(xg1)*s2t**2*st2*xb1**5*xg1**2+2*
     . log(xg1)*s2t**2*st2*xb1**5*xg1+ans30
      ans28=2*log(-(xb1-xgl))*xb2**2*xg1**3*xgl**2+2*log(-(xb1-xgl))*
     . xb2**2*xg1**2*xgl**2-4*log(-(xb1-xgl))*xb2**2*xg1*xgl**2-4*log
     . (-(xb1-xgl))*xb2*xg1**3*xgl**2+2*log(-(xb1-xgl))*xb2*xg1**2*
     . xgl**2+2*log(-(xb1-xgl))*xb2*xg1*xgl**2+2*log(-(xb1-xgl))*xg1
     . **3*xgl**2-2*log(-(xb1-xgl))*xg1**2*xgl**2-log(xg1)*c2t**2*st2
     . *xb1**4*xb2**3+log(xg1)*c2t**2*st2*xb1**4*xb2**2*xg1+2*log(xg1
     . )*c2t**2*st2*xb1**4*xb2**2-2*log(xg1)*c2t**2*st2*xb1**4*xb2*
     . xg1-log(xg1)*c2t**2*st2*xb1**4*xb2+log(xg1)*c2t**2*st2*xb1**4*
     . xg1+2*log(xg1)*c2t**2*st2*xb1**3*xb2**3*xg1-2*log(xg1)*c2t**2*
     . st2*xb1**3*xb2**2*xg1**2-4*log(xg1)*c2t**2*st2*xb1**3*xb2**2*
     . xg1+4*log(xg1)*c2t**2*st2*xb1**3*xb2*xg1**2+2*log(xg1)*c2t**2*
     . st2*xb1**3*xb2*xg1-2*log(xg1)*c2t**2*st2*xb1**3*xg1**2-log(xg1
     . )*c2t**2*st2*xb1**2*xb2**3*xg1**2+log(xg1)*c2t**2*st2*xb1**2*
     . xb2**2*xg1**3+2*log(xg1)*c2t**2*st2*xb1**2*xb2**2*xg1**2-2*log
     . (xg1)*c2t**2*st2*xb1**2*xb2*xg1**3+ans29
      ans27=4*log(-(xb1-xgl))*xb1**2*xb2**2*xgl**2-4*log(-(xb1-xgl))*
     . xb1**2*xb2*xg1**3+4*log(-(xb1-xgl))*xb1**2*xb2*xg1**2*xgl**2+2
     . *log(-(xb1-xgl))*xb1**2*xb2*xg1**2-2*log(-(xb1-xgl))*xb1**2*
     . xb2*xg1*xgl**2+2*log(-(xb1-xgl))*xb1**2*xb2*xg1-2*log(-(xb1-
     . xgl))*xb1**2*xb2*xgl**2+2*log(-(xb1-xgl))*xb1**2*xg1**3-2*log(
     . -(xb1-xgl))*xb1**2*xg1**2*xgl**2-2*log(-(xb1-xgl))*xb1**2*xg1
     . **2+2*log(-(xb1-xgl))*xb1**2*xg1*xgl**2+4*log(-(xb1-xgl))*xb1*
     . xb2**3*xg1**2*xgl-4*log(-(xb1-xgl))*xb1*xb2**3*xg1*xgl-4*log(-
     . (xb1-xgl))*xb1*xb2**2*xg1**3*xgl-4*log(-(xb1-xgl))*xb1*xb2**2*
     . xg1**2*xgl+8*log(-(xb1-xgl))*xb1*xb2**2*xg1*xgl+8*log(-(xb1-
     . xgl))*xb1*xb2*xg1**3*xgl-4*log(-(xb1-xgl))*xb1*xb2*xg1**2*xgl-
     . 4*log(-(xb1-xgl))*xb1*xb2*xg1*xgl-4*log(-(xb1-xgl))*xb1*xg1**3
     . *xgl+4*log(-(xb1-xgl))*xb1*xg1**2*xgl-2*log(-(xb1-xgl))*xb2**3
     . *xg1**2*xgl**2+2*log(-(xb1-xgl))*xb2**3*xg1*xgl**2+ans28
      ans26=-2*log(-(xb1-xgl))*xb1**4*xb2*xg1-2*log(-(xb1-xgl))*xb1**
     . 4*xb2-2*log(-(xb1-xgl))*xb1**4*xg1**2+2*log(-(xb1-xgl))*xb1**4
     . *xg1-4*log(-(xb1-xgl))*xb1**3*xb2**3*xg1*xgl+4*log(-(xb1-xgl))
     . *xb1**3*xb2**3*xgl+4*log(-(xb1-xgl))*xb1**3*xb2**2*xg1**2*xgl+
     . 4*log(-(xb1-xgl))*xb1**3*xb2**2*xg1*xgl-8*log(-(xb1-xgl))*xb1
     . **3*xb2**2*xgl-8*log(-(xb1-xgl))*xb1**3*xb2*xg1**2*xgl+4*log(-
     . (xb1-xgl))*xb1**3*xb2*xg1*xgl+4*log(-(xb1-xgl))*xb1**3*xb2*xgl
     . +4*log(-(xb1-xgl))*xb1**3*xg1**2*xgl-4*log(-(xb1-xgl))*xb1**3*
     . xg1*xgl-2*log(-(xb1-xgl))*xb1**2*xb2**3*xg1**2+2*log(-(xb1-xgl
     . ))*xb1**2*xb2**3*xg1*xgl**2+2*log(-(xb1-xgl))*xb1**2*xb2**3*
     . xg1-2*log(-(xb1-xgl))*xb1**2*xb2**3*xgl**2+2*log(-(xb1-xgl))*
     . xb1**2*xb2**2*xg1**3-2*log(-(xb1-xgl))*xb1**2*xb2**2*xg1**2*
     . xgl**2+2*log(-(xb1-xgl))*xb1**2*xb2**2*xg1**2-2*log(-(xb1-xgl)
     . )*xb1**2*xb2**2*xg1*xgl**2-4*log(-(xb1-xgl))*xb1**2*xb2**2*xg1
     . +ans27
      ans25=-4*log(-(xb1-xgl))*st2*xb1*xb2**2*xg1**2*xgl+8*log(-(xb1-
     . xgl))*st2*xb1*xb2**2*xg1*xgl+8*log(-(xb1-xgl))*st2*xb1*xb2*xg1
     . **3*xgl-4*log(-(xb1-xgl))*st2*xb1*xb2*xg1**2*xgl-4*log(-(xb1-
     . xgl))*st2*xb1*xb2*xg1*xgl-4*log(-(xb1-xgl))*st2*xb1*xg1**3*xgl
     . +4*log(-(xb1-xgl))*st2*xb1*xg1**2*xgl-2*log(-(xb1-xgl))*st2*
     . xb2**3*xg1**2*xgl**2+2*log(-(xb1-xgl))*st2*xb2**3*xg1*xgl**2+2
     . *log(-(xb1-xgl))*st2*xb2**2*xg1**3*xgl**2+2*log(-(xb1-xgl))*
     . st2*xb2**2*xg1**2*xgl**2-4*log(-(xb1-xgl))*st2*xb2**2*xg1*xgl
     . **2-4*log(-(xb1-xgl))*st2*xb2*xg1**3*xgl**2+2*log(-(xb1-xgl))*
     . st2*xb2*xg1**2*xgl**2+2*log(-(xb1-xgl))*st2*xb2*xg1*xgl**2+2*
     . log(-(xb1-xgl))*st2*xg1**3*xgl**2-2*log(-(xb1-xgl))*st2*xg1**2
     . *xgl**2+2*log(-(xb1-xgl))*xb1**4*xb2**3*xg1-2*log(-(xb1-xgl))*
     . xb1**4*xb2**3-2*log(-(xb1-xgl))*xb1**4*xb2**2*xg1**2-2*log(-(
     . xb1-xgl))*xb1**4*xb2**2*xg1+4*log(-(xb1-xgl))*xb1**4*xb2**2+4*
     . log(-(xb1-xgl))*xb1**4*xb2*xg1**2+ans26
      ans24=2*log(-(xb1-xgl))*st2*xb1**2*xb2**3*xg1-2*log(-(xb1-xgl))
     . *st2*xb1**2*xb2**3*xgl**2+2*log(-(xb1-xgl))*st2*xb1**2*xb2**2*
     . xg1**3-2*log(-(xb1-xgl))*st2*xb1**2*xb2**2*xg1**2*xgl**2+2*log
     . (-(xb1-xgl))*st2*xb1**2*xb2**2*xg1**2-2*log(-(xb1-xgl))*st2*
     . xb1**2*xb2**2*xg1*xgl**2-4*log(-(xb1-xgl))*st2*xb1**2*xb2**2*
     . xg1+4*log(-(xb1-xgl))*st2*xb1**2*xb2**2*xgl**2-4*log(-(xb1-xgl
     . ))*st2*xb1**2*xb2*xg1**3+4*log(-(xb1-xgl))*st2*xb1**2*xb2*xg1
     . **2*xgl**2+2*log(-(xb1-xgl))*st2*xb1**2*xb2*xg1**2-2*log(-(xb1
     . -xgl))*st2*xb1**2*xb2*xg1*xgl**2+2*log(-(xb1-xgl))*st2*xb1**2*
     . xb2*xg1-2*log(-(xb1-xgl))*st2*xb1**2*xb2*xgl**2+2*log(-(xb1-
     . xgl))*st2*xb1**2*xg1**3-2*log(-(xb1-xgl))*st2*xb1**2*xg1**2*
     . xgl**2-2*log(-(xb1-xgl))*st2*xb1**2*xg1**2+2*log(-(xb1-xgl))*
     . st2*xb1**2*xg1*xgl**2+4*log(-(xb1-xgl))*st2*xb1*xb2**3*xg1**2*
     . xgl-4*log(-(xb1-xgl))*st2*xb1*xb2**3*xg1*xgl-4*log(-(xb1-xgl))
     . *st2*xb1*xb2**2*xg1**3*xgl+ans25
      ans23=2*log(-(xb1-xgl))*st2*xb1**4*xb2**3*xg1-2*log(-(xb1-xgl))
     . *st2*xb1**4*xb2**3-2*log(-(xb1-xgl))*st2*xb1**4*xb2**2*xg1**2-
     . 2*log(-(xb1-xgl))*st2*xb1**4*xb2**2*xg1+4*log(-(xb1-xgl))*st2*
     . xb1**4*xb2**2+4*log(-(xb1-xgl))*st2*xb1**4*xb2*xg1**2-2*log(-(
     . xb1-xgl))*st2*xb1**4*xb2*xg1-2*log(-(xb1-xgl))*st2*xb1**4*xb2-
     . 2*log(-(xb1-xgl))*st2*xb1**4*xg1**2+2*log(-(xb1-xgl))*st2*xb1
     . **4*xg1-4*log(-(xb1-xgl))*st2*xb1**3*xb2**3*xg1*xgl+4*log(-(
     . xb1-xgl))*st2*xb1**3*xb2**3*xgl+4*log(-(xb1-xgl))*st2*xb1**3*
     . xb2**2*xg1**2*xgl+4*log(-(xb1-xgl))*st2*xb1**3*xb2**2*xg1*xgl-
     . 8*log(-(xb1-xgl))*st2*xb1**3*xb2**2*xgl-8*log(-(xb1-xgl))*st2*
     . xb1**3*xb2*xg1**2*xgl+4*log(-(xb1-xgl))*st2*xb1**3*xb2*xg1*xgl
     . +4*log(-(xb1-xgl))*st2*xb1**3*xb2*xgl+4*log(-(xb1-xgl))*st2*
     . xb1**3*xg1**2*xgl-4*log(-(xb1-xgl))*st2*xb1**3*xg1*xgl-2*log(-
     . (xb1-xgl))*st2*xb1**2*xb2**3*xg1**2+2*log(-(xb1-xgl))*st2*xb1
     . **2*xb2**3*xg1*xgl**2+ans24
      ans44=(xb2-xg1)
      ans22=ans23*ans44
      ans21=(2*(xb1**4+xg1**2-2*(xg1+1)*xb1**3+(xg1**2+4*xg1+1)*xb1**
     . 2)*(xb2**2-xg1)*xb1-(xb2-xg1)**2*(xb2-1)**2*xb2*xg1-(2*(xb2**4
     . +3*xb2**2*xg1-2*xg1**2)*(xg1+1)-(xb2**4+xg1**2)*xb2-(xg1**2+4*
     . xg1+1)*xb2**3)*xb1**2-(xb1**4*xb2**2-xb1**4*xg1+xb1**3*xb2**3-
     . 2*xb1**3*xb2**2*xg1-2*xb1**3*xb2**2-xb1**3*xb2*xg1+2*xb1**3*
     . xg1**2+2*xb1**3*xg1+xb1**2*xb2**4-2*xb1**2*xb2**3*xg1-2*xb1**2
     . *xb2**3+xb1**2*xb2**2*xg1**2+3*xb1**2*xb2**2*xg1+xb1**2*xb2**2
     . +2*xb1**2*xb2*xg1**2+2*xb1**2*xb2*xg1-xb1**2*xg1**3-4*xb1**2*
     . xg1**2-xb1**2*xg1-xb1*xb2**3*xg1+2*xb1*xb2**2*xg1**2+2*xb1*xb2
     . **2*xg1-xb1*xb2*xg1**3-5*xb1*xb2*xg1**2-xb1*xb2*xg1+2*xb1*xg1
     . **3+2*xb1*xg1**2-xb2**4*xg1+2*xb2**3*xg1**2+2*xb2**3*xg1-xb2**
     . 2*xg1**3-4*xb2**2*xg1**2-xb2**2*xg1+2*xb2*xg1**3+2*xb2*xg1**2-
     . xg1**3)*(xb1-xb2)*st2)*(log(xb2)-log(xg1))*(xg1-1)*s2t**2*xb1+
     . ans22
      ans20=2*ans21
      ans45=-(7*xb1+4*xgl-s2t**2*xb2-3*c2t**2*xb1)*(log(xb1)-log(xg1)
     . )*(st2+1)*(xb1**2-xg1)*(xb2-xg1)**2*(xb2-1)**2*(xg1-1)*xb1
      ans19=ans20+ans45
      ans46=(log(xb1)-log(xg1))*xb2
      ans18=ans19*ans46
      ans47=-2*((((2*(3*xb2**2-xg1-(xg1+1)*xb2)*(xb1-xg1)*(xb1-1)*xb1
     . +(xb2-xg1)**2*(xb2-1)**2*xb2-((3*xb2**2-xg1-(xg1+1)*xb2)*(xb1-
     . xg1)*(xb1-1)*xb1-(xb2-xg1)**2*(xb2-1)**2*xb2)*st2)*s2t**2+2*(
     . st2-2)*(xb1-xg1)*(xb1-1)*(4*xb2**3-2*xb2**2*xg1+7*xb2**2*xgl-2
     . *xb2**2-2*xb2*xg1*xgl-2*xb2*xgl-3*xg1*xgl)+2*(xg1+1-2*xb2)*(
     . st2-2)*(xb1-xg1)*(xb1-1)*c2t**2*xb2**2)*xb2+2*(log(-(xb2-xgl))
     . -log(xgl))*(st2-2)*(xb1-xg1)*(xb1-1)*(xb2**2-xg1)*(xb2-xgl)**2
     . )*(xb1-1)*(xg1-1)+(((st2+1)*(xb2-1)**2*s2t**2+3*(st2-2)*(xb1-1
     . )**2-(st2-2)*(xb1-1)**2*c2t**2)*(xb2-xg1)**2*log(xg1)*xb2-2*(
     . log(xg1)-log(xgl))*(st2-2)*(xb1-1)**2*(xb2**2-xg1)*(xb2-2*xgl)
     . *(xg1-1))*(xb1-xg1)*xb2)*(log(xb2)-log(xg1))*(xb1-xg1)*xb1
      ans17=ans18+ans47
      ans16=-ans17
      ans3=ans4+ans16
      ans2=ans3*xg1
      ans1=-ans2
      rct22=ans1/(16*(xb1-xg1)**2*(xb1-1)**2*(xb2-xg1)**2*(xb2-1)**2*
     . (xg1-1)*xb1*xb2)

      rct32=(-(((log(xb2)-log(xg1))**2*(xb1-3*xb2)*(xb1-1)*(xg1-1)*
     . xb2+(log(xg1)+4)*(xb1-xb2)**2*(xb2-xg1)*log(xg1))*(xb1-xg1)-(
     . log(xb1)-log(xg1))**2*(3*xb1-xb2)*(xb2-xg1)*(xb2-1)*(xg1-1)*
     . xb1-2*(2*(xb1-1)*(xg1-1)-(xb2-xg1)*log(xg1))*(log(xb2)-log(xg1
     . ))*(xb1-xb2)*(xb1-xg1)*xb2+2*((xb2**2+2*xg1-(xg1+1)*xb2-(xg1+1
     . -xb1)*xb1)*(log(xb2)-log(xg1))*(xg1-1)*xb2-((xb1-xg1)*log(xg1)
     . -2*(xb2-1)*(xg1-1))*(xb1-xb2)*(xb2-xg1))*(log(xb1)-log(xg1))*
     . xb1)*c2t*s2t**2*xg1)/(16*(xb1-xb2)*(xb1-xg1)*(xb1-1)*(xb2-xg1)
     . *(xb2-1)*(xg1-1))

      rct2=rct12+rct22+rct32

      if(icontribution.eq.1) then
       r22=r212
       r42=r412
       r52=ratio*r512+r522
       r72=r712+r722
       r82=r812
       r92=r912
       rct2=rct12
      endif
      if(icontribution.eq.2) then
       r22=r222+r232
       r42=r422+r432
       r52=r532+ratio*r542
       r72=r732
       r82=r822
       r92=r922
       rct2=rct22+rct32
      endif

      ral2 = r22+r42+r52+r72+r82+r92+rct2
      bo = fi(amsb1**2,amsb2**2,am1**2)/3
     .   + (ct2/2+st2)*fi(amsb1**2,am1**2,amu**2)
     .   + (st2/2+ct2)*fi(amsb2**2,am1**2,amu**2)
      if(icontribution.eq.1) then
       bo = fi(amsb1**2,amsb2**2,am1**2)/3
      endif
      if(icontribution.eq.2) then
       bo = (ct2/2+st2)*fi(amsb1**2,am1**2,amu**2)
     .    + (st2/2+ct2)*fi(amsb2**2,am1**2,amu**2)
      endif
      ral2 = cf*ral2/bo

      anomalous = -cf/2

      fal1_hdec = dreal(ral2)*fnorm + anomalous
c     write(6,*)'alpha1_sub: ',fal1_hdec

      return
      end
 
      double precision function
     . fal2_hdec(bm2,bmu,amg,amsb1,amsb2,sb,cb,amst1,amst2,st,ct,amt,ic)
      implicit double precision (b-h,o-q,s-z), complex*16 (a,r)
      double precision amg,amsb1,amsb2,amst1,amst2,am2,amu,amt
      double precision mg,mb1,mb2,mt1,mt2,m2,mu,mt
      double precision a,ma,mb
      double complex sp,li2,xgl,xg2,xb1,xb2,xt1,xt2,xt
      double complex sxgl,sxt
      double complex xp,xm,xb12
c     sp(r) = li2(r)
      fi(a,b,c) = (a*b*log(a/b)+b*c*log(b/c)+c*a*log(c/a))
     .          / (a-b)/(b-c)/(a-c)
      xp(q,ma,mb) = (q**2+mb**2-ma**2)/2/q**2
     .  + cdsqrt(dcmplx(((q**2+mb**2-ma**2)/2/q**2)**2-mb**2/q**2,0.d0))
      xm(q,ma,mb) = (q**2+mb**2-ma**2)/2/q**2
     .  - cdsqrt(dcmplx(((q**2+mb**2-ma**2)/2/q**2)**2-mb**2/q**2,0.d0))
      xb12(q,ma,mb) = xp(q,ma,mb)*cdlog(1-1/xp(q,ma,mb))
     .              + xm(q,ma,mb)*cdlog(1-1/xm(q,ma,mb))
      t134p(xa,b,c)  = t134p_hdec(xa,b,c)
      t134(xa,b,c,d) = t134_hdec(xa,b,c,d)

      pi = 4*datan(1.d0)
      zeta2 = pi**2/6
      eps = 1.d-15
      icontribution = ic

      am2 = dabs(bm2)
      amu = dabs(bmu)
      del = 1.d-6
      if(bm2.eq.amu) amu = dabs(bmu)*(1+del)

      fnorm = 1/am2**2

      cf = 4/3.d0

      rim = dcmplx(1.d0,eps)

      sb2 = sb**2
      cb2 = cb**2
      s2b = 2*sb*cb
      c2b = cb**2-sb**2
      st2 = st**2
      ct2 = ct**2
      s2t = 2*st*ct
      c2t = ct**2-st**2

      mt  = amt
      m2  = am2
      mu  = amu
      mg  = amg
      mb1 = amsb1
      mb2 = amsb2
      mt1 = amst1
      mt2 = amst2

      xt  = amt**2/amu**2   * rim
      xgl = amg**2/amu**2   * rim
      xg2 = am2**2/amu**2 * rim
      xb1 = amsb1**2/amu**2 * rim
      xb2 = amsb2**2/amu**2 * rim
      xt1 = amst1**2/amu**2 * rim
      xt2 = amst2**2/amu**2 * rim

      sxgl = cdsqrt(amg**2/amu**2   * rim)
      sxt  = cdsqrt(amt**2/amu**2   * rim)

c--r2
      ans6=14*(((xb1-xb2-(xb2-1)*xb1**2)*sb2+(xb2-1)*xb1)*(xb2-1)-(((
     . xb2+1)*xb1-xb2)*xb2-(xb2**2-xb2+1)*xb1**2)*sb2**2)*xg2**4
      ans5=(((xg2+1-2*xb1)*sb2*xb1+xb1**2-xg2)*(log(xb1)-log(xg2))**2
     . *(sb2-1)*(xb2-xg2)**2*(xb2-1)**2*xb1+((xg2+1-2*xb2)*sb2*xb2+(
     . xb2-xg2)*(xb2-1))*(log(xb2)-log(xg2))**2*(xb1-xg2)**2*(xb1-1)
     . **2*sb2*xb2)*(xg2-1)+(2*((2*xb1+1)*(xb2-1)+3*(xb1-xb2)*sb2)+((
     . xb1-xb2)*sb2+(xb2-1)*xb1)*log(xg2))*((xb1-xb2)*sb2+xb2-1)*(xb1
     . -xg2)**2*(xb2-xg2)**2*log(xg2)-2*((3*(xg2+1-2*xb2)*sb2*xb2+2*(
     . xb2-xg2)*(xb2-1))*(xb1-1)*(xg2-1)+((xb1-xb2)*sb2+xb2-1)*(xb2-
     . xg2)**2*log(xg2))*(log(xb2)-log(xg2))*(xb1-xg2)**2*(xb1-1)*sb2
     . *xb2-14*(((xb2+2)*xb1**2+xb2)*(xb2-1)**2+(xb1**2*xb2**2+xb1**2
     . -6*xb1*xb2+2*xb1+xb2**2+2*xb2-1)*(xb1+xb2)*sb2**2+2*((xb2-1)*
     . xb1-xb2**2-(xb2**2+xb2-3)*xb1**2)*(xb2-1)*sb2)*xb1*xb2*xg2+14*
     . ((2*xb2-1+xb1**2*xb2+(xb2**2-5*xb2+2)*xb1)*sb2**2-(((2*xb2-3)*
     . xb1+1)*sb2-(xb2-1)*xb1)*(xb2-1))*xb1**2*xb2**2+ans6
      ans7=(xb1-xb2)
      ans4=ans5*ans7
      ans9=14*((((xb1-xb2)*(2*xb2**2+2*xb2-1)*xb1-xb2**2-(5*xb2**2-3*
     . xb2-3)*xb1**3)*sb2+((2*xb2+1)*xb1**2+(xb2+2)*xb2)*(xb2-1)*xb1)
     . *(xb2-1)+((xb1**4+xb1*xb2**3+xb1+2*xb2**2-xb2)*xb2-(5*xb2**3+1
     . )*xb1**2+(5*xb2**3-5*xb2**2+2)*xb1**3)*sb2**2)*(xb1-xb2)*xg2**
     . 2-2*(((2*(2*xb1**2-xg2)-(xg2+1)*xb1+3*(xg2+1-2*xb1)*sb2*xb1)*(
     . xb2-1)*(xg2-1)-((xb1-xb2)*sb2+xb2-1)*(xb1-xg2)**2*log(xg2))*(
     . xb2-xg2)-(xg2+1-xb2-xb1)*(log(xb2)-log(xg2))*(xb1-xg2)*(xb1-1)
     . *(xg2-1)*sb2*xb2)*(log(xb1)-log(xg2))*(sb2-1)*(xb1-xb2)*(xb2-
     . xg2)*(xb2-1)*xb1
      ans8=((((sb2-1)*(xb1+1)*(xb2-1)*t134p(mu,mb1,m2)-(xb1-1)*(xb2+1
     . )*t134p(mu,mb2,m2)*sb2)*((xb1-xb2)*sb2+xb2-1)*(xb1-xb2)*(xb1-
     . xg2)*(xb2-xg2)+((xb1-xg2)*(xb1-1)*t134p(mb2,mb1,m2)-(xb2-xg2)*
     . (xb2-1)*t134p(mb1,mb2,m2))*(sb2-1)*(xb1+xb2)*(xb1-1)*(xb2-1)*(
     . xg2-1)*sb2)*(xb1-xg2)*(xb2-xg2)-((sb2-1)*(xb1+xg2)*(xb2-xg2)*
     . t134p(m2,mb1,m2)-(xb1-xg2)*(xb2+xg2)*t134p(m2,mb2,m2)*sb2)*((
     . xb1-xb2)*sb2+xb2-xg2)*(xb1-xb2)*(xb1-1)**2*(xb2-1)**2)*xg2+14*
     . (((3*(xb2-1)*xb1+(xb2-3)*xb2)*xb1**2+(xb2+1)*xb2+(2*xb2+1)*(
     . xb2-1)*xb1)*(xb2-1)*sb2-((2*xb2+1+xb1**2)*(xb2-1)**2*xb1+2*(
     . xb1**2*xb2**2-xb1**2*xb2+xb1**2-xb1*xb2**2-xb1*xb2+xb2**2)*(
     . xb1+xb2)*sb2**2))*(xb1-xb2)*xg2**3+ans9
      ans3=ans4+ans8
      ans2=ans3*xg2
      ans1=-ans2
      r212=ans1/(4*(xb1-xb2)*(xb1-xg2)**2*(xb1-1)**2*(xb2-xg2)**2*(
     . xb2-1)**2*(xg2-1))

      ans4=(xb1+xb2)*(xb1-xg2)*(xb1-1)*(xb2-xg2)**2*(xb2-1)**2*(xg2-1
     . )*t134p(mb1,mb2,m2)*xg2-(xb1-xb2)**2*(xb1-xg2)*(xb1-1)**2*(xb2
     . +xg2)*(xb2-1)**2*t134p(m2,mb2,m2)*xg2+(xb1-xb2)**2*(xb1+xg2)*(
     . xb1-1)**2*(xb2-xg2)*(xb2-1)**2*t134p(m2,mb1,m2)*xg2-(log(xg2)+
     . 6)*(xb1-xb2)**3*(xb1-xg2)**2*(xb2-xg2)**2*log(xg2)-(xg2+1-2*
     . xb2)*(log(xb2)-log(xg2))**2*(xb1-xb2)*(xb1-xg2)**2*(xb1-1)**2*
     . (xg2-1)*xb2**2-(xg2+1-2*xb1)*(log(xb1)-log(xg2))**2*(xb1-xb2)*
     . (xb2-xg2)**2*(xb2-1)**2*(xg2-1)*xb1**2+2*(3*(xg2+1-2*xb2)*(xb1
     . -1)*(xg2-1)*xb2+(xb1-xb2)*(xb2-xg2)**2*log(xg2))*(log(xb2)-log
     . (xg2))*(xb1-xb2)*(xb1-xg2)**2*(xb1-1)*xb2+2*((3*(xg2+1-2*xb1)*
     . (xb2-1)*(xg2-1)*xb1-(xb1-xb2)*(xb1-xg2)**2*log(xg2))*(xb2-xg2)
     . -(xg2+1-xb2-xb1)*(log(xb2)-log(xg2))*(xb1-xg2)*(xb1-1)*(xg2-1)
     . *xb2)*(log(xb1)-log(xg2))*(xb1-xb2)*(xb2-xg2)*(xb2-1)*xb1
      ans3=(14*(xb1**4*xb2**3-xb1**4*xb2*xg2+xb1**3*xb2**4-5*xb1**3*
     . xb2**3*xg2-5*xb1**3*xb2**3+2*xb1**3*xb2**2*xg2**2+7*xb1**3*xb2
     . **2*xg2+2*xb1**3*xb2**2-2*xb1**3*xb2*xg2**2-2*xb1**3*xb2*xg2+2
     . *xb1**3*xg2**2+2*xb1**2*xb2**3*xg2**2+7*xb1**2*xb2**3*xg2+2*
     . xb1**2*xb2**3-xb1**2*xb2**2*xg2**3-5*xb1**2*xb2**2*xg2**2-5*
     . xb1**2*xb2**2*xg2-xb1**2*xb2**2+xb1**2*xb2*xg2**3+xb1**2*xb2*
     . xg2**2+xb1**2*xb2*xg2-xb1**2*xg2**3-xb1**2*xg2**2-xb1*xb2**4*
     . xg2-2*xb1*xb2**3*xg2**2-2*xb1*xb2**3*xg2+xb1*xb2**2*xg2**3+xb1
     . *xb2**2*xg2**2+xb1*xb2**2*xg2+xb1*xb2*xg2**3+xb1*xb2*xg2**2+2*
     . xb2**3*xg2**2-xb2**2*xg2**3-xb2**2*xg2**2)*(xg2-1)+(xb1-xb2)*(
     . xb1-xg2)**2*(xb1-1)*(xb2-xg2)**2*(xb2+1)*t134p(mu,mb2,m2)*xg2-
     . (xb1-xb2)*(xb1-xg2)**2*(xb1+1)*(xb2-xg2)**2*(xb2-1)*t134p(mu,
     . mb1,m2)*xg2)*(xb1-xb2)-(xb1+xb2)*(xb1-xg2)**2*(xb1-1)**2*(xb2-
     . xg2)*(xb2-1)*(xg2-1)*t134p(mb2,mb1,m2)*xg2+ans4
      ans5=(sb2-1)*sb2*xg2
      ans2=ans3*ans5
      ans1=-ans2
      r21p2=ans1/(4*(xb1-xb2)*(xb1-xg2)**2*(xb1-1)**2*(xb2-xg2)**2*(
     . xb2-1)**2*(xg2-1))

      r212 = r212 + r21p2

      ans5=-14*(((((5*xt2-2)*(xt2-1)+xt1)*xt1**2+(xt2**2+2*xt2-1)*xt2
     . -(7*xt2**2-5*xt2+1)*xt1)*xg2*xt1*xt2-((2*xt2-1+xt1**2*xt2+(xt2
     . **2-5*xt2+2)*xt1)*xt1**2*xt2**2-(xg2-2*xt1-2*xt2+1)*(xt1**2*
     . xt2**2-xt1**2*xt2+xt1**2-xt1*xt2**2-xt1*xt2+xt2**2)*xg2**2))*
     . st2-(xg2-xt1**2)*(xg2-xt2)**2*(xt2-1)**2*xt1)*(xg2-1)*(xt1-xt2
     . )*ct2
      ans4=(((14*(xg2-xt2**2)*(xt1-xt2)*xt2+(xg2-xt2)*(xt1+xt2)*(xt2-
     . 1)*t134p(mt2,mt1,m2)*ct2*xg2)*(xg2-xt1)*(xt1-1)-(xg2-xt2)**2*(
     . xt1+xt2)*(xt2-1)**2*t134p(mt1,mt2,m2)*ct2*xg2)*(xg2-1)*(xt1-1)
     . *st2-((xt1-xt2)*st2+xt2-1)*(xg2-xt1)*(xg2-xt2)**2*(xt1-xt2)*(
     . xt1+1)*(xt2-1)*t134p(mu,mt1,m2)*ct2*xg2)*(xg2-xt1)-2*((((4*xt1
     . -1)*xt1-(xt1+2)*xg2-3*(2*xt1-1-xg2)*st2*xt1)*(xg2-1)*(xt2-1)-(
     . (xt1-xt2)*st2+xt2-1)*(xg2-xt1)**2*log(xg2))*(xg2-xt2)-(xt2-1+
     . xt1-xg2)*(log(xg2)-log(xt2))*(xg2-xt1)*(xg2-1)*(xt1-1)*st2*xt2
     . )*(log(xg2)-log(xt1))*(xg2-xt2)*(xt1-xt2)*(xt2-1)*ct2*xt1+ans5
      ans3=(((((xg2-xt2-(xt1-xt2)*st2)*(xg2+xt1)*(xt1-1)*(xt2-1)**2*
     . t134p(m2,mt1,m2)*ct2+((xt1-xt2)*ct2-(xt1-1))*(xg2-xt1)**2*(xg2
     . -xt2)*(xt2+1)*t134p(mu,mt2,m2)*st2)*(xg2-xt2)+(xg2-xt1+(xt1-
     . xt2)*ct2)*(xg2-xt1)*(xg2+xt2)*(xt1-1)*(xt2-1)**2*t134p(m2,mt2,
     . m2)*st2)*xg2+((2*xt2-1-xg2)*ct2*xt2+xg2-xt2**2)*(log(xg2)-log(
     . xt2))**2*(xg2-xt1)**2*(xg2-1)*(xt1-1)*st2*xt2)*(xt1-1)-(((xt1-
     . xt2)**2*st2-(xt2-1)**2*xt1)*ct2-(xt1-1)**2*st2*xt2)*(xg2-xt1)
     . **2*(xg2-xt2)**2*log(xg2)**2+((2*xt1-1-xg2)*st2*xt1+xg2-xt1**2
     . )*(log(xg2)-log(xt1))**2*(xg2-xt2)**2*(xg2-1)*(xt2-1)**2*ct2*
     . xt1+2*(((2*xt1+1)*(xt2-1)**2-3*(xt1-xt2)**2*st2)*ct2+(xt1-1)**
     . 2*(2*xt2+1)*st2)*(xg2-xt1)**2*(xg2-xt2)**2*log(xg2)-2*(((4*xt2
     . -1)*xt2-(xt2+2)*xg2-3*(2*xt2-1-xg2)*ct2*xt2)*(xg2-1)*(xt1-1)+(
     . (xt1-xt2)*ct2-(xt1-1))*(xg2-xt2)**2*log(xg2))*(log(xg2)-log(
     . xt2))*(xg2-xt1)**2*(xt1-1)*st2*xt2)*(xt1-xt2)+ans4
      ans2=ans3*xg2
      ans1=-ans2
      r222=ans1/(2*(xg2-xt1)**2*(xg2-xt2)**2*(xg2-1)*(xt1-xt2)*(xt1-1
     . )**2*(xt2-1)**2)

      ans3=((((xg2+xt2)*(xt1-xt2)**2*(xt1-1)*t134p(m2,mt2,m2)-(xg2-
     . xt2)**2*(xg2-1)*(xt1+xt2)*t134p(mt1,mt2,m2))*(xg2-xt1)-(xg2+
     . xt1)*(xg2-xt2)*(xt1-xt2)**2*(xt1-1)*t134p(m2,mt1,m2))*(xt1-1)*
     . (xt2-1)**2-(((xt1+1)*(xt2-1)*t134p(mu,mt1,m2)-(xt1-1)*(xt2+1)*
     . t134p(mu,mt2,m2))*(xg2-xt2)*(xt1-xt2)**2-(xg2-1)*(xt1+xt2)*(
     . xt1-1)**2*(xt2-1)*t134p(mt2,mt1,m2))*(xg2-xt1)**2*(xg2-xt2))*
     . xg2-14*((((5*xt2-2)*(xt2-1)+xt1)*xt1**2+(xt2**2+2*xt2-1)*xt2-(
     . 7*xt2**2-5*xt2+1)*xt1)*xg2*xt1*xt2-((2*xt2-1+xt1**2*xt2+(xt2**
     . 2-5*xt2+2)*xt1)*xt1**2*xt2**2-(xg2-2*xt1-2*xt2+1)*(xt1**2*xt2
     . **2-xt1**2*xt2+xt1**2-xt1*xt2**2-xt1*xt2+xt2**2)*xg2**2))*(xg2
     . -1)*(xt1-xt2)
      ans2=(((2*xt2-1-xg2)*(log(xg2)-log(xt2))**2*(xg2-1)*(xt1-1)**2*
     . xt2**2-(log(xg2)+6)*(xg2-xt2)**2*(xt1-xt2)**2*log(xg2))*(xg2-
     . xt1)**2+(2*xt1-1-xg2)*(log(xg2)-log(xt1))**2*(xg2-xt2)**2*(xg2
     . -1)*(xt2-1)**2*xt1**2+2*(3*(2*xt2-1-xg2)*(xg2-1)*(xt1-1)*xt2-(
     . xg2-xt2)**2*(xt1-xt2)*log(xg2))*(log(xg2)-log(xt2))*(xg2-xt1)
     . **2*(xt1-1)*xt2+2*((3*(2*xt1-1-xg2)*(xg2-1)*(xt2-1)*xt1+(xg2-
     . xt1)**2*(xt1-xt2)*log(xg2))*(xg2-xt2)+(xt2-1+xt1-xg2)*(log(xg2
     . )-log(xt2))*(xg2-xt1)*(xg2-1)*(xt1-1)*xt2)*(log(xg2)-log(xt1))
     . *(xg2-xt2)*(xt2-1)*xt1)*(xt1-xt2)+ans3
      ans1=ans2*ct2*st2*xg2
      r22p2=ans1/(2*(xg2-xt1)**2*(xg2-xt2)**2*(xg2-1)*(xt1-xt2)*(xt1-
     . 1)**2*(xt2-1)**2)

      r222 = r222 + r22p2

      r22=r212+r222

c--r4
      ans3=-28*((((sb2-1)*(xb2**2-3)*xb2-2)*xb1-(xb1**4+xb2**2-3*(xb2
     . **2+1)*xb1**2)*sb2)*xb2-((sb2-1)*(3*xb2**2-1)+2*xb2**3)*xb1**3
     . )*xg2**2+28*(((2*(2*sb2-1)+(sb2-1)*(xb2**2-3)*xb2)*xb1+(3*xb2
     . **2-1-(xb2**2+1)*xb1**2)*sb2)*xb1-(2*(2*sb2-1)*xb2-(sb2-1)*(
     . xb2**2+1))*xb2)*xb1*xb2*xg2-28*((2*(2*sb2-1)*xb2-(sb2-1)*(xb2
     . **2+1))*xb1**3+(xb2**2+1+(xb2**2-3)*xb1**2)*sb2*xb2-(2*(2*sb2-
     . 1)*xb2**3-(sb2-1)*(3*xb2**2-1))*xb1)*xg2**3
      ans2=((17*xb2**2-7*xg2-5*(xg2+1)*xb2)*(xg2-1)-4*(xb2-xg2)**2*
     . log(xg2)-2*(log(xb2)-log(xg2))*(xb2**2-xg2)*(xg2-1))*(log(xb2)
     . -log(xg2))*(xb1-xg2)**2*(xb1-1)**2*sb2*xb2-2*(((xb1+xg2)*(xb1-
     . 1)**2*t134p(mb1,m2,m2)-(xb1-xg2)**2*(xb1+1)*t134p(mb1,mu,m2))*
     . (sb2-1)*(xb2-xg2)**2*(xb2-1)**2-((xb2+xg2)*(xb2-1)**2*t134p(
     . mb2,m2,m2)-(xb2-xg2)**2*(xb2+1)*t134p(mb2,mu,m2))*(xb1-xg2)**2
     . *(xb1-1)**2*sb2)*xg2+((7*xb1*xb2+5*xb1+5*xb2-17)*(xb1-xb2)*sb2
     . +(7*xb1+5)*(xb2-1)**2+2*((xb1*xb2-1)*(xb1-xb2)*sb2+(xb2-1)**2*
     . xb1)*log(xg2))*(xb1-xg2)**2*(xb2-xg2)**2*log(xg2)-28*(((sb2-1)
     . *(xb2**2+1)+2*xb2)*xb1-(xb1**2+1)*sb2*xb2)*(xb1**2*xb2**2+xg2
     . **4)-((17*xb1**2-7*xg2-5*(xg2+1)*xb1)*(xg2-1)-4*(xb1-xg2)**2*
     . log(xg2)-2*(log(xb1)-log(xg2))*(xb1**2-xg2)*(xg2-1))*(log(xb1)
     . -log(xg2))*(sb2-1)*(xb2-xg2)**2*(xb2-1)**2*xb1+ans3
      ans1=ans2*xg2
      r412=ans1/(4*(xb1-xg2)**2*(xb1-1)**2*(xb2-xg2)**2*(xb2-1)**2*(
     . xg2-1))

      ans4=28*((((st2-1)*(xt2**2-3)*xt2-2)*xt1-(xt1**4+xt2**2-3*(xt2
     . **2+1)*xt1**2)*st2)*xt2-((st2-1)*(3*xt2**2-1)+2*xt2**3)*xt1**3
     . )*xg2**2-28*(((2*(2*st2-1)+(st2-1)*(xt2**2-3)*xt2)*xt1+(3*xt2
     . **2-1-(xt2**2+1)*xt1**2)*st2)*xt1-(2*(2*st2-1)*xt2-(st2-1)*(
     . xt2**2+1))*xt2)*xg2*xt1*xt2+28*((2*(2*st2-1)*xt2-(st2-1)*(xt2
     . **2+1))*xt1**3+(xt2**2+1+(xt2**2-3)*xt1**2)*st2*xt2-(2*(2*st2-
     . 1)*xt2**3-(st2-1)*(3*xt2**2-1))*xt1)*xg2**3
      ans3=((((17*xt2-5)*xt2-(5*xt2+7)*xg2)*(xg2-1)-4*(xg2-xt2)**2*
     . log(xg2)-2*(log(xg2)-log(xt2))*(xg2-xt2**2)*(xg2-1))*(log(xg2)
     . -log(xt2))*(xt1-1)**2*st2*xt2-((7*xt1*xt2+5*xt1+5*xt2-17)*(xt1
     . -xt2)*st2+(7*xt1+5)*(xt2-1)**2+2*((xt1*xt2-1)*(xt1-xt2)*st2+(
     . xt2-1)**2*xt1)*log(xg2))*(xg2-xt2)**2*log(xg2))*(xg2-xt1)**2+2
     . *(((xg2+xt1)*(xt1-1)**2*t134p(mt1,m2,m2)-(xg2-xt1)**2*(xt1+1)*
     . t134p(mt1,mu,m2))*(st2-1)*(xg2-xt2)**2*(xt2-1)**2-((xg2+xt2)*(
     . xt2-1)**2*t134p(mt2,m2,m2)-(xg2-xt2)**2*(xt2+1)*t134p(mt2,mu,
     . m2))*(xg2-xt1)**2*(xt1-1)**2*st2)*xg2+((5*xg2*xt1+7*xg2-17*xt1
     . **2+5*xt1)*(xg2-1)+4*(xg2-xt1)**2*log(xg2)+2*(log(xg2)-log(xt1
     . ))*(xg2-xt1**2)*(xg2-1))*(log(xg2)-log(xt1))*(st2-1)*(xg2-xt2)
     . **2*(xt2-1)**2*xt1+28*(((st2-1)*(xt2**2+1)+2*xt2)*xt1-(xt1**2+
     . 1)*st2*xt2)*(xg2**4+xt1**2*xt2**2)+ans4
      ans2=ans3*xg2
      ans1=-ans2
      r422=ans1/(2*(xg2-xt1)**2*(xg2-xt2)**2*(xg2-1)*(xt1-1)**2*(xt2-
     . 1)**2)

      r42=r412+r422

c--r5
      ans5=2*(((((xgl+1)*xg2+xgl)*xb2-(xb2**2+2*xg2)*xgl+(xb2-xgl)*
     . xb1**2-((2*(xg2+1)-xb2)*xb2-((xgl+1)*xg2+xgl))*xb1)*sb2**2-(2*
     . sb2-1)*(xb1-xgl)*(xb2-xg2)*(xb2-1))*(log(xb2)-log(xg2))*(xg2-1
     . )*xb2-((((xb1-xb2)*sb2+xb2-1)*(xb1-xg2)*log(xg2)*sb2-2*(sb2-1)
     . *(xb1-xgl)*(xb2-1)*(xg2-1))*(xb2-xgl)-((xb1-xb2)*sb2-(xb1-xgl)
     . )*(log(xg2)-log(xgl))*(sb2-1)*(xb2-1)*(xg2-1)*xgl)*(xb2-xg2))*
     . (log(xb1)-log(xg2))*xb1
      ans4=2*(((sb2-1)*(xb1-xgl)*(xb2-xg2)*t134p(m2,mb2,m2)-(xb1-xg2)
     . *(xb2-xgl)*t134p(m2,mb1,m2)*sb2)*((xb1-xb2)*sb2+xb2-xg2)*(xb1-
     . 1)*(xb2-1)-((sb2-1)*(xb1-xgl)*(xb2-1)*t134p(mu,mb2,m2)-(xb1-1)
     . *(xb2-xgl)*t134p(mu,mb1,m2)*sb2)*((xb1-xb2)*sb2+xb2-1)*(xb1-
     . xg2)*(xb2-xg2)-((sb2-1)**2*(xb1-xgl)*(xb2-xg2)*(xb2-1)*t134p(
     . mb1,mb2,m2)-(xb1-xg2)*(xb1-1)*(xb2-xgl)*t134p(mb2,mb1,m2)*sb2
     . **2)*(xb1-xb2)*(xg2-1)+(((xb1-xb2)*sb2+xb2-xg2)*(xb1-1)*(xb2-1
     . )*(xg2-xgl)*t134p(m2,mg,m2)+((xb1-xb2)*sb2+xb2-1)*(xb1-xg2)*(
     . xb2-xg2)*(xgl-1)*t134p(mu,mg,m2)+((sb2-1)*(xb1-xgl)*(xb2-xg2)*
     . (xb2-1)*t134p(mb1,mg,m2)-(xb1-xg2)*(xb1-1)*(xb2-xgl)*t134p(mb2
     . ,mg,m2)*sb2)*(xg2-1))*((xb1-xb2)*sb2-(xb1-xgl)))*xg2+ans5
      ans3=((2*((xb1-xb2)*sb2-(xb1-xgl))*(log(xg2)-log(xgl))*xgl+(log
     . (xg2)+4)*(xb1-xgl)*(xb2-xgl))*((xb1-xb2)*sb2+xb2-1)*(xb2-xg2)*
     . log(xg2)-((2*sb2-3)*xb2+xgl)*(log(xb2)-log(xg2))**2*(xb1-xgl)*
     . (xb1-1)*(xg2-1)*sb2*xb2)*(xb1-xg2)-((2*sb2+1)*xb1-xgl)*(log(
     . xb1)-log(xg2))**2*(sb2-1)*(xb2-xg2)*(xb2-xgl)*(xb2-1)*(xg2-1)*
     . xb1+2*((((xb1-xb2)*sb2+xb2-1)*(sb2-1)*(xb2-xg2)*log(xg2)-2*(
     . xb1-1)*(xb2-xgl)*(xg2-1)*sb2)*(xb1-xgl)-((xb1-xb2)*sb2-(xb1-
     . xgl))*(log(xg2)-log(xgl))*(xb1-1)*(xg2-1)*sb2*xgl)*(log(xb2)-
     . log(xg2))*(xb1-xg2)*xb2+ans4
      ans2=ans3*xg2
      ans1=-ans2
      r512=ans1/(16*(xb1-xg2)*(xb1-xgl)*(xb1-1)*(xb2-xg2)*(xb2-xgl)*(
     . xb2-1)*(xg2-1))

      ans4=(((((xb2-xg2)*t134p(mu,mb1,m2)-(xb2-1)*t134p(m2,mb1,m2)+(
     . t134p(mb2,mb1,m2)-t134p(mb2,mg,m2))*(xg2-1))*(xb1-1)*(xb2-xgl)
     . -(xb1-xgl)*(xb2-xg2)*(xb2-1)*t134p(mu,mb2,m2))*(xb1-xg2)-(((
     . t134p(mb1,mb2,m2)-t134p(mb1,mg,m2))*(xg2-1)-(xb1-1)*t134p(m2,
     . mb2,m2))*(xb1-xgl)*(xb2-xg2)*(xb2-1)-((xb1-xg2)*(xb2-xg2)*(xgl
     . -1)*t134p(mu,mg,m2)+(xb1-1)*(xb2-1)*(xg2-xgl)*t134p(m2,mg,m2))
     . *(xb1-xb2)))*xg2+(log(xg2)-log(xgl))*(xb1-xb2)*(xb1-xg2)*(xb2-
     . xg2)*log(xg2)*xgl)*(xb1-xb2)
      ans3=((((xgl+1)*xg2+xgl)*xb2-(xb2**2+2*xg2)*xgl+(xb2-xgl)*xb1**
     . 2-((2*(xg2+1)-xb2)*xb2-((xgl+1)*xg2+xgl))*xb1)*(log(xb2)-log(
     . xg2))*(xg2-1)*xb2+((log(xg2)-log(xgl))*(xb2-1)*(xg2-1)*xgl-(
     . xb1-xg2)*(xb2-xgl)*log(xg2))*(xb1-xb2)*(xb2-xg2))*(log(xb1)-
     . log(xg2))*xb1-(((log(xb1)-log(xg2))**2*(xb2-xg2)*(xb2-xgl)*(
     . xb2-1)*xb1**2+(log(xb2)-log(xg2))**2*(xb1-xg2)*(xb1-xgl)*(xb1-
     . 1)*xb2**2)*(xg2-1)+((log(xg2)-log(xgl))*(xb1-1)*(xg2-1)*xgl-(
     . xb1-xgl)*(xb2-xg2)*log(xg2))*(log(xb2)-log(xg2))*(xb1-xb2)*(
     . xb1-xg2)*xb2)+ans4
      ans5=(sb2-1)*sb2*xg2
      ans2=ans3*ans5
      ans1=-ans2
      r51p2=ans1/(8*(xb1-xg2)*(xb1-xgl)*(xb1-1)*(xb2-xg2)*(xb2-xgl)*(
     . xb2-1)*(xg2-1))

      r512 = r512 + r51p2

      ans4=2*((((xgl+1)*xg2+xgl)*xb2-(xb2**2+2*xg2)*xgl+(xb2-xgl)*xb1
     . **2-((2*(xg2+1)-xb2)*xb2-((xgl+1)*xg2+xgl))*xb1)*(log(xb2)-log
     . (xg2))*(xg2-1)*sb2*xb2-((((xb1-xb2)*sb2+xb2-1)*(xb1-xg2)*log(
     . xg2)+2*(xb1-xgl)*(xb2-1)*(xg2-1))*(xb2-xgl)-((xb1-xb2)*sb2+xb2
     . -xgl)*(log(xg2)-log(xgl))*(xb2-1)*(xg2-1)*xgl)*(xb2-xg2))*(log
     . (xb1)-log(xg2))*(sb2-1)*xb1
      ans3=-2*((((sb2-1)*(xb1-xgl)*(xb2-xg2)*(xb2-1)*t134p(mb1,mg,m2)
     . -(xb1-xg2)*(xb1-1)*(xb2-xgl)*t134p(mb2,mg,m2)*sb2)*(xg2-1)+((
     . xb1-xb2)*sb2+xb2-1)*(xb1-xg2)*(xb2-xg2)*(xgl-1)*t134p(mu,mg,m2
     . ))*((xb1-xb2)*sb2+xb2-xgl)+((sb2-1)*(xb1-1)*(xb2-xgl)*t134p(mu
     . ,mb1,m2)-(xb1-xgl)*(xb2-1)*t134p(mu,mb2,m2)*sb2)*((xb1-xb2)*
     . sb2+xb2-1)*(xb1-xg2)*(xb2-xg2)+((xb1-xg2)*(xb1-1)*(xb2-xgl)*
     . t134p(mb2,mb1,m2)-(xb1-xgl)*(xb2-xg2)*(xb2-1)*t134p(mb1,mb2,m2
     . ))*(sb2-1)*(xb1-xb2)*(xg2-1)*sb2-((sb2-1)*(xb1-xg2)*(xb2-xgl)*
     . t134p(m2,mb1,m2)-(xb1-xgl)*(xb2-xg2)*t134p(m2,mb2,m2)*sb2-((
     . xb1-xb2)*sb2+xb2-xgl)*(xg2-xgl)*t134p(m2,mg,m2))*((xb1-xb2)*
     . sb2+xb2-xg2)*(xb1-1)*(xb2-1))*xg2+ans4
      ans2=((2*((xb1-xb2)*sb2+xb2-xgl)*(log(xg2)-log(xgl))*xgl-(log(
     . xg2)+4)*(xb1-xgl)*(xb2-xgl))*((xb1-xb2)*sb2+xb2-1)*(xb1-xg2)*
     . log(xg2)-((2*sb2-3)*xb1+xgl)*(log(xb1)-log(xg2))**2*(sb2-1)*(
     . xb2-xgl)*(xb2-1)*(xg2-1)*xb1)*(xb2-xg2)-((2*sb2+1)*xb2-xgl)*(
     . log(xb2)-log(xg2))**2*(xb1-xg2)*(xb1-xgl)*(xb1-1)*(xg2-1)*sb2*
     . xb2+2*((((xb1-xb2)*sb2+xb2-1)*(xb2-xg2)*log(xg2)+2*(xb1-1)*(
     . xb2-xgl)*(xg2-1))*(xb1-xgl)-((xb1-xb2)*sb2+xb2-xgl)*(log(xg2)-
     . log(xgl))*(xb1-1)*(xg2-1)*xgl)*(log(xb2)-log(xg2))*(xb1-xg2)*
     . sb2*xb2+ans3
      ans1=-ans2*xg2
      r522=ans1/(16*(xb1-xg2)*(xb1-xgl)*(xb1-1)*(xb2-xg2)*(xb2-xgl)*(
     . xb2-1)*(xg2-1))

      ans4=-(((((xb2-xg2)*t134p(mu,mb1,m2)-(xb2-1)*t134p(m2,mb1,m2)+(
     . t134p(mb2,mb1,m2)-t134p(mb2,mg,m2))*(xg2-1))*(xb1-1)*(xb2-xgl)
     . -(xb1-xgl)*(xb2-xg2)*(xb2-1)*t134p(mu,mb2,m2))*(xb1-xg2)-(((
     . t134p(mb1,mb2,m2)-t134p(mb1,mg,m2))*(xg2-1)-(xb1-1)*t134p(m2,
     . mb2,m2))*(xb1-xgl)*(xb2-xg2)*(xb2-1)-((xb1-xg2)*(xb2-xg2)*(xgl
     . -1)*t134p(mu,mg,m2)+(xb1-1)*(xb2-1)*(xg2-xgl)*t134p(m2,mg,m2))
     . *(xb1-xb2)))*xg2-(log(xg2)-log(xgl))*(xb1-xb2)*(xb1-xg2)*(xb2-
     . xg2)*log(xg2)*xgl)*(xb1-xb2)
      ans3=((((xgl+1)*xg2+xgl)*xb2-(xb2**2+2*xg2)*xgl+(xb2-xgl)*xb1**
     . 2-((2*(xg2+1)-xb2)*xb2-((xgl+1)*xg2+xgl))*xb1)*(log(xb2)-log(
     . xg2))*(xg2-1)*xb2+((log(xg2)-log(xgl))*(xb2-1)*(xg2-1)*xgl-(
     . xb1-xg2)*(xb2-xgl)*log(xg2))*(xb1-xb2)*(xb2-xg2))*(log(xb1)-
     . log(xg2))*xb1-(((log(xb1)-log(xg2))**2*(xb2-xg2)*(xb2-xgl)*(
     . xb2-1)*xb1**2+(log(xb2)-log(xg2))**2*(xb1-xg2)*(xb1-xgl)*(xb1-
     . 1)*xb2**2)*(xg2-1)+((log(xg2)-log(xgl))*(xb1-1)*(xg2-1)*xgl-(
     . xb1-xgl)*(xb2-xg2)*log(xg2))*(log(xb2)-log(xg2))*(xb1-xb2)*(
     . xb1-xg2)*xb2)+ans4
      ans5=(sb2-1)*sb2*xg2
      ans2=ans3*ans5
      ans1=ans2
      r52p2=ans1/(8*(xb1-xg2)*(xb1-xgl)*(xb1-1)*(xb2-xg2)*(xb2-xgl)*(
     . xb2-1)*(xg2-1))

      r522 = r522 + r52p2

      ans4=2*(((xg2-xt2-(xt1-xt2)*st2)*(xgl+xt-xg2)*(xt1-1)*(xt2-1)*
     . t134(m2,mt,mg,m2)+(xt-1+xgl)*((xt1-xt2)*st2+xt2-1)*(xg2-xt1)*(
     . xg2-xt2)*t134(mu,mt,mg,m2)+((xt-xt1+xgl)*(st2-1)*(xg2-xt2)*(
     . xt2-1)*t134(mt1,mt,mg,m2)-(xt-xt2+xgl)*(xg2-xt1)*(xt1-1)*t134(
     . mt2,mt,mg,m2)*st2)*(xg2-1))*((xb1-xb2)*sb2-(xb1-xgl))-(xg2-xt-
     . xb1)*(xg2-xt2-(xt1-xt2)*st2)*(xb2-xgl)*(xt1-1)*(xt2-1)*t134(m2
     . ,mt,mb1,m2)*sb2+((xg2-xt-xb2)*(xg2-xt2-(xt1-xt2)*st2)*(xt1-1)*
     . (xt2-1)*t134(m2,mt,mb2,m2)-(xt-1+xb2)*((xt1-xt2)*st2+xt2-1)*(
     . xg2-xt1)*(xg2-xt2)*t134(mu,mt,mb2,m2)-((xt-xt1+xb2)*(st2-1)*(
     . xg2-xt2)*(xt2-1)*t134(mt1,mt,mb2,m2)-(xt-xt2+xb2)*(xg2-xt1)*(
     . xt1-1)*t134(mt2,mt,mb2,m2)*st2)*(xg2-1))*(sb2-1)*(xb1-xgl))*
     . xg2
      ans3=(((2*(xt-1+xb1)*t134(mu,mt,mb1,m2)*sb2*xg2+(log(xg2)+4)*(
     . xb1-xgl)*log(xg2))*((xt1-xt2)*st2+xt2-1)*(xg2-xt2)-2*(xt-xt2+
     . xb1)*(xg2-1)*(xt1-1)*t134(mt2,mt,mb1,m2)*sb2*st2*xg2)*(xg2-xt1
     . )+2*(xt-xt1+xb1)*(st2-1)*(xg2-xt2)*(xg2-1)*(xt2-1)*t134(mt1,mt
     . ,mb1,m2)*sb2*xg2+(log(xt2)-4-log(xg2))*(log(xg2)-log(xt2))*(
     . xb1-xgl)*(xg2-xt1)*(xg2-1)*(xt1-1)*st2*xt2-(log(xt1)-4-log(xg2
     . ))*(log(xg2)-log(xt1))*(st2-1)*(xb1-xgl)*(xg2-xt2)*(xg2-1)*(
     . xt2-1)*xt1)*(xb2-xgl)-2*((((xt1-xt2)*st2+xt2-1)*(xg2-xt2)*log(
     . xg2)-(log(xg2)-log(xt2))*(xg2-1)*(xt1-1)*st2*xt2)*(xg2-xt1)+(
     . log(xg2)-log(xt1))*(st2-1)*(xg2-xt2)*(xg2-1)*(xt2-1)*xt1)*((
     . log(xb1)-log(xg2))*(xb2-xgl)*sb2*xb1-(log(xb2)-log(xg2))*(sb2-
     . 1)*(xb1-xgl)*xb2-((xb1-xb2)*sb2-(xb1-xgl))*(log(xg2)-log(xgl))
     . *xgl)+ans4
      ans2=ans3*xg2
      ans1=-ans2
      r532=ans1/(8*(xb1-xgl)*(xb2-xgl)*(xg2-xt1)*(xg2-xt2)*(xg2-1)*(
     . xt1-1)*(xt2-1))

      ans3=-2*(((xg2-xt2-(xt1-xt2)*st2)*(xgl-xt-xg2)*(xt1-1)*(xt2-1)*
     . t134(m2,mt,mg,m2)-(xt+1-xgl)*((xt1-xt2)*st2+xt2-1)*(xg2-xt1)*(
     . xg2-xt2)*t134(mu,mt,mg,m2)-((xt+xt1-xgl)*(st2-1)*(xg2-xt2)*(
     . xt2-1)*t134(mt1,mt,mg,m2)-(xt+xt2-xgl)*(xg2-xt1)*(xt1-1)*t134(
     . mt2,mt,mg,m2)*st2)*(xg2-1))*((xb1-xb2)*sb2+xb2-xgl)-(xg2+xt-
     . xb1)*(xg2-xt2-(xt1-xt2)*st2)*(sb2-1)*(xb2-xgl)*(xt1-1)*(xt2-1)
     . *t134(m2,mt,mb1,m2)+((xg2+xt-xb2)*(xg2-xt2-(xt1-xt2)*st2)*(xt1
     . -1)*(xt2-1)*t134(m2,mt,mb2,m2)+(xt+1-xb2)*((xt1-xt2)*st2+xt2-1
     . )*(xg2-xt1)*(xg2-xt2)*t134(mu,mt,mb2,m2)+((xt+xt1-xb2)*(st2-1)
     . *(xg2-xt2)*(xt2-1)*t134(mt1,mt,mb2,m2)-(xt+xt2-xb2)*(xg2-xt1)*
     . (xt1-1)*t134(mt2,mt,mb2,m2)*st2)*(xg2-1))*(xb1-xgl)*sb2)*xg2
      ans2=(((2*(xt+1-xb1)*(sb2-1)*t134(mu,mt,mb1,m2)*xg2-(log(xg2)+4
     . )*(xb1-xgl)*log(xg2))*((xt1-xt2)*st2+xt2-1)*(xg2-xt2)-2*(xt+
     . xt2-xb1)*(sb2-1)*(xg2-1)*(xt1-1)*t134(mt2,mt,mb1,m2)*st2*xg2)*
     . (xg2-xt1)+2*(xt+xt1-xb1)*(sb2-1)*(st2-1)*(xg2-xt2)*(xg2-1)*(
     . xt2-1)*t134(mt1,mt,mb1,m2)*xg2-(log(xt2)-4-log(xg2))*(log(xg2)
     . -log(xt2))*(xb1-xgl)*(xg2-xt1)*(xg2-1)*(xt1-1)*st2*xt2+(log(
     . xt1)-4-log(xg2))*(log(xg2)-log(xt1))*(st2-1)*(xb1-xgl)*(xg2-
     . xt2)*(xg2-1)*(xt2-1)*xt1)*(xb2-xgl)-2*((((xt1-xt2)*st2+xt2-1)*
     . (xg2-xt2)*log(xg2)-(log(xg2)-log(xt2))*(xg2-1)*(xt1-1)*st2*xt2
     . )*(xg2-xt1)+(log(xg2)-log(xt1))*(st2-1)*(xg2-xt2)*(xg2-1)*(xt2
     . -1)*xt1)*((log(xb1)-log(xg2))*(sb2-1)*(xb2-xgl)*xb1-(log(xb2)-
     . log(xg2))*(xb1-xgl)*sb2*xb2-((xb1-xb2)*sb2+xb2-xgl)*(log(xg2)-
     . log(xgl))*xgl)+ans3
      ans1=-ans2*xg2
      r542=ans1/(8*(xb1-xgl)*(xb2-xgl)*(xg2-xt1)*(xg2-xt2)*(xg2-1)*(
     . xt1-1)*(xt2-1))

      ans4=2*((log(xb1)-log(xg2))*(sb2-1)*(xb2-xgl)*xb1-(log(xb2)-log
     . (xg2))*(xb1-xgl)*sb2*xb2-((xb1-xb2)*sb2+xb2-xgl)*(log(xg2)-log
     . (xgl))*xgl)*(((log(xg2)-log(xt2))*(xg2-1)*(xt1-1)*xt2-(xg2-xt2
     . )*(xt1-xt2)*log(xg2))*(xg2-xt1)-(log(xg2)-log(xt1))*(xg2-xt2)*
     . (xg2-1)*(xt2-1)*xt1)+2*((((xt-xt2-xb2)*(xg2-1)*(xt1-1)*t134(
     . mt2,mt,mb2,m2)-(xt-1-xb2)*(xg2-xt2)*(xt1-xt2)*t134(mu,mt,mb2,
     . m2))*(xg2-xt1)-(xt-xt1-xb2)*(xg2-xt2)*(xg2-1)*(xt2-1)*t134(mt1
     . ,mt,mb2,m2))*(xb1-xgl)*sb2-(((xt-xt2-xgl)*(xg2-1)*(xt1-1)*t134
     . (mt2,mt,mg,m2)-(xt-1-xgl)*(xg2-xt2)*(xt1-xt2)*t134(mu,mt,mg,m2
     . ))*(xg2-xt1)-(xt-xt1-xgl)*(xg2-xt2)*(xg2-1)*(xt2-1)*t134(mt1,
     . mt,mg,m2))*((xb1-xb2)*sb2+xb2-xgl))*xg2
      ans3=(((2*(xt-1-xb1)*(sb2-1)*t134(mu,mt,mb1,m2)*xg2-(log(xg2)+4
     . )*(xb1-xgl)*log(xg2))*(xg2-xt2)*(xt1-xt2)-2*(xt-xt2-xb1)*(sb2-
     . 1)*(xg2-1)*(xt1-1)*t134(mt2,mt,mb1,m2)*xg2)*(xg2-xt1)+2*(xt-
     . xt1-xb1)*(sb2-1)*(xg2-xt2)*(xg2-1)*(xt2-1)*t134(mt1,mt,mb1,m2)
     . *xg2)*(xb2-xgl)-2*(xg2-xt+xb2)*(xb1-xgl)*(xt1-xt2)*(xt1-1)*(
     . xt2-1)*t134(m2,mt,mb2,m2)*sb2*xg2+2*(xg2-xt+xb1)*(sb2-1)*(xb2-
     . xgl)*(xt1-xt2)*(xt1-1)*(xt2-1)*t134(m2,mt,mb1,m2)*xg2+2*((xb1-
     . xb2)*sb2+xb2-xgl)*(xgl-xt+xg2)*(xt1-xt2)*(xt1-1)*(xt2-1)*t134(
     . m2,mt,mg,m2)*xg2-(log(xt2)-4-log(xg2))*(log(xg2)-log(xt2))*(
     . xb1-xgl)*(xb2-xgl)*(xg2-xt1)*(xg2-1)*(xt1-1)*xt2+(log(xt1)-4-
     . log(xg2))*(log(xg2)-log(xt1))*(xb1-xgl)*(xb2-xgl)*(xg2-xt2)*(
     . xg2-1)*(xt2-1)*xt1+ans4
      ans2=ans3*s2t*xg2
      ans1=-ans2
      r53p2=ans1/(16*(xb1-xgl)*(xb2-xgl)*(xg2-xt1)*(xg2-xt2)*(xg2-1)*
     . (xt1-1)*(xt2-1))

      r54p2=(((((xg2-xt2)*(xg2-1)*t134(mt1,mt,mb2,m2)-(xt1-xt2)*(xt1-
     . 1)*t134(m2,mt,mb2,m2))*(xt2-1)+((xg2-xt2)*(xt1-xt2)*t134(mu,mt
     . ,mb2,m2)-(xg2-1)*(xt1-1)*t134(mt2,mt,mb2,m2))*(xg2-xt1))*(sb2-
     . 1)*(xb1-xgl)-(((xg2-xt2)*(xg2-1)*t134(mt1,mt,mg,m2)-(xt1-xt2)*
     . (xt1-1)*t134(m2,mt,mg,m2))*(xt2-1)+((xg2-xt2)*(xt1-xt2)*t134(
     . mu,mt,mg,m2)-(xg2-1)*(xt1-1)*t134(mt2,mt,mg,m2))*(xg2-xt1))*((
     . xb1-xb2)*sb2-(xb1-xgl))-(((xg2-xt2)*(xg2-1)*t134(mt1,mt,mb1,m2
     . )-(xt1-xt2)*(xt1-1)*t134(m2,mt,mb1,m2))*(xt2-1)+((xg2-xt2)*(
     . xt1-xt2)*t134(mu,mt,mb1,m2)-(xg2-1)*(xt1-1)*t134(mt2,mt,mb1,m2
     . ))*(xg2-xt1))*(xb2-xgl)*sb2)*s2t*xg2**2)/(4*(xb1-xgl)*(xb2-xgl
     . )*(xg2-xt1)*(xg2-xt2)*(xg2-1)*(xt1-1)*(xt2-1))

      r53p2 = mt/m2 * r53p2
      r54p2 = mt*m2/mu**2 * r54p2

      r532 = r532 + r53p2
      r542 = r542 + r54p2

      ratio = amg/am2
      r52=r512+ratio*r522+r532+ratio*r542

c--r7
      ans8=-((((xb2**2+5*xg2)*(xg2+1)*xb2-xg2**2-(2*xg2**2+7*xg2+2)*
     . xb2**2-(3*xb2**2+xg2-2*(xg2+1)*xb2)*xb1**2+((5*xb2**2+xg2)*(
     . xg2+1)-xb2**3-(2*xg2**2+7*xg2+2)*xb2)*xb1)*xb1+(2*xb2**4-xg2**
     . 2-2*(2*xb2**2+xg2)*(xg2+1)*xb2+(2*xg2**2+7*xg2+2)*xb2**2)*xb2)
     . *(xb1-xg2)*(xb1-1)*sb2*xb1+(2*(2*(xg2+1)-xb1)*xb1**4+(xb2-xg2)
     . *(xb2-1)*xb2*xg2-((xg2+1-xb2)*xb2+2*xg2**2+7*xg2+2)*xb1**3-((2
     . *xb2**2+5*xg2)*(xg2+1)*xb2-xg2**2-(2*xg2**2+7*xg2+2)*xb2**2)*
     . xb1-((5*xb2**2-2*xg2)*(xg2+1)-3*xb2**3-(2*xg2**2+7*xg2+2)*xb2)
     . *xb1**2)*(xb2-xg2)*(xb2-1)*cb2*xb2)*(log(xb2)-log(xg2))*(xg2-1
     . )*sb2
      ans7=((((((7*(xg2+1)-5*xb2-7*xb1)*xb1+5*(xg2+1)*xb2-7*xg2)*xb1+
     . (4*xb2**2-xg2-4*(xg2+1)*xb2)*xb2)*(xb1-xg2)*(xb1-1)*sb2**2-2*(
     . 2*(2*xb1**2+xg2)-3*(xg2+1)*xb1)*(xb1-xb2)*(xb2-xg2)*(xb2-1)*
     . cb2**2)*xb1-((8*(xg2+1)-3*xb2)*xb1**3-(8*xb1**4+xb2**2*xg2)+(3
     . *(xg2+1)*xb2-7*xg2)*xb1*xb2-(5*xb2**2+8*xg2-5*(xg2+1)*xb2)*xb1
     . **2)*(xb2-xg2)*(xb2-1)*cb2*sb2)*(xb2-1)*(xg2-1)-((xb1-1)*sb2+(
     . xb2-1)*cb2)**2*(xb1-xb2)*(xb1-xg2)**2*(xb2-xg2)*log(xg2)*xb1)*
     . (xb2-xg2)+ans8
      ans9=(log(xb1)-log(xg2))*cb2
      ans6=2*ans7*ans9
      ans5=(((((xb2**2+3*xg2-2*(xg2+1)*xb2)*xb1+6*(xb2-xg2)*(xb2-1)*
     . xb2)*xb2+(3*xb2**2+xg2-2*(xg2+1)*xb2)*xb1**2)*cb2+(11*xb2**2+5
     . *xg2-8*(xg2+1)*xb2)*(xb1-xb2)*sb2*xb2)*(xb1-xg2)*(xb1-1)*sb2-2
     . *((xg2+1-xb1)*xb1**2+(xb2-xg2)*(xb2-1)*xb2-(xg2+1-xb2)*xb1*xb2
     . )*(xb2-xg2)*(xb2-1)*cb2**2*xb2)*(log(xb2)-log(xg2))**2*(xb1-
     . xg2)*(xb1-1)*(xg2-1)*sb2-2*((((((3*xb2**2+7*xg2-5*(xg2+1)*xb2)
     . *xb1+8*(xb2-xg2)*(xb2-1)*xb2)*xb2+(5*xb2**2+xg2-3*(xg2+1)*xb2)
     . *xb1**2)*cb2+2*(2*(2*xb2**2+xg2)-3*(xg2+1)*xb2)*(xb1-xb2)*sb2*
     . xb2)*(xb1-xg2)*(xb1-1)*sb2-(4*(xg2+1-xb1)*xb1**2+7*(xb2-xg2)*(
     . xb2-1)*xb2+(5*xb2**2+xg2-5*(xg2+1)*xb2)*xb1)*(xb2-xg2)*(xb2-1)
     . *cb2**2*xb2)*(xb1-1)*(xg2-1)+((xb1-1)*sb2+(xb2-1)*cb2)**2*(xb1
     . -xb2)*(xb1-xg2)*(xb2-xg2)**2*log(xg2)*xb2)*(log(xb2)-log(xg2))
     . *(xb1-xg2)*sb2+ans6
      ans4=4*((((5*xb1**2+6*xb1*xb2+3*xb2**2)*(xb1-xg2)*(xb1-1)*sb2-(
     . 3*xb1**2+6*xb1*xb2+5*xb2**2)*(xb2-xg2)*(xb2-1)*cb2)*cb2*sb2+2*
     . ((xb1-xg2)*(xb1-1)*sb2**3*xb2+(xb2-xg2)*(xb2-1)*cb2**3*xb1)*(
     . xb1-xb2))*(xb1-1)*(xb2-1)*(xg2-1)-((xb1+1)*t134p(mu,mb1,m2)*
     . cb2+(xb2+1)*t134p(mu,mb2,m2)*sb2)*((xb1-1)*sb2+(xb2-1)*cb2)**2
     . *(xb1-xb2)*(xb1-xg2)*(xb2-xg2)*xg2)*(xb1-xg2)*(xb2-xg2)+(((6*(
     . xg2+1)-xb2)*xb1**3-(6*xb1**4+xb2**2*xg2)+(2*(xg2+1)*xb2-3*xg2)
     . *xb1*xb2-(3*(xb2**2+2*xg2)-2*(xg2+1)*xb2)*xb1**2)*(xb2-xg2)*(
     . xb2-1)*cb2*sb2-(2*((xg2+1-xb2)*(xb1+xb2)*(xb1-xb2)-xb1**3+((
     . xg2+1)*xb2-xg2)*xb1)*(xb1-xg2)*(xb1-1)*sb2**2-(11*xb1**2+5*xg2
     . -8*(xg2+1)*xb1)*(xb1-xb2)*(xb2-xg2)*(xb2-1)*cb2**2)*xb1)*(log(
     . xb1)-log(xg2))**2*(xb2-xg2)*(xb2-1)*(xg2-1)*cb2+ans5
      ans3=(4*((xb1+xg2)*t134p(m2,mb1,m2)*cb2+(xb2+xg2)*t134p(m2,mb2,
     . m2)*sb2)*((xb1-xg2)*sb2+(xb2-xg2)*cb2)**2*(xb1-1)**2*(xb2-1)**
     . 2*xg2+((xb1-1)*sb2+(xb2-1)*cb2)**2*(log(xg2)+4)*(cb2*xb1+sb2*
     . xb2)*(xb1-xg2)**2*(xb2-xg2)**2*log(xg2))*(xb1-xb2)-4*((3*xb2**
     . 2-xg2-(xg2+1)*xb2)*(xb1-xb2)*sb2+4*(xb2-xg2)*(xb2-1)*cb2*xb2)*
     . (xb1-xg2)**2*(xb1-1)**2*(xg2-1)*t134p(mb2,mb2,m2)*sb2**2*xg2-4
     . *(((xb1**2+xb2**2)*(xg2+1)-2*(xb2**2+xg2)*xb1)*cb2-2*(xb1+xb2)
     . *(xb1-xg2)*(xb1-1)*sb2)*(xb2-xg2)**2*(xb2-1)**2*(xg2-1)*t134p(
     . mb1,mb2,m2)*cb2*sb2*xg2-4*((3*xb1**2-xg2-(xg2+1)*xb1)*(xb1-xb2
     . )*cb2-4*(xb1-xg2)*(xb1-1)*sb2*xb1)*(xb2-xg2)**2*(xb2-1)**2*(
     . xg2-1)*t134p(mb1,mb1,m2)*cb2**2*xg2+4*((((xg2+1)*xb2-2*xg2)*
     . xb2+(xg2+1-2*xb2)*xb1**2)*sb2-2*(xb1+xb2)*(xb2-xg2)*(xb2-1)*
     . cb2)*(xb1-xg2)**2*(xb1-1)**2*(xg2-1)*t134p(mb2,mb1,m2)*cb2*sb2
     . *xg2+ans4
      ans2=ans3*xg2
      ans1=-ans2
      r712=ans1/(16*(xb1-xb2)*(xb1-xg2)**2*(xb1-1)**2*(xb2-xg2)**2*(
     . xb2-1)**2*(xg2-1))

      ans5=-(2*(3*(xg2+1+xb2)*xb1**2-(5*xb1**3+xb2*xg2)-((xg2+1)*xb2+
     . xg2)*xb1)*cb2-(3*xb1**2-xg2-(xg2+1)*xb1)*(xb1-xb2)*sb2)*(xb2-
     . xg2)**2*(xb2-1)**2*(xg2-1)*t134p(mb1,mb1,m2)
      ans4=((((xb2-2+xb1)*cb2+2*(xb1-1)*sb2)*(xb2+1)*t134p(mu,mb2,m2)
     . -((xb2-2+xb1)*sb2+2*(xb2-1)*cb2)*(xb1+1)*t134p(mu,mb1,m2))*(
     . xb1-xg2)**2*(xb2-xg2)**2+((xb2-2*xg2+xb1)*sb2+2*(xb2-xg2)*cb2)
     . *(xb1+xg2)*(xb1-1)**2*(xb2-1)**2*t134p(m2,mb1,m2)-((xb2-2*xg2+
     . xb1)*cb2+2*(xb1-xg2)*sb2)*(xb1-1)**2*(xb2+xg2)*(xb2-1)**2*
     . t134p(m2,mb2,m2))*(xb1-xb2)**2-(((xb1**2+xb2**2)*(xg2+1)-2*(
     . xb2**2+xg2)*xb1)*cb2-2*(xb1+xb2)*(xb1-xg2)*(xb1-1)*sb2)*(xb2-
     . xg2)**2*(xb2-1)**2*(xg2-1)*t134p(mb1,mb2,m2)+((((xg2+1)*xb2-2*
     . xg2)*xb2+(xg2+1-2*xb2)*xb1**2)*sb2-2*(xb1+xb2)*(xb2-xg2)*(xb2-
     . 1)*cb2)*(xb1-xg2)**2*(xb1-1)**2*(xg2-1)*t134p(mb2,mb1,m2)-(2*(
     . (5*xb2**2+xg2-3*(xg2+1)*xb2)*xb2-(3*xb2**2-xg2-(xg2+1)*xb2)*
     . xb1)*sb2-(3*xb2**2-xg2-(xg2+1)*xb2)*(xb1-xb2)*cb2)*(xb1-xg2)**
     . 2*(xb1-1)**2*(xg2-1)*t134p(mb2,mb2,m2)+ans5
      ans3=4*ans4*xg2
      ans11=-((((xb2**2+5*xg2)*(xg2+1)*xb2-xg2**2-(2*xg2**2+7*xg2+2)*
     . xb2**2-(3*xb2**2+xg2-2*(xg2+1)*xb2)*xb1**2+((5*xb2**2+xg2)*(
     . xg2+1)-xb2**3-(2*xg2**2+7*xg2+2)*xb2)*xb1)*xb1+(2*xb2**4-xg2**
     . 2-2*(2*xb2**2+xg2)*(xg2+1)*xb2+(2*xg2**2+7*xg2+2)*xb2**2)*xb2)
     . *(xb1-xg2)*(xb1-1)*sb2*xb1+(2*(2*(xg2+1)-xb1)*xb1**4+(xb2-xg2)
     . *(xb2-1)*xb2*xg2-((xg2+1-xb2)*xb2+2*xg2**2+7*xg2+2)*xb1**3-((2
     . *xb2**2+5*xg2)*(xg2+1)*xb2-xg2**2-(2*xg2**2+7*xg2+2)*xb2**2)*
     . xb1-((5*xb2**2-2*xg2)*(xg2+1)-3*xb2**3-(2*xg2**2+7*xg2+2)*xb2)
     . *xb1**2)*(xb2-xg2)*(xb2-1)*cb2*xb2)*(log(xb2)-log(xg2))*(xg2-1
     . )
      ans10=((((14*(xg2+1)-5*xb2)*xb1**4-(7*xb1**5+5*xb2*xg2**2)+(2*(
     . xg2+1+4*xb2)*xb2-(7*xg2**2+20*xg2+7))*xb1**3-(2*((xb2**2-4*xg2
     . )*(xg2+1)+2*xb2**3)-(xg2**2-12*xg2+1)*xb2)*xb1**2+(2*(xb2**2+4
     . *xg2)*(xg2+1)*xb2-3*xg2**2-2*(xg2**2+1)*xb2**2)*xb1)*sb2*xb1-(
     . (20*(xg2+1)+13*xb2)*xb1**3-(24*xb1**4+xb2**2*xg2)+(3*(xg2+1)*
     . xb2+xg2)*xb1*xb2-(5*xb2**2+16*xg2+7*(xg2+1)*xb2)*xb1**2)*(xb2-
     . xg2)*(xb2-1)*cb2)*(xb2-1)*(xg2-1)-((xb2-2+xb1)*sb2+2*(xb2-1)*
     . cb2)*(xb1-xb2)**2*(xb1-xg2)**2*(xb2-xg2)*log(xg2)*xb1)*(xb2-
     . xg2)+ans11
      ans12=(log(xb1)-log(xg2))
      ans9=2*ans10*ans12
      ans8=-((2*(2*(xg2+1)-xb2-xb1)*xb1**4-(3*xb2**2+5*xg2-3*(xg2+1)*
     . xb2)*xb2*xg2-((7*(xg2+1)-11*xb2)*xb2+2*xg2**2-3*xg2+2)*xb1**3+
     . ((xb2**2-4*xg2)*(xg2+1)-9*xb2**3+(6*xg2**2-xg2+6)*xb2)*xb1**2+
     . ((6*xb2**2+5*xg2)*(xg2+1)*xb2+3*xg2**2-(6*xg2**2+7*xg2+6)*xb2
     . **2)*xb1)*sb2*xb1-((22*(xg2+1)+21*xb2)*xb1**3-(28*xb1**4+xb2**
     . 2*xg2)+(2*(xg2+1)*xb2+7*xg2)*xb1*xb2-(3*xb2**2+16*xg2+14*(xg2+
     . 1)*xb2)*xb1**2)*(xb2-xg2)*(xb2-1)*cb2)*(log(xb1)-log(xg2))**2*
     . (xb2-xg2)*(xb2-1)*(xg2-1)+ans9
      ans7=2*((((2*((xg2+1-4*xb2)*xb2+xg2**2+1-(xg2+1-2*xb2)*xb1)*xb1
     . *xb2+5*(xb2**4+xg2**2)-2*(xb2**2+4*xg2)*(xg2+1)*xb2-(xg2**2-12
     . *xg2+1)*xb2**2)*xb1+(7*xb2**4+3*xg2**2-2*(7*xb2**2+4*xg2)*(xg2
     . +1)*xb2+(7*xg2**2+20*xg2+7)*xb2**2)*xb2)*cb2*xb2-((5*xb2**2+
     . xg2-3*(xg2+1)*xb2)*xb1**2+4*(6*xb2**2-5*xb2*xg2-5*xb2+4*xg2)*
     . xb2**2-(13*xb2**2+xg2-7*(xg2+1)*xb2)*xb1*xb2)*(xb1-xg2)*(xb1-1
     . )*sb2)*(xb1-1)*(xg2-1)+((xb2-2+xb1)*cb2+2*(xb1-1)*sb2)*(xb1-
     . xb2)**2*(xb1-xg2)*(xb2-xg2)**2*log(xg2)*xb2)*(log(xb2)-log(xg2
     . ))*(xb1-xg2)+ans8
      ans6=(4*((5*xb1**4+7*xb2**2*xg2+(5*xb2**2+3*xg2)*xb1**2-(5*(xg2
     . +1)-2*xb2)*xb1**3+(2*(xb2**2+2*xg2)-9*(xg2+1)*xb2)*xb1*xb2)*
     . sb2-(((5*xb2**2+3*xg2-5*(xg2+1)*xb2)*xb2+2*(xb2**2+2*xg2+xb1**
     . 2)*xb1)*xb2+(5*xb2**2+7*xg2-9*(xg2+1)*xb2)*xb1**2)*cb2)*(xb1-1
     . )*(xb2-1)*(xg2-1)+((xb1-2)*sb2+(xb2-2)*cb2)*(log(xg2)+4)*(xb1-
     . xb2)**3*(xb1-xg2)*(xb2-xg2)*log(xg2))*(xb1-xg2)*(xb2-xg2)+((((
     . xb2**2+3*xg2)*(xg2+1)+11*xb2**3-(6*xg2**2+7*xg2+6)*xb2-3*(3*
     . xb2**2+xg2-2*(xg2+1)*xb2)*xb1)*xb1**2-(2*xb2**4-3*xg2**2-4*(
     . xb2**2-xg2)*(xg2+1)*xb2+(2*xg2**2-3*xg2+2)*xb2**2)*xb2-(2*xb2
     . **4+5*xg2**2+(7*xb2**2-5*xg2)*(xg2+1)*xb2-(6*xg2**2-xg2+6)*xb2
     . **2)*xb1)*cb2*xb2+((3*xb2**2+xg2-2*(xg2+1)*xb2)*(xb1-7*xb2)*
     . xb1+2*(14*xb2**2-11*xb2*xg2-11*xb2+8*xg2)*xb2**2)*(xb1-xg2)*(
     . xb1-1)*sb2)*(log(xb2)-log(xg2))**2*(xb1-xg2)*(xb1-1)*(xg2-1)+
     . ans7
      ans2=ans3+ans6
      ans1=ans2*cb2*sb2*xg2
      r71p2=ans1/(16*(xb1-xb2)*(xb1-xg2)**2*(xb1-1)**2*(xb2-xg2)**2*(
     . xb2-1)**2*(xg2-1))

      r712 = r712 + r71p2

      ans8=(((3*xt2-2)*xt1**4+2*(xt2-1)**2*xt2**3-(4*xt2+1)*(3*xt2-2)
     . *xt1**3+(2*xt2**2-21*xt2+16)*xt1*xt2**2+(17*xt2**2-2*xt2-8)*
     . xt1**2*xt2)*xt2-((4*xt2+1-xt1)*(2*xt2-1)*xt1**2-(2*xt2**2-18*
     . xt2+13)*xt2**2-(16*xt2**2-7*xt2-2)*xt1*xt2)*xg2**2-((2*(xt2**2
     . +xt2-1)*xt2+(2*xt2-1)*xt1**2)*xt1**2+(4*xt2**2-25*xt2+18)*xt2
     . **3-(5*xt2**2-1)*xt1**3+(21*xt2**2-24*xt2+7)*xt1*xt2**2)*xg2)*
     . st2**2
      ans7=((2*(4*xt2-7)*(xt2-1)*xt2**3+(2*xt2-1)*xt1**4+(xt2**2-3*
     . xt2+1)*xt1**3+(3*xt2**2-5*xt2+1)*xt1**2*xt2+(14*xt2**2-25*xt2+
     . 12)*xt1*xt2**2)*xg2-((2*((2*xt2-5)*xt1+2*(xt2-1)*xt2)*(xt2-1)*
     . xt2**2-(xt2+1-xt1)*(3*xt2-2)*xt1**3+(6*xt2**2-3*xt2-2)*xt1**2*
     . xt2)*xt2-((xt2+1-xt1)*(2*xt2-1)*xt1**2-2*(2*xt2-5)*(xt2-1)*xt2
     . **2-(10*xt2**2-12*xt2+3)*xt1*xt2)*xg2**2))*st2-2*(xg2*xt1**2-
     . xg2*xt1*xt2-xg2*xt2**2+xg2*xt2-xt1**3+xt1**2+xt1*xt2**2-xt1*
     . xt2+xt2**3-xt2**2)*(xg2-xt2)*(xt2-1)*xt2+ans8
      ans9=(log(xg2)-log(xt2))**2*(xg2-xt1)*(xg2-1)*(xt1-1)*st2
      ans6=ans7*ans9
      ans5=-ans6
      ans16=-(((2*((5*xt2-9)*xt1+7*(xt2-1)*xt2)*(xt2-1)*xt2**2-(xt2+1
     . -xt1)*(5*xt2-3)*xt1**3+(8*xt2**2-3*xt2-3)*xt1**2*xt2)*xt2-((
     . xt2+1-xt1)*(3*xt2-1)*xt1**2-2*(7*xt2-11)*(xt2-1)*xt2**2-(18*
     . xt2**2-25*xt2+9)*xt1*xt2)*xg2**2-(((xt2-2)*xt2+xt1**2)*(3*xt2-
     . 1)*xt1**2+4*(7*xt2-9)*(xt2-1)*xt2**3+(2*xt2**2-5*xt2+1)*xt1**3
     . +(28*xt2**2-51*xt2+25)*xt1*xt2**2)*xg2)*st2+(4*xg2*xt1**2-5*
     . xg2*xt1*xt2+xg2*xt1-7*xg2*xt2**2+7*xg2*xt2-4*xt1**3+4*xt1**2+5
     . *xt1*xt2**2-5*xt1*xt2+7*xt2**3-7*xt2**2)*(xg2-xt2)*(xt2-1)*xt2
     . )
      ans15=(((5*xt2-3)*xt1**4+7*(xt2-1)**2*xt2**3-3*(3*xt2**2-1)*xt1
     . **3+(5*xt2**2-26*xt2+19)*xt1*xt2**2+(16*xt2**2-5*xt2-5)*xt1**2
     . *xt2)*xt2-((5*xt2**2+2*xt2-1-(3*xt2-1)*xt1)*xt1**2-(7*xt2**2-
     . 28*xt2+19)*xt2**2-(19*xt2**2-17*xt2+4)*xt1*xt2)*xg2**2-(((5*
     . xt2-2)*(xt2-1)*xt2+(3*xt2-1)*xt1**2-(5*xt2-1)*xt1)*xt1**2+2*(7
     . *xt2**2-22*xt2+14)*xt2**3+(26*xt2**2-39*xt2+17)*xt1*xt2**2)*
     . xg2)*st2**2+ans16
      ans17=(xg2-1)*(xt1-1)
      ans14=ans15*ans17
      ans18=((xt1-xt2)*st2+xt2-1)**2*(xg2-xt1)*(xg2-xt2)**2*(xt1-xt2)
     . *log(xg2)*xt2
      ans13=ans14+ans18
      ans19=(log(xg2)-log(xt2))*(xg2-xt1)*st2
      ans12=2*ans13*ans19
      ans11=-ans12
      ans23=-(((3*(3*xt2-4)*xt2+5*xt1**2)*xt1+(10*xt2-13)*xt2**2+(18*
     . xt2-17)*xt1**2)*st2**2-((5*xt1**2+4*xt1*xt2+5*xt2**2)*(xt1+xt2
     . -2)*st2**3-2*(xt1-xt2)*(xt2-1)*xt1+(9*xt1**2+5*xt2**2)*(xt2-1)
     . *st2))*(xt1-1)*(xt2-1)*xg2**3-((2*xt1**3+xt2**2-2*(xt2+1)*xt1*
     . xt2+(2*xt2-1)*xt1**2-((xt1+2*xt2)*xt1-(xt2+2)*xt2)*xg2)*st2-(
     . xt1**2-2*xt1*xt2**2+xt2**2+(xt1**2-2*xt1+xt2**2)*xg2))*(st2-1)
     . *(xg2-xt2)**2*(xg2-1)*(xt2-1)**2*t134p(mt1,mt2,m2)*st2
      ans22=((((7*xt2-5)*xt2-(3*xt2-1)*xt1)*xt2-((5*xt2-3)*xt2-(xt2+1
     . )*xt1)*xg2)*st2+4*(xg2-xt2)*(xt2-1)*xt2)*(xg2-xt1)**2*(xg2-1)*
     . (xt1-1)**2*t134p(mt2,mt2,m2)*st2**2-(((st2-1)*(xg2+xt1)*t134p(
     . m2,mt1,m2)-(xg2+xt2)*t134p(m2,mt2,m2)*st2)*(xg2-xt2-(xt1-xt2)*
     . st2)**2*(xt1-1)**2*(xt2-1)**2-((st2-1)*(xt1+1)*t134p(mu,mt1,m2
     . )-(xt2+1)*t134p(mu,mt2,m2)*st2)*((xt1-xt2)*st2+xt2-1)**2*(xg2-
     . xt1)**2*(xg2-xt2)**2)*(xt1-xt2)+(((xt1+xt2)*(xt1-xt2)*(2*xt2-1
     . )-2*(xt2-1)*xt1*xt2-((xt1+xt2)*(xt1-xt2)-2*(xt2-1)*xt1)*xg2)*
     . st2-2*(xg2-xt2)*(xt1+xt2)*(xt2-1))*(st2-1)*(xg2-xt1)**2*(xg2-1
     . )*(xt1-1)**2*t134p(mt2,mt1,m2)*st2+(((7*xt1**2+xt2-(3*xt2+5)*
     . xt1)*xt1-(5*xt1**2-xt2-(xt2+3)*xt1)*xg2)*st2-((3*xt1-1)*xt1-(
     . xt1+1)*xg2)*(xt1-xt2))*(st2-1)**2*(xg2-xt2)**2*(xg2-1)*(xt2-1)
     . **2*t134p(mt1,mt1,m2)+ans23
      ans21=4*ans22*xg2
      ans20=-ans21
      ans28=-(2*xg2**2*xt1**3-2*xg2**2*xt1**2*xt2-2*xg2**2*xt1**2-2*
     . xg2**2*xt1*xt2**2+5*xg2**2*xt1*xt2-xg2**2*xt1+xg2**2*xt2**2-
     . xg2**2*xt2-4*xg2*xt1**4+xg2*xt1**3*xt2+7*xg2*xt1**3+5*xg2*xt1
     . **2*xt2**2-7*xg2*xt1**2*xt2-2*xg2*xt1**2+2*xg2*xt1*xt2**3-7*
     . xg2*xt1*xt2**2+5*xg2*xt1*xt2-xg2*xt2**3+xg2*xt2**2+2*xt1**5-4*
     . xt1**4-xt1**3*xt2**2+xt1**3*xt2+2*xt1**3-3*xt1**2*xt2**3+5*xt1
     . **2*xt2**2-2*xt1**2*xt2+2*xt1*xt2**3-2*xt1*xt2**2)*(xg2-xt2)*(
     . xt2-1)*xt2
      ans27=(((3*xt1-2)*(xt2-1)**2*xt2**3+(2*xt2-1)*(xt2+2)*xt1**3+(3
     . *xt2-2)*xt1**5-(xt2**2-2*xt2+2)*xt1**2*xt2**2-(xt2**2+6*xt2-4)
     . *xt1**4)*xt1*xt2-(xt1**3-2*xt1**2+xt1+xt2**3-2*xt2**2+xt2)*(2*
     . xt1*xt2-xt1-xt2)*xg2**3+(2*((2*xt2-1)*xt1**5-(xt2-1)**2*xt2**3
     . )+(3*xt2**2-12*xt2+4)*xt1**4-(2*xt2**3+4*xt2**2-11*xt2+2)*xt1
     . **3+(3*xt2**3-4*xt2**2+6*xt2-4)*xt1**2*xt2+(4*xt2**3-12*xt2**2
     . +11*xt2-4)*xt1*xt2**2)*xg2**2-(((2*xt2-5)*xt1-xt2)*(xt2-1)**2*
     . xt2**3+(2*xt2-1)*xt1**6+2*(3*xt2**2-6*xt2+2)*xt1**2*xt2**3+(6*
     . xt2**2-9*xt2+2)*xt1**5-(2*xt2**3-8*xt2**2-4*xt2+5)*xt1**3*xt2-
     . (2*xt2**3+12*xt2**2-12*xt2+1)*xt1**4)*xg2)*st2+ans28
      ans29=(log(xg2)-log(xt2))*(xg2-1)*st2
      ans26=ans27*ans29
      ans38=4*xg2**2*xt1**3*xt2**2-2*xg2**2*xt1**3*xt2-6*xg2**2*xt1**
     . 2*xt2**4+8*xg2**2*xt1**2*xt2**3-2*xg2**2*xt1**2*xt2**2+4*xg2**
     . 2*xt1**2*xt2-4*xg2**2*xt1**2+4*xg2**2*xt1*xt2**4-4*xg2**2*xt1*
     . xt2**3-4*xg2**2*xt1*xt2**2+4*xg2**2*xt1*xt2-8*xg2*xt1**4*xt2**
     . 3+8*xg2*xt1**4*xt2**2+8*xg2*xt1**4*xt2-8*xg2*xt1**4+8*xg2*xt1
     . **3*xt2**4-8*xg2*xt1**3*xt2**3-2*xg2*xt1**3*xt2**2-4*xg2*xt1**
     . 3*xt2+6*xg2*xt1**3-2*xg2*xt1**2*xt2**3+4*xg2*xt1**2*xt2**2-2*
     . xg2*xt1**2*xt2-4*xg2*xt1*xt2**4+8*xg2*xt1*xt2**3-4*xg2*xt1*xt2
     . **2+8*xt1**4*xt2**3-16*xt1**4*xt2**2+8*xt1**4*xt2-8*xt1**3*xt2
     . **4+10*xt1**3*xt2**3+4*xt1**3*xt2**2-6*xt1**3*xt2+6*xt1**2*xt2
     . **4-12*xt1**2*xt2**3+6*xt1**2*xt2**2
      ans37=27*st2*xg2*xt1**3*xt2-20*st2*xg2*xt1**3+5*st2*xg2*xt1**2*
     . xt2**5-5*st2*xg2*xt1**2*xt2**4-14*st2*xg2*xt1**2*xt2**3+23*st2
     . *xg2*xt1**2*xt2**2-9*st2*xg2*xt1**2*xt2-2*st2*xg2*xt1*xt2**4+4
     . *st2*xg2*xt1*xt2**3-2*st2*xg2*xt1*xt2**2-st2*xg2*xt2**5+2*st2*
     . xg2*xt2**4-st2*xg2*xt2**3-24*st2*xt1**4*xt2**3+48*st2*xt1**4*
     . xt2**2-24*st2*xt1**4*xt2+13*st2*xt1**3*xt2**4-6*st2*xt1**3*xt2
     . **3-27*st2*xt1**3*xt2**2+20*st2*xt1**3*xt2-5*st2*xt1**2*xt2**5
     . +3*st2*xt1**2*xt2**4+9*st2*xt1**2*xt2**3-7*st2*xt1**2*xt2**2+3
     . *st2*xt1*xt2**5-6*st2*xt1*xt2**4+3*st2*xt1*xt2**3-6*xg2**3*xt1
     . **3*xt2**2+12*xg2**3*xt1**3*xt2-6*xg2**3*xt1**3+6*xg2**3*xt1**
     . 2*xt2**3-8*xg2**3*xt1**2*xt2**2-2*xg2**3*xt1**2*xt2+4*xg2**3*
     . xt1**2-4*xg2**3*xt1*xt2**3+8*xg2**3*xt1*xt2**2-4*xg2**3*xt1*
     . xt2+8*xg2**2*xt1**4*xt2**2-16*xg2**2*xt1**4*xt2+8*xg2**2*xt1**
     . 4-2*xg2**2*xt1**3*xt2**3+ans38
      ans36=-2*st2*xg2**3*xt1**2*xt2**2+25*st2*xg2**3*xt1**2*xt2-16*
     . st2*xg2**3*xt1**2+3*st2*xg2**3*xt1*xt2**4-5*st2*xg2**3*xt1*xt2
     . **3+st2*xg2**3*xt1*xt2**2+st2*xg2**3*xt1*xt2-st2*xg2**3*xt2**4
     . +2*st2*xg2**3*xt2**3-st2*xg2**3*xt2**2-24*st2*xg2**2*xt1**4*
     . xt2**2+48*st2*xg2**2*xt1**4*xt2-24*st2*xg2**2*xt1**4-7*st2*xg2
     . **2*xt1**3*xt2**3+14*st2*xg2**2*xt1**3*xt2**2-7*st2*xg2**2*xt1
     . **3*xt2+2*st2*xg2**2*xt1**2*xt2**4+12*st2*xg2**2*xt1**2*xt2**3
     . -14*st2*xg2**2*xt1**2*xt2**2-16*st2*xg2**2*xt1**2*xt2+16*st2*
     . xg2**2*xt1**2-3*st2*xg2**2*xt1*xt2**5+5*st2*xg2**2*xt1*xt2**4-
     . 2*st2*xg2**2*xt1*xt2**3+st2*xg2**2*xt1*xt2**2-st2*xg2**2*xt1*
     . xt2+st2*xg2**2*xt2**5-st2*xg2**2*xt2**4-st2*xg2**2*xt2**3+st2*
     . xg2**2*xt2**2+24*st2*xg2*xt1**4*xt2**3-24*st2*xg2*xt1**4*xt2**
     . 2-24*st2*xg2*xt1**4*xt2+24*st2*xg2*xt1**4-13*st2*xg2*xt1**3*
     . xt2**4+13*st2*xg2*xt1**3*xt2**3-7*st2*xg2*xt1**3*xt2**2+ans37
      ans35=-5*st2**2*xg2*xt1**2*xt2**5+5*st2**2*xg2*xt1**2*xt2**4+12
     . *st2**2*xg2*xt1**2*xt2**3-29*st2**2*xg2*xt1**2*xt2**2+17*st2**
     . 2*xg2*xt1**2*xt2+2*st2**2*xg2*xt1*xt2**4-4*st2**2*xg2*xt1*xt2
     . **3+2*st2**2*xg2*xt1*xt2**2+st2**2*xg2*xt2**5-2*st2**2*xg2*xt2
     . **4+st2**2*xg2*xt2**3+7*st2**2*xt1**6*xt2-7*st2**2*xt1**6+5*
     . st2**2*xt1**5*xt2**2-19*st2**2*xt1**5*xt2+14*st2**2*xt1**5+16*
     . st2**2*xt1**4*xt2**3-42*st2**2*xt1**4*xt2**2+33*st2**2*xt1**4*
     . xt2-7*st2**2*xt1**4-9*st2**2*xt1**3*xt2**4+4*st2**2*xt1**3*xt2
     . **3+24*st2**2*xt1**3*xt2**2-19*st2**2*xt1**3*xt2+5*st2**2*xt1
     . **2*xt2**5-5*st2**2*xt1**2*xt2**4-5*st2**2*xt1**2*xt2**3+5*st2
     . **2*xt1**2*xt2**2-3*st2**2*xt1*xt2**5+6*st2**2*xt1*xt2**4-3*
     . st2**2*xt1*xt2**3+20*st2*xg2**3*xt1**3*xt2**2-40*st2*xg2**3*
     . xt1**3*xt2+20*st2*xg2**3*xt1**3-7*st2*xg2**3*xt1**2*xt2**3+
     . ans36
      ans34=26*st2**2*xg2**2*xt1**4*xt2**2-63*st2**2*xg2**2*xt1**4*
     . xt2+37*st2**2*xg2**2*xt1**4+5*st2**2*xg2**2*xt1**3*xt2**3-25*
     . st2**2*xg2**2*xt1**3*xt2**2+20*st2**2*xg2**2*xt1**3*xt2-12*st2
     . **2*xg2**2*xt1**2*xt2**3+12*st2**2*xg2**2*xt1**2*xt2**2+19*st2
     . **2*xg2**2*xt1**2*xt2-19*st2**2*xg2**2*xt1**2+3*st2**2*xg2**2*
     . xt1*xt2**5-5*st2**2*xg2**2*xt1*xt2**4+2*st2**2*xg2**2*xt1*xt2
     . **3+4*st2**2*xg2**2*xt1*xt2**2-4*st2**2*xg2**2*xt1*xt2-st2**2*
     . xg2**2*xt2**5+st2**2*xg2**2*xt2**4+st2**2*xg2**2*xt2**3-st2**2
     . *xg2**2*xt2**2-7*st2**2*xg2*xt1**6*xt2+7*st2**2*xg2*xt1**6-5*
     . st2**2*xg2*xt1**5*xt2**2+5*st2**2*xg2*xt1**5*xt2-16*st2**2*xg2
     . *xt1**4*xt2**3+16*st2**2*xg2*xt1**4*xt2**2+37*st2**2*xg2*xt1**
     . 4*xt2-37*st2**2*xg2*xt1**4+9*st2**2*xg2*xt1**3*xt2**4-9*st2**2
     . *xg2*xt1**3*xt2**3+20*st2**2*xg2*xt1**3*xt2**2-48*st2**2*xg2*
     . xt1**3*xt2+28*st2**2*xg2*xt1**3+ans35
      ans33=-2*log(xg2)*xg2*xt1**4*xt2+log(xg2)*xg2*xt1**4+log(xg2)*
     . xg2*xt1**3*xt2**3-2*log(xg2)*xg2*xt1**3*xt2**2+log(xg2)*xg2*
     . xt1**3*xt2-2*log(xg2)*xg2*xt1**2*xt2**4+4*log(xg2)*xg2*xt1**2*
     . xt2**3-2*log(xg2)*xg2*xt1**2*xt2**2-log(xg2)*xt1**4*xt2**3+2*
     . log(xg2)*xt1**4*xt2**2-log(xg2)*xt1**4*xt2+log(xg2)*xt1**3*xt2
     . **4-2*log(xg2)*xt1**3*xt2**3+log(xg2)*xt1**3*xt2**2-7*st2**2*
     . xg2**3*xt1**4*xt2+7*st2**2*xg2**3*xt1**4-19*st2**2*xg2**3*xt1
     . **3*xt2**2+47*st2**2*xg2**3*xt1**3*xt2-28*st2**2*xg2**3*xt1**3
     . +5*st2**2*xg2**3*xt1**2*xt2**3+12*st2**2*xg2**3*xt1**2*xt2**2-
     . 36*st2**2*xg2**3*xt1**2*xt2+19*st2**2*xg2**3*xt1**2-3*st2**2*
     . xg2**3*xt1*xt2**4+5*st2**2*xg2**3*xt1*xt2**3-6*st2**2*xg2**3*
     . xt1*xt2**2+4*st2**2*xg2**3*xt1*xt2+st2**2*xg2**3*xt2**4-2*st2
     . **2*xg2**3*xt2**3+st2**2*xg2**3*xt2**2+14*st2**2*xg2**2*xt1**5
     . *xt2-14*st2**2*xg2**2*xt1**5+ans34
      ans32=-6*log(xg2)*st2*xg2**2*xt1**3*xt2-2*log(xg2)*st2*xg2**2*
     . xt1*xt2**4+2*log(xg2)*st2*xg2**2*xt1*xt2**3+2*log(xg2)*st2*xg2
     . *xt1**5*xt2-2*log(xg2)*st2*xg2*xt1**5-6*log(xg2)*st2*xg2*xt1**
     . 3*xt2**3+6*log(xg2)*st2*xg2*xt1**3*xt2**2+4*log(xg2)*st2*xg2*
     . xt1**2*xt2**4-4*log(xg2)*st2*xg2*xt1**2*xt2**3-2*log(xg2)*st2*
     . xt1**5*xt2**2+2*log(xg2)*st2*xt1**5*xt2+4*log(xg2)*st2*xt1**4*
     . xt2**3-4*log(xg2)*st2*xt1**4*xt2**2-2*log(xg2)*st2*xt1**3*xt2
     . **4+2*log(xg2)*st2*xt1**3*xt2**3+log(xg2)*xg2**3*xt1**2*xt2**2
     . -2*log(xg2)*xg2**3*xt1**2*xt2+log(xg2)*xg2**3*xt1**2-log(xg2)*
     . xg2**3*xt1*xt2**3+2*log(xg2)*xg2**3*xt1*xt2**2-log(xg2)*xg2**3
     . *xt1*xt2-2*log(xg2)*xg2**2*xt1**3*xt2**2+4*log(xg2)*xg2**2*xt1
     . **3*xt2-2*log(xg2)*xg2**2*xt1**3+log(xg2)*xg2**2*xt1**2*xt2**3
     . -2*log(xg2)*xg2**2*xt1**2*xt2**2+log(xg2)*xg2**2*xt1**2*xt2+
     . log(xg2)*xg2**2*xt1*xt2**4-2*log(xg2)*xg2**2*xt1*xt2**3+log(
     . xg2)*xg2**2*xt1*xt2**2+log(xg2)*xg2*xt1**4*xt2**2+ans33
      ans31=log(xg2)*st2**2*xg2**3*xt1**4-3*log(xg2)*st2**2*xg2**3*
     . xt1**3*xt2+3*log(xg2)*st2**2*xg2**3*xt1**2*xt2**2-log(xg2)*st2
     . **2*xg2**3*xt1*xt2**3-2*log(xg2)*st2**2*xg2**2*xt1**5+5*log(
     . xg2)*st2**2*xg2**2*xt1**4*xt2-3*log(xg2)*st2**2*xg2**2*xt1**3*
     . xt2**2-log(xg2)*st2**2*xg2**2*xt1**2*xt2**3+log(xg2)*st2**2*
     . xg2**2*xt1*xt2**4+log(xg2)*st2**2*xg2*xt1**6-log(xg2)*st2**2*
     . xg2*xt1**5*xt2-3*log(xg2)*st2**2*xg2*xt1**4*xt2**2+5*log(xg2)*
     . st2**2*xg2*xt1**3*xt2**3-2*log(xg2)*st2**2*xg2*xt1**2*xt2**4-
     . log(xg2)*st2**2*xt1**6*xt2+3*log(xg2)*st2**2*xt1**5*xt2**2-3*
     . log(xg2)*st2**2*xt1**4*xt2**3+log(xg2)*st2**2*xt1**3*xt2**4+2*
     . log(xg2)*st2*xg2**3*xt1**3*xt2-2*log(xg2)*st2*xg2**3*xt1**3-4*
     . log(xg2)*st2*xg2**3*xt1**2*xt2**2+4*log(xg2)*st2*xg2**3*xt1**2
     . *xt2+2*log(xg2)*st2*xg2**3*xt1*xt2**3-2*log(xg2)*st2*xg2**3*
     . xt1*xt2**2-4*log(xg2)*st2*xg2**2*xt1**4*xt2+4*log(xg2)*st2*xg2
     . **2*xt1**4+6*log(xg2)*st2*xg2**2*xt1**3*xt2**2+ans32
      ans39=(xg2-xt2)
      ans30=ans31*ans39
      ans25=ans26+ans30
      ans40=(log(xg2)-log(xt1))*(st2-1)
      ans24=2*ans25*ans40
      ans10=-(((2*((xt2-2+xt1)*xt1**4-(xt2-1)*xt2**3)+(3*xt2+8)*(xt2-
     . 1)*xt1*xt2**2-2*(6*xt2**2+xt2-8)*xt1**2*xt2+(17*xt2**2-21*xt2+
     . 2)*xt1**3)*xt1-((xt2-1)*xt2**2-2*xt1**4-2*(8*xt2-9)*xt1**3-2*(
     . xt2**2+xt2-1)*xt1*xt2+(8*xt2**2+7*xt2-13)*xt1**2)*xg2**2+((xt2
     . -1)*xt2**3-4*xt1**5-2*(xt2+1)*(xt2-1)*xt1*xt2**2+(5*xt2-7)*(
     . xt2+1)*xt1**2*xt2-(21*xt2-25)*xt1**4-2*(xt2**2-12*xt2+9)*xt1**
     . 3)*xg2)*st2**2-((22*xg2*xt1**3-14*xg2*xt1**2*xt2-16*xg2*xt1**2
     . +2*xg2*xt1*xt2**2+7*xg2*xt1*xt2-xg2*xt2**2-28*xt1**4+21*xt1**3
     . *xt2+22*xt1**3-3*xt1**2*xt2**2-14*xt1**2*xt2+2*xt1*xt2**2)*st2
     . -(8*xg2*xt1-5*xg2-11*xt1**2+8*xt1)*(xt1-xt2)*xt1)*(xg2-xt2)*(
     . xt2-1))*(log(xg2)-log(xt1))**2*(st2-1)*(xg2-xt2)*(xg2-1)*(xt2-
     . 1)+ans11+ans20+ans24
      ans4=4*(((16*xt2+5+5*xt1)*xt1**4+(10*xt2**2+10*xt2-23)*xt2**3+(
     . 26*xt2**2-7*xt2-34)*xt1*xt2**2+(30*xt2**2+3*xt2-47)*xt1**2*xt2
     . +(39*xt2**2-11*xt2-22)*xt1**3)*st2**2-((xt1**3+2*xt1**2*xt2+
     . xt1**2+2*xt1*xt2**2-2*xt1*xt2-3*xt1+xt2**3+xt2**2-3*xt2)*(5*
     . xt1**2+4*xt1*xt2+5*xt2**2)*st2**3-2*(2*xt1*xt2+xt1+xt2**2+2*
     . xt2)*(xt1-xt2)*(xt2-1)*xt1+((2*xt2+1)*xt1+(xt2+2)*xt2)*(9*xt1
     . **2+5*xt2**2)*(xt2-1)*st2))*(xt1-1)*(xt2-1)*xg2**2+ans5+ans10
      ans3=-4*((5*((xt2+1)*xt1**5+2*(xt2-1)*xt2**4)+3*(2*xt2**2+7*xt2
     . -13)*xt1**2*xt2**2+2*(5*xt2**2+8*xt2-16)*xt1*xt2**3+(6*xt2**2+
     . 11*xt2-5)*xt1**4+(15*xt2**2+21*xt2-40)*xt1**3*xt2)*st2**2-((
     . xt1**3*xt2+xt1**3+xt1**2*xt2-xt1**2+xt1*xt2**3+xt1*xt2**2-4*
     . xt1*xt2+xt2**3-xt2**2)*(5*xt1**2+4*xt1*xt2+5*xt2**2)*st2**3-2*
     . (xt1*xt2+2*xt1+xt2)*(xt1-xt2)*(xt2-1)*xt1*xt2+((xt2+2)*xt1+xt2
     . )*(9*xt1**2+5*xt2**2)*(xt2-1)*st2*xt2))*(xt1-1)*(xt2-1)*xg2+
     . ans4
      ans2=4*((5*(2*(xt2-1)*xt2**3+xt1**4)+3*(2*xt2-3)*xt1*xt2**2+3*(
     . 5*xt2-6)*xt1**2*xt2+(6*xt2-5)*xt1**3)*st2**2-((5*xt1**2+4*xt1*
     . xt2+5*xt2**2)*(xt1**2-xt1+xt2**2-xt2)*st2**3-2*(xt1-xt2)*(xt2-
     . 1)*xt1*xt2+(9*xt1**2+5*xt2**2)*(xt2-1)*st2*xt2))*(xt1-1)*(xt2-
     . 1)*xt1*xt2+((xt1-xt2)*st2+xt2-1)**2*((xt1-xt2)*st2-xt1)*(log(
     . xg2)+4)*(xg2-xt1)**2*(xg2-xt2)**2*(xt1-xt2)*log(xg2)-4*(((29*
     . xt2-17+10*xt1)*xt1**3+(20*xt2**2-13*xt2-13)*xt2**2+(25*xt2**2-
     . 25*xt2-12)*xt1*xt2+(42*xt2**2-29*xt2-17)*xt1**2)*st2**2-(2*((5
     . *xt1**2+4*xt1*xt2+5*xt2**2)*(xt1**2+xt1*xt2-xt1+xt2**2-xt2-1)*
     . st2**3-(xt1+2*xt2+1)*(xt1-xt2)*(xt2-1)*xt1)+(2*xt2+1+xt1)*(9*
     . xt1**2+5*xt2**2)*(xt2-1)*st2))*(xt1-1)*(xt2-1)*xg2**3+ans3
      ans1=ans2*xg2
      r722=ans1/(8*(xg2-xt1)**2*(xg2-xt2)**2*(xg2-1)*(xt1-xt2)*(xt1-1
     . )**2*(xt2-1)**2)

      ans13=-(2*xg2**2*xt1**3-2*xg2**2*xt1**2*xt2-2*xg2**2*xt1**2-2*
     . xg2**2*xt1*xt2**2+5*xg2**2*xt1*xt2-xg2**2*xt1+xg2**2*xt2**2-
     . xg2**2*xt2-4*xg2*xt1**4+xg2*xt1**3*xt2+7*xg2*xt1**3+5*xg2*xt1
     . **2*xt2**2-7*xg2*xt1**2*xt2-2*xg2*xt1**2+2*xg2*xt1*xt2**3-7*
     . xg2*xt1*xt2**2+5*xg2*xt1*xt2-xg2*xt2**3+xg2*xt2**2+2*xt1**5-4*
     . xt1**4-xt1**3*xt2**2+xt1**3*xt2+2*xt1**3-3*xt1**2*xt2**3+5*xt1
     . **2*xt2**2-2*xt1**2*xt2+2*xt1*xt2**3-2*xt1*xt2**2)*(xg2-xt2)*(
     . xt2-1)*xt2
      ans12=(((3*xt1-2)*(xt2-1)**2*xt2**3+(2*xt2-1)*(xt2+2)*xt1**3+(3
     . *xt2-2)*xt1**5-(xt2**2-2*xt2+2)*xt1**2*xt2**2-(xt2**2+6*xt2-4)
     . *xt1**4)*xt1*xt2-(xt1**3-2*xt1**2+xt1+xt2**3-2*xt2**2+xt2)*(2*
     . xt1*xt2-xt1-xt2)*xg2**3+(2*((2*xt2-1)*xt1**5-(xt2-1)**2*xt2**3
     . )+(3*xt2**2-12*xt2+4)*xt1**4-(2*xt2**3+4*xt2**2-11*xt2+2)*xt1
     . **3+(3*xt2**3-4*xt2**2+6*xt2-4)*xt1**2*xt2+(4*xt2**3-12*xt2**2
     . +11*xt2-4)*xt1*xt2**2)*xg2**2-(((2*xt2-5)*xt1-xt2)*(xt2-1)**2*
     . xt2**3+(2*xt2-1)*xt1**6+2*(3*xt2**2-6*xt2+2)*xt1**2*xt2**3+(6*
     . xt2**2-9*xt2+2)*xt1**5-(2*xt2**3-8*xt2**2-4*xt2+5)*xt1**3*xt2-
     . (2*xt2**3+12*xt2**2-12*xt2+1)*xt1**4)*xg2)*st2+ans13
      ans14=(log(xg2)-log(xt2))*(xg2-1)
      ans11=ans12*ans14
      ans10=-ans11
      ans9=(((((xt2-1)*xt2**3-14*xt1**5-(3*xt2-2)*(xt2-1)*xt1*xt2**2-
     . (5*xt2-4)*(xt2-7)*xt1**3+(7*xt2-17)*xt1**2*xt2-2*(13*xt2-22)*
     . xt1**4-((xt2-1)*xt2**2-7*xt1**4-(19*xt2-28)*xt1**3-(3*xt2**2-2
     . *xt2+4)*xt1*xt2+(5*xt2**2+17*xt2-19)*xt1**2)*xg2)*xg2-(3*(xt2-
     . 1)*xt2**3-7*xt1**5-5*(xt2+1)*(xt2-1)*xt1*xt2**2-(5*xt2-14)*xt1
     . **4+(9*xt2**2+5*xt2-19)*xt1**2*xt2-(16*xt2**2-26*xt2+7)*xt1**3
     . )*xt1)*st2-(20*xg2*xt1**3-7*xg2*xt1**2*xt2-16*xg2*xt1**2+3*xg2
     . *xt1*xt2**2+xg2*xt1*xt2-xg2*xt2**2-24*xt1**4+13*xt1**3*xt2+20*
     . xt1**3-5*xt1**2*xt2**2-7*xt1**2*xt2+3*xt1*xt2**2)*(xg2-xt2)*(
     . xt2-1))*(xg2-1)*(xt2-1)-((xt1-xt2)*st2+2*(xt2-1))*(xg2-xt1)**2
     . *(xg2-xt2)*(xt1-xt2)**2*log(xg2)*xt1)*(xg2-xt2)+ans10
      ans15=(log(xg2)-log(xt1))
      ans8=2*ans9*ans15
      ans7=2*(((((5*xt2-3)*xt1**4+7*(xt2-1)**2*xt2**3-3*(3*xt2**2-1)*
     . xt1**3+(5*xt2**2-26*xt2+19)*xt1*xt2**2+(16*xt2**2-5*xt2-5)*xt1
     . **2*xt2)*xt2-((5*xt2**2+2*xt2-1-(3*xt2-1)*xt1)*xt1**2-(7*xt2**
     . 2-28*xt2+19)*xt2**2-(19*xt2**2-17*xt2+4)*xt1*xt2)*xg2**2-(((5*
     . xt2-2)*(xt2-1)*xt2+(3*xt2-1)*xt1**2-(5*xt2-1)*xt1)*xt1**2+2*(7
     . *xt2**2-22*xt2+14)*xt2**3+(26*xt2**2-39*xt2+17)*xt1*xt2**2)*
     . xg2)*st2+((2*(((xt1-xt2)*xt1+xt2**2-6*xt2+4)*xt1+(7*xt2**2-10*
     . xt2+4)*xt2)*xt2+((xt2**2+8*xt2-5-2*xt1*xt2)*xt1-(7*xt2**2-8*
     . xt2+3)*xt2)*xg2)*xg2-(2*(2*xt2-1)*xt1**3+7*(xt2-1)**2*xt2**2-2
     . *(4*xt2**2-xt2-1)*xt1**2+(5*xt2**2-2*xt2-1)*xt1*xt2)*xt2)*xt2)
     . *(xg2-1)*(xt1-1)+(xt2-2+xt1+(xt1-xt2)*st2)*(xg2-xt1)*(xg2-xt2)
     . **2*(xt1-xt2)**2*log(xg2)*xt2)*(log(xg2)-log(xt2))*(xg2-xt1)+
     . ans8
      ans6=(((2*((xt2-2+xt1)*xt1**4-(xt2-1)*xt2**3)+(3*xt2+8)*(xt2-1)
     . *xt1*xt2**2-2*(6*xt2**2+xt2-8)*xt1**2*xt2+(17*xt2**2-21*xt2+2)
     . *xt1**3)*xt1-((xt2-1)*xt2**2-2*xt1**4-2*(8*xt2-9)*xt1**3-2*(
     . xt2**2+xt2-1)*xt1*xt2+(8*xt2**2+7*xt2-13)*xt1**2)*xg2**2+((xt2
     . -1)*xt2**3-4*xt1**5-2*(xt2+1)*(xt2-1)*xt1*xt2**2+(5*xt2-7)*(
     . xt2+1)*xt1**2*xt2-(21*xt2-25)*xt1**4-2*(xt2**2-12*xt2+9)*xt1**
     . 3)*xg2)*st2-(22*xg2*xt1**3-14*xg2*xt1**2*xt2-16*xg2*xt1**2+2*
     . xg2*xt1*xt2**2+7*xg2*xt1*xt2-xg2*xt2**2-28*xt1**4+21*xt1**3*
     . xt2+22*xt1**3-3*xt1**2*xt2**2-14*xt1**2*xt2+2*xt1*xt2**2)*(xg2
     . -xt2)*(xt2-1))*(log(xg2)-log(xt1))**2*(xg2-xt2)*(xg2-1)*(xt2-1
     . )+ans7
      ans5=((((3*xt2-2)*xt1**4+2*(xt2-1)**2*xt2**3-(4*xt2+1)*(3*xt2-2
     . )*xt1**3+(2*xt2**2-21*xt2+16)*xt1*xt2**2+(17*xt2**2-2*xt2-8)*
     . xt1**2*xt2)*xt2-((4*xt2+1-xt1)*(2*xt2-1)*xt1**2-(2*xt2**2-18*
     . xt2+13)*xt2**2-(16*xt2**2-7*xt2-2)*xt1*xt2)*xg2**2-((2*(xt2**2
     . +xt2-1)*xt2+(2*xt2-1)*xt1**2)*xt1**2+(4*xt2**2-25*xt2+18)*xt2
     . **3-(5*xt2**2-1)*xt1**3+(21*xt2**2-24*xt2+7)*xt1*xt2**2)*xg2)*
     . st2+(((6*xt1*xt2-3*xt1+xt2**2-7*xt2+3)*xt1**2+(4*xt2**2+3*xt2-
     . 4)*xt2**2-(7*xt2**2+xt2-5)*xt1*xt2-((2*xt2**2+4*xt2-3)*xt2+3*(
     . 2*xt2-1)*xt1**2-(6*xt2**2+5*xt2-5)*xt1)*xg2)*xg2-(3*(3*xt2-2)*
     . xt1**3+2*(xt2-1)**2*xt2**2+(2*xt2**2+7*xt2-6)*xt1*xt2-(11*xt2
     . **2+xt2-6)*xt1**2)*xt2)*xt2)*(log(xg2)-log(xt2))**2*(xg2-xt1)*
     . (xg2-1)*(xt1-1)+ans6
      ans4=-4*(((5*xt2**2+5*xt2-8)*xt2**2+2*xt1**4+(7*xt2**2+xt2-20)*
     . xt1**2+(12*xt2**2-xt2-7)*xt1*xt2)*xt2+(16*xt2**2-5*xt2-7)*xt1
     . **3-(xt1**3+2*xt1**2*xt2+xt1**2+2*xt1*xt2**2-2*xt1*xt2-3*xt1+
     . xt2**3+xt2**2-3*xt2)*(5*xt1**2+4*xt1*xt2+5*xt2**2)*st2)*(xt1-1
     . )*(xt2-1)*xg2**2+4*((((xt1+xt2-2*xg2+(xt1-xt2)*st2)*(xg2+xt2)*
     . t134p(m2,mt2,m2)+(2*(xg2-xt2)-(xt1-xt2)*st2)*(xg2+xt1)*t134p(
     . m2,mt1,m2))*(xt1-1)**2*(xt2-1)**2-((xt2-2+xt1+(xt1-xt2)*st2)*(
     . xt2+1)*t134p(mu,mt2,m2)-((xt1-xt2)*st2+2*(xt2-1))*(xt1+1)*
     . t134p(mu,mt1,m2))*(xg2-xt1)**2*(xg2-xt2)**2)*(xt1-xt2)**2-(((5
     . *xt2-3)*xt2-4*xt1)*xt2+(9*xt2-7)*xt1**2-(5*xt1**2+4*xt1*xt2+5*
     . xt2**2)*(xt1+xt2-2)*st2)*(xt1-1)*(xt2-1)*xg2**3)*xg2+ans5
      ans3=4*(((7*xt2**2-7*xt2-4)*xt2+(11*xt2-7)*xt1**2)*xt1+(10*xt2
     . **2-3*xt2-3)*xt2**2+(14*xt2**2-11*xt2-7)*xt1**2-2*(5*xt1**2+4*
     . xt1*xt2+5*xt2**2)*(xt1**2+xt1*xt2-xt1+xt2**2-xt2-1)*st2)*(xt1-
     . 1)*(xt2-1)*xg2**3-4*((2*xt1**3+xt2**2-2*(xt2+1)*xt1*xt2+(2*xt2
     . -1)*xt1**2-((xt1+2*xt2)*xt1-(xt2+2)*xt2)*xg2)*st2-(xt1**2-2*
     . xt1*xt2**2+xt2**2+(xt1**2-2*xt1+xt2**2)*xg2))*(xg2-xt2)**2*(
     . xg2-1)*(xt2-1)**2*t134p(mt1,mt2,m2)*xg2+4*((2*(xt2+1)*xt1**4+5
     . *(xt2-1)*xt2**3+(2*xt2**2+7*xt2-13)*xt1**2*xt2+(5*xt2**2+7*xt2
     . -16)*xt1**3+(5*xt2**2+7*xt2-8)*xt1*xt2**2)*xt2-(xt1**3*xt2+xt1
     . **3+xt1**2*xt2-xt1**2+xt1*xt2**3+xt1*xt2**2-4*xt1*xt2+xt2**3-
     . xt2**2)*(5*xt1**2+4*xt1*xt2+5*xt2**2)*st2)*(xt1-1)*(xt2-1)*xg2
     . +ans4
      ans2=(4*((((7*xt2-5)*xt2-(3*xt2-1)*xt1)*xt2-((5*xt2-3)*xt2-(xt2
     . +1)*xt1)*xg2)*st2-((3*xt2-1)*xt2-(xt2+1)*xg2)*(xt1-xt2))*(xg2-
     . 1)*(xt1-1)**2*t134p(mt2,mt2,m2)*xg2-((xt1-xt2)*st2+xt2-2)*(log
     . (xg2)+4)*(xg2-xt2)**2*(xt1-xt2)**3*log(xg2)+4*(((xt1+xt2)*(xt1
     . -xt2)*(2*xt2-1)-2*(xt2-1)*xt1*xt2-((xt1+xt2)*(xt1-xt2)-2*(xt2-
     . 1)*xt1)*xg2)*st2-2*(xg2-xt2)*(xt1+xt2)*(xt2-1))*(xg2-1)*(xt1-1
     . )**2*t134p(mt2,mt1,m2)*xg2)*(xg2-xt1)**2-4*((2*(xt1**2+xt2**2)
     . *xt1+5*(xt2-1)*xt2**2+(5*xt2-9)*xt1**2)*xt2-(5*xt1**2+4*xt1*
     . xt2+5*xt2**2)*(xt1**2-xt1+xt2**2-xt2)*st2)*(xt1-1)*(xt2-1)*xt1
     . *xt2+4*(((7*xt1**2+xt2-(3*xt2+5)*xt1)*xt1-(5*xt1**2-xt2-(xt2+3
     . )*xt1)*xg2)*st2-2*((5*xt1**2+xt2-3*(xt2+1)*xt1)*xt1-(3*xt1**2-
     . xt2-(xt2+1)*xt1)*xg2))*(xg2-xt2)**2*(xg2-1)*(xt2-1)**2*t134p(
     . mt1,mt1,m2)*xg2+ans3
      ans16=(st2-1)*st2*xg2
      ans1=ans2*ans16
      r72p2=ans1/(8*(xg2-xt1)**2*(xg2-xt2)**2*(xg2-1)*(xt1-xt2)*(xt1-
     . 1)**2*(xt2-1)**2)

      r722 = r722 + r72p2

      r72=r712+r722

c--r8
      ans6=(2*(2*((((2*xgl+1)*xg2+2*xgl+(xgl+1+xg2)*xb2)*xb1**2+xb1**
     . 4-xb2*xg2*xgl-(xb2+xgl)*xb1*xg2-(3*xgl+1+xg2+xb2)*xb1**3)*sb2-
     . (xb1**3-xb1**2*xg2-xb1**2*xgl-xb1**2+xb1*xg2+xg2*xgl)*(xb1-xb2
     . ))+((2*(xb1**3+xb2*xg2)-(xb1+xb2)*(xg2+1)*xb1)*sb2-(xb1*xg2+
     . xb1-2*xg2)*(xb1-xb2))*log(xgl)*xgl-((2*(xb1**3+xb2*xg2)-(xb1+
     . xb2)*(xg2+1)*xb1)*sb2-(xb1*xg2+xb1-2*xg2)*(xb1-xb2))*log(xg2)*
     . xgl)+((2*(xb1**3+xb2*xg2)-(xb1+xb2)*(xg2+1)*xb1)*sb2-(xb1*xg2+
     . xb1-2*xg2)*(xb1-xb2))*(log(xb1)-log(xg2))*xgl)*(log(xb1)-log(
     . xg2))*(sb2-1)*(xb2-xg2)**2*(xb2-1)**2*(xg2-1)
      ans5=2*(((2*(xb2**3-xg2*xgl)+3*(xg2+1)*xb2*xgl-(4*xgl+1+xg2)*
     . xb2**2+((2*xgl-1-xg2)*xb2-((xgl-2)*xg2+xgl))*xb1)*sb2-2*(xb2-
     . xg2)*(xb2-xgl)*(xb2-1))*(xb1-xg2)**2*(xb1-1)**2*(xg2-1)*t134p(
     . mb2,mg,m2)*sb2+((((2*xgl-3)*xb2-4*xgl+(2*xgl-3+6*xb2)*xb1)*sb2
     . **2-(2*sb2-1)*(3*xb1+2*xgl)*(xb2-1))*(xb1-1)*(xb2-1)*xg2**3+((
     . xb1-xb2)*sb2+xb2-xg2)**2*(xb1-1)**2*(xb2-1)**2*(xg2-xgl)*t134p
     . (m2,mg,m2)+((xb1-xb2)*sb2+xb2-1)**2*(xb1-xg2)**2*(xb2-xg2)**2*
     . (xgl-1)*t134p(mu,mg,m2))*(xb1-xb2)+(((4*xgl+1+xg2-2*xb1)*xb1**
     . 2+((xgl-2)*xg2+xgl)*xb2+2*xg2*xgl-((2*xgl-1-xg2)*xb2+3*(xg2+1)
     . *xgl)*xb1)*sb2+(xb1*xg2-2*xb1*xgl+xb1+xg2*xgl-2*xg2+xgl)*(xb1-
     . xb2))*(sb2-1)*(xb2-xg2)**2*(xb2-1)**2*(xg2-1)*t134p(mb1,mg,m2)
     . )*xg2+ans6
      ans4=-2*(2*(((((2*xgl+1)*xg2+2*xgl)*xb2+xb2**3-xg2*xgl-(3*xgl+1
     . +xg2)*xb2**2)*xb2+((xgl+1+xg2)*xb2**2-(xb2**3+xb2*xg2+xg2*xgl)
     . )*xb1)*sb2+2*(xb2-xg2)*(xb2-1)*xb2*xgl)+((((xg2+1)*xb2-2*xg2)*
     . xb1+(xg2+1-2*xb2)*xb2**2)*sb2+2*(xb2-xg2)*(xb2-1)*xb2)*(log(
     . xg2)-log(xgl))*xgl)*(log(xb2)-log(xg2))*(xb1-xg2)**2*(xb1-1)**
     . 2*(xg2-1)*sb2+ans5
      ans3=-2*(((3*xb2+2*xgl)*(xb2+1)*xb1**3+2*(xb2-1)*xb2**2*xgl+(3*
     . xb2**2+9*xb2+2*xgl)*(xb2-1)*xb1**2+((2*xgl-9)*xb2-8*xgl+(2*xgl
     . +3)*xb2**2)*xb1*xb2)*sb2**2-(2*sb2-1)*(xb1*xb2+2*xb1+xb2)*(3*
     . xb1+2*xgl)*(xb2-1)*xb2)*(xb1-xb2)*(xb1-1)*(xb2-1)*xg2+2*(((2*(
     . xb2**2-3)*xgl+(2*xgl-3)*xb2)*xb2+((6*xb2+2*xgl-3)*(2*xb2+1)+(3
     . *xb2+2*xgl)*xb1)*xb1**2+(3*xb2**3+4*xb2**2*xgl-6*xgl-4*(xgl+3)
     . *xb2)*xb1)*sb2**2-(2*sb2-1)*(2*xb1*xb2+xb1+xb2**2+2*xb2)*(3*
     . xb1+2*xgl)*(xb2-1))*(xb1-xb2)*(xb1-1)*(xb2-1)*xg2**2-2*(2*((
     . xb2**2+2*xg2-(xg2+1)*xb2-(xg2+1-xb1)*xb1)*sb2**2-(2*sb2-1)*(
     . xb2-xg2)*(xb2-1))*(xb1-1)*(xb2-1)*(xg2-1)-((xb1-xb2)*sb2+xb2-1
     . )**2*(xb1-xg2)*(xb2-xg2)*log(xg2))*(log(xg2)-log(xgl))*(xb1-
     . xb2)*(xb1-xg2)*(xb2-xg2)*xgl+ans4
      ans2=(((((xg2+1)*xb2-2*xg2)*xb1+(xg2+1-2*xb2)*xb2**2)*sb2+2*(
     . xb2-xg2)*(xb2-1)*xb2)*(log(xb2)-log(xg2))**2*(xb1-1)**2*(xg2-1
     . )*sb2+((xb1-xb2)*sb2+xb2-1)**2*(log(xg2)+4)*(xb1-xb2)*(xb2-xg2
     . )**2*log(xg2))*(xb1-xg2)**2*xgl+2*(((3*xb2+2*xgl)*xb1**2+2*(
     . xb2-1)*xb2*xgl+(3*xb2**2-6*xb2-2*xgl)*xb1)*sb2**2-(2*sb2-1)*(3
     . *xb1+2*xgl)*(xb2-1)*xb2)*(xb1-xb2)*(xb1-1)*(xb2-1)*xb1*xb2-((
     . xb2**2+2*xg2-(xg2+1)*xb2-(xg2+1-xb1)*xb1)*sb2**2-(2*sb2-1)*(
     . xb2-xg2)*(xb2-1))*(log(xg2)-log(xgl))**2*(xb1-xb2)*(xb1-xg2)*(
     . xb1-1)*(xb2-xg2)*(xb2-1)*(xg2-1)*xgl-2*(((4*xgl-3)*xb2**2-4*
     . xgl-(4*xgl+3)*xb2+((4*xgl-3+9*xb2)*xb1+(9*xb2+4*xgl+3)*(xb2-1)
     . )*xb1)*sb2**2-(2*sb2-1)*(3*xb1+2*xgl)*(xb1+2*xb2+1)*(xb2-1))*(
     . xb1-xb2)*(xb1-1)*(xb2-1)*xg2**3+ans3
      ans1=ans2*xg2
      r812=ans1/(8*(xb1-xb2)*(xb1-xg2)**2*(xb1-1)**2*(xb2-xg2)**2*(
     . xb2-1)**2*(xg2-1))

      ans6=(2*(2*(((2*xgl+1)*xg2+2*xgl+(xgl+1+xg2)*xb2)*xb1**2+xb1**4
     . -xb2*xg2*xgl-(xb2+xgl)*xb1*xg2-(3*xgl+1+xg2+xb2)*xb1**3)+(2*(
     . xb1**3+xb2*xg2)-(xb1+xb2)*(xg2+1)*xb1)*log(xgl)*xgl-(2*(xb1**3
     . +xb2*xg2)-(xb1+xb2)*(xg2+1)*xb1)*log(xg2)*xgl)+(2*(xb1**3+xb2*
     . xg2)-(xb1+xb2)*(xg2+1)*xb1)*(log(xb1)-log(xg2))*xgl)*(log(xb1)
     . -log(xg2))*(xb2-xg2)**2*(xb2-1)**2*(xg2-1)
      ans5=2*((2*(xb2**3-xg2*xgl)+3*(xg2+1)*xb2*xgl-(4*xgl+1+xg2)*xb2
     . **2+((2*xgl-1-xg2)*xb2-((xgl-2)*xg2+xgl))*xb1)*(xb1-xg2)**2*(
     . xb1-1)**2*(xg2-1)*t134p(mb2,mg,m2)+(((2*xgl-3)*xb2-4*xgl+(2*
     . xgl-3+6*xb2)*xb1)*(xb1-1)*(xb2-1)*xg2**3+((xb1-xg2)**2*(xb2-
     . xg2)**2*(xgl-1)*t134p(mu,mg,m2)+(xb1-1)**2*(xb2-1)**2*(xg2-xgl
     . )*t134p(m2,mg,m2))*(xb1-xb2)**2)*(xb1-xb2))*xg2-2*(2*((((2*xgl
     . +1)*xg2+2*xgl)*xb2+xb2**3-xg2*xgl-(3*xgl+1+xg2)*xb2**2)*xb2+((
     . xgl+1+xg2)*xb2**2-(xb2**3+xb2*xg2+xg2*xgl))*xb1)+(((xg2+1)*xb2
     . -2*xg2)*xb1+(xg2+1-2*xb2)*xb2**2)*(log(xg2)-log(xgl))*xgl)*(
     . log(xb2)-log(xg2))*(xb1-xg2)**2*(xb1-1)**2*(xg2-1)+ans6
      ans4=2*((2*(xb2**2-3)*xgl+(2*xgl-3)*xb2)*xb2+((6*xb2+2*xgl-3)*(
     . 2*xb2+1)+(3*xb2+2*xgl)*xb1)*xb1**2+(3*xb2**3+4*xb2**2*xgl-6*
     . xgl-4*(xgl+3)*xb2)*xb1)*(xb1-xb2)*(xb1-1)*(xb2-1)*xg2**2-2*(2*
     . (xb2**2+2*xg2-(xg2+1)*xb2-(xg2+1-xb1)*xb1)*(xb1-1)*(xb2-1)*(
     . xg2-1)-(xb1-xb2)**2*(xb1-xg2)*(xb2-xg2)*log(xg2))*(log(xg2)-
     . log(xgl))*(xb1-xb2)*(xb1-xg2)*(xb2-xg2)*xgl+2*((4*xgl+1+xg2-2*
     . xb1)*xb1**2+((xgl-2)*xg2+xgl)*xb2+2*xg2*xgl-((2*xgl-1-xg2)*xb2
     . +3*(xg2+1)*xgl)*xb1)*(xb2-xg2)**2*(xb2-1)**2*(xg2-1)*t134p(mb1
     . ,mg,m2)*xg2+ans5
      ans3=((((xg2+1)*xb2-2*xg2)*xb1+(xg2+1-2*xb2)*xb2**2)*(log(xb2)-
     . log(xg2))**2*(xb1-1)**2*(xg2-1)+(log(xg2)+4)*(xb1-xb2)**3*(xb2
     . -xg2)**2*log(xg2))*(xb1-xg2)**2*xgl+2*((3*xb2+2*xgl)*xb1**2+2*
     . (xb2-1)*xb2*xgl+(3*xb2**2-6*xb2-2*xgl)*xb1)*(xb1-xb2)*(xb1-1)*
     . (xb2-1)*xb1*xb2-(xb2**2+2*xg2-(xg2+1)*xb2-(xg2+1-xb1)*xb1)*(
     . log(xg2)-log(xgl))**2*(xb1-xb2)*(xb1-xg2)*(xb1-1)*(xb2-xg2)*(
     . xb2-1)*(xg2-1)*xgl-2*((4*xgl-3)*xb2**2-4*xgl-(4*xgl+3)*xb2+((4
     . *xgl-3+9*xb2)*xb1+(9*xb2+4*xgl+3)*(xb2-1))*xb1)*(xb1-xb2)*(xb1
     . -1)*(xb2-1)*xg2**3-2*((3*xb2+2*xgl)*(xb2+1)*xb1**3+2*(xb2-1)*
     . xb2**2*xgl+(3*xb2**2+9*xb2+2*xgl)*(xb2-1)*xb1**2+((2*xgl-9)*
     . xb2-8*xgl+(2*xgl+3)*xb2**2)*xb1*xb2)*(xb1-xb2)*(xb1-1)*(xb2-1)
     . *xg2+ans4
      ans7=(sb2-1)*sb2*xg2
      ans2=ans3*ans7
      ans1=-ans2
      r81p2=ans1/(8*(xb1-xb2)*(xb1-xg2)**2*(xb1-1)**2*(xb2-xg2)**2*(
     . xb2-1)**2*(xg2-1))

      r812 = r812 + r81p2

      ans7=-(((((xt-xt2)**2*xt+xgl**3-(xt+2*xt2)*xgl**2)*((2*xt2-1)*
     . xt2-xt1)-(4*(3*xt2-2-xt1)*xt*xt2**2+((2*xt2-1)*xt2-xt1)*(xt+
     . xt2)*(xt-xt2))*xgl)*xt2-(((xt-xt2)**2*xt+xgl**3-(xt+2*xt2)*xgl
     . **2)*((xt2-2)*xt1+xt2**2)-(4*((2*xt2-1)*xt2-xt1)*xt*xt2+((xt2-
     . 2)*xt1+xt2**2)*(xt+xt2)*(xt-xt2))*xgl)*xg2)*st2+2*(xg2-xt2)*(
     . xgl**2-2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)*(xgl+xt)*(xt2
     . -1)*xt2)*(log(xg2)-log(xt2))
      ans6=4*(((((7*xt2-5)*xt2-(3*xt2-1)*xt1+(3*xt2-2-xt1)*xt)*xgl**2
     . -((3*xt2-2-xt1)*xgl**3-(xt*xt1-3*xt*xt2+2*xt-xt1*xt2+xt1+xt2**
     . 2-xt2)*(xt-xt2)**2)+((4*((4*xt2-3)*xt2-(2*xt2-1)*xt1)+(3*xt2-2
     . -xt1)*xt)*xt-((5*xt2-4)*xt2-(3*xt2-2)*xt1)*xt2)*xgl)*xt2**2-((
     . ((5*xt2-3)*xt2-(xt2+1)*xt1)*xt2+((2*xt2-1)*xt2-xt1)*xt)*xgl**2
     . -(((2*xt2-1)*xt2-xt1)*xgl**3-(xt*xt1-2*xt*xt2**2+xt*xt2-xt1*
     . xt2**2+xt1*xt2+xt2**3-xt2**2)*(xt-xt2)**2)+((4*(3*xt2-2-xt1)*
     . xt2**2+((2*xt2-1)*xt2-xt1)*xt)*xt-((4*xt2-3)*xt2-(2*xt2-1)*xt1
     . )*xt2**2)*xgl)*xg2)*st2-2*(xg2-xt2)*(xgl**2-2*xgl*xt-2*xgl*xt2
     . +xt**2-2*xt*xt2+xt2**2)*(xgl+xt)*(xt2-1)*xt2)+ans7
      ans8=(log(xg2)-log(xt2))*(xg2-1)*(xt1-1)**2*st2
      ans5=ans6*ans8
      ans9=((xt-xt2)**2+xgl**2-2*(xt+xt2)*xgl)*((xt1-xt2)*st2+xt2-1)
     . **2*(log(xg2)+4)*(xg2-xt2)**2*(xgl+xt)*(xt1-xt2)*log(xg2)
      ans4=ans5+ans9
      ans10=((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)*(xg2-xt1)**2
      ans3=ans4*ans10
      ans14=-(((((xt-xt1)**2*xt+xgl**3-(xt+2*xt1)*xgl**2)*(2*xt1**2-
     . xt1-xt2)+(4*(xt2+2-3*xt1)*xt*xt1**2-(xt+xt1)*(xt-xt1)*(2*xt1**
     . 2-xt1-xt2))*xgl)*xt1-(((xt-xt1)**2*xt+xgl**3-(xt+2*xt1)*xgl**2
     . )*(xt1**2+xt1*xt2-2*xt2)-((xt+xt1)*(xt-xt1)*(xt1**2+xt1*xt2-2*
     . xt2)+4*(2*xt1**2-xt1-xt2)*xt*xt1)*xgl)*xg2)*st2-((((xt-xt1)**2
     . *xt+xgl**3-(xt+2*xt1)*xgl**2)*(xt1-2)-((xt+xt1)*(xt-xt1)*(xt1-
     . 2)-4*xt*xt1)*xgl)*xg2+((xt-xt1)**2*xt+xgl**3-(xt+2*xt1)*xgl**2
     . -(xt**2+4*xt*xt1**2-xt1**2)*xgl)*xt1)*(xt1-xt2))*(log(xg2)-log
     . (xt1))
      ans13=4*((((7*xt1**2+xt2-(3*xt2+5)*xt1-(xt2+2-3*xt1)*xt)*xgl**2
     . +(xt2+2-3*xt1)*xgl**3-(3*xt*xt1-xt*xt2-2*xt-xt1**2+xt1*xt2+xt1
     . -xt2)*(xt-xt1)**2+((4*(4*xt1**2+xt2-(2*xt2+3)*xt1)-(xt2+2-3*
     . xt1)*xt)*xt-(5*xt1**2+2*xt2-(3*xt2+4)*xt1)*xt1)*xgl)*xt1**2-((
     . (5*xt1**2-xt2-(xt2+3)*xt1)*xt1+(2*xt1**2-xt1-xt2)*xt)*xgl**2-(
     . (2*xt*xt1**2-xt*xt1-xt*xt2-xt1**3+xt1**2*xt2+xt1**2-xt1*xt2)*(
     . xt-xt1)**2+(2*xt1**2-xt1-xt2)*xgl**3)-((4*(xt2+2-3*xt1)*xt1**2
     . -(2*xt1**2-xt1-xt2)*xt)*xt+(4*xt1**2+xt2-(2*xt2+3)*xt1)*xt1**2
     . )*xgl)*xg2)*st2-(((xt-xt1**2+xt1)*(xt-xt1)**2+xgl**3-((xt1+1)*
     . xt1+xt)*xgl**2-((xt+4*xt1**2)*xt-(2*xt1-1)*xt1**2)*xgl)*xg2-((
     . xt-xt1+1)*(xt-xt1)**2+xgl**3-(3*xt1-1+xt)*xgl**2-((xt+8*xt1-4)
     . *xt-(3*xt1-2)*xt1)*xgl)*xt1**2)*(xt1-xt2))+ans14
      ans15=((xt-xt2)**2+xgl**2-2*(xt+xt2)*xgl)*(log(xg2)-log(xt1))*(
     . st2-1)*(xg2-xt2)**2*(xg2-1)*(xt2-1)**2
      ans12=ans13*ans15
      ans11=-ans12
      ans21=-((2*((2*(xt2+1)-3*xt1)*xt1-(3*xt2-2)*xt2)*xt-(2*xt**2-
     . xt1**2-4*xt1*xt2-xt2**2)*(xt1+xt2-2))*xgl**2+(xgl**4-2*xgl**3*
     . xt1-2*xgl**3*xt2+xt**4-2*xt**3*xt1-2*xt**3*xt2+xt**2*xt1**2+4*
     . xt**2*xt1*xt2+xt**2*xt2**2-2*xt*xt1**2*xt2-2*xt*xt1*xt2**2+xt1
     . **2*xt2**2)*(xt1+xt2-2)+2*((xt1**3+3*xt1**2*xt2+xt2**3+(3*xt2-
     . 8)*xt1*xt2)*xt-(xt1+xt2-2)*(xt1+xt2)*xt1*xt2+((2*(xt2+1)-3*xt1
     . )*xt1-(3*xt2-2)*xt2)*xt**2)*xgl)*xg2
      ans20=2*(((xt2-1)*xt2**3+xt1**4-(2*xt2+3)*xt1**2*xt2+(4*xt2-3)*
     . xt1*xt2**2+(4*xt2-1)*xt1**3)*xt+(((xt2-2)*xt2-3*xt1**2)*xt1-3*
     . (xt2-1)*xt2**2+(xt2+3)*xt1**2)*xt**2-(xt1**2-xt1+xt2**2-xt2)*(
     . xt1+xt2)*xt1*xt2)*xgl+(2*(((xt2-2)*xt2-3*xt1**2)*xt1-3*(xt2-1)
     . *xt2**2+(xt2+3)*xt1**2)*xt-(2*xt**2-xt1**2-4*xt1*xt2-xt2**2)*(
     . xt1**2-xt1+xt2**2-xt2))*xgl**2+(xgl**4-2*xgl**3*xt1-2*xgl**3*
     . xt2+xt**4-2*xt**3*xt1-2*xt**3*xt2+xt**2*xt1**2+4*xt**2*xt1*xt2
     . +xt**2*xt2**2-2*xt*xt1**2*xt2-2*xt*xt1*xt2**2+xt1**2*xt2**2)*(
     . xt1**2-xt1+xt2**2-xt2)+ans21
      ans22=st2**2
      ans19=ans20*ans22
      ans23=(2*st2-1)*(xg2-xt2)*(xgl**2-2*xgl*xt-2*xgl*xt2+xt**2-2*xt
     . *xt2+xt2**2)*(xgl+xt-xt1)**2*(xt2-1)
      ans18=ans19+ans23
      ans24=((log(xg2)-log(xgl))**2*xgl+(log(xg2)-log(xt))**2*xt)*(
     . xg2-xt1)*(xg2-xt2)*(xg2-1)*(xt1-xt2)*(xt1-1)*(xt2-1)
      ans17=ans18*ans24
      ans16=-ans17
      ans30=-2*(10*((xt2-1+xt1)*xt1+xt2**2-xt2-1)*xt**2+(28*xt1**2-17
     . *xt1*xt2-13*xt1+28*xt2**2-13*xt2-13)*(xt1+xt2)*xt-(2*xt1**2+5*
     . xt1*xt2+xt1+2*xt2**2+xt2+1)*(xt1-xt2)**2)*xgl**3-2*(((7*xt2-3)
     . *xt1**3-3*(xt2+1)*xt2**2+(7*xt2**2-7*xt2-4)*xt1*xt2+(16*xt2**2
     . -7*xt2-3)*xt1**2)*xt1*xt2-(8*((xt2-1+xt1)*xt1+xt2**2-xt2-1)*xt
     . **3-(3*xt1**3*xt2-3*xt1**3-21*xt1**2*xt2**2+8*xt1**2*xt2-3*xt1
     . **2+3*xt1*xt2**3+8*xt1*xt2**2+11*xt1*xt2-3*xt2**3-3*xt2**2+(28
     . *xt1**2-17*xt1*xt2-13*xt1+28*xt2**2-13*xt2-13)*xt**2)*(xt1+xt2
     . ))*xt-2*((5*xt2-4+6*xt1)*xt1**3+2*(3*xt2**2-2*xt2-2)*xt2**2+(5
     . *xt2**2-5*xt2-4)*xt1**2+(5*xt2**2-5*xt2-1)*xt1*xt2)*xt**2)*xgl
      ans29=(4*((5*xt2-4+6*xt1)*xt1**3+2*(3*xt2**2-2*xt2-2)*xt2**2+(5
     . *xt2**2-5*xt2-4)*xt1**2+(5*xt2**2-5*xt2-1)*xt1*xt2)*xt-(20*((
     . xt2-1+xt1)*xt1+xt2**2-xt2-1)*xt**3+(96*xt**2*xt1**2-42*xt**2*
     . xt1*xt2-50*xt**2*xt1+96*xt**2*xt2**2-50*xt**2*xt2-50*xt**2-xt1
     . **3*xt2+3*xt1**3-28*xt1**2*xt2**2+7*xt1**2*xt2+3*xt1**2-xt1*
     . xt2**3+7*xt1*xt2**2+4*xt1*xt2+3*xt2**3+3*xt2**2)*(xt1+xt2)))*
     . xgl**2+4*((xt2-1+xt1)*xt1+xt2**2-xt2-1)*xgl**5+(4*xt*xt1**2+4*
     . xt*xt1*xt2-4*xt*xt1+4*xt*xt2**2-4*xt*xt2-4*xt+9*xt1**2*xt2-3*
     . xt1**2+9*xt1*xt2**2-6*xt1*xt2-3*xt1-3*xt2**2-3*xt2)*(xt-xt1)**
     . 2*(xt-xt2)**2+(16*((xt2-1+xt1)*xt1+xt2**2-xt2-1)*xt-(8*xt1**2-
     . xt1*xt2-5*xt1+8*xt2**2-5*xt2-5)*(xt1+xt2))*xgl**4+ans30
      ans31=st2**2
      ans28=ans29*ans31
      ans32=-(2*st2-1)*(2*xgl**3+12*xgl**2*xt-xgl**2*xt1+12*xgl*xt**2
     . -4*xgl*xt1**2+2*xt**3-xt**2*xt1-4*xt*xt1**2+3*xt1**3)*(xgl**2-
     . 2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)*(xt1+2*xt2+1)*(xt2-1
     . )
      ans27=ans28+ans32
      ans33=(xt1-xt2)*(xt1-1)*(xt2-1)*xg2**3
      ans26=2*ans27*ans33
      ans25=-ans26
      ans39=2*(((2*xt2-5)*xt2+2*xt1**2+(6*xt2-5)*xt1)*xt1**2*xt2**2-4
     . *((xt1-1)*xt1+(xt2-1)*xt2)*xt**4-(((5*xt2-16)*xt1+3*xt2)*xt2+(
     . 5*xt2+3)*xt1**2)*xt*xt1*xt2-(((xt2-2)*xt2-14*xt1**2)*xt1-14*(
     . xt2-1)*xt2**2+(xt2+14)*xt1**2)*xt**3-(((xt2-6+6*xt1)*xt1**2+(
     . xt2-3)*xt2**2)*xt1+6*(xt2-1)*xt2**3+(4*xt2-3)*xt1**2*xt2)*xt**
     . 2)*xgl
      ans38=(((xt2-4+4*xt1)*xt1+(xt2-2)*xt2)*xt1+4*(xt2-1)*xt2**2-8*(
     . (xt1-1)*xt1+(xt2-1)*xt2)*xt)*xgl**4-(2*((xt1-1)*xt1+(xt2-1)*
     . xt2)*xgl**5+(2*xt*xt1**2-2*xt*xt1+2*xt*xt2**2-2*xt*xt2+3*xt1**
     . 2*xt2+3*xt1*xt2**2-6*xt1*xt2)*(xt-xt1)**2*(xt-xt2)**2)-2*((((
     . xt2-2)*xt2-14*xt1**2)*xt1-14*(xt2-1)*xt2**2+(xt2+14)*xt1**2)*
     . xt-(5*((xt1-1)*xt1+(xt2-1)*xt2)*xt**2-(xt1**2+3*xt1*xt2-xt1+
     . xt2**2-xt2)*(xt1-xt2)**2))*xgl**3+(2*(((xt2-24+24*xt1)*xt1+(
     . xt2-2)*xt2)*xt1+24*(xt2-1)*xt2**2+5*((xt1-1)*xt1+(xt2-1)*xt2)*
     . xt)*xt**2+((xt2+2)*xt2**2+xt1**3-(11*xt2-16)*xt1*xt2-(11*xt2-2
     . )*xt1**2)*xt1*xt2-2*(((xt2-6+6*xt1)*xt1**2+(xt2-3)*xt2**2)*xt1
     . +6*(xt2-1)*xt2**3+(4*xt2-3)*xt1**2*xt2)*xt)*xgl**2+ans39
      ans40=st2**2
      ans37=ans38*ans40
      ans41=(2*st2-1)*(2*xgl**3+12*xgl**2*xt-xgl**2*xt1+12*xgl*xt**2-
     . 4*xgl*xt1**2+2*xt**3-xt**2*xt1-4*xt*xt1**2+3*xt1**3)*(xgl**2-2
     . *xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)*(xt2-1)*xt2
      ans36=ans37+ans41
      ans42=(xt1-xt2)*(xt1-1)*(xt2-1)*xt1*xt2
      ans35=2*ans36*ans42
      ans34=-ans35
      ans49=2*((6*((xt2+1)*xt1**5+(xt2-1)*xt2**4)+(xt2**2+5*xt2-8)*
     . xt1**2*xt2**2+(xt2**2+7*xt2-6)*xt1**4+(4*xt2**2+5*xt2-17)*xt1
     . **3*xt2+(6*xt2**2+7*xt2-17)*xt1*xt2**3)*xt**2+(4*((xt1**2+xt2
     . **2)*(xt2-1)+(xt2+1)*xt1**3+(xt2**2+xt2-4)*xt1*xt2)*xt**3-((14
     . *xt1**3*xt2+14*xt1**3-15*xt1**2*xt2**2-xt1**2*xt2-14*xt1**2+14
     . *xt1*xt2**3-xt1*xt2**2-11*xt1*xt2+14*xt2**3-14*xt2**2)*xt**2-(
     . 5*xt1**2*xt2**2+5*xt1**2*xt2+6*xt1**2+5*xt1*xt2**2-27*xt1*xt2+
     . 6*xt2**2)*xt1*xt2)*(xt1+xt2))*xt-2*((xt2+1)*xt1**3+(xt2-4)*xt2
     . **2+(3*xt2-2)*(xt2+2)*xt1**2+(xt2**2+4*xt2-7)*xt1*xt2)*xt1**2*
     . xt2**2)*xgl
      ans48=(2*xt*xt1**3*xt2+2*xt*xt1**3+2*xt*xt1**2*xt2-2*xt*xt1**2+
     . 2*xt*xt1*xt2**3+2*xt*xt1*xt2**2-8*xt*xt1*xt2+2*xt*xt2**3-2*xt*
     . xt2**2+3*xt1**3*xt2**2+3*xt1**3*xt2+3*xt1**2*xt2**3+6*xt1**2*
     . xt2**2-9*xt1**2*xt2+3*xt1*xt2**3-9*xt1*xt2**2)*(xt-xt1)**2*(xt
     . -xt2)**2+(8*((xt1**2+xt2**2)*(xt2-1)+(xt2+1)*xt1**3+(xt2**2+
     . xt2-4)*xt1*xt2)*xt-(4*xt1**3*xt2+4*xt1**3-3*xt1**2*xt2**2+xt1
     . **2*xt2-4*xt1**2+4*xt1*xt2**3+xt1*xt2**2-7*xt1*xt2+4*xt2**3-4*
     . xt2**2)*(xt1+xt2))*xgl**4-2*(5*((xt1**2+xt2**2)*(xt2-1)+(xt2+1
     . )*xt1**3+(xt2**2+xt2-4)*xt1*xt2)*xt**2+(14*xt1**3*xt2+14*xt1**
     . 3-15*xt1**2*xt2**2-xt1**2*xt2-14*xt1**2+14*xt1*xt2**3-xt1*xt2
     . **2-11*xt1*xt2+14*xt2**3-14*xt2**2)*(xt1+xt2)*xt-(xt1**3*xt2+
     . xt1**3+3*xt1**2*xt2**2+4*xt1**2*xt2-xt1**2+xt1*xt2**3+4*xt1*
     . xt2**2-xt1*xt2+xt2**3-xt2**2)*(xt1-xt2)**2)*xgl**3+ans49
      ans47=(2*(6*((xt2+1)*xt1**5+(xt2-1)*xt2**4)+(xt2**2+5*xt2-8)*
     . xt1**2*xt2**2+(xt2**2+7*xt2-6)*xt1**4+(4*xt2**2+5*xt2-17)*xt1
     . **3*xt2+(6*xt2**2+7*xt2-17)*xt1*xt2**3)*xt-(10*((xt1**2+xt2**2
     . )*(xt2-1)+(xt2+1)*xt1**3+(xt2**2+xt2-4)*xt1*xt2)*xt**3+(2*(24*
     . xt1**3*xt2+24*xt1**3-23*xt1**2*xt2**2+xt1**2*xt2-24*xt1**2+24*
     . xt1*xt2**3+xt1*xt2**2-27*xt1*xt2+24*xt2**3-24*xt2**2)*xt**2+(
     . xt1**3*xt2+xt1**3-12*xt1**2*xt2**2-11*xt1**2*xt2+5*xt1**2+xt1*
     . xt2**3-11*xt1*xt2**2+20*xt1*xt2+xt2**3+5*xt2**2)*xt1*xt2)*(xt1
     . +xt2)))*xgl**2+2*((xt1**2+xt2**2)*(xt2-1)+(xt2+1)*xt1**3+(xt2
     . **2+xt2-4)*xt1*xt2)*xgl**5+ans48
      ans50=st2**2
      ans46=ans47*ans50
      ans51=-(2*st2-1)*(2*xgl**3+12*xgl**2*xt-xgl**2*xt1+12*xgl*xt**2
     . -4*xgl*xt1**2+2*xt**3-xt**2*xt1-4*xt*xt1**2+3*xt1**3)*(xgl**2-
     . 2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)*(xt1*xt2+2*xt1+xt2)*
     . (xt2-1)*xt2
      ans45=ans46+ans51
      ans52=(xt1-xt2)*(xt1-1)*(xt2-1)*xg2
      ans44=2*ans45*ans52
      ans43=-ans44
      ans58=((xg2-xt2-(xt1-xt2)*st2)**2*(xgl+xt-xg2)*(xt1-1)**2*(xt2-
     . 1)**2*t134(m2,mt,mg,m2)-(xt-1+xgl)*((xt1-xt2)*st2+xt2-1)**2*(
     . xg2-xt1)**2*(xg2-xt2)**2*t134(mu,mt,mg,m2))*((xt-xt2)**2+xgl**
     . 2-2*(xt+xt2)*xgl)*(xt1-xt2)
      ans57=(((((8*xt2-5)*xt2-(2*xt2+1)*xt1)*xt2**2-((4*xt2-3)*xt2-(2
     . *xt2-1)*xt1)*(xt+2*xt2)*xt)*xgl+((4*xt2-3)*xt2-(2*xt2-1)*xt1)*
     . xgl**3-(2*xt*xt1*xt2-xt*xt1-4*xt*xt2**2+3*xt*xt2-xt1*xt2+2*xt2
     . **3-xt2**2)*(xt-xt2)**2-(((10*xt2-7)*xt2-(4*xt2-1)*xt1)*xt2+((
     . 4*xt2-3)*xt2-(2*xt2-1)*xt1)*xt)*xgl**2-((((5*xt2-2)*xt2+(xt2-4
     . )*xt1)*xt2-(3*xt2-2-xt1)*(xt+2*xt2)*xt)*xgl+(3*xt2-2-xt1)*xgl
     . **3-(xt*xt1-3*xt*xt2+2*xt+xt1*xt2-2*xt1+xt2**2)*(xt-xt2)**2-((
     . 7*xt2-4)*xt2-(xt2+2)*xt1+(3*xt2-2-xt1)*xt)*xgl**2)*xg2)*st2+2*
     . (xg2-xt2)*(xgl**2-2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)*(
     . xgl+xt-xt2)*(xt2-1))*(xg2-xt1)**2*(xg2-1)*(xt1-1)**2*t134(mt2,
     . mt,mg,m2)*st2+ans58
      ans59=((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)
      ans56=ans57*ans59
      ans62=(xg2-xt2)**2*(xg2-1)*(xt2-1)**2*t134(mt1,mt,mg,m2)
      ans61=((((8*xt1**2-xt2-(2*xt2+5)*xt1)*xt1**2-(4*xt1**2+xt2-(2*
     . xt2+3)*xt1)*(xt+2*xt1)*xt)*xgl+(4*xt1**2+xt2-(2*xt2+3)*xt1)*
     . xgl**3+(4*xt*xt1**2-2*xt*xt1*xt2-3*xt*xt1+xt*xt2-2*xt1**3+xt1
     . **2+xt1*xt2)*(xt-xt1)**2-((10*xt1**2+xt2-(4*xt2+7)*xt1)*xt1+(4
     . *xt1**2+xt2-(2*xt2+3)*xt1)*xt)*xgl**2-(((5*xt1**2-4*xt2+(xt2-2
     . )*xt1)*xt1+(xt2+2-3*xt1)*(xt+2*xt1)*xt)*xgl-((xt2+2-3*xt1)*xgl
     . **3-(3*xt*xt1-xt*xt2-2*xt-xt1**2-xt1*xt2+2*xt2)*(xt-xt1)**2)-(
     . 7*xt1**2-2*xt2-(xt2+4)*xt1-(xt2+2-3*xt1)*xt)*xgl**2)*xg2)*st2-
     . ((2*xt*xt1-xt-xt1)*(xt-xt1)**2+(2*xt1-1)*xgl**3-((4*xt1-1)*xt1
     . +(2*xt1-1)*xt)*xgl**2-((xt+2*xt1)*(2*xt1-1)*xt-(2*xt1+1)*xt1**
     . 2)*xgl-((xt+xt1-2)*(xt-xt1)**2+xgl**3-(xt1+2+xt)*xgl**2-((xt+2
     . *xt1)*xt+(xt1-4)*xt1)*xgl)*xg2)*(xt1-xt2))*((xt-xt2)**2+xgl**2
     . -2*(xt+xt2)*xgl)*(st2-1)*ans62
      ans60=-ans61
      ans66=-(2*st2-1)*(2*xgl**3+12*xgl**2*xt-xgl**2*xt1+12*xgl*xt**2
     . -4*xgl*xt1**2+2*xt**3-xt**2*xt1-4*xt*xt1**2+3*xt1**3)*(xgl**2-
     . 2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)*(xt2-1)
      ans65=(2*(((2*xt2+13-14*xt1)*xt1-(14*xt2-13)*xt2+4*(xt2-2+xt1)*
     . xt)*xt**3-(((5*xt2-4)*xt1-3*xt2)*xt2+(5*xt2-3)*xt1**2)*xt1*xt2
     . -(3*((xt2-1)*xt1**3-xt2**3)-8*(2*xt2-1)*xt1**2*xt2+(3*xt2+8)*
     . xt1*xt2**2)*xt+((3*xt2-8+6*xt1)*xt1**2+2*(3*xt2-4)*xt2**2+(3*
     . xt2-2)*xt1*xt2)*xt**2)*xgl-(((2*xt2-5+4*xt1)*xt1+(4*xt2-5)*xt2
     . -8*(xt2-2+xt1)*xt)*xgl**4-(2*(xt2-2+xt1)*xgl**5+(2*xt*xt1+2*xt
     . *xt2-4*xt+6*xt1*xt2-3*xt1-3*xt2)*(xt-xt1)**2*(xt-xt2)**2)-2*((
     . (2*xt2+13-14*xt1)*xt1-(14*xt2-13)*xt2)*xt-(5*(xt2-2+xt1)*xt**2
     . -(xt1+xt2+1)*(xt1-xt2)**2))*xgl**3-(((2*xt2-7)*xt1-3*xt2)*xt2
     . **2+(2*xt2-3)*xt1**3+(16*xt2-7)*xt1**2*xt2-2*((2*xt2-25+24*xt1
     . )*xt1+(24*xt2-25)*xt2+5*(xt2-2+xt1)*xt)*xt**2+2*((3*xt2-8+6*
     . xt1)*xt1**2+2*(3*xt2-4)*xt2**2+(3*xt2-2)*xt1*xt2)*xt)*xgl**2))
     . *st2**2+ans66
      ans67=(xt1-xt2)*(xt1-1)*(xt2-1)*xg2**3
      ans64=ans65*ans67
      ans63=-ans64
      ans55=ans56+ans60+ans63
      ans54=2*ans55*xg2
      ans53=-ans54
      ans74=2*(((2*xt1**4-3*xt2**2+(2*xt2**2-xt2-12)*xt1*xt2)*xt2+(13
     . *xt2**2-xt2-3)*xt1**3+(13*xt2**2+2*xt2-12)*xt1**2*xt2)*xt1*xt2
     . -4*((2*xt2+1+xt1)*xt1**2+(xt2**2+xt2-3)*xt2+(2*xt2**2-2*xt2-3)
     . *xt1)*xt**4-((((3*xt2-2)*xt1+3*xt2)*xt2+(2*xt2**2-3*xt2-32)*
     . xt1**2)*xt2**2+(2*xt2**2+3*xt2+3)*xt1**4+(26*xt2**2-3*xt2-2)*
     . xt1**3*xt2)*xt+(((27*xt2+14+14*xt1)*xt1-(4*xt2**2+14*xt2+27))*
     . xt1**2+(14*xt2**2+14*xt2-27)*xt2**2+(27*xt2**2-14*xt2-24)*xt1*
     . xt2)*xt**3-((13*xt2+6+6*xt1)*xt1**4+2*(3*xt2**2+3*xt2-7)*xt2**
     . 3+(8*xt2**2-7*xt2-14)*xt1**3+(8*xt2**2+2*xt2-13)*xt1**2*xt2+(
     . 13*xt2**2-7*xt2-13)*xt1*xt2**2)*xt**2)*xgl
      ans73=-(2*((2*xt2+1+xt1)*xt1**2+(xt2**2+xt2-3)*xt2+(2*xt2**2-2*
     . xt2-3)*xt1)*xgl**5+(2*xt*xt1**3+4*xt*xt1**2*xt2+2*xt*xt1**2+4*
     . xt*xt1*xt2**2-4*xt*xt1*xt2-6*xt*xt1+2*xt*xt2**3+2*xt*xt2**2-6*
     . xt*xt2+3*xt1**3*xt2+12*xt1**2*xt2**2-3*xt1**2+3*xt1*xt2**3-12*
     . xt1*xt2-3*xt2**2)*(xt-xt1)**2*(xt-xt2)**2)+2*((((27*xt2+14+14*
     . xt1)*xt1-(4*xt2**2+14*xt2+27))*xt1**2+(14*xt2**2+14*xt2-27)*
     . xt2**2+(27*xt2**2-14*xt2-24)*xt1*xt2)*xt+5*((2*xt2+1+xt1)*xt1
     . **2+(xt2**2+xt2-3)*xt2+(2*xt2**2-2*xt2-3)*xt1)*xt**2-(xt1**2+4
     . *xt1*xt2+xt2**2)*(xt1+xt2+1)*(xt1-xt2)**2)*xgl**3+ans74
      ans72=(2*(((49*xt2+24+24*xt1)*xt1+4*xt2**2-24*xt2-49)*xt1**2+(
     . 24*xt2**2+24*xt2-49)*xt2**2+(49*xt2**2-24*xt2-52)*xt1*xt2+5*((
     . 2*xt2+1+xt1)*xt1**2+(xt2**2+xt2-3)*xt2+(2*xt2**2-2*xt2-3)*xt1)
     . *xt)*xt**2+(xt1**5+3*xt2**3+(xt2**2+4*xt2+12)*xt1*xt2**2-2*(6*
     . xt2**2+2*xt2-15)*xt1**2*xt2)*xt2-(12*xt2**2-4*xt2-3)*xt1**4-2*
     . (19*xt2**2+2*xt2-6)*xt1**3*xt2-2*((13*xt2+6+6*xt1)*xt1**4+2*(3
     . *xt2**2+3*xt2-7)*xt2**3+(8*xt2**2-7*xt2-14)*xt1**3+(8*xt2**2+2
     . *xt2-13)*xt1**2*xt2+(13*xt2**2-7*xt2-13)*xt1*xt2**2)*xt)*xgl**
     . 2+(((9*xt2+4+4*xt1)*xt1+4*xt2**2-4*xt2-9)*xt1**2+(4*xt2**2+4*
     . xt2-9)*xt2**2+(9*xt2**2-4*xt2-12)*xt1*xt2-8*((2*xt2+1+xt1)*xt1
     . **2+(xt2**2+xt2-3)*xt2+(2*xt2**2-2*xt2-3)*xt1)*xt)*xgl**4+
     . ans73
      ans75=st2**2
      ans71=ans72*ans75
      ans76=(2*st2-1)*(2*xgl**3+12*xgl**2*xt-xgl**2*xt1+12*xgl*xt**2-
     . 4*xgl*xt1**2+2*xt**3-xt**2*xt1-4*xt*xt1**2+3*xt1**3)*(xgl**2-2
     . *xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)*(2*xt1*xt2+xt1+xt2**2
     . +2*xt2)*(xt2-1)
      ans70=ans71+ans76
      ans77=(xt1-xt2)*(xt1-1)*(xt2-1)*xg2**2
      ans69=2*ans70*ans77
      ans68=-ans69
      ans89=-(2*(((2*xt2-1)*xt2**2+2*xt1**3+(3*xt2-8)*xt1*xt2+(3*xt2-
     . 1)*xt1**2)*xt+((2*(xt2+2)-5*xt1)*xt1-(5*xt2-4)*xt2)*xt**2+(xt
     . **3-xt1**2*xt2-xt1*xt2**2)*(xt1+xt2-2))*xgl+(2*((2*(xt2+2)-5*
     . xt1)*xt1-(5*xt2-4)*xt2)*xt-(6*xt**2-xt1**2-4*xt1*xt2-xt2**2)*(
     . xt1+xt2-2))*xgl**2+(xgl**4+2*xgl**3*xt-2*xgl**3*xt1-2*xgl**3*
     . xt2+xt**4-2*xt**3*xt1-2*xt**3*xt2+xt**2*xt1**2+4*xt**2*xt1*xt2
     . +xt**2*xt2**2-2*xt*xt1**2*xt2-2*xt*xt1*xt2**2+xt1**2*xt2**2)*(
     . xt1+xt2-2))*xg2
      ans88=(2*(((xt2-2)*xt2-5*xt1**2)*xt1-5*(xt2-1)*xt2**2+(xt2+5)*
     . xt1**2)*xt-(6*xt**2-xt1**2-4*xt1*xt2-xt2**2)*(xt1**2-xt1+xt2**
     . 2-xt2))*xgl**2+(xgl**4+2*xgl**3*xt-2*xgl**3*xt1-2*xgl**3*xt2+
     . xt**4-2*xt**3*xt1-2*xt**3*xt2+xt**2*xt1**2+4*xt**2*xt1*xt2+xt
     . **2*xt2**2-2*xt*xt1**2*xt2-2*xt*xt1*xt2**2+xt1**2*xt2**2)*(xt1
     . **2-xt1+xt2**2-xt2)+2*((2*(xt1**3+xt1**2*xt2-xt1**2-xt1*xt2**2
     . +xt1*xt2+xt2**3-xt2**2)*(xt1+xt2)-(2*xt2+3)*xt1**2*xt2+(4*xt2-
     . 3)*xt1*xt2**2)*xt+(xt**3-xt1**2*xt2-xt1*xt2**2)*(xt1**2-xt1+
     . xt2**2-xt2)+(((xt2-2)*xt2-5*xt1**2)*xt1-5*(xt2-1)*xt2**2+(xt2+
     . 5)*xt1**2)*xt**2)*xgl+ans89
      ans90=st2**2
      ans87=ans88*ans90
      ans91=(2*st2-1)*(xg2-xt2)*(xgl**2+4*xgl*xt-2*xgl*xt1+xt**2-2*xt
     . *xt1+xt1**2)*(xgl**2-2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)
     . *(xt2-1)
      ans86=ans87+ans91
      ans92=(xg2-1)*(xt1-1)*(xt2-1)
      ans85=2*ans86*ans92
      ans93=-((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)*((xt-xt2)**2+xgl**2-
     . 2*(xt+xt2)*xgl)*((xt1-xt2)*st2+xt2-1)**2*(xg2-xt1)*(xg2-xt2)*
     . log(xg2)
      ans84=ans85+ans93
      ans94=(xg2-xt2)*(xt1-xt2)
      ans83=ans84*ans94
      ans95=-(((2*((3*xt2-2-xt1)*xt+(2*xt2-1)*xt2-xt1)*xgl*xt2-(((2*
     . xt2-1)*xt2-xt1)*xgl**2-(2*xt*xt1*xt2-xt*xt1-4*xt*xt2**2+3*xt*
     . xt2-xt1*xt2+2*xt2**3-xt2**2)*(xt-xt2)))*xt2-(2*(((2*xt2-1)*xt2
     . -xt1)*xt+((xt2-2)*xt1+xt2**2)*xt2)*xgl-(((xt2-2)*xt1+xt2**2)*
     . xgl**2-(xt*xt1-3*xt*xt2+2*xt+xt1*xt2-2*xt1+xt2**2)*(xt-xt2)*
     . xt2))*xg2)*st2-2*((xt-xt2)**2+xgl**2-2*(xt+xt2)*xgl)*(xg2-xt2)
     . *(xt2-1)*xt2)*((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)*(log(xg2)-
     . log(xt2))*(xg2-xt1)*(xg2-1)*(xt1-1)**2*st2
      ans82=ans83+ans95
      ans96=(xg2-xt1)
      ans81=ans82*ans96
      ans100=(xt1-xt2)*(xt1-1)*xt
      ans99=2*((((xt1**2-2*xt2)*xt1**2+(2*xt1+xt2)*(xt2-1)*xt2**2+(2*
     . xt2-1)*xt1**3-((xt1-1)*xt1+(xt2-1)*xt2)*xt**2+2*(((xt2-2)*xt2-
     . 2*xt1**2)*xt1-2*(xt2-1)*xt2**2+(xt2+2)*xt1**2)*xt)*xgl-((((xt1
     . +xt2)*(xt2-2)+2*xt1**2)*xt1+2*(xt2-1)*xt2**2+((xt1-1)*xt1+(xt2
     . -1)*xt2)*xt)*xgl**2-(((xt1-1)*xt1+(xt2-1)*xt2)*xgl**3+(xt*xt1
     . **2-xt*xt1+xt*xt2**2-xt*xt2-xt1**3+xt1**2-xt2**3+xt2**2)*(xt-
     . xt1)*(xt-xt2)))+(((2*((2*xt2-1)*xt2+2*xt1**2-(2*xt2+1)*xt1)+(
     . xt2-2+xt1)*xt)*xt-((2*(xt2-2)*xt2+xt1**2)*xt1+(xt2-1)*xt2**2+(
     . 2*xt2-1)*xt1**2))*xgl+((xt1+xt2)*(2*xt2-3)+2*xt1**2+(xt2-2+xt1
     . )*xt)*xgl**2-((xt2-2+xt1)*xgl**3+(xt*xt1+xt*xt2-2*xt-xt1**2+
     . xt1-xt2**2+xt2)*(xt-xt1)*(xt-xt2)))*xg2)*st2**2+(2*st2-1)*(xg2
     . -xt2)*(xgl**2-2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)*(xgl+
     . xt-xt1)*(xt2-1))*(log(xg2)-log(xt))*(xg2-xt1)*ans100
      ans101=-(((2*((xt2+2-3*xt1)*xt-(2*xt1**2-xt1-xt2))*xgl*xt1+(4*
     . xt*xt1**2-2*xt*xt1*xt2-3*xt*xt1+xt*xt2-2*xt1**3+xt1**2+xt1*xt2
     . )*(xt-xt1)+(2*xt1**2-xt1-xt2)*xgl**2)*xt1-((3*xt*xt1-xt*xt2-2*
     . xt-xt1**2-xt1*xt2+2*xt2)*(xt-xt1)*xt1+(xt1**2+xt1*xt2-2*xt2)*
     . xgl**2-2*((2*xt1**2-xt1-xt2)*xt+(xt1**2+xt1*xt2-2*xt2)*xt1)*
     . xgl)*xg2)*st2+(((xt+xt1-2)*(xt-xt1)*xt1-(xt1-2)*xgl**2+2*((xt1
     . -2)*xt1-xt)*xgl)*xg2+((2*(xt+1)*xt1-xgl)*xgl-(2*xt*xt1-xt-xt1)
     . *(xt-xt1))*xt1)*(xt1-xt2))*((xt-xt2)**2+xgl**2-2*(xt+xt2)*xgl)
     . *(log(xg2)-log(xt1))*(st2-1)*(xg2-xt2)*(xt2-1)
      ans98=ans99+ans101
      ans102=(xg2-xt2)*(xg2-1)*(xt2-1)
      ans97=ans98*ans102
      ans80=ans81+ans97
      ans103=(log(xg2)-log(xgl))*xgl
      ans79=2*ans80*ans103
      ans78=-ans79
      ans115=-(2*(((2*xt2-1)*xt2**2+2*xt1**3+(3*xt2-8)*xt1*xt2+(3*xt2
     . -1)*xt1**2)*xt+((2*(xt2+2)-5*xt1)*xt1-(5*xt2-4)*xt2)*xt**2+(xt
     . **3-xt1**2*xt2-xt1*xt2**2)*(xt1+xt2-2))*xgl+(2*((2*(xt2+2)-5*
     . xt1)*xt1-(5*xt2-4)*xt2)*xt-(6*xt**2-xt1**2-4*xt1*xt2-xt2**2)*(
     . xt1+xt2-2))*xgl**2+(xgl**4+2*xgl**3*xt-2*xgl**3*xt1-2*xgl**3*
     . xt2+xt**4-2*xt**3*xt1-2*xt**3*xt2+xt**2*xt1**2+4*xt**2*xt1*xt2
     . +xt**2*xt2**2-2*xt*xt1**2*xt2-2*xt*xt1*xt2**2+xt1**2*xt2**2)*(
     . xt1+xt2-2))*xg2
      ans114=(2*(((xt2-2)*xt2-5*xt1**2)*xt1-5*(xt2-1)*xt2**2+(xt2+5)*
     . xt1**2)*xt-(6*xt**2-xt1**2-4*xt1*xt2-xt2**2)*(xt1**2-xt1+xt2**
     . 2-xt2))*xgl**2+(xgl**4+2*xgl**3*xt-2*xgl**3*xt1-2*xgl**3*xt2+
     . xt**4-2*xt**3*xt1-2*xt**3*xt2+xt**2*xt1**2+4*xt**2*xt1*xt2+xt
     . **2*xt2**2-2*xt*xt1**2*xt2-2*xt*xt1*xt2**2+xt1**2*xt2**2)*(xt1
     . **2-xt1+xt2**2-xt2)+2*((2*(xt1**3+xt1**2*xt2-xt1**2-xt1*xt2**2
     . +xt1*xt2+xt2**3-xt2**2)*(xt1+xt2)-(2*xt2+3)*xt1**2*xt2+(4*xt2-
     . 3)*xt1*xt2**2)*xt+(xt**3-xt1**2*xt2-xt1*xt2**2)*(xt1**2-xt1+
     . xt2**2-xt2)+(((xt2-2)*xt2-5*xt1**2)*xt1-5*(xt2-1)*xt2**2+(xt2+
     . 5)*xt1**2)*xt**2)*xgl+ans115
      ans116=st2**2
      ans113=ans114*ans116
      ans117=(2*st2-1)*(xg2-xt2)*(xgl**2+4*xgl*xt-2*xgl*xt1+xt**2-2*
     . xt*xt1+xt1**2)*(xgl**2-2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**
     . 2)*(xt2-1)
      ans112=ans113+ans117
      ans118=(xg2-1)*(xt1-1)*(xt2-1)
      ans111=2*ans112*ans118
      ans119=-((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)*((xt-xt2)**2+xgl**2
     . -2*(xt+xt2)*xgl)*((xt1-xt2)*st2+xt2-1)**2*(xg2-xt1)*(xg2-xt2)*
     . log(xg2)
      ans110=ans111+ans119
      ans120=(xg2-xt2)*(xt1-xt2)
      ans109=ans110*ans120
      ans121=-(((2*(3*xt2-2-xt1)*(xt+xt2)*xgl*xt2-((2*xt2-1)*xt2-xt1)
     . *(xt-xt2)**2-((4*xt2-3)*xt2-(2*xt2-1)*xt1)*xgl**2)*xt2-(2*((2*
     . xt2-1)*xt2-xt1)*(xt+xt2)*xgl-((xt2-2)*xt1+xt2**2)*(xt-xt2)**2-
     . (3*xt2-2-xt1)*xgl**2*xt2)*xg2)*st2-2*((xt-xt2)**2+xgl**2-2*(xt
     . +xt2)*xgl)*(xg2-xt2)*(xt2-1)*xt2)*((xt-xt1)**2+xgl**2-2*(xt+
     . xt1)*xgl)*(log(xg2)-log(xt2))*(xg2-xt1)*(xg2-1)*(xt1-1)**2*st2
      ans108=ans109+ans121
      ans122=(xg2-xt1)
      ans107=ans108*ans122
      ans123=-(((2*(xt2+2-3*xt1)*(xt+xt1)*xgl*xt1+(xt-xt1)**2*(2*xt1
     . **2-xt1-xt2)+(4*xt1**2+xt2-(2*xt2+3)*xt1)*xgl**2)*xt1+(2*(xt+
     . xt1)*(2*xt1**2-xt1-xt2)*xgl-(xt-xt1)**2*(xt1**2+xt1*xt2-2*xt2)
     . +(xt2+2-3*xt1)*xgl**2*xt1)*xg2)*st2-(((xt-xt1)**2*(xt1-2)-xgl
     . **2*xt1+2*(xt+xt1)*xgl)*xg2+((xt-xt1)**2+(2*xt1-1)*xgl**2-2*(
     . xt+xt1)*xgl*xt1)*xt1)*(xt1-xt2))*((xt-xt2)**2+xgl**2-2*(xt+xt2
     . )*xgl)*(log(xg2)-log(xt1))*(st2-1)*(xg2-xt2)**2*(xg2-1)*(xt2-1
     . )**2
      ans106=ans107+ans123
      ans124=(log(xg2)-log(xt))*xt
      ans105=2*ans106*ans124
      ans104=-ans105
      ans2=ans3+ans11+ans16+ans25+ans34+ans43+ans53+ans68+ans78+
     . ans104
      ans1=ans2*xg2
      r822=ans1/(4*((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)*((xt-xt2)**2+
     . xgl**2-2*(xt+xt2)*xgl)*(xg2-xt1)**2*(xg2-xt2)**2*(xg2-1)*(xt1-
     . xt2)*(xt1-1)**2*(xt2-1)**2)

      ans14=2*xt**5*xt2+4*xt**4*xt1**3+xt**4*xt1**2*xt2-4*xt**4*xt1**
     . 2+xt**4*xt1*xt2**2-2*xt**4*xt1*xt2+4*xt**4*xt2**3-4*xt**4*xt2
     . **2-2*xt**3*xt1**4-2*xt**3*xt1**3*xt2+2*xt**3*xt1**3+8*xt**3*
     . xt1**2*xt2**2-2*xt**3*xt1**2*xt2-2*xt**3*xt1*xt2**3-2*xt**3*
     . xt1*xt2**2-2*xt**3*xt2**4+2*xt**3*xt2**3+xt**2*xt1**4*xt2-11*
     . xt**2*xt1**3*xt2**2+2*xt**2*xt1**3*xt2-11*xt**2*xt1**2*xt2**3+
     . 16*xt**2*xt1**2*xt2**2+xt**2*xt1*xt2**4+2*xt**2*xt1*xt2**3+4*
     . xt*xt1**4*xt2**2+12*xt*xt1**3*xt2**3-10*xt*xt1**3*xt2**2+4*xt*
     . xt1**2*xt2**4-10*xt*xt1**2*xt2**3-3*xt1**4*xt2**3-3*xt1**3*xt2
     . **4+6*xt1**3*xt2**3
      ans13=xgl**2*xt1**4*xt2-11*xgl**2*xt1**3*xt2**2+2*xgl**2*xt1**3
     . *xt2-11*xgl**2*xt1**2*xt2**3+16*xgl**2*xt1**2*xt2**2+xgl**2*
     . xt1*xt2**4+2*xgl**2*xt1*xt2**3-8*xgl*xt**4*xt1**2+8*xgl*xt**4*
     . xt1-8*xgl*xt**4*xt2**2+8*xgl*xt**4*xt2+28*xgl*xt**3*xt1**3-2*
     . xgl*xt**3*xt1**2*xt2-28*xgl*xt**3*xt1**2-2*xgl*xt**3*xt1*xt2**
     . 2+4*xgl*xt**3*xt1*xt2+28*xgl*xt**3*xt2**3-28*xgl*xt**3*xt2**2-
     . 12*xgl*xt**2*xt1**4-2*xgl*xt**2*xt1**3*xt2+12*xgl*xt**2*xt1**3
     . -8*xgl*xt**2*xt1**2*xt2**2+6*xgl*xt**2*xt1**2*xt2-2*xgl*xt**2*
     . xt1*xt2**3+6*xgl*xt**2*xt1*xt2**2-12*xgl*xt**2*xt2**4+12*xgl*
     . xt**2*xt2**3-10*xgl*xt*xt1**3*xt2**2-6*xgl*xt*xt1**3*xt2-10*
     . xgl*xt*xt1**2*xt2**3+32*xgl*xt*xt1**2*xt2**2-6*xgl*xt*xt1*xt2
     . **3+4*xgl*xt1**4*xt2**2+12*xgl*xt1**3*xt2**3-10*xgl*xt1**3*xt2
     . **2+4*xgl*xt1**2*xt2**4-10*xgl*xt1**2*xt2**3-2*xt**5*xt1**2+2*
     . xt**5*xt1-2*xt**5*xt2**2+ans14
      ans12=10*xgl**3*xt**2*xt2**2-10*xgl**3*xt**2*xt2+28*xgl**3*xt*
     . xt1**3-2*xgl**3*xt*xt1**2*xt2-28*xgl**3*xt*xt1**2-2*xgl**3*xt*
     . xt1*xt2**2+4*xgl**3*xt*xt1*xt2+28*xgl**3*xt*xt2**3-28*xgl**3*
     . xt*xt2**2-2*xgl**3*xt1**4-2*xgl**3*xt1**3*xt2+2*xgl**3*xt1**3+
     . 8*xgl**3*xt1**2*xt2**2-2*xgl**3*xt1**2*xt2-2*xgl**3*xt1*xt2**3
     . -2*xgl**3*xt1*xt2**2-2*xgl**3*xt2**4+2*xgl**3*xt2**3+10*xgl**2
     . *xt**3*xt1**2-10*xgl**2*xt**3*xt1+10*xgl**2*xt**3*xt2**2-10*
     . xgl**2*xt**3*xt2+48*xgl**2*xt**2*xt1**3+2*xgl**2*xt**2*xt1**2*
     . xt2-48*xgl**2*xt**2*xt1**2+2*xgl**2*xt**2*xt1*xt2**2-4*xgl**2*
     . xt**2*xt1*xt2+48*xgl**2*xt**2*xt2**3-48*xgl**2*xt**2*xt2**2-12
     . *xgl**2*xt*xt1**4-2*xgl**2*xt*xt1**3*xt2+12*xgl**2*xt*xt1**3-8
     . *xgl**2*xt*xt1**2*xt2**2+6*xgl**2*xt*xt1**2*xt2-2*xgl**2*xt*
     . xt1*xt2**3+6*xgl**2*xt*xt1*xt2**2-12*xgl**2*xt*xt2**4+12*xgl**
     . 2*xt*xt2**3+ans13
      ans11=5*xg2*xt**4*xt1-4*xg2*xt**4*xt2**2+5*xg2*xt**4*xt2+2*xg2*
     . xt**3*xt1**3-2*xg2*xt**3*xt1**2*xt2+2*xg2*xt**3*xt1**2-2*xg2*
     . xt**3*xt1*xt2**2-4*xg2*xt**3*xt1*xt2+2*xg2*xt**3*xt2**3+2*xg2*
     . xt**3*xt2**2+2*xg2*xt**2*xt1**3*xt2-3*xg2*xt**2*xt1**3+16*xg2*
     . xt**2*xt1**2*xt2**2-7*xg2*xt**2*xt1**2*xt2+2*xg2*xt**2*xt1*xt2
     . **3-7*xg2*xt**2*xt1*xt2**2-3*xg2*xt**2*xt2**3-10*xg2*xt*xt1**3
     . *xt2**2+6*xg2*xt*xt1**3*xt2-10*xg2*xt*xt1**2*xt2**3+8*xg2*xt*
     . xt1**2*xt2**2+6*xg2*xt*xt1*xt2**3+6*xg2*xt1**3*xt2**3-3*xg2*
     . xt1**3*xt2**2-3*xg2*xt1**2*xt2**3-2*xgl**5*xt1**2+2*xgl**5*xt1
     . -2*xgl**5*xt2**2+2*xgl**5*xt2-8*xgl**4*xt*xt1**2+8*xgl**4*xt*
     . xt1-8*xgl**4*xt*xt2**2+8*xgl**4*xt*xt2+4*xgl**4*xt1**3+xgl**4*
     . xt1**2*xt2-4*xgl**4*xt1**2+xgl**4*xt1*xt2**2-2*xgl**4*xt1*xt2+
     . 4*xgl**4*xt2**3-4*xgl**4*xt2**2+10*xgl**3*xt**2*xt1**2-10*xgl
     . **3*xt**2*xt1+ans12
      ans10=-16*xg2*xgl**2*xt*xt2**2+2*xg2*xgl**2*xt1**3*xt2-3*xg2*
     . xgl**2*xt1**3+16*xg2*xgl**2*xt1**2*xt2**2-7*xg2*xgl**2*xt1**2*
     . xt2+2*xg2*xgl**2*xt1*xt2**3-7*xg2*xgl**2*xt1*xt2**2-3*xg2*xgl
     . **2*xt2**3+8*xg2*xgl*xt**4*xt1+8*xg2*xgl*xt**4*xt2-16*xg2*xgl*
     . xt**4-28*xg2*xgl*xt**3*xt1**2+4*xg2*xgl*xt**3*xt1*xt2+26*xg2*
     . xgl*xt**3*xt1-28*xg2*xgl*xt**3*xt2**2+26*xg2*xgl*xt**3*xt2+12*
     . xg2*xgl*xt**2*xt1**3+6*xg2*xgl*xt**2*xt1**2*xt2-16*xg2*xgl*xt
     . **2*xt1**2+6*xg2*xgl*xt**2*xt1*xt2**2-4*xg2*xgl*xt**2*xt1*xt2+
     . 12*xg2*xgl*xt**2*xt2**3-16*xg2*xgl*xt**2*xt2**2-6*xg2*xgl*xt*
     . xt1**3*xt2+6*xg2*xgl*xt*xt1**3+32*xg2*xgl*xt*xt1**2*xt2**2-16*
     . xg2*xgl*xt*xt1**2*xt2-6*xg2*xgl*xt*xt1*xt2**3-16*xg2*xgl*xt*
     . xt1*xt2**2+6*xg2*xgl*xt*xt2**3-10*xg2*xgl*xt1**3*xt2**2+6*xg2*
     . xgl*xt1**3*xt2-10*xg2*xgl*xt1**2*xt2**3+8*xg2*xgl*xt1**2*xt2**
     . 2+6*xg2*xgl*xt1*xt2**3+2*xg2*xt**5*xt1+2*xg2*xt**5*xt2-4*xg2*
     . xt**5-4*xg2*xt**4*xt1**2-2*xg2*xt**4*xt1*xt2+ans11
      ans9=2*xg2*xgl**5*xt1+2*xg2*xgl**5*xt2-4*xg2*xgl**5+8*xg2*xgl**
     . 4*xt*xt1+8*xg2*xgl**4*xt*xt2-16*xg2*xgl**4*xt-4*xg2*xgl**4*xt1
     . **2-2*xg2*xgl**4*xt1*xt2+5*xg2*xgl**4*xt1-4*xg2*xgl**4*xt2**2+
     . 5*xg2*xgl**4*xt2-10*xg2*xgl**3*xt**2*xt1-10*xg2*xgl**3*xt**2*
     . xt2+20*xg2*xgl**3*xt**2-28*xg2*xgl**3*xt*xt1**2+4*xg2*xgl**3*
     . xt*xt1*xt2+26*xg2*xgl**3*xt*xt1-28*xg2*xgl**3*xt*xt2**2+26*xg2
     . *xgl**3*xt*xt2+2*xg2*xgl**3*xt1**3-2*xg2*xgl**3*xt1**2*xt2+2*
     . xg2*xgl**3*xt1**2-2*xg2*xgl**3*xt1*xt2**2-4*xg2*xgl**3*xt1*xt2
     . +2*xg2*xgl**3*xt2**3+2*xg2*xgl**3*xt2**2-10*xg2*xgl**2*xt**3*
     . xt1-10*xg2*xgl**2*xt**3*xt2+20*xg2*xgl**2*xt**3-48*xg2*xgl**2*
     . xt**2*xt1**2-4*xg2*xgl**2*xt**2*xt1*xt2+50*xg2*xgl**2*xt**2*
     . xt1-48*xg2*xgl**2*xt**2*xt2**2+50*xg2*xgl**2*xt**2*xt2+12*xg2*
     . xgl**2*xt*xt1**3+6*xg2*xgl**2*xt*xt1**2*xt2-16*xg2*xgl**2*xt*
     . xt1**2+6*xg2*xgl**2*xt*xt1*xt2**2-4*xg2*xgl**2*xt*xt1*xt2+12*
     . xg2*xgl**2*xt*xt2**3+ans10
      ans15=(xg2-1)*(xt1-1)*(xt2-1)
      ans8=ans9*ans15
      ans7=((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)*((xt-xt2)**2+xgl**2-2*
     . (xt+xt2)*xgl)*(xt-1+xgl)*(xg2-xt1)*(xg2-xt2)*(xt1-xt2)**2*t134
     . (mu,mt,mg,m2)*xg2+ans8
      ans16=(xg2-xt1)*(xg2-xt2)
      ans6=2*ans7*ans16
      ans17=-(2*(xgl+xt-xg2)*(xt1-1)**2*(xt2-1)**2*t134(m2,mt,mg,m2)*
     . xg2-(log(xg2)+4)*(xg2-xt1)**2*(xg2-xt2)**2*(xgl+xt)*log(xg2))*
     . ((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)*((xt-xt2)**2+xgl**2-2*(xt+
     . xt2)*xgl)*(xt1-xt2)**2
      ans5=ans6+ans17
      ans18=(xt1-xt2)
      ans4=ans5*ans18
      ans3=-ans4
      ans23=-((((xt-xt2)**2*xt+xgl**3-(xt+2*xt2)*xgl**2)*((2*xt2-1)*
     . xt2-xt1)-(4*(3*xt2-2-xt1)*xt*xt2**2+((2*xt2-1)*xt2-xt1)*(xt+
     . xt2)*(xt-xt2))*xgl)*xt2-(((xt-xt2)**2*xt+xgl**3-(xt+2*xt2)*xgl
     . **2)*((xt2-2)*xt1+xt2**2)-(4*((2*xt2-1)*xt2-xt1)*xt*xt2+((xt2-
     . 2)*xt1+xt2**2)*(xt+xt2)*(xt-xt2))*xgl)*xg2)*(log(xg2)-log(xt2)
     . )
      ans22=4*((((7*xt2-5)*xt2-(3*xt2-1)*xt1+(3*xt2-2-xt1)*xt)*xgl**2
     . -((3*xt2-2-xt1)*xgl**3-(xt*xt1-3*xt*xt2+2*xt-xt1*xt2+xt1+xt2**
     . 2-xt2)*(xt-xt2)**2)+((4*((4*xt2-3)*xt2-(2*xt2-1)*xt1)+(3*xt2-2
     . -xt1)*xt)*xt-((5*xt2-4)*xt2-(3*xt2-2)*xt1)*xt2)*xgl)*xt2**2-((
     . ((5*xt2-3)*xt2-(xt2+1)*xt1)*xt2+((2*xt2-1)*xt2-xt1)*xt)*xgl**2
     . -(((2*xt2-1)*xt2-xt1)*xgl**3-(xt*xt1-2*xt*xt2**2+xt*xt2-xt1*
     . xt2**2+xt1*xt2+xt2**3-xt2**2)*(xt-xt2)**2)+((4*(3*xt2-2-xt1)*
     . xt2**2+((2*xt2-1)*xt2-xt1)*xt)*xt-((4*xt2-3)*xt2-(2*xt2-1)*xt1
     . )*xt2**2)*xgl)*xg2)+ans23
      ans24=((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)*(log(xg2)-log(xt2))*(
     . xg2-xt1)**2*(xg2-1)*(xt1-1)**2
      ans21=ans22*ans24
      ans20=-ans21
      ans27=-((((xt-xt1)**2*xt+xgl**3-(xt+2*xt1)*xgl**2)*(2*xt1**2-
     . xt1-xt2)+(4*(xt2+2-3*xt1)*xt*xt1**2-(xt+xt1)*(xt-xt1)*(2*xt1**
     . 2-xt1-xt2))*xgl)*xt1-(((xt-xt1)**2*xt+xgl**3-(xt+2*xt1)*xgl**2
     . )*(xt1**2+xt1*xt2-2*xt2)-((xt+xt1)*(xt-xt1)*(xt1**2+xt1*xt2-2*
     . xt2)+4*(2*xt1**2-xt1-xt2)*xt*xt1)*xgl)*xg2)*(log(xg2)-log(xt1)
     . )
      ans26=4*(((7*xt1**2+xt2-(3*xt2+5)*xt1-(xt2+2-3*xt1)*xt)*xgl**2+
     . (xt2+2-3*xt1)*xgl**3-(3*xt*xt1-xt*xt2-2*xt-xt1**2+xt1*xt2+xt1-
     . xt2)*(xt-xt1)**2+((4*(4*xt1**2+xt2-(2*xt2+3)*xt1)-(xt2+2-3*xt1
     . )*xt)*xt-(5*xt1**2+2*xt2-(3*xt2+4)*xt1)*xt1)*xgl)*xt1**2-(((5*
     . xt1**2-xt2-(xt2+3)*xt1)*xt1+(2*xt1**2-xt1-xt2)*xt)*xgl**2-((2*
     . xt*xt1**2-xt*xt1-xt*xt2-xt1**3+xt1**2*xt2+xt1**2-xt1*xt2)*(xt-
     . xt1)**2+(2*xt1**2-xt1-xt2)*xgl**3)-((4*(xt2+2-3*xt1)*xt1**2-(2
     . *xt1**2-xt1-xt2)*xt)*xt+(4*xt1**2+xt2-(2*xt2+3)*xt1)*xt1**2)*
     . xgl)*xg2)+ans27
      ans28=((xt-xt2)**2+xgl**2-2*(xt+xt2)*xgl)*(log(xg2)-log(xt1))*(
     . xg2-xt2)**2*(xg2-1)*(xt2-1)**2
      ans25=ans26*ans28
      ans31=-((2*((2*(xt2+1)-3*xt1)*xt1-(3*xt2-2)*xt2)*xt-(2*xt**2-
     . xt1**2-4*xt1*xt2-xt2**2)*(xt1+xt2-2))*xgl**2+(xgl**4-2*xgl**3*
     . xt1-2*xgl**3*xt2+xt**4-2*xt**3*xt1-2*xt**3*xt2+xt**2*xt1**2+4*
     . xt**2*xt1*xt2+xt**2*xt2**2-2*xt*xt1**2*xt2-2*xt*xt1*xt2**2+xt1
     . **2*xt2**2)*(xt1+xt2-2)+2*((xt1**3+3*xt1**2*xt2+xt2**3+(3*xt2-
     . 8)*xt1*xt2)*xt-(xt1+xt2-2)*(xt1+xt2)*xt1*xt2+((2*(xt2+1)-3*xt1
     . )*xt1-(3*xt2-2)*xt2)*xt**2)*xgl)*xg2
      ans30=2*(((xt2-1)*xt2**3+xt1**4-(2*xt2+3)*xt1**2*xt2+(4*xt2-3)*
     . xt1*xt2**2+(4*xt2-1)*xt1**3)*xt+(((xt2-2)*xt2-3*xt1**2)*xt1-3*
     . (xt2-1)*xt2**2+(xt2+3)*xt1**2)*xt**2-(xt1**2-xt1+xt2**2-xt2)*(
     . xt1+xt2)*xt1*xt2)*xgl+(2*(((xt2-2)*xt2-3*xt1**2)*xt1-3*(xt2-1)
     . *xt2**2+(xt2+3)*xt1**2)*xt-(2*xt**2-xt1**2-4*xt1*xt2-xt2**2)*(
     . xt1**2-xt1+xt2**2-xt2))*xgl**2+(xgl**4-2*xgl**3*xt1-2*xgl**3*
     . xt2+xt**4-2*xt**3*xt1-2*xt**3*xt2+xt**2*xt1**2+4*xt**2*xt1*xt2
     . +xt**2*xt2**2-2*xt*xt1**2*xt2-2*xt*xt1*xt2**2+xt1**2*xt2**2)*(
     . xt1**2-xt1+xt2**2-xt2)+ans31
      ans32=((log(xg2)-log(xgl))**2*xgl+(log(xg2)-log(xt))**2*xt)*(
     . xg2-xt1)*(xg2-xt2)*(xg2-1)*(xt1-xt2)*(xt1-1)*(xt2-1)
      ans29=ans30*ans32
      ans41=-(2*(((2*xt2-1)*xt2**2+2*xt1**3+(3*xt2-8)*xt1*xt2+(3*xt2-
     . 1)*xt1**2)*xt+((2*(xt2+2)-5*xt1)*xt1-(5*xt2-4)*xt2)*xt**2+(xt
     . **3-xt1**2*xt2-xt1*xt2**2)*(xt1+xt2-2))*xgl+(2*((2*(xt2+2)-5*
     . xt1)*xt1-(5*xt2-4)*xt2)*xt-(6*xt**2-xt1**2-4*xt1*xt2-xt2**2)*(
     . xt1+xt2-2))*xgl**2+(xgl**4+2*xgl**3*xt-2*xgl**3*xt1-2*xgl**3*
     . xt2+xt**4-2*xt**3*xt1-2*xt**3*xt2+xt**2*xt1**2+4*xt**2*xt1*xt2
     . +xt**2*xt2**2-2*xt*xt1**2*xt2-2*xt*xt1*xt2**2+xt1**2*xt2**2)*(
     . xt1+xt2-2))*xg2
      ans40=(2*(((xt2-2)*xt2-5*xt1**2)*xt1-5*(xt2-1)*xt2**2+(xt2+5)*
     . xt1**2)*xt-(6*xt**2-xt1**2-4*xt1*xt2-xt2**2)*(xt1**2-xt1+xt2**
     . 2-xt2))*xgl**2+(xgl**4+2*xgl**3*xt-2*xgl**3*xt1-2*xgl**3*xt2+
     . xt**4-2*xt**3*xt1-2*xt**3*xt2+xt**2*xt1**2+4*xt**2*xt1*xt2+xt
     . **2*xt2**2-2*xt*xt1**2*xt2-2*xt*xt1*xt2**2+xt1**2*xt2**2)*(xt1
     . **2-xt1+xt2**2-xt2)+2*((2*(xt1**3+xt1**2*xt2-xt1**2-xt1*xt2**2
     . +xt1*xt2+xt2**3-xt2**2)*(xt1+xt2)-(2*xt2+3)*xt1**2*xt2+(4*xt2-
     . 3)*xt1*xt2**2)*xt+(xt**3-xt1**2*xt2-xt1*xt2**2)*(xt1**2-xt1+
     . xt2**2-xt2)+(((xt2-2)*xt2-5*xt1**2)*xt1-5*(xt2-1)*xt2**2+(xt2+
     . 5)*xt1**2)*xt**2)*xgl+ans41
      ans42=(xg2-1)*(xt1-1)*(xt2-1)
      ans39=2*ans40*ans42
      ans43=-((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)*((xt-xt2)**2+xgl**2-
     . 2*(xt+xt2)*xgl)*(xg2-xt1)*(xg2-xt2)*(xt1-xt2)**2*log(xg2)
      ans38=ans39+ans43
      ans44=(xg2-xt2)*(xt1-xt2)
      ans37=ans38*ans44
      ans45=-((2*((3*xt2-2-xt1)*xt+(2*xt2-1)*xt2-xt1)*xgl*xt2-(((2*
     . xt2-1)*xt2-xt1)*xgl**2-(2*xt*xt1*xt2-xt*xt1-4*xt*xt2**2+3*xt*
     . xt2-xt1*xt2+2*xt2**3-xt2**2)*(xt-xt2)))*xt2-(2*(((2*xt2-1)*xt2
     . -xt1)*xt+((xt2-2)*xt1+xt2**2)*xt2)*xgl-(((xt2-2)*xt1+xt2**2)*
     . xgl**2-(xt*xt1-3*xt*xt2+2*xt+xt1*xt2-2*xt1+xt2**2)*(xt-xt2)*
     . xt2))*xg2)*((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)*(log(xg2)-log(
     . xt2))*(xg2-xt1)*(xg2-1)*(xt1-1)**2
      ans36=ans37+ans45
      ans46=(xg2-xt1)
      ans35=ans36*ans46
      ans49=-((2*((xt2+2-3*xt1)*xt-(2*xt1**2-xt1-xt2))*xgl*xt1+(4*xt*
     . xt1**2-2*xt*xt1*xt2-3*xt*xt1+xt*xt2-2*xt1**3+xt1**2+xt1*xt2)*(
     . xt-xt1)+(2*xt1**2-xt1-xt2)*xgl**2)*xt1-((3*xt*xt1-xt*xt2-2*xt-
     . xt1**2-xt1*xt2+2*xt2)*(xt-xt1)*xt1+(xt1**2+xt1*xt2-2*xt2)*xgl
     . **2-2*((2*xt1**2-xt1-xt2)*xt+(xt1**2+xt1*xt2-2*xt2)*xt1)*xgl)*
     . xg2)*((xt-xt2)**2+xgl**2-2*(xt+xt2)*xgl)*(log(xg2)-log(xt1))*(
     . xg2-xt2)*(xt2-1)
      ans48=2*(((xt1**2-2*xt2)*xt1**2+(2*xt1+xt2)*(xt2-1)*xt2**2+(2*
     . xt2-1)*xt1**3-((xt1-1)*xt1+(xt2-1)*xt2)*xt**2+2*(((xt2-2)*xt2-
     . 2*xt1**2)*xt1-2*(xt2-1)*xt2**2+(xt2+2)*xt1**2)*xt)*xgl-((((xt1
     . +xt2)*(xt2-2)+2*xt1**2)*xt1+2*(xt2-1)*xt2**2+((xt1-1)*xt1+(xt2
     . -1)*xt2)*xt)*xgl**2-(((xt1-1)*xt1+(xt2-1)*xt2)*xgl**3+(xt*xt1
     . **2-xt*xt1+xt*xt2**2-xt*xt2-xt1**3+xt1**2-xt2**3+xt2**2)*(xt-
     . xt1)*(xt-xt2)))+(((2*((2*xt2-1)*xt2+2*xt1**2-(2*xt2+1)*xt1)+(
     . xt2-2+xt1)*xt)*xt-((2*(xt2-2)*xt2+xt1**2)*xt1+(xt2-1)*xt2**2+(
     . 2*xt2-1)*xt1**2))*xgl+((xt1+xt2)*(2*xt2-3)+2*xt1**2+(xt2-2+xt1
     . )*xt)*xgl**2-((xt2-2+xt1)*xgl**3+(xt*xt1+xt*xt2-2*xt-xt1**2+
     . xt1-xt2**2+xt2)*(xt-xt1)*(xt-xt2)))*xg2)*(log(xg2)-log(xt))*(
     . xg2-xt1)*(xt1-xt2)*(xt1-1)*xt+ans49
      ans50=(xg2-xt2)*(xg2-1)*(xt2-1)
      ans47=ans48*ans50
      ans34=ans35+ans47
      ans51=(log(xg2)-log(xgl))*xgl
      ans33=2*ans34*ans51
      ans60=-(2*(((2*xt2-1)*xt2**2+2*xt1**3+(3*xt2-8)*xt1*xt2+(3*xt2-
     . 1)*xt1**2)*xt+((2*(xt2+2)-5*xt1)*xt1-(5*xt2-4)*xt2)*xt**2+(xt
     . **3-xt1**2*xt2-xt1*xt2**2)*(xt1+xt2-2))*xgl+(2*((2*(xt2+2)-5*
     . xt1)*xt1-(5*xt2-4)*xt2)*xt-(6*xt**2-xt1**2-4*xt1*xt2-xt2**2)*(
     . xt1+xt2-2))*xgl**2+(xgl**4+2*xgl**3*xt-2*xgl**3*xt1-2*xgl**3*
     . xt2+xt**4-2*xt**3*xt1-2*xt**3*xt2+xt**2*xt1**2+4*xt**2*xt1*xt2
     . +xt**2*xt2**2-2*xt*xt1**2*xt2-2*xt*xt1*xt2**2+xt1**2*xt2**2)*(
     . xt1+xt2-2))*xg2
      ans59=(2*(((xt2-2)*xt2-5*xt1**2)*xt1-5*(xt2-1)*xt2**2+(xt2+5)*
     . xt1**2)*xt-(6*xt**2-xt1**2-4*xt1*xt2-xt2**2)*(xt1**2-xt1+xt2**
     . 2-xt2))*xgl**2+(xgl**4+2*xgl**3*xt-2*xgl**3*xt1-2*xgl**3*xt2+
     . xt**4-2*xt**3*xt1-2*xt**3*xt2+xt**2*xt1**2+4*xt**2*xt1*xt2+xt
     . **2*xt2**2-2*xt*xt1**2*xt2-2*xt*xt1*xt2**2+xt1**2*xt2**2)*(xt1
     . **2-xt1+xt2**2-xt2)+2*((2*(xt1**3+xt1**2*xt2-xt1**2-xt1*xt2**2
     . +xt1*xt2+xt2**3-xt2**2)*(xt1+xt2)-(2*xt2+3)*xt1**2*xt2+(4*xt2-
     . 3)*xt1*xt2**2)*xt+(xt**3-xt1**2*xt2-xt1*xt2**2)*(xt1**2-xt1+
     . xt2**2-xt2)+(((xt2-2)*xt2-5*xt1**2)*xt1-5*(xt2-1)*xt2**2+(xt2+
     . 5)*xt1**2)*xt**2)*xgl+ans60
      ans61=(xg2-1)*(xt1-1)*(xt2-1)
      ans58=2*ans59*ans61
      ans62=-((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)*((xt-xt2)**2+xgl**2-
     . 2*(xt+xt2)*xgl)*(xg2-xt1)*(xg2-xt2)*(xt1-xt2)**2*log(xg2)
      ans57=ans58+ans62
      ans63=(xg2-xt2)*(xt1-xt2)
      ans56=ans57*ans63
      ans64=-((2*(3*xt2-2-xt1)*(xt+xt2)*xgl*xt2-((2*xt2-1)*xt2-xt1)*(
     . xt-xt2)**2-((4*xt2-3)*xt2-(2*xt2-1)*xt1)*xgl**2)*xt2-(2*((2*
     . xt2-1)*xt2-xt1)*(xt+xt2)*xgl-((xt2-2)*xt1+xt2**2)*(xt-xt2)**2-
     . (3*xt2-2-xt1)*xgl**2*xt2)*xg2)*((xt-xt1)**2+xgl**2-2*(xt+xt1)*
     . xgl)*(log(xg2)-log(xt2))*(xg2-xt1)*(xg2-1)*(xt1-1)**2
      ans55=ans56+ans64
      ans65=(xg2-xt1)
      ans54=ans55*ans65
      ans66=-((2*(xt2+2-3*xt1)*(xt+xt1)*xgl*xt1+(xt-xt1)**2*(2*xt1**2
     . -xt1-xt2)+(4*xt1**2+xt2-(2*xt2+3)*xt1)*xgl**2)*xt1+(2*(xt+xt1)
     . *(2*xt1**2-xt1-xt2)*xgl-(xt-xt1)**2*(xt1**2+xt1*xt2-2*xt2)+(
     . xt2+2-3*xt1)*xgl**2*xt1)*xg2)*((xt-xt2)**2+xgl**2-2*(xt+xt2)*
     . xgl)*(log(xg2)-log(xt1))*(xg2-xt2)**2*(xg2-1)*(xt2-1)**2
      ans53=ans54+ans66
      ans67=(log(xg2)-log(xt))*xt
      ans52=2*ans53*ans67
      ans19=-2*(((8*xt1**2-xt2-(2*xt2+5)*xt1)*xt1**2-(4*xt1**2+xt2-(2
     . *xt2+3)*xt1)*(xt+2*xt1)*xt)*xgl+(4*xt1**2+xt2-(2*xt2+3)*xt1)*
     . xgl**3+(4*xt*xt1**2-2*xt*xt1*xt2-3*xt*xt1+xt*xt2-2*xt1**3+xt1
     . **2+xt1*xt2)*(xt-xt1)**2-((10*xt1**2+xt2-(4*xt2+7)*xt1)*xt1+(4
     . *xt1**2+xt2-(2*xt2+3)*xt1)*xt)*xgl**2-(((5*xt1**2-4*xt2+(xt2-2
     . )*xt1)*xt1+(xt2+2-3*xt1)*(xt+2*xt1)*xt)*xgl-((xt2+2-3*xt1)*xgl
     . **3-(3*xt*xt1-xt*xt2-2*xt-xt1**2-xt1*xt2+2*xt2)*(xt-xt1)**2)-(
     . 7*xt1**2-2*xt2-(xt2+4)*xt1-(xt2+2-3*xt1)*xt)*xgl**2)*xg2)*((xt
     . -xt2)**2+xgl**2-2*(xt+xt2)*xgl)*(xg2-xt2)**2*(xg2-1)*(xt2-1)**
     . 2*t134(mt1,mt,mg,m2)*xg2+ans20+ans25+ans29+ans33+ans52
      ans2=2*((((8*xt2-5)*xt2-(2*xt2+1)*xt1)*xt2**2-((4*xt2-3)*xt2-(2
     . *xt2-1)*xt1)*(xt+2*xt2)*xt)*xgl+((4*xt2-3)*xt2-(2*xt2-1)*xt1)*
     . xgl**3-(2*xt*xt1*xt2-xt*xt1-4*xt*xt2**2+3*xt*xt2-xt1*xt2+2*xt2
     . **3-xt2**2)*(xt-xt2)**2-(((10*xt2-7)*xt2-(4*xt2-1)*xt1)*xt2+((
     . 4*xt2-3)*xt2-(2*xt2-1)*xt1)*xt)*xgl**2-((((5*xt2-2)*xt2+(xt2-4
     . )*xt1)*xt2-(3*xt2-2-xt1)*(xt+2*xt2)*xt)*xgl+(3*xt2-2-xt1)*xgl
     . **3-(xt*xt1-3*xt*xt2+2*xt+xt1*xt2-2*xt1+xt2**2)*(xt-xt2)**2-((
     . 7*xt2-4)*xt2-(xt2+2)*xt1+(3*xt2-2-xt1)*xt)*xgl**2)*xg2)*((xt-
     . xt1)**2+xgl**2-2*(xt+xt1)*xgl)*(xg2-xt1)**2*(xg2-1)*(xt1-1)**2
     . *t134(mt2,mt,mg,m2)*xg2+ans3+ans19
      ans68=(st2-1)*st2*xg2
      ans1=ans2*ans68
      r82p2=ans1/(4*((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)*((xt-xt2)**2+
     . xgl**2-2*(xt+xt2)*xgl)*(xg2-xt1)**2*(xg2-xt2)**2*(xg2-1)*(xt1-
     . xt2)*(xt1-1)**2*(xt2-1)**2)

      ans7=((xt-xt2)**2+xgl**2-2*(xt+xt2)*xgl)*(xt2-1)**2
      ans6=(((((7*xt1**2+xt2-(3*xt2+5)*xt1)*xt1+2*(4*xt1**2+xt2-(2*
     . xt2+3)*xt1)*xt)*xgl-((4*xt1**2+xt2-(2*xt2+3)*xt1)*xgl**2+(4*xt
     . *xt1**2-2*xt*xt1*xt2-3*xt*xt1+xt*xt2-3*xt1**3+xt1**2*xt2+2*xt1
     . **2)*(xt-xt1))-((5*xt1**2-xt2-(xt2+3)*xt1-2*(xt2+2-3*xt1)*xt)*
     . xgl+(xt2+2-3*xt1)*xgl**2-(3*xt*xt1-xt*xt2-2*xt-2*xt1**2+xt1+
     . xt2)*(xt-xt1))*xg2)*st2-(((5*xt1**2+xt2-3*(xt2+1)*xt1)*xt1+2*(
     . 3*xt1**2+xt2-2*(xt2+1)*xt1)*xt)*xgl-((3*xt1**2+xt2-2*(xt2+1)*
     . xt1)*xgl**2+(3*xt*xt1**2-2*xt*xt1*xt2-2*xt*xt1+xt*xt2-2*xt1**3
     . +xt1**2*xt2+xt1**2)*(xt-xt1))-((3*xt1**2-xt2-(xt2+1)*xt1-2*(
     . xt2+1-2*xt1)*xt)*xgl+(xt2+1-2*xt1)*xgl**2-(2*xt*xt1-xt*xt2-xt-
     . xt1**2+xt2)*(xt-xt1))*xg2))*(xg2-xt2)**2*(xg2-1)*t134(mt1,mt,
     . mg,m2)-((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)*(xg2-xt2-(xt1-xt2)*
     . st2)*(xt1-xt2)**2*(xt1-1)**2*t134(m2,mt,mg,m2))*ans7
      ans8=-((((((7*xt2-5)*xt2-(3*xt2-1)*xt1)*xt2+2*((4*xt2-3)*xt2-(2
     . *xt2-1)*xt1)*xt)*xgl-(((4*xt2-3)*xt2-(2*xt2-1)*xt1)*xgl**2-(2*
     . xt*xt1*xt2-xt*xt1-4*xt*xt2**2+3*xt*xt2-xt1*xt2**2+3*xt2**3-2*
     . xt2**2)*(xt-xt2))-(((5*xt2-3)*xt2-(xt2+1)*xt1+2*(3*xt2-2-xt1)*
     . xt)*xgl-((3*xt2-2-xt1)*xgl**2-(xt*xt1-3*xt*xt2+2*xt-xt1+2*xt2
     . **2-xt2)*(xt-xt2)))*xg2)*st2-((xt-xt2)**2+xgl**2-2*(xt+xt2)*
     . xgl)*(xg2-xt2)*(xt2-1))*(xg2-1)*(xt1-1)**2*t134(mt2,mt,mg,m2)+
     . ((xt-xt2)**2+xgl**2-2*(xt+xt2)*xgl)*((xt1-xt2)*st2+xt2-1)*(xg2
     . -xt2)**2*(xt1-xt2)**2*t134(mu,mt,mg,m2))*((xt-xt1)**2+xgl**2-2
     . *(xt+xt1)*xgl)*(xg2-xt1)**2
      ans5=ans6+ans8
      ans4=2*ans5*xg2
      ans12=-(2*(2*((xt2-1+xt1)*xt1+xt2**2-xt2-1)*st2-(2*xt2+1+xt1)*(
     . xt2-1))*xt+(16*xt1**2-5*xt1*xt2-9*xt1+16*xt2**2-9*xt2-9)*(xt1+
     . xt2)*st2-(xt1+8*xt2)*(xt1+2*xt2+1)*(xt2-1))*xgl**3+(2*(2*((xt2
     . -1+xt1)*xt1+xt2**2-xt2-1)*st2-(2*xt2+1+xt1)*(xt2-1))*(3*xt1**2
     . +2*xt1*xt2+3*xt2**2-xt**2)*xt-(((40*xt1**2-23*xt1*xt2-19*xt1+
     . 40*xt2**2-19*xt2-19)*(xt1+xt2)*st2+(xt1+2*xt2+1)*(xt1-20*xt2)*
     . (xt2-1))*xt**2+((2*xt1**2-19*xt1*xt2+5*xt1+2*xt2**2+5*xt2+5)*(
     . xt1+xt2)*st2+(6*xt1-xt2)*(xt1+2*xt2+1)*(xt2-1))*xt1*xt2))*xgl+
     . ((((5*xt2-1+8*xt1)*xt1**2+(5*xt2**2-5*xt2-4)*xt2)*xt1+(8*xt2**
     . 2-xt2-1)*xt2**2-(8*xt2**2+5*xt2+1)*xt1**2)*st2+(3*xt1**2-2*xt1
     . *xt2-4*xt2**2)*(xt1+2*xt2+1)*(xt2-1))*xt**2
      ans11=((((5*xt2-1+8*xt1)*xt1**2+(5*xt2**2-5*xt2-4)*xt2)*xt1+(8*
     . xt2**2-xt2-1)*xt2**2-(8*xt2**2+5*xt2+1)*xt1**2)*st2+(3*xt1**2-
     . 2*xt1*xt2-4*xt2**2)*(xt1+2*xt2+1)*(xt2-1)-((40*xt1**2-23*xt1*
     . xt2-19*xt1+40*xt2**2-19*xt2-19)*(xt1+xt2)*st2+(xt1+2*xt2+1)*(
     . xt1-20*xt2)*(xt2-1))*xt-4*(2*((xt2-1+xt1)*xt1+xt2**2-xt2-1)*
     . st2-(2*xt2+1+xt1)*(xt2-1))*xt**2)*xgl**2+(2*((xt2-1+xt1)*xt1+
     . xt2**2-xt2-1)*st2-(2*xt2+1+xt1)*(xt2-1))*(4*xt**4-3*xt1**2*xt2
     . **2+4*xgl**4)-(((16*xt1**2-5*xt1*xt2-9*xt1+16*xt2**2-9*xt2-9)*
     . (xt1+xt2)*st2-(xt1+8*xt2)*(xt1+2*xt2+1)*(xt2-1))*xt**2+((2*xt1
     . **2-19*xt1*xt2+5*xt1+2*xt2**2+5*xt2+5)*(xt1+xt2)*st2+(6*xt1-
     . xt2)*(xt1+2*xt2+1)*(xt2-1))*xt1*xt2)*xt+ans12
      ans13=(xt1-xt2)*(xt1-1)*(xt2-1)*xg2**3
      ans10=2*ans11*ans13
      ans17=(2*(((xt1**2+xt2**2)*(xt2-1)+(xt2+1)*xt1**3+(xt2**2+xt2-4
     . )*xt1*xt2)*st2-((xt2+2)*xt1+xt2)*(xt2-1)*xt2)*(3*xt1**2+2*xt1*
     . xt2+3*xt2**2-xt**2)*xt-(((20*xt1**3*xt2+20*xt1**3-21*xt1**2*
     . xt2**2-xt1**2*xt2-20*xt1**2+20*xt1*xt2**3-xt1*xt2**2-17*xt1*
     . xt2+20*xt2**3-20*xt2**2)*(xt1+xt2)*st2+(xt1*xt2+2*xt1+xt2)*(
     . xt1-20*xt2)*(xt2-1)*xt2)*xt**2+((xt1**3*xt2+xt1**3-7*xt1**2*
     . xt2**2-6*xt1**2*xt2-xt1**2+xt1*xt2**3-6*xt1*xt2**2+17*xt1*xt2+
     . xt2**3-xt2**2)*(xt1+xt2)*st2+(xt1*xt2+2*xt1+xt2)*(6*xt1-xt2)*(
     . xt2-1)*xt2)*xt1*xt2))*xgl+(2*(2*((xt2+1)*xt1**5+(xt2-1)*xt2**4
     . )+(2*xt2-1)*(xt2+2)*xt1*xt2**3+(xt2**2-2*xt2-1)*xt1**2*xt2**2+
     . (xt2**2+3*xt2-2)*xt1**4-(3*xt2**2+2*xt2+2)*xt1**3*xt2)*st2+(3*
     . xt1**2-2*xt1*xt2-4*xt2**2)*(xt1*xt2+2*xt1+xt2)*(xt2-1)*xt2)*xt
     . **2
      ans16=-(((8*xt1**3*xt2+8*xt1**3-7*xt1**2*xt2**2+xt1**2*xt2-8*
     . xt1**2+8*xt1*xt2**3+xt1*xt2**2-11*xt1*xt2+8*xt2**3-8*xt2**2)*(
     . xt1+xt2)*st2-(xt1*xt2+2*xt1+xt2)*(xt1+8*xt2)*(xt2-1)*xt2)*xt**
     . 2+((xt1**3*xt2+xt1**3-7*xt1**2*xt2**2-6*xt1**2*xt2-xt1**2+xt1*
     . xt2**3-6*xt1*xt2**2+17*xt1*xt2+xt2**3-xt2**2)*(xt1+xt2)*st2+(
     . xt1*xt2+2*xt1+xt2)*(6*xt1-xt2)*(xt2-1)*xt2)*xt1*xt2)*xt-(2*(((
     . xt1**2+xt2**2)*(xt2-1)+(xt2+1)*xt1**3+(xt2**2+xt2-4)*xt1*xt2)*
     . st2-((xt2+2)*xt1+xt2)*(xt2-1)*xt2)*xt+(8*xt1**3*xt2+8*xt1**3-7
     . *xt1**2*xt2**2+xt1**2*xt2-8*xt1**2+8*xt1*xt2**3+xt1*xt2**2-11*
     . xt1*xt2+8*xt2**3-8*xt2**2)*(xt1+xt2)*st2-(xt1*xt2+2*xt1+xt2)*(
     . xt1+8*xt2)*(xt2-1)*xt2)*xgl**3+ans17
      ans15=(2*(2*((xt2+1)*xt1**5+(xt2-1)*xt2**4)+(2*xt2-1)*(xt2+2)*
     . xt1*xt2**3+(xt2**2-2*xt2-1)*xt1**2*xt2**2+(xt2**2+3*xt2-2)*xt1
     . **4-(3*xt2**2+2*xt2+2)*xt1**3*xt2)*st2+(3*xt1**2-2*xt1*xt2-4*
     . xt2**2)*(xt1*xt2+2*xt1+xt2)*(xt2-1)*xt2-((20*xt1**3*xt2+20*xt1
     . **3-21*xt1**2*xt2**2-xt1**2*xt2-20*xt1**2+20*xt1*xt2**3-xt1*
     . xt2**2-17*xt1*xt2+20*xt2**3-20*xt2**2)*(xt1+xt2)*st2+(xt1*xt2+
     . 2*xt1+xt2)*(xt1-20*xt2)*(xt2-1)*xt2)*xt-4*(((xt1**2+xt2**2)*(
     . xt2-1)+(xt2+1)*xt1**3+(xt2**2+xt2-4)*xt1*xt2)*st2-((xt2+2)*xt1
     . +xt2)*(xt2-1)*xt2)*xt**2)*xgl**2+(((xt1**2+xt2**2)*(xt2-1)+(
     . xt2+1)*xt1**3+(xt2**2+xt2-4)*xt1*xt2)*st2-((xt2+2)*xt1+xt2)*(
     . xt2-1)*xt2)*(4*xt**4-3*xt1**2*xt2**2+4*xgl**4)+ans16
      ans18=(xt1-xt2)*(xt1-1)*(xt2-1)*xg2
      ans14=2*ans15*ans18
      ans21=((((xt2+1-4*xt1)*xt1+(xt2+4)*xt2)*xt1-(4*xt2-1)*xt2**2)*
     . st2-(3*xt1**2-2*xt1*xt2-4*xt2**2)*(xt2-1)+4*((xt2-2+xt1)*st2-(
     . xt2-1))*xt**2-(((2*xt2+19-20*xt1)*xt1-(20*xt2-19)*xt2)*st2-(
     . xt1-20*xt2)*(xt2-1))*xt)*xgl**2
      ans20=(((xt2+5)*xt2+xt1**2-(12*xt2-5)*xt1)*st2+(6*xt1-xt2)*(xt2
     . -1))*xt*xt1*xt2-((xt2-2+xt1)*st2-(xt2-1))*(4*xt**4-3*xt1**2*
     . xt2**2+4*xgl**4)+(((2*xt2-9+8*xt1)*xt1+(8*xt2-9)*xt2)*st2-(xt1
     . +8*xt2)*(xt2-1))*xt**3+((((xt2+1-4*xt1)*xt1+(xt2+4)*xt2)*xt1-(
     . 4*xt2-1)*xt2**2)*st2-(3*xt1**2-2*xt1*xt2-4*xt2**2)*(xt2-1))*xt
     . **2+(((2*xt2-9+8*xt1)*xt1+(8*xt2-9)*xt2)*st2-(xt1+8*xt2)*(xt2-
     . 1)+2*((xt2-2+xt1)*st2-(xt2-1))*xt)*xgl**3+((((xt2+5)*xt2+xt1**
     . 2-(12*xt2-5)*xt1)*st2+(6*xt1-xt2)*(xt2-1))*xt1*xt2-2*((xt2-2+
     . xt1)*st2-(xt2-1))*(3*xt1**2+2*xt1*xt2+3*xt2**2-xt**2)*xt-(((2*
     . xt2+19-20*xt1)*xt1-(20*xt2-19)*xt2)*st2-(xt1-20*xt2)*(xt2-1))*
     . xt**2)*xgl+ans21
      ans22=(xt1-xt2)*(xt1-1)*(xt2-1)*xg2**4
      ans19=2*ans20*ans22
      ans25=-((((((xt2-2)*xt2-20*xt1**2)*xt1-20*(xt2-1)*xt2**2+(xt2+
     . 20)*xt1**2)*st2-(xt1-20*xt2)*(xt2-1)*xt2)*xt+2*(((xt1-1)*xt1+(
     . xt2-1)*xt2)*st2-(xt2-1)*xt2)*(3*xt1**2+2*xt1*xt2+3*xt2**2-xt**
     . 2))*xt+(((6*(xt2-2)*xt2-xt1**2)*xt1-(xt2-1)*xt2**2+(6*xt2+1)*
     . xt1**2)*st2-(6*xt1-xt2)*(xt2-1)*xt2)*xt1*xt2)*xgl-((2*((xt2-2+
     . 2*xt1)*xt1**3+2*(xt2-1)*xt2**3)+(2*xt2+1)*xt1*xt2**2-(6*xt2-1)
     . *xt1**2*xt2)*st2+(3*xt1**2-2*xt1*xt2-4*xt2**2)*(xt2-1)*xt2-4*(
     . ((xt1-1)*xt1+(xt2-1)*xt2)*st2-(xt2-1)*xt2)*xt**2+((((xt2-2)*
     . xt2-20*xt1**2)*xt1-20*(xt2-1)*xt2**2+(xt2+20)*xt1**2)*st2-(xt1
     . -20*xt2)*(xt2-1)*xt2)*xt)*xgl**2
      ans24=((((xt2-8+8*xt1)*xt1+(xt2-2)*xt2)*xt1+8*(xt2-1)*xt2**2)*
     . st2-(xt1+8*xt2)*(xt2-1)*xt2)*xt**3-(((xt1-1)*xt1+(xt2-1)*xt2)*
     . st2-(xt2-1)*xt2)*(4*xt**4-3*xt1**2*xt2**2+4*xgl**4)-(((6*(xt2-
     . 2)*xt2-xt1**2)*xt1-(xt2-1)*xt2**2+(6*xt2+1)*xt1**2)*st2-(6*xt1
     . -xt2)*(xt2-1)*xt2)*xt*xt1*xt2+((((xt2-8+8*xt1)*xt1+(xt2-2)*xt2
     . )*xt1+8*(xt2-1)*xt2**2)*st2-(xt1+8*xt2)*(xt2-1)*xt2+2*(((xt1-1
     . )*xt1+(xt2-1)*xt2)*st2-(xt2-1)*xt2)*xt)*xgl**3-((2*((xt2-2+2*
     . xt1)*xt1**3+2*(xt2-1)*xt2**3)+(2*xt2+1)*xt1*xt2**2-(6*xt2-1)*
     . xt1**2*xt2)*st2+(3*xt1**2-2*xt1*xt2-4*xt2**2)*(xt2-1)*xt2)*xt
     . **2+ans25
      ans26=(xt1-xt2)*(xt1-1)*(xt2-1)*xt1*xt2
      ans23=2*ans24*ans26
      ans31=((2*(5*xt2+2+2*xt1)*xt1**4+(4*xt2**2+4*xt2-5)*xt2**3-(5*
     . xt2**2-xt2+5)*xt1**3-(5*xt2**2+10*xt2+4)*xt1**2*xt2+(10*xt2**2
     . +xt2-4)*xt1*xt2**2)*st2+(3*xt1**2-2*xt1*xt2-4*xt2**2)*(2*xt1*
     . xt2+xt1+xt2**2+2*xt2)*(xt2-1)-4*(((2*xt2+1+xt1)*xt1**2+(xt2**2
     . +xt2-3)*xt2+(2*xt2**2-2*xt2-3)*xt1)*st2-((2*xt2+1)*xt1+(xt2+2)
     . *xt2)*(xt2-1))*xt**2-((((39*xt2+20+20*xt1)*xt1-(4*xt2**2+20*
     . xt2+39))*xt1**2+(20*xt2**2+20*xt2-39)*xt2**2+(39*xt2**2-20*xt2
     . -36)*xt1*xt2)*st2+(2*xt1*xt2+xt1+xt2**2+2*xt2)*(xt1-20*xt2)*(
     . xt2-1))*xt)*xgl**2
      ans30=-((((17*xt2+8+8*xt1)*xt1+4*xt2**2-8*xt2-17)*xt1**2+(8*xt2
     . **2+8*xt2-17)*xt2**2+(17*xt2**2-8*xt2-20)*xt1*xt2)*st2-(2*xt1*
     . xt2+xt1+xt2**2+2*xt2)*(xt1+8*xt2)*(xt2-1)+2*(((2*xt2+1+xt1)*
     . xt1**2+(xt2**2+xt2-3)*xt2+(2*xt2**2-2*xt2-3)*xt1)*st2-((2*xt2+
     . 1)*xt1+(xt2+2)*xt2)*(xt2-1))*xt)*xgl**3+((((4*xt2-1-xt1)*xt1**
     . 3-(xt2**2+xt2+4)*xt2**2+(4*xt2**2+xt2-22)*xt1*xt2+(24*xt2**2+
     . xt2-4)*xt1**2)*st2-(2*xt1*xt2+xt1+xt2**2+2*xt2)*(6*xt1-xt2)*(
     . xt2-1))*xt1*xt2+2*(((2*xt2+1+xt1)*xt1**2+(xt2**2+xt2-3)*xt2+(2
     . *xt2**2-2*xt2-3)*xt1)*st2-((2*xt2+1)*xt1+(xt2+2)*xt2)*(xt2-1))
     . *(3*xt1**2+2*xt1*xt2+3*xt2**2-xt**2)*xt-((((39*xt2+20+20*xt1)*
     . xt1-(4*xt2**2+20*xt2+39))*xt1**2+(20*xt2**2+20*xt2-39)*xt2**2+
     . (39*xt2**2-20*xt2-36)*xt1*xt2)*st2+(2*xt1*xt2+xt1+xt2**2+2*xt2
     . )*(xt1-20*xt2)*(xt2-1))*xt**2)*xgl+ans31
      ans29=(((4*xt2-1-xt1)*xt1**3-(xt2**2+xt2+4)*xt2**2+(4*xt2**2+
     . xt2-22)*xt1*xt2+(24*xt2**2+xt2-4)*xt1**2)*st2-(2*xt1*xt2+xt1+
     . xt2**2+2*xt2)*(6*xt1-xt2)*(xt2-1))*xt*xt1*xt2+(((2*xt2+1+xt1)*
     . xt1**2+(xt2**2+xt2-3)*xt2+(2*xt2**2-2*xt2-3)*xt1)*st2-((2*xt2+
     . 1)*xt1+(xt2+2)*xt2)*(xt2-1))*(4*xt**4-3*xt1**2*xt2**2+4*xgl**4
     . )-((((17*xt2+8+8*xt1)*xt1+4*xt2**2-8*xt2-17)*xt1**2+(8*xt2**2+
     . 8*xt2-17)*xt2**2+(17*xt2**2-8*xt2-20)*xt1*xt2)*st2-(2*xt1*xt2+
     . xt1+xt2**2+2*xt2)*(xt1+8*xt2)*(xt2-1))*xt**3+((2*(5*xt2+2+2*
     . xt1)*xt1**4+(4*xt2**2+4*xt2-5)*xt2**3-(5*xt2**2-xt2+5)*xt1**3-
     . (5*xt2**2+10*xt2+4)*xt1**2*xt2+(10*xt2**2+xt2-4)*xt1*xt2**2)*
     . st2+(3*xt1**2-2*xt1*xt2-4*xt2**2)*(2*xt1*xt2+xt1+xt2**2+2*xt2)
     . *(xt2-1))*xt**2+ans30
      ans32=(xt1-xt2)*(xt1-1)*(xt2-1)*xg2**2
      ans28=2*ans29*ans32
      ans27=-ans28
      ans38=-((((xt1**2+2*xt2)*xt1**2-(2*xt1-xt2)*(xt2-1)*xt2**2-(2*
     . xt2+1)*xt1**3+(3*((xt1-1)*xt1+(xt2-1)*xt2)*xt-2*(xt2-2+xt1)*
     . xt1*xt2)*xt)*xgl+((xt1-1)*xt1+(xt2-1)*xt2)*xgl**3-(xt*xt1**2-
     . xt*xt1+xt*xt2**2-xt*xt2-xt1**3+xt1**2-xt2**3+xt2**2)*(xt-xt1)*
     . (xt-xt2)+(((xt2-2)*xt2-2*xt1**2)*xt1-2*(xt2-1)*xt2**2+(xt2+2)*
     . xt1**2-3*((xt1-1)*xt1+(xt2-1)*xt2)*xt)*xgl**2+(((2*xt2-1)*xt2+
     . 2*xt1**2-(2*xt2+1)*xt1+3*(xt2-2+xt1)*xt)*xgl**2-((xt2-2+xt1)*
     . xgl**3-(xt*xt1+xt*xt2-2*xt-xt1**2+xt1-xt2**2+xt2)*(xt-xt1)*(xt
     . -xt2))+((2*(xt2-2)*xt2-xt1**2)*xt1-(xt2-1)*xt2**2+(2*xt2+1)*
     . xt1**2+(2*((2*xt2-1)*xt1-xt2)-3*(xt2-2+xt1)*xt)*xt)*xgl)*xg2)*
     . st2+(xg2-xt2)*(xgl**2-2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2
     . )*(xgl-xt+xt1)*(xt2-1))*log(xg2)
      ans37=-(xg2-xt1)*(xgl**2-2*xgl*xt-2*xgl*xt1+xt**2-2*xt*xt1+xt1
     . **2)*(xgl-xt+xt2)*(xt1-1)*log(xt2)*st2-(st2-1)*(xg2-xt2)*(xgl
     . **2-2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)*(xgl-xt+xt1)*(
     . xt2-1)*log(xt1)+ans38
      ans36=3*((((xt1**2-2*xt2)*xt1**2+(2*xt1+xt2)*(xt2-1)*xt2**2+(2*
     . xt2-1)*xt1**3-((xt1-1)*xt1+(xt2-1)*xt2)*xt**2+2*(((xt2-2)*xt2-
     . 2*xt1**2)*xt1-2*(xt2-1)*xt2**2+(xt2+2)*xt1**2)*xt)*xgl-((((xt1
     . +xt2)*(xt2-2)+2*xt1**2)*xt1+2*(xt2-1)*xt2**2+((xt1-1)*xt1+(xt2
     . -1)*xt2)*xt)*xgl**2-(((xt1-1)*xt1+(xt2-1)*xt2)*xgl**3+(xt*xt1
     . **2-xt*xt1+xt*xt2**2-xt*xt2-xt1**3+xt1**2-xt2**3+xt2**2)*(xt-
     . xt1)*(xt-xt2)))+(((2*((2*xt2-1)*xt2+2*xt1**2-(2*xt2+1)*xt1)+(
     . xt2-2+xt1)*xt)*xt-((2*(xt2-2)*xt2+xt1**2)*xt1+(xt2-1)*xt2**2+(
     . 2*xt2-1)*xt1**2))*xgl+((xt1+xt2)*(2*xt2-3)+2*xt1**2+(xt2-2+xt1
     . )*xt)*xgl**2-((xt2-2+xt1)*xgl**3+(xt*xt1+xt*xt2-2*xt-xt1**2+
     . xt1-xt2**2+xt2)*(xt-xt1)*(xt-xt2)))*xg2)*st2+(xg2-xt2)*(xgl**2
     . -2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)*(xgl+xt-xt1)*(xt2-1
     . ))+ans37
      ans35=2*ans36
      ans39=((((xt1**2-2*xt2)*xt1**2+(2*xt1+xt2)*(xt2-1)*xt2**2+(2*
     . xt2-1)*xt1**3-((xt1-1)*xt1+(xt2-1)*xt2)*xt**2+2*(((xt2-2)*xt2-
     . 2*xt1**2)*xt1-2*(xt2-1)*xt2**2+(xt2+2)*xt1**2)*xt)*xgl-((((xt1
     . +xt2)*(xt2-2)+2*xt1**2)*xt1+2*(xt2-1)*xt2**2+((xt1-1)*xt1+(xt2
     . -1)*xt2)*xt)*xgl**2-(((xt1-1)*xt1+(xt2-1)*xt2)*xgl**3+(xt*xt1
     . **2-xt*xt1+xt*xt2**2-xt*xt2-xt1**3+xt1**2-xt2**3+xt2**2)*(xt-
     . xt1)*(xt-xt2)))+(((2*((2*xt2-1)*xt2+2*xt1**2-(2*xt2+1)*xt1)+(
     . xt2-2+xt1)*xt)*xt-((2*(xt2-2)*xt2+xt1**2)*xt1+(xt2-1)*xt2**2+(
     . 2*xt2-1)*xt1**2))*xgl+((xt1+xt2)*(2*xt2-3)+2*xt1**2+(xt2-2+xt1
     . )*xt)*xgl**2-((xt2-2+xt1)*xgl**3+(xt*xt1+xt*xt2-2*xt-xt1**2+
     . xt1-xt2**2+xt2)*(xt-xt1)*(xt-xt2)))*xg2)*st2+(xg2-xt2)*(xgl**2
     . -2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)*(xgl+xt-xt1)*(xt2-1
     . ))*(log(xg2)-log(xt))
      ans34=ans35+ans39
      ans40=(log(xg2)-log(xt))*(xg2-xt1)*(xg2-xt2)*(xg2-1)*(xt1-xt2)*
     . (xt1-1)*(xt2-1)*xt
      ans33=ans34*ans40
      ans46=((((xt1**2-2*xt2)*xt1**2+(2*xt1+xt2)*(xt2-1)*xt2**2+(2*
     . xt2-1)*xt1**3-((xt1-1)*xt1+(xt2-1)*xt2)*xt**2+2*(((xt2-2)*xt2-
     . 2*xt1**2)*xt1-2*(xt2-1)*xt2**2+(xt2+2)*xt1**2)*xt)*xgl-((((xt1
     . +xt2)*(xt2-2)+2*xt1**2)*xt1+2*(xt2-1)*xt2**2+((xt1-1)*xt1+(xt2
     . -1)*xt2)*xt)*xgl**2-(((xt1-1)*xt1+(xt2-1)*xt2)*xgl**3+(xt*xt1
     . **2-xt*xt1+xt*xt2**2-xt*xt2-xt1**3+xt1**2-xt2**3+xt2**2)*(xt-
     . xt1)*(xt-xt2)))+(((2*((2*xt2-1)*xt2+2*xt1**2-(2*xt2+1)*xt1)+(
     . xt2-2+xt1)*xt)*xt-((2*(xt2-2)*xt2+xt1**2)*xt1+(xt2-1)*xt2**2+(
     . 2*xt2-1)*xt1**2))*xgl+((xt1+xt2)*(2*xt2-3)+2*xt1**2+(xt2-2+xt1
     . )*xt)*xgl**2-((xt2-2+xt1)*xgl**3+(xt*xt1+xt*xt2-2*xt-xt1**2+
     . xt1-xt2**2+xt2)*(xt-xt1)*(xt-xt2)))*xg2)*st2+(xg2-xt2)*(xgl**2
     . -2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)*(xgl+xt-xt1)*(xt2-1
     . ))*log(xg2)
      ans45=(xg2-xt1)*(xgl**2-2*xgl*xt-2*xgl*xt1+xt**2-2*xt*xt1+xt1**
     . 2)*(xgl-xt-xt2)*(xt1-1)*log(xt2)*st2+(st2-1)*(xg2-xt2)*(xgl**2
     . -2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)*(xgl-xt-xt1)*(xt2-1
     . )*log(xt1)+2*(((2*((xt1-1)*xt1**2+(xt2-1)*xt2**2)-((xt1-1)*xt1
     . +(xt2-1)*xt2)*xt)*xt-((xt1-1)*xt1**3+(xt2-1)*xt2**3)+(2*((xt1-
     . 1)*xt1**2+(xt2-1)*xt2**2+((xt1-1)*xt1+(xt2-1)*xt2)*xt)-((xt1-1
     . )*xt1+(xt2-1)*xt2)*xgl)*xgl-((2*((xt1-1)*xt1+(xt2-1)*xt2)-(xt2
     . -2+xt1)*xt)*xt-((xt1-1)*xt1**2+(xt2-1)*xt2**2)+(2*((xt1-1)*xt1
     . +(xt2-1)*xt2+(xt2-2+xt1)*xt)-(xt2-2+xt1)*xgl)*xgl)*xg2)*st2-((
     . xt-xt2)**2+xgl**2-2*(xt+xt2)*xgl)*(xg2-xt2)*(xt2-1))*log(xt)*
     . xt+ans46
      ans44=3*((((xt1**2-2*xt2)*xt1**2+(2*xt1+xt2)*(xt2-1)*xt2**2+(2*
     . xt2-1)*xt1**3-((xt1-1)*xt1+(xt2-1)*xt2)*xt**2+2*(((xt2-2)*xt2-
     . 2*xt1**2)*xt1-2*(xt2-1)*xt2**2+(xt2+2)*xt1**2)*xt)*xgl-((((xt1
     . +xt2)*(xt2-2)+2*xt1**2)*xt1+2*(xt2-1)*xt2**2+((xt1-1)*xt1+(xt2
     . -1)*xt2)*xt)*xgl**2-(((xt1-1)*xt1+(xt2-1)*xt2)*xgl**3+(xt*xt1
     . **2-xt*xt1+xt*xt2**2-xt*xt2-xt1**3+xt1**2-xt2**3+xt2**2)*(xt-
     . xt1)*(xt-xt2)))+(((2*((2*xt2-1)*xt2+2*xt1**2-(2*xt2+1)*xt1)+(
     . xt2-2+xt1)*xt)*xt-((2*(xt2-2)*xt2+xt1**2)*xt1+(xt2-1)*xt2**2+(
     . 2*xt2-1)*xt1**2))*xgl+((xt1+xt2)*(2*xt2-3)+2*xt1**2+(xt2-2+xt1
     . )*xt)*xgl**2-((xt2-2+xt1)*xgl**3+(xt*xt1+xt*xt2-2*xt-xt1**2+
     . xt1-xt2**2+xt2)*(xt-xt1)*(xt-xt2)))*xg2)*st2+(xg2-xt2)*(xgl**2
     . -2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)*(xgl+xt-xt1)*(xt2-1
     . ))+ans45
      ans43=2*ans44
      ans47=((((xt1**2-2*xt2)*xt1**2+(2*xt1+xt2)*(xt2-1)*xt2**2+(2*
     . xt2-1)*xt1**3-((xt1-1)*xt1+(xt2-1)*xt2)*xt**2+2*(((xt2-2)*xt2-
     . 2*xt1**2)*xt1-2*(xt2-1)*xt2**2+(xt2+2)*xt1**2)*xt)*xgl-((((xt1
     . +xt2)*(xt2-2)+2*xt1**2)*xt1+2*(xt2-1)*xt2**2+((xt1-1)*xt1+(xt2
     . -1)*xt2)*xt)*xgl**2-(((xt1-1)*xt1+(xt2-1)*xt2)*xgl**3+(xt*xt1
     . **2-xt*xt1+xt*xt2**2-xt*xt2-xt1**3+xt1**2-xt2**3+xt2**2)*(xt-
     . xt1)*(xt-xt2)))+(((2*((2*xt2-1)*xt2+2*xt1**2-(2*xt2+1)*xt1)+(
     . xt2-2+xt1)*xt)*xt-((2*(xt2-2)*xt2+xt1**2)*xt1+(xt2-1)*xt2**2+(
     . 2*xt2-1)*xt1**2))*xgl+((xt1+xt2)*(2*xt2-3)+2*xt1**2+(xt2-2+xt1
     . )*xt)*xgl**2-((xt2-2+xt1)*xgl**3+(xt*xt1+xt*xt2-2*xt-xt1**2+
     . xt1-xt2**2+xt2)*(xt-xt1)*(xt-xt2)))*xg2)*st2+(xg2-xt2)*(xgl**2
     . -2*xgl*xt-2*xgl*xt2+xt**2-2*xt*xt2+xt2**2)*(xgl+xt-xt1)*(xt2-1
     . ))*(log(xg2)-log(xgl))
      ans42=ans43+ans47
      ans48=(log(xg2)-log(xgl))*(xg2-xt1)*(xg2-xt2)*(xg2-1)*(xt1-xt2)
     . *(xt1-1)*(xt2-1)*xgl
      ans41=ans42*ans48
      ans9=-((2*((xt+2*xt1)*(xt-xt1)+xgl**2-(2*xt-xt1)*xgl)+((xt-xt1)
     . *xt+xgl**2-(2*xt+xt1)*xgl)*(log(xg2)-log(xt1)))*((xt-xt2)**2+
     . xgl**2-2*(xt+xt2)*xgl)*(log(xg2)-log(xt1))*(st2-1)*(xg2-xt2)*(
     . xt2-1)+(2*((xt+2*xt2)*(xt-xt2)+xgl**2-(2*xt-xt2)*xgl)+((xt-xt2
     . )*xt+xgl**2-(2*xt+xt2)*xgl)*(log(xg2)-log(xt2)))*((xt-xt1)**2+
     . xgl**2-2*(xt+xt1)*xgl)*(log(xg2)-log(xt2))*(xg2-xt1)*(xt1-1)*
     . st2)*(xg2-xt1)*(xg2-xt2)*(xg2-1)*(xt1-xt2)*(xt1-1)*(xt2-1)+
     . ans10+ans14+ans19+ans23+ans27+ans33+ans41
      ans3=ans4+ans9
      ans2=ans3*s2t*sxgl*sxt*xg2
      ans1=-ans2
      r82pp2=ans1/(2*((xt-xt1)**2+xgl**2-2*(xt+xt1)*xgl)*((xt-xt2)**2
     . +xgl**2-2*(xt+xt2)*xgl)*(xg2-xt1)**2*(xg2-xt2)**2*(xg2-1)*(xt1
     . -xt2)*(xt1-1)**2*(xt2-1)**2)

      r822 = r822 + r82p2 + r82pp2

      r82=r812+r822

c--r9
      ans7=-((4*(xg2+1-xb1)*xb1**2+(xb2-xg2)*(xb2-1)*xb2-(xb2**2-xb2*
     . xg2-xb2+5*xg2)*xb1)*(xb2-xg2)*(xb2-1)*xb2+(3*xb1**3*xb2**2-xb1
     . **3*xb2*xg2-xb1**3*xb2-xb1**3*xg2-8*xb1**2*xb2**3+3*xb1**2*xb2
     . **2*xg2+3*xb1**2*xb2**2+xb1**2*xb2*xg2**2-2*xb1**2*xb2*xg2+xb1
     . **2*xb2+xb1**2*xg2**2+xb1**2*xg2+8*xb1*xb2**3*xg2+8*xb1*xb2**3
     . -6*xb1*xb2**2*xg2**2-9*xb1*xb2**2*xg2-6*xb1*xb2**2+3*xb1*xb2*
     . xg2**2+3*xb1*xb2*xg2-xb1*xg2**2-xb2**5+2*xb2**4*xg2+2*xb2**4-
     . xb2**3*xg2**2-12*xb2**3*xg2-xb2**3+8*xb2**2*xg2**2+8*xb2**2*
     . xg2-5*xb2*xg2**2)*(xb1-xb2)*sb2**2)
      ans6=(((6*xb2**2+xg2)*(xg2+1)-11*xb2**3+(xg2**2-5*xg2+1)*xb2)*
     . xb1**3+(3*xb2**2-xg2-(xg2+1)*xb2)*xb1**4+2*(xb2**2-xb2*xg2-xb2
     . +3*xg2)*(xb2-xg2)*(xb2-1)*xb2**2+((7*xb2**2+6*xg2)*(xg2+1)*xb2
     . +(2*xb2**2+xg2)*(2*xb2**2-xg2)-(9*xg2**2+11*xg2+9)*xb2**2)*xb1
     . **2-(2*xb2**4+9*xg2**2-9*(xg2+1)*xb2*xg2-(2*xg2**2-11*xg2+2)*
     . xb2**2)*xb1*xb2)*sb2+ans7
      ans8=(xb1-1)*(xg2-1)
      ans5=ans6*ans8
      ans9=((xb1-xb2)*sb2+xb2-1)**2*(xb1-xb2)*(xb1-xg2)*(xb2-xg2)**2*
     . log(xg2)*xb2
      ans4=ans5+ans9
      ans10=(log(xb2)-log(xg2))*(xb1-xg2)*sb2
      ans3=2*ans4*ans10
      ans23=-4*xb1**2*xb2**3*xg2**2+2*xb1**2*xb2**3*xg2+4*xb1**2*xb2
     . **3+4*xb1**2*xb2**2*xg2**3+2*xb1**2*xb2**2*xg2**2-4*xb1**2*xb2
     . **2*xg2-2*xb1**2*xb2**2-2*xb1**2*xb2*xg2**3+2*xb1**2*xb2*xg2
      ans22=-4*sb2*xb1*xb2**3*xg2-sb2*xb1*xb2**3-3*sb2*xb1*xb2**2*xg2
     . **3+sb2*xb1*xb2**2*xg2**2+2*sb2*xb1*xb2**2*xg2+sb2*xb1*xb2*xg2
     . **3-sb2*xb1*xb2*xg2**2+sb2*xb2**5*xg2**2-sb2*xb2**5*xg2-sb2*
     . xb2**4*xg2**3-sb2*xb2**4*xg2**2+2*sb2*xb2**4*xg2+2*sb2*xb2**3*
     . xg2**3-sb2*xb2**3*xg2**2-sb2*xb2**3*xg2-sb2*xb2**2*xg2**3+sb2*
     . xb2**2*xg2**2+4*xb1**4*xb2**3*xg2-4*xb1**4*xb2**3-4*xb1**4*xb2
     . **2*xg2**2-4*xb1**4*xb2**2*xg2+8*xb1**4*xb2**2+8*xb1**4*xb2*
     . xg2**2-4*xb1**4*xb2*xg2-4*xb1**4*xb2-4*xb1**4*xg2**2+4*xb1**4*
     . xg2-4*xb1**3*xb2**4*xg2+4*xb1**3*xb2**4+2*xb1**3*xb2**3*xg2**2
     . +4*xb1**3*xb2**3*xg2-6*xb1**3*xb2**3+2*xb1**3*xb2**2*xg2**3-4*
     . xb1**3*xb2**2*xg2**2+2*xb1**3*xb2**2*xg2-4*xb1**3*xb2*xg2**3+2
     . *xb1**3*xb2*xg2**2+2*xb1**3*xb2+2*xb1**3*xg2**3-2*xb1**3*xg2+2
     . *xb1**2*xb2**4*xg2**2-2*xb1**2*xb2**4-2*xb1**2*xb2**3*xg2**3+
     . ans23
      ans21=-3*sb2*xb1**3*xb2**3*xg2**2-11*sb2*xb1**3*xb2**3*xg2+14*
     . sb2*xb1**3*xb2**3-8*sb2*xb1**3*xb2**2*xg2**3+6*sb2*xb1**3*xb2
     . **2*xg2**2-3*sb2*xb1**3*xb2**2*xg2+5*sb2*xb1**3*xb2**2+16*sb2*
     . xb1**3*xb2*xg2**3-3*sb2*xb1**3*xb2*xg2**2-5*sb2*xb1**3*xb2*xg2
     . -8*sb2*xb1**3*xb2-8*sb2*xb1**3*xg2**3+8*sb2*xb1**3*xg2-3*sb2*
     . xb1**2*xb2**5*xg2+3*sb2*xb1**2*xb2**5-2*sb2*xb1**2*xb2**4*xg2
     . **2+3*sb2*xb1**2*xb2**4*xg2-sb2*xb1**2*xb2**4+5*sb2*xb1**2*xb2
     . **3*xg2**3+2*sb2*xb1**2*xb2**3*xg2-7*sb2*xb1**2*xb2**3-6*sb2*
     . xb1**2*xb2**2*xg2**3+2*sb2*xb1**2*xb2**2*xg2**2-sb2*xb1**2*xb2
     . **2*xg2+5*sb2*xb1**2*xb2**2-3*sb2*xb1**2*xb2*xg2**3+4*sb2*xb1
     . **2*xb2*xg2**2-sb2*xb1**2*xb2*xg2+4*sb2*xb1**2*xg2**3-4*sb2*
     . xb1**2*xg2**2+sb2*xb1*xb2**5*xg2**2-sb2*xb1*xb2**5-sb2*xb1*xb2
     . **4*xg2**3-3*sb2*xb1*xb2**4*xg2**2+2*sb2*xb1*xb2**4*xg2+2*sb2*
     . xb1*xb2**4+3*sb2*xb1*xb2**3*xg2**3+2*sb2*xb1*xb2**3*xg2**2+
     . ans22
      ans20=-sb2**2*xb1*xb2**5*xg2**2+sb2**2*xb1*xb2**5+sb2**2*xb1*
     . xb2**4*xg2**3-sb2**2*xb1*xb2**4*xg2**2+2*sb2**2*xb1*xb2**4*xg2
     . -2*sb2**2*xb1*xb2**4+sb2**2*xb1*xb2**3*xg2**3+2*sb2**2*xb1*xb2
     . **3*xg2**2-4*sb2**2*xb1*xb2**3*xg2+sb2**2*xb1*xb2**3-6*sb2**2*
     . xb1*xb2**2*xg2**3+4*sb2**2*xb1*xb2**2*xg2**2+2*sb2**2*xb1*xb2
     . **2*xg2+4*sb2**2*xb1*xb2*xg2**3-4*sb2**2*xb1*xb2*xg2**2-sb2**2
     . *xb2**5*xg2**2+sb2**2*xb2**5*xg2+sb2**2*xb2**4*xg2**3+sb2**2*
     . xb2**4*xg2**2-2*sb2**2*xb2**4*xg2-2*sb2**2*xb2**3*xg2**3+sb2**
     . 2*xb2**3*xg2**2+sb2**2*xb2**3*xg2+sb2**2*xb2**2*xg2**3-sb2**2*
     . xb2**2*xg2**2-12*sb2*xb1**4*xb2**3*xg2+12*sb2*xb1**4*xb2**3+12
     . *sb2*xb1**4*xb2**2*xg2**2+12*sb2*xb1**4*xb2**2*xg2-24*sb2*xb1
     . **4*xb2**2-24*sb2*xb1**4*xb2*xg2**2+12*sb2*xb1**4*xb2*xg2+12*
     . sb2*xb1**4*xb2+12*sb2*xb1**4*xg2**2-12*sb2*xb1**4*xg2+11*sb2*
     . xb1**3*xb2**4*xg2-11*sb2*xb1**3*xb2**4+ans21
      ans19=-11*sb2**2*xb1**4*xg2**2+11*sb2**2*xb1**4*xg2+sb2**2*xb1
     . **4-11*sb2**2*xb1**3*xb2**4*xg2+11*sb2**2*xb1**3*xb2**4+5*sb2
     . **2*xb1**3*xb2**3*xg2**2+11*sb2**2*xb1**3*xb2**3*xg2-16*sb2**2
     . *xb1**3*xb2**3+5*sb2**2*xb1**3*xb2**2*xg2**3-13*sb2**2*xb1**3*
     . xb2**2*xg2**2+8*sb2**2*xb1**3*xb2**2*xg2-13*sb2**2*xb1**3*xb2*
     . xg2**3+8*sb2**2*xb1**3*xb2*xg2**2+5*sb2**2*xb1**3*xb2+8*sb2**2
     . *xb1**3*xg2**3-8*sb2**2*xb1**3*xg2+3*sb2**2*xb1**2*xb2**5*xg2-
     . 3*sb2**2*xb1**2*xb2**5+4*sb2**2*xb1**2*xb2**4*xg2**2-3*sb2**2*
     . xb1**2*xb2**4*xg2-sb2**2*xb1**2*xb2**4-7*sb2**2*xb1**2*xb2**3*
     . xg2**3-4*sb2**2*xb1**2*xb2**3*xg2**2+11*sb2**2*xb1**2*xb2**3+
     . 12*sb2**2*xb1**2*xb2**2*xg2**3-5*sb2**2*xb1**2*xb2**2*xg2-7*
     . sb2**2*xb1**2*xb2**2-5*sb2**2*xb1**2*xb2*xg2**2+5*sb2**2*xb1**
     . 2*xb2*xg2-5*sb2**2*xb1**2*xg2**3+5*sb2**2*xb1**2*xg2**2+ans20
      ans18=-4*log(xg2)*xb1**2*xb2**3*xg2-log(xg2)*xb1**2*xb2**2*xg2
     . **3+2*log(xg2)*xb1**2*xb2**2*xg2**2+2*log(xg2)*xb1**2*xb2**2*
     . xg2+2*log(xg2)*xb1**2*xb2*xg2**3-log(xg2)*xb1**2*xb2*xg2**2-
     . log(xg2)*xb1**2*xg2**3-log(xg2)*xb1*xb2**4*xg2**2+log(xg2)*xb1
     . *xb2**3*xg2**3+2*log(xg2)*xb1*xb2**3*xg2**2-2*log(xg2)*xb1*xb2
     . **2*xg2**3-log(xg2)*xb1*xb2**2*xg2**2+log(xg2)*xb1*xb2*xg2**3+
     . sb2**2*xb1**6*xb2*xg2-sb2**2*xb1**6*xb2-sb2**2*xb1**6*xg2+sb2
     . **2*xb1**6-sb2**2*xb1**5*xb2**2*xg2+sb2**2*xb1**5*xb2**2-2*sb2
     . **2*xb1**5*xb2*xg2**2+sb2**2*xb1**5*xb2*xg2+sb2**2*xb1**5*xb2+
     . 2*sb2**2*xb1**5*xg2**2-2*sb2**2*xb1**5+8*sb2**2*xb1**4*xb2**3*
     . xg2-8*sb2**2*xb1**4*xb2**3-6*sb2**2*xb1**4*xb2**2*xg2**2-8*sb2
     . **2*xb1**4*xb2**2*xg2+14*sb2**2*xb1**4*xb2**2+sb2**2*xb1**4*
     . xb2*xg2**3+17*sb2**2*xb1**4*xb2*xg2**2-11*sb2**2*xb1**4*xb2*
     . xg2-7*sb2**2*xb1**4*xb2-sb2**2*xb1**4*xg2**3+ans19
      ans17=-2*log(xg2)*sb2*xb1**3*xb2**3-6*log(xg2)*sb2*xb1**3*xb2**
     . 2*xg2**2-6*log(xg2)*sb2*xb1**3*xb2**2*xg2-2*log(xg2)*sb2*xb1**
     . 3*xb2*xg2**3+6*log(xg2)*sb2*xb1**3*xb2*xg2**2+2*log(xg2)*sb2*
     . xb1**3*xg2**3-4*log(xg2)*sb2*xb1**2*xb2**4*xg2+4*log(xg2)*sb2*
     . xb1**2*xb2**3*xg2+4*log(xg2)*sb2*xb1**2*xb2**2*xg2**3-4*log(
     . xg2)*sb2*xb1**2*xb2*xg2**3+2*log(xg2)*sb2*xb1*xb2**4*xg2**2-2*
     . log(xg2)*sb2*xb1*xb2**3*xg2**3-2*log(xg2)*sb2*xb1*xb2**3*xg2**
     . 2+2*log(xg2)*sb2*xb1*xb2**2*xg2**3+log(xg2)*xb1**4*xb2**3-log(
     . xg2)*xb1**4*xb2**2*xg2-2*log(xg2)*xb1**4*xb2**2+2*log(xg2)*xb1
     . **4*xb2*xg2+log(xg2)*xb1**4*xb2-log(xg2)*xb1**4*xg2-log(xg2)*
     . xb1**3*xb2**4-log(xg2)*xb1**3*xb2**3*xg2+2*log(xg2)*xb1**3*xb2
     . **3+2*log(xg2)*xb1**3*xb2**2*xg2**2+2*log(xg2)*xb1**3*xb2**2*
     . xg2-log(xg2)*xb1**3*xb2**2-4*log(xg2)*xb1**3*xb2*xg2**2-log(
     . xg2)*xb1**3*xb2*xg2+2*log(xg2)*xb1**3*xg2**2+2*log(xg2)*xb1**2
     . *xb2**4*xg2-log(xg2)*xb1**2*xb2**3*xg2**2+ans18
      ans16=log(xg2)*sb2**2*xb1**6*xb2-log(xg2)*sb2**2*xb1**6*xg2-3*
     . log(xg2)*sb2**2*xb1**5*xb2**2+log(xg2)*sb2**2*xb1**5*xb2*xg2+2
     . *log(xg2)*sb2**2*xb1**5*xg2**2+3*log(xg2)*sb2**2*xb1**4*xb2**3
     . +3*log(xg2)*sb2**2*xb1**4*xb2**2*xg2-5*log(xg2)*sb2**2*xb1**4*
     . xb2*xg2**2-log(xg2)*sb2**2*xb1**4*xg2**3-log(xg2)*sb2**2*xb1**
     . 3*xb2**4-5*log(xg2)*sb2**2*xb1**3*xb2**3*xg2+3*log(xg2)*sb2**2
     . *xb1**3*xb2**2*xg2**2+3*log(xg2)*sb2**2*xb1**3*xb2*xg2**3+2*
     . log(xg2)*sb2**2*xb1**2*xb2**4*xg2+log(xg2)*sb2**2*xb1**2*xb2**
     . 3*xg2**2-3*log(xg2)*sb2**2*xb1**2*xb2**2*xg2**3-log(xg2)*sb2**
     . 2*xb1*xb2**4*xg2**2+log(xg2)*sb2**2*xb1*xb2**3*xg2**3+2*log(
     . xg2)*sb2*xb1**5*xb2**2-2*log(xg2)*sb2*xb1**5*xb2*xg2-2*log(xg2
     . )*sb2*xb1**5*xb2+2*log(xg2)*sb2*xb1**5*xg2-4*log(xg2)*sb2*xb1
     . **4*xb2**3+4*log(xg2)*sb2*xb1**4*xb2**2+4*log(xg2)*sb2*xb1**4*
     . xb2*xg2**2-4*log(xg2)*sb2*xb1**4*xg2**2+2*log(xg2)*sb2*xb1**3*
     . xb2**4+6*log(xg2)*sb2*xb1**3*xb2**3*xg2+ans17
      ans24=(xb2-xg2)
      ans15=ans16*ans24
      ans14=-ans15
      ans13=(((2*(3*xb2**2+xg2)*(xg2+1)*xb2-(xg2**2+4*xg2+1)*xg2-(3*
     . xg2**2+4*xg2+3)*xb2**2)*xb1**4-(((3*xb2**2+xg2)*xb2-2*(xg2+1)*
     . xg2)*xb1**5-((xb2**2-xg2)*xb1**6-(xb2-xg2)**2*(xb2-1)**2*xb2**
     . 2*xg2))-(xb2**4+2*xg2**2-2*(xb2**2+2*xg2)*(xg2+1)*xb2+(xg2**2+
     . 7*xg2+1)*xb2**2)*xb1*xb2*xg2+(xb2**6+4*xb2*xg2**3+4*xb2*xg2**2
     . -xg2**3+2*(xg2**2+6*xg2+1)*(xg2+1)*xb2**3-(3*xg2**2+4*xg2+3)*
     . xb2**4-2*(4*xg2**2+7*xg2+4)*xb2**2*xg2)*xb1**2+(2*(3*xb2**4+
     . xg2**2)*(xg2+1)-3*xb2**5-6*(xg2**2+4*xg2+1)*xb2**3+2*(xg2**2+6
     . *xg2+1)*(xg2+1)*xb2**2-(xg2**2+7*xg2+1)*xb2*xg2)*xb1**3)*sb2-(
     . 2*(2*(xg2+1)-xb1)*xb1**4-(xb2-xg2)*(xb2-1)*xb2*xg2+(xb2**2-xb2
     . *xg2-xb2-xg2)*xb1*xg2-(xb2**2-xb2*xg2-xb2+2*xg2**2+9*xg2+2)*
     . xb1**3+(xb2**3-xb2**2*xg2-xb2**2+xb2*xg2+4*xg2**2+4*xg2)*xb1**
     . 2)*(xb2-xg2)*(xb2-1)*xb2)*(log(xb2)-log(xg2))*(xg2-1)*sb2+
     . ans14
      ans25=(log(xb1)-log(xg2))*(sb2-1)
      ans12=2*ans13*ans25
      ans11=-(((((2*(xg2+1)+xb2)*xb1**2-(3*xb1**3+xb1*xg2+xb2*xg2))*
     . sb2+(xb1**2-xg2)*(xb1-xb2))*((3*xb1-xb2)*sb2-3*xb1)*(log(xb1)-
     . log(xg2))**2*(sb2-1)*(xb2-xg2)*(xb2-1)**2*(xg2-1)-(((xb1-xb2)*
     . sb2+xb2-1)**2*(log(xg2)+4)*(xb1-xg2)*(xb2-xg2)*log(xg2)+4*(sb2
     . **2*xb1**2-sb2**2*xb1*xg2-sb2**2*xb1+sb2**2*xb2**2-sb2**2*xb2*
     . xg2-sb2**2*xb2+2*sb2**2*xg2-2*sb2*xb2**2+2*sb2*xb2*xg2+2*sb2*
     . xb2-2*sb2*xg2+xb2**2-xb2*xg2-xb2+xg2)*(xb1-1)*(xb2-1)*(xg2-1))
     . *((xb1-xb2)*sb2-xb1)*(xb1-xb2)*(xb1-xg2))*(xb2-xg2)+(((3*xb2**
     . 2+xg2-2*(xg2+1)*xb2)*xb2-(xb2**2-xg2)*xb1)*sb2-2*(xb2-xg2)*(
     . xb2-1)*xb2)*((xb1-3*xb2)*sb2-xb1)*(log(xb2)-log(xg2))**2*(xb1-
     . xg2)**2*(xb1-1)**2*(xg2-1)*sb2)+ans12
      ans2=ans3+ans11
      ans1=ans2*xg2
      r912=ans1/(16*(xb1-xb2)*(xb1-xg2)**2*(xb1-1)**2*(xb2-xg2)**2*(
     . xb2-1)**2*(xg2-1))

      ans6=(log(xb2)-log(xg2))*(xg2-1)
      ans5=(3*((2*(3*xb2**2+xg2)*(xg2+1)*xb2-(xg2**2+4*xg2+1)*xg2-(3*
     . xg2**2+4*xg2+3)*xb2**2)*xb1**4-(((3*xb2**2+xg2)*xb2-2*(xg2+1)*
     . xg2)*xb1**5-((xb2**2-xg2)*xb1**6-(xb2-xg2)**2*(xb2-1)**2*xb2**
     . 2*xg2))-(xb2**4+2*xg2**2-2*(xb2**2+2*xg2)*(xg2+1)*xb2+(xg2**2+
     . 7*xg2+1)*xb2**2)*xb1*xb2*xg2+(xb2**6+4*xb2*xg2**3+4*xb2*xg2**2
     . -xg2**3+2*(xg2**2+6*xg2+1)*(xg2+1)*xb2**3-(3*xg2**2+4*xg2+3)*
     . xb2**4-2*(4*xg2**2+7*xg2+4)*xb2**2*xg2)*xb1**2+(2*(3*xb2**4+
     . xg2**2)*(xg2+1)-3*xb2**5-6*(xg2**2+4*xg2+1)*xb2**3+2*(xg2**2+6
     . *xg2+1)*(xg2+1)*xb2**2-(xg2**2+7*xg2+1)*xb2*xg2)*xb1**3)*sb2-(
     . 2*(2*(xg2+1)-xb1)*xb1**4-3*(xb2-xg2)*(xb2-1)*xb2*xg2-(xb2**2-
     . xb2*xg2-xb2+3*xg2)*xb1*xg2-(7*xb2**2-7*xb2*xg2-7*xb2+2*xg2**2+
     . 15*xg2+2)*xb1**3+(3*xb2**3+xb2**2*xg2+xb2**2-4*xb2*xg2**2-5*
     . xb2*xg2-4*xb2+8*xg2**2+8*xg2)*xb1**2)*(xb2-xg2)*(xb2-1)*xb2)*
     . ans6
      ans7=(((3*(4*xb1**4-xb2**2*xg2)-(25*xb2+8*xg2+8)*xb1**3-(3*xb2*
     . xg2+3*xb2+5*xg2)*xb1*xb2+(9*xb2**2+15*xb2*xg2+15*xb2+4*xg2)*
     . xb1**2)*(xb2-xg2)*(xb2-1)-3*(xb1**5-2*xb1**4*xg2-2*xb1**4+8*
     . xb1**3*xb2**2-8*xb1**3*xb2*xg2-8*xb1**3*xb2+xb1**3*xg2**2+12*
     . xb1**3*xg2+xb1**3-3*xb1**2*xb2**3-3*xb1**2*xb2**2*xg2-3*xb1**2
     . *xb2**2+6*xb1**2*xb2*xg2**2+9*xb1**2*xb2*xg2+6*xb1**2*xb2-8*
     . xb1**2*xg2**2-8*xb1**2*xg2+xb1*xb2**3*xg2+xb1*xb2**3-xb1*xb2**
     . 2*xg2**2+2*xb1*xb2**2*xg2-xb1*xb2**2-3*xb1*xb2*xg2**2-3*xb1*
     . xb2*xg2+5*xb1*xg2**2+xb2**3*xg2-xb2**2*xg2**2-xb2**2*xg2+xb2*
     . xg2**2)*(xb1-xb2)*sb2)*(xb2-1)*(xg2-1)-(3*(xb1-xb2)*sb2+2*(xb2
     . -1))*(xb1-xb2)**2*(xb1-xg2)**2*(xb2-xg2)*log(xg2)*xb1)*(xb2-
     . xg2)
      ans4=ans5+ans7
      ans8=(log(xb1)-log(xg2))
      ans3=2*ans4*ans8
      ans12=(xb1-xg2)
      ans11=2*((((2*((xb2**2-2*xg2)*(xg2+1)-6*xb2**3+(3*xg2**2+2*xg2+
     . 3)*xb2+(2*(2*xb2**2+xg2)-3*(xg2+1)*xb2)*xb1)*xb1+3*xb2**4+7*
     . xg2**2+2*(3*xb2**2-2*xg2)*(xg2+1)*xb2-7*(xg2**2+1)*xb2**2)*xb1
     . -(3*xb2**4+11*xg2**2-2*(3*xb2**2+8*xg2)*(xg2+1)*xb2+3*(xg2**2+
     . 8*xg2+1)*xb2**2)*xb2)*xb2+3*(3*xb1**3*xb2**2-xb1**3*xb2*xg2-
     . xb1**3*xb2-xb1**3*xg2-8*xb1**2*xb2**3+3*xb1**2*xb2**2*xg2+3*
     . xb1**2*xb2**2+xb1**2*xb2*xg2**2-2*xb1**2*xb2*xg2+xb1**2*xb2+
     . xb1**2*xg2**2+xb1**2*xg2+8*xb1*xb2**3*xg2+8*xb1*xb2**3-6*xb1*
     . xb2**2*xg2**2-9*xb1*xb2**2*xg2-6*xb1*xb2**2+3*xb1*xb2*xg2**2+3
     . *xb1*xb2*xg2-xb1*xg2**2-xb2**5+2*xb2**4*xg2+2*xb2**4-xb2**3*
     . xg2**2-12*xb2**3*xg2-xb2**3+8*xb2**2*xg2**2+8*xb2**2*xg2-5*xb2
     . *xg2**2)*(xb1-xb2)*sb2)*(xb1-1)*(xg2-1)-(3*xb2-2-xb1+3*(xb1-
     . xb2)*sb2)*(xb1-xb2)**2*(xb1-xg2)*(xb2-xg2)**2*log(xg2)*xb2)*(
     . log(xb2)-log(xg2))*ans12
      ans13=(4*((2*(xb2**2+xg2)-(xg2+1)*xb2-xb1*xb2)*xb1-(3*xb2**2+4*
     . xg2-3*(xg2+1)*xb2)*xb2-3*(xb1**2-xb1*xg2-xb1+xb2**2-xb2*xg2-
     . xb2+2*xg2)*(xb1-xb2)*sb2)*(xb1-1)*(xb2-1)*(xg2-1)-(3*(xb1-xb2)
     . *sb2+3*xb2-2)*(log(xg2)+4)*(xb1-xb2)**2*(xb1-xg2)*(xb2-xg2)*
     . log(xg2))*(xb1-xb2)*(xb1-xg2)*(xb2-xg2)+(((4*(xg2+1)+3*xb2)*
     . xb1**2*xb2+12*xb1**4+5*xb1*xb2*xg2-3*xb2**2*xg2-(6*(xg2+1)+13*
     . xb2)*xb1**3-3*(3*xb1**3-xb1**2*xb2-2*xb1**2*xg2-2*xb1**2+xb1*
     . xg2+xb2*xg2)*(3*xb1-xb2)*sb2)*(log(xb1)-log(xg2))**2*(xb2-xg2)
     . **2*(xb2-1)**2+((3*(5*xb2**2+3*xg2-4*(xg2+1)*xb2)*xb2-(5*xb2**
     . 2-xg2-2*(xg2+1)*xb2)*xb1)*xb2-3*(xb1*xb2**2-xb1*xg2-3*xb2**3+2
     . *xb2**2*xg2+2*xb2**2-xb2*xg2)*(xb1-3*xb2)*sb2)*(log(xb2)-log(
     . xg2))**2*(xb1-xg2)**2*(xb1-1)**2)*(xg2-1)
      ans10=ans11+ans13
      ans9=-ans10
      ans2=ans3+ans9
      ans14=(sb2-1)*sb2*xg2
      ans1=ans2*ans14
      r91p2=ans1/(16*(xb1-xb2)*(xb1-xg2)**2*(xb1-1)**2*(xb2-xg2)**2*(
     . xb2-1)**2*(xg2-1))

      r912 = r912 + r91p2

      ans8=-(((xt1**3*xt2+xt1**3-3*xt1**2*xt2**2+2*xt1**2*xt2-xt1**2-
     . 8*xt1*xt2**3+9*xt1*xt2**2-3*xt1*xt2-2*xt2**4+12*xt2**3-8*xt2**
     . 2-(xt1**2*xt2+xt1**2-6*xt1*xt2**2+3*xt1*xt2-xt1-xt2**3+8*xt2**
     . 2-5*xt2)*xg2)*xg2-(3*xt1**3*xt2-xt1**3-8*xt1**2*xt2**2+3*xt1**
     . 2*xt2+xt1**2+8*xt1*xt2**2-6*xt1*xt2-xt2**4+2*xt2**3-xt2**2)*
     . xt2)*(xt1-xt2)*st2**2+(4*xg2*xt1**2+xg2*xt1*xt2-5*xg2*xt1-xg2*
     . xt2**2+xg2*xt2-4*xt1**3+4*xt1**2-xt1*xt2**2+xt1*xt2+xt2**3-xt2
     . **2)*(xg2-xt2)*(xt2-1)*xt2)
      ans7=((2*((xt2+1)*xt1-(xt2-1)*xt2)*(xt2-1)*xt2**2-(3*xt2-1)*xt1
     . **4-(4*xt2**2+7*xt2-9)*xt1**2*xt2+(11*xt2**2-6*xt2-1)*xt1**3)*
     . xt2-((xt2+1)*xt1**3+2*(xt2-1)*(xt2-3)*xt2**2-(3*xt2-1)**2*xt1
     . **2+(2*xt2**2+9*xt2-9)*xt1*xt2)*xg2**2+((xt2+1)*xt1**4+4*(xt2-
     . 1)*(xt2-2)*xt2**3-(3*xt2-1)*(2*xt2-1)*xt1**3+(11*xt2-9)*xt1*
     . xt2**2-(7*xt2**2-11*xt2+6)*xt1**2*xt2)*xg2)*st2+ans8
      ans9=(xg2-1)*(xt1-1)
      ans6=ans7*ans9
      ans10=((xt1-xt2)*st2+xt2-1)**2*(xg2-xt1)*(xg2-xt2)**2*(xt1-xt2)
     . *log(xg2)*xt2
      ans5=ans6+ans10
      ans11=(log(xg2)-log(xt2))*(xg2-xt1)*st2
      ans4=2*ans5*ans11
      ans17=(2*xg2**2*xt1**3-4*xg2**2*xt1**2+xg2**2*xt1*xt2+xg2**2*
     . xt1-xg2**2*xt2**2+xg2**2*xt2-4*xg2*xt1**4-xg2*xt1**3*xt2+9*xg2
     . *xt1**3+xg2*xt1**2*xt2**2-xg2*xt1**2*xt2-4*xg2*xt1**2-xg2*xt1*
     . xt2**2+xg2*xt1*xt2+xg2*xt2**3-xg2*xt2**2+2*xt1**5-4*xt1**4+xt1
     . **3*xt2**2-xt1**3*xt2+2*xt1**3-xt1**2*xt2**3+xt1**2*xt2**2)*(
     . xg2-xt2)*(xt2-1)*xt2
      ans16=(((xt2-1)**2*xt2**2+xt1**4+(xt2**2-4*xt2+2)*xt1*xt2-(2*
     . xt2**2-xt2+2)*xt1**3-(2*xt2**3-8*xt2**2+4*xt2-1)*xt1**2)*xg2**
     . 3-((xt1-3*xt2)*xt1**3+(xt2+2)*(xt2-1)**2*xt2+3*(2*xt2-1)*xt1**
     . 2-(3*xt2**3-6*xt2**2+6*xt2-2)*xt1)*xt1**2*xt2**2+((xt2-2+xt1)*
     . xt1**5+(xt1+xt2)*(xt2-1)**2*xt2**3+2*(2*xt2**2-7*xt2+4)*xt1**2
     . *xt2**2-(6*xt2**3-24*xt2**2+14*xt2-1)*xt1**3*xt2-(6*xt2**3-4*
     . xt2**2+2*xt2-1)*xt1**4)*xg2-(2*((xt2-1)**2*xt2**3+xt1**5)-(xt2
     . **2-4*xt2+2)*(3*xt2-2)*xt1**2*xt2+(2*xt2**2-7*xt2+4)*xt1*xt2**
     . 2-(3*xt2**2-2*xt2+4)*xt1**4-(6*xt2**3-14*xt2**2+7*xt2-2)*xt1**
     . 3)*xg2**2)*st2+ans17
      ans18=(log(xg2)-log(xt2))*(xg2-1)*st2
      ans15=ans16*ans18
      ans28=4*xg2*xt1**2*xt2**2-2*xg2*xt1**2*xt2+4*xt1**4*xt2**3-8*
     . xt1**4*xt2**2+4*xt1**4*xt2-4*xt1**3*xt2**4+6*xt1**3*xt2**3-2*
     . xt1**3*xt2+2*xt1**2*xt2**4-4*xt1**2*xt2**3+2*xt1**2*xt2**2
      ans27=st2*xg2*xt2**5-2*st2*xg2*xt2**4+st2*xg2*xt2**3-12*st2*xt1
     . **4*xt2**3+24*st2*xt1**4*xt2**2-12*st2*xt1**4*xt2+11*st2*xt1**
     . 3*xt2**4-14*st2*xt1**3*xt2**3-5*st2*xt1**3*xt2**2+8*st2*xt1**3
     . *xt2-3*st2*xt1**2*xt2**5+st2*xt1**2*xt2**4+7*st2*xt1**2*xt2**3
     . -5*st2*xt1**2*xt2**2+st2*xt1*xt2**5-2*st2*xt1*xt2**4+st2*xt1*
     . xt2**3-2*xg2**3*xt1**3*xt2**2+4*xg2**3*xt1**3*xt2-2*xg2**3*xt1
     . **3+2*xg2**3*xt1**2*xt2**3-4*xg2**3*xt1**2*xt2**2+2*xg2**3*xt1
     . **2*xt2+4*xg2**2*xt1**4*xt2**2-8*xg2**2*xt1**4*xt2+4*xg2**2*
     . xt1**4-2*xg2**2*xt1**3*xt2**3+4*xg2**2*xt1**3*xt2**2-2*xg2**2*
     . xt1**3*xt2-2*xg2**2*xt1**2*xt2**4+4*xg2**2*xt1**2*xt2**3-2*xg2
     . **2*xt1**2*xt2**2-4*xg2*xt1**4*xt2**3+4*xg2*xt1**4*xt2**2+4*
     . xg2*xt1**4*xt2-4*xg2*xt1**4+4*xg2*xt1**3*xt2**4-4*xg2*xt1**3*
     . xt2**3-2*xg2*xt1**3*xt2**2+2*xg2*xt1**3-2*xg2*xt1**2*xt2**3+
     . ans28
      ans26=st2*xg2**3*xt2**4-2*st2*xg2**3*xt2**3+st2*xg2**3*xt2**2-
     . 12*st2*xg2**2*xt1**4*xt2**2+24*st2*xg2**2*xt1**4*xt2-12*st2*
     . xg2**2*xt1**4+3*st2*xg2**2*xt1**3*xt2**3-6*st2*xg2**2*xt1**3*
     . xt2**2+3*st2*xg2**2*xt1**3*xt2+2*st2*xg2**2*xt1**2*xt2**4-2*
     . st2*xg2**2*xt1**2*xt2**2-4*st2*xg2**2*xt1**2*xt2+4*st2*xg2**2*
     . xt1**2-st2*xg2**2*xt1*xt2**5+3*st2*xg2**2*xt1*xt2**4-2*st2*xg2
     . **2*xt1*xt2**3-st2*xg2**2*xt1*xt2**2+st2*xg2**2*xt1*xt2-st2*
     . xg2**2*xt2**5+st2*xg2**2*xt2**4+st2*xg2**2*xt2**3-st2*xg2**2*
     . xt2**2+12*st2*xg2*xt1**4*xt2**3-12*st2*xg2*xt1**4*xt2**2-12*
     . st2*xg2*xt1**4*xt2+12*st2*xg2*xt1**4-11*st2*xg2*xt1**3*xt2**4+
     . 11*st2*xg2*xt1**3*xt2**3+3*st2*xg2*xt1**3*xt2**2+5*st2*xg2*xt1
     . **3*xt2-8*st2*xg2*xt1**3+3*st2*xg2*xt1**2*xt2**5-3*st2*xg2*xt1
     . **2*xt2**4-2*st2*xg2*xt1**2*xt2**3+st2*xg2*xt1**2*xt2**2+st2*
     . xg2*xt1**2*xt2-2*st2*xg2*xt1*xt2**4+4*st2*xg2*xt1*xt2**3-2*st2
     . *xg2*xt1*xt2**2+ans27
      ans25=-5*st2**2*xg2*xt1**2*xt2-2*st2**2*xg2*xt1*xt2**4+4*st2**2
     . *xg2*xt1*xt2**3-2*st2**2*xg2*xt1*xt2**2-st2**2*xg2*xt2**5+2*
     . st2**2*xg2*xt2**4-st2**2*xg2*xt2**3+st2**2*xt1**6*xt2-st2**2*
     . xt1**6-st2**2*xt1**5*xt2**2-st2**2*xt1**5*xt2+2*st2**2*xt1**5+
     . 8*st2**2*xt1**4*xt2**3-14*st2**2*xt1**4*xt2**2+7*st2**2*xt1**4
     . *xt2-st2**2*xt1**4-11*st2**2*xt1**3*xt2**4+16*st2**2*xt1**3*
     . xt2**3-5*st2**2*xt1**3*xt2+3*st2**2*xt1**2*xt2**5+st2**2*xt1**
     . 2*xt2**4-11*st2**2*xt1**2*xt2**3+7*st2**2*xt1**2*xt2**2-st2**2
     . *xt1*xt2**5+2*st2**2*xt1*xt2**4-st2**2*xt1*xt2**3+8*st2*xg2**3
     . *xt1**3*xt2**2-16*st2*xg2**3*xt1**3*xt2+8*st2*xg2**3*xt1**3-5*
     . st2*xg2**3*xt1**2*xt2**3+6*st2*xg2**3*xt1**2*xt2**2+3*st2*xg2
     . **3*xt1**2*xt2-4*st2*xg2**3*xt1**2+st2*xg2**3*xt1*xt2**4-3*st2
     . *xg2**3*xt1*xt2**3+3*st2*xg2**3*xt1*xt2**2-st2*xg2**3*xt1*xt2+
     . ans26
      ans24=11*st2**2*xg2**2*xt1**4-5*st2**2*xg2**2*xt1**3*xt2**3+13*
     . st2**2*xg2**2*xt1**3*xt2**2-8*st2**2*xg2**2*xt1**3*xt2-4*st2**
     . 2*xg2**2*xt1**2*xt2**4+4*st2**2*xg2**2*xt1**2*xt2**3+5*st2**2*
     . xg2**2*xt1**2*xt2-5*st2**2*xg2**2*xt1**2+st2**2*xg2**2*xt1*xt2
     . **5+st2**2*xg2**2*xt1*xt2**4-2*st2**2*xg2**2*xt1*xt2**3-4*st2
     . **2*xg2**2*xt1*xt2**2+4*st2**2*xg2**2*xt1*xt2+st2**2*xg2**2*
     . xt2**5-st2**2*xg2**2*xt2**4-st2**2*xg2**2*xt2**3+st2**2*xg2**2
     . *xt2**2-st2**2*xg2*xt1**6*xt2+st2**2*xg2*xt1**6+st2**2*xg2*xt1
     . **5*xt2**2-st2**2*xg2*xt1**5*xt2-8*st2**2*xg2*xt1**4*xt2**3+8*
     . st2**2*xg2*xt1**4*xt2**2+11*st2**2*xg2*xt1**4*xt2-11*st2**2*
     . xg2*xt1**4+11*st2**2*xg2*xt1**3*xt2**4-11*st2**2*xg2*xt1**3*
     . xt2**3-8*st2**2*xg2*xt1**3*xt2**2+8*st2**2*xg2*xt1**3-3*st2**2
     . *xg2*xt1**2*xt2**5+3*st2**2*xg2*xt1**2*xt2**4+5*st2**2*xg2*xt1
     . **2*xt2**2+ans25
      ans23=-2*log(xg2)*xg2*xt1**4*xt2+log(xg2)*xg2*xt1**4+log(xg2)*
     . xg2*xt1**3*xt2**3-2*log(xg2)*xg2*xt1**3*xt2**2+log(xg2)*xg2*
     . xt1**3*xt2-2*log(xg2)*xg2*xt1**2*xt2**4+4*log(xg2)*xg2*xt1**2*
     . xt2**3-2*log(xg2)*xg2*xt1**2*xt2**2-log(xg2)*xt1**4*xt2**3+2*
     . log(xg2)*xt1**4*xt2**2-log(xg2)*xt1**4*xt2+log(xg2)*xt1**3*xt2
     . **4-2*log(xg2)*xt1**3*xt2**3+log(xg2)*xt1**3*xt2**2-st2**2*xg2
     . **3*xt1**4*xt2+st2**2*xg2**3*xt1**4-5*st2**2*xg2**3*xt1**3*xt2
     . **2+13*st2**2*xg2**3*xt1**3*xt2-8*st2**2*xg2**3*xt1**3+7*st2**
     . 2*xg2**3*xt1**2*xt2**3-12*st2**2*xg2**3*xt1**2*xt2**2+5*st2**2
     . *xg2**3*xt1**2-st2**2*xg2**3*xt1*xt2**4-st2**2*xg2**3*xt1*xt2
     . **3+6*st2**2*xg2**3*xt1*xt2**2-4*st2**2*xg2**3*xt1*xt2-st2**2*
     . xg2**3*xt2**4+2*st2**2*xg2**3*xt2**3-st2**2*xg2**3*xt2**2+2*
     . st2**2*xg2**2*xt1**5*xt2-2*st2**2*xg2**2*xt1**5+6*st2**2*xg2**
     . 2*xt1**4*xt2**2-17*st2**2*xg2**2*xt1**4*xt2+ans24
      ans22=-6*log(xg2)*st2*xg2**2*xt1**3*xt2-2*log(xg2)*st2*xg2**2*
     . xt1*xt2**4+2*log(xg2)*st2*xg2**2*xt1*xt2**3+2*log(xg2)*st2*xg2
     . *xt1**5*xt2-2*log(xg2)*st2*xg2*xt1**5-6*log(xg2)*st2*xg2*xt1**
     . 3*xt2**3+6*log(xg2)*st2*xg2*xt1**3*xt2**2+4*log(xg2)*st2*xg2*
     . xt1**2*xt2**4-4*log(xg2)*st2*xg2*xt1**2*xt2**3-2*log(xg2)*st2*
     . xt1**5*xt2**2+2*log(xg2)*st2*xt1**5*xt2+4*log(xg2)*st2*xt1**4*
     . xt2**3-4*log(xg2)*st2*xt1**4*xt2**2-2*log(xg2)*st2*xt1**3*xt2
     . **4+2*log(xg2)*st2*xt1**3*xt2**3+log(xg2)*xg2**3*xt1**2*xt2**2
     . -2*log(xg2)*xg2**3*xt1**2*xt2+log(xg2)*xg2**3*xt1**2-log(xg2)*
     . xg2**3*xt1*xt2**3+2*log(xg2)*xg2**3*xt1*xt2**2-log(xg2)*xg2**3
     . *xt1*xt2-2*log(xg2)*xg2**2*xt1**3*xt2**2+4*log(xg2)*xg2**2*xt1
     . **3*xt2-2*log(xg2)*xg2**2*xt1**3+log(xg2)*xg2**2*xt1**2*xt2**3
     . -2*log(xg2)*xg2**2*xt1**2*xt2**2+log(xg2)*xg2**2*xt1**2*xt2+
     . log(xg2)*xg2**2*xt1*xt2**4-2*log(xg2)*xg2**2*xt1*xt2**3+log(
     . xg2)*xg2**2*xt1*xt2**2+log(xg2)*xg2*xt1**4*xt2**2+ans23
      ans21=log(xg2)*st2**2*xg2**3*xt1**4-3*log(xg2)*st2**2*xg2**3*
     . xt1**3*xt2+3*log(xg2)*st2**2*xg2**3*xt1**2*xt2**2-log(xg2)*st2
     . **2*xg2**3*xt1*xt2**3-2*log(xg2)*st2**2*xg2**2*xt1**5+5*log(
     . xg2)*st2**2*xg2**2*xt1**4*xt2-3*log(xg2)*st2**2*xg2**2*xt1**3*
     . xt2**2-log(xg2)*st2**2*xg2**2*xt1**2*xt2**3+log(xg2)*st2**2*
     . xg2**2*xt1*xt2**4+log(xg2)*st2**2*xg2*xt1**6-log(xg2)*st2**2*
     . xg2*xt1**5*xt2-3*log(xg2)*st2**2*xg2*xt1**4*xt2**2+5*log(xg2)*
     . st2**2*xg2*xt1**3*xt2**3-2*log(xg2)*st2**2*xg2*xt1**2*xt2**4-
     . log(xg2)*st2**2*xt1**6*xt2+3*log(xg2)*st2**2*xt1**5*xt2**2-3*
     . log(xg2)*st2**2*xt1**4*xt2**3+log(xg2)*st2**2*xt1**3*xt2**4+2*
     . log(xg2)*st2*xg2**3*xt1**3*xt2-2*log(xg2)*st2*xg2**3*xt1**3-4*
     . log(xg2)*st2*xg2**3*xt1**2*xt2**2+4*log(xg2)*st2*xg2**3*xt1**2
     . *xt2+2*log(xg2)*st2*xg2**3*xt1*xt2**3-2*log(xg2)*st2*xg2**3*
     . xt1*xt2**2-4*log(xg2)*st2*xg2**2*xt1**4*xt2+4*log(xg2)*st2*xg2
     . **2*xt1**4+6*log(xg2)*st2*xg2**2*xt1**3*xt2**2+ans22
      ans29=(xg2-xt2)
      ans20=ans21*ans29
      ans19=-ans20
      ans14=ans15+ans19
      ans30=(log(xg2)-log(xt1))*(st2-1)
      ans13=2*ans14*ans30
      ans12=((((xt2+2-3*xt1)*xt1**2+(2*xt1**2-xt1-xt2)*xg2)*st2-(xg2-
     . xt1**2)*(xt1-xt2))*((3*xt1-xt2)*st2-3*xt1)*(log(xg2)-log(xt1))
     . **2*(st2-1)*(xg2-xt2)*(xg2-1)*(xt2-1)**2-(((xt1-xt2)*st2+xt2-1
     . )**2*(log(xg2)+4)*(xg2-xt1)*(xg2-xt2)*log(xg2)-4*(st2**2*xg2*
     . xt1+st2**2*xg2*xt2-2*st2**2*xg2-st2**2*xt1**2+st2**2*xt1-st2**
     . 2*xt2**2+st2**2*xt2-2*st2*xg2*xt2+2*st2*xg2+2*st2*xt2**2-2*st2
     . *xt2+xg2*xt2-xg2-xt2**2+xt2)*(xg2-1)*(xt1-1)*(xt2-1))*((xt1-
     . xt2)*st2-xt1)*(xg2-xt1)*(xt1-xt2))*(xg2-xt2)+(((3*xt2-2-xt1)*
     . xt2**2-((2*xt2-1)*xt2-xt1)*xg2)*st2+2*(xg2-xt2)*(xt2-1)*xt2)*(
     . (xt1-3*xt2)*st2-xt1)*(log(xg2)-log(xt2))**2*(xg2-xt1)**2*(xg2-
     . 1)*(xt1-1)**2*st2+ans13
      ans3=ans4+ans12
      ans2=ans3*xg2
      ans1=-ans2
      r922=ans1/(8*(xg2-xt1)**2*(xg2-xt2)**2*(xg2-1)*(xt1-xt2)*(xt1-1
     . )**2*(xt2-1)**2)

      ans8=(2*xg2**2*xt1**3+4*xg2**2*xt1**2*xt2-8*xg2**2*xt1**2-xg2**
     . 2*xt1*xt2+3*xg2**2*xt1-3*xg2**2*xt2**2+3*xg2**2*xt2-4*xg2*xt1
     . **4-7*xg2*xt1**3*xt2+15*xg2*xt1**3-xg2*xt1**2*xt2**2+5*xg2*xt1
     . **2*xt2-8*xg2*xt1**2+xg2*xt1*xt2**2-xg2*xt1*xt2+3*xg2*xt2**3-3
     . *xg2*xt2**2+2*xt1**5-4*xt1**4+7*xt1**3*xt2**2-7*xt1**3*xt2+2*
     . xt1**3-3*xt1**2*xt2**3-xt1**2*xt2**2+4*xt1**2*xt2)*(xg2-xt2)*(
     . xt2-1)*xt2
      ans7=3*(((xt2-1)**2*xt2**2+xt1**4+(xt2**2-4*xt2+2)*xt1*xt2-(2*
     . xt2**2-xt2+2)*xt1**3-(2*xt2**3-8*xt2**2+4*xt2-1)*xt1**2)*xg2**
     . 3-((xt1-3*xt2)*xt1**3+(xt2+2)*(xt2-1)**2*xt2+3*(2*xt2-1)*xt1**
     . 2-(3*xt2**3-6*xt2**2+6*xt2-2)*xt1)*xt1**2*xt2**2+((xt2-2+xt1)*
     . xt1**5+(xt1+xt2)*(xt2-1)**2*xt2**3+2*(2*xt2**2-7*xt2+4)*xt1**2
     . *xt2**2-(6*xt2**3-24*xt2**2+14*xt2-1)*xt1**3*xt2-(6*xt2**3-4*
     . xt2**2+2*xt2-1)*xt1**4)*xg2-(2*((xt2-1)**2*xt2**3+xt1**5)-(xt2
     . **2-4*xt2+2)*(3*xt2-2)*xt1**2*xt2+(2*xt2**2-7*xt2+4)*xt1*xt2**
     . 2-(3*xt2**2-2*xt2+4)*xt1**4-(6*xt2**3-14*xt2**2+7*xt2-2)*xt1**
     . 3)*xg2**2)*st2+ans8
      ans9=(log(xg2)-log(xt2))*(xg2-1)
      ans6=ans7*ans9
      ans10=((3*((xt1**4-2*xt1**3+8*xt1**2*xt2**2-8*xt1**2*xt2+xt1**2
     . -3*xt1*xt2**3-3*xt1*xt2**2+6*xt1*xt2+xt2**3-xt2**2)*xt1+(xt1**
     . 3+6*xt1**2*xt2-8*xt1**2-xt1*xt2**2-3*xt1*xt2+5*xt1-xt2**2+xt2)
     . *xg2**2-(2*xt1**4+8*xt1**3*xt2-12*xt1**3+3*xt1**2*xt2**2-9*xt1
     . **2*xt2+8*xt1**2-xt1*xt2**3-2*xt1*xt2**2+3*xt1*xt2-xt2**3+xt2
     . **2)*xg2)*(xt1-xt2)*st2-(8*xg2*xt1**3-15*xg2*xt1**2*xt2-4*xg2*
     . xt1**2+3*xg2*xt1*xt2**2+5*xg2*xt1*xt2+3*xg2*xt2**2-12*xt1**4+
     . 25*xt1**3*xt2+8*xt1**3-9*xt1**2*xt2**2-15*xt1**2*xt2+3*xt1*xt2
     . **2)*(xg2-xt2)*(xt2-1))*(xg2-1)*(xt2-1)-(3*(xt1-xt2)*st2+2*(
     . xt2-1))*(xg2-xt1)**2*(xg2-xt2)*(xt1-xt2)**2*log(xg2)*xt1)*(xg2
     . -xt2)
      ans5=ans6+ans10
      ans11=(log(xg2)-log(xt1))
      ans4=2*ans5*ans11
      ans13=((((3*xt2+4)*xt2+12*xt1**2-(13*xt2+6)*xt1)*xt1**2-(6*xt1
     . **3-4*xt1**2*xt2-5*xt1*xt2+3*xt2**2)*xg2+3*((2*xt1**2-xt1-xt2)
     . *xg2-(3*xt1-xt2-2)*xt1**2)*(3*xt1-xt2)*st2)*(log(xg2)-log(xt1)
     . )**2*(xg2-xt2)**2*(xt2-1)**2-((((5*xt2-2)*xt1-3*(5*xt2-4)*xt2)
     . *xt2+(3*(4*xt2-3)*xt2-(2*xt2+1)*xt1)*xg2)*xt2-3*((xt1-2*xt2**2
     . +xt2)*xg2-(xt1-3*xt2+2)*xt2**2)*(xt1-3*xt2)*st2)*(log(xg2)-log
     . (xt2))**2*(xg2-xt1)**2*(xt1-1)**2)*(xg2-1)-(4*((3*(xt2-1)*xt2+
     . xt1**2-(2*xt2-1)*xt1)*xt2-((3*xt2-4)*xt2-(xt2-2)*xt1)*xg2+3*(
     . xt1**2-xt1+xt2**2-xt2-(xt1+xt2-2)*xg2)*(xt1-xt2)*st2)*(xg2-1)*
     . (xt1-1)*(xt2-1)+(3*(xt1-xt2)*st2+3*xt2-2)*(log(xg2)+4)*(xg2-
     . xt1)*(xg2-xt2)*(xt1-xt2)**2*log(xg2))*(xg2-xt1)*(xg2-xt2)*(xt1
     . -xt2)
      ans12=2*((((2*(4*xt2-3)*xt1**3-3*(xt2-1)**2*xt2**2+(3*xt2**2+6*
     . xt2-7)*xt1*xt2-2*(6*xt2**2-xt2-3)*xt1**2)*xt2-((3*xt2**2-16*
     . xt2+11)*xt2-2*(3*xt2-2)*xt1**2+(7*xt2**2+4*xt2-7)*xt1)*xg2**2+
     . 2*(((xt2**2+2*xt2-2-(3*xt2-2)*xt1)*xt1+(3*xt2**2-2)*xt2)*xt1+(
     . 3*xt2**2-12*xt2+8)*xt2**2)*xg2)*xt2-3*((xt1**3*xt2+xt1**3-3*
     . xt1**2*xt2**2+2*xt1**2*xt2-xt1**2-8*xt1*xt2**3+9*xt1*xt2**2-3*
     . xt1*xt2-2*xt2**4+12*xt2**3-8*xt2**2-(xt1**2*xt2+xt1**2-6*xt1*
     . xt2**2+3*xt1*xt2-xt1-xt2**3+8*xt2**2-5*xt2)*xg2)*xg2-(3*xt1**3
     . *xt2-xt1**3-8*xt1**2*xt2**2+3*xt1**2*xt2+xt1**2+8*xt1*xt2**2-6
     . *xt1*xt2-xt2**4+2*xt2**3-xt2**2)*xt2)*(xt1-xt2)*st2)*(xg2-1)*(
     . xt1-1)+(3*xt2-2-xt1+3*(xt1-xt2)*st2)*(xg2-xt1)*(xg2-xt2)**2*(
     . xt1-xt2)**2*log(xg2)*xt2)*(log(xg2)-log(xt2))*(xg2-xt1)+ans13
      ans3=ans4+ans12
      ans14=(st2-1)*st2*xg2
      ans2=ans3*ans14
      ans1=-ans2
      r92p2=ans1/(8*(xg2-xt1)**2*(xg2-xt2)**2*(xg2-1)*(xt1-xt2)*(xt1-
     . 1)**2*(xt2-1)**2)

      r922 = r922 + r92p2

      r92=r912+r922

c--rct
      ans7=((2*sb2**2*xb2-2*sb2*xb2+3*xgl)*(xb2+2)*(xb2-1)*xb2-2*(xb1
     . +2*xb2)*sb2**2*xb1**4+2*((4*sb2+1)*(2*xb2+1)*(xb2-1)-(8*xb2**2
     . -7*xb2-7)*sb2**2)*xb1**3-2*((sb2*xb2-xgl)*(xb2+1)*(xb2-1)**2-(
     . xb2**2-xb2-1)*sb2**2*xb2**2)*xb1-((8*sb2*xb2**2+6*sb2*xb2+4*
     . sb2-xb2**2-14*xb2*xgl-7*xgl+1)*(xb2-1)-2*(4*xb2**3-xb2**2-xb2-
     . 4)*sb2**2)*xb1**2)*(xb2-1)*xb1*xg2**2-((2*sb2**2*xb2-2*sb2*xb2
     . +3*xgl)*(2*xb2+1)*(xb2-1)-4*sb2**2*xb1**4+2*((4*sb2+1)*(xb2-1)
     . -(5*xb2-7)*sb2**2)*xb1**3-2*(2*(sb2*xb2-xgl)*(xb2-1)*xb2-(2*
     . xb2**3-2*xb2**2-xb2-1)*sb2**2)*xb1+(2*(xb2-1-(xb2-3)*sb2)*sb2*
     . xb2+(2*xb2+7*xgl)*(xb2-1))*xb1**2)*(xb2-1)*xb1*xg2**3
      ans6=-(2*((sb2**2*xb2-sb2*xb2+xgl)*(xb2-1)*xb2+(xb1-2)*sb2**2*
     . xb1**3)-(2*(sb2-1)*(3*xb2+2)*sb2+7*xgl-1)*(xb2-1)*xb1*xb2-2*((
     . 4*sb2+1)*(xb2-1)*xb2-(2*xb2-1)**2*sb2**2)*xb1**2)*(xb2-1)*xb1
     . **2*xb2+((2*sb2**2*xb2-2*sb2*xb2+3*xgl)*(xb2-1)-2*sb2**2*xb1**
     . 3+((4*sb2+1)*(xb2-1)-4*(xb2-2)*sb2**2)*xb1**2-2*((sb2*xb2-xgl)
     . *(xb2-1)-(xb2**2-xb2-1)*sb2**2)*xb1)*(xb2-1)*xb1*xg2**4-(2*((4
     . *sb2+1)*(xb2+2)*(xb2-1)*xb2-(4*xb2**3+4*xb2**2-11*xb2+1)*sb2**
     . 2)*xb1**3+(2*sb2**2*xb2-2*sb2*xb2+3*xgl)*(xb2-1)*xb2**2-((6*
     . sb2*xb2**2+12*sb2*xb2+8*sb2-7*xb2*xgl-14*xgl+2)*(xb2-1)-2*(3*
     . xb2**3+3*xb2**2-2*xb2-6)*sb2**2)*xb1**2*xb2-2*(((xb2+1)*xb1-2)
     . *sb2**2*xb1**3+2*(sb2**2*xb2-sb2*xb2+xgl)*(xb2-1)*xb2)*xb1)*(
     . xb2-1)*xb1*xg2+ans7
      ans5=-2*((xb1**4*xb2**2-xb1**4*xg2+xb1**3*xb2**3-2*xb1**3*xb2**
     . 2*xg2-2*xb1**3*xb2**2-xb1**3*xb2*xg2+2*xb1**3*xg2**2+2*xb1**3*
     . xg2+xb1**2*xb2**4-2*xb1**2*xb2**3*xg2-2*xb1**2*xb2**3+xb1**2*
     . xb2**2*xg2**2+3*xb1**2*xb2**2*xg2+xb1**2*xb2**2+2*xb1**2*xb2*
     . xg2**2+2*xb1**2*xb2*xg2-xb1**2*xg2**3-4*xb1**2*xg2**2-xb1**2*
     . xg2-xb1*xb2**3*xg2+2*xb1*xb2**2*xg2**2+2*xb1*xb2**2*xg2-xb1*
     . xb2*xg2**3-5*xb1*xb2*xg2**2-xb1*xb2*xg2+2*xb1*xg2**3+2*xb1*xg2
     . **2-xb2**4*xg2+2*xb2**3*xg2**2+2*xb2**3*xg2-xb2**2*xg2**3-4*
     . xb2**2*xg2**2-xb2**2*xg2+2*xb2*xg2**3+2*xb2*xg2**2-xg2**3)*(
     . xb1-xb2)*sb2+(xb1**2-xg2)*(xb2-xg2)**2*(xb2-1)**2*xb2)*(log(
     . xb2)-log(xg2))*(xg2-1)*sb2*xb1+ans6
      ans4=((2*((xb1-2)*xb1+xb2**2-2*xb2+2)*sb2**2-(2*sb2+1)*(xb2-1)
     . **2)*(xb1-xg2)**2*log(xg2)*xb1**2-((log(-(xb1-xgl))-log(xgl))*
     . (xb1-xgl)**2-(log(xg2)-log(xgl))*(xb1-2*xgl)*xb1)*(xb1**2-xg2)
     . *(xb2-1)**2*(xg2-1))*(xb2-xg2)**2+ans5
      ans8=(log(xb1)-log(xg2))*(sb2-1)*xb2
      ans3=ans4*ans8
      ans14=-(((xb1-2)*xb1-(2*xb2**2-4*xb2+1)-2*((xb1-2)*xb1+xb2**2-2
     . *xb2+2)*sb2**2+2*((xb1-2)*xb1+2*xb2**2-4*xb2+3)*sb2)*(xb2-xg2)
     . **2*log(xg2)*xb2-(log(xg2)-log(xgl))*(xb1-1)**2*(xb2**2-xg2)*(
     . xb2-2*xgl)*(xg2-1))*(xb1-xg2)*xb2
      ans13=((2*xb2**5+3*xg2**2*xgl-4*(xg2+1)*xb2**4+2*(xg2**2+3*xg2+
     . 1)*xb2**3+2*((xgl+1)*xg2+xgl)*xb2*xg2-(7*xgl+3+3*xg2)*xb2**2*
     . xg2-(xb1-xg2-1)*(2*xb2**3-xb2**2*xg2+7*xb2**2*xgl-xb2**2-2*xb2
     . *xg2*xgl-2*xb2*xgl-3*xg2*xgl)*xb1+2*(((4*xb2**2-xg2)*(xg2+1)*
     . xb2-xg2**2-(2*xg2**2+xg2+2)*xb2**2+((3*xb2**2-xg2-(xg2+1)*xb2)
     . *xb1-((xb2**2-xg2)*(xg2+1)+(2*xb2+xg2+1)*(2*xb2-xg2-1)*xb2))*
     . xb1)*xb1-2*(xb2**4+xg2**2-(2*xb2**2+3*xg2)*(xg2+1)*xb2+(xg2**2
     . +6*xg2+1)*xb2**2)*xb2-(((4*xb2**2-xg2)*(xg2+1)*xb2-xg2**2-(2*
     . xg2**2+xg2+2)*xb2**2+((3*xb2**2-xg2-(xg2+1)*xb2)*xb1-((xb2**2-
     . xg2)*(xg2+1)+(2*xb2+xg2+1)*(2*xb2-xg2-1)*xb2))*xb1)*xb1-(xb2**
     . 4+xg2**2-2*(xb2**2+2*xg2)*(xg2+1)*xb2+(xg2**2+8*xg2+1)*xb2**2)
     . *xb2)*sb2)*sb2)*xb2-(log(-(xb2-xgl))-log(xgl))*(xb1-xg2)*(xb1-
     . 1)*(xb2**2-xg2)*(xb2-xgl)**2)*(xb1-1)*(xg2-1)+ans14
      ans15=(log(xb2)-log(xg2))*(xb1-xg2)*sb2
      ans12=ans13*ans15
      ans16=-((((xb1*xb2-2*xb1*xgl-2*xb2*xgl+2*xg2*xgl-xg2+2*xgl)*(
     . xb1-xb2)*sb2+(xb1-2*xgl)*(xb2-xg2)*(xb2-1))*(xb1-1)*(xb2-1)*(
     . xg2-1)+((xb1*xb2-2*xb1*xgl-2*xb2*xgl+4*xgl-1)*(xb1-xb2)*sb2+(
     . xb1-2*xgl)*(xb2-1)**2)*(xb1-xg2)*(xb2-xg2)*log(xg2))*(log(xg2)
     . -log(xgl))*(xb1-xg2)-((sb2-1)*(3*xb1-xb2)*sb2-(xb1+xgl))*(log(
     . xb1)-log(xg2))**2*(sb2-1)*(xb1**2-xg2)*(xb2-xg2)*(xb2-1)**2*(
     . xg2-1))*(xb2-xg2)*xb2
      ans11=ans12+ans16
      ans10=ans11*xb1
      ans9=-ans10
      ans22=((((xb1*xb2+5*xb1*xgl+4*xb2**2-4*xb2*xg2+5*xb2*xgl-4*xb2-
     . 5*xg2*xgl+3*xg2-5*xgl)*(xb1-xb2)*sb2+(xb1+5*xgl)*(xb2-xg2)*(
     . xb2-1)+4*(xb1**2-xb1*xg2-xb1+xb2**2-xb2*xg2-xb2+2*xg2)*(xb1-
     . xb2)*sb2**3-4*(xb1**2-xb1*xg2-xb1+2*xb2**2-2*xb2*xg2-2*xb2+3*
     . xg2)*(xb1-xb2)*sb2**2)*xb2+(log(-(xb2-xgl))-log(xgl))*(xb1-xg2
     . )*(xb1-1)*(xb2-xgl)**2*sb2)*xb1-(log(-(xb1-xgl))-log(xgl))*(
     . sb2-1)*(xb1-xgl)**2*(xb2-xg2)*(xb2-1)*xb2)*(xb1-1)*(xb2-1)*(
     . xg2-1)
      ans21=(((xb1*xb2+5*xb1*xgl+4*xb2**2+5*xb2*xgl-8*xb2-10*xgl+3)*(
     . xb1-xb2)*sb2+(xb1+5*xgl)*(xb2-1)**2+4*(xb1**2-2*xb1+xb2**2-2*
     . xb2+2)*(xb1-xb2)*sb2**3-4*(xb1**2-2*xb1+2*xb2**2-4*xb2+3)*(xb1
     . -xb2)*sb2**2)*xb1*xb2-((xb1**2*xb2**2-2*xb1**2*xb2*xgl+xb1**2*
     . xgl**2-2*xb1*xb2**2*xgl+xb1*xb2*xgl**2+4*xb1*xb2*xgl-xb1*xb2-2
     . *xb1*xgl**2+xb2**2*xgl**2-2*xb2*xgl**2+xgl**2)*(xb1-xb2)*sb2+(
     . xb1-xgl)**2*(xb2-1)**2*xb2)*log(xgl)+(xb1-1)**2*(xb2-xgl)**2*
     . log(-(xb2-xgl))*sb2*xb1-(sb2-1)*(xb1-xgl)**2*(xb2-1)**2*log(-(
     . xb1-xgl))*xb2+((xb1*xgl+xb2**2+xb2*xgl-2*xb2-2*xgl+1)*(xb1-xb2
     . )*sb2+(xb2-1)**2*xgl+(xb1**2-2*xb1+xb2**2-2*xb2+2)*(xb1-xb2)*
     . sb2**3-(xb1**2-2*xb1+2*xb2**2-4*xb2+3)*(xb1-xb2)*sb2**2)*log(
     . xg2)*xb1*xb2)*(xb1-xg2)*(xb2-xg2)*log(xg2)+ans22
      ans23=(xb2-xg2)
      ans20=ans21*ans23
      ans24=((sb2-1)*(xb1-3*xb2)*sb2+xb2+xgl)*(log(xb2)-log(xg2))**2*
     . (xb1-xg2)*(xb1-1)**2*(xb2**2-xg2)*(xg2-1)*sb2*xb1*xb2
      ans19=ans20+ans24
      ans25=(xb1-xg2)
      ans18=ans19*ans25
      ans17=-ans18
      ans2=ans3+ans9+ans17
      ans1=ans2*xg2
      rct12=ans1/(4*(xb1-xg2)**2*(xb1-1)**2*(xb2-xg2)**2*(xb2-1)**2*(
     . xg2-1)*xb1*xb2)

      rct22=((((log(xb2)-log(xg2))**2*(xb1-3*xb2)*(xb1-1)*(xg2-1)*xb2
     . +(log(xg2)+4)*(xb1-xb2)**2*(xb2-xg2)*log(xg2))*(xb1-xg2)-(log(
     . xb1)-log(xg2))**2*(3*xb1-xb2)*(xb2-xg2)*(xb2-1)*(xg2-1)*xb1-2*
     . (2*(xb1-1)*(xg2-1)-(xb2-xg2)*log(xg2))*(log(xb2)-log(xg2))*(
     . xb1-xb2)*(xb1-xg2)*xb2+2*((xb2**2+2*xg2-(xg2+1)*xb2-(xg2+1-xb1
     . )*xb1)*(log(xb2)-log(xg2))*(xg2-1)*xb2-((xb1-xg2)*log(xg2)-2*(
     . xb2-1)*(xg2-1))*(xb1-xb2)*(xb2-xg2))*(log(xb1)-log(xg2))*xb1)*
     . (2*sb2-1)*(sb2-1)*sb2*xg2)/(4*(xb1-xb2)*(xb1-xg2)*(xb1-1)*(xb2
     . -xg2)*(xb2-1)*(xg2-1))

      ans10=2*((xg2**3*xt1**2+xg2**3*xt1*xt2-2*xg2**3*xt1+xg2**3*xt2
     . **2-2*xg2**3*xt2+xg2**3-2*xg2**2*xt1**3-xg2**2*xt1**2*xt2**2-2
     . *xg2**2*xt1**2*xt2+4*xg2**2*xt1**2-2*xg2**2*xt1*xt2**2+5*xg2**
     . 2*xt1*xt2-2*xg2**2*xt1-2*xg2**2*xt2**3+4*xg2**2*xt2**2-2*xg2**
     . 2*xt2+xg2*xt1**4+2*xg2*xt1**3*xt2**2+xg2*xt1**3*xt2-2*xg2*xt1
     . **3+2*xg2*xt1**2*xt2**3-3*xg2*xt1**2*xt2**2-2*xg2*xt1**2*xt2+
     . xg2*xt1**2+xg2*xt1*xt2**3-2*xg2*xt1*xt2**2+xg2*xt1*xt2+xg2*xt2
     . **4-2*xg2*xt2**3+xg2*xt2**2-xt1**4*xt2**2-xt1**3*xt2**3+2*xt1
     . **3*xt2**2-xt1**2*xt2**4+2*xt1**2*xt2**3-xt1**2*xt2**2)*(xt1-
     . xt2)*st2+(xg2-xt1**2)*(xg2-xt2)**2*(xt2-1)**2*xt2)*log(xt2)*
     . st2
      ans9=((2*xg2*xgl*xt1+3*xg2*xgl+2*xg2*xt*xt1+3*xg2*xt+xg2*xt1**2
     . -7*xgl*xt1**2+2*xgl*xt1-7*xt*xt1**2+2*xt*xt1-2*xt1**3+xt1**2+2
     . *(2*xg2*xt1**2-xg2*xt1*xt2-xg2*xt2-4*xt1**3+3*xt1**2*xt2+2*xt1
     . **2-xt1*xt2)*st2)*(xg2-xt2)*(xt2-1)-2*(xg2**2*xt1**3+2*xg2**2*
     . xt1**2*xt2-4*xg2**2*xt1**2-xg2**2*xt1*xt2**2+xg2**2*xt1*xt2+
     . xg2**2*xt1-xg2**2*xt2**2+xg2**2*xt2-2*xg2*xt1**4-4*xg2*xt1**3*
     . xt2+8*xg2*xt1**3+xg2*xt1**2*xt2**2+xg2*xt1**2*xt2-4*xg2*xt1**2
     . +xg2*xt1*xt2**3-2*xg2*xt1*xt2**2+xg2*xt1*xt2+xg2*xt2**3-xg2*
     . xt2**2+xt1**5-2*xt1**4+4*xt1**3*xt2**2-4*xt1**3*xt2+xt1**3-3*
     . xt1**2*xt2**3+xt1**2*xt2**2+2*xt1**2*xt2+xt1*xt2**3-xt1*xt2**2
     . )*st2**2-2*(xg2*xt1+2*xg2-4*xt1**2+xt1)*(xg2-xt2)*(xt2-1)*s2t*
     . sxgl*sxt+(xt-xt1+xgl-2*s2t*sxgl*sxt)*(xg2-xt1**2)*(xg2-xt2)*(
     . xt2-1)*xb12(mt1,mg,mt))*(xg2-xt2)*(xt2-1)+ans10
      ans11=(xg2-1)
      ans8=ans9*ans11
      ans12=(2*((xt1**5-2*xt1**4-xt2**3-(xt2+4)*xt1**2*xt2**2-(2*xt2-
     . 1)*xt1**3)*xg2+(xg2**4+xt1**2*xt2**2-(2*xt1**3-2*xt1**2*xt2-5*
     . xt1**2+2*xt1-xt2**2-2*xt2)*xg2**2)*(xt1+xt2)-(((xt2+4-xt1)*xt1
     . +2*xt2-1)*xt1+(2*xt2+1)*xt2)*xg2**3)*st2**2-(2*(xg2**2*xt1+xg2
     . **2*xt2-xg2*xt1**2*xt2-2*xg2*xt1**2-xg2*xt2+xt1**3+xt1**2*xt2)
     . *st2+(xg2-xt1)**2*xt1)*(xg2-xt2)**2)*(xt2-1)**2*log(xg2)
      ans7=ans8+ans12
      ans13=(log(xg2)-log(xt1))*(st2-1)
      ans6=ans7*ans13
      ans5=-ans6
      ans19=2*(((2*(2*xt2-1)*xt1-(xt2-1)**2*xt2)*xt2+(3*xt2-1)*xt1**3
     . -(4*xt2**2+xt2-1)*xt1**2)*xt2-((xt2**2-4*xt2+1)*xt2-(xt2+1)*
     . xt1**2+(2*xt2**2+xt2+1)*xt1)*xg2**2+(2*(xt2**2-4*xt2+2)*xt2**2
     . -(xt2+1)*xt1**3-(xt2**2-2*xt2-1)*xt1**2+(4*xt2**2-xt2-1)*xt1*
     . xt2)*xg2)*st2**2
      ans18=(((xt1-1)*(2*xt2-1)*xt1-2*(xt2-1)**2*xt2)*xt2+(xt1-1)*(7*
     . xt2-2)*xt*xt1+(xt1-1)*(7*xt2-2)*xgl*xt1)*xt2-((2*xt2**2-3*xt2+
     . 2-xt1*xt2)*xt2-(xt1-1)*(2*xt2+3)*xt-(xt1-1)*(2*xt2+3)*xgl)*xg2
     . **2-(((2*(xt2-1)+xt1)*xt1-(4*xt2**2-6*xt2+3))*xt2**2+(2*xt1*
     . xt2+3*xt1+7*xt2**2-2*xt2)*(xt1-1)*xt+(2*xt1*xt2+3*xt1+7*xt2**2
     . -2*xt2)*(xt1-1)*xgl)*xg2-2*((4*xt2-1)*xt2-(xt2+2)*xg2)*(xg2-
     . xt1)*(xt1-1)*s2t*sxgl*sxt-2*((2*((2*xt2-1)*xt1-(xt2-1)**2*xt2)
     . *xt2+(3*xt2-1)*xt1**3-(4*xt2**2+xt2-1)*xt1**2)*xt2-(2*(xt2**2-
     . 3*xt2+1)*xt2-(xt2+1)*xt1**2+(2*xt2**2+xt2+1)*xt1)*xg2**2-((xt2
     . **2-2*xt2-1+(xt2+1)*xt1)*xt1**2-2*(2*xt2**2-6*xt2+3)*xt2**2-(4
     . *xt2**2-xt2-1)*xt1*xt2)*xg2)*st2+ans19
      ans20=(xg2-1)*(xt1-1)
      ans17=ans18*ans20
      ans21=-(((xt1-2)*xt1-(2*xt2**2-4*xt2+1)-2*((xt1-2)*xt1+xt2**2-2
     . *xt2+2)*st2**2+2*((xt1-2)*xt1+2*xt2**2-4*xt2+3)*st2)*(xg2-xt2)
     . **2*log(xg2)*xt2-(xt-xt2+xgl+2*s2t*sxgl*sxt)*(xg2-xt2**2)*(xg2
     . -1)*(xt1-1)**2*xb12(mt2,mg,mt))*(xg2-xt1)
      ans16=ans17+ans21
      ans22=(log(xg2)-log(xt2))*(xg2-xt1)*st2
      ans15=ans16*ans22
      ans14=(((((xt1*xt2-1-(xt1+xt2-2)*xt-2*(xt1+xt2-2)*xgl)*(xt1-xt2
     . )*st2-(xt-xt1+2*xgl)*(xt2-1)**2-2*(((xt1-2)*xt1+xt2**2-2*xt2+2
     . )*st2-(xt2-1)**2)*s2t*sxgl*sxt)*(xg2-xt1)*(xg2-xt2)*log(xg2)-(
     . (xt2-1+xt1)*xt-xt1*xt2+2*(xt2-1+xt1)*xgl-(xt-1+2*xgl)*xg2)*(
     . xg2-1)*(xt1-xt2)*(xt1-1)*(xt2-1)*st2)*(xg2-xt1)-(((xt-xt1+2*
     . xgl-2*s2t*sxgl*sxt)*(log(xg2)-log(xt1))*(st2-1)*(xg2-xt1**2)-(
     . xt-xt1+2*xgl)*(xg2-xt1)*(xt1-1))*(xg2-xt2)*(xt2-1)+2*(((xt1-1)
     . *xt1+(xt2-1)*xt2-(xt2-2+xt1)*xg2)*st2+(xg2-xt2)*(xt2-1))*(xg2-
     . xt1)*(xt1-1)*s2t*sxgl*sxt)*(xg2-1)*(xt2-1))*(xg2-xt2)+(xt-xt2+
     . 2*xgl+2*s2t*sxgl*sxt)*(log(xg2)-log(xt2))*(xg2-xt1)**2*(xg2-
     . xt2**2)*(xg2-1)*(xt1-1)**2*st2)*(log(xg2)-log(xgl))+ans15
      ans4=-((5*xt+xt1+5*xgl)*(xt2-1)**2-4*(xt1**2-2*xt1+2*xt2**2-4*
     . xt2+3-(xt1**2-2*xt1+xt2**2-2*xt2+2)*st2)*(xt1-xt2)*st2**2+(xt1
     . *xt2+4*xt2**2-8*xt2+3+5*(xt1+xt2-2)*xt+5*(xt1+xt2-2)*xgl)*(xt1
     . -xt2)*st2+6*(((xt1-2)*xt1+xt2**2-2*xt2+2)*st2-(xt2-1)**2)*s2t*
     . sxgl*sxt-(xt-xt1+xgl-2*s2t*sxgl*sxt)*(st2-1)*(xt2-1)**2*xb12(
     . mt1,mg,mt)+(xt-xt2+xgl+2*s2t*sxgl*sxt)*(xt1-1)**2*xb12(mt2,mg,
     . mt)*st2)*(xg2-xt1)**2*(xg2-xt2)**2*log(xg2)+ans5+ans14
      ans3=-(((((xt2-1+xt1-xg2)*(xt1-xt2)*st2-(xg2-xt2)*(xt2-1))*(xg2
     . -1)*(xt1-1)*(xt2-1)+((xt1+xt2-2)*(xt1-xt2)*st2+(xt2-1)**2)*(
     . xg2-xt1)*(xg2-xt2)*log(xg2))*(xg2-xt2)-(log(xg2)-log(xt2))*(
     . xg2-xt1)*(xg2-xt2**2)*(xg2-1)*(xt1-1)**2*st2)*(xg2-xt1)+(log(
     . xg2)-log(xt1))*(st2-1)*(xg2-xt1**2)*(xg2-xt2)**2*(xg2-1)*(xt2-
     . 1)**2)*(log(xg2)-log(xt))*xt-(((4*(xt2-1)+xt1)*xt2+5*(xt2-1+
     . xt1)*xt+5*(xt2-1+xt1)*xgl-(4*xt2-3+5*xt+5*xgl)*xg2-4*((xt1-1)*
     . xt1+2*(xt2-1)*xt2-(2*xt2-3+xt1)*xg2-((xt1-1)*xt1+(xt2-1)*xt2-(
     . xt2-2+xt1)*xg2)*st2)*st2)*(xg2-xt1)*(xt1-xt2)*(xt1-1)*st2+(xt+
     . xt1+xgl-(st2-1)*(3*xt1-xt2)*st2-s2t*sxgl*sxt)*(log(xg2)-log(
     . xt1))**2*(st2-1)*(xg2-xt1**2)*(xg2-xt2)*(xt2-1))*(xg2-xt2)*(
     . xg2-1)*(xt2-1)+ans4
      ans2=((((xt-xt2+xgl+2*s2t*sxgl*sxt)*(xg2-xt1)*(xt1-1)*xb12(mt2,
     . mg,mt)*st2+(5*xt+xt1+5*xgl)*(xg2-xt2)*(xt2-1)-(xt-xt1+xgl-2*
     . s2t*sxgl*sxt)*(st2-1)*(xg2-xt2)*(xt2-1)*xb12(mt1,mg,mt)-6*(((
     . xt1-1)*xt1+(xt2-1)*xt2-(xt2-2+xt1)*xg2)*st2+(xg2-xt2)*(xt2-1))
     . *s2t*sxgl*sxt)*(xg2-xt2)*(xt2-1)+(xt+xt2+xgl+s2t*sxgl*sxt+(st2
     . -1)*(xt1-3*xt2)*st2)*(log(xg2)-log(xt2))**2*(xg2-xt1)*(xg2-xt2
     . **2)*(xt1-1)*st2)*(xg2-1)*(xt1-1)+((xt1**2-2*xt1+2*xt2**2-4*
     . xt2+3-(xt1**2-2*xt1+xt2**2-2*xt2+2)*st2)*(xt1-xt2)*st2**2-(xgl
     . +xt)*(xt2-1)**2-((xt1+xt2-2)*xt+(xt2-1)**2+(xt1+xt2-2)*xgl)*(
     . xt1-xt2)*st2-(((xt1-2)*xt1+xt2**2-2*xt2+2)*st2-(xt2-1)**2)*s2t
     . *sxgl*sxt)*(xg2-xt1)*(xg2-xt2)**2*log(xg2)**2)*(xg2-xt1)+ans3
      ans1=ans2*xg2
      rct32=ans1/(2*(xg2-xt1)**2*(xg2-xt2)**2*(xg2-1)*(xt1-1)**2*(xt2
     . -1)**2)

      ans3=(((xb12(mt2,mg,mt)+6+xb12(mt1,mg,mt))*(xg2-1)*(xt2-1)*s2t*
     . sxgl*sxt+2*((xg2-xt1)*log(xg2)+2*(xg2-1)*(xt2-1))*(st2-1)*(xt1
     . -xt2)*st2)*(xg2-xt2)+2*((xt1-1)*xt1+(xt2-1)*xt2-(xt2-2+xt1)*
     . xg2)*(log(xg2)-log(xt2))*(st2-1)*(xg2-1)*st2*xt2)*(log(xg2)-
     . log(xt1))*xt1
      ans2=(((st2-1)*(xt1-xt2)*st2+s2t*sxgl*sxt)*(xg2-xt2)*(xt1-xt2)*
     . log(xg2)**2-((st2-1)*(xt1-3*xt2)*st2+s2t*sxgl*sxt)*(log(xg2)-
     . log(xt2))**2*(xg2-1)*(xt1-1)*xt2)*(xg2-xt1)+((st2-1)*(3*xt1-
     . xt2)*st2+s2t*sxgl*sxt)*(log(xg2)-log(xt1))**2*(xg2-xt2)*(xg2-1
     . )*(xt2-1)*xt1+((xb12(mt2,mg,mt)+6+xb12(mt1,mg,mt))*s2t*sxgl*
     . sxt+4*(st2-1)*(xt1-xt2)*st2)*(xg2-xt1)*(xg2-xt2)*(xt1-xt2)*log
     . (xg2)-((xb12(mt2,mg,mt)+6+xb12(mt1,mg,mt))*(xg2-1)*(xt1-1)*s2t
     . *sxgl*sxt+2*((xg2-xt2)*log(xg2)+2*(xg2-1)*(xt1-1))*(st2-1)*(
     . xt1-xt2)*st2)*(log(xg2)-log(xt2))*(xg2-xt1)*xt2-2*(((log(xg2)-
     . log(xt2))*(xg2-1)*(xt1-1)*xt2-(xg2-xt2)*(xt1-xt2)*log(xg2))*(
     . xg2-xt1)-(log(xg2)-log(xt1))*(xg2-xt2)*(xg2-1)*(xt2-1)*xt1)*(
     . log(xg2)-log(xgl))*s2t*sxgl*sxt+ans3
      ans4=(2*st2-1)*xg2
      ans1=ans2*ans4
      rct42=ans1/(2*(xg2-xt1)*(xg2-xt2)*(xg2-1)*(xt1-xt2)*(xt1-1)*(
     . xt2-1))

      rct2=rct12+rct22+rct32+rct42

      if(icontribution.eq.1) then
       r22=r212
       r42=r412
       r52=r512+ratio*r522
       r72=r712
       r82=r812
       r92=r912
       rct2=rct12+rct22
      endif
      if(icontribution.eq.2) then
       r22=r222
       r42=r422
       r52=r532+ratio*r542
       r72=r722
       r82=r822
       r92=r922
       rct2=rct32+rct42
      endif

      ral2 = r22+r42+r52+r72+r82+r92+rct2
      bo = cb2/2*fi(amsb1**2,am2**2,amu**2)
     .   + sb2/2*fi(amsb2**2,am2**2,amu**2)
     .   + ct2*fi(amst1**2,am2**2,amu**2)
     .   + st2*fi(amst2**2,am2**2,amu**2)
      if(icontribution.eq.1) then
       bo = cb2/2*fi(amsb1**2,am2**2,amu**2)
     .    + sb2/2*fi(amsb2**2,am2**2,amu**2)
      endif
      if(icontribution.eq.2) then
       bo = ct2*fi(amst1**2,am2**2,amu**2)
     .    + st2*fi(amst2**2,am2**2,amu**2)
      endif
      ral2 = cf*ral2/bo

      anomalous = -cf/2

      fal2_hdec = dreal(ral2)*fnorm + anomalous
c     write(6,*)'alpha2_sub: ',fal2_hdec,bo

      return
      end
 
