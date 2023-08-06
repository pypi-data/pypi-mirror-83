#
#-*- coding:utf-8 -*-
"""
A module to support Tektronix TDS3000 series OSC. Mostly work with other OSC from Tektronix, with minor modification.
(C) Noboru Yamamoto,2009. KEK, Ibaraki, JAPAN
Referenc:
 "TDS3000,TDS3000B, and TDS3000C series Digital Phosphor Oscilloscopes", 071--381-03,Tektronix

 RPS server info on TDS300
  Get RPC info
   program vers proto   port
    395183    1   tcp   1008 # VXI11-core
    395184    1   tcp   1005 # VXI11-async

DPO4034B:
Starting Nmap 6.40-2 ( http://nmap.org ) at 2013-12-17 09:40 JST
Nmap scan report for 192.168.2.4
Host is up (0.00014s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE
80/tcp   open  http
81/tcp   open  hosts2-ns -> e-Scope 
111/tcp  open  rpcbind
1001/tcp open  unknown -> VXI11-asyn
MAC Address: 08:00:11:1F:38:64 (Tektronix)

Nmap done: 1 IP address (1 host up) scanned in 0.20 seconds
[noboru-mbookpro:~] noboru% rpcinfo -p 192.168.2.4
   program vers proto   port
    100000    2   tcp    111  portmapper
    100000    2   udp    111  portmapper
    395183    1   tcp    998  # VXI11-core
    395184    1   tcp   1001  # VXI11-asyn

"""
from TekOSC import *
from TekOSC import waveform as _waveform

class TekDPO(TekOSC):
    # for DPO4K device="inst0"
    def __init__(self,host,device="inst0,0",proto="tcp"):
        TekOSC.__init__(self,host,device,proto)
        self.write(b"VERBOSE OFF;")
        
    def get_cursor(self):
        self.write(b":CURS?;")
        resp=self.read(requestSize=4096)[:-1]
        return DPOCursor(resp)
    
    def get_waveform(self,ch=1,io_timeout=3000,requestSize=4096):
        if (type(ch) == types.StringType):
            self.write(b":DAT:SOU %s;"%ch)
        else:
            self.write(b":DAT:SOU CH%d;"%ch)
        h=self.ask(b":WFMO?;") # this opeation may take 0.3 sec avg.
        self.write(b":curve?;")
        #time.sleep(0.3) # need to wait until DPO is ready to send
        r=self.readResponce(io_timeout=io_timeout, requestSize=requestSize)
        if r:
            wf=waveform(h,r)
        else:
            raise IOError("No value")
        return wf

    def get_curve(self,ch=1,io_timeout=3000, requestSize=4096):
        self.write(b":DAT:SOU CH%d;:CURV?;"%ch)
        #time.sleep(0.5) # need to wait until DPO is ready to send
        return self.readResponce(io_timeout=io_timeout,
                                requestSize=requestSize)

    def set_fulldata(self): # well, it is not quite correct.
        #
        self.write(b"HOR:RECO 10000000;")
        self.write(b":DATA:START 1;")
        self.write(b":DATA:STOP 10000000;")

    def set_wf_binary(self,fmt="RIBIN"):
        self.write(b":DATA:ENC %s;"%fmt)
        
    def set_wf_ascii(self):
        self.write(b":DATA:ENC ASCI;")

    def set_ENC(self, mode):
        #enc=("ASCIi","FAStest",
        #"RIBinary","RPBinary",
        #"SRIbinary","SRPbinary")
        enc=("ASCI","RIB","RPB","SRI","SRP")
        if (mode in enc):
            self.write(b":DATA:ENC %s;"%mode)
        elif type(mode) is types.StringType:
            self.write(b":DATA:ENC %s;"%mode)
        else:
            self.write(b":DATA:ENC %s;"%enc[mode])

    def set_byte_width(self,nb):
        "nb should be 1 or 2"
        if (nb == 1) or (nb ==2):
            self.write(b":WFMO:BYT_N %d"%nb)
        else:
            raise ValueError("argument out of range")
        
    def set_record_length(self,recl):
        #recl:100,10000,100000,5000000 for DPO3k(?)
        #recl:100,10000,100000,10000000,20000000 for DPO4k 
        self.write(b"HOR:RECO %d"%recl)
        self.write(b"WFMINPRE:NR_PT %d"%recl)
        self.write(b":DATA:START 1")
        self.write(b":DATA:STOP %d"%recl)

    def get_SESR(self):
        self.write(b"*ESR?;")
        return SESR(int(self.read()))

    def get_SBR(self):
        self.write(b"*STB?;")
        return SBR(int(self.read()))

    def get_DESER(self):
        self.write(b":DESE?;")
        return DESER(self.read())

    def get_ESER(self):
        self.write(b"*ESE?;")
        return ESER(self.read())

    def get_SRER(self):
        self.write(b"*SRE?;")
        return SRER(self.read())

    def get_measurement(self,requestSize=4096):
        self.write(b":MEASU?;")
        return self.readResponce(requestSize=requestSize)

    def qACQ(self):
        labels=(
            'STOPAFTER',
            'STATE',
            'MODE',
            'NUMENV',
            'NUMAVG',
            'SAMPLINGMODE'
            )
        acq=self.ask(b":ACQ?")
        d=self.respToDict(labels,acq)
        if d:
            self.__dict__.update(d)

    def qDATA(self):
        labels=('DESTINATION', 'ENCDG', 'SOURCE', 'START', 'STOP', 'WIDTH')
        self.QueryForDict(":DATA?",labels)
            
    def QueryForDict(self,cmd,labels):
        acq=self.ask(cmd)
        d=self.respToDict(labels,acq)
        if d:
            self.__dict__.update(d)
        
