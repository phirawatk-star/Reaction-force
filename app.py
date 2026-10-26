import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title='Beam Reaction Calculator', page_icon='🏗️', layout='centered')
st.title('🏗️ Beam Reaction Calculator')
st.caption('Simply supported beam • 1 span • 2 adjustable downward point loads')
st.info('แบบจำลอง: คานรองรับแบบ Pin–Roller, แรงจุดแนวดิ่ง 2 จุด, ไม่รวมแรงกระจาย น้ำหนักคาน หรือโมเมนต์ภายนอก')

L = st.number_input('ความยาวคาน L (m)', min_value=0.01, value=6.0, step=0.5, format='%.2f')
c1,c2=st.columns(2)
with c1:
    st.subheader('Point load 1')
    P1=st.number_input('P1 (tonf) ↓',min_value=0.0,value=5.0,step=0.5,format='%.2f')
    a1=st.number_input('ตำแหน่ง x1 จาก A (m)',min_value=0.0,max_value=float(L),value=min(2.0,float(L)),step=0.1,format='%.2f')
with c2:
    st.subheader('Point load 2')
    P2=st.number_input('P2 (tonf) ↓',min_value=0.0,value=8.0,step=0.5,format='%.2f')
    a2=st.number_input('ตำแหน่ง x2 จาก A (m)',min_value=0.0,max_value=float(L),value=min(4.5,float(L)),step=0.1,format='%.2f')

RB=(P1*a1+P2*a2)/L
RA=P1+P2-RB
st.divider()
st.subheader('ผลการคำนวณแรงปฏิกิริยา')
r1,r2=st.columns(2)
r1.metric('RA ที่จุด A ↑',f'{RA:.3f} tonf')
r2.metric('RB ที่จุด B ↑',f'{RB:.3f} tonf')
st.latex(r'R_B=\frac{P_1 x_1+P_2 x_2}{L}')
st.latex(r'R_A=P_1+P_2-R_B')
st.write(f'ตรวจสอบสมดุลแนวดิ่ง: RA + RB = **{RA+RB:.3f} tonf**; P1 + P2 = **{P1+P2:.3f} tonf**')

fig,ax=plt.subplots(figsize=(10,3.3))
ax.plot([0,L],[0,0],lw=7,color='#547da3',solid_capstyle='butt')
ax.plot(0,-0.11,marker='^',markersize=18,color='#26936b')
ax.plot(L,-0.11,marker='o',markersize=13,color='#26936b')
for i,(p,x) in enumerate([(P1,a1),(P2,a2)],1):
    if p>0:
        ax.annotate('',xy=(x,0.07),xytext=(x,0.9),arrowprops=dict(arrowstyle='-|>',lw=2.2,color='#d24b43'))
        ax.text(x,1.03,f'P{i}={p:g} tonf\nx={x:g} m',ha='center',va='bottom',fontsize=9)
ax.text(0,-0.55,f'A\nRA={RA:.2f}',ha='center',va='top')
ax.text(L,-0.55,f'B\nRB={RB:.2f}',ha='center',va='top')
ax.set_xlim(-max(L*.15,.6),L+max(L*.15,.6))
ax.set_ylim(-1.4,1.85)
ax.axis('off')
st.pyplot(fig)
plt.close(fig)

st.subheader('Shear force & bending moment')
xs=np.linspace(0,L,601)
V=np.array([RA-(P1 if x>=a1 else 0)-(P2 if x>=a2 else 0) for x in xs])
M=RA*xs-P1*np.maximum(xs-a1,0)-P2*np.maximum(xs-a2,0)
fig2,ax2=plt.subplots(figsize=(9,2.7))
ax2.step(xs,V,where='post'); ax2.axhline(0,color='black',lw=.8);ax2.set_xlabel('x (m)');ax2.set_ylabel('V (tonf)');ax2.grid(alpha=.25)
st.pyplot(fig2);plt.close(fig2)
fig3,ax3=plt.subplots(figsize=(9,2.7))
ax3.plot(xs,M);ax3.fill_between(xs,0,M,alpha=.13);ax3.axhline(0,color='black',lw=.8);ax3.set_xlabel('x (m)');ax3.set_ylabel('M (tonf·m)');ax3.grid(alpha=.25)
st.pyplot(fig3);plt.close(fig3)
keypoints=sorted(set([0.0,float(a1),float(a2),float(L)]))
peak=max((RA*x-P1*max(x-a1,0)-P2*max(x-a2,0),x) for x in keypoints)
st.success(f'Maximum bending moment = {peak[0]:.3f} tonf·m ที่ x = {peak[1]:.3f} m')
st.warning('ใช้เพื่อคำนวณสถิตยศาสตร์ของคาน Simply Supported เท่านั้น หากจุดรองรับเป็น Fixed/Continuous หรือมีน้ำหนักคานและแรงอื่น ต้องปรับแบบจำลองก่อนนำไปใช้ออกแบบจริง')
