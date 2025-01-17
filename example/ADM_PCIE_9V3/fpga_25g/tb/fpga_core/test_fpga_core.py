"""

Copyright (c) 2020 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import logging
import os

from scapy.layers.l2 import Ether, ARP
from scapy.layers.inet import IP, UDP
from scapy.all import *

import cocotb_test.simulator

import cocotb
from cocotb.log import SimLog
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

from cocotbext.eth import XgmiiFrame, XgmiiSource, XgmiiSink
from cocotbext.axi import AxiStreamFrame, AxiStreamBus, AxiStreamSource, AxiStreamSink 

from netaddr import *

class TB:
    def __init__(self, dut):
        self.dut = dut

        self.log = SimLog("cocotb.tb")
        self.log.setLevel(logging.DEBUG)

        cocotb.start_soon(Clock(dut.clk, 2.56, units="ns").start())

        self.source = AxiStreamSource(AxiStreamBus.from_prefix(dut, "tx_payload_axis"), dut.clk, dut.rst)
        self.sink = AxiStreamSink(AxiStreamBus.from_prefix(dut, "rx_payload_axis"), dut.clk, dut.rst)
        # Ethernet
        cocotb.start_soon(Clock(dut.qsfp_0_rx_clk_0, 2.56, units="ns").start())
        self.qsfp_0_0_source = XgmiiSource(dut.qsfp_0_rxd_0, dut.qsfp_0_rxc_0, dut.qsfp_0_rx_clk_0, dut.qsfp_0_rx_rst_0)
        cocotb.start_soon(Clock(dut.qsfp_0_tx_clk_0, 2.56, units="ns").start())
        self.qsfp_0_0_sink = XgmiiSink(dut.qsfp_0_txd_0, dut.qsfp_0_txc_0, dut.qsfp_0_tx_clk_0, dut.qsfp_0_tx_rst_0)

        cocotb.start_soon(Clock(dut.qsfp_0_rx_clk_1, 2.56, units="ns").start())
        self.qsfp_0_1_source = XgmiiSource(dut.qsfp_0_rxd_1, dut.qsfp_0_rxc_1, dut.qsfp_0_rx_clk_1, dut.qsfp_0_rx_rst_1)
        cocotb.start_soon(Clock(dut.qsfp_0_tx_clk_1, 2.56, units="ns").start())
        self.qsfp_0_1_sink = XgmiiSink(dut.qsfp_0_txd_1, dut.qsfp_0_txc_1, dut.qsfp_0_tx_clk_1, dut.qsfp_0_tx_rst_1)

        cocotb.start_soon(Clock(dut.qsfp_0_rx_clk_2, 2.56, units="ns").start())
        self.qsfp_0_2_source = XgmiiSource(dut.qsfp_0_rxd_2, dut.qsfp_0_rxc_2, dut.qsfp_0_rx_clk_2, dut.qsfp_0_rx_rst_2)
        cocotb.start_soon(Clock(dut.qsfp_0_tx_clk_2, 2.56, units="ns").start())
        self.qsfp_0_2_sink = XgmiiSink(dut.qsfp_0_txd_2, dut.qsfp_0_txc_2, dut.qsfp_0_tx_clk_2, dut.qsfp_0_tx_rst_2)

        cocotb.start_soon(Clock(dut.qsfp_0_rx_clk_3, 2.56, units="ns").start())
        self.qsfp_0_3_source = XgmiiSource(dut.qsfp_0_rxd_3, dut.qsfp_0_rxc_3, dut.qsfp_0_rx_clk_3, dut.qsfp_0_rx_rst_3)
        cocotb.start_soon(Clock(dut.qsfp_0_tx_clk_3, 2.56, units="ns").start())
        self.qsfp_0_3_sink = XgmiiSink(dut.qsfp_0_txd_3, dut.qsfp_0_txc_3, dut.qsfp_0_tx_clk_3, dut.qsfp_0_tx_rst_3)

        cocotb.start_soon(Clock(dut.qsfp_1_rx_clk_0, 2.56, units="ns").start())
        self.qsfp_1_0_source = XgmiiSource(dut.qsfp_1_rxd_0, dut.qsfp_1_rxc_0, dut.qsfp_1_rx_clk_0, dut.qsfp_1_rx_rst_0)
        cocotb.start_soon(Clock(dut.qsfp_1_tx_clk_0, 2.56, units="ns").start())
        self.qsfp_1_0_sink = XgmiiSink(dut.qsfp_1_txd_0, dut.qsfp_1_txc_0, dut.qsfp_1_tx_clk_0, dut.qsfp_1_tx_rst_0)

        cocotb.start_soon(Clock(dut.qsfp_1_rx_clk_1, 2.56, units="ns").start())
        self.qsfp_1_1_source = XgmiiSource(dut.qsfp_1_rxd_1, dut.qsfp_1_rxc_1, dut.qsfp_1_rx_clk_1, dut.qsfp_1_rx_rst_1)
        cocotb.start_soon(Clock(dut.qsfp_1_tx_clk_1, 2.56, units="ns").start())
        self.qsfp_1_1_sink = XgmiiSink(dut.qsfp_1_txd_1, dut.qsfp_1_txc_1, dut.qsfp_1_tx_clk_1, dut.qsfp_1_tx_rst_1)

        cocotb.start_soon(Clock(dut.qsfp_1_rx_clk_2, 2.56, units="ns").start())
        self.qsfp_1_2_source = XgmiiSource(dut.qsfp_1_rxd_2, dut.qsfp_1_rxc_2, dut.qsfp_1_rx_clk_2, dut.qsfp_1_rx_rst_2)
        cocotb.start_soon(Clock(dut.qsfp_1_tx_clk_2, 2.56, units="ns").start())
        self.qsfp_1_2_sink = XgmiiSink(dut.qsfp_1_txd_2, dut.qsfp_1_txc_2, dut.qsfp_1_tx_clk_2, dut.qsfp_1_tx_rst_2)

        cocotb.start_soon(Clock(dut.qsfp_1_rx_clk_3, 2.56, units="ns").start())
        self.qsfp_1_3_source = XgmiiSource(dut.qsfp_1_rxd_3, dut.qsfp_1_rxc_3, dut.qsfp_1_rx_clk_3, dut.qsfp_1_rx_rst_3)
        cocotb.start_soon(Clock(dut.qsfp_1_tx_clk_3, 2.56, units="ns").start())
        self.qsfp_1_3_sink = XgmiiSink(dut.qsfp_1_txd_3, dut.qsfp_1_txc_3, dut.qsfp_1_tx_clk_3, dut.qsfp_1_tx_rst_3)

        dut.user_sw.setimmediatevalue(0)

    async def init(self):

        self.dut.rst.setimmediatevalue(0)
        self.dut.qsfp_0_rx_rst_0.setimmediatevalue(0)
        self.dut.qsfp_0_tx_rst_0.setimmediatevalue(0)
        self.dut.qsfp_0_rx_rst_1.setimmediatevalue(0)
        self.dut.qsfp_0_tx_rst_1.setimmediatevalue(0)
        self.dut.qsfp_0_rx_rst_2.setimmediatevalue(0)
        self.dut.qsfp_0_tx_rst_2.setimmediatevalue(0)
        self.dut.qsfp_0_rx_rst_3.setimmediatevalue(0)
        self.dut.qsfp_0_tx_rst_3.setimmediatevalue(0)
        self.dut.qsfp_1_rx_rst_0.setimmediatevalue(0)
        self.dut.qsfp_1_tx_rst_0.setimmediatevalue(0)
        self.dut.qsfp_1_rx_rst_1.setimmediatevalue(0)
        self.dut.qsfp_1_tx_rst_1.setimmediatevalue(0)
        self.dut.qsfp_1_rx_rst_2.setimmediatevalue(0)
        self.dut.qsfp_1_tx_rst_2.setimmediatevalue(0)
        self.dut.qsfp_1_rx_rst_3.setimmediatevalue(0)
        self.dut.qsfp_1_tx_rst_3.setimmediatevalue(0)

        for k in range(10):
            await RisingEdge(self.dut.clk)

        self.dut.rst <= 1
        self.dut.qsfp_0_rx_rst_0 <= 1
        self.dut.qsfp_0_tx_rst_0 <= 1
        self.dut.qsfp_0_rx_rst_1 <= 1
        self.dut.qsfp_0_tx_rst_1 <= 1
        self.dut.qsfp_0_rx_rst_2 <= 1
        self.dut.qsfp_0_tx_rst_2 <= 1
        self.dut.qsfp_0_rx_rst_3 <= 1
        self.dut.qsfp_0_tx_rst_3 <= 1
        self.dut.qsfp_1_rx_rst_0 <= 1
        self.dut.qsfp_1_tx_rst_0 <= 1
        self.dut.qsfp_1_rx_rst_1 <= 1
        self.dut.qsfp_1_tx_rst_1 <= 1
        self.dut.qsfp_1_rx_rst_2 <= 1
        self.dut.qsfp_1_tx_rst_2 <= 1
        self.dut.qsfp_1_rx_rst_3 <= 1
        self.dut.qsfp_1_tx_rst_3 <= 1

        for k in range(10):
            await RisingEdge(self.dut.clk)

        self.dut.rst <= 0
        self.dut.qsfp_0_rx_rst_0 <= 0
        self.dut.qsfp_0_tx_rst_0 <= 0
        self.dut.qsfp_0_rx_rst_1 <= 0
        self.dut.qsfp_0_tx_rst_1 <= 0
        self.dut.qsfp_0_rx_rst_2 <= 0
        self.dut.qsfp_0_tx_rst_2 <= 0
        self.dut.qsfp_0_rx_rst_3 <= 0
        self.dut.qsfp_0_tx_rst_3 <= 0
        self.dut.qsfp_1_rx_rst_0 <= 0
        self.dut.qsfp_1_tx_rst_0 <= 0
        self.dut.qsfp_1_rx_rst_1 <= 0
        self.dut.qsfp_1_tx_rst_1 <= 0
        self.dut.qsfp_1_rx_rst_2 <= 0
        self.dut.qsfp_1_tx_rst_2 <= 0
        self.dut.qsfp_1_rx_rst_3 <= 0
        self.dut.qsfp_1_tx_rst_3 <= 0

    def set_idle_generator(self, generator=None):
        if generator:
            self.source.set_pause_generator(generator())

    def set_backpressure_generator(self, generator=None):
        if generator:
            self.sink.set_pause_generator(generator())

    def set_config(self, local_mac, local_ip, gateway_ip, dest_mac, dest_ip, subnet_mask = '255.255.255.0'):
        self.dut.local_mac = local_mac
        self.dut.local_ip = local_ip
        self.dut.gateway_ip = gateway_ip
        self.dut.subnet_mask = subnet_mask
        self.dut.dest_mac = dest_mac
        self.dut.dest_ip = dest_ip

def size_list():
    data_width = len(cocotb.top.axis_tdata)
    byte_width = data_width // 8
    return list(range(1, byte_width*4+1)) + [512] + [1]*64


def incrementing_payload(length):
    return bytearray(itertools.islice(itertools.cycle(range(256)), length))

"""
def in4_pseudoheader(proto, u, plen):
    # type: (int, IP, int) -> bytes
 
    if u.len is not None:
        if u.ihl is None:
            olen = sum(len(x) for x in u.options)
            ihl = 5 + olen // 4 + (1 if olen % 4 else 0)
        else:
            ihl = u.ihl
        ln = max(u.len - 4 * ihl, 0)
    else:
        ln = plen

    # Filter out IPOption_LSRR and IPOption_SSRR
    sr_options = [opt for opt in u.options if isinstance(opt, IPOption_LSRR) or
                  isinstance(opt, IPOption_SSRR)]
    len_sr_options = len(sr_options)
    if len_sr_options == 1 and len(sr_options[0].routers):
        # The checksum must be computed using the final
        # destination address
        u.dst = sr_options[0].routers[-1]
    elif len_sr_options > 1:
        message = "Found %d Source Routing Options! "
        message += "Falling back to IP.dst for checksum computation."
        warning(message, len_sr_options)

    return struct.pack("!4s4sHH",
                       inet_pton(socket.AF_INET, u.src),
                       inet_pton(socket.AF_INET, u.dst),
                       proto,
                       ln)