def bit(n,d):
    return (d>>n)&1
    
class Register:
    def __init__(self,ini_data):
        self.val=int(ini_data)

    def __str__(self):
        s=""
        for item in self.__dict__.items():
            if item[0] == "val":
                continue
            s+="%s:%d, "%item
        return s

class SESR(Register):
    """Standard Event Status Register
    bit7...................................bit.0
    PON | URQ | CME | EXE | DDE| QYE| RQC | OPC
    """
    def __init__(self,ini_data):
        Register.__init__(self,ini_data)
        self.pon=bit(7,self.val)
        self.urq=bit(6,self.val)
        self.cme=bit(5,self.val)
        self.exe=bit(4,self.val)
        self.dde=bit(3,self.val)
        self.qye=bit(2,self.val)
        self.rqc=bit(1,self.val)
        self.opc=bit(0,self.val)
        
class SBR(Register):
    """Status Byte Register
    bit7..................................bit.0
    - | RQS/MSS | ESB| MAV | - |  - |  - |  - 
    """
    def __init__(self,ini_data):
        Register.__init__(self,ini_data)
        self.rqs=bit(6,self.val)
        self.mss=bit(6,self.val)
        self.esb=bit(5,self.val)
        self.mav=bit(4,self.val)

class DESER(Register):
    """ Device Event Status Enable Register"
    bit7..................................bit.0
    PON | URQ | CME | EXE | DDE | QYE | RQC | OPC
    """
    def __init__(self,ini_data):
        Register.__init__(self,ini_data)
        self.pon=bit(7,self.val)
        self.urq=bit(6,self.val)
        self.cme=bit(5,self.val)
        self.exe=bit(4,self.val)
        self.dde=bit(3,self.val)
        self.qye=bit(2,self.val)
        self.rqc=bit(1,self.val)
        self.opc=bit(0,self.val)

class ESER(Register):
    """ Event Status Enable Register"
    bit7..................................bit.0
    PON | URQ | CME | EXE | DDE | QYE | RQC | OPC
    """
    def __init__(self,ini_data):
        Register.__init__(self,ini_data)
        self.pon=bit(7,self.val)
        self.urq=bit(6,self.val)
        self.cme=bit(5,self.val)
        self.exe=bit(4,self.val)
        self.dde=bit(3,self.val)
        self.qye=bit(2,self.val)
        self.rqc=bit(1,self.val)
        self.opc=bit(0,self.val)

class SRER(Register):
    """ Service Request Enable Register"
    bit7...........................bit.0
    - | - | ESB | MAV | - | - | - | -
    """
    def __init__(self,ini_data):
        Register.__init__(self,ini_data)
        self.esb=bit(5,self.val)
        self.mav=bit(4,self.val)
