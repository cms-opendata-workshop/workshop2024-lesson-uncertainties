from ROOT import TH1F, TFile
import pickle

f = open('hists_for_ROOT.p', 'rb')
hists = pickle.load(f)
f.close()

xsec = {'signal':1.0,
        'tt_semilep':831.76*0.438,
        'tt_had':831.76*0.457,
        'tt_lep':831.76*0.105,
        'wjets':61526.7}

roothists = {}
for sample in hists.keys():
    print(sample)

    mtt = hists[sample]['mtt']

    if sample == "data":
        roothists[sample] = TH1F("mtt__data_obs",";m_{t#bar{t}} (GeV);events",50,0,3000)
        roothists[sample].FillN(len(mtt), mtt, np.ones(len(mtt)))
    else:
        genweight = hists[sample]['genWeight']
        Ngen = hists[sample]['N_gen']

        lumiweight = 16400*xsec[sample]*hists[sample]['genWeight']/Ngen 
        weight = lumiweight*hists[sample]['pu_weight']*hists[sample]['muId_weight']
        pu_weight_up = lumiweight*hists[sample]['pu_weight_up']*hists[sample]['muId_weight']
        pu_weight_dn = lumiweight*hists[sample]['pu_weight_dn']*hists[sample]['muId_weight']
        muId_weight_up = lumiweight*hists[sample]['pu_weight']*hists[sample]['muId_weight_up']
        muId_weight_dn = lumiweight*hists[sample]['pu_weight']*hists[sample]['muId_weight_dn']

        roothists[sample+'_nominal'] = TH1F("mtt__"+sample,";m_{t#bar{t}} (GeV);events",50,0,3000)
        roothists[sample+'_nominal'].FillN(len(mtt), mtt, weight)
        roothists[sample+'_puUp'] = TH1F("mtt__"+sample+"__puUp",";m_{t#bar{t}} (GeV);events",50,0,3000)
        roothists[sample+'_puUp'].FillN(len(mtt), mtt, pu_weight_up)
        roothists[sample+'_puDn'] = TH1F("mtt__"+sample+"__puDown",";m_{t#bar{t}} (GeV);events",50,0,3000)
        roothists[sample+'_puDn'].FillN(len(mtt), mtt, pu_weight_dn)
        roothists[sample+'_muIdUp'] = TH1F("mtt__"+sample+"__muIdUp",";m_{t#bar{t}} (GeV);events",50,0,3000)
        roothists[sample+'_muIdUp'].FillN(len(mtt), mtt, muId_weight_up)
        roothists[sample+'_muIdDn'] = TH1F("mtt__"+sample+"__muIdDown",";m_{t#bar{t}} (GeV);events",50,0,3000)
        roothists[sample+'_muIdDn'].FillN(len(mtt), mtt, muId_weight_dn)

output = TFile.Open("Zprime_hists_FULL.root","recreate")
for ihist in roothists:
    roothists[ihist].Write()

output.Close()


