import json
import unittest
from pathlib import Path

from src.prediction import (
    load_model_bundle,
    predict_stress,
    validate_student_input,
)


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "stress_risk_pipeline.joblib"
METADATA_PATH = ROOT / "models" / "stress_risk_model_metadata.json"


class PredictionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model, cls.metadata = load_model_bundle(MODEL_PATH, METADATA_PATH)
        cls.valid_input = {
            feature: schema["allowed_values"][len(schema["allowed_values"]) // 2]
            for feature, schema in cls.metadata["input_schema"].items()
        }

    def test_valid_prediction(self):
        result = predict_stress(self.valid_input, self.model, self.metadata)
        self.assertIn(result["predicted_label"], {"Low", "Medium", "High"})
        self.assertAlmostEqual(sum(result["probabilities"].values()), 1.0)

    def test_output_order_matches_metadata(self):
        model_input = validate_student_input(self.valid_input, self.metadata)
        self.assertEqual(
            list(model_input.columns),
            self.metadata["features_in_order"],
        )

    def test_missing_answer_is_rejected(self):
        invalid = dict(self.valid_input)
        invalid.pop("safety")
        with self.assertRaisesRegex(ValueError, "Missing answers"):
            validate_student_input(invalid, self.metadata)

    def test_out_of_range_answer_is_rejected(self):
        invalid = {**self.valid_input, "study_load": 20}
        with self.assertRaisesRegex(ValueError, "study_load must be one of"):
            validate_student_input(invalid, self.metadata)

    def test_non_integer_answer_is_rejected(self):
        invalid = {**self.valid_input, "bullying": 2.5}
        with self.assertRaisesRegex(ValueError, "finite integer code"):
            validate_student_input(invalid, self.metadata)

    def test_model_metadata_is_non_diagnostic(self):
        metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
        boundaries = " ".join(metadata["use_boundaries"]).lower()
        self.assertIn("not a diagnostic", boundaries)


if __name__ == "__main__":
    unittest.main()