#
# data objects
#
class waveform(_waveform):
    enc={"ASCII":"%d","RIBINARY":">h",'RPBINARY':">H",'SRIBINARY':"<h",'SRPBINARY':"<H"}
    BFMT={'RI':{1:"b",2:"h",4:"l",8:"q"},'RP':{1:"B",2:"H",4:"L",8:"Q"}}
    BORD={"MSB":">","LSB":"<"}
    """
    Preample for TDS3k:
        
    preamble for DPO3k:
    >>> dpo3k.ask(b":WFMO?;")
    '1;8;BIN;RI;MSB;"Ch1, DC coupling, 5.000mV/div, 400.0us/div, 10000 points, Sample mode";10000;Y;"s";400.0000E-9;-2.0000E-3;0;"V";200.0000E-6;0.0E+0;0.0E+0\n'

    preamble for DPO7k:
    >>> dpo7k.ask(b":WFMO?;")
    '2;16;BIN;RI;MSB;"Ch1, DC coupling, 1.000mV/div, 1.000us/div, 10000 points, Sample mode";10000;Y;"s";1.0000E-9;0.0000;5000;"V";156.2500E-9;18.4320E+3;0.0000;1\n'
    """

    def __init__(self,preamble,wfdata):
        """
        Examples WAVFRM? might return the waveform data as:(VERBOSE 0, header 1)
        :WFMOUTPRE:BYT_NR 1;BIT_NR 8;ENCDG ASCII;BN_FMT RI;BYT_OR MSB;
        "Ch1, DC coupling, 100.0mV/div, 4.000us/div, 10000 points, Sample ";
        NR_PT 20;PT_FMT Y;X_UNIT "s";XINCR 4.0000E-9;XZERO -20.0000E-6;PT_OFF 0;
        YUNIT "V";YMULT 4.0000E-3;YOFF 0.0000;YZERO 0.0000;
        :CURVE 2,1,4,2,4,3,0,3,3,3,3,3,3,4,3,5,6,6,7,3....
        """
        self.rdata=preamble.split(";")
        self.rdata.append(wfdata)
        if (len(self.rdata) < 17):
            sys.stderr.write(b"%s data read:"%(self.rdata[:16], len(self.rdata)))
            raise ValueError("Not enough data")

        self.byte_width=int(self.rdata[0])
        self.bit_width=int(self.rdata[1])
        self.ENC=self.rdata[2]
        self.BIN_FMT=self.rdata[3]
        self.BYTE_ORDER=self.rdata[4]
        self.wfid=self.rdata[5]
        self.Data_Num=int(self.rdata[6])
        self.point_fmt=self.rdata[7]
        self.X_Unit=self.rdata[8]
        self.X_Incr=float(self.rdata[9])
        self.X_Zero=float(self.rdata[10])
        self.Point_Offset=int(self.rdata[11])
        self.Y_Unit=self.rdata[12]
        self.Y_Mult=float(self.rdata[13])
        self.Y_Offset=float(self.rdata[14])
        self.Y_Zero=float(self.rdata[15])

        # curve start from rdata[16] < wrong! On newer models, header may contains more than 17 parameters.
        if (self.ENC == "ASCII" or self.ENC == "ASC"):
            self.conv_fmt=float
            self.wfsize=""
            if (curve[0] == ":"):
                self.raw=wfdata[len(":CURVE "):-1]
            else:
                self.raw=wfdata[:-1]
        else:
            self.conv_fmt=self.BORD[self.BYTE_ORDER]+self.BFMT[self.BIN_FMT][self.byte_width]
            if (wfdata[0] == "#"):
                sz=2+int(wfdata[1])
                self.wfsize=dsz=int(wfdata[2:sz])
                self.raw=wfdata[sz:-1]
            else:
                self.raw=wfdata[:-1]
        #
        self._convert()

    def _convert(self):
        if (self.ENC == "ASCII" or self.ENC == "ASC"):
            self.wf=[float(x) for x in self.raw.split(",")]
        else:
            self.wf=[struct.unpack(self.conv_fmt,self.raw[i:i+self.byte_width])[0]
                     for i in range(0,len(self.raw),self.byte_width)]
        
        self.y=[((y-self.Y_Offset)*self.Y_Mult+self.Y_Zero) for y in self.wf]
        self.x=[ (x*self.X_Incr+self.X_Zero) for x in range(len(self.y))]
        
