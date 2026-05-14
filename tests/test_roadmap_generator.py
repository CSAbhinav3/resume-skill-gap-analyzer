import pytest
import json
from app.services.roadmap_generator import parse_roadmap_response


def valid_roadmap_json():
    return json.dumps({
        "target_role": "Data Scientist",
        "overall_match_score": 32.5,
        "phases": [
            {
                "phase": "30_day",
                "goal": "Foundation",
                "weeks": [
                    {"week": 1, "focus": "Python", "topics": [], "resources": [], "goal": "Learn Python"},
                    {"week": 2, "focus": "SQL", "topics": [], "resources": [], "goal": "Learn SQL"},
                    {"week": 3, "focus": "ML", "topics": [], "resources": [], "goal": "Learn ML"},
                    {"week": 4, "focus": "Project", "topics": [], "resources": [], "goal": "Build project"},
                ]
            },
            {
                "phase": "60_day",
                "goal": "Intermediate",
                "weeks": [
                    {"week": 5, "focus": "Docker", "topics": [], "resources": [], "goal": "Learn Docker"},
                    {"week": 6, "focus": "AWS", "topics": [], "resources": [], "goal": "Learn AWS"},
                    {"week": 7, "focus": "MLflow", "topics": [], "resources": [], "goal": "Learn MLflow"},
                    {"week": 8, "focus": "Project", "topics": [], "resources": [], "goal": "Build project"},
                ]
            },
            {
                "phase": "90_day",
                "goal": "Advanced",
                "weeks": [
                    {"week": 9,  "focus": "SVM", "topics": [], "resources": [], "goal": "Learn SVM"},
                    {"week": 10, "focus": "XGBoost", "topics": [], "resources": [], "goal": "Learn XGBoost"},
                    {"week": 11, "focus": "Research", "topics": [], "resources": [], "goal": "Research"},
                    {"week": 12, "focus": "Portfolio", "topics": [], "resources": [], "goal": "Portfolio"},
                ]
            },
        ],
        "weekly_breakdown": [
            {"week": i, "phase": "30_day", "focus": f"Week {i}", "goal": f"Goal {i}"}
            for i in range(1, 13)
        ]
    })


def test_parse_valid_roadmap():
    result = parse_roadmap_response(valid_roadmap_json())
    assert "phases" in result
    assert "weekly_breakdown" in result
    assert len(result["phases"]) == 3


def test_parse_roadmap_with_markdown():
    raw = f"```json\n{valid_roadmap_json()}\n```"
    result = parse_roadmap_response(raw)
    assert len(result["phases"]) == 3


def test_parse_wrong_phase_count_raises():
    data = json.loads(valid_roadmap_json())
    data["phases"] = data["phases"][:2]  # only 2 phases
    with pytest.raises(ValueError, match="3 phases"):
        parse_roadmap_response(json.dumps(data))


def test_parse_missing_phases_key_raises():
    data = {"weekly_breakdown": []}
    with pytest.raises(ValueError, match="missing keys"):
        parse_roadmap_response(json.dumps(data))


def test_parse_invalid_json_raises():
    with pytest.raises(ValueError, match="invalid JSON"):
        parse_roadmap_response("not json")