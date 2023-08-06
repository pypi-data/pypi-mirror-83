Refractoriness
==============

.. contents::
    :local:
    :depth: 1


Brian allows you to model the absolute refractory period of a neuron in a flexible
way. The definition of refractoriness consists of two components: the amount of time
after a spike that a neuron is considered to be refractory, and what changes in the
neuron during the refractoriness.

Defining the refractory period
------------------------------

The refractory period is specified by the ``refractory`` keyword in the
`NeuronGroup` initializer. In the simplest case, this is simply a fixed time,
valid for all neurons::

    G = NeuronGroup(N, model='...', threshold='...', reset='...',
                    refractory=2*ms)

Alternatively, it can be a string expression that evaluates to a time. This
expression will be evaluated after every spike and allows for a changing
refractory period. For example, the following will set the refractory period
to a random duration between 1ms and 3ms after every spike::

    G = NeuronGroup(N, model='...', threshold='...', reset='...',
                    refractory='(1 + 2*rand())*ms')

In general, modelling a refractory period that varies across neurons involves
declaring a state variable that stores the refractory period per neuron as a
model parameter. The refractory expression can then refer to this parameter::

    G = NeuronGroup(N, model='''...
                                refractory : second''', threshold='...',
                    reset='...', refractory='refractory')
    # Set the refractory period for each cell
    G.refractory = ...

This state variable can also be a dynamic variable itself. For example, it can
serve as an adaptation mechanism by increasing it after every spike and letting
it relax back to a steady-state value between spikes::

    refractory_0 = 2*ms
    tau_refractory = 50*ms
    G = NeuronGroup(N, model='''...
                                drefractory/dt = (refractory_0 - refractory) / tau_refractory : second''',
                    threshold='...', refractory='refractory',
                    reset='''...
                             refractory += 1*ms''')
    G.refractory = refractory_0

In some cases, the condition for leaving the refractory period is not easily
expressed as a certain time span. For example, in a Hodgkin-Huxley type model the
threshold is only used for *counting* spikes and the refractoriness is used to
prevent to count multiple spikes for a single threshold crossing (the threshold
condition would evaluate to ``True`` for several time points). When a neuron
should leave the refractory period is not easily expressed as a time span but
more naturally as a condition that the neuron should remain refractory for as
long as it stays above the threshold. This can be achieved by using a string
expression for the ``refractory`` keyword that evaluates to a boolean condition::

    G = NeuronGroup(N, model='...', threshold='v > -20*mV',
                    refractory='v >= -20*mV')

The ``refractory`` keyword should be read as "stay refractory as long as the
condition remains true". In fact, specifying a time span for the refractoriness
will be automatically transformed into a logical expression using the current
time ``t`` and the time of the last spike ``lastspike``. Specifying
``refractory=2*ms`` is basically equivalent to specifying
``refractory='(t - lastspike) <= 2*ms'``. However, this expression can give
inconsistent results for the common case that the refractory period is a
multiple of the simulation timestep. Due to floating point impreciseness, the
actual value of ``t - lastspike`` can be slightly above or below a multiple of
the simulation time step; comparing it directly to the refractory period can
therefore lead to an end of the refractory one time step sooner or later. To
avoid this issue, the actual code used for the above example is equivalent to
``refractory='timestep(t - lastspike, dt) <= timestep(2*ms, dt)'``. The
`~brian2.core.functions.timestep` function is provided by Brian and takes care of
converting a time into a time step in a safe way.

.. versionadded:: 2.1.3
    The `timestep` function is now used to avoid floating point issues in the
    refractoriness calculation. To restore the previous behaviour, set the
    `legacy.refractory_timing` preference to ``True``.

Defining model behaviour during refractoriness
----------------------------------------------

The refractoriness definition as described above only has a single
effect by itself: threshold crossings during the refractory period are ignored.
In the following model, the variable ``v`` continues to update during the
refractory period but it does not elicit a spike if it crosses the threshold::

    G = NeuronGroup(N, 'dv/dt = -v / tau : 1',
                    threshold='v > 1', reset='v=0',
                    refractory=2*ms)

There is also a second implementation of refractoriness that is
supported by Brian, one or several state variables can be clamped during the
refractory period. To model this kind of behaviour, variables that should
stop being updated during refractoriness can be marked with the
``(unless refractory)`` flag::

    G = NeuronGroup(N, '''dv/dt = -(v + w)/ tau_v : 1 (unless refractory)
                          dw/dt = -w / tau_w : 1''',
                    threshold='v > 1', reset='v=0; w+=0.1', refractory=2*ms)

In the above model, the ``v`` variable is clamped at 0 for 2ms after a spike but
the adaptation variable ``w`` continues to update during this time. In
addition, a variable of a neuron that is in its refractory period is
*read-only*: incoming synapses or other code will have no effect on the
value of ``v`` until it leaves its refractory period.

.. admonition:: The following topics are not essential for beginners.

    |


Arbitrary refractoriness
------------------------

In fact, arbitrary behaviours can be defined using Brian's refractoriness
mechanism.

A `NeuronGroup` with refractoriness automatically defines two variables:

``not_refractory``
    A boolean variable stating whether a neuron is allowed to spike.

``lastspike``
    The time of the last spike of the neuron.

The variable ``not_refractory`` is updated at every time step by checking the
refractoriness condition -- for a refractoriness defined by a time period, this
means comparing ``lastspike`` to the current time ``t``. The ``not_refractory``
variable is then used to implement
the refractoriness behaviour. Specifically, the ``threshold`` condition
is replaced by ``threshold and not_refractory`` and differential equations
that are marked as ``(unless refractory)`` are multiplied by
``int(not_refractory)`` (so that they have the value 0 when the neuron is
refractory).

This ``not_refractory`` variable is also available to the user
to define more sophisticated refractoriness behaviour.
For example, the following code updates the
``w`` variable with a different time constant during refractoriness::

    G = NeuronGroup(N, '''dv/dt = -(v + w)/ tau_v : 1 (unless refractory)
                          dw/dt = (-w / tau_active)*int(not_refractory) + (-w / tau_ref)*(1 - int(not_refractory)) : 1''',
                    threshold='v > 1', reset='v=0; w+=0.1', refractory=2*ms)
