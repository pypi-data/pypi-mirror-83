Tutorial 1. Scheduler concepts
================================

.. jupyter-kernel::
  :id: Tutorial 1. Scheduler concepts

In this tutorial we explore how to program a basic experiment using the :mod:`quantify.scheduler`.
We will give an overview of the sequncer module and show different visualization backends as well as compilation onto a hardware backend.


Concepts
----------------

The :mod:`quantify.scheduler` can be used to schedule operations on the control hardware.
The :mod:`quantify.scheduler` is designed to provide access to hardware functionality at a high-level interface.

The :mod:`quantify.scheduler` is built around the :class:`~quantify.scheduler.Schedule`, a JSON-based data structure containing :attr:`~quantify.scheduler.Schedule.operations` , :attr:`~quantify.scheduler.Schedule.timing_constraints` , and :attr:`~quantify.scheduler.Schedule.resources` .
Take a look at the :class:`quantify.scheduler.Schedule` documentation for more details.

An :class:`~quantify.scheduler.Operation` contains information on how to *represent* the operation at different levels of abstraction, such as the quantum-circuit (gate) level or the pulse level.
The :mod:`quantify.scheduler` comes with a  :mod:`~quantify.scheduler.gate_library` and a :mod:`~quantify.scheduler.pulse_library` , both containing common operations.
When adding an :class:`~quantify.scheduler.Operation` to a :class:`~quantify.scheduler.Schedule`, the user is not expected to provide all information at once.
Only when specific information is required by a backend such as a simulator or a hardware backend does the information need to be provided.

A compilation step is a transformation of the :class:`~quantify.scheduler.Schedule` and results in a new :class:`~quantify.scheduler.Schedule`.
A compilation step can be used to e.g., add pulse information to operations containing only a gate-level representation or to determine the absolute timing based on timing constraints.
A final compilation step translates the :class:`~quantify.scheduler.Schedule` into a format compatible with the desired backend.

The following diagram provides an overview of how to interact with the :class:`~quantify.scheduler.Schedule` class.
The user can create a new schedule using the quantify API, or load a schedule based on one of the supported :mod:`~quantify.scheduler.frontends` for QASM-like formats such as qiskit QASM or OpenQL cQASM (todo).
One or multiple compilation steps modify the :class:`~quantify.scheduler.Schedule` until it contains the information required for the :mod:`~quantify.scheduler.backends.visualization` used for visualization, simulation or compilation onto the hardware or back into a common QASM-like format.

.. blockdiag::

    blockdiag scheduler {

      qf_input [label="quantify API"];
      ext_input [label="Q A S M-like\nformats", stacked];
      vis_bck [label="Visualization \nbackends", stacked];
      hw_bck [label="Hardware\nbackends", stacked];
      sim_bck [label="Simulator\nbackends", stacked];
      ext_fmts [label="Q A S M-like\n formats", stacked];

      qf_input, ext_input -> Schedule;
      Schedule -> Schedule [label="Compile"];
      Schedule -> vis_bck;
      Schedule -> hw_bck;
      Schedule -> sim_bck ;
      Schedule -> ext_fmts;

      group {
        label= "Input formats";
        qf_input
        ext_input
        color="#90EE90"
        }

      group {

        Schedule
        color=red
        label="Compilation"
        }

      group {
        label = "Backends";
        color = orange;
        vis_bck, hw_bck, sim_bck, ext_fmts
        }
    }

The benefit of allowing the user to mix the high-level gate description of a circuit with the lower-level pulse description can be understood through an example.
Below we first give an example of basic usage using `Bell violations`.
We next show the `Chevron` experiment in which the user is required to mix gate-type and pulse-type information when defining the :class:`~quantify.scheduler.Schedule`.

Ex: A basic quantum circuit:  the Bell experiment
-----------------------------------------------------------------------------------------

As the first example, we want to perform the `Bell experiment <https://en.wikipedia.org/wiki/Bell%27s_theorem>`_ .
In this example, we will go quite deep into the internals of the schedule to show how the data structures work.

The goal of the Bell experiment is to create a Bell state :math:`|\Phi ^+\rangle=\frac{1}{2}(|00\rangle+|11\rangle)` followed by a measurement and observe violations of the CSHS inequality.

By changing the basis in which one of the detectors measures, we can observe an oscillation which should result in a violation of Bell's inequality.
If everything is done properly, one should observe this oscillation:

.. figure:: https://upload.wikimedia.org/wikipedia/commons/e/e2/Bell.svg
  :figwidth: 50%

Bell circuit
~~~~~~~~~~~~~~~~
Below is the QASM code used to perform this experiment in `Quantum Inspire <https://www.quantum-inspire.com/>`_ as well as a circuit diagram representation.
We will be creating this same experiment using the quantify.scheduler.

.. code-block:: python

    version 1.0

    # Bell experiment

    qubits 2

    .init
    prep_z q[0:1]

    .Entangle
    X90 q[0]
    cz q[0],q[1]

    .Rotate
    # change the value to change the basis of the detector
    Rx q[0], 0.15

    .Measurement
    Measure_all

