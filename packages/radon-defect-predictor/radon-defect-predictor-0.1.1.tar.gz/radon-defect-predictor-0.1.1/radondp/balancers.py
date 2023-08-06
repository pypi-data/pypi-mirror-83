from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler

balancers_map = dict(
    none=None,
    rus=RandomUnderSampler(sampling_strategy='majority', random_state=42),
    ros=RandomOverSampler(sampling_strategy='minority', random_state=42)
)
