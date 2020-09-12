from ROOT import *

import os
import csv
import pylab   
import time
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline

def offset(arr, off):
    size=len(arr)
    for i in xrange(0,size):
        arr[i]=arr[i]-off


c1=TCanvas("c1", "c1", 800,600)

clear = 'WFM16/'
ws='WFM17/'

results_clear=[]
results_ws=[]
for filename in os.listdir(clear):
    if filename.endswith(".CSV"):
        print filename
        #f = open(clear+filename)
        t=[]
        U=[]
        with open(clear+filename, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    tt=float(row[0])*1.e9
                    uu=float(row[1])*1.e3
                 
                    t.append(tt)
                    U.append(uu)
                except ValueError:
                    print "nooot"

        Uaverage=sum(U[7000:len(U)])/(len(U)-7000)
        offset(U,Uaverage)
        
        print len(t)
        plt.plot(t, U)
        plt.xlabel('t [ns]'); plt.ylabel('U(t) [mV]')
        #plt.show()
        f = InterpolatedUnivariateSpline(t,U, k=1)
        integral=f.integral(min(t), max(t))
        print integral
        results_clear.append(integral)



for filename in os.listdir(ws):
    if filename.endswith(".CSV"):
        print filename
        #f = open(clear+filename)
        t=[]
        U=[]
        with open(ws+filename, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    tt=float(row[0])*1.e9
                    uu=float(row[1])*1.e3
                 
                    t.append(tt)
                    U.append(uu)
                except ValueError:
                    print "nooot"

        Uaverage=sum(U[7000:len(U)])/(len(U)-7000)
        offset(U,Uaverage)  

        plt.plot(t, U)
        plt.xlabel('t [ns]'); plt.ylabel('U(t) [mV]')
        #plt.show()
        #time.sleep(100.)
        f = InterpolatedUnivariateSpline(t,U, k=1)
        integral=f.integral(min(t), max(t))
        print integral
        results_ws.append(integral)

#plt.show()
#plt.savefig("pulse.png")

hist_clear=TH1D("clear", "clear", 200, 0.9*min(results_ws ), 1.1*max(results_clear))
hist_ws=TH1D("ws", "ws", 200, 0.9*min(results_ws), 1.1*max(results_clear))
for c in results_clear:
    hist_clear.Fill(c)
for w in results_ws:
    hist_ws.Fill(w)


hist_clear.SetLineColor(kBlue+3)
hist_clear.SetLineWidth(3)

hist_ws.SetLineColor(kYellow+3)
hist_ws.SetLineWidth(3)

hist_clear.SetTitle("")
hist_clear.GetXaxis().SetTitle("[mV ns]")


hist_ws.SetTitle("")
hist_ws.GetXaxis().SetTitle("[mV ns]")

hist_clear.SetStats(False)
hist_ws.SetStats(False) 


hist_ws.DrawNormalized()
hist_clear.DrawNormalized("SAME")

leg=TLegend(0.45, 0.8, 0.6,0.95)
leg.AddEntry(hist_clear, "Clear Fiber, Green LED", "f")
leg.AddEntry(hist_ws, "WaveShifter, Green LED", "f")     

leg.Draw()

c1.SaveAs("results_green.pdf")






plt.savefig("pulse_green.pdf")
