import json
import pytest
from quantify.data.handling import set_datadir, get_datadir
import numpy as np
from qcodes.instrument.base import Instrument
from qcodes.utils.helpers import NumpyJSONEncoder
from quantify.scheduler.types import Schedule
from quantify.scheduler.gate_library import Reset, Measure, CZ, Rxy, X, X90
from quantify.scheduler.pulse_library import SquarePulse
from quantify.scheduler.backends.pulsar_backend import build_waveform_dict, build_q1asm, generate_sequencer_cfg, \
    pulsar_assembler_backend, _check_driver_version, QCM_DRIVER_VER, QRM_DRIVER_VER
from quantify.scheduler.resources import CompositeResource, Pulsar_QCM_sequencer, Pulsar_QRM_sequencer
from quantify.scheduler.compilation import qcompile


try:
    from pulsar_qcm.pulsar_qcm import pulsar_qcm_dummy
    from pulsar_qrm.pulsar_qrm import pulsar_qrm_dummy
    PULSAR_ASSEMBLER = True
except ImportError:
    PULSAR_ASSEMBLER = False


import pathlib
cfg_f = pathlib.Path(__file__).parent.parent.parent.absolute() / 'test_data' / 'transmon_test_config.json'
with open(cfg_f, 'r') as f:
    DEVICE_TEST_CFG = json.load(f)


def test_build_waveform_dict():
    real = np.random.random(int(4e3))
    complex_vals = real + (np.random.random(int(4e3)) * 1.0j)

    pulse_data = {
        'gdfshdg45': complex_vals,
        '6h5hh5hyj': real,
    }
    sequence_cfg = build_waveform_dict(pulse_data, acquisitions={'6h5hh5hyj'})
    assert len(sequence_cfg['waveforms']['awg']) == 2
    assert len(sequence_cfg['waveforms']['acq']) == 2
    wf_1 = sequence_cfg['waveforms']['awg']['gdfshdg45_I']
    wf_2 = sequence_cfg['waveforms']['awg']['gdfshdg45_Q']
    wf_3 = sequence_cfg['waveforms']['acq']['6h5hh5hyj_I']
    wf_4 = sequence_cfg['waveforms']['acq']['6h5hh5hyj_Q']
    np.testing.assert_array_equal(wf_1['data'], complex_vals.real)
    assert wf_1['index'] == 0
    np.testing.assert_array_equal(wf_2['data'], complex_vals.imag)
    assert wf_2['index'] == 1
    np.testing.assert_array_equal(wf_3['data'], real)
    assert wf_3['index'] == 0
    np.testing.assert_array_equal(wf_4['data'], np.zeros(len(wf_4['data'])))
    assert wf_4['index'] == 1


def test_bad_pulse_timings():
    short_pulse_timings = [
        (0, 'drag_ID', None),
        (4, 'square_id', None)
    ]
    short_wait_timings = [
        (0, 'square_id', None),
        (6, 'square_id', None)
    ]
    short_final_wait = [
        (0, 'square_id', None),
        (4, 'square_id', None)
    ]

    dummy_pulse_data = {
        'awg': {
            'square_id_I': {'data': np.ones(4), 'index': 0},
            'square_id_Q': {'data': np.zeros(4), 'index': 1},
            'drag_ID_I': {'data': np.ones(2), 'index': 2},
            'drag_ID_Q': {'data': np.ones(2), 'index': 3}
        }
    }

    with pytest.raises(ValueError, match="Generated wait for '0':'drag_ID' caused exception 'duration 2ns < "
                                         "cycle time 4ns'"):
        build_q1asm(short_pulse_timings, dummy_pulse_data, short_pulse_timings[-1][0] + 4, set())

    with pytest.raises(ValueError, match="Generated wait for '0':'square_id' caused exception 'duration 2ns < "
                                         "cycle time 4ns'"):
        build_q1asm(short_wait_timings, dummy_pulse_data, 10, set())

    with pytest.raises(ValueError, match="Generated wait for '4':'square_id' caused exception 'duration 2ns < "
                                         "cycle time 4ns'"):
        build_q1asm(short_final_wait, dummy_pulse_data, 10, set())


