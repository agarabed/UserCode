import sys, os
import ROOT as R

class BrazilPlot:

    def __init__(self,name='default',title = 'default', lumi = 19711, xarray=[1,2],xlabel='default var [units]',limits=[1,1],ylabel = 'cross section',oneSig = [.25,.25],twoSig=[.5,.5],AddLimitFiles=[]):
        self.name = name; self.title=title; self.lumi=lumi; self.xarray = xarray; self.xlabel = xlabel; self.limits = limits; self.ylabel = ylabel; self.oneSig = oneSig; self.twoSig=twoSig; self.Theory = {}; self.AddLimitFiles = AddLimitFiles
        self.AddLimits = {}
    
    def getLimitsTheta(self, LimitFile):
        self.xarray = []; self.limits=[]; self.oneSig=[]; self.twoSig=[]
        
        file = open(LimitFile, 'r')
        for line in file:
            if 'high' in line: continue
            values = [float(x) for x in line.replace('\n','').split(' ') if x != '']
            print values
            self.xarray.append(values[0])
            self.limits.append(values[1])
            self.oneSig.append([values[4],values[5]])
            self.twoSig.append([values[2],values[3]])
        file.close()

    def getAddLimitsTheta(self, LimitFile, AddLabel):
        try:
            self.AddLimits[AddLabel] = []; self.Addxarray[AddLabel] = [];
        except:
            self.Addxarray = {}; self.Addlimits={};
            self.AddLimits[AddLabel] = []; self.Addxarray[AddLabel] = [];
    
        file = open(LimitFile, 'r')
        for line in file:
            if 'high' in line: continue
            values = [float(x) for x in line.replace('\n','').split(' ') if x != '']
            print values
            self.Addxarray[AddLabel].append(values[0])
            self.AddLimits[AddLabel].append(values[1])
        file.close()

    def getTheory(self, signal='Chiggs'):
        self.Theory = {}
        
        if signal == 'Chiggs':
            self.Theory[200] = 1.485*1.317e-1
            self.Theory[300] = 1.556*9.016e-2
            self.Theory[400] = 1.631*3.848e-2
            self.Theory[500] = 1.695*1.713e-2
            self.Theory[600] = 1.74*8.066e-3
            self.Theory[700] = 1.788*4.004e-3
            self.Theory[800] = 1.828*2.071e-3

        if signal == 'Hplus':
            self.Theory[180] = 2*0.1501*0.081662
            self.Theory[200] = 2*0.1280*0.455760
            self.Theory[220] = 0.154027*0.893554
            #self.Theory[240] = 0.129842*0.950975
            self.Theory[250] = 2*0.07624*0.705360
            #self.Theory[260] = 0.109879*0.963801
            self.Theory[300] = 2*0.04643*0.744171
            #self.Theory[350] = 0.0536621*0.981614
            self.Theory[400] = 2*0.02942*0.722967
            self.Theory[500] = 2*0.00827*0.563428
            self.Theory[600] = 2*0.00390*0.495196
            #self.Theory[700] = 0.0056681*0.995767

    def plot(self, ylog=True):
        
        self.GraphTwoSig    = R.TGraphAsymmErrors(len(self.xarray))
        self.GraphTwoSig.SetName('2sig')
        self.GraphTwoSig.SetFillColor(R.kYellow)
        self.GraphTwoSig.SetTitle(self.title)
        
        self.GraphOneSig    = R.TGraphAsymmErrors(len(self.xarray))
        self.GraphOneSig.SetName('1sig')
        self.GraphOneSig.SetFillColor(R.kGreen)
        
        self.GraphNom       = R.TGraph(len(self.xarray))
        self.GraphNom.SetName('nom')
        self.GraphNom.SetLineStyle(2)
        self.GraphNom.SetLineWidth(3)
        
        if self.AddLimitFiles != {}:
            self.AddGraphs = {}
            for AddLabel in self.AddLimits:
                self.AddGraphs[AddLabel] = R.TGraph(len(self.xarray))
                self.AddGraphs[AddLabel].SetName('AddLabel')
                self.AddGraphs[AddLabel].SetLineStyle(6)
                self.AddGraphs[AddLabel].SetLineWidth(3)

        for i in range(len(self.xarray)):
            self.GraphNom.SetPoint(i, self.xarray[i], self.limits[i])
            
            self.GraphOneSig.SetPoint(i, self.xarray[i], self.limits[i])
            self.GraphOneSig.SetPointEYlow(i,self.limits[i]-self.oneSig[i][0])
            self.GraphOneSig.SetPointEYhigh(i,self.oneSig[i][1]-self.limits[i])
        
            self.GraphTwoSig.SetPoint(i, self.xarray[i], self.limits[i])
            self.GraphTwoSig.SetPointEYlow(i,self.limits[i]-self.twoSig[i][0])
            self.GraphTwoSig.SetPointEYhigh(i,self.twoSig[i][1]-self.limits[i])
                
            if self.AddLimitFiles != {}:
                for AddLabel in self.AddLimits:
                    self.AddGraphs[AddLabel].SetPoint(i, self.Addxarray[AddLabel][i], self.AddLimits[AddLabel][i])
        
        if self.Theory != {}:
            self.GraphTheory = R.TGraph(len(self.Theory))
            self.GraphTheory.SetLineColor(R.kRed)
            self.GraphTheory.SetLineStyle(2)
            self.GraphTheory.SetLineWidth(3)
            for i in range(len(self.Theory)):
                self.GraphTheory.SetPoint(i, self.xarray[i], self.Theory[self.xarray[i]])
        
        
            self.GraphTwoSig.SetMinimum(.7*min([min([self.Theory[i] for i in self.Theory]), min([min(i) for i in self.twoSig])]))
            
        self.leg = R.TLegend(.70,.65,.85,.85)
        self.leg.SetFillColor(0)
        self.leg.SetBorderSize(0)
        self.leg.SetShadowColor(0)
        
        self.leg.AddEntry(self.GraphOneSig, '#pm 1 #sigma','F')
        self.leg.AddEntry(self.GraphTwoSig, '#pm 2 #sigma','F')
        self.leg.AddEntry(self.GraphNom, 'Expected', 'l')
        if self.Theory != {}: self.leg.AddEntry(self.GraphTheory, 'Theory','l')
        
        self.PlotCanvas = R.TCanvas(self.name,self.name,1000,700)
        if ylog: self.PlotCanvas.SetLogy()
        self.GraphTwoSig.GetYaxis().SetRangeUser(.001, 5)
        self.GraphTwoSig.Draw('AE3')
        self.GraphOneSig.Draw('E3SAME')
        self.GraphNom.Draw('LSAME')
        if self.AddLimitFiles != {}:
            for AddLabel in self.AddLimits:
                self.AddGraphs[AddLabel].Draw('LSAME')
        if self.Theory != {}: self.GraphTheory.Draw('LSAME')
        self.leg.Draw('SAME')
        
        prelimTex=R.TLatex()
        prelimTex.SetNDC()
        prelimTex.SetTextSize(0.04)
        prelimTex.SetTextAlign(31) # align right
        lumi=self.lumi/1000.
        lumi=round(lumi,2)
        prelimTex.DrawLatex(0.9, 0.92, "CMS Preliminary, "+str(lumi)+" fb^{-1} at #sqrt{s} = 8 TeV");
        
        self.GraphTwoSig.GetXaxis().SetTitle(self.xlabel)
        self.GraphTwoSig.GetXaxis().SetTitleSize(.05)
        self.GraphTwoSig.GetXaxis().SetTitleOffset(.85)
        self.GraphTwoSig.GetYaxis().SetTitle(self.ylabel)
        self.GraphTwoSig.GetYaxis().SetTitleSize(.05)
        self.GraphTwoSig.GetYaxis().SetTitleOffset(.85)
        self.PlotCanvas.SaveAs(self.name + '_limits.pdf')
        self.PlotCanvas.SaveAs(self.name + '_limits.root')
        self.PlotCanvas.SaveAs(self.name + '_limits.C')

file = sys.argv[1]
if len(sys.argv) > 2:
    additional = sys.argv[2:]
else:
    additional = []

a = BrazilPlot(name ='Ht', title='', xlabel='H^{+/-} mass [GeV]', ylabel = 'Expected Limit [pb]', AddLimitFiles = additional)
a.getLimitsTheta(file)

for moreLimits in additional:
    if 'UP' in moreLimits: label = 'UP'
    if 'DOWN' in moreLimits: label = 'DOWN'
    a.getAddLimitsTheta(moreLimits, label)

a.getTheory('Hplus')
a.plot()