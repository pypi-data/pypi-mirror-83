from typing import Any, List, Optional


class StepBuilder(object):
    _title: str
    _data: Any

    def __init__(self, title: str):
        super().__init__()
        self._title = title
        self._data = {"type": "blocks", "blocks": []}

    def build(self):
        return {"name": self._title, "action": self._data}

    def set_title(self, title: str):
        self._title = title

    def add_block(self, block):
        self._data["blocks"].append(block)
        return self

    def add_text(self, content: str):
        return self.add_block({"type": "text", "content": content})

    def add_youtube_video(self, videoId: str):
        return self.add_block({"type": "youTubeVideo", "videoId": videoId,})

    def add_web_page(self, url: str):
        return self.add_block({"type": "webPage", "url": url,})

    def add_note(self, text: str):
        return self.add_block({"type": "note", "text": text,})

    def add_exercise_info(self, text: str, reps: str):
        return self.add_block({"type": "exerciseInfo", "title": text, "sets": [{"reps": reps}]})

    def add_timer_countdown(self, text: str, countdownBeforeStart: bool, time: str):
        return self.add_block(
            {
                "type": "timer",
                "title": text,
                "countdownBeforeStart": countdownBeforeStart,
                "mode": {"type": "countdown", "duration": time},
            }
        )

    def add_timer_stopwatch(self, text: str, countdownBeforeStart: bool):
        return self.add_block(
            {
                "type": "timer",
                "title": text,
                "countdownBeforeStart": countdownBeforeStart,
                "mode": {"type": "stopwatch"},
            }
        )

    def add_sensor_field(
        self,
        title: str,
        required: bool = False,
        id: str = None,
        samplingFrequency: int = 100,
        sensorTypes: List[str] = ["gyroscope", "accelerometer"],
    ):
        return self.add_block(
            {
                "type": "sensorField",
                "title": title,
                "required": required,
                "id": id,
                "samplingFrequency": samplingFrequency,
                "sensorTypes": sensorTypes,
            }
        )

    def add_text_field(
        self,
        title: str,
        required: bool = False,
        id: str = None,
        suggestions: Optional[List[str]] = [],
    ):
        return self.add_block(
            {
                "type": "textField",
                "title": title,
                "required": required,
                "id": id,
                "suggestions": suggestions,
            }
        )

    def add_image_field(self, title: str, required: bool = False, id: str = None):
        return self.add_block(
            {"type": "imageField", "title": title, "required": required, "id": id,}
        )

    def add_date_time_field(self, title: str, required: bool = False, id: str = None):
        return self.add_block(
            {"type": "dateTimeField", "title": title, "required": required, "id": id,}
        )

    def add_scale_field(
        self,
        title: str,
        required: bool = False,
        min: int = 0,
        max: int = 10,
        step: int = 1,
        id: str = None,
    ):
        return self.add_block(
            {
                "type": "scaleField",
                "title": title,
                "required": required,
                "id": id,
                "min": min,
                "max": max,
                "step": step,
            }
        )

    def add_multiple_choice_field(
        self, title: str, required: bool = False, choices: list = [], id: str = None
    ):
        return self.add_block(
            {
                "type": "multipleChoiceField",
                "title": title,
                "required": required,
                "id": id,
                "choices": choices,
            }
        )

    def add_number_field(
        self,
        title: str,
        required: bool = False,
        min: int = 0,
        max: int = 10,
        step: int = 1,
        id: str = None,
    ):
        return self.add_block(
            {
                "type": "numberField",
                "title": title,
                "required": required,
                "id": id,
                "min": min,
                "max": max,
                "step": step,
            }
        )