class DPOCursor(TekCursor):
    """
    0 :CURS:FUNC SCREEN
    1 MOD IND
    2 VBA:POSITION1 -391.000E-6
    3 POSITION2 347.000E-6
    4 DELT 738.0000E-6
    5 HPOS1 -5.080E-3
    6 HPOS2 5.080E-3
    7 UNI SEC
    8 VDELT 10.1600E-3
    9 :CURS:HBA:DELT 4.7000E-3
    10 POSITION1 2.9200E-3
    11 POSITION2 -1.7800E-3
    12 UNI BAS
    13 :CURS:XY:RECT:X:POSITION1 0.0E+0
    14 POSITION2 0.0E+0
    15 UNI "s"
    16 DEL 0.0E+0
    17 :CURS:XY:RECT:Y:POSITION1 0.0E+0
    18 POSITION2 0.0E+0
    19 UNI "s"
    20 DEL 0.0E+0
    21 :CURS:XY:POL:RADIUS:POSITION1 0.0E+0
    22 POSITION2 0.0E+0
    23 UNI "s"
    24 DEL 0.0E+0
    25 :CURS:XY:POL:THETA:POSITION1 0.0E+0
    26 POSITION2 0.0E+0
    27 UNI "s"
    28 DEL 0.0E+0
    29 :CURS:XY:PRODUCT:POSITION1 0.0E+0
    30 POSITION2 0.0E+0
    31 UNI "s"
    32 DEL 0.0E+0
    33 :CURS:XY:RATIO:POSITION1 0.0E+0
    34 POSITION2 0.0E+0
    35 UNI "s"
    36 DEL 0.0E+0
    """
    def __init__(self,data):
        ent=data.split(";")
        self.function=ent[0]
        self.mode=ent[1]
        self.vba_unit=ent[7]
        self.vba=(float(ent[2]),float(ent[3]),float(ent[4]),
                  float(ent[5]),float(ent[6]),float(ent[8]))
        self.hba=(float(ent[9]),float(ent[10]),float(ent[11]))
        self.hba_unit=ent[12]
        self.xy_rect_x_unit=ent[15]
        self.xy_rect_x=(float(ent[13]),float(ent[14]),float(ent[16]))
        self.xy_rect_y_unit=ent[19]
        self.xy_rect_y=(float(ent[17]),float(ent[18]),float(ent[20]))
        self.xy_pol_r_unit=ent[23]
        self.xy_pol_r=(float(ent[21]),float(ent[22]),float(ent[24]))
        self.xy_pol_t_unit=ent[27]
        self.xy_pol_t=(float(ent[25]),float(ent[26]),float(ent[28]))
        self.xy_product_unit=ent[31]
        self.xy_product=(float(ent[29]),float(ent[30]),float(ent[32]))
        self.xy_ratio_unit=ent[35]
        self.xy_ratio=(float(ent[33]),float(ent[34]),float(ent[36]))

# def test(hostip="10.8.46.20",device="inst0"):
#     import Gnuplot
#     tek=TekOSC(hostip,device=device)
#     #tek.set_fulldata()
#     gp=Gnuplot.Gnuplot()
#     return (tek,gp)

def test_run(tek):
    runstate=tek.qAcqState()
    stopafter=tek.qAcqStopAfter()
    tek.Stop()
    tek.set_AcqStopAfter("SEQ")
    tek.Run();tek.qOPC()
    wf1,wf2=test_update(tek)
    tek.set_AcqStopAfter(stopafter)
    tek.set_AcqState(runstate)
    return (wf1,wf2)

def test_update(tek):
    wf1=tek.get_waveform(1)
    wf2=tek.get_waveform(2)
    return (wf1,wf2)

def test_srq(hostname="192.168.2.4", device="inst0"):
    """
    To generate a service request (SRQ) interrupt to an external controller, at least one bit in the Status Byte Register must be enabled. These bits are enabled by using the *SRE common command to set the corresponding bit in the Service Request Enable Register. These enabled bits can then set RQS and MSS (bit 6) in the Status Byte Register.
    """
    import select,threading,atexit
    osc=tek=TekOSC(hostname,device)
    #osc.create_intr_chan(proto=cVXI11.Device_AddrFamily.DEVICE_UDP)
    osc.createSVCThread()
    sys.stdout.write(b"Thread Created\n")
    osc.Stop()
    #osc.set_wf_point_mode("MAX")
    #osc.set_wf_point("5000")
    osc.write(b":DESE 1") #OPC
    osc.write(b"*ESE 1") #Pon(7)/URQ(6)/CME(5)/EXE(4)/DDE(3)/QYE(2)/RQL(1)/OPC(0)
    osc.write(b"*SRE 32") # SRE /ESB(5)/MAV(4)
    osc.write(b"*SRE 48") # enable all SRQ source
    osc.write(b"*OPC")
    osc.enable_srq()
    #
    osc.check_SRQ_source()
    osc.svc_lock.acquire(Flase)
    sys.stdout.write(b"%s"%osc.svc_lock.locked()) #should be True
    osc.write(b":ACQ:STATE RUN;*OPC;")
    sys.stdout.write(b"%s"%osc.svc_lock.locked())
    return osc

def test_dpo(host=b"169.254.254.254"):
    dev=Vxi11Device(host,device=b"inst0")
    return dev

if __name__ == "__main__":
    test("169.254.4.84")
