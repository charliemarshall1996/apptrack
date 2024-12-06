
class ChoiceBase:
    @classmethod
    def choices(cls):
        # Filter attributes that are tuples of length 2 (value and label)
        return [
            (value[0], value[1])
            for value in cls.__dict__.values()
            if isinstance(value, tuple) and len(value) == 2
        ]


class ReminderUnitChoices(ChoiceBase):
    DAYS = "d", "Days"
    HOURS = "h", "Hours"
    MINUTES = "m", "Minutes"
