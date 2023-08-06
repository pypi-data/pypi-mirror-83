from sklearn.preprocessing import MinMaxScaler, StandardScaler

normalizers_map = dict(
    none=None,
    minmax=MinMaxScaler(),
    std=StandardScaler()
)
