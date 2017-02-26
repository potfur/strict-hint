from strict_hint.strict_hint import StrictHint


def strict(wrapped):
    return StrictHint()(wrapped)
