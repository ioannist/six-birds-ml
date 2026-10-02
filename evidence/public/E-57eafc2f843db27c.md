# r13 calibration

{
  "registration_sha256": "b0876ea3cc9fd03831e4406a6f33f8650b54df7cd2294e446308b2c034bc8411",
  "device": "cpu",
  "checks": {
    "B": true,
    "signatures": true,
    "sums": true,
    "probes": true,
    "movement": true,
    "futility": true,
    "diagnosis": true,
    "supplier_access": true
  },
  "elapsed_seconds": 146.01797534013167,
  "B": {
    "original": {
      "oracle": {
        "pass": true,
        "criteria": {
          "natural_KL": true,
          "unseen_KL": true,
          "witness": true,
          "law_TV": true,
          "rerender": true,
          "swaps": true
        },
        "natural_KL_bits": 0.0,
        "unseen_count": 42067,
        "law_maximum_TV": 0.0
      },
      "board_only": {
        "pass": false,
        "criteria": {
          "natural_KL": false,
          "unseen_KL": false,
          "witness": false,
          "law_TV": false,
          "rerender": true,
          "swaps": false
        },
        "natural_KL_bits": 0.013513916482317617,
        "unseen_count": 42067,
        "law_maximum_TV": 0.1875000149011612
      }
    },
    "equal": {
      "oracle": {
        "pass": true,
        "criteria": {
          "natural_KL": true,
          "unseen_KL": true,
          "witness": true,
          "law_TV": true,
          "rerender": true,
          "swaps": true
        },
        "natural_KL_bits": -8.599132204111091e-08,
        "unseen_count": 43949,
        "law_maximum_TV": 2.9802322387695312e-08
      },
      "board_only": {
        "pass": true,
        "criteria": {
          "natural_KL": true,
          "unseen_KL": true,
          "witness": true,
          "law_TV": true,
          "rerender": true,
          "swaps": true
        },
        "natural_KL_bits": -8.599132204111091e-08,
        "unseen_count": 43949,
        "law_maximum_TV": 2.9802322387695312e-08
      }
    }
  },
  "A": {
    "local_correct": 1555,
    "local_total": 1555,
    "board_correct": 24435,
    "board_total": 24435
  },
  "oracle_probe_minimum": 0.998046875,
  "signature_calibration": {
    "original": {
      "oracle_cutoff_band": [
        {
          "rendering": 0,
          "cutoff": {
            "boards": 930,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 0.0
          },
          "complement": {
            "boards": 23505,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 0.0
          }
        },
        {
          "rendering": 1,
          "cutoff": {
            "boards": 930,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 0.0
          },
          "complement": {
            "boards": 23505,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 0.0
          }
        },
        {
          "rendering": 2,
          "cutoff": {
            "boards": 930,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 0.0
          },
          "complement": {
            "boards": 23505,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 0.0
          }
        },
        {
          "rendering": 3,
          "cutoff": {
            "boards": 930,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 0.0
          },
          "complement": {
            "boards": 23505,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 0.0
          }
        }
      ],
      "oracle_saved_r9": {
        "count": 101,
        "maximum_TV": 0.0,
        "above_0_02_TV": 0,
        "categorical_misreads": 0,
        "rows": [
          {
            "board_id": 22816,
            "rendering_id": 1535,
            "records": [
              [
                0,
                5
              ],
              [
                3,
                3
              ],
              [
                0,
                1
              ],
              [
                0,
                0
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N1",
                "prefix_index": 111,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24251,
            "rendering_id": 2852,
            "records": [
              [
                0,
                2
              ],
              [
                0,
                5
              ],
              [
                0,
                3
              ],
              [
                0,
                0
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 3
              },
              {
                "seed": 1,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 3
              },
              {
                "seed": 2,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22616,
            "rendering_id": 4081,
            "records": [
              [
                0,
                1
              ],
              [
                2,
                4
              ],
              [
                0,
                4
              ],
              [
                0,
                0
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "neutral_N",
                "scenario": 31,
                "member": "N"
              },
              {
                "seed": 2,
                "case": "same_category_substitution",
                "scenario": 31,
                "member": "N"
              },
              {
                "seed": 2,
                "case": "upper_state_exchange_same_N",
                "scenario": 31,
                "member": "N"
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 10695,
            "rendering_id": 8656,
            "records": [
              [
                2,
                4
              ],
              [
                3,
                0
              ],
              [
                1,
                3
              ],
              [
                0,
                0
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "neutral_N",
                "scenario": 31,
                "member": "L"
              },
              {
                "seed": 2,
                "case": "same_category_substitution",
                "scenario": 31,
                "member": "L"
              },
              {
                "seed": 2,
                "case": "upper_state_exchange_same_N",
                "scenario": 31,
                "member": "L"
              }
            ],
            "exact_category": 0,
            "predicted_category": 0,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.5,
                0.25,
                0.25
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22588,
            "rendering_id": 27424,
            "records": [
              [
                0,
                4
              ],
              [
                2,
                2
              ],
              [
                0,
                0
              ],
              [
                0,
                1
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24326,
            "rendering_id": 30665,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                2
              ],
              [
                0,
                4
              ],
              [
                0,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N5",
                "prefix_index": 359,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": 2,
            "outputs_after_L_H": [
              [
                0.25,
                0.25,
                0.5
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22499,
            "rendering_id": 53192,
            "records": [
              [
                0,
                2
              ],
              [
                0,
                3
              ],
              [
                4,
                5
              ],
              [
                0,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 5
              },
              {
                "seed": 2,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22784,
            "rendering_id": 57629,
            "records": [
              [
                4,
                5
              ],
              [
                0,
                0
              ],
              [
                0,
                4
              ],
              [
                0,
                2
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 4
              },
              {
                "seed": 2,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22619,
            "rendering_id": 59296,
            "records": [
              [
                2,
                4
              ],
              [
                4,
                2
              ],
              [
                0,
                5
              ],
              [
                0,
                2
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22794,
            "rendering_id": 70320,
            "records": [
              [
                0,
                0
              ],
              [
                0,
                4
              ],
              [
                3,
                0
              ],
              [
                0,
                2
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23742,
            "rendering_id": 82354,
            "records": [
              [
                0,
                4
              ],
              [
                2,
                3
              ],
              [
                0,
                1
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N6",
                "prefix_index": 427,
                "round": 7
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24321,
            "rendering_id": 85627,
            "records": [
              [
                1,
                1
              ],
              [
                0,
                4
              ],
              [
                0,
                5
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 7
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24307,
            "rendering_id": 85649,
            "records": [
              [
                4,
                5
              ],
              [
                0,
                4
              ],
              [
                0,
                5
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 7
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24337,
            "rendering_id": 86165,
            "records": [
              [
                0,
                5
              ],
              [
                3,
                4
              ],
              [
                0,
                5
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "set_H",
                "scenario": 10,
                "member": "H"
              }
            ],
            "exact_category": 2,
            "predicted_category": 2,
            "outputs_after_L_H": [
              [
                0.25,
                0.25,
                0.5
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24257,
            "rendering_id": 86373,
            "records": [
              [
                0,
                3
              ],
              [
                4,
                5
              ],
              [
                0,
                5
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 7
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22926,
            "rendering_id": 96994,
            "records": [
              [
                0,
                4
              ],
              [
                3,
                5
              ],
              [
                2,
                5
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23003,
            "rendering_id": 99274,
            "records": [
              [
                0,
                4
              ],
              [
                1,
                3
              ],
              [
                3,
                2
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 5
              },
              {
                "seed": 1,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 5
              },
              {
                "seed": 2,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22967,
            "rendering_id": 101827,
            "records": [
              [
                1,
                1
              ],
              [
                0,
                4
              ],
              [
                3,
                5
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 2
              },
              {
                "seed": 2,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24301,
            "rendering_id": 108065,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                2
              ],
              [
                0,
                0
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 2
              },
              {
                "seed": 1,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 2
              },
              {
                "seed": 2,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23715,
            "rendering_id": 109003,
            "records": [
              [
                2,
                1
              ],
              [
                0,
                3
              ],
              [
                0,
                1
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N5",
                "prefix_index": 359,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22824,
            "rendering_id": 109822,
            "records": [
              [
                3,
                4
              ],
              [
                0,
                0
              ],
              [
                0,
                2
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N5",
                "prefix_index": 366,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24426,
            "rendering_id": 109924,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                4
              ],
              [
                0,
                2
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": 2,
            "outputs_after_L_H": [
              [
                0.25,
                0.25,
                0.5
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24305,
            "rendering_id": 110877,
            "records": [
              [
                4,
                3
              ],
              [
                0,
                5
              ],
              [
                0,
                3
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 2
              },
              {
                "seed": 1,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 2
              },
              {
                "seed": 2,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22942,
            "rendering_id": 110909,
            "records": [
              [
                4,
                5
              ],
              [
                1,
                0
              ],
              [
                0,
                3
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24361,
            "rendering_id": 111771,
            "records": [
              [
                3,
                3
              ],
              [
                0,
                5
              ],
              [
                0,
                4
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N1",
                "prefix_index": 111,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": 2,
            "outputs_after_L_H": [
              [
                0.25,
                0.25,
                0.5
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23614,
            "rendering_id": 111952,
            "records": [
              [
                3,
                4
              ],
              [
                1,
                5
              ],
              [
                0,
                4
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N5",
                "prefix_index": 359,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23617,
            "rendering_id": 112001,
            "records": [
              [
                1,
                5
              ],
              [
                2,
                1
              ],
              [
                0,
                4
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23605,
            "rendering_id": 112361,
            "records": [
              [
                1,
                5
              ],
              [
                4,
                1
              ],
              [
                0,
                4
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N6",
                "prefix_index": 392,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24352,
            "rendering_id": 112644,
            "records": [
              [
                4,
                0
              ],
              [
                0,
                4
              ],
              [
                0,
                5
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": 2,
            "outputs_after_L_H": [
              [
                0.25,
                0.25,
                0.5
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23665,
            "rendering_id": 113125,
            "records": [
              [
                4,
                1
              ],
              [
                3,
                2
              ],
              [
                0,
                5
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N6",
                "prefix_index": 427,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23760,
            "rendering_id": 113326,
            "records": [
              [
                2,
                4
              ],
              [
                4,
                3
              ],
              [
                0,
                5
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23829,
            "rendering_id": 115291,
            "records": [
              [
                0,
                1
              ],
              [
                0,
                3
              ],
              [
                1,
                2
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24300,
            "rendering_id": 117994,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                3
              ],
              [
                1,
                5
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 6
              },
              {
                "seed": 1,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 6
              },
              {
                "seed": 2,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 19361,
            "rendering_id": 118555,
            "records": [
              [
                4,
                1
              ],
              [
                3,
                3
              ],
              [
                1,
                5
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 1
              }
            ],
            "exact_category": 0,
            "predicted_category": 0,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.5,
                0.25,
                0.25
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23502,
            "rendering_id": 121637,
            "records": [
              [
                2,
                5
              ],
              [
                0,
                4
              ],
              [
                2,
                3
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23051,
            "rendering_id": 123633,
            "records": [
              [
                0,
                3
              ],
              [
                1,
                5
              ],
              [
                2,
                5
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 4
              },
              {
                "seed": 2,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23776,
            "rendering_id": 123845,
            "records": [
              [
                0,
                5
              ],
              [
                3,
                0
              ],
              [
                2,
                5
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N5",
                "prefix_index": 366,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23591,
            "rendering_id": 124504,
            "records": [
              [
                0,
                4
              ],
              [
                1,
                4
              ],
              [
                3,
                0
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 9
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22814,
            "rendering_id": 126119,
            "records": [
              [
                4,
                5
              ],
              [
                0,
                3
              ],
              [
                3,
                2
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "neutral_N",
                "scenario": 31,
                "member": "N_other"
              },
              {
                "seed": 2,
                "case": "same_category_substitution",
                "scenario": 31,
                "member": "N_other"
              },
              {
                "seed": 2,
                "case": "upper_state_exchange_same_N",
                "scenario": 31,
                "member": "N_other"
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23459,
            "rendering_id": 130635,
            "records": [
              [
                2,
                3
              ],
              [
                0,
                4
              ],
              [
                4,
                1
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "neutral_N",
                "scenario": 20,
                "member": "N_other"
              },
              {
                "seed": 0,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "N_other"
              },
              {
                "seed": 0,
                "case": "upper_state_exchange_same_N",
                "scenario": 20,
                "member": "N_other"
              },
              {
                "seed": 1,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "N_other"
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23640,
            "rendering_id": 132215,
            "records": [
              [
                0,
                5
              ],
              [
                4,
                3
              ],
              [
                4,
                2
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "set_H",
                "scenario": 10,
                "member": "N"
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22918,
            "rendering_id": 132407,
            "records": [
              [
                2,
                5
              ],
              [
                0,
                3
              ],
              [
                4,
                3
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 3
              },
              {
                "seed": 2,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23892,
            "rendering_id": 132461,
            "records": [
              [
                1,
                5
              ],
              [
                0,
                5
              ],
              [
                4,
                3
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23447,
            "rendering_id": 132724,
            "records": [
              [
                0,
                4
              ],
              [
                2,
                2
              ],
              [
                4,
                3
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N6",
                "prefix_index": 392,
                "round": 7
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22615,
            "rendering_id": 137233,
            "records": [
              [
                2,
                1
              ],
              [
                2,
                2
              ],
              [
                0,
                2
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "set_H",
                "scenario": 10,
                "member": "N_other"
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24267,
            "rendering_id": 137805,
            "records": [
              [
                2,
                3
              ],
              [
                0,
                3
              ],
              [
                0,
                3
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 8
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24414,
            "rendering_id": 139662,
            "records": [
              [
                2,
                0
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": 2,
            "outputs_after_L_H": [
              [
                0.25,
                0.25,
                0.5
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24408,
            "rendering_id": 139668,
            "records": [
              [
                3,
                0
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "neutral_N",
                "scenario": 31,
                "member": "H"
              },
              {
                "seed": 2,
                "case": "same_category_substitution",
                "scenario": 31,
                "member": "H"
              },
              {
                "seed": 2,
                "case": "upper_state_exchange_same_N",
                "scenario": 31,
                "member": "H"
              }
            ],
            "exact_category": 2,
            "predicted_category": 2,
            "outputs_after_L_H": [
              [
                0.25,
                0.25,
                0.5
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24407,
            "rendering_id": 139679,
            "records": [
              [
                4,
                5
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "neutral_N",
                "scenario": 20,
                "member": "H"
              },
              {
                "seed": 0,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "H"
              },
              {
                "seed": 0,
                "case": "upper_state_exchange_same_N",
                "scenario": 20,
                "member": "H"
              },
              {
                "seed": 1,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "H"
              }
            ],
            "exact_category": 2,
            "predicted_category": 2,
            "outputs_after_L_H": [
              [
                0.25,
                0.25,
                0.5
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24066,
            "rendering_id": 140207,
            "records": [
              [
                2,
                5
              ],
              [
                3,
                5
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23967,
            "rendering_id": 140302,
            "records": [
              [
                3,
                4
              ],
              [
                4,
                2
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 3
              },
              {
                "seed": 1,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 3
              },
              {
                "seed": 2,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23894,
            "rendering_id": 145774,
            "records": [
              [
                0,
                4
              ],
              [
                4,
                5
              ],
              [
                1,
                5
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N6",
                "prefix_index": 392,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23236,
            "rendering_id": 147696,
            "records": [
              [
                1,
                0
              ],
              [
                0,
                3
              ],
              [
                2,
                2
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 9
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24416,
            "rendering_id": 147755,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                2,
                2
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N5",
                "prefix_index": 366,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": 2,
            "outputs_after_L_H": [
              [
                0.25,
                0.25,
                0.5
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24042,
            "rendering_id": 149574,
            "records": [
              [
                4,
                0
              ],
              [
                0,
                5
              ],
              [
                2,
                4
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23248,
            "rendering_id": 152197,
            "records": [
              [
                1,
                1
              ],
              [
                0,
                3
              ],
              [
                3,
                1
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24385,
            "rendering_id": 153154,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                5
              ],
              [
                3,
                2
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 1
              },
              {
                "seed": 2,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": 2,
            "outputs_after_L_H": [
              [
                0.25,
                0.25,
                0.5
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23105,
            "rendering_id": 154017,
            "records": [
              [
                4,
                3
              ],
              [
                0,
                3
              ],
              [
                3,
                3
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N5",
                "prefix_index": 366,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22661,
            "rendering_id": 154082,
            "records": [
              [
                0,
                2
              ],
              [
                1,
                0
              ],
              [
                3,
                3
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N6",
                "prefix_index": 427,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23074,
            "rendering_id": 159418,
            "records": [
              [
                4,
                4
              ],
              [
                0,
                3
              ],
              [
                4,
                3
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N6",
                "prefix_index": 392,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23524,
            "rendering_id": 166114,
            "records": [
              [
                0,
                4
              ],
              [
                2,
                5
              ],
              [
                0,
                4
              ],
              [
                1,
                0
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N6",
                "prefix_index": 427,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22666,
            "rendering_id": 166922,
            "records": [
              [
                0,
                2
              ],
              [
                2,
                2
              ],
              [
                0,
                5
              ],
              [
                1,
                0
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23278,
            "rendering_id": 168395,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                3
              ],
              [
                1,
                1
              ],
              [
                1,
                0
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 2
              },
              {
                "seed": 2,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24098,
            "rendering_id": 194285,
            "records": [
              [
                0,
                5
              ],
              [
                4,
                2
              ],
              [
                0,
                5
              ],
              [
                1,
                1
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N5",
                "prefix_index": 366,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 3754,
            "rendering_id": 200186,
            "records": [
              [
                4,
                2
              ],
              [
                2,
                0
              ],
              [
                2,
                0
              ],
              [
                1,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 1
              },
              {
                "seed": 1,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 1
              },
              {
                "seed": 2,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 1
              }
            ],
            "exact_category": 0,
            "predicted_category": 0,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.5,
                0.25,
                0.25
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22980,
            "rendering_id": 220473,
            "records": [
              [
                0,
                3
              ],
              [
                4,
                5
              ],
              [
                0,
                4
              ],
              [
                1,
                2
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24397,
            "rendering_id": 220654,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                1,
                2
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 1
              },
              {
                "seed": 2,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": 2,
            "outputs_after_L_H": [
              [
                0.25,
                0.25,
                0.5
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23027,
            "rendering_id": 273702,
            "records": [
              [
                2,
                0
              ],
              [
                0,
                3
              ],
              [
                0,
                4
              ],
              [
                1,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23599,
            "rendering_id": 274024,
            "records": [
              [
                0,
                4
              ],
              [
                2,
                2
              ],
              [
                0,
                4
              ],
              [
                1,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N6",
                "prefix_index": 427,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24349,
            "rendering_id": 274653,
            "records": [
              [
                0,
                3
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                1,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N6",
                "prefix_index": 427,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": 2,
            "outputs_after_L_H": [
              [
                0.25,
                0.25,
                0.5
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23343,
            "rendering_id": 274803,
            "records": [
              [
                0,
                3
              ],
              [
                1,
                4
              ],
              [
                0,
                5
              ],
              [
                1,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N5",
                "prefix_index": 359,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23914,
            "rendering_id": 274834,
            "records": [
              [
                0,
                4
              ],
              [
                1,
                5
              ],
              [
                0,
                5
              ],
              [
                1,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N6",
                "prefix_index": 427,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23914,
            "rendering_id": 280054,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                5
              ],
              [
                1,
                5
              ],
              [
                1,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 6212,
            "rendering_id": 296872,
            "records": [
              [
                3,
                4
              ],
              [
                4,
                1
              ],
              [
                4,
                5
              ],
              [
                1,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 1
              },
              {
                "seed": 1,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 1
              },
              {
                "seed": 2,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 1
              }
            ],
            "exact_category": 0,
            "predicted_category": 0,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.5,
                0.25,
                0.25
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22563,
            "rendering_id": 326525,
            "records": [
              [
                0,
                5
              ],
              [
                4,
                0
              ],
              [
                0,
                2
              ],
              [
                2,
                0
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23428,
            "rendering_id": 328264,
            "records": [
              [
                0,
                4
              ],
              [
                3,
                4
              ],
              [
                0,
                4
              ],
              [
                2,
                0
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 8
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 11603,
            "rendering_id": 394257,
            "records": [
              [
                4,
                3
              ],
              [
                0,
                1
              ],
              [
                3,
                0
              ],
              [
                2,
                2
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 1
              }
            ],
            "exact_category": 0,
            "predicted_category": 0,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.5,
                0.25,
                0.25
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 24037,
            "rendering_id": 424055,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                3,
                3
              ],
              [
                2,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 7
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22726,
            "rendering_id": 433959,
            "records": [
              [
                1,
                3
              ],
              [
                0,
                5
              ],
              [
                0,
                2
              ],
              [
                2,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 7
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22621,
            "rendering_id": 436588,
            "records": [
              [
                4,
                4
              ],
              [
                0,
                2
              ],
              [
                0,
                5
              ],
              [
                2,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 8
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23192,
            "rendering_id": 458253,
            "records": [
              [
                0,
                3
              ],
              [
                0,
                5
              ],
              [
                4,
                5
              ],
              [
                2,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N6",
                "prefix_index": 392,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23771,
            "rendering_id": 462775,
            "records": [
              [
                4,
                1
              ],
              [
                0,
                5
              ],
              [
                0,
                4
              ],
              [
                2,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23490,
            "rendering_id": 485224,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                4
              ],
              [
                4,
                5
              ],
              [
                2,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 4
              },
              {
                "seed": 1,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 4
              },
              {
                "seed": 2,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23367,
            "rendering_id": 509524,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                4
              ],
              [
                4,
                2
              ],
              [
                3,
                0
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 8
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22881,
            "rendering_id": 515834,
            "records": [
              [
                2,
                2
              ],
              [
                0,
                4
              ],
              [
                0,
                3
              ],
              [
                3,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23943,
            "rendering_id": 517675,
            "records": [
              [
                4,
                1
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                3,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N5",
                "prefix_index": 359,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22803,
            "rendering_id": 535594,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                3
              ],
              [
                4,
                1
              ],
              [
                3,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 3
              },
              {
                "seed": 2,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23396,
            "rendering_id": 597745,
            "records": [
              [
                4,
                1
              ],
              [
                0,
                4
              ],
              [
                0,
                4
              ],
              [
                3,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 8
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 22546,
            "rendering_id": 621963,
            "records": [
              [
                0,
                3
              ],
              [
                0,
                2
              ],
              [
                0,
                1
              ],
              [
                3,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "neutral_N",
                "scenario": 20,
                "member": "N"
              },
              {
                "seed": 0,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "N"
              },
              {
                "seed": 0,
                "case": "upper_state_exchange_same_N",
                "scenario": 20,
                "member": "N"
              },
              {
                "seed": 1,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "N"
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 21979,
            "rendering_id": 625381,
            "records": [
              [
                0,
                1
              ],
              [
                4,
                2
              ],
              [
                0,
                4
              ],
              [
                3,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "set_H",
                "scenario": 10,
                "member": "L"
              }
            ],
            "exact_category": 0,
            "predicted_category": 0,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.5,
                0.25,
                0.25
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23691,
            "rendering_id": 625445,
            "records": [
              [
                0,
                5
              ],
              [
                4,
                4
              ],
              [
                0,
                4
              ],
              [
                3,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N5",
                "prefix_index": 359,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23233,
            "rendering_id": 626495,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                3
              ],
              [
                1,
                0
              ],
              [
                3,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23822,
            "rendering_id": 627425,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                4
              ],
              [
                1,
                1
              ],
              [
                3,
                5
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N5",
                "prefix_index": 366,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23300,
            "rendering_id": 657095,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                3
              ],
              [
                1,
                4
              ],
              [
                4,
                0
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 4
              },
              {
                "seed": 1,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 4
              },
              {
                "seed": 2,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23065,
            "rendering_id": 670595,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                3
              ],
              [
                4,
                1
              ],
              [
                4,
                0
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 18523,
            "rendering_id": 678801,
            "records": [
              [
                3,
                3
              ],
              [
                1,
                0
              ],
              [
                0,
                4
              ],
              [
                4,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "neutral_N",
                "scenario": 20,
                "member": "L"
              },
              {
                "seed": 0,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "L"
              },
              {
                "seed": 0,
                "case": "upper_state_exchange_same_N",
                "scenario": 20,
                "member": "L"
              },
              {
                "seed": 1,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "L"
              }
            ],
            "exact_category": 0,
            "predicted_category": 0,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.5,
                0.25,
                0.25
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23301,
            "rendering_id": 684095,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                3
              ],
              [
                1,
                4
              ],
              [
                4,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 7440,
            "rendering_id": 745546,
            "records": [
              [
                2,
                4
              ],
              [
                1,
                5
              ],
              [
                3,
                0
              ],
              [
                4,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N6",
                "prefix_index": 392,
                "round": 1
              }
            ],
            "exact_category": 0,
            "predicted_category": 0,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.5,
                0.25,
                0.25
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23383,
            "rendering_id": 760204,
            "records": [
              [
                0,
                4
              ],
              [
                3,
                2
              ],
              [
                0,
                4
              ],
              [
                4,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23677,
            "rendering_id": 786771,
            "records": [
              [
                3,
                3
              ],
              [
                0,
                5
              ],
              [
                0,
                4
              ],
              [
                4,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          },
          {
            "board_id": 23358,
            "rendering_id": 787384,
            "records": [
              [
                0,
                4
              ],
              [
                4,
                2
              ],
              [
                0,
                4
              ],
              [
                4,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N6",
                "prefix_index": 392,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": 1,
            "outputs_after_L_H": [
              [
                0.5,
                0.25,
                0.25
              ],
              [
                0.25,
                0.25,
                0.5
              ]
            ],
            "TV_after_L_H": [
              0.0,
              0.0
            ]
          }
        ]
      }
    },
    "equal": {
      "oracle_cutoff_band": [
        {
          "rendering": 0,
          "cutoff": {
            "boards": 930,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 2.9802322387695312e-08
          },
          "complement": {
            "boards": 23505,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 2.9802322387695312e-08
          }
        },
        {
          "rendering": 1,
          "cutoff": {
            "boards": 930,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 2.9802322387695312e-08
          },
          "complement": {
            "boards": 23505,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 2.9802322387695312e-08
          }
        },
        {
          "rendering": 2,
          "cutoff": {
            "boards": 930,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 2.9802322387695312e-08
          },
          "complement": {
            "boards": 23505,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 2.9802322387695312e-08
          }
        },
        {
          "rendering": 3,
          "cutoff": {
            "boards": 930,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 2.9802322387695312e-08
          },
          "complement": {
            "boards": 23505,
            "prediction_TV_errors": 0,
            "error_rate": 0.0,
            "maximum_TV": 2.9802322387695312e-08
          }
        }
      ],
      "oracle_saved_r9": {
        "count": 101,
        "maximum_TV": 2.9802322387695312e-08,
        "above_0_02_TV": 0,
        "categorical_misreads": null,
        "rows": [
          {
            "board_id": 22816,
            "rendering_id": 1535,
            "records": [
              [
                0,
                5
              ],
              [
                3,
                3
              ],
              [
                0,
                1
              ],
              [
                0,
                0
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N1",
                "prefix_index": 111,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24251,
            "rendering_id": 2852,
            "records": [
              [
                0,
                2
              ],
              [
                0,
                5
              ],
              [
                0,
                3
              ],
              [
                0,
                0
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 3
              },
              {
                "seed": 1,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 3
              },
              {
                "seed": 2,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22616,
            "rendering_id": 4081,
            "records": [
              [
                0,
                1
              ],
              [
                2,
                4
              ],
              [
                0,
                4
              ],
              [
                0,
                0
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "neutral_N",
                "scenario": 31,
                "member": "N"
              },
              {
                "seed": 2,
                "case": "same_category_substitution",
                "scenario": 31,
                "member": "N"
              },
              {
                "seed": 2,
                "case": "upper_state_exchange_same_N",
                "scenario": 31,
                "member": "N"
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 10695,
            "rendering_id": 8656,
            "records": [
              [
                2,
                4
              ],
              [
                3,
                0
              ],
              [
                1,
                3
              ],
              [
                0,
                0
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "neutral_N",
                "scenario": 31,
                "member": "L"
              },
              {
                "seed": 2,
                "case": "same_category_substitution",
                "scenario": 31,
                "member": "L"
              },
              {
                "seed": 2,
                "case": "upper_state_exchange_same_N",
                "scenario": 31,
                "member": "L"
              }
            ],
            "exact_category": 0,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22588,
            "rendering_id": 27424,
            "records": [
              [
                0,
                4
              ],
              [
                2,
                2
              ],
              [
                0,
                0
              ],
              [
                0,
                1
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24326,
            "rendering_id": 30665,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                2
              ],
              [
                0,
                4
              ],
              [
                0,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N5",
                "prefix_index": 359,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22499,
            "rendering_id": 53192,
            "records": [
              [
                0,
                2
              ],
              [
                0,
                3
              ],
              [
                4,
                5
              ],
              [
                0,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 5
              },
              {
                "seed": 2,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22784,
            "rendering_id": 57629,
            "records": [
              [
                4,
                5
              ],
              [
                0,
                0
              ],
              [
                0,
                4
              ],
              [
                0,
                2
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 4
              },
              {
                "seed": 2,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22619,
            "rendering_id": 59296,
            "records": [
              [
                2,
                4
              ],
              [
                4,
                2
              ],
              [
                0,
                5
              ],
              [
                0,
                2
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22794,
            "rendering_id": 70320,
            "records": [
              [
                0,
                0
              ],
              [
                0,
                4
              ],
              [
                3,
                0
              ],
              [
                0,
                2
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23742,
            "rendering_id": 82354,
            "records": [
              [
                0,
                4
              ],
              [
                2,
                3
              ],
              [
                0,
                1
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N6",
                "prefix_index": 427,
                "round": 7
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24321,
            "rendering_id": 85627,
            "records": [
              [
                1,
                1
              ],
              [
                0,
                4
              ],
              [
                0,
                5
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 7
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24307,
            "rendering_id": 85649,
            "records": [
              [
                4,
                5
              ],
              [
                0,
                4
              ],
              [
                0,
                5
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 7
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24337,
            "rendering_id": 86165,
            "records": [
              [
                0,
                5
              ],
              [
                3,
                4
              ],
              [
                0,
                5
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "set_H",
                "scenario": 10,
                "member": "H"
              }
            ],
            "exact_category": 2,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24257,
            "rendering_id": 86373,
            "records": [
              [
                0,
                3
              ],
              [
                4,
                5
              ],
              [
                0,
                5
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 7
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22926,
            "rendering_id": 96994,
            "records": [
              [
                0,
                4
              ],
              [
                3,
                5
              ],
              [
                2,
                5
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23003,
            "rendering_id": 99274,
            "records": [
              [
                0,
                4
              ],
              [
                1,
                3
              ],
              [
                3,
                2
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 5
              },
              {
                "seed": 1,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 5
              },
              {
                "seed": 2,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22967,
            "rendering_id": 101827,
            "records": [
              [
                1,
                1
              ],
              [
                0,
                4
              ],
              [
                3,
                5
              ],
              [
                0,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 2
              },
              {
                "seed": 2,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24301,
            "rendering_id": 108065,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                2
              ],
              [
                0,
                0
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 2
              },
              {
                "seed": 1,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 2
              },
              {
                "seed": 2,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23715,
            "rendering_id": 109003,
            "records": [
              [
                2,
                1
              ],
              [
                0,
                3
              ],
              [
                0,
                1
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N5",
                "prefix_index": 359,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22824,
            "rendering_id": 109822,
            "records": [
              [
                3,
                4
              ],
              [
                0,
                0
              ],
              [
                0,
                2
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N5",
                "prefix_index": 366,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24426,
            "rendering_id": 109924,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                4
              ],
              [
                0,
                2
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24305,
            "rendering_id": 110877,
            "records": [
              [
                4,
                3
              ],
              [
                0,
                5
              ],
              [
                0,
                3
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 2
              },
              {
                "seed": 1,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 2
              },
              {
                "seed": 2,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22942,
            "rendering_id": 110909,
            "records": [
              [
                4,
                5
              ],
              [
                1,
                0
              ],
              [
                0,
                3
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24361,
            "rendering_id": 111771,
            "records": [
              [
                3,
                3
              ],
              [
                0,
                5
              ],
              [
                0,
                4
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N1",
                "prefix_index": 111,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23614,
            "rendering_id": 111952,
            "records": [
              [
                3,
                4
              ],
              [
                1,
                5
              ],
              [
                0,
                4
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N5",
                "prefix_index": 359,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23617,
            "rendering_id": 112001,
            "records": [
              [
                1,
                5
              ],
              [
                2,
                1
              ],
              [
                0,
                4
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23605,
            "rendering_id": 112361,
            "records": [
              [
                1,
                5
              ],
              [
                4,
                1
              ],
              [
                0,
                4
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N6",
                "prefix_index": 392,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24352,
            "rendering_id": 112644,
            "records": [
              [
                4,
                0
              ],
              [
                0,
                4
              ],
              [
                0,
                5
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23665,
            "rendering_id": 113125,
            "records": [
              [
                4,
                1
              ],
              [
                3,
                2
              ],
              [
                0,
                5
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N6",
                "prefix_index": 427,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23760,
            "rendering_id": 113326,
            "records": [
              [
                2,
                4
              ],
              [
                4,
                3
              ],
              [
                0,
                5
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23829,
            "rendering_id": 115291,
            "records": [
              [
                0,
                1
              ],
              [
                0,
                3
              ],
              [
                1,
                2
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24300,
            "rendering_id": 117994,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                3
              ],
              [
                1,
                5
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 6
              },
              {
                "seed": 1,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 6
              },
              {
                "seed": 2,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 19361,
            "rendering_id": 118555,
            "records": [
              [
                4,
                1
              ],
              [
                3,
                3
              ],
              [
                1,
                5
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 1
              }
            ],
            "exact_category": 0,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23502,
            "rendering_id": 121637,
            "records": [
              [
                2,
                5
              ],
              [
                0,
                4
              ],
              [
                2,
                3
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23051,
            "rendering_id": 123633,
            "records": [
              [
                0,
                3
              ],
              [
                1,
                5
              ],
              [
                2,
                5
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 4
              },
              {
                "seed": 2,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23776,
            "rendering_id": 123845,
            "records": [
              [
                0,
                5
              ],
              [
                3,
                0
              ],
              [
                2,
                5
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N5",
                "prefix_index": 366,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23591,
            "rendering_id": 124504,
            "records": [
              [
                0,
                4
              ],
              [
                1,
                4
              ],
              [
                3,
                0
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 9
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22814,
            "rendering_id": 126119,
            "records": [
              [
                4,
                5
              ],
              [
                0,
                3
              ],
              [
                3,
                2
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "neutral_N",
                "scenario": 31,
                "member": "N_other"
              },
              {
                "seed": 2,
                "case": "same_category_substitution",
                "scenario": 31,
                "member": "N_other"
              },
              {
                "seed": 2,
                "case": "upper_state_exchange_same_N",
                "scenario": 31,
                "member": "N_other"
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23459,
            "rendering_id": 130635,
            "records": [
              [
                2,
                3
              ],
              [
                0,
                4
              ],
              [
                4,
                1
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "neutral_N",
                "scenario": 20,
                "member": "N_other"
              },
              {
                "seed": 0,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "N_other"
              },
              {
                "seed": 0,
                "case": "upper_state_exchange_same_N",
                "scenario": 20,
                "member": "N_other"
              },
              {
                "seed": 1,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "N_other"
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23640,
            "rendering_id": 132215,
            "records": [
              [
                0,
                5
              ],
              [
                4,
                3
              ],
              [
                4,
                2
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "set_H",
                "scenario": 10,
                "member": "N"
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22918,
            "rendering_id": 132407,
            "records": [
              [
                2,
                5
              ],
              [
                0,
                3
              ],
              [
                4,
                3
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 3
              },
              {
                "seed": 2,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23892,
            "rendering_id": 132461,
            "records": [
              [
                1,
                5
              ],
              [
                0,
                5
              ],
              [
                4,
                3
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23447,
            "rendering_id": 132724,
            "records": [
              [
                0,
                4
              ],
              [
                2,
                2
              ],
              [
                4,
                3
              ],
              [
                0,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N6",
                "prefix_index": 392,
                "round": 7
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22615,
            "rendering_id": 137233,
            "records": [
              [
                2,
                1
              ],
              [
                2,
                2
              ],
              [
                0,
                2
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "set_H",
                "scenario": 10,
                "member": "N_other"
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24267,
            "rendering_id": 137805,
            "records": [
              [
                2,
                3
              ],
              [
                0,
                3
              ],
              [
                0,
                3
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 8
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24414,
            "rendering_id": 139662,
            "records": [
              [
                2,
                0
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24408,
            "rendering_id": 139668,
            "records": [
              [
                3,
                0
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "neutral_N",
                "scenario": 31,
                "member": "H"
              },
              {
                "seed": 2,
                "case": "same_category_substitution",
                "scenario": 31,
                "member": "H"
              },
              {
                "seed": 2,
                "case": "upper_state_exchange_same_N",
                "scenario": 31,
                "member": "H"
              }
            ],
            "exact_category": 2,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24407,
            "rendering_id": 139679,
            "records": [
              [
                4,
                5
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "neutral_N",
                "scenario": 20,
                "member": "H"
              },
              {
                "seed": 0,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "H"
              },
              {
                "seed": 0,
                "case": "upper_state_exchange_same_N",
                "scenario": 20,
                "member": "H"
              },
              {
                "seed": 1,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "H"
              }
            ],
            "exact_category": 2,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24066,
            "rendering_id": 140207,
            "records": [
              [
                2,
                5
              ],
              [
                3,
                5
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23967,
            "rendering_id": 140302,
            "records": [
              [
                3,
                4
              ],
              [
                4,
                2
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 3
              },
              {
                "seed": 1,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 3
              },
              {
                "seed": 2,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23894,
            "rendering_id": 145774,
            "records": [
              [
                0,
                4
              ],
              [
                4,
                5
              ],
              [
                1,
                5
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N6",
                "prefix_index": 392,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23236,
            "rendering_id": 147696,
            "records": [
              [
                1,
                0
              ],
              [
                0,
                3
              ],
              [
                2,
                2
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 9
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24416,
            "rendering_id": 147755,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                2,
                2
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N5",
                "prefix_index": 366,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24042,
            "rendering_id": 149574,
            "records": [
              [
                4,
                0
              ],
              [
                0,
                5
              ],
              [
                2,
                4
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23248,
            "rendering_id": 152197,
            "records": [
              [
                1,
                1
              ],
              [
                0,
                3
              ],
              [
                3,
                1
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24385,
            "rendering_id": 153154,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                5
              ],
              [
                3,
                2
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 1
              },
              {
                "seed": 2,
                "case": "H_N3",
                "prefix_index": 251,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23105,
            "rendering_id": 154017,
            "records": [
              [
                4,
                3
              ],
              [
                0,
                3
              ],
              [
                3,
                3
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N5",
                "prefix_index": 366,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22661,
            "rendering_id": 154082,
            "records": [
              [
                0,
                2
              ],
              [
                1,
                0
              ],
              [
                3,
                3
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N6",
                "prefix_index": 427,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23074,
            "rendering_id": 159418,
            "records": [
              [
                4,
                4
              ],
              [
                0,
                3
              ],
              [
                4,
                3
              ],
              [
                0,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N6",
                "prefix_index": 392,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23524,
            "rendering_id": 166114,
            "records": [
              [
                0,
                4
              ],
              [
                2,
                5
              ],
              [
                0,
                4
              ],
              [
                1,
                0
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N6",
                "prefix_index": 427,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22666,
            "rendering_id": 166922,
            "records": [
              [
                0,
                2
              ],
              [
                2,
                2
              ],
              [
                0,
                5
              ],
              [
                1,
                0
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23278,
            "rendering_id": 168395,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                3
              ],
              [
                1,
                1
              ],
              [
                1,
                0
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 2
              },
              {
                "seed": 2,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24098,
            "rendering_id": 194285,
            "records": [
              [
                0,
                5
              ],
              [
                4,
                2
              ],
              [
                0,
                5
              ],
              [
                1,
                1
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N5",
                "prefix_index": 366,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 3754,
            "rendering_id": 200186,
            "records": [
              [
                4,
                2
              ],
              [
                2,
                0
              ],
              [
                2,
                0
              ],
              [
                1,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 1
              },
              {
                "seed": 1,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 1
              },
              {
                "seed": 2,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 1
              }
            ],
            "exact_category": 0,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22980,
            "rendering_id": 220473,
            "records": [
              [
                0,
                3
              ],
              [
                4,
                5
              ],
              [
                0,
                4
              ],
              [
                1,
                2
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24397,
            "rendering_id": 220654,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                1,
                2
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 1
              },
              {
                "seed": 2,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23027,
            "rendering_id": 273702,
            "records": [
              [
                2,
                0
              ],
              [
                0,
                3
              ],
              [
                0,
                4
              ],
              [
                1,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23599,
            "rendering_id": 274024,
            "records": [
              [
                0,
                4
              ],
              [
                2,
                2
              ],
              [
                0,
                4
              ],
              [
                1,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N6",
                "prefix_index": 427,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24349,
            "rendering_id": 274653,
            "records": [
              [
                0,
                3
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                1,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N6",
                "prefix_index": 427,
                "round": 1
              }
            ],
            "exact_category": 2,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23343,
            "rendering_id": 274803,
            "records": [
              [
                0,
                3
              ],
              [
                1,
                4
              ],
              [
                0,
                5
              ],
              [
                1,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N5",
                "prefix_index": 359,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23914,
            "rendering_id": 274834,
            "records": [
              [
                0,
                4
              ],
              [
                1,
                5
              ],
              [
                0,
                5
              ],
              [
                1,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N6",
                "prefix_index": 427,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23914,
            "rendering_id": 280054,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                5
              ],
              [
                1,
                5
              ],
              [
                1,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 6212,
            "rendering_id": 296872,
            "records": [
              [
                3,
                4
              ],
              [
                4,
                1
              ],
              [
                4,
                5
              ],
              [
                1,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 1
              },
              {
                "seed": 1,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 1
              },
              {
                "seed": 2,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 1
              }
            ],
            "exact_category": 0,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22563,
            "rendering_id": 326525,
            "records": [
              [
                0,
                5
              ],
              [
                4,
                0
              ],
              [
                0,
                2
              ],
              [
                2,
                0
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23428,
            "rendering_id": 328264,
            "records": [
              [
                0,
                4
              ],
              [
                3,
                4
              ],
              [
                0,
                4
              ],
              [
                2,
                0
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 8
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 11603,
            "rendering_id": 394257,
            "records": [
              [
                4,
                3
              ],
              [
                0,
                1
              ],
              [
                3,
                0
              ],
              [
                2,
                2
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 1
              }
            ],
            "exact_category": 0,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 24037,
            "rendering_id": 424055,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                3,
                3
              ],
              [
                2,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 7
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22726,
            "rendering_id": 433959,
            "records": [
              [
                1,
                3
              ],
              [
                0,
                5
              ],
              [
                0,
                2
              ],
              [
                2,
                4
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N7",
                "prefix_index": 499,
                "round": 7
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22621,
            "rendering_id": 436588,
            "records": [
              [
                4,
                4
              ],
              [
                0,
                2
              ],
              [
                0,
                5
              ],
              [
                2,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 8
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23192,
            "rendering_id": 458253,
            "records": [
              [
                0,
                3
              ],
              [
                0,
                5
              ],
              [
                4,
                5
              ],
              [
                2,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N6",
                "prefix_index": 392,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23771,
            "rendering_id": 462775,
            "records": [
              [
                4,
                1
              ],
              [
                0,
                5
              ],
              [
                0,
                4
              ],
              [
                2,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23490,
            "rendering_id": 485224,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                4
              ],
              [
                4,
                5
              ],
              [
                2,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 4
              },
              {
                "seed": 1,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 4
              },
              {
                "seed": 2,
                "case": "L_N5",
                "prefix_index": 348,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23367,
            "rendering_id": 509524,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                4
              ],
              [
                4,
                2
              ],
              [
                3,
                0
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N8",
                "prefix_index": 562,
                "round": 8
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22881,
            "rendering_id": 515834,
            "records": [
              [
                2,
                2
              ],
              [
                0,
                4
              ],
              [
                0,
                3
              ],
              [
                3,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23943,
            "rendering_id": 517675,
            "records": [
              [
                4,
                1
              ],
              [
                0,
                5
              ],
              [
                0,
                5
              ],
              [
                3,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N5",
                "prefix_index": 359,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22803,
            "rendering_id": 535594,
            "records": [
              [
                0,
                4
              ],
              [
                0,
                3
              ],
              [
                4,
                1
              ],
              [
                3,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 3
              },
              {
                "seed": 2,
                "case": "H_N4",
                "prefix_index": 313,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23396,
            "rendering_id": 597745,
            "records": [
              [
                4,
                1
              ],
              [
                0,
                4
              ],
              [
                0,
                4
              ],
              [
                3,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 8
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 22546,
            "rendering_id": 621963,
            "records": [
              [
                0,
                3
              ],
              [
                0,
                2
              ],
              [
                0,
                1
              ],
              [
                3,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "neutral_N",
                "scenario": 20,
                "member": "N"
              },
              {
                "seed": 0,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "N"
              },
              {
                "seed": 0,
                "case": "upper_state_exchange_same_N",
                "scenario": 20,
                "member": "N"
              },
              {
                "seed": 1,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "N"
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 21979,
            "rendering_id": 625381,
            "records": [
              [
                0,
                1
              ],
              [
                4,
                2
              ],
              [
                0,
                4
              ],
              [
                3,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "set_H",
                "scenario": 10,
                "member": "L"
              }
            ],
            "exact_category": 0,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23691,
            "rendering_id": 625445,
            "records": [
              [
                0,
                5
              ],
              [
                4,
                4
              ],
              [
                0,
                4
              ],
              [
                3,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N5",
                "prefix_index": 359,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23233,
            "rendering_id": 626495,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                3
              ],
              [
                1,
                0
              ],
              [
                3,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23822,
            "rendering_id": 627425,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                4
              ],
              [
                1,
                1
              ],
              [
                3,
                5
              ]
            ],
            "sources": [
              {
                "seed": 2,
                "case": "H_N5",
                "prefix_index": 366,
                "round": 5
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23300,
            "rendering_id": 657095,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                3
              ],
              [
                1,
                4
              ],
              [
                4,
                0
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 4
              },
              {
                "seed": 1,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 4
              },
              {
                "seed": 2,
                "case": "L_N3",
                "prefix_index": 196,
                "round": 4
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23065,
            "rendering_id": 670595,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                3
              ],
              [
                4,
                1
              ],
              [
                4,
                0
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 2
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 18523,
            "rendering_id": 678801,
            "records": [
              [
                3,
                3
              ],
              [
                1,
                0
              ],
              [
                0,
                4
              ],
              [
                4,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "neutral_N",
                "scenario": 20,
                "member": "L"
              },
              {
                "seed": 0,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "L"
              },
              {
                "seed": 0,
                "case": "upper_state_exchange_same_N",
                "scenario": 20,
                "member": "L"
              },
              {
                "seed": 1,
                "case": "same_category_substitution",
                "scenario": 20,
                "member": "L"
              }
            ],
            "exact_category": 0,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23301,
            "rendering_id": 684095,
            "records": [
              [
                0,
                5
              ],
              [
                0,
                3
              ],
              [
                1,
                4
              ],
              [
                4,
                1
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "H_N7",
                "prefix_index": 494,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 7440,
            "rendering_id": 745546,
            "records": [
              [
                2,
                4
              ],
              [
                1,
                5
              ],
              [
                3,
                0
              ],
              [
                4,
                3
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N6",
                "prefix_index": 392,
                "round": 1
              }
            ],
            "exact_category": 0,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23383,
            "rendering_id": 760204,
            "records": [
              [
                0,
                4
              ],
              [
                3,
                2
              ],
              [
                0,
                4
              ],
              [
                4,
                4
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N8",
                "prefix_index": 513,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23677,
            "rendering_id": 786771,
            "records": [
              [
                3,
                3
              ],
              [
                0,
                5
              ],
              [
                0,
                4
              ],
              [
                4,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N7",
                "prefix_index": 463,
                "round": 6
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          },
          {
            "board_id": 23358,
            "rendering_id": 787384,
            "records": [
              [
                0,
                4
              ],
              [
                4,
                2
              ],
              [
                0,
                4
              ],
              [
                4,
                5
              ]
            ],
            "sources": [
              {
                "seed": 0,
                "case": "L_N6",
                "prefix_index": 392,
                "round": 3
              }
            ],
            "exact_category": 1,
            "predicted_category": null,
            "outputs_after_L_H": [
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ],
              [
                0.3750000298023224,
                0.25,
                0.3750000298023224
              ]
            ],
            "TV_after_L_H": [
              2.9802322387695312e-08,
              2.9802322387695312e-08
            ]
          }
        ]
      }
    },
    "untrained_errors": 24435
  },
  "futility": {
    "pass": true,
    "sampled_floor_only_change": {
      "prediction_loss_gap_closed": -2.775557561562892e-16,
      "natural_KL_gap_closed": 0.0,
      "initial_excess_prediction_loss": 0.19999999999999996,
      "current_excess_prediction_loss": 0.2,
      "prediction_loss_criterion_available": true,
      "supervised_sums_improved": false,
      "stop": true
    },
    "nonpositive_initial_excess": {
      "prediction_loss_gap_closed": null,
      "natural_KL_gap_closed": 0.0,
      "initial_excess_prediction_loss": 0.0,
      "current_excess_prediction_loss": 0.2,
      "prediction_loss_criterion_available": false,
      "supervised_sums_improved": false,
      "stop": false
    },
    "real_excess_reduction": {
      "prediction_loss_gap_closed": 0.49999999999999983,
      "natural_KL_gap_closed": 0.0,
      "initial_excess_prediction_loss": 0.19999999999999996,
      "current_excess_prediction_loss": 0.1,
      "prediction_loss_criterion_available": true,
      "supervised_sums_improved": false,
      "stop": false
    },
    "supervised_sums_exception": {
      "prediction_loss_gap_closed": -2.775557561562892e-16,
      "natural_KL_gap_closed": 0.0,
      "initial_excess_prediction_loss": 0.19999999999999996,
      "current_excess_prediction_loss": 0.2,
      "prediction_loss_criterion_available": true,
      "supervised_sums_improved": true,
      "stop": false
    }
  },
  "supplier_access": {
    "live": {
      "prediction_gradient_norm": 0.043124452233314514,
      "sums_gradient_norm": 0.06328785419464111,
      "cosine": -0.06876417994499207,
      "prediction_gradient_effect_on_sums": 0.00018767491565085948,
      "sums_gradient_effect_on_prediction": 0.00018767491565085948,
      "live_sums_route_prediction_gradient_norm": 0.0001468420960009098
    },
    "detached": {
      "prediction_gradient_norm": 0.043002840131521225,
      "sums_gradient_norm": 0.06328785419464111,
      "cosine": -0.05616698041558266,
      "prediction_gradient_effect_on_sums": 0.00015286165580619127,
      "sums_gradient_effect_on_prediction": 0.00015286165580619127,
      "live_sums_route_prediction_gradient_norm": 0.0
    }
  },
  "movement": {
    "analytic_maximum_error": 0.0,
    "blocked_decay_displacement": 6.864347233204171e-05
  },
  "details": {
    "path": "build/oldgame_ext/r13_futility_v2_bulk/calibration_details.json",
    "sha256": "89440961e18f63f589598566898d5f5fe8cf944468be501571b55424fcb7b122"
  }
}
