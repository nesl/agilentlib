import urllib

SineKey = 31
SquareKey = 26
RampKey = 21
PulseKey = 16
NoiseKey = 11
ArbKey = 6
ManTrgKey = 1
ModKey = 30
SweepKey = 25
BurstKey = 20
StoreRc1Key = 15
UtilityKey = 10
HelpKey = 5
OutputKey = 0

KnobCW = 50
KnobCCW = 51
LeftArrow=23
RightArrow=18

# Search the Vaults of Parnassus for "XMLForms".
# First, encode the data.
data = urllib.urlencode({"KeyPunch" : KnobCW})
# Now get that file-like object again, remembering to mention the data.
f = urllib.urlopen("http://172.17.100.14/Forms/remote_fp_1", data)
# Read the results back.
s = f.read()
print s
f.close()
