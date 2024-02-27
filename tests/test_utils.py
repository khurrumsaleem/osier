from osier.utils import *
from unyt import kW, MW, minute, hour
import numpy as np
import pytest


@pytest.fixture
def technology_set_1():
    """
    This fixture uses creates technologies directly from the :class:`Technology`
    class.
    """
    nuclear = Technology(technology_name='Nuclear',
                         technology_type='production',
                         capacity=5,
                         capital_cost=6,
                         om_cost_variable=20,
                         om_cost_fixed=50,
                         fuel_cost=5
                         )
    natural_gas = Technology(technology_name='NaturalGas',
                             technology_type='production',
                             capacity=5,
                             capital_cost=1,
                             om_cost_variable=12,
                             om_cost_fixed=30,
                             fuel_cost=20
                             )

    return [nuclear, natural_gas]


def test_synchronize_units(technology_set_1):
    """
    Tests that the synchronize units function makes all of the units in a list
    of technologies the same.
    """
    u_p = kW
    u_t = minute
    u_e = u_p * u_t

    synced = synchronize_units(technology_set_1, unit_power=u_p, unit_time=u_t)
    assert synced == technology_set_1
    assert [t.unit_power for t in synced] == [u_p, u_p]
    assert [t.unit_time for t in synced] == [u_t, u_t]
    assert [t.unit_energy for t in synced] == [u_e, u_e]
    
    
def test_apply_slack():
    """
    Tests that the function to apply slack values works as expected for a single
    objective, multiple objectives, and raises exceptions..
    """
    
    slack_values = np.array([0.1, 0.05, 0.2, 0.01])
    n_objectives = len(slack_values)
    pf1D = np.arange(20,0,-1)
    pf4D = np.array([pf1D for i in range(n_objectives)]).T
    
    for slack in slack_values:
        assert np.all(pf1D*(1+slack) == apply_slack(pf1D, slack, sense='minimize'))
    
    assert np.all(pf4D*(np.ones(n_objectives)+slack_values) == apply_slack(pf4D, slack_values))
 
    with pytest.raises(ValueError) as e:
        apply_slack(pf1D, slack_values)
    
    