"""

@cocotb.test()
async def run_test(dut):

    tb = TB(dut)

    await tb.init()

    #set inserter
    #none
    local_mac = int(EUI('02:00:00:00:00:00'))
    local_ip = int(IPAddress('192.168.1.128'))
    gateway_ip = int(IPAddress('192.168.1.1'))
    subnet_mask = int(IPAddress('255.255.255.0'))
    dest_mac = int(EUI('5a:51:52:53:54:55'))
    dest_ip = int(IPAddress('192.168.1.100'))
    tb.set_config(local_mac, local_ip, gateway_ip, dest_mac, dest_ip, subnet_mask)

    tb.log.info("test UDP RX packet")

    payload = bytes([x % 256 for x in range(256)])
    eth = Ether(src='5a:51:52:53:54:55', dst='02:00:00:00:00:00')
    ip = IP(src='192.168.1.100', dst='192.168.1.128')
    udp = UDP(sport=0, dport=0)
    test_pkt = eth / ip / udp / payload

    tb.log.info("TX packet: %s", repr(test_pkt))

    test_frame = XgmiiFrame.from_payload(test_pkt.build())

    await tb.qsfp_0_0_source.send(test_frame)

    tb.log.info("Receive payload in AXIS")
    rx_frame = await tb.sink.recv()
    #print(in4_pseudoheader(socket.IPPROTO_UDP, test_pkt[IP], len(raw(test_pkt[UDP]))))
    assert rx_frame.tdata == payload
    assert rx_frame.tuser[-1] == 1  #we user tuser as crc ok
    

    

    tb.log.info("Send payload in AXIS")
    test_frame = AxiStreamFrame(payload)
    await tb.source.send(test_frame)


    tb.log.info("receive ARP request")

    rx_frame = await tb.qsfp_0_0_sink.recv()

    rx_pkt = Ether(bytes(rx_frame.get_payload()))

    tb.log.info("RX packet: %s", repr(rx_pkt))

    assert rx_pkt.dst == 'ff:ff:ff:ff:ff:ff'
    assert rx_pkt.src == test_pkt.dst
    assert rx_pkt[ARP].hwtype == 1
    assert rx_pkt[ARP].ptype == 0x0800
    assert rx_pkt[ARP].hwlen == 6
    assert rx_pkt[ARP].plen == 4
    assert rx_pkt[ARP].op == 1
    assert rx_pkt[ARP].hwsrc == test_pkt.dst
    assert rx_pkt[ARP].psrc == test_pkt[IP].dst
    assert rx_pkt[ARP].hwdst == '00:00:00:00:00:00'
    assert rx_pkt[ARP].pdst == test_pkt[IP].src

    tb.log.info("send ARP response")

    eth = Ether(src=test_pkt.src, dst=test_pkt.dst)
    arp = ARP(hwtype=1, ptype=0x0800, hwlen=6, plen=4, op=2,
        hwsrc=test_pkt.src, psrc=test_pkt[IP].src,
        hwdst=test_pkt.dst, pdst=test_pkt[IP].dst)
    resp_pkt = eth / arp

    resp_frame = XgmiiFrame.from_payload(resp_pkt.build())

    await tb.qsfp_0_0_source.send(resp_frame)


    tb.log.info("receive UDP packet")

    rx_frame = await tb.qsfp_0_0_sink.recv()

    rx_pkt = Ether(bytes(rx_frame.get_payload()))

    tb.log.info("RX packet: %s", repr(rx_pkt))

    assert rx_pkt.dst == test_pkt.src
    assert rx_pkt.src == test_pkt.dst
    
    
    assert rx_pkt[IP].dst == test_pkt[IP].src
    assert rx_pkt[IP].src == test_pkt[IP].dst
    #assert rx_pkt[UDP].dport == test_pkt[UDP].sport
    #assert rx_pkt[UDP].sport == test_pkt[UDP].dport   
    #print(hex(rx_pkt[UDP].chksum))
    #chksum = in4_chksum(socket.IPPROTO_UDP, rx_pkt[IP], raw(rx_pkt[UDP]))
    #print(hex( checksum(raw(rx_pkt[UDP].payload))))
    #print(hex(chksum))
    assert bytes(rx_pkt[UDP].payload) == payload

    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)


    tb.log.info("test UDP RX packet 2")

    payload = bytes([x % 256 for x in range(1024)])
    eth = Ether(src='5a:51:52:53:54:55', dst='02:00:00:00:00:00')
    ip = IP(src='192.168.1.100', dst='192.168.1.128')
    udp = UDP(sport=0, dport=0)
    test_pkt = eth / ip / udp / payload

    tb.log.info("TX packet 2: %s", repr(test_pkt))

    test_frame = XgmiiFrame.from_payload(test_pkt.build())

    await tb.qsfp_0_0_source.send(test_frame)

    tb.log.info("Receive payload in AXIS")
    rx_frame = await tb.sink.recv()
    #print(in4_pseudoheader(socket.IPPROTO_UDP, test_pkt[IP], len(raw(test_pkt[UDP]))))
    assert rx_frame.tdata == payload
    assert rx_frame.tuser[-1] == 1  #we user tuser as crc ok

    tb.log.info("Send payload in AXIS 2")
    test_frame = AxiStreamFrame(payload)
    await tb.source.send(test_frame)

    tb.log.info("receive UDP packet")

    rx_frame = await tb.qsfp_0_0_sink.recv()

    rx_pkt = Ether(bytes(rx_frame.get_payload()))

    tb.log.info("RX packet: %s", repr(rx_pkt))

    assert rx_pkt.dst == test_pkt.src
    assert rx_pkt.src == test_pkt.dst
    
    
    assert rx_pkt[IP].dst == test_pkt[IP].src
    assert rx_pkt[IP].src == test_pkt[IP].dst
# cocotb-test

tests_dir = os.path.abspath(os.path.dirname(__file__))
rtl_dir = os.path.abspath(os.path.join(tests_dir, '..', '..', 'rtl'))
lib_dir = os.path.abspath(os.path.join(rtl_dir, '..', 'lib'))
axis_rtl_dir = os.path.abspath(os.path.join(lib_dir, 'eth', 'lib', 'axis', 'rtl'))
eth_rtl_dir = os.path.abspath(os.path.join(lib_dir, 'eth', 'rtl'))


def test_fpga_core(request):
    dut = "fpga_core"
    module = os.path.splitext(os.path.basename(__file__))[0]
    toplevel = dut

    verilog_sources = [
        os.path.join(rtl_dir, f"{dut}.v"),
        os.path.join(eth_rtl_dir, "eth_mac_10g_fifo.v"),
        os.path.join(eth_rtl_dir, "eth_mac_10g.v"),
        os.path.join(eth_rtl_dir, "axis_xgmii_rx_64.v"),
        os.path.join(eth_rtl_dir, "axis_xgmii_tx_64.v"),
        os.path.join(eth_rtl_dir, "lfsr.v"),
        os.path.join(eth_rtl_dir, "eth_axis_rx.v"),
        os.path.join(eth_rtl_dir, "eth_axis_tx.v"),
        os.path.join(eth_rtl_dir, "udp_complete_64.v"),
        os.path.join(eth_rtl_dir, "udp_checksum_gen_64.v"),
        os.path.join(eth_rtl_dir, "udp_64.v"),
        os.path.join(eth_rtl_dir, "udp_ip_rx_64.v"),
        os.path.join(eth_rtl_dir, "udp_ip_tx_64.v"),
        os.path.join(eth_rtl_dir, "ip_complete_64.v"),
        os.path.join(eth_rtl_dir, "ip_64.v"),
        os.path.join(eth_rtl_dir, "ip_eth_rx_64.v"),
        os.path.join(eth_rtl_dir, "ip_eth_tx_64.v"),
        os.path.join(eth_rtl_dir, "ip_arb_mux.v"),
        os.path.join(eth_rtl_dir, "arp.v"),
        os.path.join(eth_rtl_dir, "arp_cache.v"),
        os.path.join(eth_rtl_dir, "arp_eth_rx.v"),
        os.path.join(eth_rtl_dir, "arp_eth_tx.v"),
        os.path.join(eth_rtl_dir, "eth_arb_mux.v"),
        os.path.join(axis_rtl_dir, "arbiter.v"),
        os.path.join(axis_rtl_dir, "priority_encoder.v"),
        os.path.join(axis_rtl_dir, "axis_fifo.v"),
        os.path.join(axis_rtl_dir, "axis_async_fifo.v"),
        os.path.join(axis_rtl_dir, "axis_async_fifo_adapter.v"),
    ]

    parameters = {}

    # parameters['A'] = val

    extra_env = {f'PARAM_{k}': str(v) for k, v in parameters.items()}

    sim_build = os.path.join(tests_dir, "sim_build",
        request.node.name.replace('[', '-').replace(']', ''))

    cocotb_test.simulator.run(
        python_search=[tests_dir],
        verilog_sources=verilog_sources,
        toplevel=toplevel,
        module=module,
        parameters=parameters,
        sim_build=sim_build,
        extra_env=extra_env,
    )
