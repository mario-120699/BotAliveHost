import nmap


nmScan = nmap.PortScanner()
nmScan.scan('188.209.80.62', '0-1024')
for port in nmScan['188.209.80.62']['tcp']:
    thisDict = nmScan['188.209.80.62']['tcp'][port]
    print('Port ' + str(port) + ': ' + thisDict['product'] + ', v' + thisDict['version'])
