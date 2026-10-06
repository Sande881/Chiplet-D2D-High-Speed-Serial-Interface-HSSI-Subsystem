import m5
from m5.objects import *

# 1. System Setup
system = System()
system.clk_domain = SrcClockDomain(clock="2GHz", voltage_domain=VoltageDomain())
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# 2. Configure 2-Way O3CPU
system.cpu = DerivO3CPU()
system.cpu.fetchWidth = 2
system.cpu.decodeWidth = 2
system.cpu.renameWidth = 2
system.cpu.issueWidth = 2
system.cpu.wbWidth = 2
system.cpu.commitWidth = 2
system.cpu.squashWidth = 2

# 3. Minimal Memory System
system.membus = SystemXBar()
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

# RISC-V standard interrupt controller
system.cpu.createInterruptController()

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# 4. Workload Setup
binary = 'tests/test-progs/hello/bin/riscv/linux/hello'

process = Process()
process.executable = binary
process.cmd = [binary] 
system.cpu.workload = process
system.cpu.createThreads()

system.workload = SEWorkload.init_compatible(binary)

# 5. Initialization
root = Root(full_system=False, system=system)
m5.instantiate()

# 6. Periodic Stat Dumping for di/dt profiling (50 ns windows)
m5.stats.periodicStatDump(m5.ticks.fromSeconds(50e-9))

print("Starting RISC-V simulation for transient analysis...")
exit_event = m5.simulate()
print(f"Simulation ended @ tick {m5.curTick()} because {exit_event.getCause()}")