.. figure:: /images/bell_circuit_QI.png
  :figwidth: 50%

Creating a schedule
~~~~~~~~~~~~~~~~~~~~

We start by initializing an empty :class:`~quantify.scheduler.Schedule`

.. jupyter-execute::

  from quantify.scheduler import Schedule
  sched = Schedule('Bell experiment')
  sched

Under the hood, the :class:`~quantify.scheduler.Schedule` is based on a dictionary that can be serialized

.. jupyter-execute::

  sched.data

We also need to define the resources. For now these are just strings because I have not implemented them properly yet.

.. jupyter-execute::

  # define the resources
  # q0, q1 = Qubits(n=2) # assumes all to all connectivity
  q0, q1 = ('q0', 'q1') # we use strings because Resources have not been implemented yet

We will now add some operations to the schedule.
Because this experiment is most conveniently described on the gate level, we use operations defined in the :mod:`quantify.scheduler.gate_library` .

.. jupyter-execute::

    from quantify.scheduler.gate_library import Reset, Measure, CZ, Rxy, X90

    # Define the operations, these will be added to the circuit
    init_all = Reset(q0, q1)
    x90_q0 = Rxy(theta=90, phi=0, qubit=q0)
    cz = CZ(qC=q0, qT=q1)
    Rxy_theta = Rxy(theta=23, phi=0, qubit=q0) # will be not be used in the experiment loop.
    meass_all = Measure(q0, q1)

Similar to the schedule, :class:`~quantify.scheduler.Operation` objects are also based on dicts.

.. jupyter-execute::

    # Rxy_theta  # produces the same output
    Rxy_theta.data

Now we create the Bell experiment, including observing the oscillation in a simple for loop.

.. jupyter-execute::

    import numpy as np

    # we use a regular for loop as we have to unroll the changing theta variable here
    for theta in np.linspace(0, 360, 21):
        sched.add(init_all)
        sched.add(x90_q0)
        sched.add(operation=cz)
        sched.add(Rxy(theta=theta, phi=0, qubit=q0))
        sched.add(Measure(q0, q1), label='M {:.2f} deg'.format(theta))

Let's take a look at the internals of the :class:`~quantify.scheduler.Schedule`.

.. jupyter-execute::

    sched

