class DiceRenderer:
    DICE_EMOJIS = {
        1: "⚀",
        2: "⚁",
        3: "⚂",
        4: "⚃",
        5: "⚄",
        6: "⚅"
    }

    @staticmethod
    def render(dice_value):
        return DiceRenderer.DICE_EMOJIS.get(dice_value, "?")
