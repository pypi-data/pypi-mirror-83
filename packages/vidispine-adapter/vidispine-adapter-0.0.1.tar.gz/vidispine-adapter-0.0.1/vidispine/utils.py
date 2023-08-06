import urllib


def generate_metadata(fields: dict) -> dict:
    metadata = {
        "timespan": [{
            "field": [{
                "name": key,
                "value": [{"value": value}]
            }
                for key, value in fields.items()
            ],
            "start": "-INF",
            "end": "+INF"
        }]
    }

    return metadata


def create_matrix_params_query(matrix_params: dict) -> str:
    if not matrix_params:
        return ''
    else:
        return ';' + ';'.join(
            f'{urlencode(key)}={urlencode(value)}'
            for key, value in matrix_params.items()
        )


def urlencode(value) -> str:
    return urllib.parse.quote(str(value))
