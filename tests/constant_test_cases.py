VALIDATION_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "id": 123,
            "name": "Телевизор",
            "package_params": {
                "width": 5,
                "height": 10
            },
            "location_and_quantity": [
                {
                    "location": "Магазин на Ленина",
                    "amount": 7
                },
                {
                    "location": "Магазин в центре",
                    "amount": 3
                }
            ]
        }
    ],
    "required": [
        "id",
        "name",
        "package_params",
        "location_and_quantity"
    ],
    "additionalProperties": False,
    "properties": {
        "id": {
            "$id": "#/properties/id",
            "type": "integer",
            "title": "The id schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                123
            ]
        },
        "name": {
            "$id": "#/properties/name",
            "type": "string",
            "title": "The name schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "Телевизор"
            ]
        },
        "package_params": {
            "$id": "#/properties/package_params",
            "type": "object",
            "title": "The package_params schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "examples": [
                {
                    "width": 5,
                    "height": 10
                }
            ],
            "required": [
                "width",
                "height"
            ],
            "additionalProperties": True,
            "properties": {
                "width": {
                    "$id": "#/properties/package_params/properties/width",
                    "type": "integer",
                    "title": "The width schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": 0,
                    "examples": [
                        5
                    ]
                },
                "height": {
                    "$id": "#/properties/package_params/properties/height",
                    "type": "integer",
                    "title": "The height schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": 0,
                    "examples": [
                        10
                    ]
                }
            }
        },
        "location_and_quantity": {
            "$id": "#/properties/location_and_quantity",
            "type": "array",
            "title": "The location_and_quantity schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "examples": [
                [
                    {
                        "location": "Магазин на Ленина",
                        "amount": 7
                    },
                    {
                        "location": "Магазин в центре",
                        "amount": 3
                    }
                ]
            ],
            "additionalItems": True,
            "items": {
                "anyOf": [
                    {
                        "$id": "#/properties/location_and_quantity/items/anyOf/0",
                        "type": "object",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "examples": [
                            {
                                "location": "Магазин на Ленина",
                                "amount": 7
                            }
                        ],
                        "required": [
                            "location",
                            "amount"
                        ],
                        "additionalProperties": True,
                        "properties": {
                            "location": {
                                "$id": "#/properties/location_and_quantity/items/anyOf/0/properties/location",
                                "type": "string",
                                "title": "The location schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "Магазин на Ленина"
                                ]
                            },
                            "amount": {
                                "$id": "#/properties/location_and_quantity/items/anyOf/0/properties/amount",
                                "type": "integer",
                                "title": "The amount schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": 0,
                                "examples": [
                                    7
                                ]
                            }
                        }
                    }
                ],
                "$id": "#/properties/location_and_quantity/items"
            }
        }
    }
}

VALID_TEST_CASES = [
    {
        "id": 1,
        "name": "Холодильник",
        "package_params": {
            "width": 120,
            "height": 270
        },
        "location_and_quantity": [
            {
                "location": "Магазин на Ленина",
                "amount": 3
            },
            {
                "location": "Магазин в центре",
                "amount": 4
            }
        ]
    },
    {
        "id": 2,
        "name": "Пылесос",
        "package_params": {
            "width": 25,
            "height": 35
        },
        "location_and_quantity": [
            {
                "location": "Магазин на Ленина",
                "amount": 13
            },
            {
                "location": "Магазин в центре",
                "amount": 0
            }
        ]
    }
]

INVALID_TEST_CASES = [
    {
        "id": 1.4,
        "name": "Холодильник",
        "package_params": {
            "width": 120,
            "height": 270
        },
        "location_and_quantity": [
            {
                "location": "Магазин на Ленина",
                "amount": 3
            },
            {
                "location": "Магазин в центре",
                "amount": 4
            }
        ]
    },
    {
        "id": 12,
        "name": 12,
        "package_params": {
            "width": 25,
            "height": 35
        },
        "location_and_quantity": [
            {
                "location": "Магазин на Ленина",
                "amount": 303
            },
            {
                "location": "Магазин в центре",
                "amount": 0
            }
        ]
    },
    {
        "id": 12,
        "name": ["Пылесос"],
        "package_params": {
            "width": 25,
            "height": 35
        },
        "location_and_quantity": [
            {
                "location": "Магазин на Ленина",
                "amount": 303
            },
            {
                "location": "Магазин в центре",
                "amount": 0
            }
        ]
    },
    {
        "id": 12,
        "name": "Пылесос",
        "package_params": {
            "width": "25",
            "height": 35
        },
        "location_and_quantity": [
            {
                "location": "Магазин на Ленина",
                "amount": 303
            },
            {
                "location": "Магазин в центре",
                "amount": 0
            }
        ]
    },
    {
        "id": 12,
        "name": "Пылесос",
        "package_params": {
            "width": 25
        },
        "location_and_quantity": [
            {
                "location": "Магазин на Ленина",
                "amount": 303
            },
            {
                "location": "Магазин в центре",
                "amount": 0
            }
        ]
    },
    {
        "id": 101,
        "name": "Пылесос",
        "package_params": {
            "width": 25,
            "height": 35
        },
        "location_and_amount": [
            {
                "location": "Магазин на Ленина",
                "amount": 303
            },
            {
                "location": "Магазин в центре",
                "amount": 0
            }
        ]
    },
    {
        "id": 101,
        "name": "Пылесос",
        "package_params": {
            "width": 25,
            "height": 35
        },
        "location_and_quantity": [
            {
                "location": "Магазин на Ленина",
                "amount": 0
            },
            {
                "location": "Магазин в центре",
                "amount": "5"
            }
        ]
    },
    {
        "id": 101,
        "name": "Пылесос",
        "package_params": {
            "width": 25,
            "height": 35
        },
        "location_and_quantity": [
            {
                "location": "Магазин на Ленина",
                "quantity": 2
            },
            {
                "location": "Магазин в центре",
                "amount": 5
            }
        ]
    },
    {
        "id": 101,
        "name": "Пылесос",
        "package_params": {
            "width": 25,
            "height": 35
        },
        "location_and_quantity": [
            {
                "location": "Магазин на Ленина",
                "quantity": 2
            },
            {
                "amount": 5
            }
        ]
    },
]