def test_overflowing_instruction_times():
    real = np.random.random(129380)
    pulse_timings = [
        (0, 'square_ID', None)
    ]
    pulse_data = {
        'awg': {
            'square_ID_I': {'data': real, 'index': 0},
            'square_ID_Q': {'data': np.zeros(len(real)), 'index': 1}
        }
    }
    program_str = build_q1asm(pulse_timings, pulse_data, len(real), set())
    with open(pathlib.Path(__file__).parent.joinpath('ref_test_large_plays_q1asm'), 'rb') as f:
        assert program_str.encode('utf-8') == f.read()

    pulse_timings.append((229380 + pow(2, 16), 'square_ID', None))
    program_str = build_q1asm(pulse_timings, pulse_data, 524296, set())
    with open(pathlib.Path(__file__).parent.joinpath('ref_test_large_waits_q1asm'), 'rb') as f:
        assert program_str.encode('utf-8') == f.read()


def test_build_q1asm():
    real = np.random.random(4)
    complex_vals = real + (np.random.random(4) * 1.0j)

    pulse_timings = [
        (0, 'square_id', None),
        (4, 'drag_ID', None),
        (16, 'square_id', None)
    ]

    pulse_data = {
        'awg': {
            'square_id_I': {'data': real, 'index': 0},
            'square_id_Q': {'data': np.zeros(len(real)), 'index': 1},
            'drag_ID_I': {'data': complex_vals.real, 'index': 2},
            'drag_ID_Q': {'data': complex_vals.imag, 'index': 3}
        }
    }

    program_str = build_q1asm(pulse_timings, pulse_data, 20, set())
    with open(pathlib.Path(__file__).parent.joinpath('ref_test_build_q1asm'), 'rb') as f:
        assert program_str.encode('utf-8') == f.read()

    program_str_sync = build_q1asm(pulse_timings, pulse_data, 30, set())
    with open(pathlib.Path(__file__).parent.joinpath('ref_test_build_q1asm_sync'), 'rb') as f:
        assert program_str_sync.encode('utf-8') == f.read()

    err = r"Provided sequence_duration.*4.*less than the total runtime of this sequence.*20"
    with pytest.raises(ValueError, match=err):
        build_q1asm(pulse_timings, pulse_data, 4, set())

    # sequence_duration greater than final timing but less than total runtime
    err = r"Provided sequence_duration.*18.*less than the total runtime of this sequence.*20"
    with pytest.raises(ValueError, match=err):
        build_q1asm(pulse_timings, pulse_data, 18, set())


def test_generate_sequencer_cfg():
    pulse_timings = [
        (0, 'square_1', None),
        (4, 'drag_1', None),
        (16, 'square_2', None),
    ]

    real = np.random.random(4)
    complex_vals = real + (np.random.random(4) * 1.0j)
    pulse_data = {
        "square_1": [0.0, 1.0, 0.0, 0.0],
        "drag_1": complex_vals,
        "square_2": real,
    }

    def check_waveform(entry, exp_data, exp_idx):
        assert exp_idx == entry['index']
        np.testing.assert_array_equal(exp_data, entry['data'])

    sequence_cfg = generate_sequencer_cfg(pulse_data, pulse_timings, 20, set())
    check_waveform(sequence_cfg['waveforms']["awg"]["square_1_I"], [0.0, 1.0, 0.0, 0.0], 0)
    check_waveform(sequence_cfg['waveforms']["awg"]["square_1_Q"], np.zeros(4), 1)
    check_waveform(sequence_cfg['waveforms']["awg"]["drag_1_I"], complex_vals.real, 2)
    check_waveform(sequence_cfg['waveforms']["awg"]["drag_1_Q"], complex_vals.imag, 3)
    check_waveform(sequence_cfg['waveforms']["awg"]["square_2_I"], real, 4)
    check_waveform(sequence_cfg['waveforms']["awg"]["square_2_Q"], np.zeros(4), 5)
    assert len(sequence_cfg['program'])

    if PULSAR_ASSEMBLER:
        with open('tmp.json', 'w') as f:
            f.write(json.dumps(sequence_cfg, cls=NumpyJSONEncoder))
        qcm = pulsar_qcm_dummy('test')
        qcm.sequencer0_waveforms_and_program('tmp.json')
        assert 'assembler finished successfully' in qcm.get_assembler_log()
        pathlib.Path('tmp.json').unlink()


