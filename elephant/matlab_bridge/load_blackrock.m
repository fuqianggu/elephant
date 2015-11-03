%Define python code to run
py_command=sprintf([
    'import sys\n' ...
    'sys.path.insert(0, "/home/denker/Projects/toolboxes/py/python-neo")\n'...
    'import neo\n' ...
    'nikos_session=neo.io.BlackrockIO("/home/denker/DatasetsCached/reachgrasp/DataNikos2/i140701-001")\n'...
    'nikos_blk=nikos_session.read_block(nsx=None,units=[],waveforms=False)\n'...
    'print nikos_blk.segments[0].spiketrains[0].times\n'...
    'print nikos_blk.segments[0].spiketrains[0].times.shape\n']);

%Run python code
py('eval',py_command);

%Get data from python
py_import('nikos_blk');

disp(nikos_blk.name)

plot(nikos_blk.spiketrains,zeros(length(nikos_blk.spiketrains),1),'x');