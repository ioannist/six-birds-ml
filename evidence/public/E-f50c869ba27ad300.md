# r13 calibration

{
  "registration_sha256": "d52dd68a0df32dac9cbeaa74adda2549a149f1af0e7629d5883d571a3615114c",
  "device": "cpu",
  "checks": {
    "B": true,
    "sums": true,
    "probes": true,
    "movement": true,
    "geometry": false,
    "diagnosis": true,
    "supplier_access": true
  },
  "elapsed_seconds": 129.06857213797048,
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
  "geometry": {
    "pass": false,
    "readers": {
      "numerical": {
        "accuracy": 1.0,
        "correct": 72,
        "total": 72,
        "converged": true
      },
      "numerical_permuted": {
        "accuracy": 1.0,
        "correct": 72,
        "total": 72,
        "converged": true
      },
      "onehot": {
        "accuracy": 1.0,
        "correct": 72,
        "total": 72,
        "converged": true
      },
      "onehot_permuted": {
        "accuracy": 0.5555555555555556,
        "correct": 40,
        "total": 72,
        "converged": true
      }
    },
    "conclusion": "BLOCKED_FAILED_NEGATIVE; fixed labels retained, no resampling"
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
    "path": "build/oldgame_ext/r13_calibration_final_bytes/calibration_details.json",
    "sha256": "3fd3b7b3494d149d611e1083c49d4a61c0a4205d0c8cc4c91a1a281e11e6fef7"
  }
}