@pytest.fixture
def dummy_pulsars():
    if PULSAR_ASSEMBLER:
        _pulsars = []
        for qcm in ['qcm0', 'qcm1']:
            _pulsars.append(pulsar_qcm_dummy(qcm))
        for qrm in ['qrm0', 'qrm1']:
            _pulsars.append(pulsar_qrm_dummy(qrm))
    else:
        _pulsars = []

    # ensures the default datadir is used which is excluded from git
    set_datadir(None)
    yield _pulsars

    # teardown
    for instr_name in list(Instrument._all_instruments):
        try:
            inst = Instrument.find_instrument(instr_name)
            inst.close()
        except KeyError:
            pass


def test_pulsar_assembler_backend(dummy_pulsars):
    """
    This test uses a full example of compilation for a simple Bell experiment.
    This test can be made simpler the more we clean up the code.
    """
    # Create an empty schedule
    sched = Schedule('Bell experiment')

    # define the resources
    q0, q1 = ('q0', 'q1')

    # Define the operations, these will be added to the circuit
    init_all = Reset(q0, q1)  # instantiates
    x90_q0 = Rxy(theta=90, phi=0, qubit=q0)

    # we use a regular for loop as we have to unroll the changing theta variable here
    for theta in np.linspace(0, 360, 21):
        sched.add(init_all)
        sched.add(x90_q0)
        sched.add(operation=CZ(qC=q0, qT="q1"))
        sched.add(Rxy(theta=theta, phi=0, qubit="q0"))
        sched.add(Rxy(theta=90, phi=0, qubit=q1))
        sched.add(Measure(q0, "q1"), label='M {:.2f} deg'.format(theta))

    # Add the resources for the pulsar qcm channels
    qcm0 = CompositeResource('qcm0', ['qcm0.s0', 'qcm0.s1'])
    qcm0_s0 = Pulsar_QCM_sequencer('qcm0.s0', instrument_name='qcm0', seq_idx=0)
    qcm0_s1 = Pulsar_QCM_sequencer('qcm0.s1', instrument_name='qcm0', seq_idx=1)

    qcm1 = CompositeResource('qcm1', ['qcm1.s0', 'qcm1.s1'])
    qcm1_s0 = Pulsar_QCM_sequencer('qcm1.s0', instrument_name='qcm1', seq_idx=0)
    qcm1_s1 = Pulsar_QCM_sequencer('qcm1.s1', instrument_name='qcm1', seq_idx=1)

    qrm0 = CompositeResource('qrm0', ['qrm0.s0', 'qrm0.s1'])
    # Currently mocking a readout module using an acquisition module
    qrm0_s0 = Pulsar_QRM_sequencer('qrm0.s0', instrument_name='qrm0', seq_idx=0)
    qrm0_s1 = Pulsar_QRM_sequencer('qrm0.s1', instrument_name='qrm0', seq_idx=1)

    sched.add_resources([qcm0, qcm0_s0, qcm0_s1, qcm1, qcm1_s0, qcm1_s1, qrm0, qrm0_s0, qrm0_s1])

    sched, cfgs = qcompile(sched, DEVICE_TEST_CFG, backend=pulsar_assembler_backend, configure_hardware=PULSAR_ASSEMBLER)

    assert len(sched.resources['qcm0.s0'].timing_tuples) == int(21*2)
    assert len(sched.resources['qcm0.s1'].timing_tuples) == int(21*1)
    assert len(qcm0_s0.timing_tuples) == int(21*2)
    assert len(qcm0_s1.timing_tuples) == 21
    assert len(qcm1_s0.timing_tuples) == 21
    assert len(qcm1_s1.timing_tuples) == 0

    assert sched.resources['qcm0.s0']['nco_freq'] == DEVICE_TEST_CFG["qubits"]["q0"]["mw_modulation_freq"]
    assert sched.resources['qrm0.s0']['nco_freq'] == DEVICE_TEST_CFG["qubits"]["q0"]["ro_pulse_modulation_freq"]
    assert sched.resources['qcm1.s0']['nco_freq'] == DEVICE_TEST_CFG["qubits"]["q1"]["mw_modulation_freq"]
    assert sched.resources['qrm0.s1']['nco_freq'] == DEVICE_TEST_CFG["qubits"]["q1"]["ro_pulse_modulation_freq"]

    if PULSAR_ASSEMBLER:
        assert dummy_pulsars[0].get('sequencer0_mod_en_awg')