We can see that the number of unique operations is 24 corresponding to 4 operations that occur in every loop and 21 unique rotations for the different theta angles. (21+4 = 25 so we are missing something.

.. jupyter-execute::

    sched.data.keys()

The schedule consists of a hash table containing all the operations.
This allows efficient loading of pulses or gates to memory and also enables efficient adding of pulse type information as a compilation step.

.. jupyter-execute::

    from itertools import islice
    # showing the first 5 elements of the operation dict
    dict(islice(sched.data['operation_dict'].items(), 5))

The timing constraints are stored as a list of pulses.

.. jupyter-execute::

  sched.data['timing_constraints'][:6]

Visualization using a circuit diagram
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

So far we have only defined timing constraints but the duration of pulses is not known.

For this purpose we do our first compilation step:

.. jupyter-execute::

  from quantify.scheduler.compilation import _determine_absolute_timing
  # We modify the schedule in place adding timing information
  # setting clock_unit='ideal' ignores the duration of operations and sets it to 1.
  _determine_absolute_timing(sched, clock_unit='ideal')

And we can use this to create a default visualizaton:

.. jupyter-execute::

  %matplotlib inline

  from quantify.scheduler.backends import visualization as viz
  f, ax = viz.circuit_diagram_matplotlib(sched)
  # all gates are plotted, but it doesn't all fit in a matplotlib figure
  ax.set_xlim(-.5, 9.5)

Compilation onto a Transmon backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Of course different Qubits are driven with different techniques which must be defined. Here we have a pair of Transmon qubits,
which respond to microwave pulses:

.. jupyter-execute::

    #  q0 ro_pulse_modulation_freq should be 80e6, requires issue38 resolution
    device_test_cfg = {
          "qubits":
          {
              "q0": {"mw_amp180": 0.5, "mw_motzoi": -0.25, "mw_duration": 20e-9,
                     "mw_modulation_freq": 50e6, "mw_ef_amp180": 0.87, "mw_ch": "qcm0.s0",
                     "ro_ch": "qrm0.s0", "ro_pulse_amp": 0.5, "ro_pulse_modulation_freq": 80e6,
                     "ro_pulse_type": "square", "ro_pulse_duration": 150e-9,
                     "ro_acq_delay": 120e-9, "ro_acq_integration_time": 700e-9,
                     "ro_acq_weigth_type": "SSB",
                     "init_duration": 250e-6
                     },
              "q1": {"mw_amp180": 0.45, "mw_motzoi": -0.15, "mw_duration": 20e-9,
                     "mw_modulation_freq": 80e6, "mw_ef_amp180": 0.27, "mw_ch": "qcm1.s0",
                     "ro_ch": "qrm0.s1", "ro_pulse_amp": 0.5, "ro_pulse_modulation_freq": -23e6,
                     "ro_pulse_type": "square", "ro_pulse_duration": 100e-9,
                     "ro_acq_delay": 120e-9, "ro_acq_integration_time": 700e-9,
                     "ro_acq_weigth_type": "SSB",
                     "init_duration": 250e-6 }
          },
          "edges":
          {
              "q0-q1": {
                  "flux_duration": 40e-9,
                  "flux_ch_control": "qcm0.s1", "flux_ch_target": "qcm1.s1",
                  "flux_amp_control": 0.5,  "flux_amp_target": 0,
                  "phase_correction_control": 0,
                  "phase_correction_target": 0}
          }
      }


With this information, the compiler can now generate the waveforms required.

Resources
----------

Our gates and timings are now defined but we still need to describe how the various devices in our experiments are connected; Quantify uses the :class:`quantify.scheduler.types.Resource` to represent this.
Of particular interest to us are the :class:`quantify.scheduler.resources.CompositeResource` and the :class:`quantify.scheduler.resources.Pulsar_QCM_sequencer`,
which represent a collection of Resources and a single Core on the Pulsar QCM:

.. jupyter-execute::

    from quantify.scheduler.resources import CompositeResource, Pulsar_QCM_sequencer, Pulsar_QRM_sequencer
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

With this information added, we can now compile the full program with an appropriate backend:

.. jupyter-execute::

  from quantify.scheduler.compilation import qcompile
  import quantify.scheduler.backends.pulsar_backend as pb
  sched, config_dict = qcompile(sched, device_test_cfg, backend=pb.pulsar_assembler_backend)

Let's take a look at what our finished configuration looks like:

.. jupyter-execute::

    config_dict

It contains a list of JSON files representing the configuration for each device. Now we are ready to deploy to hardware.

Visualization using a pulse diagram
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The compiler also provides pulse schedule visualization, which can be useful for a quick verification that your schedule is as expected:

.. jupyter-execute::

  from quantify.scheduler.backends.visualization import pulse_diagram_plotly
  fig = pulse_diagram_plotly(sched, ch_list=['qcm0.s0', 'qcm1.s0', 'qrm0.s0', 'qrm0.r0'])
  fig.show()

By default :func:`quantify.scheduler.backends.visualization.pulse_diagram_plotly` shows the first 8 channels encountered in in a schedule, but by specifying a list of channels, a more compact visualization can be created.

Connecting to Hardware
----------------------

The Pulsar QCM provides a QCodes based Python API. As well as interfacing with real hardware, it provides a mock driver we can use for testing and development, which we will
also use for demonstration purposes as part of this tutorial:

.. jupyter-execute::

    # todo install from pypi when released
    try:
        from pulsar_qcm.pulsar_qcm import pulsar_qcm_dummy
        from pulsar_qrm.pulsar_qrm import pulsar_qrm_dummy
        PULSAR_ASSEMBLER = True
    except ImportError:
        PULSAR_ASSEMBLER = False

The Pulsar QCM backend provides a method for deploying our complete configuration to all our devices at once:

.. jupyter-execute::
    :raises:

    if PULSAR_ASSEMBLER:
        _pulsars = []
        # first we need to create some Instruments representing the other devices in our configuration
        for qcm_name in ['qcm0', 'qcm1']:
            _pulsars.append(pulsar_qcm_dummy(qcm_name))
        for qrm_name in ['qrm0', 'qrm1']:
            _pulsars.append(pulsar_qrm_dummy(qrm_name))
        pb.configure_pulsar_sequencers(config_dict)

At this point, the assembler on the device will load the waveforms into memory and verify the program can be executed. We must next arm and then start the device:

.. jupyter-execute::
    :raises:

    if PULSAR_ASSEMBLER:
        qcm0 = _pulsars[0]
        qrm0 = _pulsars[2]

        qcm0.arm_sequencer()
        qrm0.arm_sequencer()
        qcm0.start_sequencer()
        qrm0.start_sequencer()

Provided we have synchronized our Pulsars properly using the sync-line, our experiment will now run. Once it's complete,
it is necessary to stop the QRMs before we read any data they have acquired. We first instruct the QRM to move it's
acquisition to disk memory with a named identifier and number of samples. We then request the QRM to return these
acquisitions over the driver so we can do some processing in Python:

.. jupyter-execute::
    :raises:

    if PULSAR_ASSEMBLER:
        seq_idx = 0
        qrm0.stop_sequencer()
        qrm0.store_acquisition(seq_idx, "meas_0", 4800)
        acq = qrm0.get_acquisitions(seq_idx)

.. note::

  This is it for now! Let's discuss.

Ex: Mixing pulse and gate-level descriptions, the Chevron experiment
-----------------------------------------------------------------------------------------

In this example, we want to perform a Chevron experiment



.. seealso::

    The complete source code of this tutorial can be found in

    :jupyter-download:notebook:`Tutorial 1. Scheduler concepts`

    :jupyter-download:script:`Tutorial 1. Scheduler concepts`
