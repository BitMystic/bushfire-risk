import cdsapi

c = cdsapi.Client()

c.retrieve(
    'sis-agrometeorological-indicators',
    {
        'format': 'zip',
        'variable': '2m_temperature',
        'statistic': '24_hour_maximum',
        'area': [
            -33, 150, -34,
            152,
        ],
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11',
        ],
        'year': '2023',
        'month': '09',
    },
    'data/download.zip')