def test_mismatched_mod_freq():
    bad_config = {
        "qubits": {
            "q0": {"mw_amp180": 0.75, "mw_motzoi": -0.25, "mw_duration": 20e-9, "mw_modulation_freq": 50e6,
                   "mw_ef_amp180": 0.87, "mw_ch": "qcm0.s0"},
            "q1": {"mw_amp180": 0.75, "mw_motzoi": -0.25, "mw_duration": 20e-9, "mw_modulation_freq": 70e6,
                   "mw_ef_amp180": 0.87, "mw_ch": "qcm0.s0"}
        },
        "edges": {
            "q0-q1": {}
        }
    }
    sched = Schedule('Mismatched mod freq')
    q0, q1 = ('q0', 'q1')
    sched.add(Rxy(theta=90, phi=0, qubit=q0))
    sched.add(Rxy(theta=90, phi=0, qubit=q1))
    qcm0_s0 = Pulsar_QCM_sequencer('qcm0.s0', instrument_name='qcm0', seq_idx=0)
    sched.add_resource(qcm0_s0)
    with pytest.raises(ValueError, match=r'pulse.*\d+ on channel qcm0.s0 has an inconsistent modulation frequency: '
                                         r'expected 50000000 but was 70000000'):
        qcompile(sched, bad_config, backend=pulsar_assembler_backend)


def test_gate_and_pulse():
    sched = Schedule("Chevron Experiment")
    qcm0_s0 = Pulsar_QCM_sequencer('qcm0.s0', instrument_name='qcm0', seq_idx=0)

    sched.add(X('q0'))
    sched.add(SquarePulse(0.8, 20e-9, 'q0:mw_ch'))
    sched.add(Rxy(90, 90, 'q0'))
    sched.add(SquarePulse(0.4, 20e-9, 'q0:mw_ch'))

    sched.add_resources([qcm0_s0])
    sched, cfgs = qcompile(sched, DEVICE_TEST_CFG, backend=pulsar_assembler_backend)
    with open(cfgs["qcm0.s0"], 'rb') as cfg:
        prog = json.load(cfg)
        assert len(prog['waveforms']['awg']) == 4


@pytest.mark.skipif(not PULSAR_ASSEMBLER, reason="requires pulsar drivers available")
def test_bad_driver_vers():
    def subtest(device, version):
        _check_driver_version(device, version)
        # sad path
        device._build = {'version': 'l.o.l.'}
        error = "Backend requires Pulsar Dummy to have driver version {}, found l.o.l. installed.".format(version)
        with pytest.raises(ValueError, match=error):
            _check_driver_version(device, version)

    subtest(pulsar_qcm_dummy('qcm_bad_vers'), QCM_DRIVER_VER)
    subtest(pulsar_qrm_dummy('qrm_bad_vers'), QRM_DRIVER_VER)
