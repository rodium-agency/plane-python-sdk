from plane.models.projects import Project, UpdateProject
from plane.models.work_items import WorkItemStateDurations


def test_update_project_sends_only_the_state_time_fields_that_were_set():
    payload = UpdateProject(
        state_time_tracking=False,
        state_time_start="10:00:00",
        state_time_days=[0, 2, 4],
    ).model_dump(exclude_none=True)

    assert payload["state_time_tracking"] is False
    assert payload["state_time_start"] == "10:00:00"
    assert payload["state_time_days"] == [0, 2, 4]
    assert "state_time_end" not in payload
    assert "name" not in payload


def test_project_response_keeps_the_schedule():
    project = Project.model_validate(
        {
            "name": "Trofy",
            "identifier": "TROFY",
            "state_time_tracking": True,
            "state_time_start": "09:00:00",
            "state_time_end": "17:00:00",
            "state_time_days": [0, 1, 2, 3, 4],
        }
    )

    assert project.state_time_tracking is True
    assert project.state_time_days == [0, 1, 2, 3, 4]


def test_state_durations_response():
    body = WorkItemStateDurations.model_validate(
        {
            "enabled": True,
            "timezone": "Europe/Paris",
            "start": "09:00:00",
            "end": "17:00:00",
            "days": [0, 1, 2, 3, 4],
            "transitions": [
                {
                    "id": "activity-1",
                    "created_at": "2026-10-05T09:10:00Z",
                    "old_state": {"id": "doing", "name": "En cours"},
                    "new_state": {"id": "review", "name": "Revue en cours"},
                    "duration_seconds": 600,
                    "label": "10 min",
                }
            ],
        }
    )

    assert body.enabled is True
    assert body.transitions[0].duration_seconds == 600
    assert body.transitions[0].label == "10 min"
