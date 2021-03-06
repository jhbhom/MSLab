from ROOT import *

import sys
import os
import csv
import pylab   
import time
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline

__author__='Jihyun Bhom'
__date="15.09.2002"
measurmeents = {
    "Blue LED": {
        "Clear Fiber": "WFM14",
        "Wave Shifter": "WFM15"
    },
    "Green LED": {
        "Clear Fiber": "WFM16",
        "Wave Shifter": "WFM17"
    },     
     "UV LED": {
        "Clear Fiber": "WFM35",
        "Wave Shifter": "WFM24"
    },      
    "Red LED": {
        "Clear Fiber": "WFM21",
        "Wave Shifter": "WFM34"
    },   
    "IR LED": {
        "Clear Fiber": "WFM22",
        "Wave Shifter": "WFM28"
    },  
    "White LED": {
        "Clear Fiber": "WFM23",
        "Wave Shifter": "WFM29"
    }
    }
def Filename(name):
    return name.replace(" ", "_")
    

# function to offset the pedestal
def offset(arr, off):
    size=len(arr)
    for i in xrange(0,size):
        arr[i]=arr[i]-off


# function that does the analysis of data for each color        
def ana_color(clear_name, ws_name, color):
    

    c1=TCanvas("c1", "c1", 800,600)

    clear = clear_name+"/"
    ws=ws_name+"/"

    results_clear=[]
    results_ws=[]
    results_peak_ws=[]
    results_peak_clear=[]
    
    print 'Starting clear fiber', clear
    for filename in os.listdir(clear):
        if filename.endswith(".CSV"):
            #print filename
       
            t=[]
            U=[]
            UMAX=-10000.
            with open(clear+filename, 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    try:
                        tt=float(row[0])*1.e9
                        uu=float(row[1])*1.e3
                 
                        t.append(tt)
                        U.append(uu)
                    except ValueError:
                        aaa=1
            #Uaverage=sum(U[7000:len(U)])/(len(U)-7000)
            #print int(0.3*len(U))
            Uaverage=sum(U[0:int(0.3*len(U))])/(0.3*len(U))
            #print 'WS pedestrial: ', Uaverage
            #Uaverage=U[0]
            #Uaverage=0.
            offset(U,Uaverage)
            UMAX=max(U)

            
            #print len(t)
            plt.plot(t, U)
            plt.xlabel('t [ns]'); plt.ylabel('U(t) [mV]')
            #plt.show()
            f = InterpolatedUnivariateSpline(t,U, k=1)
            integral=f.integral(min(t), max(t))
            #print integral
            results_clear.append(integral)
            results_peak_clear.append(UMAX)
            
    print 'Finished clear fiber, starting ws', ws
    for filename in os.listdir(ws):
        if filename.endswith(".CSV"):
            #print filename
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
                        aaa=1

            #Uaverage=sum(U[7000:len(U)])/(len(U)-7000) 
            Uaverage=sum(U[0:int(0.3*len(U))])/(0.3*len(U))
            #print 'WS pedestrial: ', Uaverage
            #Uaverage=U[0]
            #Uaverage=0.
            offset(U,Uaverage)  
            UMAX=max(U)
            plt.plot(t, U)
            plt.xlabel('t [ns]'); plt.ylabel('U(t) [mV]')
            #plt.show()
            #time.sleep(100.)
            f = InterpolatedUnivariateSpline(t,U, k=1)
            integral=f.integral(min(t), max(t))
            results_ws.append(integral)
            results_peak_ws.append(UMAX)
    print 'Finishe ws'
    Min=min(results_ws+results_clear)
    Max=max(results_ws+results_clear)
    MinU=min(results_peak_ws+ results_peak_clear)
    MaxU=max(results_peak_clear+ results_peak_ws)

    print MinU, MaxU
    
    hist_clear=TH1D("clear", "clear", 200, Min, Max)
    hist_ws=TH1D("ws", "ws", 200, Min, Max)
    
    histU_clear=TH1D("clear", "clear", 200, MinU, MaxU)
    histU_ws=TH1D("ws", "ws", 200, MinU, MaxU)
    

    for c in results_clear:
        hist_clear.Fill(c)
    for w in results_ws:
        hist_ws.Fill(w)
    for c in results_peak_clear:
        histU_clear.Fill(c)
    for w in results_peak_ws:
        histU_ws.Fill(w)

        

    mean_ws= hist_ws.GetMean()
    mean_clear= hist_clear.GetMean()
    

    RMS_ws= hist_ws.GetRMS()
    RMS_clear= hist_clear.GetRMS()
    
    meanU_ws= histU_ws.GetMean()
    meanU_clear= histU_clear.GetMean()
    
    RMSU_ws= histU_ws.GetRMS()
    RMSU_clear= histU_clear.GetRMS()    
    

    Min=max(Min, min(mean_ws-4.*RMS_ws, mean_clear -4.*RMS_clear))
    Max=min(Max, max(mean_ws+4.*RMS_ws, mean_clear +4.*RMS_clear))

    MinU=max(MinU, min(meanU_ws-4.*RMSU_ws, meanU_clear -4.*RMSU_clear))
    MaxU=min(MaxU, max(meanU_ws+4.*RMSU_ws, meanU_clear +4.*RMSU_clear))    
    print meanU_ws, meanU_clear
    print MinU, MaxU
    
    hist_clear=TH1D("clear", "clear", 200, Min, Max)
    hist_ws=TH1D("ws", "ws", 200, Min, Max)
    
    histU_clear=TH1D("clear", "clear", 200, MinU, MaxU)
    histU_ws=TH1D("ws", "ws", 200, MinU, MaxU)
    
  
    
    for c in results_clear:
        hist_clear.Fill(c)
    for w in results_ws:
        hist_ws.Fill(w)
    for c in results_peak_clear:
        histU_clear.Fill(c)
    for w in results_peak_ws:
        histU_ws.Fill(w)

    
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

    histU_clear.SetLineColor(kBlue+3)
    histU_clear.SetLineWidth(3)

    histU_ws.SetLineColor(kYellow+3)
    histU_ws.SetLineWidth(3)

    histU_clear.SetTitle("")
    histU_clear.GetXaxis().SetTitle("[mV]")


    histU_ws.SetTitle("")
    histU_ws.GetXaxis().SetTitle("[mV]")

    histU_clear.SetStats(False)
    histU_ws.SetStats(False) 
    
    hist_ws.DrawNormalized()
    hist_clear.DrawNormalized("SAME")

    leg=TLegend(0.35, 0.5, 0.6,0.8)
    leg.AddEntry(hist_clear, "Clear Fiber, "+color, "f")
    leg.AddEntry(hist_ws, "WaveShifter, "+color, "f")     

    leg.Draw()

    c1.SaveAs("results_"+color+".pdf")

    histU_ws.DrawNormalized()
    histU_clear.DrawNormalized("SAME")
    
    leg=TLegend(0.35, 0.5, 0.6,0.8)
    leg.AddEntry(histU_clear, "Clear Fiber, "+color, "f")
    leg.AddEntry(histU_ws, "WaveShifter, "+color, "f")     

    leg.Draw()

    c1.SaveAs("resultsU_"+color+".pdf")




    plt.savefig("pulse_"+color+".png")
    plt.savefig("pulse_"+color+".pdf")
    plt.savefig("pulse_"+color+"self.eps")
    
    plt.clf()

def main(argv):
    for i in measurmeents:
        #print i["Clear Fiber"], i["Wave Shifter"], i
        print Filename(i), measurmeents[i]["Clear Fiber"], measurmeents[i]["Wave Shifter"]
        ana_color(measurmeents[i]["Clear Fiber"],
                  measurmeents[i]["Wave Shifter"],
                  Filename(i))

if __name__=="__main__":
    sys.exit(main(sys.argv))
